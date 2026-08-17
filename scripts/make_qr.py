# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "qrcode>=7.4",
#   "pillow>=10.0",
#   "opencv-contrib-python-headless>=4.9",
# ]
# ///
"""魔法少女風 QR code 產生器。

用法（於專案根目錄）：
    uv run scripts/make_qr.py

產出：docs/public/qr-intro.png（印刷用）與 docs/public/qr-intro.svg（向量版），
並以 OpenCV（WeChat 偵測器＋標準偵測器多尺寸）驗證可掃描。

想調整外觀，改下方「設定區」即可；調整原則：
- 點陣顏色（C_TOP／C_BOT）要維持夠深（在乳白底上要能二值化），避免淡色
- QUIET（靜區）至少 4；所有裝飾都放在靜區之外
- 中央徽章半徑（EMBLEM_R_MODULES）不要超過 4 個模組（糾錯 H 級的安全範圍）
- 改完務必看結尾的驗證輸出為 PASS，並用手機實掃一次
"""

import math
from pathlib import Path

import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image, ImageDraw, ImageFont

# ============================================
# 設定區：網址、文字、尺寸、配色、圖案開關
# ============================================

URL = "https://maho-shojo.vercel.app/intro/"
CAPTION = "魔法少女 TRPG──序章"          # 底部標注文字（留空字串 "" 則不畫）

ROOT = Path(__file__).resolve().parent.parent
OUT_PNG = ROOT / "docs" / "public" / "qr-intro.png"
OUT_SVG = ROOT / "docs" / "public" / "qr-intro.svg"

# --- 尺寸（單位：模組＝QR 的一格） ---
S = 28              # 每模組像素
QUIET = 5           # 靜區寬度（掃描必需的留白，至少 4）
EXTRA = 4           # 靜區外的裝飾邊寬度
BOTTOM_EXTRA = 3    # 底部標注文字的額外空間

# --- 配色 ---
BG = (253, 248, 239)          # 底色（乳白）
C_TOP = (74, 47, 143)         # 點陣漸層起點（深紫，左上）
C_BOT = (176, 53, 121)        # 點陣漸層終點（洋紅，右下）
GOLD = (201, 151, 28)         # 金色（星徽、外環、角星）
ACCENT = (208, 102, 192)      # 粉紫（角落小星）
CAPTION_COLOR = (109, 95, 138)

# --- 圖案樣式 ---
MODULE_RADIUS = 0.3     # 資料點圓角（0＝方塊、0.5＝圓形）
MODULE_GAP = 1          # 資料點之間的間隙（px；越大越「點狀」但掃描裕度變小）
EYE_RADIUS = 1.9        # 定位眼外框圓角（單位：模組；0＝方角）
EMBLEM_ENABLED = True   # 中央星徽
EMBLEM_R_MODULES = 3.5  # 星徽半徑（模組數，勿超過 4）
RINGS_ENABLED = True    # 外圍雙金環（魔法陣）
CORNER_STARS_ENABLED = True  # 四角星星
FONT_PATHS = [          # 標注字型（依序嘗試；都失敗則略過標注）
    "C:/Windows/Fonts/msjh.ttc",
    "C:/Windows/Fonts/msyh.ttc",
]

VERIFY_SIZES = (400, 500, 700, 900)  # 驗證用縮放尺寸

# ============================================
# 產生 QR 矩陣（糾錯 H 級：容忍約 30% 遮損，造型的本錢）
# ============================================

qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, border=0)
qr.add_data(URL)
qr.make(fit=True)
m = qr.modules
n = len(m)
print(f"version={qr.version}, modules={n}x{n}")

PAD = (QUIET + EXTRA) * S
W = n * S + PAD * 2
H = W + BOTTOM_EXTRA * S
CX = PAD + n * S / 2
CY = PAD + n * S / 2
EMB_R = EMBLEM_R_MODULES * S


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def module_color(r, c):
    """對角漸層：左上 C_TOP → 右下 C_BOT。"""
    return lerp(C_TOP, C_BOT, (r + c) / (2 * (n - 1)))


def in_eye(r, c):
    return (r < 7 and c < 7) or (r < 7 and c >= n - 7) or (r >= n - 7 and c < 7)


def in_emblem(r, c):
    if not EMBLEM_ENABLED:
        return False
    x = PAD + (c + 0.5) * S
    y = PAD + (r + 0.5) * S
    return math.hypot(x - CX, y - CY) < EMB_R + 0.5 * S


