#!/usr/bin/env python
"""由 reference/ 各條目的 frontmatter 產生索引與名詞總表。

產生：
    reference/INDEX.md                     主索引（依地區）
    reference/indexes/by-language-family.md 語系交叉索引
    reference/indexes/by-era.md             時代交叉索引
    reference/name-glossary.md              原文專有名詞對照總表

用法：
    .venv/Scripts/python.exe scripts/build_reference_indexes.py
"""

from __future__ import annotations

import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(ROOT, "reference")

ERA_LABELS = [
    ("ancient", "上古（至西元 500 年前後）"),
    ("medieval", "中世紀（約 500—1450）"),
    ("early-modern", "近世獵巫盛期（約 1450—1750）"),
    ("modern", "近現代（1750 年之後）"),
]

TYPE_LABELS = {
    "folklore": "民俗／神話",
    "trial": "審判事件",
    "person": "人物",
    "text-law": "文獻與法制",
}

# 各條目的 language_family 寫法詳略不一（「原典為印歐語系……」「孤立語言（巴斯克語，
# 不屬印歐語系）」等），直接拿字串分組會生出假群組。改以下列關鍵字正規化成語系層級，
# 取字串中最先出現者為準；完整敘述仍完整呈現在索引表格的「語系」欄。
FAMILY_KEYS = [
    ("孤立語言", "孤立語言（巴斯克語）"),
    ("印歐語系", "印歐語系"),
    ("烏拉語系", "烏拉語系"),
    ("亞非語系", "亞非語系"),
    ("尼日—剛果語系", "尼日—剛果語系"),
    ("日本語系", "日本語系（日琉語系）"),
    ("朝鮮語系", "朝鮮語系"),
    ("漢藏語系", "漢藏語系"),
]
FAMILY_ORDER = [label for _, label in FAMILY_KEYS]

# sources-and-law 底下各條目的 region 各自標明適用範圍，不適合當章節標題。
DIR_TITLES = {"sources-and-law": "文獻與法制（跨地區）"}


def parse_frontmatter(text):
    """極簡 YAML 子集解析：key: value、key: [a, b]、以及一層縮排的巢狀區塊。"""
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    data = {}
    current_block = None
    for raw in text[4:end].splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indented = raw[0] in " \t"
        line = raw.strip()
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if indented and current_block is not None:
            data.setdefault(current_block, {})[key] = strip_scalar(value)
            continue
        if value == "":
            current_block = key
            data.setdefault(key, {})
            continue
        current_block = None
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            data[key] = [v.strip() for v in inner.split(",") if v.strip()] if inner else []
        else:
            data[key] = strip_scalar(value)
    return data


