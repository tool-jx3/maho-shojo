# 待收錄候選清單

本檔由 `scripts/build_reference_backlog.py` 依 [backlog/candidates-raw.tsv](backlog/candidates-raw.tsv) 產生，該原始檔則來自 `scripts/find_reference_candidates.py` 對各語言維基百科分類樹的掃描。

建立首批 35 條時，選錄清單是憑印象開出來的，因此像 Lutzelfrau 這種地方性形象根本沒有機會浮上檯面。本清單的用意是把「還有什麼沒收」變成可查證、可逐項檢視的問題。

## 怎麼用

- 這是**機器掃描的結果，不是選錄決定**。每一項都需要人工判斷是否適合收錄。
- 已收錄的條目會在重跑腳本時自動從清單消失，不必手動勾除。
- 判斷是否值得收錄時，優先看：有沒有發源語言的條目、內容量是否足以支撐逐段對譯、以及是否補上了現有資料庫沒有的維度（地區、語系、時代、類型）。
- **各主題清單的數字是 wikitext 原始碼的位元組數，不是純文字字數。**實測比值：歐洲語言約 1.7—2.2 倍，日／中／韓約 3.4—7.6 倍——也就是說同樣的位元組數，CJK 條目的實際內容只有歐洲條目的三分之一左右。跨語言比較時務必把這個偏差算進去。「優先候選」表則已換成實測的純文字字數。

## 統計

| 項目 | 數量 |
| --- | --- |
| 掃描結果原始筆數 | 5622 |
| 濾除：虛構作品與流行文化 | 2083 |
| 濾除：已收錄 | 49 |
| **待檢視** | **3490** |

掃描涵蓋 en、de、fr、es、it、sv、ru、pl、ja 九個語言版本的獵巫與巫術相關分類。未涵蓋的語言（ko、zh、ar、he、yo、ln 等）目前只能靠個別查找，這是本清單已知的偏誤。

分類樹裡混有大量虛構作品與流行文化條目，腳本的排除規則只能濾掉大部分，各主題清單中仍會殘留一些明顯不相干的項目。

## 優先候選（人工挑選）

以下是從掃描結果中挑出、明確屬於本資料庫範圍且尚未收錄的項目，可以直接從這裡開下一批。已收錄者會自動從表中消失。

