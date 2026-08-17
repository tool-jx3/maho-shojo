# 翻譯檢核報告：mc-guide（主持人指南）

檢核日期：2026-08-17　原文：es/rules/mc-guide.md　譯文：rules/mc-guide.md

## 摘要

- 檢核段落數：47 節全文逐段（正文約 90 段＋範例 42 則）／發現問題：A 級 11 筆、B 級 14 筆、C 級 20 筆
- 整體評語：本章整體語感流暢、MC 框架詞（目標／原則／反應／柔性反應／硬性反應／動作／虛構敘事）與 glossary 高度一致，範例段落的敘事口吻掌握得宜。主要問題集中在**專有名詞與其他章節脫鉤**——霞野誤作「霞間」（6 處）、焰靈魔典誤作「火焰之書」、奈緒誤作「奈央」、天聖之劍誤作「天劍」、戶上兄妹關係與主流相反——由於本章術語被全站多章引用，這批名詞須優先修正。另有數處西文誤譯與大量代詞（你／妳、他們／她們）政策不一致待決策。

## A 級（明確錯誤）

### A1｜terminology｜Kasumano 誤作「霞間」（應為「霞野」，且「大廈」應為「大樓」）

- 位置：譯文第 202、208、241、252、263、279 行
- 原文：「Estás comprobando los expedientes del edificio Kasumano.」（202）／「empresas Kasumano」（252、263）／「El sello de Kasumano」（279）
- 譯文：「霞間大廈」「霞間企業」「霞間的印章」
- 問題：全站主流與 glossary（Presidente de Kasumano＝霞野社長）均作「霞野」，建築物均作「霞野大樓」。佐證：moves.md:89、light-vs-darkness.md:71/238/395、fundamentals.md:135、first-chapter.md:107/109/111/155、eclipse.md:419/423/443/462、darkness-enemies.md:67/71/220/227/265。本章 6 處為全站唯一的「霞間」。
- 建議修法：202/208「霞野大樓的檔案」；241「霞野大樓的電梯」；252「突入霞野企業分部」；263「霞野企業的印章」；279「霞野的印章」。

### A2｜terminology｜Ignem Grimoris 誤作「火焰之書」（glossary 定論：焰靈魔典）

- 位置：譯文第 319、340 行
- 原文：「Puedes arrebatarle el Ignem Grimoris a la Hechicera…」（319）／「el alma de un inocente se introduce en el Ignem Grimoris de la Hechicera de Llamas Oscuras」（340）
- 譯文：「你可以趁著火焰之書掛在魔女腰帶上……」／「被吸入暗焰女巫的火焰之書中」
- 問題：glossary 已定論「Ignem Grimoris＝焰靈魔典」；eclipse.md:237/273/275/277/278/282/344/350/354/355/359 全部使用「焰靈魔典」。
- 建議修法：兩處改為「焰靈魔典」。

### A3｜terminology｜Celestial Sword 誤作「天劍」（glossary 定論：天聖之劍，且缺 ruby 標註）

- 位置：譯文第 269 行
- 原文：「Con un golpe de la Celestial Sword logras derrotar y desposeer a Ino.」
- 譯文：「你用天劍的一擊成功擊敗並驅除了伊野身上的附身。」
- 問題：glossary 定論「天聖之劍」，全站一致（moves.md:79/319/424/533、light-vs-darkness.md:202、first-chapter.md:226/288/428/438/518、character-creation.md:295/299）。且依 style-decisions.json 的 ruby 政策，此為本頁首次（唯一）出現，應加英文原名標註。
- 建議修法：「你用<ruby>天聖之劍<rp>（</rp><rt>Celestial Sword</rt><rp>）</rp></ruby>的一擊……」

### A4｜terminology｜Nao 誤作「奈央」（glossary 定論：奈緒）

- 位置：譯文第 261 行
- 原文：「observas que tu hermana Nao se encuentra en estado de shock」
- 譯文：「你看到你的姐姐奈央一臉呆滯」
- 問題：glossary 定論「Nao＝奈緒」；moves.md:168/487/493/677 均作「姊姊奈緒」。
- 建議修法：「你看到你的姊姊奈緒一臉呆滯」（「姊姊」並見 B12）。

