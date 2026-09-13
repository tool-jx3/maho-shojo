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

這支腳本做三種獨立的檢查、外加兩種不算違規的提醒：
1. 上述的行文掃描——名詞表已定案的繁體中文形，卻仍在行文中出現原文形。
2. 表格本身的缺陷——「說明」欄已經寫明中文行文該怎麼寫（例如「中文行文作
   『讀』『売』」），但「繁體中文」欄卻沒有照做。第 1 種檢查天生看不到這種
   缺陷：它只挑「繁體中文」與「原文」不同的列來找行文誤用，而欄位本身沒改對
   時，兩欄恰好相同，根本不會被挑中。読売テレビ 那個真實案例正是這種缺陷，
   詳見 check_table_prescriptions() 與 classify_prescription() 的說明。
3. 出處存在性（裁決 R）——「說明」欄宣稱某個繁中譯名有出處時，那個譯名
   必須真的出現在 `.cache/` 底下某個抓回來的頁面裡。批 B 有四筆譯名的措辭
   出自 WebSearch 摘要而非頁面本文，逐詞比對後在全部快取檔中 0 命中；那四筆
   都是「看起來一定查得到、所以沒去 grep」的詞，靠人工判斷哪一列該查是攔不住
   的。說明欄指名「規則書」的列另外把規則書本體併入搜尋範圍——那是真實的出處，
   只是不是抓回來的網頁。詳見 check_provenance() 與其上方註解。
4. 提醒（不計入結束碼）——「說明」欄裡看得出有 2 的那種規定語氣（「中文
   行文」／「本庫繁中行文」），但引號組排列的方式套不進目前認得的句型，
   看不懂。看不懂不能悶不吭聲：那正是這整支腳本原本要補的洞——一份規定
   換個寫法，檢查器就自動放行、沒人會發現。但看不懂也不該硬猜一個答案去
   斷言表格有錯，猜錯了就是不實指控。折衷是印出提醒、不算違規、不影響
   結束碼，交給人工確認。
5. 提醒（不計入結束碼）——`.cache/` 不存在或沒有可讀的文字檔時，第 3 種檢查
   無從執行。此時印出一則提醒明說「本次未執行出處檢查」，而**不是**安靜地
   全部放行。一支沒真的檢查卻回報成功的檢查器，跟它要防的缺陷是同一個形狀。

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


def parse_glossary_table(lines):
    """解析『專有名詞對照』表格，回傳 (all_rows, table_lines)。

    - all_rows 是 [(原文, 繁體中文, 說明, 行號)]，**表格裡的每一資料列都收**——
      即使「繁體中文」與「原文」兩欄相同也收，因為 check_table_prescriptions()
      要靠「說明」欄本身的文字，去判斷這一列的繁體中文欄有沒有打錯；「兩欄相同
      所以不必檢查」正是 読売テレビ 那個真實案例的錯法：欄位本身沒改對，兩欄自然
      相同，若只收兩欄不同的列，這個檢查就會對這一整類錯誤結構性失明。
    - table_lines 是表格本身（標題列、分隔列、資料列）占用的行號集合；這些行是
      名詞表自己的內容，不是中文行文，找原文形時要整段排除，否則名詞表的原文欄
      與說明欄裡的原文寫法會被自己的規則誤判成違規。

    標題列與分隔列固定緊接在標題之後、各占一列，用列序判斷比逐格比對文字內容
    更穩定——說明欄未來若寫進「---」之類的字樣，逐字比對會誤判。
    """
    all_rows = []
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
        if len(cells) < 4:
            continue
        yuan, zh, note = cells[0], cells[2], cells[3]
        if yuan and zh:
            all_rows.append((yuan, zh, note, lineno))
    return all_rows, table_lines


def diff_rows(all_rows):
    """從 all_rows 篩出「繁體中文」與「原文」不同的列，供裁決 B 的行文掃描使用。

    兩欄相同代表本庫刻意沿用原文（未查得官方繁中名等情形），不受裁決 B 規範；
    這一篩選只服務行文掃描，table-defect 檢查（見 check_table_prescriptions）
    要看的是全部列，兩者用途不同，不能共用同一份清單。
    """
    return [(yuan, zh, lineno) for yuan, zh, _note, lineno in all_rows if yuan != zh]


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


