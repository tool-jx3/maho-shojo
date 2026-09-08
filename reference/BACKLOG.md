# 待收錄候選清單

本檔由 `scripts/build_reference_backlog.py` 依 [backlog/candidates-raw.tsv](backlog/candidates-raw.tsv) 產生，該原始檔則來自 `scripts/find_reference_candidates.py` 對各語言維基百科分類樹的掃描。

建立首批 35 條時，選錄清單是憑印象開出來的，因此像 Lutzelfrau 這種地方性形象根本沒有機會浮上檯面。本清單的用意是把「還有什麼沒收」變成可查證、可逐項檢視的問題。

## 怎麼用

- 這是**機器掃描的結果，不是選錄決定**。每一項都需要人工判斷是否適合收錄。
- 已收錄的條目會在重跑腳本時自動從清單消失，不必手動勾除。
- 判斷是否值得收錄時，優先看：有沒有發源語言的條目、內容量是否足以支撐逐段對譯、以及是否補上了現有資料庫沒有的維度（地區、語系、時代、類型）。
- 字元數是該語言維基條目的原始大小，僅供粗估；實際可用內容要擷取後才知道。

## 統計

| 項目 | 數量 |
| --- | --- |
| 掃描結果原始筆數 | 4563 |
| 濾除：虛構作品與流行文化 | 2061 |
| 濾除：已收錄 | 42 |
| **待檢視** | **2460** |

掃描涵蓋 en、de、fr、es、it、sv、ru、pl、ja 九個語言版本的獵巫與巫術相關分類。未涵蓋的語言（ko、zh、ar、he、yo、ln 等）目前只能靠個別查找，這是本清單已知的偏誤。

分類樹裡混有大量虛構作品與流行文化條目，腳本的排除規則只能濾掉大部分，各主題清單中仍會殘留一些明顯不相干的項目。

## 優先候選（人工挑選）

以下是從掃描結果中挑出、明確屬於本資料庫範圍且尚未收錄的項目，可以直接從這裡開下一批。已收錄者會自動從表中消失。

