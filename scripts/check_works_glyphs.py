#!/usr/bin/env python
"""檢查 reference/works/entries/ 底下條目是否違反裁決 B。

裁決 B：日文專有名詞譯入中文行文時，須改用繁體中文字形——引文中的「虚淵玄」，
到了中文行文要寫成「虛淵玄」；裁決 I 的例外是保留不譯的原題，整段用『』包住，
照抄日文原題的字形。

scripts/check_reference.py 的簡體字偵測對含假名（或諺文）的整行豁免，理由是東亞
條目常見「片假名詞＋日語新字體漢字」混寫的原文，硬要逐字比對簡體字表會誤傷這類
原文。但這個豁免範圍太寬：一行只要混了假名，就連其中未轉換的日文漢字（例如
「読売テレビ」裡的「読」「売」）也一併放行——這兩個字未必落在簡體字表裡，
check_reference.py 因此對這類違規結構性地看不見。

裁決 B 的違規因此不能靠字表比對，只能靠條目自己的「專有名詞對照」表：表裡
「繁體中文」欄與「原文」欄不同，就代表這個詞的中文行文寫法已經欽定；若行文中
仍找得到「原文」欄的逐字寫法，就是把原文字形帶進了中文行文，違反裁決 B。

用法：
    .venv/Scripts/python.exe scripts/check_works_glyphs.py [路徑...]
未給路徑時預設檢查 reference/works/entries/ 底下所有 .md。
"""

from __future__ import annotations

import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DEFAULT_DIR = os.path.join(ROOT, "reference", "works", "entries")

GLOSSARY_HEADING = "## 專有名詞對照"
SOURCE_HEADING = "## 來源與授權"

# URL 裡的原文（wiki 連結、原文標題的網址編碼）不是行文，逐字保留；否則條目會被
# 逼著把來源網址也改寫過，反而更難讀。
URL_RE = re.compile(r"https?://\S+")

# 條目慣用四種括號引用原文，各自對應不同的「這是原文，不是中文行文」場合：
# 『』（裁決 I 保留不譯的完整作品原題）、「」（歌曲／單行本篇名，或逐字引述原文
# 語句）、〈〉（維基條目的節／小節標題、單篇文章名）、《》（作品的外文別名或
# 外語電影原名，如日本上映片名）。四種都是「引用原文本身」而非「行文中誤用原文
# 字形」，裁決 B 不適用；否則像〈セフィーロ（裏）〉這種逐字引用維基小節標題的
# 寫法，會被逼著去竄改標題原文才能通過檢查。
BRACKET_PAIRS = (("『", "』"), ("「", "」"), ("〈", "〉"), ("《", "》"))


def iter_files(paths):
    for p in paths:
        if os.path.isdir(p):
            for dirpath, _dirnames, filenames in os.walk(p):
                for fn in sorted(filenames):
                    if fn.endswith(".md"):
                        yield os.path.join(dirpath, fn)
        elif p.endswith(".md"):
            yield p


def frontmatter_end(lines):
    """回傳 frontmatter 結尾那一行（第二個 ---）的行號；沒有 frontmatter 則回傳 0。"""
    if not lines or lines[0] != "---":
        return 0
    for i, line in enumerate(lines[1:], 2):
        if line == "---":
            return i
    return 0


def glossary_rows_and_span(lines):
    """解析『專有名詞對照』表格。

    回傳 (rows, table_lines)：
    - rows 是 [(原文, 繁體中文, 行號)]，只收「繁體中文」與「原文」不同的資料列——
      兩欄相同代表本庫刻意沿用原文（未查得官方繁中名等情形），不受裁決 B 規範。
    - table_lines 是表格本身（標題列、分隔列、資料列）占用的行號集合；這些行是
      名詞表自己的內容，不是中文行文，找原文形時要整段排除，否則名詞表的原文欄
      與說明欄裡的原文寫法會被自己的規則誤判成違規。

    標題列與分隔列固定緊接在標題之後、各占一列，用列序判斷比逐格比對文字內容
    更穩定——說明欄未來若寫進「---」之類的字樣，逐字比對會誤判。
    """
    rows = []
    table_lines = set()
    state = "before"  # before -> header -> sep -> data
    for lineno, line in enumerate(lines, 1):
        if line.strip() == GLOSSARY_HEADING:
            state = "header"
            continue
        if state == "before":
            continue
        if line.startswith("## "):
            break
        stripped = line.strip()
        if not (stripped.startswith("|") and stripped.endswith("|")):
            continue
        table_lines.add(lineno)
        if state == "header":
            state = "sep"
            continue
        if state == "sep":
            state = "data"
            continue
        cells = [c.strip() for c in stripped[1:-1].split("|")]
        if len(cells) < 3:
            continue
        yuan, zh = cells[0], cells[2]
        if yuan and zh and yuan != zh:
            rows.append((yuan, zh, lineno))
    return rows, table_lines