def strip_scalar(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    if value in ("null", "~", ""):
        return None
    return value


def collect():
    entries = []
    for sub in ("regions", "sources-and-law"):
        base = os.path.join(REF, sub)
        if not os.path.isdir(base):
            continue
        for dirpath, _dirnames, filenames in os.walk(base):
            for fn in sorted(filenames):
                if not fn.endswith(".md"):
                    continue
                path = os.path.join(dirpath, fn)
                with io.open(path, encoding="utf-8") as f:
                    text = f.read()
                fm = parse_frontmatter(text)
                if not fm.get("id"):
                    continue
                rel = os.path.relpath(path, REF).replace("\\", "/")
                fm["_path"] = rel
                fm["_dir"] = os.path.dirname(rel)
                fm["_glossary"] = parse_glossary(text)
                entries.append(fm)
    entries.sort(key=lambda e: (e["_dir"], e["id"]))
    return entries


def parse_glossary(text):
    """抓出「## 專有名詞對照」表格中的資料列。"""
    m = re.search(r"^##\s*專有名詞對照\s*$", text, re.M)
    if not m:
        return []
    rest = text[m.end():]
    nxt = re.search(r"^##\s", rest, re.M)
    if nxt:
        rest = rest[: nxt.start()]
    rows = []
    for line in rest.splitlines():
        line = line.strip()
        if not line.startswith("|") or not line.endswith("|"):
            continue
        cells = [c.strip() for c in line[1:-1].split("|")]
        if len(cells) < 3:
            continue
        if set("".join(cells)) <= set("-: "):
            continue
        if cells[0] in ("原文",):
            continue
        rows.append(cells)
    return rows


def link(entry, from_dir=""):
    prefix = "../" if from_dir else ""
    return "[%s](%s%s)" % (entry.get("title_zh") or entry["id"], prefix, entry["_path"])


def fmt_native(entry):
    native = entry.get("title_native") or ""
    rom = entry.get("title_romanized")
    if rom and rom != native:
        return "%s（%s）" % (native, rom)
    return native


def region_of(entry):
    return entry.get("region") or "未分類"


def section_title(entries):
    d = entries[0]["_dir"]
    if d in DIR_TITLES:
        return DIR_TITLES[d]
    return region_of(entries[0])


def family_of(entry):
    """把詳略不一的 language_family 敘述正規化成語系層級。"""
    text = entry.get("language_family") or ""
    hits = [(text.find(k), label) for k, label in FAMILY_KEYS if k in text]
    if not hits:
        return "未標註"
    return min(hits)[1]


def table(entries, from_dir="", family_column=False):
    head = ["條目", "原文名稱", "語言"]
    head += ["語系"] if family_column else []
    head += ["時代", "類型"]
    out = ["| %s |" % " | ".join(head), "| %s |" % " | ".join(["---"] * len(head))]
    for e in entries:
        cells = [link(e, from_dir), fmt_native(e), e.get("language") or ""]
        if family_column:
            cells.append(e.get("language_family") or "")
        cells += [
            e.get("era") or "",
            TYPE_LABELS.get(e.get("type"), e.get("type") or ""),
        ]
        out.append("| %s |" % " | ".join(cells))
    return "\n".join(out)


def group(entries, keyfunc):
    buckets = {}
    for e in entries:
        buckets.setdefault(keyfunc(e), []).append(e)
    return buckets


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("寫入 %s" % os.path.relpath(path, ROOT).replace("\\", "/"))


def build_main_index(entries):
    parts = [
        "# 魔女傳說參考資料庫 主索引",
        "",
        "依地區分類。語系與時代的交叉索引見 [語系索引](indexes/by-language-family.md)"
        "與 [時代索引](indexes/by-era.md)；原文名詞對照見 [名詞總表](name-glossary.md)。",
        "",
        "共收錄 %d 條。" % len(entries),
        "",
    ]
    by_dir = group(entries, lambda e: e["_dir"])
    for d in sorted(by_dir):
        items = by_dir[d]
        parts.append("## %s（%d 條）" % (section_title(items), len(items)))
        parts.append("")
        parts.append(table(items))
        parts.append("")
    return "\n".join(parts)


def build_language_index(entries):
    parts = [
        "# 語系交叉索引",
        "",
        "依條目原文所屬的語系分類。條目取材橫跨多個語系時（例如巴斯克語傳說配西班牙語"
        "司法檔案、拉丁文原典配德語條目），歸入其發源語言所屬的語系，完整敘述見「語系」欄。"
        "回到 [主索引](../INDEX.md)。",
        "",
    ]
    by_fam = group(entries, family_of)
    ordered = [f for f in FAMILY_ORDER if f in by_fam]
    ordered += [f for f in sorted(by_fam) if f not in FAMILY_ORDER]
    for fam in ordered:
        items = by_fam[fam]
        parts.append("## %s（%d 條）" % (fam, len(items)))
        parts.append("")
        parts.append(table(items, from_dir="indexes", family_column=True))
        parts.append("")
    return "\n".join(parts)


def build_era_index(entries):
    parts = [
        "# 時代交叉索引",
        "",
        "依條目主要對應的時代分類。同一形象跨越多個時代者，歸入其成形或事件發生的時代。"
        "回到 [主索引](../INDEX.md)。",
        "",
    ]
    by_era = group(entries, lambda e: (e.get("era_bucket") or "未標註"))
    for key, label in ERA_LABELS:
        if key not in by_era:
            continue
        items = by_era.pop(key)
        parts.append("## %s（%d 條）" % (label, len(items)))
        parts.append("")
        parts.append(table(items, from_dir="indexes"))
        parts.append("")
    for key in sorted(by_era):
        parts.append("## %s" % key)
        parts.append("")
        parts.append(table(by_era[key], from_dir="indexes"))
        parts.append("")
    return "\n".join(parts)


def build_glossary(entries):
    parts = [
        "# 原文專有名詞對照總表",
        "",
        "彙整各條目「專有名詞對照」一節的內容，依條目排列。"
        "本表僅供本資料庫使用，與遊戲規則術語庫 `glossary.json` 各自獨立。"
        "回到 [主索引](INDEX.md)。",
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
    entries = collect()
    if not entries:
        print("reference/ 底下找不到任何含 frontmatter 的條目。")
        return 1
    write(os.path.join(REF, "INDEX.md"), build_main_index(entries))
    write(os.path.join(REF, "indexes", "by-language-family.md"), build_language_index(entries))
    write(os.path.join(REF, "indexes", "by-era.md"), build_era_index(entries))
    write(os.path.join(REF, "name-glossary.md"), build_glossary(entries))
    print("\n共處理 %d 條條目。" % len(entries))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
