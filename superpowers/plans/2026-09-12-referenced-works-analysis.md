# 規則書參考作品分析資料庫 實作計畫

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 `reference/works/` 建立一個獨立子庫，收錄 Mahō Shōjo 規則書提及的 17 部魔法少女類作品的作品分析，依「作品含意／設計概念／劇本設計」三軸收集，非繁中材料保存原文並逐段對譯。

**Architecture:** 與既有的魔女傳說庫平行的獨立子庫，各自有 README、索引與名詞總表，schema 不共用。條目以日語維基百科為主幹來源，官方網站與製作方訪談為補強。分析與其證據不分離——原文引用直接嵌在它所支持的那一節底下。

**Tech Stack:** Python 3.11+（`.venv/Scripts/python.exe`，Windows）、既有的 `scripts/fetch_wiki.py` 擷取工具、WebFetch／WebSearch 取訪談與官方資料。無測試框架；驗證手段是 `scripts/check_reference.py` 與索引產生器的實際輸出。

**Spec:** `superpowers/specs/2026-09-12-referenced-works-analysis-design.md`

## Global Constraints

每個 Task 的要求都隱含包含本節。

- **Law 6**：一律繁體中文（zh-TW）。不得出現簡體字，不得使用中國大陸用語。
- **Law 8**：全形標點（：，。、；「」『』（）……）；數字與拉丁文字用半形；省略號一律 `……`，不得用 `...`。
- **Law 9**：罕用字、雙關、文化負載詞若影響語意或語氣，停下來向使用者提 2～3 個候選，不自行定案。
- **片名一律沿用規則書已定案的繁中譯名**（見下方「17 部作品對照表」），不另譯、不用其他地區譯名。
- **原文引文逐字保留**，不修正拼寫、標點或錯誤。原文有誤植或來源互相矛盾時照譯，另以 `:::note[譯註]` 指出。
- **不得以推測填滿三軸。** 查不到就依「查無材料時的寫法」明載查過哪些來源。寫一段看似合理但無來源的分析，是本計畫定義的失敗。
- **不得寫入 `glossary.json`。** 本子庫的名詞收於 `reference/works/name-glossary.md`。
- **不得加入「用於 Mahō Shōjo 的取材建議」一類的章節。** 使用者已明確排除。
- 所有 Python 指令用 `.venv/Scripts/python.exe`（Windows 路徑，Git Bash 下照樣可執行）。
- 每個 Task 結束時 commit，commit message 用繁體中文，並附下列兩行：

```
Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_018jhDXf9VLWurb8g4gWSKYb
```

---

## 17 部作品對照表

Task 2、3、5、6、7、8 都從這張表取值。`pact_mapping` 只填規則書自己寫出的對應（`docs/src/content/docs/rules/pacts.md` 第 19／21／23 行），其餘一律 `null`，**不得自行歸類**。

| id | title_zh | title_native（ja 維基條目名，須查證） | year | origin（預期值，以來源查證為準） | pact_mapping | cited_in |
| --- | --- | --- | --- | --- | --- | --- |
| `sailor-moon` | 美少女戰士 | 美少女戦士セーラームーン | 1991 | 漫畫改編 | 正義騎士 | introduction.md, pacts.md, friendship-romance.md |
| `magic-knight-rayearth` | 魔法騎士雷阿斯 | 魔法騎士レイアース | 1994 | 漫畫改編 | null | introduction.md |
| `cardcaptor-sakura` | 庫洛魔法使 | カードキャプターさくら | 1996 | 漫畫改編 | 光明子女 | introduction.md, pacts.md |
| `tokyo-mew-mew` | 東京喵喵 | 東京ミュウミュウ | 2002 | 漫畫改編 | null | introduction.md |
| `mai-hime` | 舞-HiME | 舞-HiME | 2004 | 原創動畫 | null | introduction.md |
| `lyrical-nanoha` | 魔法少女奈葉 | 魔法少女リリカルなのは | 2004 | 遊戲改編 | 光明子女 | introduction.md, pacts.md, friendship-romance.md |
| `precure` | 光之美少女 | プリキュアシリーズ | 2004 | 玩具企劃 | 正義騎士 | introduction.md, pacts.md |
| `shakugan-no-shana` | 灼眼的夏娜 | 灼眼のシャナ | 2005 | 輕小說改編 | null | introduction.md |
| `kampfer` | 肯普法 | けんぷファー | 2009 | 輕小說改編 | null | introduction.md |
| `toaru-kagaku-no-railgun` | 科學超電磁砲 | とある科学の超電磁砲 | 2009 | 漫畫改編 | null | introduction.md |
| `madoka-magica` | 魔法少女小圓 | 魔法少女まどか☆マギカ | 2011 | 原創動畫 | 契約傀儡 | introduction.md, pacts.md, friendship-romance.md |
| `mahou-shoujo-ikusei-keikaku` | 魔法少女育成計畫 | 魔法少女育成計画 | 2012 | 輕小說改編 | null | introduction.md |
| `symphogear` | 戰姬絕唱 Symphogear | 戦姫絶唱シンフォギア | 2013 | 原創動畫 | null | introduction.md |
| `kill-la-kill` | Kill la Kill | キルラキル | 2013 | 原創動畫 | null | introduction.md |
| `yuki-yuna-wa-yusha-de-aru` | 結城友奈是勇者 | 結城友奈は勇者である | 2014 | 原創動畫 | 契約傀儡 | introduction.md, pacts.md |
| `sailor-moon-crystal` | 美少女戰士 Crystal | 美少女戦士セーラームーン Crystal | 2014 | 漫畫改編 | null | introduction.md |
| `mahou-shoujo-site` | 魔法少女網站 | 魔法少女サイト | 2018 | 漫畫改編 | 契約傀儡 | pacts.md |

