# 魔女傳說參考資料庫

蒐集歷史上的魔女／女巫傳說，**以該傳說發源語言的維基百科條目為主要來源**，保存原文並完整翻譯成繁體中文，依地區、語系、時代三個軸整理。

本資料庫是 `maho-shojo` repo 底下的獨立資料夾，**不併入 Astro 網站**，也不參與規則書的翻譯與術語檢查流程。

## 從哪裡開始

| 檔案 | 內容 |
| --- | --- |
| [INDEX.md](INDEX.md) | 主索引，依地區列出全部條目 |
| [indexes/by-language-family.md](indexes/by-language-family.md) | 語系交叉索引 |
| [indexes/by-era.md](indexes/by-era.md) | 時代交叉索引 |
| [name-glossary.md](name-glossary.md) | 各條目原文專有名詞對照總表 |
| [BACKLOG.md](BACKLOG.md) | 待收錄候選清單，含人工挑選的優先候選與依主題分列的完整掃描結果 |

## 目錄結構

```
reference/
  README.md                    本檔
  INDEX.md                     主索引（依地區）
  indexes/                     語系與時代的交叉索引
  name-glossary.md             原文專有名詞對照總表
  regions/
    01-british-isles/          不列顛群島
    02-western-europe/         西歐
    03-central-europe/         中歐
    04-northern-europe/        北歐
    05-southern-europe/        南歐
    06-eastern-europe/         東歐
    07-west-asia-north-africa/ 西亞・北非
    08-east-asia/              東亞
    09-sub-saharan-africa/     撒哈拉以南非洲
    10-americas/               美洲
  sources-and-law/             跨地區的文獻與法制
  concepts/                    跨地區的概念條目（女巫概念本身、兒童女巫、魔法書……）
  BACKLOG.md                   待收錄候選清單（索引）
  backlog/                     依主題分列的候選清單，及未篩選的原始掃描結果
```

地區是唯一的目錄分類軸；語系與時代不另開目錄，改由 `indexes/` 底下的交叉索引呈現，因此不會有條目被漏掉。

## 條目的組成

每個條目是一個 Markdown 檔，含 YAML frontmatter 與五個固定章節：

| 章節 | 內容 |
| --- | --- |
| `## 概要` | 三到五句繁體中文，說明這是什麼、為何重要 |
| `## 原文與對照翻譯` | 導言與關鍵章節逐段對照：原文以 blockquote 逐字抄錄，下方接該段繁體中文譯文 |
| `## 其餘章節摘要` | 未逐段對譯的章節，以繁體中文逐節摘要涵蓋 |
| `## 專有名詞對照` | 原文｜羅馬轉寫｜繁體中文｜說明 |
| `## 來源與授權` | 語言版本、原文條目名、URL、擷取日期、授權標註 |

frontmatter 記錄 `id`、`title_zh`、`title_native`、`region`、`countries`、`language`、`language_family`、`era`、`era_bucket`、`year_range`、`type`、`source`、`tags`，索引即由這些欄位產生。

`type` 有五種：`folklore`（民俗／神話）、`trial`（審判事件）、`person`（人物）、`text-law`（文獻與法制）、`concept`（概念）。
`era_bucket` 有四種：`ancient`、`medieval`、`early-modern`、`modern`。

## 來源政策

1. 優先使用**傳說發源語言**的維基版本：俄羅斯傳說用 `ru`、巴斯克傳說用 `eu`、日本妖怪用 `ja`，依此類推。
2. 發源語言沒有條目、或內容過於單薄時，退用最近的學術通行語版本（`es`／`pt`／`en`／`fr`／`de`／`la`），並在 frontmatter 的 `source.fallback_reason` 說明原因。
   **判定「沒有這個條目」之前，必須實際查過通行語版本。** `scripts/fetch_wiki.py` 在擷取失敗時會自動去 `en`／`de`／`fr`／`es` 查同名條目並回報字元數，據此判斷。Lutzelfrau 一條就是因為只查了德語版、沒查英語版，在首批被誤判為「維基百科沒有此條目」而漏收。
3. 同一事件橫跨兩種語言時（例如蘇加拉穆爾迪案的巴斯克語傳說與西班牙語司法檔案），兩種原文並取，主要語言記在 `language`，次要語言記在 `language_secondary`。
4. 原文引文**逐字保留**，不修正拼寫、標點或錯誤。原文有誤植、或不同語言版本互相矛盾時，照譯，另以 `:::note[譯註]` 區塊指出。

