# 翻譯檢核報告：character-creation（角色創建）

檢核日期：2026-08-17　原文：es/rules/character-creation.md（原始萃取稿）　譯文：rules/character-creation.md

## 摘要

- 檢核段落數：128（含條列項、星座／元素／血型小節與 8 個範例區塊，逐段全數比對）／發現問題：A 級 11 筆、B 級 4 筆、C 級 27 筆
- 整體評語：本章整體結構完整、無漏段，術語大多依 glossary 落實（扮演書、屬性五項、盟約三型、點數類均正確），範例的 ruby 標註也符合 style-decisions 規範。主要問題集中在：一處規則語意誤譯（「選擇三個選項」）、數個單字級誤譯（heroína、intensa、emociones extremas、seguramente）、同章數字慣例與「建構／構建」混用，以及與 archetypes.md 的動作選項名稱不一致。星座與血型形容詞清單的譯法大致可靠，但有幾處單字偏移值得微調。

## A 級（明確錯誤）

### A1｜fidelity｜「受眷顧者」規則誤譯：「在三個選項中做選擇」應為「選擇三個選項」

- 位置：譯文第 323 行（## 選擇動作 範例）
- 原文：「Cuando obtiene este Movimiento, deberá escoger entre tres opciones y Esther se decide por las siguientes: Por el poder de la Justicia, Guiada por el corazón … y Susurros de los Guardianes.」
- 譯文：「獲得此動作時，她必須在三個選項中做選擇，Esther 選了以下幾項：『以正義之力』、『由心指引』……和『守護者的低語』。」
- 問題：依 archetypes.md 第 110 行，「受眷顧者」的規則是「選擇三個選項：」（六選三）；譯文「在三個選項中做選擇」誤指總共只有三個選項，且與後文列出三項自相矛盾，屬規則語意偏移。
- 建議修法：「獲得此動作時，她必須從中選擇三個選項，Esther 選了以下幾項：……」

### A2｜fidelity｜heroína 誤譯為「魔法少女」

- 位置：譯文第 248 行（## 光之裝束 第 2 段）
- 原文：「En el momento en el que una magical girl se transforma y viste su traje, pasa de ser una persona ordinaria a una heroína.」
- 譯文：「當魔法少女變身穿上裝束的那一刻，她從一個普通人變成了魔法少女。」
- 問題：heroína＝英雄（女英雄）；變身前她已經是魔法少女，原意是「從平凡之人蛻變為英雄」，譯文邏輯不通。
- 建議修法：「當魔法少女變身穿上裝束的那一刻，她就從平凡之人搖身一變，成為英雄。」

### A3｜fidelity｜射手座 emociones extremas 誤譯「極致情感」

- 位置：譯文第 134 行（#### 射手座 第 1 段）
- 原文：「convirtiéndolas en atletas y amantes de las emociones extremas」
- 譯文：「使她們成為運動健將和極致情感的愛好者」
- 問題：emociones（fuertes/extremas）此處為西語慣用義「刺激」，指熱愛極限刺激（與前文「運動健將」呼應），非「情感」。
- 建議修法：「使她們成為運動健將與極限刺激的愛好者」

### A4｜fidelity｜A 型負面特質 intensa 誤譯「偏執」

- 位置：譯文第 194 行（#### A 型 負面特質）
- 原文：「Obstinada, ansiosa, reservada, intensa, nerviosa y tímida.」
- 譯文：「固執、焦慮、內向、偏執、緊張、害羞。」
- 問題：intensa 指情感過於濃烈強烈（用情太深、「太用力」），並非「偏執」（多疑妄想）。
- 建議修法：「固執、焦慮、內向、情感濃烈、緊張、害羞。」

### A5｜fidelity｜假朋友 seguramente 誤為「一定」

- 位置：譯文第 216 行（### 最珍貴的寶物 第 1 段）
- 原文：「pero seguramente ayude al MC a construir la historia」
- 譯文：「但一定能幫助主持人（MC）建構故事」
- 問題：seguramente＋虛擬式＝「想必／很可能」，非「一定」；同章第 246 行的 seguramente 已正確譯為「大概」，前後標準不一。
- 建議修法：「但想必能幫助主持人（MC）建構故事。」

