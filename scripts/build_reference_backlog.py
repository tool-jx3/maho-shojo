#!/usr/bin/env python
"""把候選條目掃描結果整理成可檢視的待辦清單 reference/BACKLOG.md。

輸入：reference/backlog/candidates-raw.tsv
      （由 scripts/find_reference_candidates.py 產生的原始掃描結果，未經篩選）

處理：
1. 濾掉虛構作品／流行文化類別的條目（分類路徑或標題命中黑名單）
2. 扣掉 reference/ 底下已經收錄的條目（比對原文標題與各條目的來源 URL）
3. 依分類路徑歸納成主題群組，依內容量排序

輸出：reference/BACKLOG.md（勾選清單）

新增條目後重跑本腳本，已收錄者會自動從待辦中消失。

用法：
    .venv/Scripts/python.exe scripts/build_reference_backlog.py
"""

from __future__ import annotations

import io
import os
import re
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_reference_indexes import collect  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(ROOT, "reference")
RAW = os.path.join(REF, "backlog", "candidates-raw.tsv")
# 優先候選的實際純文字字數，覆寫掃描得到的原始碼位元組估算值
PRIORITY_SIZES = os.path.join(REF, "backlog", "priority-sizes.tsv")
THIN = 4000  # 純文字字數低於此值，逐段對譯的格式會撐不起來
OUT = os.path.join(REF, "BACKLOG.md")
NL = chr(10)

LANG_NAMES = {
    "en": "英語", "de": "德語", "fr": "法語", "es": "西班牙語", "it": "義大利語",
    "sv": "瑞典語", "ru": "俄語", "pl": "波蘭語", "ja": "日語", "nl": "荷蘭語",
    "is": "冰島語", "no": "挪威語", "eu": "巴斯克語", "la": "拉丁語",
    "zh": "中文", "ko": "韓語", "fur": "弗留利語", "sco": "蘇格蘭語",
    "ga": "愛爾蘭語", "gd": "蘇格蘭蓋爾語", "fi": "芬蘭語", "hu": "匈牙利語",
    "uk": "烏克蘭語", "el": "希臘語", "he": "希伯來語", "ar": "阿拉伯語",
    "yo": "約魯巴語", "ln": "林加拉語",
}

# 只看分類路徑的最末層（最具體的那個分類）來判斷是否為虛構作品／流行文化。
# 看整條路徑會誤殺：例如 Witchcraft in fairy tales 掛在 Fiction about witchcraft 底下，
# 但童話中的女巫正是本資料庫要收的東西。
FICTION_SEGMENT = re.compile(
    r"(Fiction about|in fiction|Modern witchcraft|Wizarding|ヘンゼルとグレーテル|"
    r"Films? about|Video games? about|television|télévisé|Film mettant|im Film|"
    r"Anime and manga|Arthurian fiction|Fiction about curses|immaginari|"
    r"opere di fantasia|ficticios|en la ficción|en cine|Magicien ou sorcier de fiction|"
    r"を題材とした|Brujas en el arte|nell'arte|dans l'art|in art|Comic|Manga|"
    r"Personnage de|Personaje de|Personaggio di|Roman|Novel|Album|Band|Song|"
    r"Musical|Oper |Spiel|Game)",
    re.I,
)
# 即使命中上面的規則，這些主題仍要保留
KEEP_SEGMENT = re.compile(r"(fairy tales?|Märchen|conte|cuento|fiaba|folklore|légende|leyenda)", re.I)

# 整棵排除：Kategorie:Sagengestalt 是德語「傳說人物」的通用分類，與巫術無關
# （撈進了阿提拉、帕西法爾、仙女座等），第一次掃描誤用它當種子，第二次已移除。
EXCLUDE_PATH = re.compile(r"^Kategorie:Sagengestalt")


def is_fiction(path, title):
    if EXCLUDE_PATH.search(path):
        return True
    segment = path.split(" > ")[-1]
    if KEEP_SEGMENT.search(segment):
        return False
    return bool(FICTION_SEGMENT.search(segment))
