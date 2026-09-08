# 魔女傳說參考資料庫 設計規格

- 日期：2026-09-08
- 狀態：已核准（使用者確認，不含「取材建議」一節）
- 產出位置：`reference/`

## 1. 目的

蒐集歷史上的魔女／女巫傳說，**以該傳說發源語言的維基百科條目為主要來源**，保存原文並完整翻譯成繁體中文，依「地區／語系／時代」三軸整理，供 Mahō Shōjo 專案作為背景資料查閱。

本資料庫**不併入 Astro 網站**，是 repo 根目錄下的獨立資料夾。

## 2. 範圍

- 收錄類型：民俗／神話中的魔女形象 + 真實的女巫審判事件 + 相關文獻與法制。
- 首批規模：35 條。
- 原文粒度：導言與關鍵章節**逐段原文＋逐段繁中對譯**；其餘章節以繁中摘要涵蓋，並附原文連結。
- **不含**「用於 Mahō Shōjo 的取材建議」一節（使用者明確排除）。

## 3. 目錄結構

```
reference/
  README.md                    總覽、使用說明、CC BY-SA 授權標註
  INDEX.md                     主索引（依地區）
  indexes/
    by-language-family.md      語系交叉索引
    by-era.md                  時代交叉索引
  name-glossary.md             原文專有名詞 ↔ 繁中對照總表
  regions/
    01-british-isles/
    02-western-europe/
    03-central-europe/
    04-northern-europe/
    05-southern-europe/
    06-eastern-europe/
    07-west-asia-north-africa/
    08-east-asia/
    09-sub-saharan-africa/
    10-americas/
  sources-and-law/             跨地區的文獻與法制
```

檔名一律 kebab-case 的拉丁轉寫 id，例如 `baba-yaga.md`、`bamberger-hexenprozesse.md`。

## 4. 條目模板

```markdown
---
id: baba-yaga
title_zh: 芭芭雅嘎
title_native: Баба-яга
title_romanized: Baba-yaga          # 非拉丁字母時必填，否則省略
region: 東歐
countries: [俄羅斯, 烏克蘭, 白俄羅斯]
language: ru
language_family: 印歐語系／斯拉夫語族／東斯拉夫語支
era: 中世紀晚期—近現代
era_bucket: early-modern            # ancient | medieval | early-modern | modern
year_range: "1755—"                 # 有明確年代者填；純神話填 null
type: folklore                      # folklore | trial | person | text-law
source:
  wiki: https://ru.wikipedia.org/wiki/Баба-яга
  wiki_lang: ru
  retrieved: 2026-09-08
  license: CC BY-SA 4.0
  fallback_reason: null             # 非發源語言來源時說明原因
tags: [森林, 食人, 雞腳屋, 引路者]
---

## 概要

（三到五句繁體中文，說明這是什麼、為何重要。）

## 原文與對照翻譯

### 導言

> （原文段落，逐字抄錄，保留原標點）

（該段的繁體中文譯文。）

> （下一段原文）

（譯文。）

### <原文章節標題>（繁中章節名）

（同上，逐段對照。）

## 其餘章節摘要

（原文條目中未逐段對譯的章節，以繁體中文摘要涵蓋，逐節列出。）

## 專有名詞對照

| 原文 | 羅馬轉寫 | 繁體中文 | 說明 |
| --- | --- | --- | --- |

## 來源與授權

- 維基百科（<語言>）〈<原文條目名>〉，<URL>，擷取日期 2026-09-08。
- 授權：CC BY-SA 4.0。原文引用依該授權標示出處，譯文為本專案自行翻譯。
```

## 5. 取得原文的方法

以維基百科 API 取純文字，避免 wikitext 標記混入引文：

```
https://<lang>.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1&redirects=1&format=json&titles=<TITLE>
```

需要原始標記（表格、模板參數）時再取 `?action=raw`。

## 6. 翻譯與寫作規範

沿用專案的 Immutable Laws：

- **Law 6**：一律繁體中文（zh-TW），不得出現簡體字或中國大陸用語。
- **Law 8**：全形標點（：，。、；「」『』（）……），數字與拉丁文字用半形；省略號用 `……`。
- **Law 9**：罕用字、雙關、文化負載詞若影響語意或語氣，先向使用者提出 2～3 個候選再定案。
- 原文引文**逐字保留**，不修正原文的拼寫與標點。
- 譯文求信達，不過度在地化；避免以中文典故成語替換西文概念（見既有專案慣例）。
- 專有名詞**不寫入 `glossary.json`**（該檔為遊戲規則術語庫），統一收錄於 `reference/name-glossary.md`。

