# -*- coding: utf-8 -*-
"""從更新後的 xlsx 匯出 4 張 *_sheet_source 為 TSV。

格式：
  - 每一格（含空格）一律用 "" 包起來
  - 格內換行統一為 CRLF，格內的 " 轉義為 ""
  - 列分隔 CRLF，檔尾不加換行
"""
import os
import sys

import openpyxl

sys.stdout.reconfigure(encoding="utf-8")

SRC, OUT = sys.argv[1], sys.argv[2]
SHEETS = ["raw_sheet_source", "pacto_sheet_source",
          "amistad_sheet_source", "romance_sheet_source"]


def cell_text(v):
    if v is None:
        return ""
    if isinstance(v, bool):
        return "TRUE" if v else "FALSE"
    if isinstance(v, float) and v == int(v):
        return str(int(v))
    return str(v)


def quote(s):
    # 格內換行一律 CRLF；引號轉義；整格包 ""
    s = s.replace("\r\n", "\n").replace("\r", "\n").replace("\n", "\r\n")
    return '"' + s.replace('"', '""') + '"'


wb = openpyxl.load_workbook(SRC)
os.makedirs(OUT, exist_ok=True)

for name in SHEETS:
    ws = wb[name]
    grid = [[cell_text(v) for v in row] for row in ws.iter_rows(values_only=True)]
    # 裁掉完全沒有資料的尾端列／欄
    while grid and not any(c.strip() for c in grid[-1]):
        grid.pop()
    ncol = 0
    for r in grid:
        for i, c in enumerate(r):
            if c.strip():
                ncol = max(ncol, i + 1)
    grid = [r[:ncol] + [""] * (ncol - len(r[:ncol])) for r in grid]

    lines = ["\t".join(quote(c) for c in r) for r in grid]
    path = os.path.join(OUT, "魔法少女扮演書 - %s.tsv" % name)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write("\r\n".join(lines))
    multiline = sum(1 for r in grid for c in r if "\n" in c or "\r" in c)
    print("%-24s %2d 列 × %2d 欄  含換行的格 %d  →  %s"
          % (name, len(grid), ncol, multiline, os.path.basename(path)))
