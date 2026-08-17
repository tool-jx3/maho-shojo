# 翻譯檢核報告：advancement（成長與經驗）

檢核日期：2026-08-17　原文：es/rules/advancement.md　譯文：rules/advancement.md

## 摘要

- 檢核段落數：45／發現問題：A 級 2 筆、B 級 4 筆、C 級 7 筆
- 整體評語：本章翻譯整體忠實且流暢，遊戲機制詞（閃耀點數、成長、扮演書、形態等）均符合 glossary 規定，章內自身一致性良好。最大的問題不在章內，而在跨章：本章詳述的各成長名稱與 archetypes.md 各原型扮演書的成長清單措辭幾乎全數不一致（解鎖 vs 取得、上限 vs 最高等），讀者對照扮演書查規則時會找不到對應條目，需整批決策統一。另有一處西文語感誤譯與數字慣例混用。

## A 級（明確錯誤）

### A1｜fidelity｜「el último enemigo」誤譯為「最後一個敵人」

- 位置：譯文第 165 行（:::tip[光之裝束的提升] 第 3 段）
- 原文：「¿Quizás el último enemigo les hizo darse cuenta de que tenían algún poder oculto?」
- 譯文：「還是最後一個敵人讓她們意識到自己擁有某種隱藏的力量？」
- 問題：此處「último」指「最近的、上一個（交手的敵人）」，中文「最後一個敵人」會被讀成「最終敵人／最後的魔王」，語意偏移。
- 建議修法：「還是上一個交手的敵人讓她們意識到自己擁有某種隱藏的力量？」

### A2｜taiwan-usage（數字慣例）｜點數與門檻值使用中文數字，與同章阿拉伯數字混用

- 位置：譯文第 28、32 行（點數）；第 44、46 行（成長次數門檻）；相關：第 32（五次）、36（兩次、三次、四名）、45（兩項）、56 行（兩項）
- 原文：「apunta 1 punto de Lux est ... y 1 punto adicional」（範例一）；「Si el PJ tiene menos de 6 Avances ...」「Si se tienen 6 o más Avances ...」（摘要）
- 譯文：「記錄一點閃耀點數（因發動終曲），再加一點」（28）；「各獲得一點閃耀點數」（32）；「成長次數少於六次」（44）；「達到六次或以上」（46）
- 問題：依數字慣例，點數與規則門檻值應用阿拉伯數字（「1 點」不是「一點」）；同章第 32、36、77 行已用「6 點」「7 點」「9 點」「（4 + 3 = 7）」，且第 77 行成長數在算式中作「+ 7」，同章混用。原文範例一與摘要處皆為阿拉伯數字「1」「6」。
- 建議修法：第 28 行改「記錄 1 點閃耀點數（因發動終曲），再加 1 點」；第 32 行改「獲得 1 點閃耀點數」；第 44 行改「成長次數少於 6 次」；第 46 行改「達到 6 次或以上」。第 32（五次）、36、45、56 行的成長／人數量詞建議一併改為「5 次」「2 次」「3 次」「4 名」「2 項」以與算式對齊。
- 附註：全站其他章大量使用「獲得一點友情點數」「花費一點友情點數」句式（pacts.md:244、moves.md:466、friendship-romance.md:39 等數十處），本筆修正時宜同步發起全站數字慣例統一決策，避免本章改完後反而與他章不一致。

## B 級（需決策）

### B1｜terminology｜成長名稱與 archetypes.md 扮演書清單系統性不一致

