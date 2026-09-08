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
# 假名（含片假名中點）與諺文。含這些字元的行屬日、韓文原文（章節標題、對照表等），
# 其中的日語新字體漢字（会、来、実、体……）並非簡體中文，故不作簡體字判定。
NATIVE_SCRIPT = re.compile(r"[぀-ヿᄀ-ᇿ가-힯]")


def iter_files(paths):
    for p in paths:
        if os.path.isdir(p):
            for dirpath, _dirnames, filenames in os.walk(p):
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

    lines = text.splitlines()
    # frontmatter 用 YAML 語法，半形逗號屬正常，不納入標點檢查
    fm_end = 0
    if lines and lines[0] == "---":
        for i, line in enumerate(lines[1:], 1):
            if line == "---":
                fm_end = i
                break

    for lineno, line in enumerate(lines, 1):
        is_quote = line.lstrip().startswith(">")
        # 原文引用行與日、韓文原文行逐字保留，不做簡體字判定
        if not (is_quote or NATIVE_SCRIPT.search(line)):
            bad = sorted({ch for ch in line if ch in SIMPLIFIED})
            if bad:
                problems.append("第 %d 行出現簡體字：%s" % (lineno, "、".join(bad)))
        if lineno <= fm_end or is_quote:
            # frontmatter 與原文引用逐字保留，不檢查標點
            continue
        if HALFWIDTH_AFTER_CJK.search(line):
            problems.append("第 %d 行中文後接半形標點" % lineno)
        if TRIPLE_DOT.search(line):
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
        is_entry = "/regions/" in rel or "/sources-and-law/" in rel
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
