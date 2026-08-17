# 翻譯檢核報告：eclipse（蝕）

檢核日期：2026-08-17　原文：es/rules/eclipse.md（原始萃取稿）　譯文：rules/eclipse.md

## 摘要

- 檢核段落數：約 130（逐段、逐清單條目比對，含 9 座黑暗倒數鐘共 51 個階段條目）／發現問題：A 級 10 筆、B 級 9 筆、C 級 12 筆
- 整體評語：本章翻譯整體忠實流暢，機制術語（蝕／末影／本影／半影／皇冠／衝動／倒數鐘及五種衝動類型）幾乎全數符合 glossary，倒數鐘階段名 26 處全部與 glossary 中文值一致，原文 Ímpetu／Impulso 混用亦被正確統一為「衝動」。主要問題集中在三處規則語意誤譯（本影的功能、本影可不指派、黑暗城堡兩譯）、「Devorador de Luz」9 處違反 glossary 定譯「吞光者」，以及數字與記法慣例的同章混用。
- **關於派遣指示的查證（Primer cuarto／Último cuarto）**：譯文**並未漏譯也未改用他詞**。經 Grep 全站西文語料查證，「Primer cuarto」「Último cuarto」「Medio」「Anillo」這些西文形式**從未出現在任何 es 原文檔中**；原書實際使用的階段名是「Cuarto creciente（25%）」「Media oscuridad（50%）」「Cuarto final（75%）」「Anillo solar（90%）」（僅出現於本章，es/rules/eclipse.md 第 416、418、420、422 行等 34 處）。譯文全部正確譯為 glossary 的中文值「上弦／半暗／終弦／日環」（譯文第 260、262、264、266 行起共 26 處）。問題出在 **glossary 的西文鍵名有誤**（疑為建檔時憑記憶擬定），詳見 B1。

## A 級（明確錯誤）

### A1｜terminology｜「Devorador de Luz」違反 glossary 定譯「吞光者」
- 位置：譯文第 481、493、495、499、500、508、516、518、529 行（### 星辰王國的最後光芒 全節）
- 原文：「Campeones: Devoradores de Luz y el Caballero Melancólico.」等
- 譯文：「**首領：** 光明吞噬者和憂鬱騎士。」等（全節 9 處均作「光明吞噬者」）
- 問題：glossary「Devorador de Luz」定譯「吞光者」。全站主流佐證：darkness-enemies.md 第 97、105（敵人卡名稱欄即「吞光者」）、267、271 行；mc-guide.md 第 281、305、343 行，均作「吞光者」。darkness-enemies.md 第 271 行的範例（擊敗吞光者恢復星辰王國區域）與本章描述的正是同一種敵人。（另 moves.md:515、light-vs-darkness.md:403、693 作「光之吞噬者」亦偏離，屬他章問題，此處僅供跨章統一時參考。）
- 建議修法：本章 9 處「光明吞噬者」一律改為「吞光者」。

### A2｜fidelity｜本影的功能誤譯：「推進問題」變成「解決問題」
- 位置：譯文第 188 行（### 本影 第 1 段）
- 原文：「Las Umbras son pequeños planes que ayudan a avanzar, o bien el Eclipse, o bien un problema importante para los PJ.」
- 譯文：「本影是幫助推進蝕或解決玩家角色面臨的重大問題的小型計畫。」
- 問題：原文是「幫助推進蝕、**或推進**一個對玩家角色而言的重大問題」——本影是黑暗方的計畫，推進的是玩家角色的麻煩，絕非幫忙「解決」。語意反轉。
- 建議修法：「本影是小型計畫，用來推進蝕，或推進一個困擾玩家角色的重大問題。」

### A3｜fidelity｜「不必全部指派」誤譯為「不指派給同一個蝕」
- 位置：譯文第 218 行（#### 選擇衝動 下第 3 段）
- 原文：「Puede que no quieras asignar todas las Umbras a un Eclipse. Esto puede funcionar si quieres empezar a preparar semillas para un Avatar futuro…」
- 譯文：「你可能不想將所有本影都指派給同一個蝕。」
- 問題：原文指「可以有本影暫時**不掛在任何蝕之下**」（為未來的化身預留種子、或關聯未明），並非「不要都掛在同一個蝕」。後文「你隨時可以回來建立連結」證實此意。規則語意偏移。
- 建議修法：「你不一定要把每個本影都指派給蝕。」

