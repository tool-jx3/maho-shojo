# 翻譯檢核報告：archetypes（原型扮演書）

檢核日期：2026-08-17　原文：es/rules/archetypes.md（原始萃取稿）　譯文：rules/archetypes.md

## 摘要

- 檢核段落數：約 150（散文 35 段＋六張扮演書全部區塊）／發現問題：A 級 3 筆、B 級 8 筆、C 級 14 筆
- 整體評語：整體品質良好——六張扮演書的表格數值、屬性組合、成長清單與動作效果經逐格比對全數正確，術語（動作名、後果名、光之裝束力量）在本章內部高度一致且符合 glossary。主要問題集中在兩處：點數量詞全章使用中文數字（違反數字慣例，且與同句的阿拉伯數字混用）；以及本章 54 個動作／選項名未入 glossary，其中「受眷顧者」的選項名已與 character-creation、moves、first-chapter 三章出現不同譯法，急需統一建檔。

## A 級（明確錯誤）

### A1｜terminology｜點數量詞全章用中文數字，違反數字慣例且同章（甚至同句）混用

- 位置：譯文第 122、202、205、208、214、221、356、359、372、376、384、493、498、501、590、608、611、626、629、634、717、720、723、732、735、751、762、764、766、795、857、866、869、870、871、873 行
- 原文：「Consigues 1 Punto de Luz」「ganas 3 puntos de Ímpetu」「gasta 1 punto de Popularidad」「baja en 1 punto tu Medidor de Poder」等（原文一律用阿拉伯數字）
- 譯文：「獲得一點光點」「獲得三點活力」「花費一點人氣值」「將你的能力量表降低一點」「消除兩點」等
- 問題：專案數字慣例明定「骰值、點數、數值用阿拉伯數字（『1 點』不是『一點』）」。本章所有資源點數（光點、友情點數、黑暗點數、活力、人氣值、神聖力量點數）皆用中文數字，而傷痛與吸收值卻用阿拉伯數字，同章混用即為 A 級；第 590 行「花費一點活力來抵消 8 點傷痛」更是同句混用。第 626 行「人氣值永遠不能超過一點」還會誤讀為「超過一點點」。
- 建議修法：全部改為阿拉伯數字——「獲得 1 點光點」「獲得 3 點活力」「花費 1 點人氣值」「降低 1 點」「消除 2 點」「不能超過 1 點」等。
- 附註（全站佐證）：此問題並非本章獨有——pacts.md 多用「1 點友情點數」（68、89、98 行等），friendship-romance.md 幾乎全用「一點」（39、60、65 行等），moves.md 甚至 453 行「1 點友情點數」與 466 行「一點友情點數」描述同一動作。建議列入全站批次統一（類似已知議題「創建」的處理方式），但本章佔比最高、應優先修正。

### A2｜fidelity｜衛士簡介漏譯「不失去光明」子句

- 位置：譯文第 46 行（### 衛士 下第 2 段）
- 原文：「un poderoso código de valores, que le permite centrar su corazón para no perder la Luz y confundirla con la Oscuridad」
- 譯文：「一套強大的價值準則，使她能夠安定內心，不讓光明與黑暗混淆」
- 問題：「para no perder la Luz」（不致失去光明）未譯出，只剩「混淆」一半語意。
- 建議修法：「一套強大的價值準則，使她能夠定住己心，不致失去光明、將光明與黑暗混淆。」

### A3｜fidelity｜「沒事了，明天一切都會好起來」7-9 選項主詞遺失，規則對象不明

- 位置：譯文第 870–873 行（聖母 進階動作）
- 原文：「7-9 Elimina el Punto de Oscuridad, elige uno: El PJ elegido y tú perdéis un Punto de Amistad. / Recibe una Consecuencia. / Ganas un Punto de Oscuridad.」
- 譯文：「7-9　消除該黑暗點數，選擇其一：被選中的玩家角色與你各失去一點友情點數。／承受一項後果。／獲得一點黑暗點數。」
- 問題：第三個選項原文為第二人稱「Ganas」（你獲得），譯文省略主詞後，讀者可能誤以為是被選中的玩家角色獲得黑暗點數，規則對象偏移。第二個選項原文「Recibe」為第三人稱（對照「Ganas」的刻意區別，較可能指被選中的玩家角色），譯文同樣無主詞。
- 建議修法：第三項改「你獲得 1 點黑暗點數。」；第二項建議補為「該玩家角色承受一項後果。」（原文此項有歧義，若判讀為施術者代價則作「你承受一項後果。」，請於定稿時擇一）。