# ── 名詞表「說明」欄的字形規定，與繁體中文欄本身是否照做 ──
#
# 裁決 B 違規多半是行文沒照著名詞表的欽定寫法走，但 読売テレビ 這個真實案例
# 是另一種錯：名詞表那一列自己都沒改對，「繁體中文」欄跟「原文」欄逐字相同，
# 而「說明」欄卻已經寫明中文行文該怎麼寫（「中文行文作『讀』『売』」）。這種
# 錯，找原文形出現在行文裡的規則天生看不到——兩欄相同，該列根本不會被列進
# diff_rows()，行文掃描永遠不會拿它來比對。這裡另立一條規則，直接比對「說明」
# 欄講的規定與「繁體中文」欄目前寫的是否一致，把問題定位在表格本身。
#
# 只認語料庫裡實際出現過的兩種措辭，且要求觸發語的名詞片語逐字相符
# （「日文原名」「中文行文」「本庫繁中行文」），動詞「作」「用」則兩邊都
# 兩種寫法互見（「日文原名用「虚」」、「中文行文作」都真實出現過），因此
# 兩邊都接受「作」或「用」。沒把「中文行文」推廣成「繁中行文」之類語料庫裡
# 沒出現過的講法——寧可漏掉未來條目可能用的新措辭，也不要去猜一個目前完全
# 沒有實例佐證的樣式，猜錯了會對著正常說明文字誤報，比不檢查更糟。
NIHON_GENMEI_RE = re.compile(r"日文原名(?:作|用)((?:「[^」]*」)+)")
ZHONGWEN_XINGWEN_RE = re.compile(r"(?:中文行文|本庫繁中行文)(?:作|用)((?:「[^」]*」)+)")
QUOTE_GROUP_RE = re.compile(r"「([^」]*)」")

# 上面兩個「嚴格版」只認引號組彼此緊鄰、中間不夾任何字元的寫法。「寬鬆版」額外
# 容許組與組之間夾頓號、逗號或空白——不是為了多認一種正式句型，而是用來偵測
# 「作者顯然想列出一整串引號組，卻因為中間多打了分隔符號，被嚴格版從第一個
# 分隔符號處截斷」這種情形：嚴格版仍然會比對成功，只是只抓到清單的前半段，
# 若照樣拿這半截當答案去比對，等於用不完整的資料下判斷，比看不懂更危險。
# 兩個版本抓到的組數只要有落差，就代表發生了這種截斷，見 classify_prescription()。
_SEP = r"[、，,\s]*"
NIHON_GENMEI_LOOSE_RE = re.compile(r"日文原名(?:作|用)((?:「[^」]*」%s)+)" % _SEP)
ZHONGWEN_XINGWEN_LOOSE_RE = re.compile(r"(?:中文行文|本庫繁中行文)(?:作|用)((?:「[^」]*」%s)+)" % _SEP)