## 擷取的已知陷阱

1. **引文模板的內容會被純文字擷取剝除。** `prop=extracts&explaintext` 不會輸出
   `{{quotation}}`、`{{Zitat}}`、`{{Cytat}}`、`{{Cite}}` 等模板的內文，因此條目中
   最關鍵的原著引文往往整段消失，只剩「……如下所述：」這樣的引導句。發現引導句
   後面接空白時，必須改以 `action=raw` 取原始碼補回。橋姬條目的《古今和歌集》和歌
   與《平家物語》〈劍卷〉約 1,800 字古日文、普雷托里烏斯與托馬修斯的原著引文、
   多魯胡夫的塔茲比爾引文，都是這樣補回來的。

2. **`prop=info` 的 `length` 是 wikitext 位元組數，不是純文字字數，而且跨語系不可比。**
   實測比值：歐洲語言約 1.7—2.2 倍，日／中／韓約 3.4—7.6 倍。同樣的位元組數，
   CJK 條目的實際內容只有歐洲條目的三分之一左右。判斷篇幅是否足夠時，
   要用 `prop=extracts` 的實際字數，不要用 `length`。

3. **中文條目要指定 `zh-tw` 變體**，否則擷取結果是簡體字。jobs 檔的第四欄填 `zh-tw`。

4. **標題可能是消歧義頁或重導向。** 已踩過的坑：`Mélusine`、`Holda`、`Blocksberg`、
   `Louhi`、`Pohjola`、`לילית` 都是消歧義頁；`清姫` 重導向到 `安珍・清姫伝説`、
   `바리데기` 重導向到 `바리공주`。擷取前先確認實際條目名。

## 翻譯規範

沿用專案根目錄 `CLAUDE.md` 的規定：

- 一律繁體中文（zh-TW），不使用簡體字，不使用中國大陸用語。
- 全形標點：：，。、；「」『』（）……；數字與拉丁文字用半形；省略號用 `……`。
- 譯文求信達，不過度在地化，不以中文典故成語替換西文概念。
- 本資料庫的專有名詞收錄於 [name-glossary.md](name-glossary.md)，**不寫入 `glossary.json`**（後者是遊戲規則的術語庫，兩者各自獨立，避免互相污染一致性檢查）。

## 維護指令

```bash
# 擷取維基百科原文（先建立 tab 分隔的 jobs 檔）
.venv/Scripts/python.exe scripts/fetch_wiki.py .cache/jobs.tsv

# 驗證條目（簡體字、半形標點、省略號、frontmatter 必填欄位）
.venv/Scripts/python.exe scripts/check_reference.py

# 重新產生索引與名詞總表
.venv/Scripts/python.exe scripts/build_reference_indexes.py

# 稽核條目對原文章節的覆蓋率（找出被整節略過的內容）
.venv/Scripts/python.exe scripts/check_coverage.py [條目路徑...]

# 從各語言維基的分類樹列舉候選條目，扣除已收錄者
.venv/Scripts/python.exe scripts/find_reference_candidates.py --depth 1 --min-size 5000

# 由掃描結果重建待辦清單（已收錄者會自動消失）
.venv/Scripts/python.exe scripts/build_reference_backlog.py
```

新增條目後務必重跑 `check_reference.py`、`build_reference_indexes.py` 與 `build_reference_backlog.py`。

`check_coverage.py` **有已知誤判**：它以原文章節名做字串比對，而本資料庫的「其餘章節摘要」允許使用中文小節標題，因此以中文改寫標題的章節會被判為未涵蓋。它只能當篩查工具，不能當驗收標準；被標記的項目要逐一人工確認。

`find_reference_candidates.py` 的輸出同樣需要人工篩選——分類樹裡混有虛構作品與流行文化條目，腳本的排除規則只能濾掉大部分。

## 授權

各條目引用的原文取自維基百科，授權為 **CC BY-SA 4.0**；每個條目的「來源與授權」一節都標明語言版本、原文條目名稱、URL 與擷取日期。繁體中文譯文、摘要與名詞對照表為本專案自行撰寫，同樣以 CC BY-SA 4.0 釋出。