`cited_in` 欄在 frontmatter 中寫完整路徑，例如 `docs/src/content/docs/rules/introduction.md`。

---

## 共用條目模板

Task 2、3、5、6、7、8 每寫一個條目都**逐字套用**這個模板，只替換值。不要憑記憶重寫結構。

````markdown
---
id: <id>
title_zh: <繁中片名，取自 17 部作品對照表>
title_native: <日文原名>
title_romanized: <羅馬轉寫>
title_en: <英文通行名；查無填 null>
year: <西元年，數字>
years: "<系列仍延續者填區間如 2004—；單作填 null>"
media: [<電視動畫>, <劇場版>, <漫畫>, ……]
origin: <原創動畫 | 漫畫改編 | 輕小說改編 | 遊戲改編 | 玩具企劃>
studio: [<製作公司，日文原名>]
key_staff:
  監督: <姓名，日文原名>
  シリーズ構成: <姓名>
  キャラクターデザイン: <姓名>
pact_mapping: <光明子女 | 正義騎士 | 契約傀儡 | null>
cited_in:
  - docs/src/content/docs/rules/<檔名>.md
source:
  wiki: <ja 維基 URL>
  wiki_lang: ja
  wiki_secondary: <系列作的各作品條目 URL；無則 null>
  retrieved: <YYYY-MM-DD，執行當日>
  license: CC BY-SA 4.0
  extra:
    - title: <來源原文標題>
      publisher: <媒體或官方名稱>
      url: <URL；典藏版本填典藏網址>
      archived: <true | false>
      retrieved: <YYYY-MM-DD>
tags: [<關鍵詞>]
---

## 概要

（三到五句繁體中文：這是什麼作品、為什麼被規則書引為參考。）

## 作品含意

（主題、母題、作品在說什麼。每則非繁中材料寫成下列兩段一組：）

> （原文逐字抄錄，保留原標點）

（該段的繁體中文譯文。）

## 設計概念

（企劃緣起、製作意圖、角色與美術設計概念、系列定位。體例同上。）

## 劇本設計

（系列構成、敘事結構、腳本手法、關鍵轉折的設計。體例同上。）

## 其餘重要脈絡

（播映沿革、續作、評價與影響，以繁體中文摘要，不逐段對譯。）

## 專有名詞對照

| 原文 | 羅馬轉寫 | 繁體中文 | 說明 |
| --- | --- | --- | --- |

## 來源與授權

- 維基百科（日語）〈<原文條目名>〉，<URL>，擷取日期 <YYYY-MM-DD>。授權：CC BY-SA 4.0。
- <非維基來源逐筆列出：標題、發行者、URL、擷取日期；典藏版本註明「網際網路典藏館」>
````

### 查無材料時的寫法

三軸中某一軸確實查不到可佐證的材料時，該節寫成：

```markdown
## 設計概念

:::note[查證結果]
已查日語維基百科〈<條目名>〉全文、官方網站（<URL>，<狀態：現存／已失效，走網際網路典藏館>）、<列出實際查過的其他來源>，未見製作方對本作設計概念的具體說明。
:::
```

**必須先實際查過官方網站與可檢索的訪談，才能寫這個區塊。** 只查了維基就下結論，是魔女庫 Lutzelfrau 事件重演。

### 每個條目的取材流程（六步，固定）

1. 建 jobs 檔（**用 Write 工具建，不要用 shell 參數傳日文標題**，Git Bash 在 Windows 上會弄壞編碼）：

```
ja	<日文條目名>	<id>-ja
```

寫到 `.cache/jobs-<id>.tsv`，然後：

```bash
.venv/Scripts/python.exe scripts/fetch_wiki.py .cache/jobs-<id>.tsv
```

輸出在 `.cache/wiki/<id>-ja.txt`。若印出 `MISS`，依腳本列出的站內候選修正標題重跑——條目名可能是重導向或消歧義頁。

2. 讀 `.cache/wiki/<id>-ja.txt`，找〈概要〉〈作風〉〈テーマ〉〈制作〉〈評価〉等與三軸相關的章節。
3. **檢查引文是否被模板剝除**：看到「……と述べている：」「……と語る。」後面接空白，或引文沒有出處，就是 `{{Quotation}}`／`{{Cquote}}`／`{{Blockquote}}` 被純文字擷取吃掉了。改取原始碼補回：

```bash
curl -s "https://ja.wikipedia.org/w/index.php?title=<URL編碼的條目名>&action=raw" -o .cache/wiki/<id>-ja-raw.txt
```

4. 以 WebSearch 找製作方訪談與官方企劃文，關鍵詞範例：`<日文原名> 監督 インタビュー`、`<日文原名> 脚本 インタビュー`、`<日文原名> 企画 経緯`、`<日文原名> 公式サイト`。以 WebFetch 取內容。2002—2009 年的官方網站多已失效，改查 `https://web.archive.org/web/2010/<原網址>`。
5. 依模板寫條目到 `reference/works/entries/<id>.md`。
6. 驗證並 commit（每個 Task 的步驟裡有確切指令）。

---

## File Structure

| 檔案 | 責任 |
| --- | --- |
| `scripts/check_reference.py`（改） | 全 `reference/` 的書寫規範與 frontmatter 驗證。改為依路徑前綴分流兩套 schema |
| `scripts/build_works_indexes.py`（新） | 只負責 `reference/works/` 的四份產生檔。不與魔女庫的產生器共用程式碼——兩者的分組軸完全不同，強行共用會讓兩邊都變複雜 |
| `reference/works/entries/<id>.md`（新，17 檔） | 一部作品一檔，自足，不依賴其他條目 |
| `reference/works/README.md`（新） | 子庫說明、來源政策、劇透警告、維護指令 |
| `reference/works/INDEX.md`、`indexes/by-pact.md`、`indexes/by-origin.md`、`name-glossary.md`（新，產生） | 由腳本產生，**不得手改** |
| `reference/README.md`（改） | 改寫為兩個子庫的總覽 |