def classify_prescription(yuan, note):
    """解析這一列「說明」欄的字形規定，回傳 (kind, value) 三選一：

    - ("match", expected)：辨認出乾淨的句型，expected 是據此算出的「繁體中文」
      欄理論值，交給呼叫端與該欄目前的內容比對。
    - ("notice", None)：說明欄裡確實出現「中文行文」或「本庫繁中行文」這個
      觸發語，但引號組的排列方式套不進下面認得的任何一種句型——可能是未來
      條目換了寫法（例如組與組之間夾了頓號），也可能是別的原因，總之看不懂。
      看不懂不能悶不吭聲地放過（那正是這整支檢查要補的洞），也不能拿殘缺或
      對不上的解析結果去亂猜一個答案（猜錯了就是不實指控，比不檢查更糟）；
      折衷是回報一則提醒，請人工確認，但不當成確定的表格缺陷。
    - ("absent", None)：說明欄裡根本沒有「中文行文」或「本庫繁中行文」這個
      觸發語，不是在規定中文行文的字形，不必理會。

    語料庫裡實際觀察到的兩種乾淨句型（判斷順序即保守程度由高到低）：

    1. 逐字替換：「日文原名作「Y1」「Y2」…，中文行文作「Z1」「Z2」…」，兩邊
       引號組數相同、且每一組都恰好是單一字元（例如「読」→「讀」、「売」→
       「売」，読売テレビ 那列就是兩組）。條件卡得這麼緊，是因為替換動作本身
       只在「單字元換單字元」時才有意義——若「中文行文作」那一組是多字元
       （例如虚淵玄那一列的「虛淵玄」，對應的日文原名只單獨標了「虚」一字），
       拿它去取代原文裡的單一字元，會把周圍字元重複黏貼一次，產生錯誤結果，
       不能套用逐字替換。
    2. 直接宣告全形：不符合上面的逐字替換條件、但「中文行文作／用」後面恰好
       只有一組引號（不論長度），且「日文原名」那邊沒有或同樣只有一組（若
       日文原名那邊有兩組以上，代表作者原本想列的是多組逐字替換，只是中文
       行文那邊的清單被截斷成一組，不能誤認成直接宣告），視為直接宣告整欄
       應該是什麼（虚淵玄那一列即此類：「本庫繁中行文作「虛淵玄」」直接
       給出完整繁中形）。
    """
    zh_loose = ZHONGWEN_XINGWEN_LOOSE_RE.search(note)
    if not zh_loose:
        return ("absent", None)

    zh_strict = ZHONGWEN_XINGWEN_RE.search(note)
    z_groups_loose = QUOTE_GROUP_RE.findall(zh_loose.group(1))
    z_groups_strict = QUOTE_GROUP_RE.findall(zh_strict.group(1)) if zh_strict else []
    if not z_groups_loose:
        return ("absent", None)

    y_loose = NIHON_GENMEI_LOOSE_RE.search(note)
    y_strict = NIHON_GENMEI_RE.search(note)
    y_groups_loose = QUOTE_GROUP_RE.findall(y_loose.group(1)) if y_loose else []
    y_groups_strict = QUOTE_GROUP_RE.findall(y_strict.group(1)) if y_strict else []

    # 寬鬆版比嚴格版多抓到組，代表引號組之間夾了分隔符號，嚴格版切出的只是
    # 半截清單，不能信任下面用嚴格版算出的任何答案。
    if len(z_groups_loose) != len(z_groups_strict) or len(y_groups_loose) != len(y_groups_strict):
        return ("notice", None)

    z_groups = z_groups_strict
    y_groups = y_groups_strict

    if (
        y_groups
        and len(y_groups) == len(z_groups)
        and all(len(y) == 1 for y in y_groups)
        and all(len(z) == 1 for z in z_groups)
        and all(y in yuan for y in y_groups)
    ):
        expected = yuan
        for y, z in zip(y_groups, z_groups):
            expected = expected.replace(y, z)
        return ("match", expected)

    if len(z_groups) == 1 and len(y_groups) <= 1:
        return ("match", z_groups[0])

    return ("notice", None)


def check_table_prescriptions(all_rows, rel):
    """比對每一列「說明」欄的字形規定與「繁體中文」欄目前的內容，找表格本身的缺陷。

    回傳 (problems, notices) 兩份清單：
    - problems 是確定的表格缺陷（説明的規定看得懂，且與繁體中文欄不一致）。
      訊息措辭刻意不用「名詞表作…但此處用了原文形…」那一套，避免讓人誤以為
      要去改行文，而看漏了真正該改的是表格欄位本身。
    - notices 是「看起來像規定，但看不懂」的提醒，不是確定的缺陷，呼叫端不把
      它們算進失敗計數，但仍要印出來，理由見 main() 與 classify_prescription()
      的說明。
    """
    problems = []
    notices = []
    for yuan, zh, note, lineno in all_rows:
        kind, value = classify_prescription(yuan, note)
        if kind == "match" and value != zh:
            problems.append(
                "%s:%d 名詞表本身有誤：說明要求繁體中文欄作「%s」，"
                "但該欄目前寫的是「%s」"
                % (rel, lineno, value, zh)
            )
        elif kind == "notice":
            notices.append(
                "%s:%d 說明欄疑似有字形規定但格式無法辨識，請人工確認"
                % (rel, lineno)
            )
    return problems, notices


