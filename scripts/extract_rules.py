# -*- coding: utf-8 -*-
"""從 docs/src/content/docs/rules/*.md 抽出角色卡建立頁所需的規則資料。"""
import io, json, re, os

R = 'docs/src/content/docs/rules/'
ATTR_KEYS = ['挑戰', '保護', '思慮', '情感', '奉獻']
PLAYBOOK_NAMES = ['勇者', '參謀', '衛士', '鬥士', '偶像', '聖母']

def read(fn):
    t = io.open(R + fn, encoding='utf-8').read()
    if t.startswith('---'):
        t = t.split('---', 2)[2]
    return t.split('\n')

def sections(lines, level):
    pref = '#' * level + ' '
    out, cur, buf = [], None, []
    for l in lines:
        if l.startswith(pref) and not l.startswith(pref + '#'):
            if cur is not None: out.append((cur, buf))
            cur, buf = l[len(pref):].strip(), []
        elif cur is not None:
            buf.append(l)
    if cur is not None: out.append((cur, buf))
    return out

def num(s):
    s = s.strip().replace('+', '')
    return int(s) if re.fullmatch(r'-?\d+', s) else 0

def bold_blocks(lines):
    """**名稱** 起始的區塊；「**選擇…：**」視為分隔標記。"""
    out, name, buf = [], None, []
    def flush():
        if name is not None:
            out.append({'name': name, 'text': '\n'.join(buf).strip()})
    for l in lines:
        s = l.strip()
        m = re.match(r'^\*\*(.+?)\*\*\s*$', s)
        if m:
            flush(); name, buf = m.group(1), []
        elif name is not None:
            buf.append(l)
    flush()
    return [split_options(power_grants(split_table(b))) for b in out if b['name']]

POWER_KEYS = ['護甲', '昇華', '摧毀', '懲罰', '堅韌']
POWER_RE = re.compile(r'(護甲|昇華|摧毀|懲罰|堅韌)\s*\+\s*(\d+)')

def power_grants(block):
    """判斷動作／選項／優勢是否提供能力量表以外的光之裝束力量加值。

    fixed       ── 變身後持續生效，直接併入加總
    choice      ── 從清單中擇一（例如正義騎士「光明之助」）
    conditional ── 需要花費資源或依情境成立，預設不併入
    """
    text = block.get('text') or ''
    found = POWER_RE.findall(text)
    if not found:
        return block
    items = [{'key': k, 'value': int(v)} for k, v in found]
    if '選擇一項光之裝束能力' in text:
        mode = 'choice'
    elif '花費' in text or '一項後果：' in text:
        mode = 'conditional'
    elif '變身' in text or '始終' in text:
        mode = 'fixed'
    else:
        mode = 'conditional'
    block['powerGrants'] = {'mode': mode, 'items': items}
    return block

def split_options(block):
    """把「從清單中選擇三項效果」這種內嵌選單抽成結構化的 options。

    目前只有聖母的「神聖力量」是這種形狀：說明後接一串 `- **名稱**：效果`。
    """
    text = block.get('text') or ''
    m = re.search(r'選擇(三|3)項效果', text)
    if not m:
        return block
    opts = [{'name': o.group(1).strip(), 'text': o.group(2).strip()}
            for o in re.finditer(r'^\s*-\s*\*\*(.+?)\*\*[：:]\s*(.*)$', text, re.M)]
    if len(opts) < 2:
        return block
    block['options'] = opts
    block['chooseCount'] = 3
    block['text'] = re.sub(r'^\s*-\s*\*\*.+?\*\*[：:].*$', '', text, flags=re.M)
    block['text'] = re.sub(r'\n{3,}', '\n\n', block['text']).strip()
    block['text'] = re.sub(r'\n*(同時獲得|也獲得)[：:]\s*$', '', block['text']).strip()
    return block