---

## Task 1: `check_reference.py` 支援 works 子庫的 schema

**Files:**
- Modify: `scripts/check_reference.py:42-52`（`REQUIRED_FIELDS`）、`:136-146`（`cjk_entry` 判斷）、`:115`（`check` 簽章）、`:177-196`（`main`）
- Test fixture（暫時檔，Task 結束前刪除）：`reference/works/entries/_fixture.md`

**Interfaces:**
- Consumes: 無（第一個 Task）
- Produces: `schema_for(rel: str) -> list[str] | None` — 依 repo 相對路徑回傳該檔的必填欄位清單，非條目檔回傳 `None`。後續所有 Task 的驗證步驟都依賴這支函式正確辨識 `reference/works/entries/`。

- [ ] **Step 1: 建立會暴露兩個缺陷的 fixture**

用 Write 工具建 `reference/works/entries/_fixture.md`（目錄需先建立）。這個 fixture 刻意**缺少 `year` 與 `origin`**，且含兩個日文新字體漢字（`体`、`声`），它們的字形與簡體字相同：

```markdown
---
id: fixture
title_zh: 測試條目
title_native: テスト
source:
  wiki: https://ja.wikipedia.org/wiki/テスト
  wiki_lang: ja
  retrieved: 2026-09-12
---

## 制作体制（製作體制）

| 原文 | 羅馬轉寫 | 繁體中文 | 說明 |
| --- | --- | --- | --- |
| 声優 | seiyū | 聲優 | 測試 |
```

- [ ] **Step 2: 執行檢查器，確認兩個缺陷都在**

Run: `.venv/Scripts/python.exe scripts/check_reference.py reference/works/entries/_fixture.md`

Expected（逐字比對）：

```
FAIL reference/works/entries/_fixture.md
     - 第 11 行出現簡體字：体
     - 第 15 行出現簡體字：声

共檢查 1 個檔案，1 個有問題。
```

兩個缺陷各自的意義：報出的兩行是**誤判**（日文原文被當成簡體字）；而缺少 `year`、`origin` **完全沒被報出來**（frontmatter 靜默跳過驗證）。兩者都要修掉。

- [ ] **Step 3: 把 `REQUIRED_FIELDS` 改成依路徑分流的對照表**

把 `scripts/check_reference.py` 第 42—52 行的 `REQUIRED_FIELDS` 整段換成：

```python
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
```

- [ ] **Step 4: 讓 `check()` 收必填欄位清單而非布林值**

把 `def check(path, is_entry):` 改成 `def check(path, required):`，並把其後的

```python
    if is_entry:
        fm = frontmatter_of(text)
        if fm is None:
            problems.append("缺少 YAML frontmatter")
        else:
            for field in REQUIRED_FIELDS:
```

改成

```python
    if required is not None:
        fm = frontmatter_of(text)
        if fm is None:
            problems.append("缺少 YAML frontmatter")
        else:
            for field in required:
```

其餘不動（`retrieved` 的檢查兩套 schema 都適用，留在原處）。

- [ ] **Step 5: 讓日文原文的豁免認得 works 子庫的語言欄位**

把 `cjk_entry` 的判斷式改成：

```python
    fm_text = frontmatter_of(text) or ""
    cjk_entry = generated or bool(
        re.search(r"^language:\s*[\"']?(ja|zh|ko)[\"']?\s*$", fm_text, re.M)
        # works 子庫的 schema 沒有頂層 language，語言記在 source.wiki_lang。
        # 不認這個欄位的話，日文原文中不含假名的純漢字（章節標題的「制作」、
        # 名詞對照表的「体」「声」「実」）會被誤判為簡體字，逼得條目去改動原文
        # 以通過檢查——魔女庫第三批踩過這個坑。
        or re.search(r"^\s+wiki_lang:\s*[\"']?(ja|zh|ko)[\"']?\s*$", fm_text, re.M))
```

- [ ] **Step 6: 讓 `main()` 改用 `schema_for()`**

把 `main()` 裡的

```python
        # 索引與說明檔沒有 frontmatter，只檢查文字規範
        is_entry = (
            "/regions/" in rel
            or "/sources-and-law/" in rel
            or "/concepts/" in rel
        )
        problems = check(path, is_entry)
```

改成

```python
        # 索引與說明檔沒有 frontmatter，schema_for 回傳 None，只檢查文字規範
        problems = check(path, schema_for(rel))
```

- [ ] **Step 7: 重跑 fixture，確認誤判消失、缺欄位被抓出來**

Run: `.venv/Scripts/python.exe scripts/check_reference.py reference/works/entries/_fixture.md`

Expected：

```
FAIL reference/works/entries/_fixture.md
     - frontmatter 缺少欄位：year
     - frontmatter 缺少欄位：origin

共檢查 1 個檔案，1 個有問題。
```

簡體字兩行必須消失，缺欄位兩行必須出現。若簡體字誤判還在，是 Step 5 的正規表示式沒對上 `wiki_lang` 的縮排。

- [ ] **Step 8: 補上缺的欄位，確認轉綠**

在 fixture 的 frontmatter 中 `title_native` 之後插入兩行：

```yaml
year: 2026
origin: 原創動畫
```

Run: `.venv/Scripts/python.exe scripts/check_reference.py reference/works/entries/_fixture.md`
Expected: `ok   reference/works/entries/_fixture.md` 與 `共檢查 1 個檔案，0 個有問題。`

- [ ] **Step 9: 確認魔女庫 140 條沒有回歸**

