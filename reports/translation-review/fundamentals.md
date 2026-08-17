# 翻譯檢核報告：fundamentals（基礎規則）

檢核日期：2026-08-17　原文：es/rules/fundamentals.md　譯文：rules/fundamentals.md

## 摘要

- 檢核段落數：95（12 節全數比對，含範例對話行與提示框）／發現問題：A 級 3 筆、B 級 5 筆、C 級 16 筆
- 整體評語：本章術語一致性佳，機制詞（動作、反應、觸發條件、五屬性、各基礎動作名、扮演書等）均符合 glossary 規定譯法，無漏段落。主要問題集中在少數明確誤譯（提示框標題「桌遊」）、用字慣例（計劃／計畫、點數數字）與第二人稱「你／妳」的使用不一致。語句大致流暢自然，僅零星翻譯腔與詞語取捨可再打磨。

## A 級（明確錯誤）

### A1｜fidelity｜提示框標題「juegos de rol」誤譯為「桌遊」

- 位置：譯文第 172 行（:::tip 標題）
- 原文：「Los dados en los juegos de rol」
- 譯文：「桌遊中的骰子」
- 問題：juegos de rol＝角色扮演遊戲，非桌遊（juegos de mesa）；下一行內文「桌遊或角色扮演遊戲的老手」（juegos de rol o de mesa）才同時包含兩者，可見標題是誤植。
- 建議修法：「:::tip[角色扮演遊戲中的骰子]」

### A2｜taiwan-usage｜「計劃」應作「計畫」（全站主流）

- 位置：譯文第 250 行（### 一個魔法、不同卻又熟悉的世界 第 2 段）
- 原文：「cómo son los planes de los Avatares…」
- 譯文：「化身的計劃是什麼樣子的……」
- 問題：全站 rules/\*.md 以「計畫」為主流（44 處，分布於 eclipse.md 18 處、mc-guide.md 8 處、darkness-enemies.md 6 處、setting.md 4 處、archetypes.md 4 處等，例：eclipse.md:69「最適合其計畫的類別」、mc-guide.md:317「你們要繼續這個計畫嗎」）；「計劃」僅 3 處（本章 250 行、moves.md、character-creation.md 各 1），且台灣慣用名詞形為「計畫」。
- 建議修法：「化身的計畫是什麼樣子……」

### A3｜terminology｜點數數值未用阿拉伯數字

- 位置：譯文第 165 行（## 動作與擲骰 範例二末段）
- 原文：「por lo que logra un punto que podrá entregar a Natsumi」
- 譯文：「因此她獲得了一個點數，可以交給夏美」
- 問題：依數字慣例，點數值應用阿拉伯數字（「1 點」不是「一點／一個點數」）。註：全站對此慣例本就混用（moves.md:466「獲得一點友情點數」vs moves.md:468「你獲得 1 點額外的友情點數」），可能需要全站統一，但本章此處可先修正。
- 建議修法：「因此她獲得 1 點，可以交給夏美幫助她通過測驗。」

## B 級（需決策）

### B1｜terminology｜第二人稱「你／妳」章內不一致，且與全站主流相左

- 位置：譯文第 57 行（「上面你認出了血之公主的符號」，Mónica 對女性角色說話）、第 137 行（「你不該出現在這裡，小姑娘」，保全對依子說話）
- 原文：「un papel en el que distingues el símbolo…」／「No deberías estar aquí, niña…」
- 問題：本章對女性角色的第二人稱大量使用「妳」（16 處，如第 53、61、67、103、145 行），僅上列 2 處用「你」，章內明顯不一致。但全站查證後，「妳」僅出現於 5 個檔案共 26 處（fundamentals 16、mc-guide 4、moves 3、eclipse 2、character-creation 1），其他章對女性角色對話一律用「你」（例：first-chapter.md:316「店員會給你一部電影……你是怎麼知道這些的？」對女性玩家）。屬全站政策問題，需決策後才知道本章該往哪個方向修。
- 候選：
  1. 全站統一用「你」（性別中立）——與現行多數章節一致，改動最少（本章需改 16 處）；規則書正文對讀者本就用「你」，可全書齊一
  2. 「對女性角色的對話用妳、對讀者與泛稱用你」定為全站規範——符合本作全女性主角的題材氛圍，本章僅需修 2 處，但其他章節需大量補改