### A4｜fidelity｜漏譯：Dungeon World 指南可於 Nosolorol 網站免費下載
- 位置：譯文第 318 行（### 自訂動作 末段）
- 原文：「…consulta la guía de Dungeon World, que puedes descargar de forma gratuita en la web de Nosolorol.」
- 譯文：「……請參閱 Dungeon World 的指南。」
- 問題：「可於 Nosolorol 網站免費下載」整句未譯。若是刻意刪除出版社宣傳資訊的在地化決策，應記入 style-decisions.json；否則屬明確漏譯。
- 建議修法：「……請參閱 Dungeon World 的指南，該指南可在 Nosolorol 網站免費下載。」

### A5｜terminology｜「videoclub」譯「錄影店」偏離全站主流「錄影帶出租店／錄影帶店」
- 位置：譯文第 391（本影名稱「仇恨錄影店」）、397、404 行
- 原文：「El videoclub del odio」「el dependiente de un videoclub」「Varios videoclubs…」
- 譯文：「仇恨錄影店」「錄影店店員」「錄影店」
- 問題：全站同一場所（格洛布的店）主流譯法為「錄影帶出租店」（moves.md:75；mc-guide.md:128、148、259、295、345）或「錄影帶店」（light-vs-darkness.md:574、576；darkness-enemies.md:124），「錄影店」僅本章出現，且非台灣慣用說法。
- 建議修法：第 391 行改「仇恨錄影帶店」；第 397 行改「錄影帶出租店店員」；第 404 行改「錄影帶店」。

### A6｜terminology｜「Castillo de la Oscuridad」同章兩譯：黑暗之城 vs 黑暗城堡
- 位置：譯文第 503 行 vs 第 525 行
- 原文：「Se manifiesta en la Tierra el castillo de la Oscuridad…」／「El Palacio se transforma en una parte del Castillo de la Oscuridad.」
- 譯文：「黑暗之城在地球上顯現……」／「宮殿轉變為黑暗城堡的一部分。」
- 問題：castillo＝城堡；「黑暗之城」易讀成「黑暗城市」，且同一建築在同章兩個倒數鐘中出現兩種譯名。全站僅此兩處（Grep 佐證）。
- 建議修法：第 503 行改「黑暗城堡在地球上顯現，完成了兩個世界之間的橋樑。」

### A7｜數字慣例｜「一點黑暗點數」與「1 點黑暗點數」同章混用
- 位置：譯文第 305 行 vs 第 416 行
- 原文：「…o ganar un Punto de Oscuridad.」（第 305 行處）
- 譯文：「在遭遇一群公主的僕從和獲得一點黑暗點數之間做出選擇。」
- 問題：點數須用阿拉伯數字（「1 點」），且同章第 416 行已作「獲得 1 點黑暗點數」，構成混用。
- 建議修法：「從『遭遇一群公主的僕從』或『獲得 1 點黑暗點數』中擇一。」

### A8｜數字慣例｜「懲罰 3／懲罰 1」未依全站記法「懲罰/3、懲罰/1」
- 位置：譯文第 472 行（受膏於偉大光明之力）
- 原文：「Cuando está transformada, tiene Castigo/3 en lugar de Castigo/1.」
- 譯文：「變身時擁有懲罰 3 而非懲罰 1。」
- 問題：原文採「Castigo/N」記法，全站已建立對應記法「懲罰/N」（moves.md:66「懲罰/1 和摧毀/0」、moves.md:533「懲罰/6」）；本處丟失斜線記法。
- 建議修法：「變身時擁有懲罰/3 而非懲罰/1。」

### A9｜數字慣例｜「二到六個部分」應作「2 到 6 個部分」
- 位置：譯文第 254 行（### 黑暗倒數鐘 第 3 段）
- 原文：「debes dividirlo en varias partes, entre 2 y 6, según los pasos…」
- 譯文：「你應該將它分為二到六個部分」
- 問題：倒數鐘分割數為規則數值，原文亦用數字「entre 2 y 6」，應用阿拉伯數字；且同章第 21 行「兩到四個小時」用「兩」，此處用「二」，寫法亦不一致。
- 建議修法：「你應該將它分為 2 到 6 個部分」。