## B 級（需決策）

### B1｜terminology｜「受眷顧者」選項名跨章譯法分裂（正義之力／以正義之力；心之引導／由心指引）

- 位置：譯文第 112 行「**正義之力**」、第 115 行「**心之引導**」
- 原文：「Por el poder de la Justicia」「Guiada por el corazón」
- 問題：跨章查證顯示其他三章使用不同譯名——「以正義之力」見 moves.md:83、first-chapter.md:442、character-creation.md:323（3 處，為多數）；「由心指引」見 character-creation.md:323。本章（選項的定義處）反而是少數形，且兩名皆未入 glossary。
- 候選：
  1. 全站統一為「以正義之力」「由心指引」——現有多數，且保留原文介詞「Por／Guiada por」的語感；只需改本章 2 處。
  2. 全站統一為「正義之力」「心之引導」——名詞化較像選項名、與同列的「神聖優雅」「救世主」風格一致；需批改其他三章 4 處。
  - 無論何者，決定後應立即入 glossary。

### B2｜terminology｜成長清單條目措辭與 advancement 章系統性不一致（解鎖／取得、上限／最高、獲得／取得）

- 位置：譯文第 187（上限 2）、188、189（解鎖）、196、197、328、455、573、702、839 行等（六張扮演書的成長清單）
- 原文：「Accedes a la forma Súper del Lux Habitu」「Mejorar una Característica (Máx. 2)」「Obtienes un Movimiento de Escudo de Luz」「Consigue 3 opciones adicionales de…」
- 問題：同一批成長條目在 advancement.md 有另一套定名——「取得光之裝束的超級形態」（advancement.md:86）vs 本章「解鎖光之裝束的超級形態」；「提升一項屬性（最高 2）」（advancement.md:112）vs 本章「（上限 2）」；「取得一個光之盾動作」（advancement.md:126）vs 本章「獲得一項光之盾動作」；「額外獲得『受眷顧者』的三個選項」（advancement.md:104）vs 本章「獲得『受眷顧者』的三個額外選項」。玩家對照兩章時會以為是不同條目。
- 候選：
  1. 以 advancement.md 為準（取得／最高／一個）——該章是成長規則的主敘述章，條目有錨點與詳解。
  2. 以本章為準（解鎖／上限／一項）——「解鎖」較符合遊戲語感、「上限」較精確；再批改 advancement.md。
  - 任一方案都建議把整套條目名視為受管理術語。

### B3｜terminology｜本章 54 個動作／選項名未入 glossary（批次建檔清單）

- 問題：依已知議題 3 只列清單供批次建檔。以下名稱皆已在本章定名且章內一致（含概述段與扮演書區塊交叉使用）：
  - 勇者選項：正義之力（Por el poder de la Justicia）、神聖優雅（Elegancia Divina）、守護者的低語（Susurros de los Guardianes）、心之引導（Guiada por el corazón）、救世主（Salvadora）、不屈（Indómita）
  - 勇者動作：內心的光永不消逝（La Luz nunca desaparece del corazón）、領銜（Primera entre iguales）、光之心（Corazón de Luz）、正義必勝（El bien siempre triunfa）、我從不孤單（Jamás estoy sola）
  - 參謀：計中計（Tramas dentro de la trama）、日常記事與購物清單（Agendas y listas de la compra）、理性凌駕感性（La razón sobre el corazón）、務實主義（Pragmática）、一絲不苟（Puntillosa）、遠端支援（Asistencia remota）、秘密之鑰（Llave de los secretos）、隱身匿跡（Pasar al anonimato）
  - 衛士：由我代受苦痛（Yo sufriré por ti）、在我的庇護下（Bajo mi protección）、今天我來煮飯（Hoy cocino yo）、休想碰她（Ni te atrevas a tocarla）、她守護我們，輪到我們了（Ella nos protege, nos toca a nosotras）、我不會再失敗了（No volveré a fallar）、我們同在（Estamos juntas en esto）、你對我的朋友有意見嗎？（¿Tienes algún problema con mis amigas?）
  - 鬥士：狂野之心（Corazón desatado）、心中之刃（Arma en el corazón）、天生戰略家（Estratega nata）、正義之拳（Mano de la Justicia）、堅不可摧（Indestructible）、吾志所向無不可為（Mi voluntad todo lo puede）、你的對手是我（Yo soy tu rival）、同心協力（Todas a una）、人生即是戰場（La vida es una batalla）
  - 偶像：我要感謝我的粉絲（Quiero dar las gracias a mis fans）、你認為他們會選誰？（¿A quién crees que elegirán?）、我無法壓抑我的感情，好嗎？（No controlo mis sentimientos, ¿vale?）、這一切好無聊……來讓氣氛熱鬧起來吧！（Todo esto es tan aburrido… ¡Vamos a animarlo!）、我的粉絲正這麼期待著（Mi público lo pide）、你們沒注意到他們看彼此的神情嗎？（¿No os fijasteis en cómo se miraban?）、別害羞，你認識……嗎？（No seas tímida, ¿conoces a…?）、沒錯，這就是我……（Sí, soy yo…）
  - 聖母：祝福攻擊（Bendecir ataque）、神聖支援（Apoyo sagrado）、束縛黑暗（Encadenar la Oscuridad）、療癒（Sanar）、生活美德（Vida de virtud）、靈魂之窗（Ver el alma en los ojos）、永遠可以更好（Siempre se puede ser mejor）、直覺與預感（Intuición y corazonada）、永不放棄（Nunca rendirse）、沒事了，明天一切都會好起來（Ya pasó, todo irá mejor mañana）
