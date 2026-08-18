# -*- coding: utf-8 -*-
"""以網站現行翻譯更新 魔法少女扮演書.xlsx，輸出為新檔。

作法：直接對 xlsx 內部 XML 動刀，只改字串相關的部件
  - xl/sharedStrings.xml   所有literal儲存格文字
  - xl/worksheets/sheet*.xml  4 張 *_source 工作表中需要「同舊字串但不同新值」的儲存格索引，
                              以及公式儲存格的快取值 <v>
  - xl/comments*.xml       註解文字（術語級替換）
其餘部件（樣式、繪圖、VML、公式本身…）逐位元組原樣複製。
"""
import html
import os
import re
import sys
import zipfile

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ["TSV_QUOTED"] = "1"

import gen_tsv          # noqa: E402
import gen_raw          # noqa: E402
from manualmap import MANUAL, CELL_OVERRIDES, apply_terms   # noqa: E402

SRC = sys.argv[1]
DST = sys.argv[2]

SOURCE_SHEETS = {
    "pacto_sheet_source":   ("xl/worksheets/sheet7.xml",  gen_tsv.build_pacto),
    "amistad_sheet_source": ("xl/worksheets/sheet9.xml",  gen_tsv.build_amistad),
    "romance_sheet_source": ("xl/worksheets/sheet11.xml", gen_tsv.build_romance),
    "raw_sheet_source":     ("xl/worksheets/sheet13.xml", gen_raw.build),
}

COL_RE = re.compile(r"^([A-Z]+)(\d+)$")
# 先比對自成對的空儲存格，避免 `.*?</c>` 在大量空格上長距離回溯
CELL_RE = re.compile(r'<c r="([A-Z]+\d+)"([^>]*?)/>|<c r="([A-Z]+\d+)"([^>]*)>(.*?)</c>', re.S)


def col_idx(ref):
    letters = COL_RE.match(ref).group(1)
    n = 0
    for ch in letters:
        n = n * 26 + (ord(ch) - 64)
    return n - 1


def row_idx(ref):
    return int(COL_RE.match(ref).group(2))


def norm(s):
    return s.replace("\r\n", "\n").replace("\r", "\n")


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# ══════════════════════════════════════════════════════════
# 1. 讀取原始 xlsx
# ══════════════════════════════════════════════════════════
zin = zipfile.ZipFile(SRC)
ss_xml = zin.read("xl/sharedStrings.xml").decode("utf-8")

si_blocks = re.findall(r"<si>(.*?)</si>", ss_xml, re.S)
T_RE = re.compile(r"<t(?:\s[^>]*)?>(.*?)</t>", re.S)
si_text = [html.unescape("".join(T_RE.findall(b))) for b in si_blocks]
print("原始 sharedStrings:", len(si_blocks))


# ══════════════════════════════════════════════════════════
# 2. 組出 old -> new 對照（自動：4 張 source 工作表；手動：顯示用工作表）
#    同一舊字串對到多個新值者視為衝突，改用逐格索引修補
# ══════════════════════════════════════════════════════════
sheet_new = {}      # sheet_xml -> {(row1based, col0based): new_text}
gmap = {}
conflict_keys = set()

for name, (path, builder) in SOURCE_SHEETS.items():
    fn, header, rows, ncol = builder()
    new_grid = [header] + rows
    sheet_new[path] = {}
    for ri, r in enumerate(new_grid, start=1):
        for ci, v in enumerate(r):
            sheet_new[path][(ri, ci)] = v

