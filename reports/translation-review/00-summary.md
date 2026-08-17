# 翻譯檢核總報告

檢核日期：2026-08-17　範圍：全站 15 章（原文 es/rules/ ↔ 譯文 rules/）　方法：逐段完整比對，無抽樣

## 總覽

全站共發現 **492 筆**：A 級（明確錯誤）123 筆、B 級（需決策）121 筆、C 級（建議）248 筆。

| 章節 | A 級 | B 級 | C 級 | 章節報告 |
|------|-----:|-----:|-----:|----------|
| index（首頁） | 0 | 6 | 5 | [index.md](./index.md) |
| introduction（導言） | 6 | 6 | 15 | [introduction.md](./introduction.md) |
| fundamentals（基礎） | 3 | 5 | 16 | [fundamentals.md](./fundamentals.md) |
| character-creation（角色創建） | 11 | 4 | 27 | [character-creation.md](./character-creation.md) |
| archetypes（原型劇本） | 3 | 8 | 14 | [archetypes.md](./archetypes.md) |
| moves（動作） | 12 | 9 | 20 | [moves.md](./moves.md) |
| light-vs-darkness（光明與黑暗） | 11 | 7 | 13 | [light-vs-darkness.md](./light-vs-darkness.md) |
| friendship-romance（友情與戀愛） | 10 | 7 | 13 | [friendship-romance.md](./friendship-romance.md) |
| pacts（盟約） | 15 | 14 | 24 | [pacts.md](./pacts.md) |
| eclipse（蝕） | 10 | 9 | 12 | [eclipse.md](./eclipse.md) |
| darkness-enemies（黑暗與敵人） | 9 | 11 | 16 | [darkness-enemies.md](./darkness-enemies.md) |
| advancement（成長） | 2 | 4 | 7 | [advancement.md](./advancement.md) |
| mc-guide（主持人指南） | 11 | 14 | 20 | [mc-guide.md](./mc-guide.md) |
| setting（世界觀） | 7 | 7 | 33 | [setting.md](./setting.md) |
| first-chapter（第一次聚會） | 13 | 10 | 13 | [first-chapter.md](./first-chapter.md) |
| **合計** | **123** | **121** | **248** | |

整體評語：核心機制詞（盟約、護符、動作、各屬性）在絕大多數位置執行到位，數值與範例計算全數與原文一致；主要問題集中在跨章術語斷裂、點數的中文數字寫法、少量西文假朋友誤譯與規則語意偏移。

## 跨章 A 級主題（批次修正對象）

以下錯誤跨越多章、方向明確，將依各章報告逐筆修正：

1. **Devorador de Luz＝「吞光者」的三種錯誤變體，共 13 處**：eclipse「光明吞噬者」9 處、moves＋light-vs-darkness「光之吞噬者」3 處、pacts「噬光者」1 處（正確形僅存 mc-guide 3 處、darkness-enemies 4 處）。已以全站 grep 覆核。
2. **專有名詞脫鉤**：mc-guide「霞間」6 處應為「霞野」（已覆核全站僅此 6 處異體）；「火焰之書」應為 glossary 定論「焰靈魔典」；「天劍」應為「天聖之劍」；人名「奈央」應為「奈緒」。
3. **「被選者」2 處**（pacts）違反 glossary 禁用形，應為「受選者」。
4. **點數／骰值中文數字**：「一點○○點數」等全站逾 120 處（friendship-romance 50+、archetypes 36、moves 19、light-vs-darkness、pacts 5 等），違反「數值用阿拉伯數字」慣例且多章同句混用；統一改「1 點」。
5. **中國用語**：紐帶（setting 2、pacts 1）、要麼……要麼（setting 1、darkness-enemies 3）、信號（setting 2）、裹挾、通過作介詞、團隊協作、《戀如雨止》等中國譯名、「計劃」3 處（全站主流「計畫」44 處）。
6. **規則語意偏移（各章合計約 15 筆）**：主詞遺失（誰不能變身／誰獲得黑暗點數）、can/must 混淆（強制消暗點譯成「可以」）、方向譯反（「推進重大問題」譯成「解決」、類比方向顛倒、恩賜使用時序顛倒）、觸發條件漏限定詞、「最後一個敵人」應為「上一個敵人」等。
7. **first-chapter 引用名稱不一致 13 處**：MC 反應名、原則名、真理之光問題清單、偶像動作名皆與定義章（mc-guide／moves／archetypes）不符，統一改從定義章定稿。
8. **明確漏譯與誤譯**：introduction「兩種生活合而為一」、pacts「知識的泉源」「robar（奪走幸福）」、simpatía／condenadas／raramente 等假朋友、videoclub＝錄影帶出租店（first-chapter 5 處，mc-guide 已定名「格洛布錄影帶出租店」）。

## 全站 B 級決策清單（待使用者逐項定奪）

### 術語與譯名