### A10｜taiwan-usage｜「替罪羊」為中國用語
- 位置：譯文第 90 行（征服類典型反應）
- 原文：「Presentar un cabeza de turco.」
- 譯文：「推出一個替罪羊。」
- 問題：台灣慣用「代罪羔羊」；「替罪羊」為中國大陸主流用形（全站僅此 1 處，無其他先例）。
- 建議修法：「推出一個代罪羔羊。」

## B 級（需決策）

### B1｜terminology｜glossary 西文鍵名與原書不符（Primer cuarto 等 4 鍵）
- 位置：glossary.json「Primer cuarto→上弦」「Medio→半暗」「Último cuarto→終弦」「Anillo→日環」；譯文第 260–266 行起共 26 處
- 問題：全站西文語料查無「Primer cuarto／Último cuarto／Medio／Anillo」，原書實際用詞為「Cuarto creciente／Media oscuridad／Cuarto final／Anillo solar」（僅見於本章）。譯文中文值全數正確使用，無漏譯；但 glossary 鍵名錯誤會使今後的術語一致性檢查（term_read）永遠比對不到，持續產生「已入 glossary 但譯文未見使用」的假警報。
- 候選：
  1. 將 4 個鍵名更正為原書實際用詞（Cuarto creciente／Media oscuridad／Cuarto final／Anillo solar）——與語料一致，工具檢查恢復有效；建議採用。
  2. 保留舊鍵並新增 4 個正確鍵（notes 註明同義）——保守做法，但留下永遠比對不到的死鍵。

### B2｜terminology｜「Reino Estelar／Reina Estelar」跨章兩譯：星之王國 vs 星辰王國
- 位置：譯文第 322、328、475、495、501、518、522–524、529 行（星辰王國）、第 531 行（星辰女王）
- 問題：本章與 darkness-enemies.md（第 84、271 行）作「星辰王國」；pacts.md:144（「江本咲，星之女王」）、moves.md:250、260、517、537、545、713、mc-guide.md:281、305 作「星之王國／星之女王」。同一專名（含女王稱號）全站兩譯並存，且未入 glossary。
- 候選：
  1. 「星之王國／星之女王」——出現章節較多（3 章 9 處），且與角色卡（pacts.md 江本咲）綁定，改動範圍較小。
  2. 「星辰王國／星辰女王」——與本章及 darkness-enemies.md 一致，詞感較完整。
  - 無論何者，決定後應入 glossary（Reino Estelar、Reina Estelar 兩條）。

### B3｜terminology｜本章新創未建檔名稱清單（供批次建檔）
- 位置：全章
- 問題：以下名稱出現於本章但未入 glossary（依全站議題 3 合併為一筆）：
  - 蝕類別補遺：Ascensión（昇華）已有；四類別皆已入檔 ✓
  - 皇冠名（15 個）：Gobernar 統治、Obtener poder 獲取力量、Puente 橋樑、Someter 臣服、Amor 愛、Indemnizar 索賠、Envidia 嫉妒、Fracaso 雪恥、Contención 封存、Contaminar 汙染、Incendiar 焚燒、Vacío 虛空、Restaurar 復原、Liberar 解放、Deificación 封神
  - 角色／專名：el rey del Vacío 虛空之王、el Caballero Melancólico 憂鬱騎士、El Coach 教練、el Hombre de Negro 黑衣人、Yimi（未譯，保留原文）、Nichinan 日南、Reino Estelar 星辰王國（見 B2）、Castillo de la Oscuridad 黑暗城堡（見 A6）
  - 自訂動作名：Sellar el grimorio 封印魔導書、Servir a la nueva Reina 臣服於新女王、Ungir el poder de la gran Luz 受膏於偉大光明之力、Luz retornada 歸還的光明、Recuerdo del pasado 往昔的記憶、Polvo Estelar 星塵、Maestra del fuego 火之大師、Contorsionista supremo 至尊柔術師（見 B5）、Vara de la Luz Infinita 無限光之杖、Forma Estelar 星辰形態