### A5｜terminology｜Togami 誤作「弟弟」（全站主流：雙胞胎哥哥）

- 位置：譯文第 305 行
- 原文：「un Devorador de Luz se traga al hermano de Natsumi, Togami」
- 譯文：「一隻吞光者正在吞噬夏美的弟弟戶上」
- 問題：戶上是夏美的雙胞胎兄弟，主流譯為哥哥：moves.md:430「雙胞胎哥哥戶上」、moves.md:695「雙胞胎哥哥戶上」、light-vs-darkness.md:39「你哥哥」（2 次）。唯 light-vs-darkness.md:610 作「雙胞胎弟弟」，該處為既存全站矛盾，須一併統一。
- 建議修法：「夏美的哥哥戶上」。

### A6｜terminology｜profesor 誤作「教授」（校園語境應為「老師」）

- 位置：譯文第 257 行
- 原文：「la fría mirada de un profesor, un cambio en la actitud de una madre」
- 譯文：「一位教授冰冷的目光、一位母親態度的轉變」
- 問題：西文 profesor 泛指教師；本作為中學校園背景，全站均譯「老師」（moves.md:135/329、fundamentals.md:103/209/213、light-vs-darkness.md:602）。
- 建議修法：「一位老師冰冷的目光」。

### A7｜fidelity｜偶像段落漏譯「brillar más」並誤譯「luzca su corona」

- 位置：譯文第 474 行（### 偶像 第 3 段）
- 原文：「deberías usar su arma contra ella, de forma que pueda incluso brillar más utilizando rivales, enemigos, rumores… La vida social activa tiene un montón de elementos que hacen que una Idol luzca su corona a la vez que sufre por mantenerla.」
- 譯文：「你應該用她的武器來對付她——利用競爭對手、敵人、謠言……活躍的社交生活有大量元素能讓偶像在保衛皇冠的同時因維護它而受苦。」
- 問題：漏譯「de forma que pueda incluso brillar más」（讓她反而更加閃耀——這是使用此手法的目的）；「luzca su corona」是「展現皇冠的光彩」而非「保衛皇冠」。
- 建議修法：「因此，你應該用她的武器來對付她——藉由競爭對手、敵人、謠言……反而讓她更加閃耀。活躍的社交生活有大量元素，能讓偶像一面展現皇冠的光彩，一面為保住它而受苦。」

### A8｜fidelity｜「sin miedo ni subterfugios」誤譯為「不靠恐懼」

- 位置：譯文第 462 行（### 鬥士 第 1 段）
- 原文：「busca retos que pueda afrontar de cara, sin miedo ni subterfugios」
- 譯文：「追求可以正面迎擊的挑戰，不靠恐懼也不靠詭計」
- 問題：「sin miedo」是「無所畏懼」（描述迎擊時的態度），不是「不依靠恐懼」。
- 建議修法：「追求可以正面迎擊的挑戰——無所畏懼、不耍花招。」

### A9｜fidelity｜「lleva años detrás de esto」誤譯為「追查此事」

- 位置：譯文第 317 行
- 原文：「Según los rumores, el consejo escolar lleva años detrás de esto」
- 譯文：「據傳聞，學生會已經追查此事好幾年了」
- 問題：「llevar años detrás de esto」意為「多年來一直謀求此事（把社團廢掉）」，不是「調查」；誤譯後因果反轉（變成學生會在查案）。
- 建議修法：「據傳聞，學生會多年來一直想促成此事」。

### A10｜terminology｜數字慣例：「最後一個友情點數」

- 位置：譯文第 418 行（### 阿特洛波斯之禍 第 1 段）
- 原文：「cada vez que un PJ gasta su último Punto de Amistad, dejando su reserva a 0」
- 譯文：「每當玩家角色用完最後一個友情點數、將儲備降至 0 時」
- 問題：點數量須用阿拉伯數字（本章其餘處均遵守，如第 366 行「1 點，最多 2 點」）。
- 建議修法：「用完最後 1 點友情點數」。

