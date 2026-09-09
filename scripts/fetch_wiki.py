#!/usr/bin/env python
"""擷取維基百科條目純文字，供 reference/ 魔女傳說資料庫使用。

用法：
    .venv/Scripts/python.exe scripts/fetch_wiki.py <jobs.tsv>

jobs.tsv 為 UTF-8、以 tab 分隔的檔案，每行：
    <語言代碼>\t<條目標題>\t<輸出檔名>[\t<字型變體>]

例：
    ru	Баба-яга	baba-yaga-ru
    zh	巫蠱之禍	wugu-zh	zh-tw

輸出寫入 .cache/wiki/<輸出檔名>.txt（該目錄已被 .gitignore 排除）。
找不到條目時會印出 MISS、該語言維基的搜尋候選標題，並自動查 en／de／fr／es
是否有同名條目可作為降級來源，據以修正 jobs.tsv 後重跑。

注意：標題含非 ASCII 字元時，請以 Write 工具建立 jobs.tsv，不要用 shell 參數傳遞，
以免 Git Bash 在 Windows 上把引數編碼弄壞。
"""

from __future__ import annotations

import io
import json
import os
import sys
import time
from datetime import date
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, ".cache", "wiki")
# 發源語言查無條目時，依序嘗試這些通行語版本再下結論。
FALLBACK_LANGS = ["en", "de", "fr", "es"]

# Wikimedia 的 User-Agent 政策要求標明用途與聯絡方式，否則容易被限流（HTTP 429）。
UA = (
    "maho-shojo-reference/1.0 "
    "(zh-TW translation research; https://github.com/tool-jx3/maho-shojo)"
)


def api(lang, params):
    url = "https://%s.wikipedia.org/w/api.php?%s" % (
        lang,
        urllib.parse.urlencode(params, encoding="utf-8"),
    )
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=45) as r:
        return json.loads(r.read().decode("utf-8"))


def extract(lang, title, variant=None):
    params = {
        "action": "query",
        "prop": "extracts",
        "explaintext": 1,
        "redirects": 1,
        "format": "json",
        "formatversion": 2,
        "titles": title,
    }
    if variant:
        params["variant"] = variant
        params["uselang"] = variant
    d = api(lang, params)
    pg = d["query"]["pages"][0]
    return pg.get("title", title), pg.get("extract", "") or ""


def search(lang, term, limit=10):
    d = api(
        lang,
        {
            "action": "query",
            "list": "search",
            "srsearch": term,
            "srlimit": limit,
            "format": "json",
            "formatversion": 2,
        },
    )
    return [h["title"] for h in d["query"]["search"]]


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    os.makedirs(OUT, exist_ok=True)
    with io.open(sys.argv[1], encoding="utf-8") as f:
        jobs = [
            l.rstrip("\n").split("\t")
            for l in f
            if l.strip() and not l.startswith("#")
        ]

    missing = 0
    for row in jobs:
        lang, title, name = row[0], row[1], row[2]
        variant = row[3] if len(row) > 3 and row[3].strip() else None
        try:
            got, text = extract(lang, title, variant)
            if not text.strip():
                missing += 1
                print("MISS %-28s %s/%s" % (name, lang, title))
                print("       %s 站內候選：%s" % (lang, "、".join(search(lang, title)) or "（無）"))
                # 發源語言查無條目時，務必再查通行語版本再下結論。
                # Lutzelfrau 一例即因只查了 de、沒查 en 而被誤判為「維基百科沒有此條目」。
                for alt in FALLBACK_LANGS:
                    if alt == lang:
                        continue
                    try:
                        alt_title, alt_text = extract(alt, title)
                        if alt_text.strip():
                            print(
                                "       %s 有條目〈%s〉（%d 字元）——可作為降級來源"
                                % (alt, alt_title, len(alt_text))
                            )
                        else:
                            hits = search(alt, title)
                            if hits:
                                print("       %s 站內候選：%s" % (alt, "、".join(hits[:5])))
                    except Exception:  # noqa: BLE001
                        pass
                    time.sleep(0.3)
                continue
            path = os.path.join(OUT, name + ".txt")
            with io.open(path, "w", encoding="utf-8") as out:
                out.write("# %s (%s.wikipedia.org)\n" % (got, lang))
                out.write(
                    "# url: https://%s.wikipedia.org/wiki/%s\n"
                    % (lang, urllib.parse.quote(got.replace(" ", "_")))
                )
                out.write("# retrieved: %s\n" % date.today().isoformat())
                out.write("=" * 60 + "\n")
                out.write(text)
            print("OK   %-28s %s/%s  chars=%d" % (name, lang, got, len(text)))
        except Exception as e:  # noqa: BLE001
            missing += 1
            print("ERR  %-28s %s/%s  %s" % (name, lang, title, e))
        time.sleep(0.4)

    print("\n完成 %d 筆，%d 筆需要修正標題。" % (len(jobs) - missing, missing))
    return 0


if __name__ == "__main__":
    sys.exit(main())