def split_table(block):
    """把區塊文字中的 Markdown 表格抽成 {headers, rows}，並從文字中移除。"""
    headers, rows, body = None, [], []
    for line in block['text'].split('\n'):
        ln = line.strip()
        if ln.startswith('|'):
            if set(ln.replace('|', '').strip()) <= set(':- '):
                continue  # 分隔列
            cells = [c.strip() for c in ln.strip('|').split('|')]
            if headers is None:
                headers = cells
            else:
                rows.append(cells)
            continue
        body.append(line)
    if headers and rows:
        block['table'] = {'headers': headers, 'rows': rows}
        block['text'] = '\n'.join(body).strip()
    return block


def parse_signature(body):
    """回傳 {mode, ...}。"""
    text = '\n'.join(body)
    opts = [power_grants({'name': m.group(1).strip(), 'text': m.group(2).strip()})
            for m in re.finditer(r'^\s*-\s*\*\*(.+?)\*\*[：:]\s*(.*)$', text, re.M)]
    if opts and '選擇三個選項' in text:
        # 「同時獲得：」之後的粗體區塊
        tail = text.split('同時獲得：', 1)[1] if '同時獲得：' in text else ''
        return {'mode': 'options', 'chooseCount': 3, 'options': opts,
                'granted': bold_blocks(tail.split('\n'))}
    blocks = bold_blocks(body)
    granted, choose, choose_label, cc = [], [], None, 0
    bucket = granted
    for b in blocks:
        m = re.match(r'^選擇(一項|其一|一個)(.*?)[：:]?$', b['name'])
        if m:
            choose_label = b['name'].rstrip('：:')
            cc = 1
            bucket = choose
            continue
        bucket.append(b)
    return {'mode': 'moves', 'granted': granted, 'chooseFrom': choose,
            'chooseCount': cc, 'chooseLabel': choose_label}

def parse_attributes(body):
    rows, header = [], None
    for l in body:
        s = l.strip()
        if not s.startswith('|') or s.startswith('|:'): continue
        cells = [c.strip() for c in s.strip('|').split('|')]
        if any(k in cells for k in ATTR_KEYS): header = cells; continue
        rows.append(cells)
    note = ' '.join(x.strip() for x in body
                    if x.strip() and not x.strip().startswith('|') and '選擇一組' not in x)
    if header and header[0] == '' and rows:  # 組合表
        sets = [{'label': r[0], 'values': dict(zip(ATTR_KEYS, [num(v) for v in r[1:6]]))}
                for r in rows if len(r) >= 6]
        return {'mode': 'sets', 'sets': sets, 'note': note.strip()}
    for r in rows:
        if len(r) == 5:
            return {'mode': 'fixed', 'values': dict(zip(ATTR_KEYS, [num(v) for v in r])),
                    'note': note.strip()}
    return {'mode': 'fixed', 'values': {k: 0 for k in ATTR_KEYS}, 'note': note.strip()}

# ---------------- 成長類型說明（advancement.md「成長類型」） ----------------
ADV = read('advancement.md')
ADV_DESC = {'b': {}, 'a': {}}
for _t, _body in sections(ADV, 2):
    if _t != '成長類型':
        continue
    for _kind, _sec in sections(_body, 3):
        _key = 'b' if _kind == '基礎成長' else 'a' if _kind == '進階成長' else None
        if not _key:
            continue
        for _name, _txt in sections(_sec, 4):
            _clean = [x.strip() for x in _txt if x.strip() and not x.strip().startswith(':::')]
            ADV_DESC[_key][_name] = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', '\n'.join(_clean))

# ---------------- 後果說明（light-vs-darkness.md「後果」） ----------------
LVD = read('light-vs-darkness.md')
CONS_INFO = {}
for _t, _body in sections(LVD, 2):
    if _t != '後果':
        continue
    for _l in _body:
        m = re.match(r'^-\s*\*\*(.+?)\*\*\s*[—-]\s*(\S+?)\s*=\s*(.+)$', _l.strip())
        if m:
            CONS_INFO[m.group(1)] = {'attribute': m.group(2), 'text': m.group(3).strip()}
    for _sub, _sec in sections(_body, 3):
        if _sub != '落敗後果':
            continue
        _p = [x.strip() for x in _sec if x.strip() and not x.strip().startswith(':::')]
        if _p:
            CONS_INFO['落敗'] = {'attribute': '', 'text': re.sub(r'\[(.+?)\]\(.+?\)', r'\1', _p[0])}