| 條目 | 語言 | 純文字字數 | 為什麼值得收 |
| --- | --- | --- | --- |
| [Hexenverfolgung](https://de.wikipedia.org/wiki/Hexenverfolgung) | 德語 | 88,134 | 獵巫的德語總論條目，本庫目前只有個案沒有通論 |
| [Witch hunt](https://en.wikipedia.org/wiki/Witch_hunt) | 英語 | 53,375 | 獵巫的英語總論，可與德語版互為對照 |
| [Häxprocess](https://sv.wikipedia.org/wiki/H%C3%A4xprocess) | 瑞典語 | 112,801 | 瑞典語總論，補北歐視角 |
| [Hexenverfolgung im Waadtland](https://de.wikipedia.org/wiki/Hexenverfolgung_im_Waadtland) | 德語 | 20,656 | 沃州，歐洲最早的大規模獵巫地之一 |
| [Hexenprozesse in Freiburg (Schweiz)](https://de.wikipedia.org/wiki/Hexenprozesse_in_Freiburg_%28Schweiz%29) | 德語 | 33,460 | 瑞士地區審判，與安娜·葛爾迪一條互補 |
| [Hexenprozesse in der Grafschaft Werdenfels](https://de.wikipedia.org/wiki/Hexenprozesse_in_der_Grafschaft_Werdenfels) | 德語 | 21,865 | 巴伐利亞地區審判 |
| [Die Besessenen von Aix-en-Provence](https://de.wikipedia.org/wiki/Die_Besessenen_von_Aix-en-Provence) | 德語 | 23,279 | 1611 年附身案，與盧丹案同型 |
| [Cotton Mather](https://en.wikipedia.org/wiki/Cotton_Mather) | 英語 | 55,570 | 塞勒姆審判的關鍵推手，本庫已有塞勒姆卻無此人 |
| [Hostienfrevel](https://de.wikipedia.org/wiki/Hostienfrevel) | 德語 | 22,356 | 褻瀆聖體指控，與獵巫並行的迫害機制 |
| [Diana](https://de.wikipedia.org/wiki/Diana) | 德語 | 16,980 | 《主教教規》所述夜行女神信仰的源頭 |
| [Ritualmordlegende](https://de.wikipedia.org/wiki/Ritualmordlegende) | 德語 | 102,038 | 血祭誹謗，與獵巫平行的另一套迫害機制 |
| [Morgan le Fay](https://en.wikipedia.org/wiki/Morgan_le_Fay) | 英語 | 60,343 | 亞瑟王傳說中的女巫，本庫缺凱爾特—法蘭西線 |
| [Hecate](https://en.wikipedia.org/wiki/Hecate) | 英語 | 43,834 | 希臘巫術女神，喀爾刻條目多次提及卻無專條 |
| [Gilles de Rais](https://en.wikipedia.org/wiki/Gilles_de_Rais) | 英語 | 82,487 | 與魔鬼交易母題的著名審判 |
| [Аэндорская волшебница](https://ru.wikipedia.org/wiki/%D0%90%D1%8D%D0%BD%D0%B4%D0%BE%D1%80%D1%81%D0%BA%D0%B0%D1%8F_%D0%B2%D0%BE%D0%BB%D1%88%D0%B5%D0%B1%D0%BD%D0%B8%D1%86%D0%B0) | 俄語 | 27,750 | 隱多珥的女巫，聖經中的招魂者 |
| [Zduhać](https://en.wikipedia.org/wiki/Zduha%C4%87) | 英語 | 50,594 | 南斯拉夫的靈魂出竅戰士，與貝南丹提同型 |
| [Dahut](https://fr.wikipedia.org/wiki/Dahut) | 法語 | 49,743 | 布列塔尼伊斯城傳說中的女性形象 |
| [Lieu du sabbat](https://fr.wikipedia.org/wiki/Lieu_du_sabbat) | 法語 | 9,133 | 巫魔會地點的母題研究 |
| [Carrefour dans le folklore et la mythologie](https://fr.wikipedia.org/wiki/Carrefour_dans_le_folklore_et_la_mythologie) | 法語 | 51,042 | 十字路口母題，橫跨多個既有條目 |
| [Crapaud dans l'imaginaire et la tradition en Occident](https://fr.wikipedia.org/wiki/Crapaud_dans_l%27imaginaire_et_la_tradition_en_Occident) | 法語 | 77,248 | 蟾蜍母題，蘇加拉穆爾迪案的核心物證 |
| [Goezia (pratica magica)](https://it.wikipedia.org/wiki/Goezia_%28pratica_magica%29) | 義大利語 | 43,350 | 召魔術傳統，與魔法書條目互補 |
| [Guillaume Adeline](https://de.wikipedia.org/wiki/Guillaume_Adeline) | 德語 | 15,935 | 15 世紀的獵巫反對者，早於魏爾一個世紀 |
| [Johannes Pistorius der Jüngere](https://de.wikipedia.org/wiki/Johannes_Pistorius_der_J%C3%BCngere) | 德語 | 13,124 | 獵巫反對者 |
| [Matthäus Alber](https://de.wikipedia.org/wiki/Matth%C3%A4us_Alber) | 德語 | 19,672 | 獵巫反對者 |
| [Simon Gogräve](https://de.wikipedia.org/wiki/Simon_Gogr%C3%A4ve) | 德語 | 12,596 | 獵巫反對者 |
| [Dietrich Schnepf](https://de.wikipedia.org/wiki/Dietrich_Schnepf) | 德語 | 11,741 | 獵巫反對者 |
| [Bader-Ann](https://de.wikipedia.org/wiki/Bader-Ann) | 德語 | 51,904 | 受害者個案 |
| [Paula von Weitershausen](https://de.wikipedia.org/wiki/Paula_von_Weitershausen) | 德語 | 29,542 | 加害者個案 |
| [Sebastian Röttinger](https://de.wikipedia.org/wiki/Sebastian_R%C3%B6ttinger) | 德語 | 20,309 | 加害者個案 |
| [Elizabeth Howe](https://en.wikipedia.org/wiki/Elizabeth_Howe) | 英語 | 15,397 | 塞勒姆受害者個案 |
| [Elizabeth Frauncis](https://en.wikipedia.org/wiki/Elizabeth_Frauncis) | 英語 | 8,879 | 英格蘭最早的女巫審判被告之一 |
| [巫女](https://ja.wikipedia.org/wiki/%E5%B7%AB%E5%A5%B3) | 日語 | 6,477 | 日本的神職少女，與歐洲「女巫是被迫害者」完全相反的模式 |
| [斎宮](https://ja.wikipedia.org/wiki/%E6%96%8E%E5%AE%AE) | 日語 | 5,788 | 卜定的未婚皇女，被選中後與世隔絕侍神，最徹底的「被選中的少女」制度 |
| [陰陽道](https://ja.wikipedia.org/wiki/%E9%99%B0%E9%99%BD%E9%81%93) | 日語 | 7,281 | 式神與安倍晴明條目的制度背景 |
| [イタコ](https://ja.wikipedia.org/wiki/%E3%82%A4%E3%82%BF%E3%82%B3) | 日語 | 1,894 | 東北地方的盲眼女性靈媒，口寄せ（招魂）　**篇幅偏薄** |
| [ユタ](https://ja.wikipedia.org/wiki/%E3%83%A6%E3%82%BF) | 日語 | 8,282 | 沖繩的女性靈媒，與制度性的ノロ相對的民間靈能者 |
| [ノロ](https://ja.wikipedia.org/wiki/%E3%83%8E%E3%83%AD) | 日語 | 3,694 | 琉球的女祭司，聞得大君之下的神女組織　**篇幅偏薄** |
| [飯縄権現](https://ja.wikipedia.org/wiki/%E9%A3%AF%E7%B8%84%E6%A8%A9%E7%8F%BE) | 日語 | 2,657 | 飯綱法與管狐信仰的本尊　**篇幅偏薄** |
| [扶乩](https://zh.wikipedia.org/wiki/%E6%89%B6%E4%B9%A9) | 中文 | 1,809 | 漢文化圈的降筆術，與歐洲的招魂術可對照　**篇幅偏薄** |
| [麻姑](https://zh.wikipedia.org/wiki/%E9%BA%BB%E5%A7%91) | 中文 | 2,364 | 道教女仙，長生與滄海桑田的象徵　**篇幅偏薄** |
| [무녀](https://ko.wikipedia.org/wiki/%EB%AC%B4%EB%85%80) | 韓語 | 5,877 | 韓國的女巫，무당條目的性別專條 |
| [굿](https://ko.wikipedia.org/wiki/%EA%B5%BF) | 韓語 | 3,482 | 韓國巫俗的儀式，바리공주敘事詩即在其中吟唱　**篇幅偏薄** |
| [점복](https://ko.wikipedia.org/wiki/%EC%A0%90%EB%B3%B5) | 韓語 | 2,590 | 韓國的占卜傳統　**篇幅偏薄** |
| [마고할미](https://ko.wikipedia.org/wiki/%EB%A7%88%EA%B3%A0%ED%95%A0%EB%AF%B8) | 韓語 | 678 | 韓國的創世女神，與中國麻姑同源　**篇幅偏薄** |

本表的字數為實測的**純文字字數**（`prop=extracts&explaintext`），標「（估）」者為原始碼位元組的估算值，標「—」者不在掃描涵蓋範圍內。標「篇幅偏薄」者純文字不足 4000 字，可能撐不起逐段對譯的體例，收錄前要先確認實際可用內容。

## 依主題分列

| 主題 | 項數 | 清單 |
| --- | --- | --- |
| 獵巫受害者（個案） | 154 | [backlog/victims.md](backlog/victims.md) |
| 獵巫加害者 | 83 | [backlog/perpetrators.md](backlog/perpetrators.md) |
| 獵巫的反對者 | 29 | [backlog/opponents.md](backlog/opponents.md) |
| 被處決者 | 163 | [backlog/executed.md](backlog/executed.md) |
| 受指控者與指控者 | 86 | [backlog/accused.md](backlog/accused.md) |
| 審判事件 | 245 | [backlog/trials.md](backlog/trials.md) |
| 巫術研究者與研究史 | 31 | [backlog/scholarship.md](backlog/scholarship.md) |
| 傳說中的巫者形象 | 142 | [backlog/legendary-witches.md](backlog/legendary-witches.md) |
| 小妖精與使魔 | 39 | [backlog/imps-familiars.md](backlog/imps-familiars.md) |
| 詛咒與法術 | 211 | [backlog/curses.md](backlog/curses.md) |
| 童話中的女巫 | 98 | [backlog/fairy-tales.md](backlog/fairy-tales.md) |
| 傳說人物與怪異存在 | 85 | [backlog/legendary-beings.md](backlog/legendary-beings.md) |
| 獵巫的文化再現 | 146 | [backlog/reception.md](backlog/reception.md) |
| 各地區的巫術 | 272 | [backlog/regional.md](backlog/regional.md) |
| 其他 | 1706 | [backlog/misc.md](backlog/misc.md) |

完整未篩選的掃描結果保存在 [backlog/candidates-raw.tsv](backlog/candidates-raw.tsv)，包含被規則濾掉的項目，以免有東西被靜默丟棄。