### A6｜terminology｜「展開第一章」與實際章節標題不符且缺站內連結

- 位置：譯文第 374 行（## 羈絆與角色介紹 第 3 段）
- 原文：「(para saber más dirígete a «Empezar en el primer capítulo en la página 220)」
- 譯文：「（若要了解更多，請參閱「展開第一章」章節）」
- 問題：該章已譯出且標題為「第一次聚會」（first-chapter.md:2 `title: 第一次聚會`）；譯名不符又未加連結，讀者無從對應。
- 建議修法：「（若要了解更多，請參閱「[第一次聚會](/rules/first-chapter/)」章節）」

### A7｜terminology｜「互相標註」未接軌「標籤」（Etiqueta）術語

- 位置：譯文第 377 行（## 羈絆與角色介紹 範例）
- 原文：「empiezan a responder preguntas mientras se etiquetan unas otras」
- 譯文：「開始回答問題並互相標註」
- 問題：etiquetar 對應遊戲機制 Etiqueta＝「標籤」（glossary）；全站慣用「標記為／加上標籤」（friendship-romance.md:123、145、167、191、213、239，light-vs-darkness.md:600），「標註」使機制連結斷裂。
- 建議修法：「開始回答問題並互相加上標籤」

### A8｜taiwan-usage｜「構建」與「建構」同章混用

- 位置：譯文第 345、374 行用「構建」；同章第 216、338 行用「建構」
- 問題：「構建」為中國慣用詞，台灣通行「建構」，同章兩者並存。全站查證：「建構」為主流（setting.md:8、10；mc-guide.md:100、277；fundamentals.md:122、128、250；first-chapter.md:278），「構建」為少數（introduction.md:12、14；eclipse.md:10、293；light-vs-darkness.md:508）。
- 建議修法：本章第 345 行「構建角色」→「建構角色」、第 374 行「構建第一次聚會」→「建構第一次聚會」；全站統一可另行批次處理。

### A9｜taiwan-usage｜「完善」作動詞

- 位置：譯文第 374 行
- 原文：「quizás el MC aún necesite completar algunos puntos de la ambientación」
- 譯文：「主持人（MC）可能還需要完善世界觀的某些內容」
- 問題：「完善＋受詞」的動詞用法為中國慣用；原文 completar 即「補完」。
- 建議修法：「主持人（MC）可能還需要補完世界觀的某些內容」

### A10｜numbers｜年齡數字同章混用

- 位置：譯文第 56 行「八歲到十七歲」；同章第 219 行「15 歲」
- 原文：「entre los ocho y los diecisiete años」／「tendrá 15 años」
- 問題：年齡屬數值，同章混用中文與阿拉伯數字，違反數字慣例。
- 建議修法：第 56 行改為「魔法少女似乎在 8 歲到 17 歲之間的某個時刻覺醒」。

### A11｜numbers｜「五點友情點數」應用阿拉伯數字

- 位置：譯文第 379 行；同章第 372 行已作「5 點友情點數」
- 原文：「Mónica les indica que se anoten cinco Puntos de Amistad.」
- 譯文：「Mónica 告訴她們記下五點友情點數。」
- 問題：點數值須用阿拉伯數字，且同章混用。
- 建議修法：「Mónica 告訴她們記下 5 點友情點數。」

## B 級（需決策）

### B1｜terminology｜「由心指引」與 archetypes.md「心之引導」跨章不一致（Guiada por el corazón）

- 位置：譯文第 323 行「由心指引」；archetypes.md:115「**心之引導**」
- 原文：「Guiada por el corazón (escogiendo A la luz de la verdad como Movimiento Básico)」
- 問題：同一動作選項兩章譯名不同，且皆未入 glossary。另同清單的「Por el poder de la Justicia」也不一致：本章 323、moves.md:83、first-chapter.md:442 皆作「以正義之力」，archetypes.md:112 作「正義之力」（主流 3 比 1）。
- 候選：
  1. 統一為 archetypes.md 的形式（「心之引導」「正義之力」）——扮演書頁面是玩家實際查閱的選項清單，以它為權威來源。
  2. 統一為本章／moves／first-chapter 的形式（「由心指引」「以正義之力」）——佔多數頁面，改動量較小，且「以正義之力」較貼近原文介詞結構。