### B2｜fidelity｜「de manera retroactiva」譯「倒敘」的詮釋選擇

- 位置：譯文第 44 行（## 一場簡單的對話 末段）
- 原文：「No importa si algunas de sus aportaciones se realizan de manera retroactiva si con ello se logra mejorar y avanzar la Ficción.」
- 譯文：「即使某些貢獻是以倒敘的方式加入的，只要能推進和完善虛構敘事就好。」
- 問題：retroactivo 指「追溯生效、事後補述設定」（例：玩家事後宣告「我的角色其實早就認識他」），並不限於「倒敘」（flashback）這一敘事手法，譯「倒敘」把範圍縮窄了。參照：mc-guide.md:448 將 retroactivo 譯「追溯性替代計畫」；archetypes.md:248 參謀動作情境則用「倒敘」。
- 候選：
  1. 「即使某些貢獻是事後追補的」——最貼近原意，涵蓋一切追溯性補述
  2. 「即使某些貢獻是以追溯方式補上的」——與 mc-guide.md 的「追溯性」用字呼應
  3. 維持「倒敘」——若團隊認定 TRPG 語境中兩者實務上等同

### B3｜fidelity｜霞野大樓的「club」譯「社團」語域不合

- 位置：譯文第 135 行（## 動作與擲骰 範例一）
- 原文：「es momento de que Yoriko se adentre en el misterioso club del edificio Kasumano」
- 譯文：「是時候讓依子深入神祕的霞野大樓的社團了」
- 問題：「社團」在台灣語感中強烈指向學校社團，但此場景是企業大樓（霞野為大型企業集團，見 first-chapter.md:111）、有保全、管制區域、父親的辦公室在內，此 club 應是會員制的私人俱樂部。另全站「社團」均用於學校情境（moves.md:144-160、mc-guide.md:317），「俱樂部」用於營業場所（first-chapter.md:304 影碟俱樂部）。
- 候選：
  1. 「神祕的霞野大樓俱樂部」——符合企業大樓語境與全站用法分工
  2. 「霞野大樓裡那間神祕的會所」——「會所」更強調私人會員制場所
  （順帶可解掉「神祕的霞野大樓的社團」的「的」字堆疊）

### B4｜terminology｜「主持人（MC）」章節引用名與實際章名不符

- 位置：譯文第 80、224、226 行
- 原文：「(ver el capítulo «Maestro de Ceremonias»)」等
- 譯文：「參閱「主持人（MC）」章節」
- 問題：實際章名為「主持人指南」（mc-guide.md title），且 moves.md:367 已用「[主持人指南](/rules/mc-guide/)」附連結引用；但「主持人（MC）」章節這種寫法在全站更多（light-vs-darkness.md:18、eclipse.md:69、darkness-enemies.md:301 及本章 3 處），皆未附連結。屬跨章統一問題（與既知議題 2 的 MC 稱呼精簡策略相關但不同：這裡是「章節引用名」是否對齊實際章名）。
- 候選：
  1. 全站統一改為「[主持人指南](/rules/mc-guide/)」章節——引用名與章名一致且可點擊，本章 3 處照改
  2. 維持「主持人（MC）」章節但全站補上連結——保留原文《Maestro de Ceremonias》的指涉感，但讀者在側欄找不到同名章節

### B5｜terminology｜本章未建檔名稱清單（供批次建檔）

- 本章出現、glossary 尚無獨立條目的專名僅 1 個：
  - 「edificio Kasumano」→ 霞野大樓（第 135 行；moves.md:89、light-vs-darkness.md:71、first-chapter.md:107 等多章沿用同譯，譯法已一致，建議入 glossary 固定。glossary 現僅有 Presidente de Kasumano／Criatura de Kasumano 兩個衍生詞）