| 條目 | 語言 | 字元數 | 為什麼值得收 |
| --- | --- | --- | --- |
| [Hexenverfolgung](https://de.wikipedia.org/wiki/Hexenverfolgung) | 德語 | 163,295 | 獵巫的德語總論條目，本庫目前只有個案沒有通論 |
| [Witch hunt](https://en.wikipedia.org/wiki/Witch_hunt) | 英語 | 117,050 | 獵巫的英語總論，可與德語版互為對照 |
| [Häxprocess](https://sv.wikipedia.org/wiki/H%C3%A4xprocess) | 瑞典語 | 147,513 | 瑞典語總論，補北歐視角 |
| [Hexenverfolgung im Waadtland](https://de.wikipedia.org/wiki/Hexenverfolgung_im_Waadtland) | 德語 | 36,795 | 沃州，歐洲最早的大規模獵巫地之一 |
| [Hexenprozesse in Freiburg (Schweiz)](https://de.wikipedia.org/wiki/Hexenprozesse_in_Freiburg_%28Schweiz%29) | 德語 | 52,041 | 瑞士地區審判，與安娜·葛爾迪一條互補 |
| [Hexenprozesse in der Grafschaft Werdenfels](https://de.wikipedia.org/wiki/Hexenprozesse_in_der_Grafschaft_Werdenfels) | 德語 | 41,445 | 巴伐利亞地區審判 |
| [Die Besessenen von Aix-en-Provence](https://de.wikipedia.org/wiki/Die_Besessenen_von_Aix-en-Provence) | 德語 | 28,732 | 1611 年附身案，與盧丹案同型 |
| [Cotton Mather](https://en.wikipedia.org/wiki/Cotton_Mather) | 英語 | 87,775 | 塞勒姆審判的關鍵推手，本庫已有塞勒姆卻無此人 |
| [Hostienfrevel](https://de.wikipedia.org/wiki/Hostienfrevel) | 德語 | 31,916 | 褻瀆聖體指控，與獵巫並行的迫害機制 |
| [Diana](https://de.wikipedia.org/wiki/Diana) | 德語 | 26,907 | 《主教教規》所述夜行女神信仰的源頭 |
| [Ritualmordlegende](https://de.wikipedia.org/wiki/Ritualmordlegende) | 德語 | 172,077 | 血祭誹謗，與獵巫平行的另一套迫害機制 |
| [Morgan le Fay](https://en.wikipedia.org/wiki/Morgan_le_Fay) | 英語 | 126,136 | 亞瑟王傳說中的女巫，本庫缺凱爾特—法蘭西線 |
| [Hecate](https://en.wikipedia.org/wiki/Hecate) | 英語 | 102,208 | 希臘巫術女神，喀爾刻條目多次提及卻無專條 |
| [Gilles de Rais](https://en.wikipedia.org/wiki/Gilles_de_Rais) | 英語 | 207,509 | 與魔鬼交易母題的著名審判 |
| [Аэндорская волшебница](https://ru.wikipedia.org/wiki/%D0%90%D1%8D%D0%BD%D0%B4%D0%BE%D1%80%D1%81%D0%BA%D0%B0%D1%8F_%D0%B2%D0%BE%D0%BB%D1%88%D0%B5%D0%B1%D0%BD%D0%B8%D1%86%D0%B0) | 俄語 | 68,413 | 隱多珥的女巫，聖經中的招魂者 |
| [Zduhać](https://en.wikipedia.org/wiki/Zduha%C4%87) | 英語 | 78,266 | 南斯拉夫的靈魂出竅戰士，與貝南丹提同型 |
| [Dahut](https://fr.wikipedia.org/wiki/Dahut) | 法語 | 83,279 | 布列塔尼伊斯城傳說中的女性形象 |
| [Lieu du sabbat](https://fr.wikipedia.org/wiki/Lieu_du_sabbat) | 法語 | 99,825 | 巫魔會地點的母題研究 |
| [Carrefour dans le folklore et la mythologie](https://fr.wikipedia.org/wiki/Carrefour_dans_le_folklore_et_la_mythologie) | 法語 | 88,150 | 十字路口母題，橫跨多個既有條目 |
| [Crapaud dans l'imaginaire et la tradition en Occident](https://fr.wikipedia.org/wiki/Crapaud_dans_l%27imaginaire_et_la_tradition_en_Occident) | 法語 | 143,231 | 蟾蜍母題，蘇加拉穆爾迪案的核心物證 |
| [Goezia (pratica magica)](https://it.wikipedia.org/wiki/Goezia_%28pratica_magica%29) | 義大利語 | 108,386 | 召魔術傳統，與魔法書條目互補 |
| [Guillaume Adeline](https://de.wikipedia.org/wiki/Guillaume_Adeline) | 德語 | 33,830 | 15 世紀的獵巫反對者，早於魏爾一個世紀 |
| [Johannes Pistorius der Jüngere](https://de.wikipedia.org/wiki/Johannes_Pistorius_der_J%C3%BCngere) | 德語 | 17,752 | 獵巫反對者 |
| [Matthäus Alber](https://de.wikipedia.org/wiki/Matth%C3%A4us_Alber) | 德語 | 26,653 | 獵巫反對者 |
| [Simon Gogräve](https://de.wikipedia.org/wiki/Simon_Gogr%C3%A4ve) | 德語 | 32,795 | 獵巫反對者 |
| [Dietrich Schnepf](https://de.wikipedia.org/wiki/Dietrich_Schnepf) | 德語 | 17,626 | 獵巫反對者 |
| [Bader-Ann](https://de.wikipedia.org/wiki/Bader-Ann) | 德語 | 55,937 | 受害者個案 |
| [Paula von Weitershausen](https://de.wikipedia.org/wiki/Paula_von_Weitershausen) | 德語 | 52,506 | 加害者個案 |
| [Sebastian Röttinger](https://de.wikipedia.org/wiki/Sebastian_R%C3%B6ttinger) | 德語 | 45,447 | 加害者個案 |
| [Elizabeth Howe](https://en.wikipedia.org/wiki/Elizabeth_Howe) | 英語 | 25,765 | 塞勒姆受害者個案 |
| [Elizabeth Frauncis](https://en.wikipedia.org/wiki/Elizabeth_Frauncis) | 英語 | 26,198 | 英格蘭最早的女巫審判被告之一 |

## 依主題分列

| 主題 | 項數 | 清單 |
| --- | --- | --- |
| 獵巫受害者（個案） | 130 | [backlog/victims.md](backlog/victims.md) |
| 獵巫加害者 | 73 | [backlog/perpetrators.md](backlog/perpetrators.md) |
| 獵巫的反對者 | 27 | [backlog/opponents.md](backlog/opponents.md) |
| 被處決者 | 124 | [backlog/executed.md](backlog/executed.md) |
| 受指控者與指控者 | 77 | [backlog/accused.md](backlog/accused.md) |
| 審判事件 | 242 | [backlog/trials.md](backlog/trials.md) |
| 巫術研究者與研究史 | 29 | [backlog/scholarship.md](backlog/scholarship.md) |
| 傳說中的巫者形象 | 135 | [backlog/legendary-witches.md](backlog/legendary-witches.md) |
| 小妖精與使魔 | 36 | [backlog/imps-familiars.md](backlog/imps-familiars.md) |
| 詛咒與法術 | 211 | [backlog/curses.md](backlog/curses.md) |
| 童話中的女巫 | 98 | [backlog/fairy-tales.md](backlog/fairy-tales.md) |
| 傳說人物與怪異存在 | 85 | [backlog/legendary-beings.md](backlog/legendary-beings.md) |
| 獵巫的文化再現 | 146 | [backlog/reception.md](backlog/reception.md) |
| 各地區的巫術 | 259 | [backlog/regional.md](backlog/regional.md) |
| 其他 | 788 | [backlog/misc.md](backlog/misc.md) |

完整未篩選的掃描結果保存在 [backlog/candidates-raw.tsv](backlog/candidates-raw.tsv)，包含被規則濾掉的項目，以免有東西被靜默丟棄。