def star_pts(cx, cy, r_out, r_in, rot=-90):
    """四芒星（8 頂點交錯）。調整 r_in/r_out 比例可改變星形胖瘦。"""
    pts = []
    for i in range(8):
        ang = math.radians(rot + i * 45)
        rr = r_out if i % 2 == 0 else r_in
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    return pts


# ============================================
# PNG（Pillow）
# ============================================

img = Image.new("RGBA", (W, H), BG + (255,))
d = ImageDraw.Draw(img)

# 資料模組
for r in range(n):
    for c in range(n):
        if not m[r][c] or in_eye(r, c) or in_emblem(r, c):
            continue
        x = PAD + c * S
        y = PAD + r * S
        g = MODULE_GAP
        d.rounded_rectangle(
            [x + g, y + g, x + S - g, y + S - g],
            radius=int(S * MODULE_RADIUS),
            fill=module_color(r, c) + (255,),
        )

# 定位眼（外環 7×7、留白 5×5、內塊 3×3，維持 1:1:3:1:1 比例）
for rr_, cc_ in [(0, 0), (0, n - 7), (n - 7, 0)]:
    x = PAD + cc_ * S
    y = PAD + rr_ * S
    col = module_color(rr_, cc_) + (255,)
    rad = int(S * EYE_RADIUS)
    d.rounded_rectangle([x + 1, y + 1, x + 7 * S - 1, y + 7 * S - 1], radius=rad, fill=col)
    d.rounded_rectangle([x + S + 2, y + S + 2, x + 6 * S - 2, y + 6 * S - 2], radius=int(rad * 0.7), fill=BG + (255,))
    d.rounded_rectangle([x + 2 * S + 2, y + 2 * S + 2, x + 5 * S - 2, y + 5 * S - 2], radius=int(rad * 0.45), fill=col)

