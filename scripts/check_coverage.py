#!/usr/bin/env python
"""稽核 reference/ 各條目對原文章節的覆蓋率。

做法：讀每個條目 frontmatter 的 source.wiki（與 wiki_secondary），重新擷取原文，
列出原文的頂層章節標題，再檢查每個標題是否出現在條目檔中。條目的體例要求
「原文與對照翻譯」以原文章節名開節、「其餘章節摘要」逐節涵蓋，因此原文章節名
未出現在條目裡，代表該節可能被整段略過。

參考文獻類章節（Literatur、References、脚注……）不計入。

用法：
    .venv/Scripts/python.exe scripts/check_coverage.py [條目路徑...]
"""

from __future__ import annotations

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
REF = os.path.join(ROOT, "reference")
UA = (
    "maho-shojo-reference/1.0 "
    "(zh-TW translation research; https://github.com/tool-jx3/maho-shojo)"
)

# 各語言的參考文獻／延伸閱讀類章節，不列入覆蓋率
BOILERPLATE = re.compile(
    r"^(referen|referan|referanser|explanatory note|literatur|weblink|einzelnachweis|"
    r"siehe auch|quellen|anmerkungen|"
    r"bibliograf|bibliograph|enlaces|véase|notas|note|voir aussi|liens|annexes|"
    r"external|further reading|see also|sources|notes|footnotes|primary sources|"
    r"kilde|kjelder|eksterne|litteratur|se også|källor|externa|noter|se även|"
    r"literatuur|zie ook|externe|bronnen|voetnoot|"
    r"przypisy|linki zewn|bibliografia|zobacz też|"
    r"ikus gainera|erreferentzia|kanpo estek|外部リンク|脚注|参考文献|関連項目|"
    r"註釋|注釋|参见|參見|參考|注释|각주|외부|참고|같이 보기|같이보기|同名條目|примечани|литератур|ссылк|"
    r"див\. також|джерела|посилання|πηγές|παραπομπές|εξωτερικ|δείτε|jegyzetek|"
    r"források|további|kapcsolódó|collegamenti|voci correlate|altri progetti|"
    r"מקורות|קישורים|לקריאה|ראו גם|انظر أيضا|مراجع|وصلات|مصادر)",
    re.I,
)


def api(lang, params):
    url = "https://%s.wikipedia.org/w/api.php?%s" % (
        lang,
        urllib.parse.urlencode(params, encoding="utf-8"),
    )
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=45) as r:
        return json.loads(r.read().decode("utf-8"))


# 中文維基的章節名要指定字型變體，否則 API 回傳簡體，
# 而條目依 Law 6 一律用正體，字串比對永遠對不上。
VARIANTS = {"zh": "zh-tw"}


def sections_of(lang, title):
    """回傳 [(頂層章節名, [次層小節名, ...]), ...]。

    條目可能以頂層章節名開節，也可能只取其中某個次層小節（例如只譯
    〈Biographie〉底下的〈La mission〉），因此兩層都要納入比對。
    """
    params = {
        "action": "parse",
        "page": title,
        "prop": "sections",
        "format": "json",
        "formatversion": 2,
        "redirects": 1,
    }
    if lang in VARIANTS:
        params["variant"] = VARIANTS[lang]
        params["uselang"] = VARIANTS[lang]
    d = api(lang, params)
    out = []
    for s in d.get("parse", {}).get("sections", []):
        level = s.get("toclevel")
        name = re.sub(r"<[^>]+>", "", s.get("line", "")).strip()
        if not name:
            continue
        if level == 1:
            if BOILERPLATE.match(name):
                out.append(None)  # 佔位，讓後續次層小節不會掛到前一個章節
            else:
                out.append((name, []))
        elif level in (2, 3) and out and out[-1] is not None:
            out[-1][1].append(name)
    return [x for x in out if x is not None]


def norm(s):
    """正規化空白後比對：維基的法語等章節名含不斷行空格（ ），
    條目裡通常寫成一般空格，直接字串比對會對不上。"""
    return re.sub(r"\s+", " ", s.replace(" ", " ").replace("&nbsp;", " ")).strip()


def source_pages(entry):
    """由 frontmatter 的 source 區塊還原 (語言, 條目名) 清單。"""
    src = entry.get("source") or {}
    pages = []
    for url_key, lang_key in (("wiki", "wiki_lang"),
                              ("wiki_secondary", "wiki_secondary_lang"),
                              ("wiki_tertiary", "wiki_tertiary_lang")):
        url = src.get(url_key)
        if not url:
            continue
        m = re.match(r"https?://([a-z\-]+)\.wikipedia\.org/wiki/(.+)", url)
        if not m:
            continue
        lang = src.get(lang_key) or m.group(1)
        title = urllib.parse.unquote(m.group(2)).replace("_", " ")
        pages.append((lang, title))
    return pages


def main():
    targets = sys.argv[1:]
    entries = collect()
    if targets:
        want = {os.path.basename(t) for t in targets}
        entries = [e for e in entries if os.path.basename(e["_path"]) in want]

    worst = []
    for e in entries:
        path = os.path.join(REF, e["_path"])
        text = io.open(path, encoding="utf-8").read()
        pages = source_pages(e)
        if not pages:
            print("SKIP %-34s（frontmatter 無可解析的來源 URL）" % e["id"])
            continue
        missing_all = []
        total = 0
        for lang, title in pages:
            try:
                secs = sections_of(lang, title)
            except Exception as exc:  # noqa: BLE001
                print("ERR  %-34s %s/%s %s" % (e["id"], lang, title, exc))
                continue
            total += len(secs)
            ntext = norm(text)
            for name, children in secs:
                # 頂層章節名有出現、或其任一次層小節名有出現，都算涵蓋
                if norm(name) in ntext or any(norm(c) in ntext for c in children):
                    continue
                missing_all.append("%s：%s" % (lang, name))
            time.sleep(0.4)
        if total == 0:
            continue
        covered = total - len(missing_all)
        pct = 100.0 * covered / total
        flag = "ok  " if pct >= 80 else "LOW "
        print("%s %-34s %d/%d 節（%.0f%%）" % (flag, e["id"], covered, total, pct))
        for m in missing_all:
            print("       未出現：%s" % m)
        if pct < 80:
            worst.append((pct, e["id"]))

    if worst:
        print("\n覆蓋率低於 80%% 的條目 %d 條：" % len(worst))
        for pct, eid in sorted(worst):
            print("  %-34s %.0f%%" % (eid, pct))
    return 0


if __name__ == "__main__":
    sys.exit(main())
