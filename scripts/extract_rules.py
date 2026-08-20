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
    return [attr_grants(split_options(power_grants(split_table(b)))) for b in out if b['name']]

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

ATTR_RE = re.compile(r'^(挑戰|保護|思慮|情感|奉獻)\s*\+\s*(\d+)（最高\s*(\d+)）')
ATTR_CHOICE_RE = re.compile(r'選擇一項屬性並增加\s*\+\s*(\d+)（最高\s*(\d+)）')

def attr_grants(block):
    """永久提升屬性的動作（契約傀儡「黑暗印記」「非人意識」）。"""
    text = (block.get('text') or '').strip()
    m = ATTR_CHOICE_RE.search(text)
    if m:
        block['attrGrant'] = {'mode': 'choice', 'value': int(m.group(1)), 'max': int(m.group(2))}
        return block
    m = ATTR_RE.match(text)
    if m:
        block['attrGrant'] = {'mode': 'fixed', 'key': m.group(1),
                              'value': int(m.group(2)), 'max': int(m.group(3))}
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
    # 記錄選項原本插在第幾個段落之後，重建表格時才能放回原位
    lines = text.split('\n')
    first = next(i for i, l in enumerate(lines)
                 if re.match(r'^\s*-\s*\*\*.+?\*\*[：:]', l))
    block['optionsAt'] = sum(1 for l in lines[:first] if l.strip())
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

def parse_signature_blocks(body):
    """把招牌動作段落切成有序的「標題：＋項目」區塊，供扮演書表格重建欄位。"""
    # 只認「選擇…：」「…獲得：」這兩種段落標題，避免誤抓動作內文的冒號句
    label_re = re.compile(r'^\**([^。，、:：]{0,4}?(?:選擇|獲得)[^。，、:：]{0,8})[：:]\**$')
    blocks, cur = [], None
    for l in body:
        s = l.strip()
        m = label_re.match(s) if s else None
        if m:
            cur = {'label': m.group(1),
                   'kind': 'choice' if m.group(1).startswith('選擇') else 'granted',
                   'lines': []}
            blocks.append(cur)
        elif cur is not None:
            cur['lines'].append(l)
    out = []
    for b in blocks:
        # 保留 bold_blocks 已解析出的 options／table（例如聖母「神聖力量」的六個效果）
        items = bold_blocks(b['lines'])
        if not items:
            items = [{'name': m.group(1).strip(), 'text': m.group(2).strip()}
                     for m in re.finditer(r'^\s*-\s*\*\*(.+?)\*\*[：:]\s*(.*)$',
                                          '\n'.join(b['lines']), re.M)]
        if items:
            out.append({'label': b['label'], 'kind': b['kind'], 'items': items})
    return out

def parse_adjust(note):
    """把扮演書的屬性分配說明轉成可驗證的規則。

    無法辨識時回傳 None，頁面會退回不限制的自由調整。
    """
    n = (note or '').strip()
    if not n:
        return None
    m = re.search(r'將\s*\+3\s*加到一項屬性上、將\s*\+2\s*和\s*\+1\s*分別加到兩項屬性上，'
                  r'或將\s*\+1\s*加到三項屬性上（任一屬性上限為\s*\+(\d)）', n)
    if m:
        return {'mode': 'spread', 'options': [[3], [2, 1], [1, 1, 1]], 'cap': int(m.group(1))}
    if re.search(r'將一個\s*0\s*改為\s*\+1，另一個\s*0\s*改為\s*-1', n):
        return {'mode': 'zeroSwap'}
    m = re.search(r'將\s*1\s*點加到([\u4e00-\u9fff]+)、([\u4e00-\u9fff]+)或([\u4e00-\u9fff]+)上', n)
    if m:
        return {'mode': 'points', 'total': 1, 'only': [m.group(1), m.group(2), m.group(3)]}
    if re.search(r'將\s*\+1\s*加到一項屬性上', n):
        return {'mode': 'points', 'total': 1}
    return None

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
        return {'mode': 'sets', 'sets': sets, 'note': note.strip(),
                'adjust': parse_adjust(note)}
    for r in rows:
        if len(r) == 5:
            return {'mode': 'fixed', 'values': dict(zip(ATTR_KEYS, [num(v) for v in r])),
                    'note': note.strip(), 'adjust': parse_adjust(note)}
    return {'mode': 'fixed', 'values': {k: 0 for k in ATTR_KEYS}, 'note': note.strip(),
            'adjust': parse_adjust(note)}

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