# 這些主題與「歷史上的魔女傳說」關係遠，另外標為低優先而非直接刪除
LOW_PRIORITY = re.compile(r"(Satanismo|Organisation|Wicca|New Age|Occultis)", re.I)

# 分類路徑 -> 主題群組
THEMES = [
    (r"Opfer der Hexenverfolgung|Offer|victims", "獵巫受害者（個案）"),
    (r"Täter der Hexenverfolgung", "獵巫加害者"),
    (r"Gegner der Hexenverfolgung", "獵巫的反對者"),
    (r"executed for witchcraft|avrättade för häxeri|Personas ejecutadas", "被處決者"),
    (r"accused of witchcraft|Accusers in witch trials", "受指控者與指控者"),
    (r"Procesos por brujería|Witch trials|Häxprocess|räumlicher Zuordnung|"
     r"Hexenzeitung|Witch trials in North America", "審判事件"),
    (r"Étude de la sorcellerie|Estudiosos|scholars", "巫術研究者與研究史"),
    (r"Magicien ou sorcier de légende|Sorcellerie féminine|Brujas \(brujería\)|"
     r"Ведьмы|Streghe|Czarownice", "傳說中的巫者形象"),
    (r"Imps", "小妖精與使魔"),
    (r"Maldiciones|Curses", "詛咒與法術"),
    (r"fairy tales?|Märchen|conte|cuento|fiaba", "童話中的女巫"),
    (r"Sagengestalt|Fabelwesen|légende|leyenda|folklore", "傳說人物與怪異存在"),
    (r"in der Kultur|dans l'art et la culture|Rezeption", "獵巫的文化再現"),
    (r"Witchcraft in |European witchcraft|Brujería en|Sorcellerie en|"
     r"Stregoneria in", "各地區的巫術"),
]


SLUGS = {
    "獵巫受害者（個案）": "victims",
    "獵巫加害者": "perpetrators",
    "獵巫的反對者": "opponents",
    "被處決者": "executed",
    "受指控者與指控者": "accused",
    "審判事件": "trials",
    "巫術研究者與研究史": "scholarship",
    "傳說中的巫者形象": "legendary-witches",
    "小妖精與使魔": "imps-familiars",
    "詛咒與法術": "curses",
    "童話中的女巫": "fairy-tales",
    "傳說人物與怪異存在": "legendary-beings",
    "獵巫的文化再現": "reception",
    "各地區的巫術": "regional",
    "其他": "misc",
}