### A11｜taiwan-usage｜「Mónica也」缺半形空格（格式不一致）

- 位置：譯文第 291 行
- 原文：「Sin embargo, Mónica también le indica que…」
- 譯文：「然而，Mónica也告訴她……」
- 問題：本章其餘 Mónica／Marion 後均有空格（第 343、346、360、370、374 行），僅此處漏排。
- 建議修法：「Mónica 也告訴她」。

## B 級（需決策）

### B1｜terminology｜「血之女王」與全站「血之公主」（原文本身不一致）

- 位置：譯文第 86 行
- 原文：「Un esclavo de la Reina de Sangre cae y te pega un mordisco.」
- 譯文：「血之女王的一個奴僕倒下來咬了你一口。」
- 問題：glossary 定論「Princesa de Sangre＝血之公主」，全站 26 處均作「血之公主」（本章 332、341 行亦同）；唯此處原文寫「Reina de Sangre」，應為原書筆誤或別稱，譯文照搬後產生一個全站僅出現一次的敵人名。
- 候選：
  1. 統一改「血之公主」——視原文為筆誤，維持全站敵人名單一（建議）。
  2. 保留「血之女王」——忠實反映原文差異，但需在 glossary 註記兩者同指一人，避免讀者誤認新敵人。

### B2｜terminology｜Yakumo 譯「藥雲」待商榷（未入 glossary）

- 位置：譯文第 317 行
- 原文：「si ayudáis a Yakumo a evitar que su club cierre」
- 譯文：「如果你們幫助藥雲阻止他的社團被解散」
- 問題：Yakumo 為日文名，通行漢字為「八雲」；「藥雲」非常見寫法（且與 friendship-romance.md:456 的動漫人物「塚本八雲」用字相左）。另原文「su」性別不明，譯文逕作「他的」。
- 候選：
  1. 「八雲」——日文名最通行寫法，與站內既有「八雲」用字一致（建議）。
  2. 保留「藥雲」——若刻意避免與動漫人名撞名，須入 glossary 並註明理由。

### B3｜fidelity｜「清美的姐姐」與既有設定「小妹妹」衝突

- 位置：譯文第 360 行
- 原文：「La hermana de Kiyomi entra en su cuarto. Está harta de cubrirla cada vez que desaparece…」
- 譯文：「清美的姐姐衝進她的房間。她受夠了每次清美消失時都要替她掩護……」
- 問題：西文 hermana 不分長幼，但 first-chapter.md:288「她有一個小妹妹」、first-chapter.md:226「要把她的小妹妹留在……醫院」已建立清美有妹妹的設定；此處譯「姐姐」可能自創一位新家人。
- 候選：
  1. 「清美的妹妹」——與 first-chapter 設定相容，掩護、吵架情節亦通（建議）。
  2. 保留「姐姐」——若判定原作者此處另指一位姐姐，須請使用者確認並記錄設定。

### B4｜terminology｜siervos／sirvientes de la Oscuridad 譯法分裂（黑暗使徒 vs 黑暗的爪牙）

- 位置：譯文第 18 行（siervos→黑暗使徒）、第 160 行（sirvientes→黑暗的爪牙）、第 323 行（siervos→黑暗的爪牙）
- 問題：glossary 僅定義「Servidores de la Oscuridad＝黑暗使徒」；原文以 siervos／sirvientes 作同義變體，譯文同一個西文詞（siervos）在同章一處譯「黑暗使徒」、一處譯「爪牙」。
- 候選：
  1. 一律統一為「黑暗使徒」——機制詞單一化，檢索友善（建議）。
  2. 正式名（Servidores）用「黑暗使徒」、散文變體（siervos/sirvientes）容許「黑暗的爪牙」——保留原文文體變化，但須在 glossary 註記此政策。

### B5｜terminology｜「星之王國」與「星辰王國」全站分裂（Reino de las Estrellas，未入 glossary）