Run: `.venv/Scripts/python.exe scripts/check_reference.py`
Expected: 最後一行為 `共檢查 147 個檔案，0 個有問題。`（146 個既有檔 + fixture。146 是實測值——`check_reference.py` 的 `SKIP_DIRS` 會跳過 `reference/backlog/`，故少於該目錄的實際檔數。數字若與此不符，先確認是 fixture 造成的差異，不得為了對上數字去改條目）

- [ ] **Step 10: 刪除 fixture 並 commit**

```bash
rm -rf reference/works
.venv/Scripts/python.exe scripts/check_reference.py
```

Expected: `共檢查 146 個檔案，0 個有問題。`

```bash
git add scripts/check_reference.py
git commit -F - <<'MSG'
check_reference 支援參考作品庫的 frontmatter schema

必填欄位改為依路徑前綴分流；日文原文的簡體字豁免補上
source.wiki_lang 判斷，否則新子庫的日文純漢字會被誤判。

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_018jhDXf9VLWurb8g4gWSKYb
MSG
```

---

## Task 2: 樣板條目（材料最厚）—— `madoka-magica`

這條先做，因為《魔法少女小圓》的製作訪談與主題論述在 17 部中最豐厚，用它把「材料充足」的體例定下來。

**Files:**
- Create: `reference/works/entries/madoka-magica.md`

**Interfaces:**
- Consumes: Task 1 的 `schema_for()`——本條目必須被辨識為 works 條目並通過 frontmatter 驗證
- Produces: 本檔即後續 15 條的體例基準。Task 3 之後的每個條目都應在結構上與它一致

- [ ] **Step 1: 擷取日語維基原文**

用 Write 工具建 `.cache/jobs-madoka.tsv`，內容一行（欄位以 tab 分隔）：

```
ja	魔法少女まどか☆マギカ	madoka-magica-ja
```

Run: `.venv/Scripts/python.exe scripts/fetch_wiki.py .cache/jobs-madoka.tsv`
Expected: `OK   madoka-magica-ja             ja/魔法少女まどか☆マギカ  chars=<數字>`

- [ ] **Step 2: 讀擷取結果，標出三軸材料**

讀 `.cache/wiki/madoka-magica-ja.txt`。找出對應三軸的章節，預期分別落在：〈概要〉〈作風〉〈テーマ〉→ 作品含意；〈企画〉〈制作〉〈キャラクター〉→ 設計概念；〈ストーリー構成〉〈各話〉〈脚本〉→ 劇本設計。**實際章節名以擷取結果為準，不要套用這裡的預期。**

- [ ] **Step 3: 檢查引文是否被模板剝除**

搜尋擷取結果中「と述べ」「と語」「によれば」等引導語，若其後接空白或引文無出處，取原始碼補回：

```bash
curl -s "https://ja.wikipedia.org/w/index.php?title=%E9%AD%94%E6%B3%95%E5%B0%91%E5%A5%B3%E3%81%BE%E3%81%A9%E3%81%8B%E2%98%86%E3%83%9E%E3%82%AE%E3%82%AB&action=raw" -o .cache/wiki/madoka-magica-ja-raw.txt
```

在原始碼中搜 `{{Quotation`、`{{Cquote`、`{{Blockquote`，把被剝除的引文正文與 `author`／`source` 參數取回。

- [ ] **Step 4: 找製作方訪談與官方資料**

以 WebSearch 查下列關鍵詞，各取可用者以 WebFetch 讀取全文：

- `魔法少女まどか☆マギカ 虚淵玄 インタビュー 企画`
- `魔法少女まどか☆マギカ 新房昭之 インタビュー`
- `魔法少女まどか☆マギカ 公式サイト madoka-magica.com`

每筆可用來源記下標題、發行者、URL、擷取日，供 frontmatter 的 `source.extra` 與「來源與授權」一節使用。

- [ ] **Step 5: 依共用條目模板寫出條目**

寫 `reference/works/entries/madoka-magica.md`。取值來自「17 部作品對照表」的 `madoka-magica` 列。三軸各節的每則非繁中材料，一律寫成 `> 原文逐字` 緊接一段繁中對譯。

- [ ] **Step 6: 驗證**

Run: `.venv/Scripts/python.exe scripts/check_reference.py reference/works/entries/madoka-magica.md`
Expected: `ok   reference/works/entries/madoka-magica.md` 與 `共檢查 1 個檔案，0 個有問題。`

再人工確認三項（腳本查不出來的）：
- 三軸每節都有內容，且每則非繁中材料都附了原文與對譯，無只譯不附原文者。
- `pact_mapping` 為 `契約傀儡`，與 `pacts.md` 第 23 行一致。
- `cited_in` 列的三個檔案實際存在且確實提及本作：
  `grep -l "魔法少女小圓" docs/src/content/docs/rules/introduction.md docs/src/content/docs/rules/pacts.md docs/src/content/docs/rules/friendship-romance.md`

- [ ] **Step 7: Commit**

```bash
git add reference/works/entries/madoka-magica.md
git commit -F - <<'MSG'
參考作品庫樣板條目：魔法少女小圓

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_018jhDXf9VLWurb8g4gWSKYb
MSG
```

---

## Task 3: 樣板條目（材料最薄）—— `tokyo-mew-mew`

《東京喵喵》是 17 部中維基條目最薄、官方網站（2002 年）多半已失效的一部。用它驗證「查無材料」的體例——**這個 Task 的成功標準之一，是允許三軸中有一軸寫成查證結果區塊**。

**Files:**
- Create: `reference/works/entries/tokyo-mew-mew.md`

**Interfaces:**
- Consumes: Task 2 定下的體例
- Produces: 「查無材料」區塊的實際樣本，後續條目遇到同樣情形時照此寫

