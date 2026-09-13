#!/usr/bin/env python
"""檢查 reference/works/entries/ 的引文是否逐字屬實且未偽裝連續（裁決 V）。

本庫的體例是「原文逐字引用（blockquote）＋下方繁體中文譯文」。讀者看到一個
引文區塊，預設它是來源中一段**連續**的文字；區塊內若靜悄悄跳過了原文，呈現
出來的就是一段來源裡並不存在的連續段落——這是本子庫唯一不能犯的錯。

裁決 V 因此規定：

1. 區塊內每一處省略，都要另起一行寫 `> （中略）`。
2. 該行是本庫的編輯記號、不是來源文字，逐字比對時**跳過**它。
3. 連續性改以**分段**驗證：以 `（中略）` 切開後的每一段，各自必須在**同一個**
   快取檔中連續出現，且各段在該檔中的**先後順序與區塊中的順序一致**。
4. 引文從來源的中途開始或中途結束，不需要記號——那是節錄，不是區塊內的缺口。

第 3 點比「整塊逐字連續」更嚴，不是更鬆：它同時查段內連續與段間順序，
`（中略）` 只免除段與段之間的「必須相鄰」，不免除「必須同一份來源、必須順序
正確」。拿 A 頁的一段接 B 頁的一段，或把來源後面的話擺到前面，照樣會被擋下。

搜尋範圍是 `.cache/` 底下 `wiki/`、`sources/`、`wiki-raw/`、`raw/` 的純文字檔。
比對前把所有空白（含全形空白）去除，因為純文字擷取會把行內空白正規化。

`.cache/` 不在版本控制內（見 `.gitignore`）。它不存在或沒有可讀檔案時，本腳本
印出提醒並以非零碼結束，**不會**安靜地全部放行——一支沒真的檢查卻回報成功的
檢查器，跟它要防的缺陷是同一個形狀。

用法：
    .venv/Scripts/python.exe scripts/check_works_quotes.py [路徑...]
未給路徑時預設檢查 reference/works/entries/ 底下所有 .md。
"""

from __future__ import annotations

import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DEFAULT_DIR = os.path.join(ROOT, "reference", "works", "entries")
CACHE_DIRS = ("wiki", "sources", "wiki-raw", "raw")

ELLIPSIS_MARKER = "（中略）"
WHITESPACE_RE = re.compile(r"[\s　]+")

# 單一區塊在單一快取檔中可保留的候選鏈數上限。段落通常夠長、命中唯一，這個上限
# 只在短行（例如發言人標籤「小原正和さん」）重複出現時才會用到，用來擋住組合爆炸。
MAX_CHAINS = 400


def norm(s):
    return WHITESPACE_RE.sub("", s)


def load_corpus():
    texts = {}
    for d in CACHE_DIRS:
        dp = os.path.join(ROOT, ".cache", d)
        if not os.path.isdir(dp):
            continue
        for fn in sorted(os.listdir(dp)):
            if not fn.endswith(".txt"):
                continue
            p = os.path.join(dp, fn)
            try:
                raw = io.open(p, encoding="utf-8", errors="replace").read()
            except OSError:
                continue
            texts[".cache/%s/%s" % (d, fn)] = norm(raw)
    return texts


def iter_files(paths):
    for p in paths:
        if os.path.isdir(p):
            for dirpath, _dirnames, filenames in os.walk(p):
                for fn in sorted(filenames):
                    if fn.endswith(".md"):
                        yield os.path.join(dirpath, fn)
        elif p.endswith(".md"):
            yield p


def blocks_of(lines):
    """回傳 [(起始行號, 結束行號, [(行號, 內容或 None)])]；內容為 None 代表 （中略） 記號行。

    空的 `>` 行（區塊內的段落分隔）直接丟掉，它不是引文內容。
    """
    out = []
    i = 0
    while i < len(lines):
        if lines[i].strip().startswith(">"):
            j = i
            items = []
            while j < len(lines) and lines[j].strip().startswith(">"):
                body = lines[j].strip().lstrip(">").strip()
                if body == ELLIPSIS_MARKER:
                    items.append((j + 1, None))
                elif body:
                    items.append((j + 1, norm(body)))
                j += 1
            if items:
                out.append((i + 1, j, items))
            i = j
        else:
            i += 1
    return out


def segments_of(items):
    """以 （中略） 切段，回傳 [[(行號, 內容), ...], ...]（不含記號行、不含空段）。"""
    segs, cur = [], []
    for lineno, body in items:
        if body is None:
            if cur:
                segs.append(cur)
            cur = []
        else:
            cur.append((lineno, body))
    if cur:
        segs.append(cur)
    return segs


def all_positions(hay, needle):
    out, p = [], hay.find(needle)
    while p >= 0:
        out.append(p)
        p = hay.find(needle, p + 1)
    return out