- 位置：譯文第 86、96、100、104、106、108、110、112、116、126、130、136、144、148 行（本章各成長標題）
- 問題：本章是各成長的詳述章，archetypes.md 各原型的「閃耀時刻！」清單則列出同一批成長的名稱，但兩章措辭幾乎全數不同，玩家從扮演書清單對照本章查規則時無法直接匹配。逐項比對（原文｜本章｜archetypes.md）：
  1. Accedes a la forma Súper/Triunfante del Lux Habitu｜「取得光之裝束的超級／凱旋形態」（86、136）｜「解鎖光之裝束的超級／凱旋形態」（archetypes.md:189、197 等各原型皆同）
  2. Mejorar una Característica (Máx. 2/3)｜「提升一項屬性（最高 2／3）」（112、144）｜「提升一項屬性（上限 2／3）」（archetypes.md:187、196 等）
  3. Adquiere un Movimiento de Genio que no tengas｜「取得一個尚未擁有的天才動作」（96）｜「獲得一項你尚未擁有的天才動作」（archetypes.md:328）
  4. Consigue 3 opciones adicionales de Elegida por los Guardianes｜「額外獲得『受眷顧者』的三個選項」（104）｜「獲得『受眷顧者』的三個額外選項」（archetypes.md:188）
  5. Consigue 3 opciones adicionales de Poder Sagrado｜「額外獲得『神聖力量』的三個選項」（108）｜「獲得神聖力量的三個額外選項」（archetypes.md:839，且未加引號）
  6. Obtienes un Movimiento de Escudo de Luz｜「取得一個光之盾動作」（126）｜「獲得一項光之盾動作」（archetypes.md:455）
  7. Obtiene un Movimiento de La senda de la guerrera｜「取得一個戰士之道動作」（130）｜「獲得一項戰士之道動作」（archetypes.md:573）
  8. Al escenario… Let's go MAX+｜「登上舞台……Let's go MAX+」（100）｜「『登上舞台……Let's go』MAX+」（archetypes.md:702，引號範圍不同）
  9. Movimiento de (Libreto)｜「（原型）動作」（116、148）｜「勇者進階動作」「參謀進階動作」等（archetypes.md:186、324 等；另見 B2）
  10. Movimiento de tu Libreto de Amistad｜「友情扮演書動作」｜「友情扮演書動作」——唯一完全一致的一項
- 候選：
  1. 以本章（詳述章）為準，回改 archetypes.md 各清單——本章逐條解說是規則出處，且「取得」「最高」等擇字尚可再議一次
  2. 以 archetypes.md 清單為準，回改本章標題——archetypes.md 出現次數多（六個原型 ×2 清單），改動面較小的是本章
  3. 逐項開術語決策（/term-decision），定案後批次入 glossary 並全站替換——最穩妥，成長名稱屬跨章引用的機制詞，本就該建檔管理

### B2｜terminology｜Movimiento de Avance：「成長動作」vs「進階動作」

- 位置：譯文第 118、150 行
- 原文：「Este Avance permite seleccionar un Movimiento de Avance indicado en tu Libreto de Arquetipo.」
- 譯文：「此成長允許選擇一個原型扮演書中標示的成長動作。」
- 問題：archetypes.md 對同一概念全部譯作「進階動作」（archetypes.md:12、199、337、464、584、711、848 及各清單條目「勇者進階動作」等），為全站主流；本章獨用「成長動作」。glossary 無此詞條，需決策。
- 候選：
  1. 「進階動作」——從主流，改動最小（只改本章 2 處）；缺點是與「進階成長」（Avance mayor）字面易混，且 Avance 的 glossary 定譯是「成長」
  2. 「成長動作」——與 Avance＝成長的 glossary 定譯嚴格對應，語意最準；但需回改 archetypes.md 十餘處
  3. 沿用清單實際形式「（原型名）進階動作」並將本章標題「（原型）動作」（116、148）同步改為「（原型）進階動作」——無論選 1 或 2，本章標題都應與清單條目構詞一致

### B3｜fidelity｜範例二「各獲得一點」的規則詮釋