- [ ] **Step 1: 擷取日語維基原文**

用 Write 工具建 `.cache/jobs-mew.tsv`：

```
ja	東京ミュウミュウ	tokyo-mew-mew-ja
```

Run: `.venv/Scripts/python.exe scripts/fetch_wiki.py .cache/jobs-mew.tsv`
Expected: `OK   tokyo-mew-mew-ja             ja/東京ミュウミュウ  chars=<數字>`

- [ ] **Step 2: 量測篇幅，判斷哪幾軸可能要寫查無**

記下 Step 1 印出的 `chars=` 實際字數。**不要用 `prop=info` 的 `length` 判斷篇幅**——那是 wikitext 位元組數，日文約為純文字字數的 3.4—7.6 倍。

- [ ] **Step 3: 查官方網站（含典藏版本）**

以 WebSearch 查 `東京ミュウミュウ 公式サイト テレビ東京`，取得原網址後，若已失效改查典藏版本：

```
https://web.archive.org/web/2003/<原網址>
```

以 WebFetch 讀取。記下狀態（現存／已失效走典藏館）供查證結果區塊引用。

- [ ] **Step 4: 查製作方訪談**

WebSearch 關鍵詞：`東京ミュウミュウ 吉田玲子 インタビュー`、`東京ミュウミュウ 企画 経緯 なかよし`、`東京ミュウミュウ アニメ 監督 インタビュー`。

**查得到就用，查不到就照實寫。** 這一步的目的是讓查證結果區塊能列出實際查過的來源清單，不是硬要找到東西。

- [ ] **Step 5: 依共用條目模板寫出條目**

寫 `reference/works/entries/tokyo-mew-mew.md`。取值來自「17 部作品對照表」的 `tokyo-mew-mew` 列。三軸中若有一軸確實查無材料，用「查無材料時的寫法」的 `:::note[查證結果]` 區塊，區塊內必須逐一列出 Step 3、Step 4 實際查過的來源與其狀態。

- [ ] **Step 6: 驗證**

Run: `.venv/Scripts/python.exe scripts/check_reference.py reference/works/entries/tokyo-mew-mew.md`
Expected: `ok   reference/works/entries/tokyo-mew-mew.md` 與 `共檢查 1 個檔案，0 個有問題。`

人工確認：三軸中任何寫成查證結果區塊的一節，區塊內列出的來源都是**實際查過**的，且 `pact_mapping` 為 `null`。

- [ ] **Step 7: Commit**

```bash
git add reference/works/entries/tokyo-mew-mew.md
git commit -F - <<'MSG'
參考作品庫樣板條目：東京喵喵

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_018jhDXf9VLWurb8g4gWSKYb
MSG
```

- [ ] **Step 8: 交使用者確認體例**

停下來，把 `madoka-magica.md` 與 `tokyo-mew-mew.md` 兩條交使用者看，確認體例（三軸的切分、原文對譯的密度、查無材料的寫法）再往下做。**未獲確認不得開始 Task 5。**

---

## Task 4: 索引產生器與子庫 README

此時已有 2 條條目可供產生器讀取，先把產生器做好，後續每批完成都能立刻重跑驗證。

**Files:**
- Create: `scripts/build_works_indexes.py`
- Create: `reference/works/README.md`
- Generated: `reference/works/INDEX.md`、`reference/works/indexes/by-pact.md`、`reference/works/indexes/by-origin.md`、`reference/works/name-glossary.md`

**Interfaces:**
- Consumes: `reference/works/entries/*.md` 的 frontmatter 與「## 專有名詞對照」表格
- Produces: `collect_works() -> list[dict]` — 回傳各條目 frontmatter 的字典，另含 `_path`（相對 `reference/works/` 的路徑）與 `_glossary`（名詞對照表的資料列）。Task 9 的收尾驗證會重跑本腳本。

- [ ] **Step 1: 寫索引產生器**

建 `scripts/build_works_indexes.py`。frontmatter 解析與名詞表抓取直接沿用 `build_reference_indexes.py` 既有的 `parse_frontmatter`、`parse_glossary`、`write` 三支函式——它們與魔女庫的 schema 無關，import 進來即可，不要重寫：

```python
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


def group(entries, keyfunc):
    buckets = {}
    for e in entries:
        buckets.setdefault(keyfunc(e), []).append(e)
    return buckets


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
    for pact in PACT_ORDER + [PACT_UNSPECIFIED]:
        if pact not in by_pact:
            continue
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
```

- [ ] **Step 2: 執行產生器，確認四份檔案產出**

Run: `.venv/Scripts/python.exe scripts/build_works_indexes.py`
Expected: 四行 `寫入 reference/works/...`，最後一行 `共處理 2 部作品。`

- [ ] **Step 3: 確認索引的分組正確**

`reference/works/INDEX.md` 應只有「二〇一〇年代」與「二〇〇〇年代」兩節（目前只有 2011 與 2002 兩條）。
`reference/works/indexes/by-pact.md` 應有「契約傀儡（1 部）」與「規則書未指定（1 部）」兩節。

- [ ] **Step 4: 寫子庫 README**

建 `reference/works/README.md`，須包含下列各節（內容以本計畫的 spec 為準）：

- 開頭第一個區塊是劇透警告：本庫「劇本設計」一節含完整劇透，《魔法少女小圓》《結城友奈是勇者》《舞-HiME》《魔法少女網站》尤其嚴重。
- 「從哪裡開始」表格：INDEX.md、兩份交叉索引、name-glossary.md 的連結與說明。
- 「條目的組成」：三軸各自的定義，以及「查無材料」的寫法與其理由。
- 「來源政策」：主幹為日語維基（CC BY-SA 4.0），補強為官方網站與製作方訪談（節錄引用）；失效網站走網際網路典藏館並標註。
- 「與魔女傳說庫的關係」：兩庫平行獨立，schema 不共用，名詞總表不互相併入，皆不併入 Astro 網站。
- 「維護指令」：`check_reference.py` 與 `build_works_indexes.py` 的用法。

