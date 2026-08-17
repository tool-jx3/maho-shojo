# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "resvg-py>=0.1",
# ]
# ///
"""Mahō Shōjo 透明底 logo 產生器。

用法（於專案根目錄）：
    uv run scripts/make_logo.py

產出：
    docs/public/logo.svg           向量原檔（透明底）
    docs/public/logo-1024.png      透明 PNG（寬 1024）
    docs/public/logo-512.png       透明 PNG（寬 512）

構圖：粉→紫漸層愛心＋金色新月捲弧冠（含光澤寶石與頂星）＋Mahō Shōjo 手寫字，
兩側六顆四芒星對應六本扮演書的雙色漸層（左：勇者/衛士/偶像，右：參謀/鬥士/聖母）。
想調整外觀改下方「設定區」即可；PNG 由 resvg 以系統字型渲染。
"""

import math
from pathlib import Path

# ============================================
# 設定區：配色、寶石、星星、文字
# ============================================

ROOT = Path(__file__).resolve().parent.parent
OUT_SVG = ROOT / "docs" / "public" / "logo.svg"
PNG_WIDTHS = [1024, 512]  # 產出的 PNG 寬度（檔名 logo-{寬}.png）

HEART_A = "#f68cc4"       # 愛心漸層上端（粉）
HEART_B = "#7c5bd6"       # 愛心漸層下端（紫）
HEART_STROKE = "#e5b04c"  # 愛心金邊

CROWN_A = "#f4d582"       # 皇冠金漸層上端
CROWN_B = "#cf9b2e"       # 皇冠金漸層下端
CROWN_STROKE = "#a87b1c"  # 皇冠描邊
GEM = "#5d3fc0"           # 冠座寶石（深紫水晶；光澤亮暗部自動推算）

TEXT_FILL = "#ffffff"
TEXT_STROKE = "#8547b8"
FONT_STACK = "'Brush Script MT','Segoe Script',cursive"

# 六本扮演書配色（勇者、參謀、衛士、鬥士、偶像、聖母）——雙色漸層兩端
ARCH_COLORS = [
    ("#4790aa", "#26607b"), ("#7c34a6", "#45175e"), ("#8f3da0", "#c22f57"),
    ("#d63a4a", "#2b9e8f"), ("#d066c0", "#8f4b9e"), ("#97b0cd", "#52719c"),
]
# 星星位置與大小（左列 勇者/衛士/偶像、右列 參謀/鬥士/聖母，同序章頁）
STAR_POS = [(-285, -95, 26), (-345, 45, 20), (-265, 185, 23),
            (285, -95, 26), (345, 45, 20), (265, 185, 23)]
STAR_ORDER = [0, 2, 4, 1, 3, 5]

# ============================================
# 幾何
# ============================================

HEART = ("M 0,90 C 0,35 -48,-5 -95,-5 C -150,-5 -178,42 -178,82 "
         "C -178,155 -85,222 0,285 C 85,222 178,155 178,82 "
         "C 178,42 150,-5 95,-5 C 48,-5 0,35 0,90 Z")


def star_pts(cx, cy, r_out, r_in, rot=-90):
    pts = []
    for i in range(8):
        ang = math.radians(rot + i * 45)
        rr = r_out if i % 2 == 0 else r_in
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    return pts


def star(cx, cy, r, fill, op=1.0, stroke=None, sw=0):
    pts = " ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in star_pts(cx, cy, r, r * 0.36))
    s = f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"' if stroke else ""
    return f'<polygon points="{pts}" fill="{fill}" opacity="{op}"{s}/>'