# 中央星徽：白圓＋金環＋四芒星
if EMBLEM_ENABLED:
    d.ellipse([CX - EMB_R, CY - EMB_R, CX + EMB_R, CY + EMB_R],
              fill=(255, 255, 255, 255), outline=GOLD + (255,), width=max(2, S // 6))
    d.polygon(star_pts(CX, CY, EMB_R * 0.62, EMB_R * 0.24), fill=GOLD + (255,))

# 外圍雙金環（放在靜區之外，不影響掃描）
if RINGS_ENABLED:
    ring_r1 = n * S / 2 + (QUIET + 2.0) * S
    ring_r2 = ring_r1 + 0.75 * S
    for rr2, wdt in [(ring_r1, max(2, S // 9)), (ring_r2, max(1, S // 14))]:
        d.ellipse([CX - rr2, CY - rr2, CX + rr2, CY + rr2], outline=GOLD + (90,), width=wdt)

# 四角星星
if CORNER_STARS_ENABLED:
    off = 1.6 * S
    for sx in (off, W - off):
        for sy in (off, W - off):
            d.polygon(star_pts(sx, sy, 0.95 * S, 0.34 * S), fill=GOLD + (255,))
            d.polygon(star_pts(sx + 1.4 * S, sy + (0.9 * S if sy < W / 2 else -0.9 * S), 0.4 * S, 0.15 * S),
                      fill=ACCENT + (200,))

# 底部標注
if CAPTION:
    for fp in FONT_PATHS:
        try:
            font = ImageFont.truetype(fp, int(S * 1.15))
            tw = d.textlength(CAPTION, font=font)
            d.text(((W - tw) / 2, W + int(0.6 * S)), CAPTION, font=font, fill=CAPTION_COLOR + (255,))
            break
        except Exception:
            continue
    else:
        print("caption skipped: no usable font")

OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
img.convert("RGB").save(OUT_PNG)
print("saved", OUT_PNG, img.size)

# ============================================
# SVG（同幾何的向量版）
# ============================================


def rgb(t3):
    return f"rgb({t3[0]},{t3[1]},{t3[2]})"


def svg_star(cx, cy, r_out, r_in, fill, opacity=1.0):
    pts = " ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in star_pts(cx, cy, r_out, r_in))
    return f'<polygon points="{pts}" fill="{fill}" opacity="{opacity}"/>'


parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
    f'<rect width="{W}" height="{H}" fill="{rgb(BG)}"/>',
]
for r in range(n):
    for c in range(n):
        if not m[r][c] or in_eye(r, c) or in_emblem(r, c):
            continue
        x = PAD + c * S
        y = PAD + r * S
        g = MODULE_GAP
        parts.append(
            f'<rect x="{x + g}" y="{y + g}" width="{S - 2 * g}" height="{S - 2 * g}" '
            f'rx="{S * MODULE_RADIUS:.0f}" fill="{rgb(module_color(r, c))}"/>'
        )
for rr_, cc_ in [(0, 0), (0, n - 7), (n - 7, 0)]:
    x = PAD + cc_ * S
    y = PAD + rr_ * S
    col = rgb(module_color(rr_, cc_))
    rad = S * EYE_RADIUS
    parts.append(f'<rect x="{x + 1}" y="{y + 1}" width="{7 * S - 2}" height="{7 * S - 2}" rx="{rad:.0f}" fill="{col}"/>')
    parts.append(f'<rect x="{x + S + 2}" y="{y + S + 2}" width="{5 * S - 4}" height="{5 * S - 4}" rx="{rad * 0.7:.0f}" fill="{rgb(BG)}"/>')
    parts.append(f'<rect x="{x + 2 * S + 2}" y="{y + 2 * S + 2}" width="{3 * S - 4}" height="{3 * S - 4}" rx="{rad * 0.45:.0f}" fill="{col}"/>')
if EMBLEM_ENABLED:
    parts.append(f'<circle cx="{CX}" cy="{CY}" r="{EMB_R}" fill="#fff" stroke="{rgb(GOLD)}" stroke-width="{max(2, S // 6)}"/>')
    parts.append(svg_star(CX, CY, EMB_R * 0.62, EMB_R * 0.24, rgb(GOLD)))
if RINGS_ENABLED:
    ring_r1 = n * S / 2 + (QUIET + 2.0) * S
    ring_r2 = ring_r1 + 0.75 * S
    parts.append(f'<circle cx="{CX}" cy="{CY}" r="{ring_r1}" fill="none" stroke="{rgb(GOLD)}" stroke-opacity="0.35" stroke-width="{max(2, S // 9)}"/>')
    parts.append(f'<circle cx="{CX}" cy="{CY}" r="{ring_r2}" fill="none" stroke="{rgb(GOLD)}" stroke-opacity="0.35" stroke-width="{max(1, S // 14)}"/>')
if CORNER_STARS_ENABLED:
    off = 1.6 * S
    for sx in (off, W - off):
        for sy in (off, W - off):
            parts.append(svg_star(sx, sy, 0.95 * S, 0.34 * S, rgb(GOLD)))
            parts.append(svg_star(sx + 1.4 * S, sy + (0.9 * S if sy < W / 2 else -0.9 * S), 0.4 * S, 0.15 * S, rgb(ACCENT), 0.8))
if CAPTION:
    parts.append(
        f'<text x="{W / 2}" y="{W + 1.6 * S}" text-anchor="middle" fill="{rgb(CAPTION_COLOR)}" '
        f"font-family=\"'Segoe UI', 'Noto Sans TC', 'Microsoft JhengHei', sans-serif\" "
        f'font-size="{S * 1.15:.0f}" letter-spacing="2">{CAPTION}</text>'
    )
parts.append("</svg>")
OUT_SVG.write_text("\n".join(parts), encoding="utf-8")
print("saved", OUT_SVG)

# ============================================
# 解碼驗證：WeChat 偵測器（近似手機實力）＋標準偵測器多尺寸
# ============================================

try:
    import cv2
except ImportError:
    print("cv2 不可用，略過驗證（請務必用手機實掃確認）")
else:
    cvimg = cv2.imread(str(OUT_PNG))
    det = cv2.QRCodeDetector()
    wechat = cv2.wechat_qrcode.WeChatQRCode()
    ok = True
    wres, _ = wechat.detectAndDecode(cvimg)
    print("wechat@full:", "OK" if URL in wres else f"FAIL {wres}")
    ok &= URL in wres
    for size in VERIFY_SIZES:
        scaled = cv2.resize(cvimg, (size, int(size * cvimg.shape[0] / cvimg.shape[1])))
        res, *_ = det.detectAndDecode(scaled)
        wr, _ = wechat.detectAndDecode(scaled)
        print(f"@{size}: cv2={'OK' if res == URL else 'x'} wechat={'OK' if URL in wr else 'FAIL'}")
        ok &= URL in wr
    print("RESULT:", "PASS" if ok else "FAIL")