- 其中「堅不可摧」已在 light-vs-darkness.md:27、91 被引用（一致）、「正義必勝」已在 light-vs-darkness.md:156 被引用（一致）——跨章引用已發生，建檔優先度高。

### B4｜terminology｜勇者動作「光之心」與 glossary 既有詞條「Corazón de Luz＝光明聖地」同名衝突

- 位置：譯文第 26、207 行；另 advancement.md:65 亦引用「光之心」動作
- 問題：glossary 現有「Corazón de Luz」詞條的 notes 為「地球上的光明聖地」，與本章的勇者進階動作同西文同譯名。glossary 已有消歧先例（Escudo de Luz (Sanadora)＝光之護盾）。
- 候選：
  1. 維持同名，glossary 增設「Corazón de Luz (Campeona)」詞條註明是勇者動作——原文本就同名，讀者亦可接受。
  2. 動作改譯「光明之心」以區隔聖地——消歧最徹底，但需改 3 處並確認聖地譯名出現章節。

### B5｜fidelity｜「Mi público lo pide」的 público 譯「粉絲」，與另一動作的 fans 混同

- 位置：譯文第 82、88、719 行
- 原文：「Mi público lo pide」（我的觀眾要求如此）；另有「Quiero dar las gracias a mis fans」（我要感謝我的粉絲）
- 譯文：「我的粉絲正這麼期待著」
- 問題：público（觀眾／大眾）與 fans（粉絲）是兩個不同概念，兩動作譯名共用「粉絲」，弱化了原文的區別（前者觸發不需要粉絲在場，只需有人看見；後者明定「en presencia de algún fan」）。
- 候選：
  1. 「觀眾正這麼期待著」——保留 público／fans 的機制區別。
  2. 「這是觀眾的心聲」——更口語的偶像宣言腔。
  3. 維持現譯——名稱較順口，但接受兩詞混同。

### B6｜fluency｜「領銜」（Primera entre iguales）語意流失

- 位置：譯文第 26、204 行
- 原文：「Primera entre iguales」（同儕之中的第一人，典出 primus inter pares）
- 譯文：「領銜」
- 問題：「領銜」是演藝掛名用語，遺失「在平起平坐的同伴中居首」的意涵；此動作觸發條件正是「你是唯一面對黑暗存在的魔法少女」。
- 候選：
  1. 「同儕之首」——直譯保義。
  2. 「群芳之首」——保義且帶少女作品氣息。
  3. 維持「領銜」——最簡短，但義偏。

### B7｜fluency｜「吾志所向無不可為」文言腔與全章口語動作名風格不合

- 位置：譯文第 70、592 行
- 原文：「Mi voluntad todo lo puede」（我的意志無所不能——直白的第一人稱宣言）
- 問題：本章動作名多為角色口語（「我不會再失敗了」「你的對手是我」「休想碰她」），此名獨用文言句式，語域跳動；原文並無古雅意涵（依準則須標記過度風格化）。
- 候選：
  1. 「我的意志無所不能」——白話直譯，與其他動作名同腔。
  2. 「意志所向，無所不能」——折衷。
  3. 維持現譯——較有氣勢，但風格突出。