# 用原檔的儲存格內容推導 old->new
sheet_old = {}
sheet_nums = {}
for name, (path, builder) in SOURCE_SHEETS.items():
    d = zin.read(path).decode("utf-8")
    cells = {}
    for m in CELL_RE.finditer(d):
        if m.group(1) is not None:
            continue                                   # 空儲存格
        ref, attrs, inner = m.group(3), m.group(4), m.group(5)
        if 't="s"' not in attrs:
            continue
        v = re.search(r"<v>(\d+)</v>", inner)
        if v:
            cells[(row_idx(ref), col_idx(ref))] = int(v.group(1))
    sheet_old[path] = cells
    # 數值儲存格（屬性數值）不走 sharedStrings，另外記錄
    nums = {}
    for m in CELL_RE.finditer(d):
        if m.group(1) is not None:
            continue
        ref, attrs, inner = m.group(3), m.group(4), m.group(5)
        if "t=" in attrs and 't="n"' not in attrs:
            continue
        v = re.search(r"<v>(-?[\d.]+)</v>", inner)
        if v:
            nums[(row_idx(ref), col_idx(ref))] = v.group(1)
    sheet_nums[path] = nums
    for key, idx in cells.items():
        old = si_text[idx].strip()
        new = sheet_new[path].get(key)
        if not old or new is None:
            continue
        k = norm(old)
        if k in gmap and gmap[k] != new:
            conflict_keys.add(k)
        else:
            gmap[k] = new

for k in conflict_keys:
    gmap.pop(k, None)
print("自動對照:", len(gmap), "| 衝突（改逐格處理）:", len(conflict_keys))

for k, v in MANUAL.items():
    gmap[norm(k).strip()] = v      # 查表時鍵一律 strip 過，這裡必須一致
print("加入手動對照後:", len(gmap))


# ══════════════════════════════════════════════════════════
# 3. 就地改寫 sharedStrings；需要額外字串時附加到尾端
# ══════════════════════════════════════════════════════════
new_si_text = list(si_text)
rewritten = 0
for i, t in enumerate(si_text):
    k = norm(t.strip())
    if k and k in gmap:
        new_si_text[i] = gmap[k]
        rewritten += 1
print("就地改寫的 <si>:", rewritten)

appended = {}          # text -> new index
def si_index_for(text):
    """回傳能代表 text 的 si 索引（必要時附加新項目）。"""
    for i, t in enumerate(new_si_text):
        if t == text:
            return i
    if text in appended:
        return appended[text]
    new_si_text.append(text)
    appended[text] = len(new_si_text) - 1
    return appended[text]


# ══════════════════════════════════════════════════════════
# 4. 逐格修補 4 張 source 工作表中對不上的儲存格
# ══════════════════════════════════════════════════════════
sheet_patch = {}       # path -> {(row, col): new_si_index}
num_patch = {}         # path -> {(row, col): new_number_string}
for name, (path, builder) in SOURCE_SHEETS.items():
    patch = {}
    for (ri, ci), idx in sheet_old[path].items():
        want = sheet_new[path].get((ri, ci))
        if want is None:
            continue
        if new_si_text[idx] != want:
            patch[(ri, ci)] = si_index_for(want)
    sheet_patch[path] = patch
    npatch = {}
    for (ri, ci), cur in sheet_nums[path].items():
        want = sheet_new[path].get((ri, ci))
        if want is None or not re.fullmatch(r"-?\d+", want):
            continue
        if float(cur) != float(want):
            npatch[(ri, ci)] = want
    num_patch[path] = npatch
    print(f"  {name}: 字串修補 {len(patch)} 格 / 數值修補 {len(npatch)} 格")

# 顯示用工作表的逐格覆寫（同名標籤在不同位置意思不同）
for path, cells in CELL_OVERRIDES.items():
    p = sheet_patch.setdefault(path, {})
    for ref, text in cells.items():
        p[(row_idx(ref), col_idx(ref))] = si_index_for(text)
    print(f"  {path.split('/')[-1]}: 逐格覆寫 {len(cells)} 格")


# ══════════════════════════════════════════════════════════
# 5. 產生新的 sharedStrings.xml
# ══════════════════════════════════════════════════════════
parts = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
         '<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
         'count="{cnt}" uniqueCount="{uniq}">']
body = []
for i, t in enumerate(new_si_text):
    if i < len(si_blocks) and t == si_text[i]:
        body.append("<si>" + si_blocks[i] + "</si>")          # 未改動 → 原樣保留（含 rich text）
    else:
        body.append('<si><t xml:space="preserve">' + esc(t) + "</t></si>")
