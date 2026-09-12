# 規則書參考作品分析資料庫 設計規格

- 日期：2026-09-12
- 狀態：待使用者審核
- 產出位置：`reference/works/`

## 1. 目的

蒐集 Mahō Shōjo 規則書所提及之魔法少女類作品的**作品分析**，三個收集軸為：

1. **作品含意**——主題、母題、作品在說什麼。
2. **設計概念**——企劃緣起、製作意圖、角色與美術設計概念、系列定位。
3. **劇本設計**——系列構成、敘事結構、腳本手法、關鍵轉折的設計。

非繁體中文的材料一律**保存原文並逐段翻譯成繁體中文**。

本資料庫與既有的魔女傳說庫一樣，**不併入 Astro 網站**，也不參與規則書的翻譯與術語檢查流程。

## 2. 範圍

### 收錄的 17 部

規則書全篇提及的作品共 35 部（見附錄 A 的完整清單）。本批依使用者指示**只收魔法少女類**：`introduction.md`〈參考來源〉的 16 部，加上 `pacts.md` 額外舉出的《魔法少女網站》。

| # | id | 繁中片名 | 日文原名 | 年 | 盟約對應 |
| --- | --- | --- | --- | --- | --- |
| 1 | `sailor-moon` | 美少女戰士 | 美少女戦士セーラームーン | 1991 | 正義騎士 |
| 2 | `magic-knight-rayearth` | 魔法騎士雷阿斯 | 魔法騎士レイアース | 1994 | — |
| 3 | `cardcaptor-sakura` | 庫洛魔法使 | カードキャプターさくら | 1996 | 光明子女 |
| 4 | `tokyo-mew-mew` | 東京喵喵 | 東京ミュウミュウ | 2002 | — |
| 5 | `mai-hime` | 舞-HiME | 舞-HiME | 2004 | — |
| 6 | `lyrical-nanoha` | 魔法少女奈葉 | 魔法少女リリカルなのは | 2004 | 光明子女 |
| 7 | `precure` | 光之美少女 | プリキュアシリーズ | 2004— | 正義騎士 |
| 8 | `shakugan-no-shana` | 灼眼的夏娜 | 灼眼のシャナ | 2005 | — |
| 9 | `kampfer` | 肯普法 | けんぷファー | 2009 | — |
| 10 | `toaru-kagaku-no-railgun` | 科學超電磁砲 | とある科学の超電磁砲 | 2009 | — |
| 11 | `madoka-magica` | 魔法少女小圓 | 魔法少女まどか☆マギカ | 2011 | 契約傀儡 |
| 12 | `mahou-shoujo-ikusei-keikaku` | 魔法少女育成計畫 | 魔法少女育成計画 | 2012 | — |
| 13 | `symphogear` | 戰姬絕唱 Symphogear | 戦姫絶唱シンフォギア | 2013 | — |
| 14 | `kill-la-kill` | Kill la Kill | キルラキル | 2013 | — |
| 15 | `yuki-yuna-wa-yusha-de-aru` | 結城友奈是勇者 | 結城友奈は勇者である | 2014 | 契約傀儡 |
| 16 | `sailor-moon-crystal` | 美少女戰士 Crystal | 美少女戦士セーラームーン Crystal | 2014 | — |
| 17 | `mahou-shoujo-site` | 魔法少女網站 | 魔法少女サイト | 2018 | 契約傀儡 |

「盟約對應」只填**規則書自己寫出的對應**（`pacts.md` 第 19／21／23 行），規則書未指定者填 `null`，不自行歸類。

### 明確不做的事

- **不含「用於 Mahō Shōjo 的取材建議」一節。** 沿用魔女傳說庫的先例（使用者於 2026-09-08 明確排除）。
- **不收其餘 18 部**（非魔法少女類的動漫 13 部、PbtA 桌遊 4 部、《鬥球兒彈平》1 部）。清單保留在附錄 A，日後如要開第二批，範圍已界定好。
- **不寫入 `glossary.json`。** 本子庫的專有名詞收於 `reference/works/name-glossary.md`。