### B8｜taiwan-usage｜「秘」／「祕」全站用字分裂，本章用「秘」

- 位置：譯文第 40、351 行（秘密之鑰）
- 問題：全站兩形並存——「祕」見 pacts.md（50、54、219）、mc-guide.md（356、360）、fundamentals.md、first-chapter.md（155、316）、darkness-enemies.md（325）、character-creation.md（210）；「秘」見 setting.md（多處）、friendship-romance.md（187–196 等）與本章。教育部標準字為「祕」。兩者皆非簡體字，故列 B 供全站決策。
- 候選：
  1. 全站統一「祕」——符合台灣教育部標準。
  2. 全站統一「秘」——通行俗體，現有出現數略多。

## C 級（建議）

- C1｜格式｜動作名引號不一：第 52 行「心靈之盾」、第 839 行「神聖力量」未加「」，同段「由我代受苦痛」「受眷顧者」等皆有引號。建議補齊。
- C2｜taiwan-usage｜第 12 行「成長列表」→「成長清單」（台灣慣用；本章第 255 行已用「購物清單」，章內混用）。
- C3｜taiwan-usage｜第 248 行「備案」在台灣主要指「向機關登記」，作「plan B」建議改「備用方案」或「B 計畫」。
- C4｜fluency｜第 38 行「當進入行動時，『計中計』能讓她……」主語懸空，建議「當『計中計』發動時，她能奪回……」。
- C5｜fluency／fidelity｜第 74 行西式前置結構「永遠關注潮流……，偶像魔法少女通常……」建議主語前移；第 76 行「她不喜歡其他人不看她」雙重否定，建議「若旁人不注視她，她會感到不快」；第 78 行 es「es algo inspirador」（鼓舞人心）未譯，建議「忠於自我是鼓舞人心的特質……」。
- C6｜fluency｜第 62 行「將自己的力量導向黑暗」易誤讀為「投向黑暗」，原文 canalizando sus habilidades contra ella＝用於對抗黑暗，建議「將自身能力用於對抗黑暗」。
- C7｜fluency｜第 348 行「存取某種形式的輔助」——asistente 是具體的助手（AI、精靈、書本、盟友），建議「當你擁有某種形式的助手……只要能取得其協助」。
- C8｜fluency｜第 359 行「花費一點友情點數來不被注意」拗口，建議「讓自己不引人注目，或從場景中消失」。
- C9｜fluency｜零星贅句：第 343 行「進行『抵抗黑暗』的擲骰」→「為『抵抗黑暗』擲骰」；第 482 行「當你試圖保護某人時，使用……動作時」雙「時」；第 498 行「來在該動作中獲得」；第 587 行「向黑暗使徒斥責此事」→「為此斥責黑暗使徒」；第 596 行「面對一個正在騷擾你想保護的人的敵人或某人」的字堆疊，建議「當某個敵人（或任何人）正騷擾你想保護的對象，而你試圖吸引其注意力時」。
- C10｜fidelity｜第 32 行「inconvenientes」譯「不便」偏輕，建議「缺點」或「麻煩」。
- C11｜fidelity｜第 863 行「你必須繼續執行『失去光明』動作」——seguir realizando 意為「仍須照常執行」（消除後果不免除場末擲骰），建議「場景結束時你仍須執行『失去光明』動作」。
- C12｜terminology｜第 771 行「代替吸收這些傷害」——回指對象是 Angustia（傷痛），建議「替其吸收這些傷痛」。
- C13｜命名雜項（可與 B3 建檔一併定奪）：第 492 行「狂野之心」（Corazón desatado＝解放的心）建議「解放之心」；第 850 行「生活美德」（Vida de virtud）語序建議「美德人生」；第 26、210 行「正義必勝」之 bien＝「善」非「正義」，本章已有「正義之力」「正義之拳」（各對應不同原文）共用「正義」，可考慮「邪不勝正」或「善良必勝」以區隔。
- C14｜跨章備忘（非本章錯誤）：first-chapter.md:364 用「上台……Let's go」違反 glossary 定名「登上舞台……Let's go」（本章正確）；light-vs-darkness.md:171、204 用「一個光點」與全站「一點／1 點光點」再添第三種量詞形，請於該二章報告處理。
