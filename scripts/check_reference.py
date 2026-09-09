#!/usr/bin/env python
"""驗證 reference/ 底下的魔女傳說條目是否符合專案規範。

檢查項目：
1. 簡體字（字表見 scripts/simplified_chars.txt）
   ——原文引用行（以 > 開頭）與含假名／諺文的日、韓文原文行不納入判定，
     因為日語新字體漢字與簡體中文字形相同者甚多，屬原文逐字保留的範圍。
2. 中文語境中誤用的半形標點（, ; ? !）
3. 三點省略號 ... （應使用 ……）
4. frontmatter 必填欄位

用法：
    .venv/Scripts/python.exe scripts/check_reference.py [路徑...]
未給路徑時預設檢查 reference/ 底下所有 .md。
"""

from __future__ import annotations

import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DEFAULT_DIR = os.path.join(ROOT, "reference")
SIMPLIFIED_TABLE = os.path.join(HERE, "simplified_chars.txt")


def load_simplified():
    chars = set()
    with io.open(SIMPLIFIED_TABLE, encoding="utf-8") as f:
        for line in f:
            if line.startswith("#"):
                continue
            chars.update(line.strip())
    return chars


SIMPLIFIED = load_simplified()

REQUIRED_FIELDS = [
    "id",
    "title_zh",
    "title_native",
    "region",
    "language",
    "language_family",
    "era",
    "era_bucket",
    "type",
]

# 中文字元後面接半形標點（英數字後的半形標點屬正常用法）
HALFWIDTH_AFTER_CJK = re.compile(r"[一-鿿][,;?!]")
TRIPLE_DOT = re.compile(r"(?<!\.)\.\.\.(?!\.)")
# 被括號或引號包住的省略記號是引文節略的學術慣例，或是在說明原文長什麼樣子，
# 都不是中文行文中誤用的省略號，檢查前先移除。
BRACKETED_DOTS = re.compile(r"[\(\[（〔「『<]\s*\.\.\.\s*[\)\]）〕」』>]")
# 假名（含片假名中點）與諺文。含這些字元的行屬日、韓文原文（章節標題、對照表等），
# 其中的日語新字體漢字（会、来、実、体……）並非簡體中文，故不作簡體字判定。
NATIVE_SCRIPT = re.compile(r"[぀-ヿᄀ-ᇿ가-힯]")
# 〈條目名〉《書名》「原文詞」內的內容是原文引用，東亞條目中常是純漢字的日文詞，
# 其新字體與簡體字形相同，檢查前先移除。
QUOTED_NATIVE = re.compile(r"[〈《「『]([^〉》」』]*)[〉》」』]")


def simplified_targets(line, cjk_entry):
    """回傳這一行需要做簡體字判定的文字片段。

    東亞條目的原文會出現在三個地方：章節標題、專有名詞對照表的前兩欄、
    以及行文中以〈〉《》「」框住的條目名與書名。這些都要排除，
    否則條目會被逼著去改動原文以通過檢查。
    """
    if not cjk_entry:
        return [line]
    if line.lstrip().startswith("#"):
        return []
    # URL 內的原文標題不是行文，逐字保留；否則條目會被逼著把來源網址改成
    # 百分比編碼才能通過檢查，反而更難讀。
    line = re.sub(r"https?://\S+", "", line)
    stripped = line.strip()
    if stripped.startswith("|") and stripped.endswith("|"):
        cells = [c for c in stripped[1:-1].split("|")]
        # 表格前兩欄是「原文」與「羅馬轉寫」，其餘（繁體中文、說明）仍要檢查
        return [QUOTED_NATIVE.sub("", c) for c in cells[2:]]
    return [QUOTED_NATIVE.sub("", line)]


# backlog/ 底下是機器掃描產生的外語條目標題清單，不適用中文書寫規範
SKIP_DIRS = ("backlog",)


def iter_files(paths):
    for p in paths:
        if os.path.isdir(p):
            for dirpath, _dirnames, filenames in os.walk(p):
                if os.path.basename(dirpath) in SKIP_DIRS:
                    continue
                for fn in sorted(filenames):
                    if fn.endswith(".md"):
                        yield os.path.join(dirpath, fn)
        elif p.endswith(".md"):
            yield p


def frontmatter_of(text):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    return text[4:end]


def check(path, is_entry):
    problems = []
    with io.open(path, encoding="utf-8") as f:
        text = f.read()

    if is_entry:
        fm = frontmatter_of(text)
        if fm is None:
            problems.append("缺少 YAML frontmatter")
        else:
            for field in REQUIRED_FIELDS:
                if not re.search(r"^%s:" % re.escape(field), fm, re.M):
                    problems.append("frontmatter 缺少欄位：%s" % field)
            if not re.search(r"^\s*retrieved:\s*\S", fm, re.M):
                problems.append("frontmatter 缺少 source.retrieved 擷取日期")

    # 東亞條目的章節標題採「原文章節名（繁中章節名）」體例，原文部分可能是純漢字
    # （脚注、参考文献、関連項目），其中的日語新字體與簡體字形相同。含假名／諺文的
    # 行已由 NATIVE_SCRIPT 排除，純漢字標題則靠這裡的語言判斷排除——否則會逼得
    # 條目為了通過檢查去改動標題結構，變成檢查器在扭曲內容。
    # INDEX.md、indexes/、name-glossary.md 由腳本彙整各條目產生，整份都是各語言的
    # 原文標題與名詞，同樣適用原文豁免。
    generated = os.path.basename(path) in ("INDEX.md", "name-glossary.md") or         os.path.basename(os.path.dirname(path)) == "indexes"
    cjk_entry = generated or bool(
        re.search(r"^language:\s*[\"']?(ja|zh|ko)[\"']?\s*$",
                  frontmatter_of(text) or "", re.M))

    lines = text.splitlines()
    # frontmatter 用 YAML 語法，半形逗號屬正常，不納入標點檢查
    fm_end = 0
    if lines and lines[0] == "---":
        for i, line in enumerate(lines[1:], 1):
            if line == "---":
                fm_end = i
                break

    in_code = False
    for lineno, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        is_quote = line.lstrip().startswith(">")
        if not (is_quote or NATIVE_SCRIPT.search(line)):
            bad = sorted({ch for seg in simplified_targets(line, cjk_entry)
                          for ch in seg if ch in SIMPLIFIED})
            if bad:
                problems.append("第 %d 行出現簡體字：%s" % (lineno, "、".join(bad)))
        if lineno <= fm_end or is_quote:
            # frontmatter 與原文引用逐字保留，不檢查標點
            continue
        # 程式碼區塊裡多半是 YAML／指令，半形標點屬正常
        if not in_code and HALFWIDTH_AFTER_CJK.search(line):
            problems.append("第 %d 行中文後接半形標點" % lineno)
        # 程式碼區塊與行內程式碼裡的 ... 是用法示例或原文標記，不是中文省略號
        checked = BRACKETED_DOTS.sub("", re.sub(r"`[^`]*`", "", line))
        if not in_code and TRIPLE_DOT.search(checked):
            problems.append("第 %d 行使用了 ... （應為 ……）" % lineno)

    return problems


def main():
    paths = sys.argv[1:] or [DEFAULT_DIR]
    total = 0
    failed = 0
    for path in iter_files(paths):
        total += 1
        rel = os.path.relpath(path, ROOT).replace("\\", "/")
        # 索引與說明檔沒有 frontmatter，只檢查文字規範
        is_entry = (
            "/regions/" in rel
            or "/sources-and-law/" in rel
            or "/concepts/" in rel
        )
        problems = check(path, is_entry)
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