# ── 第 3 種檢查：宣稱有出處的譯名，是否真的出現在抓回來的頁面裡（裁決 R） ──
#
# 批 B 覆審抓到四筆譯名，其措辭來自 WebSearch 摘要而不是頁面本文；逐詞比對後，
# 它們在**全部**快取檔中 0 命中（克洛諾・哈拉歐溫、假面騎士系列、超人力霸王系列、
# 祭禮之蛇）。共同成因不是「忘了查」，而是「看起來一定查得到，所以沒去 grep」。
# 靠人工判斷哪一列需要查，攔不住這一類；能攔住的只有機械化的逐列比對。
#
# 刻意設定的兩個範圍限制，寫在這裡是為了避免有人日後「順手改進」把它們拿掉：
#
# A. 本檢查**不驗證譯名來自「正確的」那個出處**，只驗證它來自「某一個實際抓回來
#    的頁面」。要判斷說明欄指名的是哪個快取檔，得去剖析中文散文（「依台灣角川
#    商品頁」「依社群資料庫（中文維基百科）」……），那非常脆弱，換個措辭就失效。
#    這裡取的是便宜的九成：憑空捏造的譯名在任何快取檔裡都找不到，而這正是真正
#    危險的那一類。指名對不對，留給人工覆審與報告裡的清查表。
# B. 說明欄**沒有**宣稱出處的列不檢查。保留日文原文、明寫「未查得」，本來就是
#    無證據時的正當結果，不該被要求在快取裡找得到。
#
# 另外，`.cache/` 是 .gitignore 排除的，全新 clone 上不存在。那種情況會印出提醒
# 並跳過本檢查（見 main()），不會回報成功——理由同檔頭第 5 點。

# 快取目錄。環境變數 WORKS_CACHE_DIR 是給測試用的鉤子：把它指到一個空目錄，
# 就能實地驗證「快取不存在時印提醒而不是假通過」這條路徑真的會走到。一支
# 永遠走不到的跳過分支，跟沒有那條分支一樣不可信。
CACHE_DIR = os.environ.get("WORKS_CACHE_DIR") or os.path.join(ROOT, ".cache")

# 規則書本體。名詞表有一類列的出處是規則書自己已定案的譯名（片名、角色名），
# 那是真實存在的出處，但它不是抓回來的網頁，永遠不會出現在 .cache/ 裡。只比對
# .cache/ 會對這類列誤報，例如 lyrical-nanoha 的「菲特・泰斯塔羅莎」出自
# docs/src/content/docs/rules/friendship-romance.md。因此說明欄提到「規則書」時，
# 搜尋範圍要加上規則書本體。
RULES_DIR = os.environ.get("WORKS_RULES_DIR") or os.path.join(
    ROOT, "docs", "src", "content", "docs", "rules")
RULES_EXTS = (".md",)
RULEBOOK_WORD = "規則書"

# 快取裡只有這幾種副檔名存的是抓回來的頁面純文字（fetch_wiki.py 與 .cache/grab.py
# 的輸出、jobs 清單）。其餘（圖檔、pyc、.md 之類）不納入，免得條目自己的草稿
# 被當成「頁面」而自我印證。
CACHE_EXTS = (".txt", ".tsv", ".csv")

# 分隔號正規化：來源（中文維基百科）的外文人名用半形中點「·」，本庫行文統一用
# 日文中點「・」（各條目已以譯註記錄這項統一）。比對時把兩者視為同一符號，
# 否則「尤諾・斯克萊亞」會在寫作「尤諾·斯克萊亞」的來源裡找不到，變成誤報。
SEPARATOR_TABLE = {ord("・"): "·", ord("･"): "·"}

