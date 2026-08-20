# -*- coding: utf-8 -*-
"""直接以 docs/src/data/rules.json 產生四張扮演書 TSV。

內容不是硬編碼的翻譯快照，而是每次都從規則 Markdown → rules.json
重新取得，翻譯一改就同步。

用法：
    python scripts/extract_rules.py                 # 先更新 rules.json
    python scripts/sheet_sync/gen_from_rules.py OUT_DIR [--quote all|minimal|none]
    python scripts/sheet_sync/gen_from_rules.py OUT_DIR --diff BASE_DIR

引號模式：
    all      每一格都加引號（v3 匯出格式，export_v3.py）
    minimal  只有含換行／定位／引號的格加引號（RFC 4180）
    none     不加引號，格內換行輸出裸 CR（Google Sheets 原始匯出格式，預設）
"""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RULES = os.path.join(ROOT, 'docs', 'src', 'data', 'rules.json')

# ── 表格專用、規則文件裡沒有的字串（欄位標題與版面用語） ──────────────
SHEET_ONLY = {
    'raw_header': {0: '扮演書', 1: 'los Libretos', 2: '說明', 3: '說明', 4: '說明',
                   5: '屬性選項', 6: '說明', 8: '挑戰', 9: '保護', 10: '思慮',
                   11: '情感', 12: '奉獻', 26: '動作', 28: '動作'},
    'romance_header': ['戀愛扮演書', '', '效果', '', '動作', '', ''],
    'amistad_header': ['友情扮演書', '', '羈絆', '', '標籤', '', '問題', '', '動作', '', ''],
    'pacto_header': ['盟約', '盟約說明', '盟約', '吉祥物', '吉祥物說明', '名稱', '來歷', '外觀',
                     '盟約', '', '', '', '盟約', '額外功能', '', '黑暗', '', '盟約動作', '', ''],
    # 屬性選項欄：組合式扮演書在表格上另有一句導言
    'set_prefix': '選擇一組屬性，',
    'set_none': '無額外調整。',
    'growth_label': '透過成長獲得',
}

ROLL_RE = re.compile(r'^(\d+\+|\d+-\d+|\d+-)$')


# ── Markdown → 單一儲存格文字 ────────────────────────────────────────
def flat(md):
    return ' '.join(flat_parts(md)).strip()


def flat_parts(md):
    """把規則 Markdown 攤平成表格儲存格用的一行文字。

    段落以半形空格相接；清單項目前置「✽ 」；擲骰結果（10+／7-9／6-）
    不加項目符號，直接以空格接續說明。
    """
    if not md:
        return ''
    out, in_item = [], False
    for line in md.split('\n'):
        s = line.strip()
        if (not s or s.startswith(':::') or s.startswith('|') or s.startswith('#')
                or re.fullmatch(r'([-*_])\1{2,}', s)):
            in_item = False
            continue
        if in_item and line.startswith('  ') and not s.startswith('-'):
            out[-1] += re.sub(r'\[(.+?)\]\(.+?\)', r'\1', s)   # 清單項目的續行
            continue
        in_item = s.startswith('-')
        s = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', s)          # 連結只留文字
        m = re.match(r'^-\s*(.*)$', s)
        if m:
            item = m.group(1).strip()
            b = re.match(r'^\*\*(.+?)\*\*[：:　]?\s*(.*)$', item)
            if b and ROLL_RE.match(b.group(1).strip()):
                out.append('%s %s' % (b.group(1).strip(), b.group(2).strip()))
            elif b:
                out.append('✽ %s：%s' % (b.group(1).strip(), b.group(2).strip())
                           if b.group(2).strip() else '✽ %s' % b.group(1).strip())
            else:
                out.append('✽ ' + item)
            continue
        out.append(s.strip('*') if re.fullmatch(r'\*\*.+\*\*', s) else s)
    return out


def move_cell(block):
    """rules.json 的動作區塊 → 儲存格文字（含被 split_options 拆走的選項）。"""
    parts = flat_parts(block.get('text', ''))
    opts = ['✽ %s：%s' % (o['name'], flat(o['text']))
            for o in block.get('options') or []]
    at = block.get('optionsAt')
    if at is None:
        at = len(parts)
    parts = parts[:at] + opts + parts[at:]
    return ' '.join(x for x in parts if x).strip()


# ── 輸出層 ──────────────────────────────────────────────────────────
def cell(c, quote):
    if quote == 'all':
        c = c.replace('\r\n', '\n').replace('\r', '\n').replace('\n', '\r\n')
        return '"' + c.replace('"', '""') + '"'
    if quote == 'minimal':
        if '\n' in c or '\t' in c or '"' in c:
            return '"' + c.replace('"', '""').replace('\n', '\r\n') + '"'
        return c
    return c.replace('\n', '\r')