# ---------------- 心之力與終曲（light-vs-darkness.md） ----------------
HEART = {}
for _t, _body in sections(LVD, 2):
    if _t != '心之力與終曲':
        continue
    for _sub, _sec in sections(_body, 3):
        m = re.match(r'^心之力（([ADP])）', _sub)
        key = m.group(1) if m else ('finalem' if _sub == '終曲' else None)
        if not key:
            continue
        effects, para = [], []
        for _l in _sec:
            x = _l.strip()
            if x.startswith(':::'):
                break
            if x.startswith('- '):
                effects.append(re.sub(r'\[(.+?)\]\(.+?\)', r'\1', x[2:].strip()))
            elif x and not x.startswith('選擇一個效果'):
                para.append(re.sub(r'\[(.+?)\]\(.+?\)', r'\1', x))
        HEART[key] = {'title': _sub, 'effects': effects, 'note': '\n'.join(para).strip()}

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
    def adv_effect(text, desc):
        """把成長項目歸類成頁面要套用的效果。"""
        if '提升一項屬性' in text:
            return 'attr3' if '上限 3' in text else 'attr2'
        if text.endswith('進階動作'):
            return 'advMove'
        if '友情扮演書動作' in text:
            return 'frMove'
        if '超級形態' in text:
            return 'super'
        if '凱旋形態' in text:
            return 'triumph'
        if '在角色建立時未選取的' in desc:
            return 'sigChoice'   # 參謀天才／衛士光之盾／鬥士戰士之道：補選當初沒選的那一項
        if '額外選擇尚未選取的' in desc:
            return 'sigExtra3'   # 勇者受眷顧者／聖母神聖力量：多三個選項
        return 'other'

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
            desc = adv_desc(text, mode)
            (basic_adv if mode == 'b' else adv_adv).append(
                {'text': text, 'boxes': boxes, 'desc': desc, 'effect': adv_effect(text, desc)})
    # 概要段落只取「XX的遊戲定位」（#### 小節）之前的部分
    intro_lines = intro_secs.get(title, [])
    _cut = next((i for i, l in enumerate(intro_lines) if l.startswith('####')), len(intro_lines))
    intro = [x.strip() for x in intro_lines[:_cut] if x.strip() and not x.startswith('#')]
    playbooks.append({
        'name': title,
        'signatureName': sig_title,
        'signature': parse_signature(sig_body),
        'signatureBlocks': parse_signature_blocks(sig_body),
        'attributes': parse_attributes(sub.get('屬性', [])),
        'lux': lux,
        'consequences': cons,
        'basicAdvances': basic_adv,
        'advancedAdvances': adv_adv,
        'advanceMoves': bold_blocks(sub.get('進階動作', [])),
        'intro': intro[0] if intro else '',
        'introFull': '\n\n'.join(intro),
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
        questions = next((re.sub(r'^\*\*問題：\*\*\s*', '', l.strip()) for l in b
                          if l.strip().startswith('**問題：**')), '')
        # 標題後、第一個粗體區塊之前的說明文字
        intro = []
        for l in b:
            x = l.strip()
            if x.startswith('**') or x.startswith('|') or x.startswith(':::'):
                break
            if x:
                intro.append(x)
        # 戀愛量表（狀態／等級／效果）
        levels = []
        for l in b:
            x = l.strip()
            if not x.startswith('|') or set(x.replace('|', '').strip()) <= set(':- '):
                continue
            c = [y.strip() for y in x.strip('|').split('|')]
            if len(c) == 3 and c[1] != '等級':
                levels.append({'state': c[0], 'level': c[1], 'effect': c[2]})
        out.append({'name': t, 'tags': tags, 'bonds': bonds, 'questions': questions,
                    'intro': ' '.join(intro), 'levels': levels, 'moves': bold_blocks(b)})
    return out
friendship = pb_list(fr['友情扮演書'])
romance = pb_list(fr['戀愛扮演書'])

# ---------------- 世界觀問卷（setting.md） ----------------
SET = read('setting.md')
WORLD_Q = {}
for _t, _b in sections(SET, 2):
    for _st, _sb in sections(_b, 3):
        if not _st.endswith('問卷'):
            continue
        WORLD_Q[_st[:-2]] = [x.strip().strip('*') for x in _sb
                             if re.fullmatch(r'\*\*.+？\*\*', x.strip())]

# ---------------- 扮演書西班牙文原名（es/archetypes.md） ----------------
_ES = io.open(R.replace('/rules/', '/es/rules/') + 'archetypes.md', encoding='utf-8').read()
_es_names = []
for _l in _ES.split('\n'):
    _l = _l.strip()
    if re.fullmatch(r'La [A-ZÁÉÍÓÚÑ][a-záéíóúñ]+', _l) and _l not in _es_names:
        _es_names.append(_l)
    if len(_es_names) == len(PLAYBOOK_NAMES):
        break
assert len(_es_names) == len(PLAYBOOK_NAMES), _es_names
for _p, _es in zip(playbooks, _es_names):
    _p['nameEs'] = _es

# ---------------- 盟約 ----------------
MASCOT_TITLES = ('同伴', '使者', '監護者')
EXTRA_TITLES = ('羈絆與友情', '合作')
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

    # 盟約說明：標題之後、第一個 ### 之前的段落
    p_intro = []
    for l in b:
        if l.startswith('###'):
            break
        x = l.strip()
        if x and not x.startswith('欲知更多'):
            p_intro.append(x)

    # 吉祥物（同伴／使者／監護者）：說明與扮演書欄位
    mascot = None
    for st, sb in sections(b, 3):
        if st not in MASCOT_TITLES:
            continue
        m_desc = [x.strip() for x in sb[:next((i for i, l in enumerate(sb)
                                               if l.startswith('####')), len(sb))]
                  if x.strip() and not x.strip().startswith('以下將更詳細地介紹')]
        fields = [{'label': ft, 'text': '\n'.join(fb).strip()}
                  for ft, fb in sections(sb, 4)
                  if ft not in ('閃耀點數',) + EXTRA_TITLES]
        mascot = {'name': st, 'desc': '\n\n'.join(m_desc), 'fields': fields}
        break

    # 額外功能：光明子女「羈絆與友情」／正義騎士「合作」／契約傀儡無
    extra = {'title': '無額外功能', 'text': ''}
    for st, sb in sections(b, 3):
        if st in EXTRA_TITLES:
            extra = {'title': st, 'text': '\n'.join(sb).strip()}
        for st4, sb4 in sections(sb, 4):
            if st4 in EXTRA_TITLES:
                extra = {'title': st4, 'text': '\n'.join(sb4).strip()}
    pacts.append({'name': t.replace('盟約：', ''), 'intro': '\n\n'.join(p_intro),
                  'mascot': mascot, 'extra': extra,
                  'darknessText': '\n'.join(sub.get('黑暗', [])).strip(),
                  'questions': WORLD_Q.get(t.replace('盟約：', ''), []),
                  'moves': moves, 'coopMoves': coop,
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
        'consequenceInfo': CONS_INFO, 'heartPowers': HEART}
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