## 3. 目錄結構

```
reference/
  README.md                  改寫為兩個子庫的總覽
  （魔女傳說庫既有檔案不動）
  works/
    README.md                子庫說明、來源政策、授權、劇透警告
    INDEX.md                 主索引（依年代）
    indexes/
      by-pact.md             依盟約對應
      by-origin.md           依原作型態
    name-glossary.md         本子庫原文專有名詞對照總表
    entries/
      madoka-magica.md       等 17 檔，檔名為 kebab-case 的 id
```

魔女傳說庫的 `name-glossary.md` 與本子庫的**各自獨立**，不互相併入，理由同魔女庫與 `glossary.json` 分離：避免不同性質的名詞污染彼此的一致性檢查。

## 4. 條目模板

分析與其證據**不分離**：原文引用直接嵌在它所支持的那一節底下，不另設集中的「原文與對照翻譯」節。這與魔女傳說庫的體例有意不同——魔女庫是「翻譯一個條目」，本庫是「以原文佐證三個分析軸」。

```markdown
---
id: madoka-magica
title_zh: 魔法少女小圓
title_native: 魔法少女まどか☆マギカ
title_romanized: Mahō Shōjo Madoka Magika
title_en: Puella Magi Madoka Magica
year: 2011
years: "2011—"                      # 系列仍在延續者填區間，單作留 null
media: [電視動畫, 劇場版, 漫畫, 遊戲]
origin: 原創動畫                     # 原創動畫 | 漫畫改編 | 輕小說改編 | 遊戲改編 | 玩具企劃
studio: [シャフト]
key_staff:
  監督: 新房昭之
  シリーズ構成・脚本: 虚淵玄
  キャラクター原案: 蒼樹うめ
pact_mapping: 契約傀儡               # 光明子女 | 正義騎士 | 契約傀儡 | null
cited_in:                            # 規則書何處提及，可回溯
  - docs/src/content/docs/rules/introduction.md
  - docs/src/content/docs/rules/pacts.md
source:
  wiki: https://ja.wikipedia.org/wiki/魔法少女まどか☆マギカ
  wiki_lang: ja
  wiki_secondary: null               # 系列作另有各作品條目時記於此
  retrieved: 2026-09-12
  license: CC BY-SA 4.0
  extra:                             # 維基以外的來源，逐筆記錄
    - title: <原文標題>
      publisher: <媒體或官方名稱>
      url: <URL；典藏版本記典藏網址>
      archived: false                # true 表示取自網際網路典藏館
      retrieved: 2026-09-12
tags: [虚淵玄, 存在主義, 願望與代價, 時間迴圈, 異空間演出]
---

## 概要

（三到五句繁體中文：這是什麼作品、為什麼被規則書引為參考。）

## 作品含意

（主題、母題、作品在說什麼。）

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

- 維基百科（日語）〈原文條目名〉，URL，擷取日期 2026-09-12。授權 CC BY-SA 4.0。
- （非維基來源逐筆列出：標題、發行者、URL、擷取日期、是否為典藏版本）
```

### 查無材料時的寫法

三軸中若某一軸確實查不到可佐證的材料，該節寫：

```markdown
## 設計概念

:::note[查證結果]
已查日語維基百科〈條目名〉全文、官方網站（URL，狀態）與（列出實際查過的來源），未見製作方對本作設計概念的具體說明。
:::
```

**不得以推測填滿。** 明載查過哪些來源，比寫一段看似合理的分析有價值。

## 5. 來源政策