def write_tsv(out_dir, filename, header, rows, ncol, quote):
    os.makedirs(out_dir, exist_ok=True)
    lines = []
    for r in [header] + rows:
        assert len(r) == ncol, (filename, len(r), ncol)
        lines.append('\t'.join(cell(c, quote) for c in r))
    path = os.path.join(out_dir, filename)
    with io.open(path, 'w', encoding='utf-8', newline='') as f:
        f.write('\r\n'.join(lines))
    print('%-40s %2d 列 × %2d 欄' % (os.path.basename(path), len(rows) + 1, ncol))
    return path


def grid(nrow, ncol):
    return [['' for _ in range(ncol)] for _ in range(nrow)]


def put(rows, col_start, data):
    """把 (欄1, 欄2, …) 序列填進從 col_start 起的欄位，必要時自動長高。"""
    for i, tup in enumerate(data):
        while i >= len(rows):
            rows.append(['' for _ in range(len(rows[0]))])
        for j, v in enumerate(tup):
            rows[i][col_start + j] = v


def sign(v):
    return ('+%d' % v) if v >= 0 else str(v)


# ══════════════════════════════════════════════════════════════════
# 1. raw_sheet_source —— 原型扮演書（33 欄）
# ══════════════════════════════════════════════════════════════════
def build_raw(d):
    NCOL = 33
    pbs = d['playbooks']
    keys = d['attributeKeys']

    names = [(p['name'], p['nameEs']) for p in pbs]
    descs = [(p['name'], flat(p['introFull'])) for p in pbs]

    attr_opts = []
    for p in pbs:
        a = p['attributes']
        note = flat(a.get('note') or '')
        if a['mode'] == 'sets':
            note = SHEET_ONLY['set_prefix'] + (note.replace('接著，', '接著', 1)
                                               if note else SHEET_ONLY['set_none'])
        attr_opts.append((p['name'], note))

    attrs = []
    for p in pbs:
        a = p['attributes']
        vsets = ([s['values'] for s in a['sets']] if a['mode'] == 'sets'
                 else [a['values']])
        for v in vsets:
            attrs.append((p['name'],
                          '/'.join('%s%s' % (k, sign(v[k])) for k in keys))
                         + tuple(str(v[k]) for k in keys))

    # 能力量表：各扮演書三個等級；偶像另有「黑暗女神」替換用的量表
    heart = []
    for p in pbs:
        for lv in [x for x in p['lux'] if x['level'] <= 3]:
            heart.append((p['name'], lv['basic'], lv['super'], lv['triumph']))
    for pact in d['pacts']:
        for pb, blocks in (pact.get('darkMoves') or {}).items():
            for blk in blocks:
                if blk.get('tableKind') == 'replaceLux':
                    for r in blk['table']['rows']:
                        if r[0].isdigit() and int(r[0]) <= 3:
                            heart.append((pb, r[1], r[2], r[3]))

    sig_names = [(p['name'], p['signatureName']) for p in pbs]

    sig = []
    for p in pbs:
        blocks = [b for b in p['signatureBlocks'] if b['kind'] == 'granted']
        blocks += [b for b in p['signatureBlocks'] if b['kind'] == 'choice']
        # 只有偶像有「透過成長獲得」的招牌動作強化，來自成長清單
        growth_extra = [a for a in p['basicAdvances'] + p['advancedAdvances']
                        if a['effect'] == 'other' and a['desc']]
        if growth_extra:
            blocks = blocks + [{'label': SHEET_ONLY['growth_label'],
                                'items': [{'name': a['text'], 'text': a['desc']}
                                          for a in growth_extra]}]
        for b in blocks:
            sig.append((p['name'], b['label'] + '：', ''))
            for i, it in enumerate(b['items']):
                if i:
                    sig.append((p['name'], '', ''))       # 表格上以空列分隔選項
                sig.append((p['name'], it['name'], move_cell(it)))

    growth = []
    for p in pbs:
        ba, aa = p['basicAdvances'], p['advancedAdvances']
        for i in range(max(len(ba), len(aa))):
            growth.append((p['name'],
                           ba[i]['text'] if i < len(ba) else '',
                           aa[i]['text'] if i < len(aa) else ''))

    advanced = [(p['name'], m['name'], move_cell(m))
                for p in pbs for m in p['advanceMoves']]

    dark = []
    for pact in d['pacts']:
        for pb, blocks in (pact.get('darkMoves') or {}).items():
            for blk in blocks:
                dark.append((pb, pact['name'], blk['name'], move_cell(blk)))

    nrow = max(len(x) for x in (names, descs, attr_opts, attrs, heart,
                                sig_names, sig, growth, advanced, dark))
    rows = grid(nrow, NCOL)
    put(rows, 0, names)
    put(rows, 2, descs)
    put(rows, 4, attr_opts)
    put(rows, 6, attrs)
    put(rows, 13, heart)
    put(rows, 17, sig_names)
    put(rows, 19, sig)
    put(rows, 22, growth)
    put(rows, 26, advanced)
    put(rows, 29, dark)

    header = [''] * NCOL
    for i, v in SHEET_ONLY['raw_header'].items():
        header[i] = v
    return 'raw_sheet_source.tsv', header, rows, NCOL