# ---------------- 原型扮演書 ----------------
ARCH = read('archetypes.md')
intro_secs = dict(sections(sections(ARCH, 2)[0][1], 3))

playbooks = []
for title, body in sections(ARCH, 2):
    if title not in PLAYBOOK_NAMES: continue
    subs = sections(body, 3)
    sub = dict(subs)
    sig_title, sig_body = subs[0]
    lux = []
    for l in sub.get('光之裝束力量', []):
        s = l.strip()
        if s.startswith('|') and not s.startswith('|:'):
            c = [x.strip() for x in s.strip('|').split('|')]
            if len(c) == 4 and c[0].isdigit():
                lux.append({'level': int(c[0]), 'basic': c[1], 'super': c[2], 'triumph': c[3]})
    cons = []
    for l in sub.get('後果', []):
        s = l.strip()
        if s.startswith('|') and not s.startswith('|:'):
            for c in s.strip('|').split('|'):
                c = c.replace('○', '').strip()
                if c: cons.append(c)
    sh, basic_adv, adv_adv, mode = sub.get('閃耀時刻！', []), [], [], None
    def adv_desc(text, kind):
        table = ADV_DESC.get(kind, {})
        if text in table:
            return table[text]
        if text.endswith('進階動作'):
            return table.get('（原型）進階動作', '')
        return ''

    for l in sh:
        if '基礎成長' in l: mode = 'b'; continue
        if '進階成長' in l: mode = 'a'; continue
        if l.strip().startswith('- '):
            item = re.sub(r'^\s*-\s*', '', l).strip()
            # 行首的 ○ 為官方扮演書上的欄位（可重複選取次數），沒有標記時視為 1 格
            m = re.match(r'^(○+)\s*', item)
            boxes = len(m.group(1)) if m else 1
            text = item[m.end():].strip() if m else item
            (basic_adv if mode == 'b' else adv_adv).append(
                {'text': text, 'boxes': boxes, 'desc': adv_desc(text, mode)})
    intro = [x.strip() for x in intro_secs.get(title, []) if x.strip() and not x.startswith('#')]
    playbooks.append({
        'name': title,
        'signatureName': sig_title,
        'signature': parse_signature(sig_body),
        'attributes': parse_attributes(sub.get('屬性', [])),
        'lux': lux,
        'consequences': cons,
        'basicAdvances': basic_adv,
        'advancedAdvances': adv_adv,
        'advanceMoves': bold_blocks(sub.get('進階動作', [])),
        'intro': intro[0] if intro else '',
    })

# ---------------- 友情／戀愛扮演書 ----------------
FR = read('friendship-romance.md')
fr = dict(sections(FR, 2))
def pb_list(lines):
    out = []
    for t, b in sections(lines, 3):
        tags = next((re.sub(r'^\*\*標籤：\*\*\s*', '', l.strip()) for l in b
                     if l.strip().startswith('**標籤：**')), '')
        bonds = next((re.sub(r'^\*\*羈絆：\*\*\s*', '', l.strip()) for l in b
                      if l.strip().startswith('**羈絆：**')), '')
        out.append({'name': t, 'tags': tags, 'bonds': bonds, 'moves': bold_blocks(b)})
    return out
friendship = pb_list(fr['友情扮演書'])
romance = pb_list(fr['戀愛扮演書'])