| 層級 | 來源 | 授權處理 |
| --- | --- | --- |
| 主幹 | 日語維基百科，以 `scripts/fetch_wiki.py` 取得 | CC BY-SA 4.0，逐條標註語言版本、條目名、URL、擷取日 |
| 補強 | 官方網站企劃文、監督／腳本／製作人訪談、公式設定資料集、雜誌訪談 | 節錄引用，逐筆標明出處與擷取日；不整篇轉錄 |

規則：

1. 主要來源固定為**日語**維基百科（本批 17 部全為日本作品，無發源語言例外）。
2. 維基條目過薄時，**必須實際查過**官方網站與可檢索的訪談後才能判定「查無」，並在該節列出查過的來源。此為魔女庫 Lutzelfrau 事件的直接教訓。
3. 2002—2009 年作品的官方網站多已失效，走網際網路典藏館取檔，`extra[].archived` 填 `true`，URL 記典藏網址。
4. 原文引文**逐字保留**，不修正拼寫與標點。原文有誤植或來源互相矛盾時照譯，另以 `:::note[譯註]` 指出。
5. 訪談引文須能明確指出發言者與場合；只有轉述而無法追到原始發言者的，歸入「其餘重要脈絡」以摘要處理，不放進三軸的引用。

### 沿用魔女庫已記錄的擷取陷阱

`reference/README.md`〈擷取的已知陷阱〉一節全部適用，其中對本批特別相關的兩項：

- **引文模板的內容會被純文字擷取剝除**（`{{Quotation}}`／`{{Cquote}}`／`{{Blockquote}}`）。動畫條目的製作訪談引文幾乎都包在模板裡，發現引導句後面接空白、或引文缺出處時，必須改以 `action=raw` 取原始碼補回。
- **`prop=info` 的 `length` 是 wikitext 位元組數，日文約為純文字字數的 3.4—7.6 倍。** 判斷篇幅是否足夠時用 `prop=extracts` 的實際字數。

新增一項本批預期會遇到的：

- **系列作條目會分裂成「系列總條目」與「各作品條目」。** 〈プリキュアシリーズ〉、〈魔法少女リリカルなのは〉、〈美少女戦士セーラームーン〉都是如此，設計概念多半在系列總條目、劇本設計多半在各作條目。主要來源記系列總條目，其餘以 `wiki_secondary` 記錄。

## 6. 翻譯與寫作規範

沿用專案 `CLAUDE.md` 的 Immutable Laws：

- **Law 6**：一律繁體中文（zh-TW），不得出現簡體字或中國大陸用語。
- **Law 8**：全形標點（：，。、；「」『』（）……），數字與拉丁文字用半形；省略號用 `……`。
- **Law 9**：罕用字、雙關、文化負載詞若影響語意或語氣，先提 2～3 個候選再定案。
- 譯文求信達，不過度在地化，不以中文典故成語替換外文概念。
- **片名一律沿用規則書已定案的繁中譯名**（見第 2 節表格），不另譯。

## 7. 劇透

「劇本設計」一節必然含完整劇透，《魔法少女小圓》、《結城友奈是勇者》、《舞-HiME》、《魔法少女網站》尤其嚴重。`reference/works/README.md` 開頭加警語，各條目不逐一加。

## 8. 腳本改動

現有工具無條件遞迴整個 `reference/`，新子庫的 frontmatter schema 不同會直接讓驗證失敗。三處最小幅度改動：

| 檔案 | 改動 |
| --- | --- |
| `scripts/check_reference.py` | `REQUIRED_FIELDS` 改為依路徑前綴分流的對照表；`reference/works/` 用新 schema（`id`／`title_zh`／`title_native`／`year`／`origin`／`source`）。簡體字、半形標點、省略號三項檢查照舊全庫適用，日文原文的豁免邏輯沿用既有機制（本子庫以 `source.wiki_lang` 判斷） |
| `scripts/build_reference_indexes.py` | 掃描時排除 `reference/works/` |
| `scripts/build_works_indexes.py` | 新增。產生 `INDEX.md`、`indexes/by-pact.md`、`indexes/by-origin.md`、`name-glossary.md` |