- [ ] **Step 5: 驗證並 commit**

Run: `.venv/Scripts/python.exe scripts/check_reference.py reference/works`
Expected: 全部 `ok`，`共檢查 7 個檔案，0 個有問題。`（2 條目 + README + INDEX + 2 索引 + name-glossary）

```bash
git add scripts/build_works_indexes.py reference/works
git commit -F - <<'MSG'
參考作品庫的索引產生器與子庫說明

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_018jhDXf9VLWurb8g4gWSKYb
MSG
```

---

## Task 5: 批 A —— 九〇年代 3 條

**Files:**
- Create: `reference/works/entries/sailor-moon.md`
- Create: `reference/works/entries/magic-knight-rayearth.md`
- Create: `reference/works/entries/cardcaptor-sakura.md`

**Interfaces:**
- Consumes: Task 2／3 定下的體例、Task 1 的 `schema_for()`
- Produces: 3 個條目檔，供 Task 9 的索引重建與交叉引用使用

- [ ] **Step 1: 三條各跑一次「每個條目的取材流程」六步**

取值來自「17 部作品對照表」對應列。三條的特別注意事項：

- `sailor-moon`：ja 維基的〈美少女戦士セーラームーン〉是**系列總條目**，動畫版另有〈美少女戦士セーラームーン (アニメ)〉。設計概念多在總條目、劇本設計多在動畫條目，主要來源記總條目，動畫條目記入 `wiki_secondary`。
- `magic-knight-rayearth`：原作為 CLAMP，注意區分漫畫版與 TV 動畫版的劇本差異（動畫第一部大幅擴寫），劇本設計一節須寫明所述為哪一版。
- `cardcaptor-sakura`：`pact_mapping` 為 `光明子女`，與 `pacts.md` 第 19 行一致。

- [ ] **Step 2: 逐條驗證**

```bash
.venv/Scripts/python.exe scripts/check_reference.py reference/works/entries/sailor-moon.md reference/works/entries/magic-knight-rayearth.md reference/works/entries/cardcaptor-sakura.md
```

Expected: 三個 `ok`，`共檢查 3 個檔案，0 個有問題。`

- [ ] **Step 3: 確認 `cited_in` 屬實**

```bash
grep -c "美少女戰士" docs/src/content/docs/rules/introduction.md docs/src/content/docs/rules/pacts.md docs/src/content/docs/rules/friendship-romance.md
grep -c "魔法騎士雷阿斯" docs/src/content/docs/rules/introduction.md
grep -c "庫洛魔法使" docs/src/content/docs/rules/introduction.md docs/src/content/docs/rules/pacts.md
```

Expected: 每個計數皆 ≥ 1。任何一個為 0，表示 `cited_in` 寫錯，回頭改條目。

- [ ] **Step 4: Commit**

```bash
git add reference/works/entries
git commit -F - <<'MSG'
參考作品庫批 A：九〇年代 3 部

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_018jhDXf9VLWurb8g4gWSKYb
MSG
```

---

## Task 6: 批 B —— 2004—2005 共 4 條

**Files:**
- Create: `reference/works/entries/mai-hime.md`
- Create: `reference/works/entries/lyrical-nanoha.md`
- Create: `reference/works/entries/precure.md`
- Create: `reference/works/entries/shakugan-no-shana.md`

**Interfaces:**
- Consumes: Task 2／3 定下的體例、Task 1 的 `schema_for()`
- Produces: 4 個條目檔

- [ ] **Step 1: 四條各跑一次「每個條目的取材流程」六步**

取值來自「17 部作品對照表」對應列。四條的特別注意事項：

- `mai-hime`：Sunrise 原創，劇本設計一節含重大劇透（中盤的類型翻轉）。
- `lyrical-nanoha`：源自成人遊戲《とらいあんぐるハート3》的外傳企劃，`origin` 為 `遊戲改編`，設計概念一節須交代這個出身。系列各作另有獨立條目，主要來源記〈魔法少女リリカルなのは〉，續作條目記入 `wiki_secondary`。`pact_mapping` 為 `光明子女`。
- `precure`：ja 維基條目名為〈プリキュアシリーズ〉（系列總條目），`years` 填 `"2004—"`。這是東映動畫的玩具企劃主導作，設計概念一節應涵蓋「肉搏戰」這個企劃起點。`pact_mapping` 為 `正義騎士`。
- `shakugan-no-shana`：輕小說改編，嚴格說不屬魔法少女類，但在規則書〈參考來源〉清單內，照收。概要一節說明它被列入的理由（角色關係）。

- [ ] **Step 2: 逐條驗證**

```bash
.venv/Scripts/python.exe scripts/check_reference.py reference/works/entries/mai-hime.md reference/works/entries/lyrical-nanoha.md reference/works/entries/precure.md reference/works/entries/shakugan-no-shana.md
```

Expected: 四個 `ok`，`共檢查 4 個檔案，0 個有問題。`

- [ ] **Step 3: 確認 `cited_in` 屬實**

```bash
grep -c "舞-HiME" docs/src/content/docs/rules/introduction.md
grep -c "魔法少女奈葉" docs/src/content/docs/rules/introduction.md docs/src/content/docs/rules/pacts.md docs/src/content/docs/rules/friendship-romance.md
grep -c "光之美少女" docs/src/content/docs/rules/introduction.md docs/src/content/docs/rules/pacts.md
grep -c "灼眼的夏娜" docs/src/content/docs/rules/introduction.md
```