- 位置：譯文第 281、305 行（星之王國）
- 問題：本章與 moves.md:250/260/517/545/636、pacts.md:544 用「星之王國」；eclipse.md:322/328/475/495/501/518/522-529 與 darkness-enemies.md:84/271 用「星辰王國」。約 8：13 分裂，須全站定案並入 glossary。
- 候選：
  1. 「星之王國」——與盟約章（此設定所屬的「光明子女」相關章節）及動作章一致。
  2. 「星辰王國」——出現次數略多（eclipse 章密集使用）。

### B6｜terminology｜「家常奇幻／高度奇幻」譯名待定（與 setting.md「日常奇幻」相左）

- 位置：譯文第 72、144、148 行（家常奇幻）；72、144 行（高度奇幻）
- 原文：「Fantasía doméstica contra alta fantasía」
- 問題：setting.md:237 將同概念譯為「日常奇幻」；「alta fantasía」台灣奇幻圈通行譯名為「高奇幻」（「高度奇幻」少見）。
- 候選：
  1. 「日常奇幻」對「高奇幻」——與 setting.md 一致且用台灣通行類型詞（建議）。
  2. 「家常奇幻」對「高奇幻」——保留 doméstica 的「居家」語感，但須回改 setting.md 統一。

### B7｜terminology｜DM／DJ 譯名（地城主持人／遊戲導演）

- 位置：譯文第 10 行
- 原文：「conocido como Dungeon Master (DM) o Director de Juego (DJ)」
- 譯文：「通常被稱為地城主持人（DM）或遊戲導演（DJ）」
- 問題：台灣 TRPG 圈通行譯名為「地下城主（DM）」與「遊戲主持人（GM／DJ）」；「地城主持人」「遊戲導演」皆非慣用。
- 候選：
  1. 「地下城主（DM）或遊戲主持人（DJ）」——採圈內通行說法（建議）。
  2. 「城主（DM）或遊戲導演（DJ）」——較直譯，保留西文 Director 的「導演」語感。

### B8｜fidelity｜被父母禁足的是誰（原文歧義）

- 位置：譯文第 122 行
- 原文：「el romance de un PJ puede estar esperándolo mientras cumple un castigo de sus padres」
- 譯文：「一個玩家角色的戀人可能正在等待，而玩家角色正在被父母禁足」
- 問題：「mientras cumple」主詞可為戀人（承接主句主詞）或 PJ；本節主旨為「畫面之外的 NPC 也有生活」，較支持是戀人（NPC）被自家父母禁足、在畫面外等待。譯文選了 PJ 被禁足的讀法。
- 候選：
  1. 「玩家角色的戀人可能一邊被自己父母禁足，一邊在畫面外等著她」——貼合本節「NPC 畫面外的生活」主旨（建議）。
  2. 維持現譯——PJ 被禁足亦通，但與段旨稍疏。

### B9｜fidelity｜「exponer su corazón」譯「敞開心扉」語意偏移

- 位置：譯文第 190 行
- 原文：「Si en algún momento un jugador ignora las señales de peligro, decide exponer su corazón o enfrentarse a un enemigo al que no puede derrotar…」
- 譯文：「一個玩家忽視了危險的訊號、決定敞開心扉、或是面對一個無法擊敗的敵人」
- 問題：與「忽視危險」「以卵擊石」並列，exponer su corazón 應是「讓內心（心之力量的根源）暴露於危險」；「敞開心扉」偏向「向人吐露心聲」，失去冒險語感。
- 候選：
  1. 「讓自己的內心暴露於危險之中」——保留與本作「心」主題機制的呼應（建議）。
  2. 「不設防地交出真心」——保留情感語感，兼帶風險意味。

### B10｜fluency｜第二人稱「你／妳」章內混用

- 位置：「妳」見譯文第 78、237、253、271 行；同為對魔法少女說話的範例，第 80、98、202、204、206、208、210、212、241、250、261、303、319 行等均用「你」
- 問題：同一章、同類 MC 對少女喊話的範例，兩種寫法並存；全站亦分裂（fundamentals.md 16 處「妳」為主，其他章多用「你」）。
- 候選：
  1. 對女性角色一律用「妳」——貼合全員魔法少女題材，與 fundamentals 一致。
  2. 一律用「你」——現代中文趨勢，維護成本低；但須回改各章「妳」。

