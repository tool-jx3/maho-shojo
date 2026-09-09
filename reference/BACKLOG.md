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
| 濾除：已收錄 | 95 |
| **待檢視** | **3444** |

掃描涵蓋 en、de、fr、es、it、sv、ru、pl、ja 九個語言版本的獵巫與巫術相關分類。未涵蓋的語言（ko、zh、ar、he、yo、ln 等）目前只能靠個別查找，這是本清單已知的偏誤。

分類樹裡混有大量虛構作品與流行文化條目，腳本的排除規則只能濾掉大部分，各主題清單中仍會殘留一些明顯不相干的項目。

## 優先候選（人工挑選）

以下是從掃描結果中挑出、明確屬於本資料庫範圍且尚未收錄的項目，可以直接從這裡開下一批。已收錄者會自動從表中消失。

| 條目 | 語言 | 純文字字數 | 為什麼值得收 |
| --- | --- | --- | --- |

本表的字數為實測的**純文字字數**（`prop=extracts&explaintext`），標「（估）」者為原始碼位元組的估算值，標「—」者不在掃描涵蓋範圍內。標「篇幅偏薄」者純文字不足 4000 字，可能撐不起逐段對譯的體例，收錄前要先確認實際可用內容。

## 依主題分列

| 主題 | 項數 | 清單 |
| --- | --- | --- |
| 獵巫受害者（個案） | 152 | [backlog/victims.md](backlog/victims.md) |
| 獵巫加害者 | 81 | [backlog/perpetrators.md](backlog/perpetrators.md) |
| 獵巫的反對者 | 24 | [backlog/opponents.md](backlog/opponents.md) |
| 被處決者 | 162 | [backlog/executed.md](backlog/executed.md) |
| 受指控者與指控者 | 85 | [backlog/accused.md](backlog/accused.md) |
| 審判事件 | 238 | [backlog/trials.md](backlog/trials.md) |
| 巫術研究者與研究史 | 31 | [backlog/scholarship.md](backlog/scholarship.md) |
| 傳說中的巫者形象 | 138 | [backlog/legendary-witches.md](backlog/legendary-witches.md) |
| 小妖精與使魔 | 39 | [backlog/imps-familiars.md](backlog/imps-familiars.md) |
| 詛咒與法術 | 211 | [backlog/curses.md](backlog/curses.md) |
| 童話中的女巫 | 98 | [backlog/fairy-tales.md](backlog/fairy-tales.md) |
| 傳說人物與怪異存在 | 82 | [backlog/legendary-beings.md](backlog/legendary-beings.md) |
| 獵巫的文化再現 | 146 | [backlog/reception.md](backlog/reception.md) |
| 各地區的巫術 | 271 | [backlog/regional.md](backlog/regional.md) |
| 其他 | 1686 | [backlog/misc.md](backlog/misc.md) |

完整未篩選的掃描結果保存在 [backlog/candidates-raw.tsv](backlog/candidates-raw.tsv)，包含被規則濾掉的項目，以免有東西被靜默丟棄。