Expected: 每個計數皆 ≥ 1。

- [ ] **Step 4: Commit**

```bash
git add reference/works/entries
git commit -F - <<'MSG'
參考作品庫批 B：2004—2005 共 4 部

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_018jhDXf9VLWurb8g4gWSKYb
MSG
```

---

## Task 7: 批 C —— 2009—2013 共 4 條

**Files:**
- Create: `reference/works/entries/kampfer.md`
- Create: `reference/works/entries/toaru-kagaku-no-railgun.md`
- Create: `reference/works/entries/mahou-shoujo-ikusei-keikaku.md`
- Create: `reference/works/entries/symphogear.md`

**Interfaces:**
- Consumes: Task 2／3 定下的體例、Task 1 的 `schema_for()`
- Produces: 4 個條目檔

- [ ] **Step 1: 四條各跑一次「每個條目的取材流程」六步**

取值來自「17 部作品對照表」對應列。四條的特別注意事項：

- `kampfer`：17 部中材料最薄的幾條之一，三軸很可能有一到兩軸要寫查證結果區塊。照 Task 3 定下的寫法辦，**不得推測補滿**。
- `toaru-kagaku-no-railgun`：〈とある魔術の禁書目録〉的外傳漫畫改編，設計概念一節須交代與本傳的關係。
- `mahou-shoujo-ikusei-keikaku`：輕小說改編，維基條目偏薄；官方網站與電擊文庫的作品頁是主要補強來源。
- `symphogear`：原創動畫，「歌唱即戰鬥」是企劃核心，設計概念一節應涵蓋這個起點。

- [ ] **Step 2: 逐條驗證**

```bash
.venv/Scripts/python.exe scripts/check_reference.py reference/works/entries/kampfer.md reference/works/entries/toaru-kagaku-no-railgun.md reference/works/entries/mahou-shoujo-ikusei-keikaku.md reference/works/entries/symphogear.md
```

Expected: 四個 `ok`，`共檢查 4 個檔案，0 個有問題。`

- [ ] **Step 3: 確認 `cited_in` 屬實**

```bash
grep -c "肯普法" docs/src/content/docs/rules/introduction.md
grep -c "科學超電磁砲" docs/src/content/docs/rules/introduction.md
grep -c "魔法少女育成計畫" docs/src/content/docs/rules/introduction.md
grep -c "Symphogear" docs/src/content/docs/rules/introduction.md
```

Expected: 每個計數皆 ≥ 1。

- [ ] **Step 4: Commit**

```bash
git add reference/works/entries
git commit -F - <<'MSG'
參考作品庫批 C：2009—2013 共 4 部

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_018jhDXf9VLWurb8g4gWSKYb
MSG
```

---

## Task 8: 批 D —— 2013—2018 共 4 條

**Files:**
- Create: `reference/works/entries/kill-la-kill.md`
- Create: `reference/works/entries/yuki-yuna-wa-yusha-de-aru.md`
- Create: `reference/works/entries/sailor-moon-crystal.md`
- Create: `reference/works/entries/mahou-shoujo-site.md`

**Interfaces:**
- Consumes: Task 2／3 定下的體例、Task 1 的 `schema_for()`
- Produces: 4 個條目檔，至此 17 條齊備

- [ ] **Step 1: 四條各跑一次「每個條目的取材流程」六步**

取值來自「17 部作品對照表」對應列。四條的特別注意事項：

- `kill-la-kill`：TRIGGER 首部電視動畫，今石洋之與中島かずき的訪談材料豐厚。嚴格說不屬魔法少女類但在〈參考來源〉清單內，概要一節說明列入理由（變身與服裝作為力量來源）。
- `yuki-yuna-wa-yusha-de-aru`：跨媒體企劃（動畫與小說同步展開），劇本設計一節含重大劇透。`pact_mapping` 為 `契約傀儡`。
- `sailor-moon-crystal`：2014 年重製版，**設計概念一節的重點是「重製的意圖」——忠於武內直子原作而非重拍 1992 年動畫版**。與 `sailor-moon` 條目互為參照，但交叉連結留給 Task 9 統一補，此處不自行加。
- `mahou-shoujo-site`：僅由 `pacts.md` 提及（不在〈參考來源〉清單內），`cited_in` 只列 `pacts.md` 一項。`pact_mapping` 為 `契約傀儡`。劇本設計一節含重大劇透。

- [ ] **Step 2: 逐條驗證**

```bash
.venv/Scripts/python.exe scripts/check_reference.py reference/works/entries/kill-la-kill.md reference/works/entries/yuki-yuna-wa-yusha-de-aru.md reference/works/entries/sailor-moon-crystal.md reference/works/entries/mahou-shoujo-site.md
```

Expected: 四個 `ok`，`共檢查 4 個檔案，0 個有問題。`

- [ ] **Step 3: 確認 `cited_in` 屬實**

```bash
grep -c "Kill la Kill" docs/src/content/docs/rules/introduction.md
grep -c "結城友奈是勇者" docs/src/content/docs/rules/introduction.md docs/src/content/docs/rules/pacts.md
grep -c "美少女戰士 Crystal" docs/src/content/docs/rules/introduction.md
grep -c "魔法少女網站" docs/src/content/docs/rules/pacts.md
```

Expected: 每個計數皆 ≥ 1。另確認 `魔法少女網站` **不在** `introduction.md` 中：
`grep -c "魔法少女網站" docs/src/content/docs/rules/introduction.md` Expected: `0`

- [ ] **Step 4: Commit**

```bash
git add reference/works/entries
git commit -F - <<'MSG'
參考作品庫批 D：2013—2018 共 4 部

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_018jhDXf9VLWurb8g4gWSKYb
MSG
```