### B11｜fluency｜第三人稱「他們／她們」指涉玩家角色時混用

- 位置：譯文第 18 行（讓他們毫無阻礙地成長→指 PJ）、第 158 行（他們最終會陷入冷漠……她們的勝利→同一主詞兩譯）、第 368 行（他們的盟約類型→指 PJ）、第 482 行（他們也想要贏……不要向她們提出→同段兩譯）
- 問題：「玩家＝他們、角色＝她們」的區分在多處未貫徹，甚至同句內切換，指涉混淆。
- 候選：
  1. 明確政策：指玩家（jugadores）一律「他們」，指玩家角色／魔法少女（PJ）一律「她們」，逐處校正（建議）。
  2. 全部統一「她們」——本作玩家群像亦以女性為預設（原書用 jugadoras 的段落不少），一刀切最簡單。

### B12｜taiwan-usage｜「姐姐」與全站「姊姊」分裂

- 位置：譯文第 98、261、358、360 行（姐姐）
- 問題：moves.md 同一人物（奈緒）5 處均作「姊姊」；台灣教育部標準字形為「姊」。全站另有 first-chapter.md:206、light-vs-darkness.md:18、friendship-romance.md 多處「姐」（含 glossary「Sororidad＝姐妹會」），須全站定案。
- 候選：
  1. 一律「姊姊／姊妹」——台灣標準用字，並同步修訂 glossary「姐妹會」（建議）。
  2. 一律「姐」——從 glossary 既有「姐妹會」，回改 moves.md。

### B13｜terminology｜本章未建檔專有名詞清單（批次建檔用）

- 位置／清單：
  - 伊野（Ino）——譯文第 94、269 行（章內一致）
  - 桐野・蘭格（Kirino Lange）——第 328 行
  - 名切美加子（Nakiri Mikako）——第 330 行
  - 血之吸血鬼（Vampiros de la Sangre）——第 247 行（「血之」＋「吸血鬼」語意重疊，可考慮「血之公主的吸血鬼」或「血族」）
  - 黑暗火焰的餘燼（Ascuas de Llamas Oscuras）——第 237 行（原文大寫，應為暗焰女巫麾下的傀儡名，宜名詞化如「暗焰餘燼」）
  - 無面者（el ser sin rostro）——第 343 行（原文小寫，可不建檔）
  - 格洛布錄影帶出租店（Videoclub Glob）——第 259、295、345 行；另全站同一地點有三種說法：錄影帶出租店（moves、本章）／錄影帶店（darkness-enemies、light-vs-darkness）／錄影店（eclipse），須統一
  - 星之王國、藥雲、血之女王——已見 B5、B2、B1
- 問題：以上均出現於全站 2 章以上或本章多處，依 Law 7 應入 glossary。
- 候選：批次以 term_edit.py 建檔（建議）／僅建跨章出現者。

### B14｜fluency｜衛士段落句式斷裂

- 位置：譯文第 454 行（### 衛士 第 1 段）
- 原文：「Este estilo de personaje crece y brilla en la adversidad, cuando puede ayudar a todas sus compañeras, por lo que suelen preferir historias de compañerismo y superación personal.」
- 譯文：「這種類型的角色在逆境中成長和閃耀，當她能幫助所有同伴時，所以他們往往偏好同伴情誼和個人成長的故事。」
- 問題：「當她能幫助所有同伴時」懸空插入，「所以」承接斷裂，且「他們」指涉又跳回玩家。
- 候選：
  1. 「這類角色在逆境中——尤其是能幫上所有同伴的時刻——成長茁壯、大放異彩，因此這類玩家往往偏好同伴情誼與自我成長的故事。」
  2. 「這類角色在能幫助所有同伴的逆境中最能成長與閃耀，所以選她的玩家通常偏好講同伴情誼和自我成長的故事。」

## C 級（建議）