- 位置：譯文第 32 行（範例二）
- 原文：「Al final de la sesión las jugadoras de Torome y Natsumi obtienen un punto de Lux est.」
- 譯文：「聚會結束時，登呂美和夏美的玩家各獲得一點閃耀點數。」
- 問題：閃耀點數是記在盟約扮演書上的共用池（本章第 23、25 行；moves.md:645「當你們獲得一個新的閃耀點數時」及 moves.md:659、663 的範例均為單點記入共用池）。原文「obtienen un punto」較可能指兩位玩家共同獲得 1 點（若是各得 1 點，西文慣用「un punto cada una」）；「各獲得」會被讀成共記 2 點，影響升級節奏的理解。原文本身未完全明示，屬詮釋選擇。
- 候選：
  1. 「登呂美和夏美的玩家獲得 1 點閃耀點數」——共同獲得單點，與共用池及 moves.md 範例的單點敘述吻合，建議採用
  2. 「登呂美和夏美的玩家為盟約記下 1 點閃耀點數」——直接點明記入共用池，最不易誤讀
  3. 維持「各獲得」——若使用者判斷「聚會結束」條件是每名玩家各觸發一次（規則面需另行確認）

### B4｜terminology｜本章出現但未入 glossary 的機制名稱清單（批次建檔用）

- 位置／問題：以下名稱在本章正文出現、glossary 尚無詞條（或義項不足），依全站策略合併列出：
  1. Movimiento de Avance →「成長動作」（118、150；archetypes.md 作「進階動作」，見 B2）
  2. Movimiento de Amistad →「友情動作」（122、154；moves.md:666 等同用，譯法一致）
  3. Lazo de Amistad →「友情羈絆」（122、154；glossary 僅有 Lazos →「羈絆」）
  4. Movimientos de Pacto →「盟約動作」（21；pacts.md:81、moves.md:706 同用，譯法一致）
  5. Movimiento de (Libreto) →「（原型）動作」（116、148；佔位符構詞，見 B2 候選 3）
  6. Corazón de Luz（勇者成長動作義項）→「光之心」（65；archetypes.md:207 同名動作。glossary 已有詞條但 notes 僅記「地球上的光明聖地」，與 eclipse.md 的地點義項同名，建議 notes 補充雙義項）
- 候選：
  1. 逐項以 term_edit.py 建檔核可——維持 Law 7 的完整流程
  2. 待全站批次建檔策略定案後一併處理——與已知全站議題 3 合流

## C 級（建議）

- C1｜fidelity｜第 52 行：「hay unas pequeñas restricciones」譯「有一些限制」，漏掉「pequeñas」的緩和語氣；可改「有一些小限制」。
- C2｜fidelity｜第 69 行：原文僅「Marion indica...」，譯文增譯「主持人（MC）Marion」。屬有助理解的補充（glossary 記載 Marion 為 MC），可保留；後續處理全站「主持人（MC）」精簡策略時一併檢視。
- C3｜fidelity｜第 77 行：「la forma Súper puede ser escogida pese a ser menor」譯「超級形態作為例外可以在此時選擇」，省略了「雖屬基礎成長」這一理由；可改「但超級形態雖屬基礎成長，仍可作為例外在此時選擇」。
- C4｜fluency｜第 161 行：「armas con una forma diferente」譯「不同形態的武器」，「形態」與本章高頻遊戲術語（超級形態、凱旋形態）撞詞；建議「造型不同的武器」。
- C5｜taiwan-usage｜第 167 行：「金屬部件」偏中國大陸慣用構詞，台灣較常說「金屬配件」或「金屬零件」；建議「也許服裝上出現了金屬配件」。
- C6｜fidelity｜第 169 行：「Habla con el MC y llegad a algún acuerdo」譯「與主持人（MC）商議」，將「討論」與「達成共識」壓縮成一詞；可改「與主持人（MC）討論並達成共識」。另「讓每一次成長都……」的「每一次」為增譯（原文單指該項成長），影響甚微。
- C7｜terminology｜glossary「Corazón de Luz」的 notes 僅記地點義項，本章第 65 行與 archetypes.md:207 另有同名勇者動作；建議於 notes 補記「亦為勇者進階動作名」以免日後誤判不一致（已列入 B4 清單第 6 項）。