### B2｜fidelity｜B 型正面特質 indecisa 逕譯「果斷」（疑原書勘誤）

- 位置：譯文第 198 行（#### B 型 正面特質）
- 原文：「Pasional, creativa, indecisa, aventurera, fuerte, alegre y curiosa.」
- 譯文：「熱情、有創意、果斷、愛冒險、堅強、開朗、好奇。」
- 問題：原文正面清單出現 indecisa（猶豫不決），與同型負面清單（第 200 行「猶豫不決」）重複，疑為原書勘誤（或本應為 decidida）；譯文逕改為反義「果斷」，屬未註明的自行更正。
- 候選：
  1. 維持「果斷」，並在勘誤／風格紀錄註明係依 decidida 推定——閱讀最順。
  2. 改譯中性詮釋如「隨性」——保留原文的模糊，不作反義更正。
  3. 忠實譯「猶豫不決」——完全忠實，但正面清單出現負面詞會使讀者困惑。

### B3｜fidelity｜Yō 與 Shō／Juana 與 Sergio 西班牙在地文化梗

- 位置：譯文第 48 行（### 姓名 第 2 段）
- 原文：「¿O acaso alguien conoce a Yō y Shō con unos nombres que no sean Juana y Sergio?」
- 譯文：「或者有人知道 Yō 和 Shō 用的不是 Juana 和 Sergio 的名字嗎？」
- 問題：此為西班牙專屬梗（日本動畫《アタッカーYOU!》西語版將主角 Yō、Shō 在地化改名為 Juana、Sergio）；現譯直譯且句式不通，台灣讀者無從理解笑點。
- 候選：
  1. 修順句子＋加譯註：「難道有人知道 Yō 和 Shō 除了 Juana 和 Sergio 以外的名字嗎？（譯註：西班牙播出的日本動畫曾將角色改為西語名，如《アタッカーYOU!》的主角）」——保留原味與資訊。
  2. 概括改寫：「畢竟在西班牙，許多觀眾只認得動畫主角的在地化譯名。」——通順，但丟失具體例子。
  3. 在地化替換為台灣讀者的共同記憶（如早年台譯《哆啦A夢》的「葉大雄、王聰明」）——最易懂，但方向由「西化」變「中文化」，偏離原文語境。

### B4｜terminology｜本章出現、尚未入 glossary 的名稱清單（批次建檔用）

- Movimientos Especiales → 特殊動作（本章 318；archetypes.md:12 同形，跨章一致）
- Movimientos de Libreto → 扮演書動作（本章 323）
- Movimientos de Pacto → 盟約動作（本章 334；pacts.md:81、230，moves.md:706 同形，跨章一致）
- Lazos de Amistad → 友情羈絆（本章 354；light-vs-darkness.md:583、friendship-romance.md:17 等同形，跨章一致）
- Por el poder de la Justicia → 以正義之力（本章 323；跨章不一致詳見 B1）
- Guiada por el corazón → 由心指引（本章 323；跨章不一致詳見 B1）
- Susurros de los Guardianes → 守護者的低語（本章 323；archetypes.md:114 同形，跨章一致）
- El poder de la Amistad → 友情之力（本章 365）

## C 級（建議）