---

## Task 9: 收尾 —— 索引重建、交叉引用、兩份 README、全庫驗收

交叉引用**一律在這個 Task 統一單向補上**。魔女庫第三批的教訓：平行批次同時互改會產生競態，正確作法是先定基準、單向改、事後 grep 驗證。

**Files:**
- Modify: `reference/README.md`（改寫為兩個子庫的總覽）
- Modify: `reference/works/entries/*.md`（僅補交叉連結）
- Regenerated: `reference/works/INDEX.md`、`indexes/by-pact.md`、`indexes/by-origin.md`、`name-glossary.md`

**Interfaces:**
- Consumes: Task 4 的 `collect_works()`、全部 17 個條目檔
- Produces: 完成的子庫

- [ ] **Step 1: 重建索引**

Run: `.venv/Scripts/python.exe scripts/build_works_indexes.py`
Expected: 四行 `寫入 reference/works/...`，最後一行 `共處理 17 部作品。`

若不是 17，先查 `reference/works/entries/` 的檔數與各檔的 `id` 欄位是否齊全。

- [ ] **Step 2: 確認盟約索引的分組數字**

開啟 `reference/works/indexes/by-pact.md`，確認四節的數字為：光明子女 2 部、正義騎士 2 部、契約傀儡 3 部、規則書未指定 10 部。合計 17。

數字不符表示某條的 `pact_mapping` 填錯——對照「17 部作品對照表」修正條目後重跑 Step 1。

- [ ] **Step 3: 單向補上交叉引用**

只補三組確實互為參照的，一律在**後出的一方**指向先出的一方，不做雙向：

- `sailor-moon-crystal.md` → 在「設計概念」一節提及 1992 年動畫版之處，連到 `[美少女戰士](sailor-moon.md)`
- `precure.md` → 在「設計概念」一節談系列定位之處，連到 `[美少女戰士](sailor-moon.md)`
- `mahou-shoujo-site.md` → 在「作品含意」一節談黑暗系轉向之處，連到 `[魔法少女小圓](madoka-magica.md)`

- [ ] **Step 4: 改寫 `reference/README.md` 為兩庫總覽**

現行 `reference/README.md` 通篇是魔女傳說庫的說明。改寫方式：保留既有的全部內容，但在開頭加一節「兩個子庫」，說明本目錄下有兩個各自獨立的資料庫：

- 魔女傳說參考資料庫（`regions/`、`concepts/`、`sources-and-law/` 等，即本檔其餘內容所述）
- 參考作品分析資料庫（`works/`，說明見 [works/README.md](works/README.md)）

並註明：兩庫 schema 不共用、名詞總表不互相併入、皆不併入 Astro 網站。**不要刪除既有的擷取陷阱、來源政策等章節**——那些是魔女庫累積的實作教訓。

- [ ] **Step 5: 全庫驗證**

```bash
.venv/Scripts/python.exe scripts/check_reference.py
```

Expected: 最後一行 `共檢查 168 個檔案，0 個有問題。`（魔女庫 146 + works 22：17 條目 + README + INDEX + 2 索引 + name-glossary）

- [ ] **Step 6: 確認魔女庫的產生器沒有被污染**

```bash
.venv/Scripts/python.exe scripts/build_reference_indexes.py
git diff --stat reference/INDEX.md reference/indexes reference/name-glossary.md
```

Expected: `git diff --stat` 無輸出。魔女庫的 `collect()` 是白名單式的，不應看到 `works/`；有輸出表示 Task 1 或 Task 4 動到了不該動的東西。

- [ ] **Step 7: 確認 `glossary.json` 未被更動**

```bash
git diff --stat glossary.json
```

Expected: 無輸出。

- [ ] **Step 8: 確認無死連結**

```bash
grep -roh "](\([^)]*\.md\)" reference/works | sed 's/^](//' | sort -u
```

逐一確認每個相對路徑實際存在（從其所在目錄解析）。

- [ ] **Step 9: 確認三軸完整**

```bash
for f in reference/works/entries/*.md; do
  for h in "## 作品含意" "## 設計概念" "## 劇本設計"; do
    grep -q "^$h$" "$f" || echo "MISSING $h in $f"
  done
done
```

Expected: 無輸出。

- [ ] **Step 10: Commit**

```bash
git add reference scripts
git commit -F - <<'MSG'
參考作品庫收尾：索引重建、交叉引用與兩庫總覽

17 部作品齊備，補上三組單向交叉引用，reference/README.md
改寫為兩個子庫的總覽。

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_018jhDXf9VLWurb8g4gWSKYb
MSG
```

---

## 驗收條件（對應 spec 第 10 節）

- [ ] `reference/works/entries/` 下 17 個條目檔皆存在，frontmatter 必填欄位齊全且 `source.retrieved` 有值（由 `check_reference.py` 保證）
- [ ] 每條的三軸皆有內容，或以查證結果區塊明載查過哪些來源（Task 9 Step 9 查標題存在；內容需人工確認）
- [ ] 所有非繁體中文材料 100% 附原文逐字引用與繁中對譯，無只譯不附原文者（人工確認）
- [ ] `pact_mapping` 只在 7 條上有值，其餘為 `null`（Task 9 Step 2）
- [ ] `cited_in` 指向的規則書路徑實際存在且該檔確實提及該作品（各批的 Step 3）
- [ ] `scripts/check_reference.py` 全庫零問題（Task 9 Step 5）
- [ ] `INDEX.md` 與兩份交叉索引涵蓋全部 17 條，無死連結（Task 9 Step 1、Step 8）
- [ ] `glossary.json` 未被更動（Task 9 Step 7）
- [ ] 魔女傳說庫既有的 146 個受檢檔案未被更動（Task 9 Step 6）