| # | 議題 | 現況 | 出處 |
|---|------|------|------|
| B-1 | index 結尾「正義的勇者」 | 與盟約定譯「正義騎士」不呼應，且與原型「勇者」撞名；全站門面 | index B1 |
| B-2 | fantasía doméstica | 三譯並存：生活奇幻（introduction）／家庭奇幻（pacts、first-chapter）／日常奇幻（setting） | introduction B1 |
| B-3 | dimensión | 「維度」16 處（setting、mc-guide）vs「次元」8 處（pacts、eclipse、darkness-enemies），glossary 無條目 | setting B |
| B-4 | Reino de las Estrellas | 「星辰王國」vs「星之王國」兩譯並存 | darkness-enemies B3 |
| B-5 | categoría（敵人資料卡欄位） | 譯「等級」與黑暗等級／能力等級／傷痛等級撞名，資料卡兩欄並列易混；pacts 作「類別」 | darkness-enemies B1 |
| B-6 | Confidente | glossary「知心人」vs 全站實際用法「知己」8 處，完全脫節 | friendship-romance |
| B-7 | 動作／優勢名個別決策 | 黑暗女主、同心同敗、黑暗之盾、審問者直覺、轉移傷痛、Corromper 腐化／墮化、Oneira 音譯與否 | pacts B3–B9 |
| B-8 | 動漫譯名 | 《魔法少女 Site》→《魔法少女網站》？《乖乖女茱莉亞》實為《Attack No. 1》（台譯《排球甜心》）西語版名 | pacts B10、friendship-romance |

### 風格與設定

| # | 議題 | 現況 | 出處 |
|---|------|------|------|
| B-9 | 你／妳 | fundamentals 16 處用「妳」，其他章一律「你」，需全站政策 | fundamentals B1 |
| B-10 | 「創建」 | 全站 104 處，台灣慣用「建立／創造」，需整體取捨 | pacts B11 |
| B-11 | 戶上長幼 | 「雙胞胎哥哥」（moves）vs「弟弟」（fundamentals、mc-guide）；light-vs-darkness 章內自相矛盾 | light-vs-darkness B |
| B-12 | 清美的手足 | mc-guide「姐姐」vs first-chapter「小妹妹」設定衝突 | mc-guide B |
| B-13 | Vanesa／Ruth 勘誤 | first-chapter 第 522 行發言者原書勘誤，內部證據指向 Ruth，修正方式需定奪 | first-chapter B2 |
| B-14 | 「主持人（MC）」全稱重複 | 每頁多次全稱＋括號，建議首次全稱、後續簡稱 | pacts C1（全站） |

### 建檔與工具

| # | 議題 | 現況 | 出處 |
|---|------|------|------|
| B-15 | 動作／優勢名批次建檔 | 各章新創名稱未入 glossary 合計 150+（pacts 約 40、archetypes 54、friendship-romance 61…），已有跨章分裂實例（advancement 9 組、character-creation 選項名） | 各章 B |
| B-16 | glossary 鍵名修正 | 「Primer cuarto」「Último cuarto」等 4 個西文鍵名與原書實際用詞不符（原書為 Cuarto creciente 等），造成工具假警報 | eclipse B1 |
| B-17 | term_read.py 誤報 | 「Puntos de Romance」實際已正確使用 7 處仍被報「未使用」，比對邏輯待檢修 | friendship-romance |

## 已排除的疑慮

- setting 章 zh/es 段落數落差（138 vs 237）：查證為 PDF 萃取稿斷行所致，**無整段漏譯**，三份問卷逐題對應。
- 「Puntos de Romance」「Primer cuarto／Último cuarto」的「未使用」警報：均非漏譯（見 B-16、B-17）。
- 「Escudo de Luz (Sanadora)」「Kurogane Sarah」：不在 first-chapter 原文中，分屬 archetypes／moves，非漏譯。
- darkness-enemies 全章數值（傷痛範圍、黑暗等級倍數、範例計算）與原文完全一致。

## 執行結果（2026-08-17～18 完成）

三階段全部執行完畢，最終決策記錄於 [_decisions.md](./_decisions.md)（D1–D26）。

**A 級（123 筆）**：全數修正、0 筆跳過，掃殘另補修 16 處同類問題。

**B 級（121 筆）**：全站決策 26 項逐一定案後批次執行；各章語感重寫依報告建議方案採用，規則詮釋歧義 3 筆採保守讀法（合作動作封鎖範圍、閃耀點數各／共、B5 原書數字矛盾照譯加註），標記於各章執行紀錄。C 級 248 筆依 D24 保留備查。

**glossary**：新增 289 條、更新 7 條、修正錯誤鍵名 6 個（含 2 個死鍵），總計 545 個已管理術語；`term_read.py` 比對邏輯修復（撇號變體與西文單複數誤報）。

**收尾統一**：秘→祕（26 處）、姐→姊（親屬稱謂）、妳→你 清零、章節引用改「[主持人指南]」連結（5 處）、星之城堡／星之宮殿、四組跨章名稱依定義章收斂、archetypes／advancement 平行修正競態還原（6 組措辭）。

**驗證**：`validate_glossary.py` 通過；`term_read.py` 缺少使用 0、禁用詞 0；Astro 建置 33 頁全數通過；共 17 檔修改（含 glossary 與工具），約 2,500 行插入、740 行刪除，全部未 commit 供複查。

**遺留備查**：C 級 248 筆（各章報告）；glossary agent 註記之 4 筆人工確認項已於收尾處理完畢，僅餘 moves 章 Kanakana Heart／Torochan 依 D23 維持原文。