# 人工挑選的優先候選：明確屬於本資料庫範圍、且首批與第二批都沒有收的。
# 格式為 (語言, 條目標題, 為什麼值得收)
PRIORITY = [
    ("de", "Hexenverfolgung", "獵巫的德語總論條目，本庫目前只有個案沒有通論"),
    ("en", "Witch hunt", "獵巫的英語總論，可與德語版互為對照"),
    ("sv", "Häxprocess", "瑞典語總論，補北歐視角"),
    ("de", "Hexenverfolgung im Waadtland", "沃州，歐洲最早的大規模獵巫地之一"),
    ("de", "Hexenprozesse in Freiburg (Schweiz)", "瑞士地區審判，與安娜·葛爾迪一條互補"),
    ("de", "Hexenprozesse in der Grafschaft Werdenfels", "巴伐利亞地區審判"),
    ("de", "Die Besessenen von Aix-en-Provence", "1611 年附身案，與盧丹案同型"),
    ("en", "Cotton Mather", "塞勒姆審判的關鍵推手，本庫已有塞勒姆卻無此人"),
    ("de", "Hostienfrevel", "褻瀆聖體指控，與獵巫並行的迫害機制"),
    ("de", "Diana", "《主教教規》所述夜行女神信仰的源頭"),
    ("de", "Ritualmordlegende", "血祭誹謗，與獵巫平行的另一套迫害機制"),
    ("en", "Morgan le Fay", "亞瑟王傳說中的女巫，本庫缺凱爾特—法蘭西線"),
    ("en", "Hecate", "希臘巫術女神，喀爾刻條目多次提及卻無專條"),
    ("en", "Gilles de Rais", "與魔鬼交易母題的著名審判"),
    ("ru", "Аэндорская волшебница", "隱多珥的女巫，聖經中的招魂者"),
    ("en", "Zduhać", "南斯拉夫的靈魂出竅戰士，與貝南丹提同型"),
    ("fr", "Dahut", "布列塔尼伊斯城傳說中的女性形象"),
    ("fr", "Lieu du sabbat", "巫魔會地點的母題研究"),
    ("fr", "Carrefour dans le folklore et la mythologie", "十字路口母題，橫跨多個既有條目"),
    ("fr", "Crapaud dans l'imaginaire et la tradition en Occident", "蟾蜍母題，蘇加拉穆爾迪案的核心物證"),
    ("it", "Goezia (pratica magica)", "召魔術傳統，與魔法書條目互補"),
    ("de", "Guillaume Adeline", "15 世紀的獵巫反對者，早於魏爾一個世紀"),
    ("de", "Johannes Pistorius der Jüngere", "獵巫反對者"),
    ("de", "Matthäus Alber", "獵巫反對者"),
    ("de", "Simon Gogräve", "獵巫反對者"),
    ("de", "Dietrich Schnepf", "獵巫反對者"),
    ("de", "Bader-Ann", "受害者個案"),
    ("de", "Paula von Weitershausen", "加害者個案"),
    ("de", "Sebastian Röttinger", "加害者個案"),
    ("en", "Elizabeth Howe", "塞勒姆受害者個案"),
    ("en", "Elizabeth Frauncis", "英格蘭最早的女巫審判被告之一"),
    # 東亞：第三批優先收人物與傳說，以下制度性、職業性的形象留待後續
    ("ja", "巫女", "日本的神職少女，與歐洲「女巫是被迫害者」完全相反的模式"),
    ("ja", "斎宮", "卜定的未婚皇女，被選中後與世隔絕侍神，最徹底的「被選中的少女」制度"),
    ("ja", "陰陽道", "式神與安倍晴明條目的制度背景"),
    ("ja", "イタコ", "東北地方的盲眼女性靈媒，口寄せ（招魂）"),
    ("ja", "ユタ", "沖繩的女性靈媒，與制度性的ノロ相對的民間靈能者"),
    ("ja", "ノロ", "琉球的女祭司，聞得大君之下的神女組織"),
    ("ja", "飯縄権現", "飯綱法與管狐信仰的本尊"),
    ("ja", "神隠し", "異界擄人母題"),
    ("zh", "扶乩", "漢文化圈的降筆術，與歐洲的招魂術可對照"),
    ("zh", "麻姑", "道教女仙，長生與滄海桑田的象徵"),
    ("ko", "무녀", "韓國的女巫，무당條目的性別專條"),
    ("ko", "굿", "韓國巫俗的儀式，바리공주敘事詩即在其中吟唱"),
    ("ko", "점복", "韓國的占卜傳統"),
    ("ko", "마고할미", "韓國的創世女神，與中國麻姑同源"),
]


def theme_of(path):
    for pattern, label in THEMES:
        if re.search(pattern, path, re.I):
            return label
    return "其他"


def covered_titles():
    seen = set()
    for e in collect():
        for key in ("title_native", "title_native_alt", "title_zh"):
            v = e.get(key)
            if v:
                for part in re.split(r"[／/]", v):
                    seen.add(part.strip())
        src = e.get("source") or {}
        for k in ("wiki", "wiki_secondary"):
            url = src.get(k)
            if not url:
                continue
            m = re.match(r"https?://[a-z\-]+\.wikipedia\.org/wiki/(.+)", url)
            if m:
                seen.add(urllib.parse.unquote(m.group(1)).replace("_", " ").strip())
    return {s for s in seen if s}