`check_coverage.py` 與 `build_reference_backlog.py` **不套用於本子庫**：前者以維基章節名比對覆蓋率，而本庫體例本就只取三軸相關章節，必然大面積「未涵蓋」，指標無意義；後者的候選來源是分類樹掃描，本庫的收錄清單由規則書決定，不需要待辦掃描。兩者需加上 `reference/works/` 的排除。

## 9. 執行批次

| 批次 | 條目 | 說明 |
| --- | --- | --- |
| 樣板批 | `madoka-magica`、`tokyo-mew-mew` | 分別是資料最厚與最薄的兩端，一次驗證「材料充足」與「必須寫查無」兩種體例。完成後交使用者確認 |
| A（3 條） | `sailor-moon`、`magic-knight-rayearth`、`cardcaptor-sakura` | 九〇年代 |
| B（4 條） | `mai-hime`、`lyrical-nanoha`、`precure`、`shakugan-no-shana` | 2004—2005 |
| C（4 條） | `kampfer`、`toaru-kagaku-no-railgun`、`mahou-shoujo-ikusei-keikaku`、`symphogear` | 2009—2013 |
| D（4 條） | `kill-la-kill`、`yuki-yuna-wa-yusha-de-aru`、`sailor-moon-crystal`、`mahou-shoujo-site` | 2013—2018 |
| 收尾 | 索引 3 份、`name-glossary.md`、`reference/works/README.md`、改寫 `reference/README.md`、腳本改動、全庫驗證 | |

A—D 平行執行。**交叉引用一律留給收尾批單向補上**——魔女庫第三批的教訓：平行 agent 同時互改會產生競態，正確作法是先定基準、單向改、事後 grep 驗證。

## 10. 驗收條件

- `reference/works/entries/` 下 17 個條目檔皆存在，frontmatter 必填欄位齊全且 `source.retrieved` 有值。
- 每條的「作品含意」「設計概念」「劇本設計」三節皆有內容，或以查證結果區塊明載查過哪些來源。
- 所有非繁體中文材料 100% 附原文逐字引用與繁中對譯，無只譯不附原文者。
- `pact_mapping` 只在規則書實際指定的 7 條上有值，其餘為 `null`。
- `cited_in` 指向的規則書路徑實際存在且該檔確實提及該作品。
- `scripts/check_reference.py` 全庫（含魔女庫既有 140 條）零問題。
- `INDEX.md` 與兩份交叉索引涵蓋全部 17 條，無死連結。
- `glossary.json` 未被更動。

---

## 附錄 A：規則書提及的全部 35 部作品

本批只收「魔法少女類」欄標 ✓ 的 17 部，其餘留待日後決定。

| 出處 | 作品 | 魔法少女類 |
| --- | --- | --- |
| `introduction.md`〈參考來源〉 | 美少女戰士、魔法騎士雷阿斯、庫洛魔法使、東京喵喵、舞-HiME、魔法少女奈葉、光之美少女、灼眼的夏娜、肯普法、科學超電磁砲、魔法少女小圓、魔法少女育成計畫、戰姬絕唱 Symphogear、Kill la Kill、結城友奈是勇者、美少女戰士 Crystal（16 部） | ✓ |
| `pacts.md` | 魔法少女網站 | ✓ |
| `friendship-romance.md`〈戀愛扮演書範例〉 | 排球甜心（アタッカーYOU!）、亂馬½、涼宮春日的憂鬱、Myself; Yourself、驚爆危機、ef: A Tale of Memories、校園迷糊大王、四月是你的謊言、Code Geass、你的名字、愛在雨過天晴時、School Days、死亡筆記本（13 部） | |
| `first-chapter.md` | 鬥球兒彈平 | |
| `introduction.md`〈關於 PbtA〉 | Apocalypse World、Dungeon World、Sombras Urbanas、Worlds in Peril（4 部） | |