# 說明欄宣稱「這個譯名有出處」的可觀察標記，分兩類。第一類是 SOURCE_ASSERT_WORDS
# 那幾個固定詞；第二類是「依<某出處>」的通式，但「依」在中文裡太常見，必須排掉
# 已知的非出處用法：
#   依裁決 X／依使用者裁決 —— 引的是本專案的裁決，不是抓回來的頁面
#   依字面譯出／依字面轉為正體字形 —— 明說是本庫自譯，正好相反
#   依日文發音所作之音譯 —— 同上
#   依作品而異 —— 「兩種拼法依作品而異」這種敘述句，根本不是在指出處
#   依者 —— 「無依者的源頭」裡切出來的假命中
# 這份負面清單是封閉的、列的是語料庫裡真的出現過的寫法；寧可漏掉一種還沒見過的
# 新措辭（漏檢只是回到現狀），也不要對正常說明文字誤報（誤報比不檢查更糟）。
SOURCE_ASSERT_WORDS = ("官方譯名", "流通譯名", "通行譯名", "官方英文名", "官方拉丁標誌",
                       "規則書")
# 裁決 P 點名「臺灣通行譯名」「臺灣官方譯名」是最常被漏掉出處的兩種措辭，故
# 「通行譯名」與「官方譯名」都列為標記（兩者都同時涵蓋臺／台兩種寫法）。
#
# 但這幾個詞也會出現在**否定**句裡（「繁中圈無統一官方譯名」「無通行譯名」），
# 那是在說「查不到」，跟宣稱出處正好相反。判斷方式是看標記前面幾個字有沒有
# 否定詞；窗口取 4 個字，足以涵蓋語料庫裡出現過的「無」「未查得」「沒有」與
# 「無統一」這類插入語，又短到不會誤吃前一個子句。
NEGATION_CHARS = ("無", "未", "沒")
NEGATION_WINDOW = 4
NOT_A_SOURCE_AFTER_YI = ("裁決", "使用者裁決", "字面", "日文發音", "作品而異", "者")
YI_RE = re.compile("依[ \u3000]?(?!%s)" % "|".join(NOT_A_SOURCE_AFTER_YI))

# 「出處同上」「處理同上」「繁中出處同上」：名詞表用這種寫法把上一列的出處承接
# 下來。四筆真實失敗裡有兩筆（克洛諾・哈拉歐溫、超人力霸王系列）正是承接列，
# 不處理承接就漏掉一半。承接的語意取「緊鄰的前一列」，這是表格實際的寫法，
# 也最可預測；中間夾了一列沒有標記的列時鏈條就斷（那會少檢查幾列，屬於可接受的
# 漏檢，見上面的限制 A）。
SAME_SOURCE_RE = re.compile(r"同上")


def normalize_separators(text):
    return text.translate(SEPARATOR_TABLE)


def display_path(path):
    """顯示用路徑：能算出相對於 repo 的路徑就用相對路徑，算不出來就用絕對路徑。

    Windows 上 os.path.relpath() 對不同磁碟機的路徑會丟 ValueError。測試時把
    WORKS_CACHE_DIR 指到別的磁碟機（或有人在 repo 外跑這支腳本）就會踩到，
    整支檢查器直接崩掉——一支會崩的檢查器等於沒有檢查器，這裡直接擋掉。
    """
    try:
        return os.path.relpath(path, ROOT).replace("\\", "/")
    except ValueError:
        return path.replace("\\", "/")


def load_cache_texts(cache_dir=None):
    """把快取裡的頁面純文字全部讀進來（已正規化分隔號）。

    回傳 list；空 list 代表「沒有可用的快取」，呼叫端據此跳過第 3 種檢查並
    印出提醒，不得當成「全部通過」。
    """
    cache_dir = cache_dir or CACHE_DIR
    texts = []
    if not os.path.isdir(cache_dir):
        return texts
    for dirpath, _dirnames, filenames in os.walk(cache_dir):
        for fn in sorted(filenames):
            if not fn.lower().endswith(CACHE_EXTS):
                continue
            path = os.path.join(dirpath, fn)
            try:
                with io.open(path, encoding="utf-8", errors="replace") as f:
                    body = f.read()
            except OSError:
                continue
            if body.strip():
                texts.append(normalize_separators(body))
    return texts