- C1｜terminology｜第 86 行：反應名引用「對她們造成傷痛」與正式名「在她們的生活中製造傷痛」（第 228、348 行）不一致（原文亦為變體 «Crea angustia en ellas»）；引用處建議靠攏正式名。
- C2｜terminology｜第 319 行：「魔女」→「女巫」，與同章「暗焰女巫」（291、340 行）簡稱統一。
- C3｜terminology｜第 283 行「名門私校」vs 第 374 行「名門學校」——同一所學校（escuela de élite），建議統一為「名門學校」。
- C4｜fidelity｜第 10 行：「nunca llegan a esta parte」譯「通常不會讀到」弱化了原文的「從來不會」；此為玩笑句，建議「從來不會讀到書的這個部分」。
- C5｜taiwan-usage｜第 92 行：「成百上千」——原文 cientos（數以百計），且該四字語偏中國慣用；建議「數以百計的故事種子」。
- C6｜fidelity｜第 106 行：「salvar el día」譯「拯救世界」過重（建議「力挽狂瀾」）；且原文「con un brazo roto después de presenciar…」修飾「看她們擊敗邪惡」，譯文移到「拯救世界」上，建議重排：「用那個絕招力挽狂瀾，或看她們在目睹重要之人險些喪命後，帶著斷臂擊敗邪惡。」
- C7｜fluency｜第 140 行：「正是造就……的分水嶺」——「分水嶺」為增譯的比喻（原文僅 es lo que crea）；可簡化為「正是造就魔法少女和黑暗使徒的關鍵」。
- C8｜fluency｜第 188 行：「例如動作擲骰結果為 7 到 9 之間有時會標明特定後果」不成句；建議「例如動作擲出 7 到 9 的部分成功——這類結果有時會載明其後果——最終仍由你用反應來塑造場景」。
- C9｜fluency｜第 206 行：「眼白翻起」→「兩眼翻白」較自然。
- C10｜fluency｜第 212 行：「數十捲 VHS 和 DVD」——DVD 不以「捲」計；建議「數十捲 VHS 與成堆 DVD」。
- C11｜fluency｜第 303 行：「鼻子碎了」→「鼻梁斷了」；「清脆的響聲」帶正面聯想，建議「那聲喀啦就夠了」。
- C12｜fluency｜第 386 行：「在 Mahō Shōjo 中，沒有明確的規則」易讀成整個遊戲沒規則；建議「對此並沒有明確規則」。
- C13｜fluency｜第 410 行：「斷裂了與戀人的羈絆」——「斷裂」不及物；建議「斬斷了與戀人的羈絆」。
- C14｜taiwan-usage｜第 420 行：「汙染」與本章（394 行）及 glossary「黑暗污跡」的「污」字不一致；建議統一用字（全站以「污」為現況多數）。
- C15｜fluency｜第 448 行：「制定追溯性替代計畫」生硬；建議「甚至以回溯方式事後補上一套備用計畫」。
- C16｜fluency｜第 450 行：「在社交方面是參謀較為薄弱的地方」句式冗；建議「社交是參謀較弱的一環」。
- C17｜fluency｜第 432 行：「充滿戲劇和悲劇的故事」→「充滿戲劇性與悲劇的故事」。
- C18｜fidelity｜第 57 行：「就讓他們有所準備」（prepáralos）指涉不明；原意應為向玩家預作鋪陳，建議「就提早鋪陳、讓大家察覺得到」。
- C19｜terminology｜第 235 行：連結文字「黑暗使徒」與目標章實際標題「黑暗勢力」不符——但 moves.md:72、light-vs-darkness.md:567 亦同，屬全站既有慣例，供全站一次決策（連結文字改「黑暗勢力」或章名改「黑暗使徒」）。
- C20｜fluency｜第 360 行：「清美知道自己做的不對」→「做得不對」。

（未列入者：第 34 行與第 398 行對「抱著看看會發生什麼的心態去遊戲」的引用格式略異、第 295 行 encargado 譯「店員」（可作「店長」）——影響甚微，可不改。）