def source_section_span(lines):
    """回傳『來源與授權』整節占用的行號集合。

    這節逐條列出日文來源條目名、發行者與媒體名稱，是來源的原文引用，不是條目
    自己的行文；裁決 B 若套用在這裡，條目會被逼著把引用來源的標題也改寫成繁體
    字形，等於竄改引用內容。
    """
    span = set()
    in_section = False
    for lineno, line in enumerate(lines, 1):
        if line.strip() == SOURCE_HEADING:
            in_section = True
            span.add(lineno)
            continue
        if in_section:
            if line.startswith("## "):
                break
            span.add(lineno)
    return span


def strip_bracket_pair(text, open_ch, close_ch):
    """移除 text 中一組括號（含巢狀）包住的內容，只留括號外的文字。

    不能用 re.compile(r"開[^閉]*閉") 一次解決：這類正規式不辨識巢狀，遇到
    「「甲「乙」丙」」這種同種括號自我巢狀的引文（例如逐字引用一段本身就包含
    引號的日文句子），會在最內層的收尾括號就把比對截斷，外層括號剩下的原文
    反而落回受檢範圍——與 check_reference.py 頭部註解描述的〈「…」〉跨括號巢狀
    是同一類問題，這裡改用逐字掃描、以深度計數來處理同種括號自我巢狀的情形。
    """
    out = []
    depth = 0
    for ch in text:
        if ch == open_ch:
            depth += 1
            continue
        if ch == close_ch:
            if depth > 0:
                depth -= 1
                continue
        if depth == 0:
            out.append(ch)
    return "".join(out)


def strip_gloss_parens(line, rows):
    """剝除「先寫繁中譯名、括號裡緊接著補一次原文」的雙語註記寫法。

    例如「世界系」（セカイ系）、《東京喵喵 NEW ～♡》（東京ミュウミュウ にゅ〜♡）：
    行文已經先用了名詞表欽定的繁中形式，括號裡的原文只是附註出處方便讀者對照，
    不是拿原文取代繁中譯名，不算裁決 B 違規。只在括號內容整段、去頭尾空白後
    恰好等於某一列的「原文」欄時才剝除——範圍限制得夠窄，才不會連「柱」被
    「原文……等」這類真正夾帶原文說明的括號一併放行。
    """
    for yuan, _zh, _row_lineno in rows:
        if not yuan:
            continue
        for open_ch, close_ch in (("（", "）"), ("(", ")")):
            line = line.replace(open_ch + yuan + close_ch, "")
    return line


def prose_text(line, rows):
    """回傳這一行用於裁決 B 判定的行文片段。

    依序做三件事：
    1. 先精確剝除「這一列的繁體中文欄位」逐字出現之處。這一步不能省：有些列的
       繁體中文本身就以原文為詞根、只是加了字或換了括號（例如「柱」→「支柱」、
       「セフィーロ」在正文一律譯「瑟菲羅」），若不先扣掉正確寫法，「支柱」會
       因為尾字是「柱」而被自己的規則誤判成用了原文形「柱」。
    2. 剝除「繁中譯名（原文附註）」這種雙語註記括號，見 strip_gloss_parens。
    3. 再剝除『』「」〈〉《》四種括號引用的原文（見 BRACKET_PAIRS 上方說明）。
    """
    line = URL_RE.sub("", line)
    for yuan, zh, _row_lineno in rows:
        if zh:
            line = line.replace(zh, "")
    line = strip_gloss_parens(line, rows)
    for open_ch, close_ch in BRACKET_PAIRS:
        line = strip_bracket_pair(line, open_ch, close_ch)
    return line


def check(path, rel):
    problems = []
    with io.open(path, encoding="utf-8") as f:
        text = f.read()
    lines = text.splitlines()

    fm_end = frontmatter_end(lines)
    rows, table_lines = glossary_rows_and_span(lines)
    source_lines = source_section_span(lines)

    if not rows:
        return problems

    in_code = False
    for lineno, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            # 程式碼區塊多半是 YAML／指令示例，不是中文行文
            continue
        if lineno <= fm_end:
            # frontmatter 的原文欄位（title_native、key_staff 等）本來就該是原文
            continue
        if lineno in table_lines or lineno in source_lines:
            continue
        if line.lstrip().startswith(">"):
            # 原文引用逐字保留，本來就該是原文字形
            continue
        seg = prose_text(line, rows)
        for yuan, zh, _row_lineno in rows:
            if yuan in seg:
                problems.append(
                    "%s:%d 名詞表作「%s」，但此處用了原文形「%s」"
                    % (rel, lineno, zh, yuan)
                )
    return problems


def main():
    paths = sys.argv[1:] or [DEFAULT_DIR]
    total = 0
    failed = 0
    for path in iter_files(paths):
        total += 1
        rel = os.path.relpath(path, ROOT).replace("\\", "/")
        problems = check(path, rel)
        if problems:
            failed += 1
            print("FAIL %s" % rel)
            for p in problems:
                print("     - %s" % p)
        else:
            print("ok   %s" % rel)
    print("\n共檢查 %d 個檔案，%d 個有問題。" % (total, failed))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