def load_rules_texts(rules_dir=None):
    """讀規則書本體（已正規化分隔號），供說明欄指名規則書的列比對。

    找不到目錄時回傳空 list；此時那類列只會比對 .cache/，與加這條規則之前的
    行為相同（可能誤報），main() 會印提醒說明本次沒有規則書可比對。
    """
    rules_dir = rules_dir or RULES_DIR
    texts = []
    if not os.path.isdir(rules_dir):
        return texts
    for dirpath, _dirnames, filenames in os.walk(rules_dir):
        for fn in sorted(filenames):
            if not fn.lower().endswith(RULES_EXTS):
                continue
            try:
                with io.open(os.path.join(dirpath, fn), encoding="utf-8") as f:
                    body = f.read()
            except OSError:
                continue
            if body.strip():
                texts.append(normalize_separators(body))
    return texts


def asserts_source(note, prev_asserts):
    """這一列的說明欄是否宣稱該譯名有出處。

    回傳 (是否宣稱, 是否為承接列)。承接列（「出處同上」）沿用前一列的結果。
    """
    for word in SOURCE_ASSERT_WORDS:
        start = 0
        while True:
            pos = note.find(word, start)
            if pos < 0:
                break
            before = note[max(0, pos - NEGATION_WINDOW):pos]
            if not any(ch in before for ch in NEGATION_CHARS):
                return True, False
            start = pos + 1
    if YI_RE.search(note):
        return True, False
    if SAME_SOURCE_RE.search(note):
        return bool(prev_asserts), True
    return False, False


def check_provenance(all_rows, rel, cache_texts, rules_texts=()):
    """逐列比對：宣稱有出處的譯名，必須在某個抓回來的頁面（或規則書）裡找得到。

    搜尋範圍分兩種，由說明欄自己決定：
    - 一般情形只找 .cache/。
    - 說明欄提到「規則書」時，額外把規則書本體併進搜尋範圍。規則書是真實的
      出處，只是不是抓回來的網頁；不加這一條，出自規則書的譯名會被誤報。
      承接列（「出處同上」）沿用前一列的搜尋範圍，因為它承接的就是那個出處。

    只回傳確定的缺陷。找不到就是找不到——這不是格式看不懂的情形，不必用提醒
    緩衝：說明欄自己宣稱了出處，而本庫抓回來的每一頁都沒有這個詞。
    """
    problems = []
    prev = False
    prev_rulebook = False
    for yuan, zh, note, lineno in all_rows:
        claims, inherited = asserts_source(note, prev)
        uses_rulebook = RULEBOOK_WORD in note or (inherited and prev_rulebook)
        prev = claims
        prev_rulebook = uses_rulebook
        if not claims:
            continue
        term = normalize_separators(zh.strip("『』「」〈〉《》").strip())
        if not term:
            continue
        haystack = list(cache_texts)
        if uses_rulebook:
            haystack += list(rules_texts)
        if any(term in t for t in haystack):
            continue
        problems.append(
            "%s:%d 說明欄宣稱「%s」有出處%s，但這個詞在%s中都找不到（裁決 R）"
            % (rel, lineno, zh, "（承接上一列）" if inherited else "",
               "規則書與 .cache/ 底下的任何一個抓取檔" if uses_rulebook
               else " .cache/ 底下的任何一個抓取檔")
        )
    return problems


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
    不是拿原文取代繁中譯名，不算裁決 B 違規。只在括號內容（不含括號本身）與
    某一列的「原文」欄逐字相同時才剝除——是逐字比對，不做任何空白容錯（不修剪
    頭尾空白，括號內外多一個全形或半形空白都不算相同）。範圍限制得夠窄，才不會
    連「柱」被「原文……等」這類真正夾帶原文說明的括號一併放行；之後若語料庫
    真的出現括號內帶空白的雙語註記，再視實例決定要不要加上空白容錯。
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