def main():
    if not os.path.exists(RAW):
        print("找不到 %s，請先跑 scripts/find_reference_candidates.py 並把結果放進該路徑。" % RAW)
        return 1

    covered = covered_titles()

    real_sizes = {}
    if os.path.exists(PRIORITY_SIZES):
        with io.open(PRIORITY_SIZES, encoding="utf-8") as f:
            for line in f:
                if line.startswith("#") or line.startswith("語言"):
                    continue
                c = line.rstrip(chr(10)).split(chr(9))
                if len(c) >= 3 and c[2].isdigit():
                    real_sizes[(c[0], c[1])] = int(c[2])

    rows = []
    total_raw = 0
    dropped_fiction = 0
    dropped_covered = 0
    with io.open(RAW, encoding="utf-8") as f:
        next(f, None)
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 4:
                continue
            lang, title, size, path = parts[0], parts[1], parts[2], parts[3]
            total_raw += 1
            if is_fiction(path, title):
                dropped_fiction += 1
                continue
            if title in covered:
                dropped_covered += 1
                continue
            rows.append((lang, title, int(size), path))

    groups = {}
    for r in rows:
        groups.setdefault(theme_of(r[3]), []).append(r)

    order = [label for _, label in THEMES] + ["其他"]
    order = [g for g in order if g in groups]

    by_key = {(r[0], r[1]): r for r in rows}
    backlog_dir = os.path.join(REF, "backlog")
    os.makedirs(backlog_dir, exist_ok=True)

    def item_line(row, bold=True):
        lang, title, size, path = row
        url = "https://%s.wikipedia.org/wiki/%s" % (
            lang, urllib.parse.quote(title.replace(" ", "_")))
        name = "**%s**" % title if bold else title
        return "- [ ] %s（%s，原始碼 %s 位元組）— [原文](%s) — 來源分類：%s" % (
            name, LANG_NAMES.get(lang, lang), format(size, ","), url, path)

    # 各主題分檔
    for g in order:
        items = sorted(groups[g], key=lambda r: -r[2])
        low = [r for r in items if LOW_PRIORITY.search(r[3])]
        normal = [r for r in items if not LOW_PRIORITY.search(r[3])]
        body = [
            "# 待收錄候選：%s" % g,
            "",
            "共 %d 項。回到 [待辦總表](../BACKLOG.md)。" % len(items),
            "",
            "本檔由 `scripts/build_reference_backlog.py` 產生，"
            "是機器掃描的結果而非選錄決定，每一項都需要人工判斷。",
            "",
        ]
        body += [item_line(r) for r in normal]
        if low:
            body += ["", "## 與本資料庫主題較遠者（%d 項）" % len(low), ""]
            body += [item_line(r, bold=False) for r in low]
        body.append("")
        with io.open(os.path.join(backlog_dir, SLUGS.get(g, "misc") + ".md"),
                     "w", encoding="utf-8") as f:
            f.write(NL.join(body))

    parts = [
        "# 待收錄候選清單",
        "",
        "本檔由 `scripts/build_reference_backlog.py` 依 "
        "[backlog/candidates-raw.tsv](backlog/candidates-raw.tsv) 產生，"
        "該原始檔則來自 `scripts/find_reference_candidates.py` "
        "對各語言維基百科分類樹的掃描。",
        "",
        "建立首批 35 條時，選錄清單是憑印象開出來的，因此像 Lutzelfrau 這種地方性形象"
        "根本沒有機會浮上檯面。本清單的用意是把「還有什麼沒收」變成可查證、可逐項檢視的問題。",
        "",
        "## 怎麼用",
        "",
        "- 這是**機器掃描的結果，不是選錄決定**。每一項都需要人工判斷是否適合收錄。",
        "- 已收錄的條目會在重跑腳本時自動從清單消失，不必手動勾除。",
        "- 判斷是否值得收錄時，優先看：有沒有發源語言的條目、內容量是否足以支撐逐段對譯、"
        "以及是否補上了現有資料庫沒有的維度（地區、語系、時代、類型）。",
        "- **各主題清單的數字是 wikitext 原始碼的位元組數，不是純文字字數。**"
        "實測比值：歐洲語言約 1.7—2.2 倍，日／中／韓約 3.4—7.6 倍——也就是說"
        "同樣的位元組數，CJK 條目的實際內容只有歐洲條目的三分之一左右。"
        "跨語言比較時務必把這個偏差算進去。「優先候選」表則已換成實測的純文字字數。",
        "",
        "## 統計",
        "",
        "| 項目 | 數量 |",
        "| --- | --- |",
        "| 掃描結果原始筆數 | %d |" % total_raw,
        "| 濾除：虛構作品與流行文化 | %d |" % dropped_fiction,
        "| 濾除：已收錄 | %d |" % dropped_covered,
        "| **待檢視** | **%d** |" % len(rows),
        "",
        "掃描涵蓋 en、de、fr、es、it、sv、ru、pl、ja 九個語言版本的獵巫與巫術相關分類。"
        "未涵蓋的語言（ko、zh、ar、he、yo、ln 等）目前只能靠個別查找，這是本清單已知的偏誤。",
        "",
        "分類樹裡混有大量虛構作品與流行文化條目，腳本的排除規則只能濾掉大部分，"
        "各主題清單中仍會殘留一些明顯不相干的項目。",
        "",
    ]

    # 優先候選（人工挑選）
    parts += ["## 優先候選（人工挑選）", ""]
    parts += ["以下是從掃描結果中挑出、明確屬於本資料庫範圍且尚未收錄的項目，"
              "可以直接從這裡開下一批。已收錄者會自動從表中消失。", ""]
    parts += ["| 條目 | 語言 | 純文字字數 | 為什麼值得收 |", "| --- | --- | --- | --- |"]
    # 人工挑選的項目即使不在掃描結果內（不屬於任何被掃描的分類、或低於字元數門檻）
    # 仍要列出，只是字元數留白——否則會因為機器沒掃到而被靜默丟棄。
    for lang, title, why in PRIORITY:
        if title in covered:
            continue
        row = by_key.get((lang, title))
        url = "https://%s.wikipedia.org/wiki/%s" % (
            lang, urllib.parse.quote(title.replace(" ", "_")))
        n = real_sizes.get((lang, title))
        if n is None:
            size = format(row[2], ",") + "（估）" if row else "—"
            note = ""
        else:
            size = format(n, ",")
            note = "　**篇幅偏薄**" if n < THIN else ""
        parts.append("| [%s](%s) | %s | %s | %s%s |" % (
            title, url, LANG_NAMES.get(lang, lang), size, why, note))
    parts.append("")
    parts.append("本表的字數為實測的**純文字字數**（`prop=extracts&explaintext`），"
                 "標「（估）」者為原始碼位元組的估算值，標「—」者不在掃描涵蓋範圍內。"
                 "標「篇幅偏薄」者純文字不足 %d 字，可能撐不起逐段對譯的體例，"
                 "收錄前要先確認實際可用內容。" % THIN)
    parts.append("")

    # 主題索引
    parts += ["## 依主題分列", "", "| 主題 | 項數 | 清單 |", "| --- | --- | --- |"]
    for g in order:
        slug = SLUGS.get(g, "misc")
        parts.append("| %s | %d | [backlog/%s.md](backlog/%s.md) |"
                     % (g, len(groups[g]), slug, slug))
    parts += ["", "完整未篩選的掃描結果保存在 "
              "[backlog/candidates-raw.tsv](backlog/candidates-raw.tsv)，"
              "包含被規則濾掉的項目，以免有東西被靜默丟棄。", ""]

    with io.open(OUT, "w", encoding="utf-8") as f:
        f.write(NL.join(parts))
    print("寫入 %s：%d 項待檢視（原始 %d、濾除虛構 %d、濾除已收錄 %d）"
          % (os.path.relpath(OUT, ROOT).replace("\\", "/"),
             len(rows), total_raw, dropped_fiction, dropped_covered))
    return 0


if __name__ == "__main__":
    sys.exit(main())