### B4｜terminology｜部分皇冠譯名的取捨（Someter／Indemnizar／Fracaso／Deificación）
- 位置：譯文第 84、105、107、152 行及範例各處
- 問題：四個皇冠名的譯法有可辯論空間：
  - **Someter→臣服**（第 84 行）：someter＝使屈服（及物）；「臣服」是不及物動詞，讀來像化身自己臣服於人。候選：1.「壓服」——保留及物「使屈服」義；2.「懾服」——較有魔王氣勢；3. 維持「臣服」——括號釋義已補足語意。
  - **Indemnizar→索賠**（第 105、167、169、340 行等）：indemnizar 此處指「討回應得之物」，「索賠」法律味過重。候選：1.「討還」——白話貼義；2.「索還」——保留「索」字氣勢；3. 維持「索賠」——已於本章多處使用，改動成本較高。
  - **Fracaso→雪恥**（第 107 行）：fracaso＝失敗，「雪恥」是譯者依括號釋義（從過去的負面事件中恢復）所作的詮釋。候選：1. 維持「雪恥」——符合復仇主題且中文皇冠名需簡潔；2.「敗北」——貼字面，但與釋義（恢復）方向相反。
  - **Deificación→封神**（第 152、429 行）：「封神」帶《封神演義》典故（受他者冊封），deificación 是自己成神。候選：1.「成神」——貼義且無典故；2.「神化」——中性；3. 維持「封神」——通俗響亮，唯有過度在地化疑慮（準則面向 3 前例）。

### B5｜fidelity｜「Contorsionismo」譯「柔術」屬假朋友式偏移
- 位置：譯文第 316 行
- 原文：「Contorsionista supremo: Cuando Castigues la Oscuridad contra el Presidente de Kasumano y esté usando su don Contorsionismo, usa Reflexiva en lugar de Combativa.」
- 譯文：「**至尊柔術師：** 當你對霞野社長懲戒黑暗且對方正在使用其恩賜『柔術』時……」
- 問題：contorsionismo＝軟骨功／柔身表演（身體極度扭曲），「柔術」在中文指日本武術 jujutsu，是另一種東西；且該恩賜屬霞野社長（黑暗使徒章可能另有此恩賜條目，需連動確認）。
- 候選：
  1. 「軟骨功」／「至尊軟骨功大師」——台灣通俗說法，畫面感強。
  2. 「柔身術」／「至尊柔身大師」——較雅，避免武術聯想。

### B6｜fidelity｜「al ocultarlas」的「隱藏」語意遺失
- 位置：譯文第 174 行（### 執行危險反應 第 1 段）
- 原文：「Estas nuevas Reacciones deben seguir tus principios, así que al ocultarlas debes justificar su aparición en la Ficción de alguna forma.」
- 譯文：「這些新的反應必須遵循你的原則，因此在運用它們時，你必須在虛構敘事中以某種方式為其出現提供合理解釋。」
- 問題：「al ocultarlas」（既然你將它們隱而不宣——呼應 MC 原則「不直呼動作之名」）被譯成「在運用它們時」，遺失了「因為反應是暗中執行的，所以才需要在敘事中合理化」的因果。
- 候選：
  1. 「……因此，由於你不會明說這些反應，必須在虛構敘事中以某種方式為其出現提供合理解釋。」——補回因果。
  2. 「……因此在暗中使用它們時，你必須……」——最小改動。

### B7｜terminology｜「星塵」撞名：本影名與動作名塌縮成同一譯名
- 位置：譯文第 512 行（本影名稱：星塵）vs 第 531 行（自訂動作：星塵）
- 原文：本影「El polvo de una estrella」／動作「Polvo Estelar」——原文是兩個不同名稱
- 問題：兩個不同的西文名稱譯成完全相同的「星塵」，讀者無法區分本影與其附屬動作。
- 候選：
  1. 本影改「一顆星星的塵埃」，動作保留「星塵」——貼原文差異。
  2. 本影改「星之塵」，動作保留「星塵」——較簡潔。

