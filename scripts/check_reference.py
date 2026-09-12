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

# 魔女傳說庫的 schema
WITCH_FIELDS = [
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

# 參考作品庫的 schema。地區／語系／時代三軸對動畫作品沒有意義，
# 改記年份與原作型態。
WORKS_FIELDS = [
    "id",
    "title_zh",
    "title_native",
    "year",
    "origin",
    "source",
]

# 依 repo 相對路徑前綴分流。兩個子庫的 frontmatter schema 不同，
# 用同一份必填清單會讓其中一邊永遠失敗。
SCHEMAS = [
    ("reference/works/entries/", WORKS_FIELDS),
    ("reference/regions/", WITCH_FIELDS),
    ("reference/sources-and-law/", WITCH_FIELDS),
    ("reference/concepts/", WITCH_FIELDS),
]


def schema_for(rel):
    """依條目的 repo 相對路徑取得必填欄位；索引與說明檔回傳 None（只檢查文字規範）。"""
    for prefix, fields in SCHEMAS:
        if rel.startswith(prefix):
            return fields
    return None

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


# works 子庫（reference/works/entries/）frontmatter 的這些頂層欄位，值恆為
# 日文原文（片名、羅馬拼音、製作公司、幕後人員姓名）；title_zh、origin、
# pact_mapping、tags 等頂層欄位承載的才是中文，仍須檢查，不列在這裡。
#
# 這批豁免只對 works 子庫的 schema 成立，不能單靠 cjk_entry 判斷：魔女傳說庫
# 的同名欄位（title_native、frontmatter 縮排欄位如 fallback_reason）在
# language: zh 或中文論述的條目下本來就是繁體中文，若不分 schema 一律豁免，
# 會讓魔女庫裡誤植的簡體字（例如西王母條目 title_native、富士山條目
# fallback_reason 裡的簡體字）悄悄通過檢查而不被發現。schema_for() 已經用路徑前綴
# 分辨兩個子庫，這裡直接沿用其結果（is_works_entry），不再另立一套判斷路徑的
# 邏輯，以免兩套邏輯將來各自修改而彼此不同步。
FRONTMATTER_NATIVE_KEYS = ("title_native", "title_romanized", "studio", "key_staff")


def simplified_targets(line, cjk_entry, in_frontmatter=False, is_works_entry=False):
    """回傳這一行需要做簡體字判定的文字片段。

    東亞條目的原文會出現在三個地方：章節標題、專有名詞對照表的前兩欄、
    以及行文中以〈〉《》「」框住的條目名與書名。這些都要排除，
    否則條目會被逼著去改動原文以通過檢查。

    works 子庫的 frontmatter 還有一批原文，且不一定含假名可觸發既有的
    NATIVE_SCRIPT 豁免——例如 title_native 純漢字寫成「魔法少女育成計画」，
    「画」在簡體字表內卻沒有假名同行。縮排的巢狀欄位（key_staff 底下的
    角色／姓名、source 底下 extra[].title／publisher 等）同樣是日文原文，
    一併豁免；否則條目會被逼著竄改日文原文的字形才能通過檢查。

    這批豁免僅限 is_works_entry（reference/works/entries/ 底下的條目）；
    魔女傳說庫即使 cjk_entry 為真，frontmatter 同名欄位仍可能是中文，必須
    繼續檢查。
    """
    if not cjk_entry:
        return [line]
    if line.lstrip().startswith("#"):
        return []
    if in_frontmatter and is_works_entry:
        if line[:1] in (" ", "\t"):
            return []
        key = line.strip().split(":", 1)[0].strip()
        if key in FRONTMATTER_NATIVE_KEYS:
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


def check(path, required):
    problems = []
    with io.open(path, encoding="utf-8") as f:
        text = f.read()

    # required 就是 schema_for(rel) 的回傳值；直接用它辨認 works 子庫，
    # 不再另外用路徑字串比對一次——兩套判斷邏輯分岔的話，其中一套改了
    # 另一套沒改，這種分歧會很隱蔽。
    is_works_entry = required is WORKS_FIELDS

    if required is not None:
        fm = frontmatter_of(text)
        if fm is None:
            problems.append("缺少 YAML frontmatter")
        else:
            for field in required:
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
    fm_text = frontmatter_of(text) or ""
    cjk_entry = generated or bool(
        re.search(r"^language:\s*[\"']?(ja|zh|ko)[\"']?\s*$", fm_text, re.M)
        # works 子庫的 schema 沒有頂層 language，語言記在 source.wiki_lang。
        # 不認這個欄位的話，日文原文中不含假名的純漢字（章節標題的「制作」、
        # 名詞對照表的「体」「声」「実」）會被誤判為簡體字，逼得條目去改動原文
        # 以通過檢查——魔女庫第三批踩過這個坑。
        or re.search(r"^\s+wiki_lang:\s*[\"']?(ja|zh|ko)[\"']?\s*$", fm_text, re.M))

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
            bad = sorted({ch for seg in simplified_targets(
                              line, cjk_entry, lineno <= fm_end, is_works_entry)
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
        # 索引與說明檔沒有 frontmatter，schema_for 回傳 None，只檢查文字規範
        problems = check(path, schema_for(rel))
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