# ══════════════════════════════════════════════════════════════════
# 2. romance_sheet_source —— 戀愛扮演書（7 欄）
# ══════════════════════════════════════════════════════════════════
def build_romance(d):
    NCOL = 7
    books = [(r['name'], flat(r['intro'])) for r in d['romance']]
    effects = [(r['name'], lv['effect']) for r in d['romance'] for lv in r['levels']]
    moves = [(r['name'], m['name'], move_cell(m))
             for r in d['romance'] for m in r['moves']]
    nrow = max(len(books), len(effects), len(moves))
    rows = grid(nrow, NCOL)
    put(rows, 0, books)
    put(rows, 2, effects)
    put(rows, 4, moves)
    return ('romance_sheet_source.tsv',
            list(SHEET_ONLY['romance_header']), rows, NCOL)


# ══════════════════════════════════════════════════════════════════
# 3. amistad_sheet_source —— 友情扮演書（11 欄）
# ══════════════════════════════════════════════════════════════════
def build_amistad(d):
    NCOL = 11
    fr = d['friendship']
    moves = [(f['name'], m['name'], move_cell(m)) for f in fr for m in f['moves']]
    nrow = max(len(fr), len(moves))
    rows = grid(nrow, NCOL)
    for i, f in enumerate(fr):
        rows[i][0] = rows[i][2] = rows[i][4] = rows[i][6] = f['name']
        rows[i][1] = flat(f['intro'])
        rows[i][3] = flat(f['bonds'])
        rows[i][5] = flat(f['tags'])
        rows[i][7] = flat(f['questions'])
    put(rows, 8, moves)
    return ('amistad_sheet_source.tsv',
            list(SHEET_ONLY['amistad_header']), rows, NCOL)


# ══════════════════════════════════════════════════════════════════
# 4. pacto_sheet_source —— 盟約扮演書（20 欄）
# ══════════════════════════════════════════════════════════════════
def build_pacto(d):
    NCOL = 20
    pacts = d['pacts']
    questions = [(p['name'], q) for p in pacts for q in p['questions']]
    extras = [(p['name'], p['extra']['title'], flat(p['extra']['text'])) for p in pacts]
    darkness = [(p['name'], flat(p['darknessText'])) for p in pacts]
    moves = [(p['name'], m['name'], move_cell(m))
             for p in pacts for m in (p['moves'] or p['advantages'])]
    nrow = max(len(pacts), len(questions), len(extras), len(darkness), len(moves))
    rows = grid(nrow, NCOL)
    for i, p in enumerate(pacts):
        m = p['mascot']
        f = {x['label']: flat(x['text']) for x in m['fields']}
        labels = [x['label'] for x in m['fields']]
        rows[i][0] = rows[i][2] = rows[i][8] = rows[i][10] = p['name']
        rows[i][1] = flat(p['intro'])
        rows[i][3] = m['name']
        rows[i][4] = flat(m['desc'])
        rows[i][5] = f[labels[0]]
        rows[i][6] = f[labels[1]]
        rows[i][7] = f[labels[2]]
        rows[i][11] = labels[1]          # 來歷／效忠對象
    put(rows, 8, questions)
    put(rows, 12, extras)
    put(rows, 15, darkness)
    put(rows, 17, moves)
    return ('pacto_sheet_source.tsv',
            list(SHEET_ONLY['pacto_header']), rows, NCOL)


BUILDERS = [build_raw, build_pacto, build_amistad, build_romance]