### B8｜fidelity｜「心之力（ ）」空括號無法理解
- 位置：譯文第 473、536 行
- 原文：「Un Poder del Corazón ( ) que ocupa un espacio…」「2 Poder del Corazón ( )」
- 問題：原書括號內應為類型圖示（A／D／P），PDF 萃取時遺失，譯文照抄空括號，讀者無從得知含義。glossary 已有「心之力 A／D／P」三型條目可用。
- 候選：
  1. 查原書 PDF 補回類型字母，如「心之力（A）」——最忠實。
  2. 改為「心之力（類型自選）」並加註——若原書即為通用圖示。
  3. 保留空括號但加註腳說明原書此處為圖示。

### B9｜taiwan-usage｜「構建」vs 全站主流「建構」
- 位置：譯文第 10、14、293 行
- 譯文：「你需要構建出有趣的東西」「當你開始構建 Mahō Shōjo 的蝕時」「以下是構建新動作的一系列建議」
- 問題：「構建」偏中國用語；全站主流為「建構」（setting.md:8、10；mc-guide.md:100、277；first-chapter.md:278；fundamentals.md:122、128、250；character-creation.md:216、338 等 11+ 處），但「構建」亦散見 introduction.md:12、14、character-creation.md:345、374、light-vs-darkness.md:508，屬跨章問題，性質類似已列管的「創建」全站議題。
- 候選：
  1. 本章 3 處先改「建構」，並將「構建→建構」納入全站統一決策清單——與「創建」議題一併批次處理。
  2. 僅登記為全站議題，暫不動本章——避免零星修改造成新的不一致。

## C 級（建議）

- **C1**｜第 73、84 行：「慾望和野心的映射」「化身慾望的映射」——「映射」偏技術詞（mapping），建議「寫照」或「映照」（setting.md:376 亦用「映射」，可一併考慮）。
- **C2**｜第 10 行：「也想看她們受苦」——原文「querrás hacerlas sufrir, verlas pelear…」中「hacerlas sufrir」是「讓她們受苦」，建議「但你同時也想讓她們受苦，看她們戰鬥、墜入愛河……」。
- **C3**｜第 12 行：「沒有履行你的目標或原則」——cumplir 此處宜拆譯：「達不成你的目標、守不住你的原則」。
- **C4**｜第 164 行：「恢復在遠古戰鬥中失去的、它們需要用來重新佔據在黑暗中地位的力量」——長定語堆疊，建議拆句：「或想恢復遠古戰鬥中失去的力量——那是它們重返黑暗權位所必需的」。
- **C5**｜第 172 行標題「執行危險反應」——「危險反應」易讀成「危險的反應」，可考慮「執行危機反應」。
- **C6**｜第 181 行：「太空署」→「太空總署」（台灣慣用）。
- **C7**｜第 216 行：「派一個首領去把她家人中的某人變成人偶」——前句主語是複數「魔法少女」，「她」指涉不明，建議「把其中一位魔法少女的家人變成人偶」。
- **C8**｜第 246 行：「都應該有一個名字」——原文 deben（必須），建議「都必須有名字和一系列標籤」。
- **C9**｜第 253 行：「最後，作為最後一步，標明……」——贅述，建議「最後，標明它達到終點時的後果」。
- **C10**｜第 280、357 行：「在將情感注滿書中後」語序不順，建議「在書中注滿情感後」；「神木」在台灣多指巨樹（阿里山神木），建議「聖木」。
- **C11**｜第 322 行「魔法領域」vs 第 328 行「魔法王國」（reino mágico／Reino Mágico）同章不一致，建議統一為「魔法王國」；另第 326、421 行「暗黑神祇」中第 421 行原文為「dios de la Oscuridad」（大寫，指黑暗陣營），依 glossary 可作「黑暗神祇」，唯 darkness-enemies.md 已有「暗黑魔法」等先例，維持亦可。
- **C12**｜零星語感：第 368 行「黑暗火焰元素」→「化為黑暗元素火焰」；第 378 行「恢復他的服務」→「讓他重新為她效力」；第 383 行「木乃伊化血肉」→「乾屍化的血肉」；第 404 行「次級版本」→「較弱的分身」；第 410 行「至少擁有 1 級黑暗等級」→「黑暗等級至少為 1」；第 470 行「受膏於偉大光明之力」宗教色彩重且方向與原文（為聖光之力敷聖）相反，可考慮「大光明之力的敷聖」；第 518 行「最後的脈搏中」→「彌留之際」。