def _hex(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _mix(a, b, t):
    return "#%02x%02x%02x" % tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def crown():
    """弧線冠：中央杖＋新月＋頂星、兩對外彎捲弧、帶座三顆光澤寶石。"""
    g = "url(#cg)"
    curls = [
        ("M 2,-128 C 20,-148 42,-150 54,-136 C 64,-124 64,-100 54,-80", 11),
        ("M -2,-128 C -20,-148 -42,-150 -54,-136 C -64,-124 -64,-100 -54,-80", 11),
        ("M 1,-116 C 12,-126 24,-122 27,-108 C 29,-94 25,-82 19,-74", 9),
        ("M -1,-116 C -12,-126 -24,-122 -27,-108 C -29,-94 -25,-82 -19,-74", 9),
        ("M 0,-74 L 0,-150", 12),
    ]
    out = ['<g transform="translate(0,20)">']
    for d_, w in curls:
        out.append(f'<path d="{d_}" fill="none" stroke="{CROWN_STROKE}" stroke-width="{w + 5}" stroke-linecap="round"/>')
    for d_, w in curls:
        out.append(f'<path d="{d_}" fill="none" stroke="{g}" stroke-width="{w}" stroke-linecap="round"/>')
    # 新月（開口朝上）
    out.append(
        f'<path d="M -13,-176 A 16 16 0 1 0 13,-176 A 14 14 0 0 1 -13,-176 Z" '
        f'fill="{g}" stroke="{CROWN_STROKE}" stroke-width="3.5" stroke-linejoin="round"/>'
    )
    # 新月上方的金色星星
    out.append(star(0, -206, 14, g, stroke=CROWN_STROKE, sw=3))
    # 帶座＋三顆光澤寶石（放射漸層＋白色高光）
    gc = _hex(GEM)
    g_light = _mix(gc, (255, 255, 255), 0.55)
    g_dark = _mix(gc, (10, 6, 40), 0.45)
    out.append(
        f'<defs><radialGradient id="gemg" cx="0.35" cy="0.3" r="0.95">'
        f'<stop offset="0" stop-color="{g_light}"/><stop offset="0.5" stop-color="{GEM}"/>'
        f'<stop offset="1" stop-color="{g_dark}"/></radialGradient></defs>'
    )
    out.append(f'<rect x="-58" y="-76" width="116" height="24" rx="9" fill="{g}" stroke="{CROWN_STROKE}" stroke-width="4"/>')
    out.append(f'<ellipse cx="0" cy="-64" rx="6.5" ry="9" fill="url(#gemg)" stroke="{CROWN_STROKE}" stroke-width="3"/>')
    out.append(f'<circle cx="-30" cy="-64" r="4.5" fill="url(#gemg)" stroke="{CROWN_STROKE}" stroke-width="2.5"/>')
    out.append(f'<circle cx="30" cy="-64" r="4.5" fill="url(#gemg)" stroke="{CROWN_STROKE}" stroke-width="2.5"/>')
    out.append('<ellipse cx="-2" cy="-68" rx="2.6" ry="3.8" transform="rotate(-22 -2 -68)" fill="#fff" opacity="0.85"/>')
    out.append('<circle cx="-31.5" cy="-65.5" r="1.7" fill="#fff" opacity="0.85"/>')
    out.append('<circle cx="28.5" cy="-65.5" r="1.7" fill="#fff" opacity="0.85"/>')
    out.append("</g>")
    return "\n".join(out)


def build():
    grads = [
        f'<linearGradient id="hg" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{HEART_A}"/><stop offset="1" stop-color="{HEART_B}"/></linearGradient>',
        f'<linearGradient id="cg" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{CROWN_A}"/><stop offset="1" stop-color="{CROWN_B}"/></linearGradient>',
    ]
    stars = []
    for (x, y, r), k in zip(STAR_POS, STAR_ORDER):
        c1, c2 = ARCH_COLORS[k]
        grads.append(
            f'<linearGradient id="sg-{k}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>'
        )
        stars.append(star(x, y, r, f"url(#sg-{k})"))
    text = (
        f'<g transform="rotate(-7)" font-family="{FONT_STACK}" font-weight="bold" '
        f'text-anchor="middle" fill="{TEXT_FILL}" stroke="{TEXT_STROKE}" stroke-width="9" '
        f'paint-order="stroke" stroke-linejoin="round">'
        f'<text x="0" y="118" font-size="96">Mahō</text>'
        f'<text x="6" y="212" font-size="96">Shōjo</text></g>'
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="-470 -260 940 620" width="940" height="620">
  <defs>{"".join(grads)}</defs>
  {"".join(stars)}
  {crown()}
  <path d="{HEART}" fill="url(#hg)" stroke="{HEART_STROKE}" stroke-width="12"/>
  {text}
</svg>"""


svg = build()
OUT_SVG.parent.mkdir(parents=True, exist_ok=True)
OUT_SVG.write_text(svg, encoding="utf-8")
print("saved", OUT_SVG)

# ============================================
# PNG 渲染（resvg；透明底、系統字型）
# ============================================

import resvg_py

for w in PNG_WIDTHS:
    png = bytes(resvg_py.svg_to_bytes(svg_string=svg, width=w, cursive_family="Brush Script MT"))
    out = OUT_SVG.parent / f"logo-{w}.png"
    out.write_bytes(png)
    print("saved", out, f"{len(png)} bytes")