- 其餘人名、動作名、敵人名均已在 glossary 中且譯法相符。

## C 級（建議）

- C1｜fluency｜第 12 行：章名「一場簡單的對話」，原題「Lo simple de una conversación」重點在「對話（本質上）的簡單」；可考慮「對話，就這麼簡單」更貼題。
- C2｜fidelity｜第 14 行：「每個人講述自己角色的行動」漏「a los demás jugadores」；建議「每個人向其他玩家講述自己角色的行動」。
- C3｜fluency｜第 16 行：「接近敘事和享受它的方式有很多種」代詞冗餘；建議「親近並享受敘事的方式有很多種」。另「讓故事始終引人入勝」原文主語是對話（la conversación）。
- C4｜fluency｜第 18 行：「有趣且有意思」同義重複（interesante y divertido），建議「有趣又好玩」；「該在哪裡做切割」建議「該在哪裡切分場景」；「實踐之後自然就能掌握」建議「多練習幾次自然就能掌握」。
- C5｜fluency｜第 27 行：「她會比起去看酒井的情況，更想調查……」語序不順；建議「比起去探望酒井，她更想調查前幾天晚上發生了什麼事」。
- C6｜fidelity｜第 35 行：「目前正值七月的考試期間」，原文「se encuentran cerca de los exámenes de julio」是考試將近（所以才要聚在一起讀書）；建議「目前七月的考試將近」。
- C7｜fidelity｜第 48 行：「當事情塵埃落定」對應「Cuando se ha resuelto」（反應結算完畢），且與後句「事態開始連鎖發展」邏輯相抵；建議「反應結算之後，事態便開始連鎖發展」。
- C8｜fidelity｜第 67、71 行：「偷窺」對應 espiar（監視／窺探），此處弟弟隔著門偷聽；建議「監視」或「偷聽」。
- C9｜taiwan-usage｜第 84 行：「行動起來」偏陸式口號語感；建議「必須採取行動」。
- C10｜fidelity｜第 103 行：「一個學生」漏 alumna 性別（女學生）；「眼睛發出鮮紅的光芒」原文僅「亮紅色的眼睛」（ojos de un color rojo brillante），未言發光；建議「一名女學生，眼睛是亮紅色的」。
- C11｜fluency｜第 117 行：「漫畫和動畫社」台灣校園慣稱「動漫社」（原文 club de manga y anime）。
- C12｜fluency｜第 130 行：「每個扮演書」量詞建議「每本扮演書」。
- C13｜fluency｜第 184 行：「在擲骰時加上加值和減值時」雙「時」；建議「為擲骰加上加值與減值時」。
- C14｜fidelity｜第 186 行：「預期的完美成功」之「完美」為增譯（原文 el resultado que esperabas）；建議「獲得你所預期的結果」。另第 188 行「相反，」建議台灣慣用「相反地，」。
- C15｜fluency｜第 201、205、137 行：「要求我一個人情」不合語法，建議「向我討一個人情」；「走著瞧」偏中國口語且帶威嚇語氣（原文 ya veremos 是中性的「再看看」），建議「且看這事會鬧到什麼地步」；「小姑娘」建議台灣口語「小妹妹」。
- C16｜taiwan-usage／fluency｜第 232、236、246、258、262 行：「做飯」建議「做菜」（兩處）；「為什麼在難過」建議「為什麼難過」；「必須始終遠離照本宣科」建議「都必須避免照本宣科」、「不確定性必須存在於每一個人之中」建議「所有人都必須面對不確定性」；小節標題「一個魔法、不同卻又熟悉的世界」建議「一個充滿魔法、既陌生又熟悉的世界」；「定期重新討論」之「定期」為增譯，建議「不時重新討論」；「費這麼大的勁」建議「費這麼大的功夫」。