def check(path, rel, cache_texts, rules_texts=()):
    """回傳 (problems, notices)。

    cache_texts 是 load_cache_texts() 讀進來的快取頁面文字；為空 list 時代表
    沒有可用的快取，第 3 種檢查（出處存在性）整個跳過，由 main() 印出提醒。

    problems 是確定的違規／缺陷，計入失敗檔案數與結束碼；notices 是「看起來
    像規定但格式無法辨識」的提醒，只印出來讓人核對，不計入失敗數也不影響
    結束碼——它是提醒人去看一眼，不是斷言表格有錯，兩者必須分開，見 main()
    的說明。
    """
    problems = []
    with io.open(path, encoding="utf-8") as f:
        text = f.read()
    lines = text.splitlines()

    fm_end = frontmatter_end(lines)
    all_rows, table_lines = parse_glossary_table(lines)
    source_lines = source_section_span(lines)

    # 表格缺陷檢查看的是全部列（含「繁體中文」與「原文」相同的列），跟下面
    # 行文掃描要用的 rows（只收兩欄不同的列）互相獨立，先做完全不影響後續。
    table_problems, notices = check_table_prescriptions(all_rows, rel)
    problems.extend(table_problems)

    # 出處存在性檢查（裁決 R）同樣看全部列，與上下兩種檢查互相獨立。
    # cache_texts 為空時跳過——沒有快取就是沒檢查，不能算通過；提醒由 main() 印。
    if cache_texts:
        problems.extend(check_provenance(all_rows, rel, cache_texts, rules_texts))

    rows = diff_rows(all_rows)
    if not rows:
        return problems, notices

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
    return problems, notices


def main():
    paths = sys.argv[1:] or [DEFAULT_DIR]
    total = 0
    failed = 0
    noted = 0

    # 快取只讀一次（批 B 時為 502 個檔、約 11 MB），供全部條目共用。
    cache_texts = load_cache_texts()
    rules_texts = load_rules_texts()
    if cache_texts and not rules_texts:
        # 規則書讀不到時，指名規則書的那些列會退回只比對 .cache/，可能誤報。
        # 同樣要明說，不能讓人以為檢查範圍是完整的。
        noted += 1
        print("     ! 出處檢查：讀不到規則書（%s），說明欄指名規則書的列本次"
              "只比對了 .cache/，可能誤報。" % display_path(RULES_DIR))
    if not cache_texts:
        # .cache/ 被 .gitignore 排除，全新 clone 上不存在。此時第 3 種檢查無從
        # 執行，必須明說「這次沒檢查」而不是安靜放行：一支沒真的檢查卻回報成功
        # 的檢查器，跟它要防的缺陷是同一個形狀。
        noted += 1
        print("     ! 出處檢查（裁決 R）本次未執行：%s 不存在或沒有可讀的快取檔"
              "（%s）。條目中宣稱有出處的譯名這一輪未經比對。"
              % (display_path(CACHE_DIR), "／".join(CACHE_EXTS)))

    for path in iter_files(paths):
        total += 1
        rel = display_path(path)
        problems, notices = check(path, rel, cache_texts, rules_texts)
        if problems:
            failed += 1
            print("FAIL %s" % rel)
            for p in problems:
                print("     - %s" % p)
        else:
            print("ok   %s" % rel)
        # 提醒獨立印在 ok／FAIL 那一行之後，用「!」而非「-」開頭以便與確定的
        # 缺陷區分；不計入 failed，結束碼因此不受提醒影響——提醒是請人看一眼，
        # 不是斷言表格有錯，不該讓人以為要靠它擋下 CI 或批次流程。
        for n in notices:
            noted += 1
            print("     ! %s" % n)
    print("\n共檢查 %d 個檔案，%d 個有問題，%d 則提醒。" % (total, failed, noted))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
