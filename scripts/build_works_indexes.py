#!/usr/bin/env python
"""由 reference/works/ 各條目的 frontmatter 產生索引與名詞總表。

產生：
    reference/works/INDEX.md                 主索引（依年代）
    reference/works/indexes/by-pact.md       盟約對應交叉索引
    reference/works/indexes/by-origin.md     原作型態交叉索引
    reference/works/name-glossary.md         原文專有名詞對照總表

用法：
    .venv/Scripts/python.exe scripts/build_works_indexes.py
"""

from __future__ import annotations

import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from build_reference_indexes import (  # noqa: E402
    group,
    parse_frontmatter,
    parse_glossary,
    write,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKS = os.path.join(ROOT, "reference", "works")
ENTRIES = os.path.join(WORKS, "entries")

# 依年代分組。規則書的參考清單橫跨 1991—2018，三個十年各有明顯的類型轉向。
DECADES = [
    ("1990", "九〇年代（1991—1999）", lambda y: 1990 <= y < 2000),
    ("2000", "二〇〇〇年代（2000—2009）", lambda y: 2000 <= y < 2010),
    ("2010", "二〇一〇年代（2010—2019）", lambda y: 2010 <= y < 2020),
]

# 規則書 pacts.md 明寫對應的才有值，其餘歸「規則書未指定」。
PACT_ORDER = ["光明子女", "正義騎士", "契約傀儡"]
PACT_UNSPECIFIED = "規則書未指定"

ORIGIN_ORDER = ["原創動畫", "漫畫改編", "輕小說改編", "遊戲改編", "玩具企劃"]


def collect_works():
    entries = []
    if not os.path.isdir(ENTRIES):
        return entries
    for fn in sorted(os.listdir(ENTRIES)):
        if not fn.endswith(".md"):
            continue
        path = os.path.join(ENTRIES, fn)
        with io.open(path, encoding="utf-8") as f:
            text = f.read()
        fm = parse_frontmatter(text)
        if not fm.get("id"):
            continue
        fm["_path"] = "entries/" + fn
        fm["_glossary"] = parse_glossary(text)
        entries.append(fm)
    entries.sort(key=lambda e: (int(e.get("year") or 0), e["id"]))
    return entries


def link(entry, from_dir=""):
    prefix = "../" if from_dir else ""
    return "[%s](%s%s)" % (entry.get("title_zh") or entry["id"],
                           prefix, entry["_path"])


def table(entries, from_dir=""):
    head = ["作品", "日文原名", "年", "原作型態", "盟約對應"]
    out = ["| %s |" % " | ".join(head),
           "| %s |" % " | ".join(["---"] * len(head))]
    for e in entries:
        out.append("| %s |" % " | ".join([
            link(e, from_dir),
            e.get("title_native") or "",
            str(e.get("year") or ""),
            e.get("origin") or "",
            e.get("pact_mapping") or "—",
        ]))
    return "\n".join(out)


def build_main_index(entries):
    parts = [
        "# 參考作品分析資料庫 主索引",
        "",
        "依年代分類。交叉索引見 [盟約對應索引](indexes/by-pact.md) 與 "
        "[原作型態索引](indexes/by-origin.md)；原文名詞對照見 "
        "[名詞總表](name-glossary.md)。",
        "",
        "共收錄 %d 部。" % len(entries),
        "",
    ]
    for _key, label, pred in DECADES:
        items = [e for e in entries if pred(int(e.get("year") or 0))]
        if not items:
            continue
        parts.append("## %s（%d 部）" % (label, len(items)))
        parts.append("")
        parts.append(table(items))
        parts.append("")
    return "\n".join(parts)


def build_pact_index(entries):
    parts = [
        "# 盟約對應交叉索引",
        "",
        "依規則書 `docs/src/content/docs/rules/pacts.md` **明寫**的對應分類。"
        "規則書未指定者歸入「規則書未指定」，不自行歸類。"
        "回到 [主索引](../INDEX.md)。",
        "",
    ]
    by_pact = group(entries, lambda e: e.get("pact_mapping") or PACT_UNSPECIFIED)
    # 未列在 PACT_ORDER、也不是 PACT_UNSPECIFIED 的值（例如 pact_mapping 誤植）
    # 仍附加在後面列出，而不是被直接漏掉——沒有任何腳本會驗證 pact_mapping
    # 的值是否合法，漏掉的話條目會從索引裡不聲不響地消失。
    ordered = [p for p in PACT_ORDER + [PACT_UNSPECIFIED] if p in by_pact]
    ordered += [p for p in sorted(by_pact) if p not in ordered]
    for pact in ordered:
        items = by_pact[pact]
        parts.append("## %s（%d 部）" % (pact, len(items)))
        parts.append("")
        parts.append(table(items, from_dir="indexes"))
        parts.append("")
    return "\n".join(parts)


def build_origin_index(entries):
    parts = [
        "# 原作型態交叉索引",
        "",
        "依作品的原作媒體分類。回到 [主索引](../INDEX.md)。",
        "",
    ]
    by_origin = group(entries, lambda e: e.get("origin") or "未標註")
    ordered = [o for o in ORIGIN_ORDER if o in by_origin]
    ordered += [o for o in sorted(by_origin) if o not in ORIGIN_ORDER]
    for origin in ordered:
        items = by_origin[origin]
        parts.append("## %s（%d 部）" % (origin, len(items)))
        parts.append("")
        parts.append(table(items, from_dir="indexes"))
        parts.append("")
    return "\n".join(parts)


def build_glossary(entries):
    parts = [
        "# 原文專有名詞對照總表",
        "",
        "彙整各條目「專有名詞對照」一節的內容，依年代排列。"
        "本表僅供本子庫使用，與魔女傳說庫的名詞總表、遊戲規則術語庫 "
        "`glossary.json` 三者各自獨立。回到 [主索引](INDEX.md)。",
        "",
    ]
    total = 0
    for e in entries:
        rows = e["_glossary"]
        if not rows:
            continue
        parts.append("## %s" % link(e))
        parts.append("")
        parts.append("| 原文 | 羅馬轉寫 | 繁體中文 | 說明 |")
        parts.append("| --- | --- | --- | --- |")
        for cells in rows:
            cells = (cells + ["", "", "", ""])[:4]
            parts.append("| %s |" % " | ".join(cells))
            total += 1
        parts.append("")
    parts.insert(4, "共 %d 條名詞。\n" % total)
    return "\n".join(parts)


def main():
    entries = collect_works()
    if not entries:
        print("reference/works/entries/ 底下找不到任何含 frontmatter 的條目。")
        return 1
    write(os.path.join(WORKS, "INDEX.md"), build_main_index(entries))
    write(os.path.join(WORKS, "indexes", "by-pact.md"), build_pact_index(entries))
    write(os.path.join(WORKS, "indexes", "by-origin.md"), build_origin_index(entries))
    write(os.path.join(WORKS, "name-glossary.md"), build_glossary(entries))
    print("\n共處理 %d 部作品。" % len(entries))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