orig_count = int(re.search(r'\bcount="(\d+)"', ss_xml).group(1))
new_ss = (parts[0].format(cnt=orig_count + len(appended), uniq=len(new_si_text))
          + "".join(body) + "</sst>")


# ══════════════════════════════════════════════════════════
# 6. 改寫工作表：套用逐格修補 + 更新公式快取值
# ══════════════════════════════════════════════════════════
def patch_sheet(path, data):
    patch = sheet_patch.get(path, {})
    npatch = num_patch.get(path, {})
    if not patch and not npatch and 't="str"' not in data:
        return data                                    # 這張表沒東西要改

    def repl_cell(m):
        if m.group(1) is not None:
            return m.group(0)                          # 空儲存格原樣保留
        ref, attrs, inner = m.group(3), m.group(4), m.group(5)
        key = (row_idx(ref), col_idx(ref))
        if key in npatch and ("t=" not in attrs or 't="n"' in attrs):
            inner = re.sub(r"<v>-?[\d.]+</v>", "<v>%s</v>" % npatch[key], inner)
            return '<c r="%s"%s>%s</c>' % (ref, attrs, inner)
        if 't="s"' in attrs and key in patch:
            inner = re.sub(r"<v>\d+</v>", "<v>%d</v>" % patch[key], inner)
            return '<c r="%s"%s>%s</c>' % (ref, attrs, inner)
        if 't="str"' in attrs:      # 公式的字串快取值
            def repl_v(vm):
                old = html.unescape(vm.group(1))
                k = norm(old.strip())
                return "<v>%s</v>" % esc(gmap[k]) if k and k in gmap else vm.group(0)
            inner = re.sub(r"<v>(.*?)</v>", repl_v, inner, flags=re.S)
            return '<c r="%s"%s>%s</c>' % (ref, attrs, inner)
        return m.group(0)

    return CELL_RE.sub(repl_cell, data)


# ══════════════════════════════════════════════════════════
# 7. 註解：術語級替換
# ══════════════════════════════════════════════════════════
def patch_comments(data):
    def repl(m):
        old = html.unescape(m.group(2))
        new = apply_terms(old)
        return m.group(1) + esc(new) + "</t>"
    # 注意：不可寫成 <t[^>]*>，那會連 <text> 開頭標籤一起吃掉而毀掉結構
    return re.sub(r"(<t(?:\s[^>]*)?>)(.*?)</t>", repl, data, flags=re.S)


# ══════════════════════════════════════════════════════════
# 8. 寫出新 xlsx：只換掉動過的部件，其餘原樣複製
# ══════════════════════════════════════════════════════════
os.makedirs(os.path.dirname(DST), exist_ok=True)
zout = zipfile.ZipFile(DST, "w", zipfile.ZIP_DEFLATED)
n_sheet, n_cmt = 0, 0
for item in zin.infolist():
    raw = zin.read(item.filename)
    if item.filename == "xl/sharedStrings.xml":
        raw = new_ss.encode("utf-8")
    elif item.filename.startswith("xl/worksheets/sheet") and item.filename.endswith(".xml"):
        txt = raw.decode("utf-8")
        out = patch_sheet(item.filename, txt)
        if out != txt:
            n_sheet += 1
        raw = out.encode("utf-8")
    elif re.match(r"xl/comments\d+\.xml$", item.filename):
        txt = raw.decode("utf-8")
        out = patch_comments(txt)
        if out != txt:
            n_cmt += 1
        raw = out.encode("utf-8")
    zi = zipfile.ZipInfo(item.filename, date_time=item.date_time)
    zi.compress_type = zipfile.ZIP_DEFLATED
    zi.external_attr = item.external_attr
    zout.writestr(zi, raw)
zout.close()

print(f"\n附加的新 <si>: {len(appended)} → 總計 {len(new_si_text)}")
print(f"改寫的工作表: {n_sheet} | 改寫的註解檔: {n_cmt}")
print("輸出:", DST, os.path.getsize(DST), "bytes")