- C1｜fidelity｜第 12 行：漏譯「por ejemplo」且主詞歧義——「如果一位玩家選擇了衛士，就不應該被其他人選擇」可改「如果一位玩家選了（例如）衛士，其他人就不應再選同一本」。
- C2｜fidelity｜交叉引用連結缺漏（合併 5 處）：第 30 行（ver página 62 → 可連 /rules/friendship-romance/）、第 41 行（ver «Ambientación» → /rules/setting/）、第 280 行（ver «Los Movimientos» → /rules/moves/）、第 304 行（ver «El Eclipse» → /rules/eclipse/）、第 338 行（ver página 262 → /rules/setting/）。本章其他頁碼引用均已轉為站內連結，此 5 處直接省略，建議補齊。
- C3｜fluency｜第 74 行：「血氣方剛」傳統上形容年輕男性，用於少女微妙；可改「天生熱血」。
- C4｜fidelity｜第 126 行：「純粹的情感力量」——intensidad＝強度非力量，可改「天蠍座的人情感純粹而濃烈」。
- C5｜fidelity｜第 128 行：「熱情是一種極端的天賦」易讀成「極有天賦」；don de extremos 意為走向兩極，可改「因為熱情是一種走向兩極的天賦」。
- C6｜fluency｜第 134 行：「踏上新的經歷」搭配不當，可改「投身新的體驗」。
- C7｜fluency｜第 142 行：「向世界展示出雄心勃勃、決心完成……」詞性不順，可改「在世人面前顯得雄心勃勃，決心達成看似不可能的壯舉」。
- C8｜fidelity｜第 150 行：「分為……的一面和……的一面」與後文「無論屬於哪一類」矛盾；原文是分成兩類人，可改「分為害羞敏感型與膚淺外向型」。
- C9｜fluency｜第 156、158 行：「視為己有」用於感受不妥，可改「感同身受」；「共感能力」與第 156 行「同理心」用詞不一，建議統一「同理心」。
- C10｜fidelity｜第 166 行：temerarias（魯莽）譯「大膽」偏弱；「personas con tacto」指說話行事得體圓融，「察言觀色」略偏，可改「不太懂得婉轉得體」。
- C11｜fluency｜第 176 行：「以及無論以何種形式傳達它們的能力」語序拗口，可改「以及不拘形式傳達這些知識的能力」。
- C12｜terminology｜第 178 行：「她們獨特的世界觀」與遊戲術語「世界觀」（Ambientación）撞名；原文為 forma de ver el mundo，可改「她們看待世界的獨特方式」。
- C13｜fluency｜第 184 行：「重要的缺點」（importantes defectos）可改「重大缺點」。
- C14｜terminology｜第 192、204 行：同字異譯——concienzuda 譯「謹慎」、cautelosa 譯「慎重」（A 型），但 O 型的 cautelosa 又譯「謹慎」；建議 concienzuda →「一絲不苟」、cautelosa 統一「謹慎」。
- C15｜fidelity｜第 210 行：excéntrica（古怪）譯「獨特」偏弱，可作「特立獨行」；diplomática 譯「圓滑」略帶貶義，可作「圓融」。
- C16｜fluency｜第 223 行：「她的最珍貴的寶物」雙重「的」，改「她最珍貴的寶物」。
- C17｜fidelity｜第 288 行：「力量分為三個等級」——categorías 為「三類」；「等級」易與「能力等級」（Nivel de Poder）混淆，可改「力量分為三類」。
- C18｜fluency｜第 297 行：「一隻背景有劍的貓」不順，可改「印著一隻貓，背景襯著一把劍」。
- C19｜fluency｜第 304 行：西式後置條件句「甚至鼓勵他們回頭修改某些部分，如果這樣做能……」，可改「如果能因此得到更有趣、更好玩的結果，甚至可以鼓勵他們回頭重做部分內容」。
- C20｜fluency｜第 334 行：「授予魔法少女小幅修改和盟約動作」動賓搭配不當，可改「為魔法少女做些小幅調整，並授予盟約動作」。
- C21｜fluency｜第 345 行：「進行了修改」冗贅，可改「做了調整」。
- C22｜fidelity｜第 338 行：「從嫉妒和猜忌」——celos y envidia 為「妒忌與眼紅」；「猜忌」（不信任）偏離 envidia。
- C23｜taiwan-usage｜第 268 行：「心型」建議作「心形」（台灣標準寫法）。
- C24｜fidelity｜第 38 行：標題「關於性別」省略了 sexos；如欲保留原意可作「關於性別與生理性別」，維持現狀亦可。
- C25｜taiwan-usage｜第 248 行：「比如」台灣較通行「例如」。
- C26｜fidelity｜第 30 行：「身邊重要之人」——原文 personas cercanas 為「身邊親近的人」，「重要」為引申；另「心如何與……之人纏繞」漏了對方的「心」（con el de las personas cercanas），可改「與身邊親近之人的心纏繞在一起」。
- C27｜fidelity｜第 88 行：「甚至善於說謊」——mentirosas 僅指愛說謊，「善於」過度引申，可改「甚至愛說謊」。