## 7. 來源政策

- 優先使用**傳說發源語言**的維基版本（俄語條目用 `ru`、巴斯克傳說用 `eu`／`es`、日本用 `ja`……）。
- 發源語言無條目或內容過於單薄時，退用最近的學術通行語版本（`es`／`pt`／`en`／`fr`／`de`），並於 frontmatter 的 `fallback_reason` 說明。
- 每條目必須記錄語言版本、URL、擷取日期。
- 維基百科內容為 CC BY-SA 4.0，`README.md` 統一標註授權與姓名標示方式。

## 8. 選錄清單（35 條）

| # | 地區 | 條目 | 原文語言 | 類型 |
| --- | --- | --- | --- | --- |
| 1 | 不列顛群島 | Alice Kyteler（1324，愛爾蘭） | en | trial |
| 2 | 不列顛群島 | North Berwick witch trials（1590–92） | en/sco | trial |
| 3 | 不列顛群島 | Pendle witches（1612） | en | trial |
| 4 | 不列顛群島 | Cailleach | gd/ga | folklore |
| 5 | 西歐 | Mélusine | fr | folklore |
| 6 | 西歐 | Affaire des poisons／La Voisin（1679） | fr | trial |
| 7 | 西歐 | Pierre de Lancre 與拉布爾獵巫（1609） | fr | trial |
| 8 | 中歐 | Bamberger Hexenprozesse（1626–31） | de | trial |
| 9 | 中歐 | Anna Göldi（1782） | de | person |
| 10 | 中歐 | Walpurgisnacht 與布洛肯山 | de | folklore |
| 11 | 中歐 | Frau Holle／Perchta | de | folklore |
| 12 | 北歐 | Mora trolldomsprocess（1668–76） | sv | trial |
| 13 | 北歐 | Vardø trolldomsprosessene（1621） | no | trial |
| 14 | 北歐 | Louhi 與《卡勒瓦拉》 | fi | folklore |
| 15 | 南歐 | Brujas de Zugarramurdi（1610） | es/eu | trial |
| 16 | 南歐 | Sorginak 與 Mari | eu | folklore |
| 17 | 南歐 | Benandanti | it | folklore |
| 18 | 南歐 | Κίρκη 喀爾刻 | el | folklore |
| 19 | 東歐 | Баба-яга | ru | folklore |
| 20 | 東歐 | 基輔禿山與 відьма | uk | folklore |
| 21 | 東歐 | Szegedi boszorkányperek（1728） | hu | trial |
| 22 | 西亞北非 | לילית 莉莉絲 | he | folklore |
| 23 | 西亞北非 | هاروت وماروت／السحر | ar | folklore |
| 24 | 東亞 | 山姥 | ja | folklore |
| 25 | 東亞 | 犬神 | ja | folklore |
| 26 | 東亞 | 巫蠱之禍（前 91） | zh | trial |
| 27 | 東亞 | 무당 巫堂 | ko | folklore |
| 28 | 非洲 | Àjẹ́（約魯巴） | yo | folklore |
| 29 | 非洲 | Kindoki（剛果） | fr/ln | folklore |
| 30 | 美洲 | Salem witch trials（1692） | en | trial |
| 31 | 美洲 | Brujos de Chiloé（1880） | es | trial |
| 32 | 文獻法制 | Canon Episcopi（10 世紀） | la | text-law |
| 33 | 文獻法制 | Malleus Maleficarum（1487） | la | text-law |
| 34 | 文獻法制 | Daemonologie（1597） | en/sco | text-law |
| 35 | 文獻法制 | Cautio Criminalis（1631） | la/de | text-law |

清單可於執行中微調（例如原文條目過於單薄時替換），替換須記錄於 `reference/README.md`。

## 9. 執行批次

1. **樣板批**：`baba-yaga`（ru）、`brujas-de-zugarramurdi`（es/eu）。完成後交使用者確認格式。
2. **量產批**（格式確認後，平行執行，每批一個地區群）：
   - 批 A：不列顛群島 4 條
   - 批 B：西歐 3 條 + 中歐 4 條
   - 批 C：北歐 3 條 + 南歐 3 條（喀爾刻、Benandanti、Sorginak）
   - 批 D：東歐 2 條 + 西亞北非 2 條
   - 批 E：東亞 4 條
   - 批 F：非洲 2 條 + 美洲 2 條
   - 批 G：文獻法制 4 條
