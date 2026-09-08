#!/usr/bin/env python
"""從各語言維基百科的分類遞迴列舉魔女傳說候選條目，扣除已收錄者。

建立 reference/ 首批 35 條時，選錄清單是憑印象由上而下開出來的，
因此像 Lutzelfrau 這種地方性形象根本沒有機會浮上檯面。本腳本改以
維基百科的分類樹做系統性列舉，讓「還有什麼沒收」變成可查證的問題。

用法：
    .venv/Scripts/python.exe scripts/find_reference_candidates.py [--depth 2] [--out 檔案]

輸出 TSV：語言、條目標題、字元數、發現路徑（來自哪個分類）。
字元數用來初步判斷內容是否足以支撐一個條目。
"""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_reference_indexes import collect  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = (
    "maho-shojo-reference/1.0 "
    "(zh-TW translation research; https://github.com/tool-jx3/maho-shojo)"
)

SEEDS = [
    ("en", "Category:Witch trials"),
    ("en", "Category:People executed for witchcraft"),
    ("en", "Category:European witchcraft"),
    ("en", "Category:Witchcraft in folklore"),
    ("de", "Kategorie:Hexenverfolgung"),
    ("fr", "Catégorie:Sorcellerie"),
    ("es", "Categoría:Brujería"),
    ("it", "Categoria:Stregoneria"),
    ("sv", "Kategori:Häxprocesser"),
    ("ru", "Категория:Ведьмы"),
    ("pl", "Kategoria:Czarownice"),
]

# 明顯不屬於「歷史上的魔女傳說」的條目，用關鍵字先濾掉
NOISE = re.compile(
    r"(Template:|Category:|Kategorie:|Catégorie:|Categoría:|Categoria:|Kategori:|"
    r"Категория:|List of|Liste |Wicca|Neopagan|現代魔女|game\)|\(band\)|\(film\)|"
    r"\(album\)|\(novel\)|\(TV |video game|comics|manga|anime)",
    re.I,
)


# 子類別名稱命中即整棵略過：虛構作品、流行文化、現代巫術宗教
SKIP_SUBCAT = re.compile(
    r"(fiction|fictional|film|television|TV |video game|novel|literature|comic|manga|"
    r"anime|character|popular culture|music|album|band|game|Harry Potter|Discworld|"
    r"Wicca|neopagan|modern paganism|Thelema|occultis|New Age|"
    r"Fiktion|Film|Fernseh|Roman|Literatur|Comic|Musik|Spiel|Kultur|"
    r"fiction|cinéma|télévision|roman|littérature|musique|jeu|culture|"
    r"ficción|cine|televisión|novela|literatura|música|juego|cultura|"
    r"finzione|cinema|televisione|romanzo|letteratura|musica|gioco|cultura|"
    r"fiktion|film|litteratur|musik|spel|kultur|"
    r"вымысл|фильм|литератур|музык|игр|культур|"
    r"fikcj|film|literatur|muzyk|gr[ay]|kultur)",
    re.I,
)


def api(lang, params):
    url = "https://%s.wikipedia.org/w/api.php?%s" % (
        lang,
        urllib.parse.urlencode(params, encoding="utf-8"),
    )
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == 4:
                raise
            time.sleep(2 ** attempt)
    return {}


def members(lang, cat, cmtype):
    out = []
    cont = None
    while True:
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": cat,
            "cmlimit": 500,
            "cmtype": cmtype,
            "format": "json",
            "formatversion": 2,
        }
        if cont:
            params["cmcontinue"] = cont
        d = api(lang, params)
        out += [m["title"] for m in d.get("query", {}).get("categorymembers", [])]
        cont = d.get("continue", {}).get("cmcontinue")
        if not cont:
            return out
        time.sleep(0.3)


def sizes(lang, titles):
    """批次取條目字元數，用來判斷內容量。"""
    out = {}
    for i in range(0, len(titles), 20):
        chunk = titles[i : i + 20]
        d = api(
            lang,
            {
                "action": "query",
                "prop": "info",
                "titles": "|".join(chunk),
                "format": "json",
                "formatversion": 2,
            },
        )
        for p in d.get("query", {}).get("pages", []):
            out[p["title"]] = p.get("length", 0)
        time.sleep(0.3)
    return out


def already_covered():
    """已收錄條目的原文標題與各語言來源標題。"""
    seen = set()
    for e in collect():
        for key in ("title_native", "title_native_alt", "title_zh"):
            v = e.get(key)
            if v:
                seen.add(v.strip())
        src = e.get("source") or {}
        for k in ("wiki", "wiki_secondary"):
            url = src.get(k)
            if not url:
                continue
            m = re.match(r"https?://[a-z\-]+\.wikipedia\.org/wiki/(.+)", url)
            if m:
                seen.add(urllib.parse.unquote(m.group(1)).replace("_", " ").strip())
    return seen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--depth", type=int, default=2)
    ap.add_argument("--min-size", type=int, default=4000)
    ap.add_argument("--out", default=".cache/reference-candidates.tsv")
    args = ap.parse_args()

    covered = already_covered()
    found = {}  # (lang, title) -> 發現路徑
    for lang, seed in SEEDS:
        queue = [(seed, seed, 0)]
        visited = set()
        while queue:
            cat, path, depth = queue.pop(0)
            if cat in visited:
                continue
            visited.add(cat)
            try:
                for t in members(lang, cat, "page"):
                    if NOISE.search(t) or t in covered:
                        continue
                    found.setdefault((lang, t), path)
                if depth < args.depth:
                    for sub in members(lang, cat, "subcat"):
                        name = sub.split(":", 1)[-1]
                        if SKIP_SUBCAT.search(name):
                            continue
                        queue.append((sub, path + " > " + name, depth + 1))
            except Exception as exc:  # noqa: BLE001
                print("ERR %s %s %s" % (lang, cat, exc), file=sys.stderr)
            time.sleep(0.3)
        print("%s %-42s 累計候選 %d" % (lang, seed, len(found)))

    by_lang = {}
    for (lang, title) in found:
        by_lang.setdefault(lang, []).append(title)

    rows = []
    for lang, titles in by_lang.items():
        sz = sizes(lang, titles)
        for t in titles:
            rows.append((lang, t, sz.get(t, 0), found[(lang, t)]))
    rows = [r for r in rows if r[2] >= args.min_size]
    rows.sort(key=lambda r: (-r[2], r[0]))

    out = os.path.join(ROOT, args.out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with io.open(out, "w", encoding="utf-8") as f:
        f.write("語言\t條目\t字元數\t發現路徑\n")
        for r in rows:
            f.write("%s\t%s\t%d\t%s\n" % r)
    print("\n候選 %d 條（字元數 >= %d，已扣除既有 %d 個標題），寫入 %s"
          % (len(rows), args.min_size, len(covered), args.out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