# ---------------- 盟約 ----------------
PA = read('pacts.md')
pacts = []
for t, b in sections(PA, 2):
    if not t.startswith('盟約：'): continue
    sub = dict(sections(b, 3))
    moves = bold_blocks(sub.get('盟約動作', []))
    coop = bold_blocks(sub.get('合作動作', []))
    dark = {}
    for st, sb in sections(sub.get('黑暗動作', []), 4):
        dark[st.replace('黑暗動作', '')] = bold_blocks(sb)
    rules = [re.sub(r'^\s*-\s*', '', l).strip() for l in sub.get('黑暗', []) if l.strip().startswith('- ')]
    adv = bold_blocks(sub.get('盟約優勢', []))
    intro = []
    if not adv:
        intro = [x.strip() for x in sub.get('盟約優勢', []) if x.strip()]
    else:
        # 粗體區塊之前的說明文字
        for x in sub.get('盟約優勢', []):
            if re.match(r'^\*\*.+\*\*\s*$', x.strip()): break
            if x.strip(): intro.append(x.strip())
    # 表格已由 split_table 統一抽出；標記用途：
    #   2 欄（等級／效果）＝額外形態；4 欄（能力等級／三形態）＝取代能力量表
    def tag_tables(blocks):
        for b in blocks:
            t = b.get('table')
            if not t:
                continue
            b['tableKind'] = ('extraForm' if len(t['headers']) == 2
                              else 'replaceLux' if len(t['headers']) == 4 else 'info')
            if b['tableKind'] == 'extraForm':
                b['formTable'] = [{'level': int(r[0]), 'effect': r[1]}
                                  for r in t['rows'] if r[0].isdigit()]
    tag_tables(adv)
    tag_tables(moves)
    tag_tables(coop)
    for k in dark:
        tag_tables(dark[k])

    # 黑暗等級 5 的後果：三種盟約各不相同，散落在該盟約的段落中
    lv5, grab = [], False
    for l in b:
        x = l.strip()
        if not x:
            continue
        if x.startswith('#'):
            grab = False
            continue
        if '黑暗等級 5' in x or '黑暗等級達到 5' in x:
            lv5.append(re.sub(r'\[(.+?)\]\(.+?\)', r'\1', x.lstrip('- ')))
            grab = x.endswith('：') or x.endswith(':')
            continue
        if grab and x.startswith('- '):
            lv5.append(re.sub(r'\[(.+?)\]\(.+?\)', r'\1', x[2:].strip()))
        else:
            grab = False

    pacts.append({'name': t.replace('盟約：', ''), 'moves': moves, 'coopMoves': coop,
                  'darkMoves': dark, 'darkRules': rules, 'advantages': adv,
                  'advantageIntro': intro, 'darkLevel5': lv5})

# ---------------- 基礎動作 ----------------
MV = read('moves.md')
mv = dict(sections(MV, 2))
basic_moves = []
for t, b in sections(mv['基礎動作'], 3):
    trig = next((l.strip().strip('*') for l in b if l.strip().startswith('**當')), '')
    m = re.search(r'擲骰\s*\+\s*([\u4e00-\u9fff]+)', '\n'.join(b))
    attr = m.group(1) if m else ''
    basic_moves.append({'name': t, 'trigger': trig, 'attribute': attr})

data = {'playbooks': playbooks, 'friendship': friendship, 'romance': romance,
        'pacts': pacts, 'basicMoves': basic_moves, 'attributeKeys': ATTR_KEYS,
        'consequenceInfo': CONS_INFO}
os.makedirs('docs/src/data', exist_ok=True)
io.open('docs/src/data/rules.json', 'w', encoding='utf-8').write(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n')

for p in playbooks:
    s = p['signature']
    print('%-3s attr=%-5s sig=%-7s granted=%d choose=%d/%s advMoves=%d lux=%d cons=%d' % (
        p['name'], p['attributes']['mode'],
        s['mode'], len(s.get('granted') or []), len(s.get('chooseFrom') or s.get('options') or []),
        s.get('chooseCount'), len(p['advanceMoves']), len(p['lux']), len(p['consequences'])))
    print('    成長欄位 基礎=%s 進階=%s' % (
        [(a['text'], a['boxes']) for a in p['basicAdvances']],
        [(a['text'], a['boxes']) for a in p['advancedAdvances']]))
print('friendship', [(f['name'], len(f['moves'])) for f in friendship])
print('romance', [(r['name'], len(r['moves'])) for r in romance])
print('pacts', [(p['name'], len(p['moves']), len(p['coopMoves']), {k: len(v) for k, v in p['darkMoves'].items()}, len(p['advantages'])) for p in pacts])
print('basicMoves', [(m['name'], m['attribute']) for m in basic_moves])