# ── 逐格比對 ────────────────────────────────────────────────────────
def read_tsv(path):
    txt = io.open(path, encoding='utf-8', newline='').read()
    rows, row, buf, q, i = [], [], [], False, 0
    while i < len(txt):
        c = txt[i]
        if q:
            if c == '"':
                if i + 1 < len(txt) and txt[i + 1] == '"':
                    buf.append('"'); i += 2; continue
                q = False; i += 1; continue
            buf.append(c); i += 1; continue
        if c == '"' and not buf:
            q = True; i += 1; continue
        if c == '\t':
            row.append(''.join(buf)); buf = []; i += 1; continue
        if c == '\r' and i + 1 < len(txt) and txt[i + 1] == '\n':
            row.append(''.join(buf)); rows.append(row); row, buf = [], []; i += 2; continue
        buf.append(c); i += 1
    row.append(''.join(buf))
    rows.append(row)
    return [[c.replace('\r\n', '\n').replace('\r', '\n') for c in r] for r in rows]


def col_cells(grid, c):
    return [(r[c] if c < len(r) else '') for r in grid]


def diff(out_dir, base_dir):
    """逐欄比對：先用 difflib 對齊列，再逐格分類差異。"""
    import difflib
    total = same = 0
    kinds = {}
    for fn in sorted(os.listdir(out_dir)):
        if not fn.endswith('.tsv'):
            continue
        bpath = os.path.join(base_dir, fn)
        if not os.path.exists(bpath):
            # 基準檔名可能帶有「魔法少女扮演書 - 」之類的前綴，改以工作表名配對
            bpath = next((os.path.join(base_dir, x) for x in sorted(os.listdir(base_dir))
                          if x.endswith(fn)), None)
        if not bpath or not os.path.exists(bpath):
            print('△ 基準沒有 %s' % fn)
            continue
        new, old = read_tsv(os.path.join(out_dir, fn)), read_tsv(bpath)
        ncol = max(len(new[0]), len(old[0]))
        print('\n══ %s   新 %d×%d ／ 基準 %d×%d'
              % (fn, len(new), len(new[0]), len(old), len(old[0])))
        for c in range(ncol):
            a, b = col_cells(new, c), col_cells(old, c)
            # 列數一致時逐列對位比較；列數不同才用 difflib 找出插入／刪除的列
            if len(a) == len(b):
                ops = [('replace', 0, len(b), 0, len(a))]
            else:
                ops = difflib.SequenceMatcher(None, b, a, autojunk=False).get_opcodes()
            for tag, i1, i2, j1, j2 in ops:
                if tag == 'equal':
                    n = sum(1 for x in b[i1:i2] if x)
                    total += n
                    same += n
                    continue
                if tag == 'replace' and (i2 - i1) == (j2 - j1):
                    for oi, ni in zip(range(i1, i2), range(j1, j2)):
                        if b[oi] and b[oi] == a[ni]:
                            total += 1
                            same += 1
                # 先依位置配對，多出來的才算新增／刪除
                pairs = list(zip(range(i1, i2), range(j1, j2)))
                k = len(pairs)
                pairs += [(i, None) for i in range(i1 + k, i2)]
                pairs += [(None, j) for j in range(j1 + k, j2)]
                for oi, ni in pairs:
                    o = b[oi] if oi is not None else ''
                    x = a[ni] if ni is not None else ''
                    if (not o and not x) or o == x:
                        continue
                    total += 1
                    if not o:
                        k = '規則新增'
                    elif not x:
                        k = '規則刪除'
                    elif re.sub(r'\s+', '', o) == re.sub(r'\s+', '', x):
                        k = '空白調整'
                    else:
                        k = '譯文更新'
                    kinds[k] = kinds.get(k, 0) + 1
                    print('  C%-2d R%-3s→%-3s [%s]\n    基準: %s\n    現在: %s'
                          % (c + 1, oi + 1 if oi is not None else '-',
                             ni + 1 if ni is not None else '-', k, o[:150], x[:150]))
    if total:
        print('\n非空儲存格 %d，相同 %d（%.1f%%），不同 %d'
              % (total, same, same * 100.0 / total, total - same))
        for k, v in sorted(kinds.items(), key=lambda x: -x[1]):
            print('  %s %d' % (k, v))


if __name__ == '__main__':
    argv = sys.argv[1:]
    out_dir = argv[0]
    quote = 'none'
    base = None
    if '--quote' in argv:
        quote = argv[argv.index('--quote') + 1]
    if '--diff' in argv:
        base = argv[argv.index('--diff') + 1]
        quote = 'all'
    data = json.load(io.open(RULES, encoding='utf-8'))
    for b in BUILDERS:
        write_tsv(out_dir, *b(data), quote=quote)
    if base:
        diff(out_dir, base)