def chain_in(text, pieces):
    """在 text 中找 pieces 的遞增不重疊出現鏈，回傳缺口總和最小者的 [(起, 迄)]；找不到回傳 None。

    逐段展開所有出現位置再取最小缺口，而不是每次都用 find(..., pos) 取最近的一個：
    短字串（發言人標籤之類）會在同一份來源裡重複出現，貪婪地取第一個命中，會把
    本來連續的區塊誤判成有巨大缺口。
    """
    occ = [all_positions(text, q) for q in pieces]
    if any(not o for o in occ):
        return None
    chains = [[(p, p + len(pieces[0]))] for p in occ[0]]
    costs = [0] * len(chains)
    for i in range(1, len(pieces)):
        ncosts, nchains = [], []
        for p in occ[i]:
            best = None
            for k, ch in enumerate(chains):
                end = ch[-1][1]
                if p >= end:
                    c = costs[k] + (p - end)
                    if best is None or c < best[0]:
                        best = (c, k)
            if best is None:
                continue
            ncosts.append(best[0])
            nchains.append(chains[best[1]] + [(p, p + len(pieces[i]))])
        if not nchains:
            return None
        if len(nchains) > MAX_CHAINS:
            order = sorted(range(len(nchains)), key=lambda x: ncosts[x])[:MAX_CHAINS]
            ncosts = [ncosts[x] for x in order]
            nchains = [nchains[x] for x in order]
        costs, chains = ncosts, nchains
    k = min(range(len(costs)), key=lambda x: costs[x])
    return costs[k], chains[k]


def rel_to_root(path):
    """相對於 repo 根的路徑；跨磁碟機（Windows）無法相對化時退回原路徑，不讓顯示用的
    路徑計算把整支檢查器打斷。"""
    try:
        return os.path.relpath(path, ROOT).replace(os.sep, "/")
    except ValueError:
        return path.replace(os.sep, "/")


def check_file(path, corpus):
    """回傳 (問題清單, 引文行數, 區塊數, 分段數)。"""
    rel = rel_to_root(path)
    lines = io.open(path, encoding="utf-8").read().split("\n")
    problems = []
    n_lines = n_blocks = n_segs = 0

    for start, end, items in blocks_of(lines):
        n_blocks += 1
        segs = segments_of(items)
        n_segs += len(segs)

        # ── 1. 逐行逐字比對（記號行已在 blocks_of 標成 None，不參與）
        for lineno, body in items:
            if body is None:
                continue
            n_lines += 1
            if not any(body in v for v in corpus.values()):
                problems.append(
                    "%s:%d 引文行在 .cache/ 底下的任何一個抓取檔中都找不到逐字出處" % (rel, lineno))

        # ── 2. 段內連續 ＋ 段間同檔同序
        seg_texts = ["".join(b for _, b in seg) for seg in segs]
        hits = []
        for key, text in corpus.items():
            r = chain_in(text, seg_texts)
            if r is not None:
                hits.append((r[0], key, r[1]))
        if not hits:
            # 分辨是「段內就不連續」還是「各段分散在不同檔」，訊息才有用
            bad = []
            for idx, st in enumerate(seg_texts):
                if not any(st in v for v in corpus.values()):
                    bad.append(idx + 1)
            if bad:
                problems.append(
                    "%s:%d-%d 第 %s 段在任何單一快取檔中都不連續（段內有未標記的略過，"
                    "應加 `> （中略）`）" % (rel, start, end, "、".join(str(b) for b in bad)))
            else:
                problems.append(
                    "%s:%d-%d 各段各自連續，但找不到一個快取檔能依原順序涵蓋全部 %d 段"
                    "（拼接了不同來源，或段落次序與來源相反）" % (rel, start, end, len(segs)))
            continue
        best = min(hits)
        if len(segs) == 1 and best[0] != 0:
            # 單段區塊的鏈只有一個元素，缺口必為 0；這裡防呆，不應發生
            problems.append("%s:%d-%d 單段區塊出現非零缺口（腳本邏輯異常）" % (rel, start, end))
    return problems, n_lines, n_blocks, n_segs


def main(argv):
    paths = argv[1:] or [DEFAULT_DIR]
    corpus = load_corpus()
    if not corpus:
        sys.stdout.write(
            "提醒：`.cache/` 底下找不到任何可讀的 .txt，本次未執行引文比對。\n"
            "      `.cache/` 不在版本控制內，需先以 scripts/fetch_wiki.py 等重新取得來源。\n")
        return 2

    files = sorted(iter_files(paths))
    total_lines = total_blocks = total_segs = bad_files = 0
    for path in files:
        problems, nl, nb, ns = check_file(path, corpus)
        total_lines += nl
        total_blocks += nb
        total_segs += ns
        rel = rel_to_root(path)
        if problems:
            bad_files += 1
            sys.stdout.write("FAIL %s\n" % rel)
            for p in problems:
                sys.stdout.write("     - %s\n" % p)
        else:
            sys.stdout.write("ok   %s\n" % rel)

    sys.stdout.write(
        "\n共檢查 %d 個檔案、%d 個引文區塊、%d 個分段、%d 行引文；%d 個檔案有問題。\n"
        % (len(files), total_blocks, total_segs, total_lines, bad_files))
    sys.stdout.write("快取語料：%d 個檔案。\n" % len(corpus))
    return 0 if bad_files == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