3. **收尾批**：`INDEX.md`、兩份交叉索引、`name-glossary.md`、`README.md`。

## 10. 驗收條件

- 35 個條目檔皆存在，frontmatter 欄位齊全且 `retrieved` 有值。
- 每條目含「原文與對照翻譯」且原文非空、非英譯（除非來源本就是英語）。
- `INDEX.md` 與兩份交叉索引涵蓋全部 35 條，無死連結。
- 全庫無簡體字；標點符合 Law 8。
- `glossary.json` 未被更動。

---

## 附錄 A：第二批（2026-09-08 後續）

### 起因

使用者詢問是否收錄了 Lutzelfrau（聖露西亞日的德語區冬季女巫形象）。查核結果：**沒有**。追查出三個層次的原因：

1. **選錄清單是憑印象開的。** 首批 35 條的名單沒有經過任何系統性列舉，地方性形象沒有機會浮上檯面。
2. **佩希塔條目漏掉了含它的名單。** 德語〈Percht〉條目的「Traditionelle Perchtengestalten」一節列出各地別名，其中就有 `Lutzl（源自 Lucia，布爾根蘭）`。負責的 agent 引用並在來源列了該條目，但摘要時整節跳過。
3. **查證時只查了發源語言版本。** 德語維基沒有 `Lutzelfrau` 條目，就據此判定「維基百科沒有此條目」，而未依本規格第 7 節的來源政策去查通行語版本——英語版其實有一個 11708 字元的完整條目。

### 對應的修正

| 原因 | 修正 |
| --- | --- |
| 1 | 新增 `scripts/find_reference_candidates.py`（分類樹列舉）與 `scripts/build_reference_backlog.py`（產生 `reference/BACKLOG.md` 待辦清單），把「還有什麼沒收」變成可查證的問題 |
| 2 | 補寫佩希塔條目的該節，並在 frontmatter 補上 `wiki_secondary` |
| 3 | `scripts/fetch_wiki.py` 在擷取失敗時自動查 en／de／fr／es 是否有同名條目並回報字元數 |

另新增 `scripts/check_coverage.py` 稽核條目對原文章節的覆蓋率。**該腳本有已知誤判**：它以原文章節名做字串比對，而本規格允許「其餘章節摘要」使用中文小節標題，因此以中文改寫標題的章節會被判為未涵蓋。經抽查確認 `affaire-des-poisons`（判 33%）等案例的內容其實完整涵蓋。它只能當篩查工具，不得作為驗收標準。

### 結構調整

- 新增 `reference/concepts/` 目錄，收錄跨地區的概念條目。
- `type` 新增 `concept`，共五種：`folklore`、`trial`、`person`、`text-law`、`concept`。
- 新增 `reference/BACKLOG.md` 與 `reference/backlog/`（依主題分列的候選清單與未篩選的原始掃描結果）。

### 第二批選錄（24 條）

補的是首批完全沒有觸及的維度，而非增加更多同類條目。

| 缺口 | 條數 | 條目 |
| --- | --- | --- |
| 獵巫的反對者 | 6 | 魏爾、托馬西烏斯、貝克爾（荷蘭語，本庫首條）、普雷托里烏斯、布倫茨、魯茨 |
| 獵巫的加害者 | 3 | 福爾納、埃希特、菲爾斯滕貝格 |
| 受害者個案 | 3 | 亨諾特、羅萊福斯、雪伍德 |
| 法制 | 1 | 《卡洛林納刑法典》1532 |
| 地區審判 | 6 | 埃爾旺根、盧丹附身、貞德審判、特廖拉、多魯胡夫、冰島（受害者以男性為主） |
| 關鍵人物與事件 | 2 | 馬修·霍普金斯、露絲·奧斯本謀殺案 1751 |
| 概念條目 | 3 | Hexe、兒童女巫、魔法書 |

另補 `lutzelfrau` 與 `lussi` 兩條（本附錄起因），全庫共 61 條。

### 驗收條件（沿用並補充）

- 所有條目通過 `check_reference.py`。
- `INDEX.md` 與兩份交叉索引涵蓋全部條目，無死連結。
- `BACKLOG.md` 與各主題清單由腳本產生，已收錄者自動排除。
- `glossary.json` 未被更動。
