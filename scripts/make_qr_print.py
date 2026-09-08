# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "qrcode>=7.4",
#   "pillow>=10.0",
#   "opencv-contrib-python-headless>=4.9",
# ]
# ///
"""4x6 明信片（2:3）滿版列印用 QR 卡片。

用法（於專案根目錄）：
    uv run scripts/make_qr_print.py

產出（docs/public/print/）：
    qr-4x6-dark.png / .jpg    深紫魔法陣版
    qr-4x6-light.png / .jpg   乳白簡潔版

規格：1200 x 1800 px、2:3、300 DPI、sRGB，實體 10.2 x 15.2 cm（4 x 6 吋）。
JPG 給 7-11 ibon／照片沖印上傳，PNG 留存檔。

滿版注意事項：
- 底圖鋪滿整張，四邊沒有白邊；沖印機會裁掉邊緣約 2～3 mm
- 因此所有「不能被裁到」的東西（標題、網址、QR）都放在 SAFE 內縮範圍內
- QR 每模組 20 px ＝ 300 DPI 下約 1.7 mm，遠高於掃描下限（約 0.4 mm）
- 靜區（QUIET）4 模組必須維持淺色，任何裝飾都不可壓進 QR 方塊範圍
- 改完務必看結尾驗證輸出為 PASS，並印一張用手機實掃確認
"""

import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

from make_qr import (
    URL,
    BG,
    GOLD,
    ACCENT,
    C_TOP,
    CAPTION_COLOR,
    build_qr,
    load_font,
    render_tile,
    star_pts,
    verify,
)

# ============================================
# 設定區
# ============================================

TITLE = "魔法少女 TRPG"
URL_TEXT = "maho-shojo.vercel.app/intro/"

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "docs" / "public" / "print"

# --- 版面（單位：px，300 DPI；1 mm ≒ 11.8 px） ---
W, H = 1200, 1800       # 4x6 吋 @300 DPI
DPI = 300
SAFE = 72               # 安全區內縮（約 6 mm），沖印裁切不會吃到內容

QR_S = 20               # QR 每模組像素（20 px ≒ 1.7 mm）
QR_QUIET = 4            # 靜區模組數（掃描必需，至少 4）
PANEL_PAD = 34          # 深色版：QR 方塊外的乳白面板留邊
PANEL_TOP = 450         # 面板上緣 y

TITLE_CY = 250          # 標題垂直中心
TITLE_SIZE = 96
TITLE_SPACING = 8
URL_CY = 1578           # 網址垂直中心
URL_SIZE = 46
URL_SPACING = 2

STAR_COUNT = 70
STAR_SEED = 20260827

# --- 深色版配色 ---
DARK_TOP = (26, 14, 50)       # 底圖漸層上緣（深紫夜）
DARK_BOT = (112, 32, 84)      # 底圖漸層下緣（洋紅）
GLOW = (170, 92, 200)         # QR 後方光暈
TITLE_GOLD = (245, 214, 128)  # 深底上的標題金（比 GOLD 亮，印出來才不濁）
URL_LIGHT = (226, 214, 242)


def gradient_bg(top, bot):
    """由上而下的線性漸層底圖。"""
    img = Image.new("RGB", (W, H), top)
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / (H - 1)
        d.line([(0, y), (W, y)], fill=tuple(round(top[i] + (bot[i] - top[i]) * t) for i in range(3)))
    return img


def radial_glow(img, cx, cy, radius, color, strength, blur):
    """在 img 上疊一層徑向光暈（以模糊過的圓形遮罩合成）。"""
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=strength)
    mask = mask.filter(ImageFilter.GaussianBlur(blur))
    img.paste(Image.new("RGB", (W, H), color), (0, 0), mask)


def side_arcs(d, cx, cy, color, opacity):
    """左右兩側的魔法陣弧線（避開上下的標題與網址）。"""
    for r, wdt in ((660, 5), (702, 2)):
        for start, end in ((-52, 52), (128, 232)):
            d.arc([cx - r, cy - r, cx + r, cy + r], start, end, fill=color + (opacity,), width=wdt)


def scatter_stars(d, avoid, palette):
    """在避開區域之外灑星星（固定亂數種子，每次產出一致）。"""
    rnd = random.Random(STAR_SEED)
    ax0, ay0, ax1, ay1 = avoid
    placed = 0
    while placed < STAR_COUNT:
        x = rnd.randint(24, W - 24)
        y = rnd.randint(24, H - 24)
        if ax0 - 26 < x < ax1 + 26 and ay0 - 26 < y < ay1 + 26:
            continue
        if TITLE_CY - 90 < y < TITLE_CY + 90 or URL_CY - 60 < y < URL_CY + 60:
            continue
        r_out = rnd.uniform(5, 15)
        col, alpha = palette[rnd.randrange(len(palette))]
        d.polygon(star_pts(x, y, r_out, r_out * 0.33), fill=col + (int(alpha * rnd.uniform(0.55, 1.0)),))
        placed += 1


def text_center(d, text, cy, font, fill, spacing=0):
    """置中橫排文字（逐字繪製以套用字距）。"""
    widths = [d.textlength(ch, font=font) for ch in text]
    total = sum(widths) + spacing * (len(text) - 1)
    x = (W - total) / 2
    for ch, w in zip(text, widths):
        d.text((x, cy), ch, font=font, fill=fill, anchor="lm")
        x += w + spacing


def build_card(tile, dark):
    """組出一張 1200x1800 的滿版卡片。"""
    tile_w = tile.size[0]
    qr_x = (W - tile_w) // 2
    qr_y = PANEL_TOP + (PANEL_PAD if dark else 0)
    cx, cy = W // 2, qr_y + tile_w // 2

    if dark:
        img = gradient_bg(DARK_TOP, DARK_BOT).convert("RGBA")
        radial_glow(img, cx, cy, 520, GLOW, 96, 190)
    else:
        img = Image.new("RGBA", (W, H), BG + (255,))
        radial_glow(img, cx, cy, 620, (255, 244, 218), 150, 220)

    deco = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dd = ImageDraw.Draw(deco)
    side_arcs(dd, cx, cy, GOLD, 130 if dark else 90)
    px0, py0 = qr_x - PANEL_PAD, PANEL_TOP
    px1, py1 = qr_x + tile_w + PANEL_PAD, PANEL_TOP + tile_w + PANEL_PAD * 2
    avoid = (px0, py0, px1, py1) if dark else (qr_x, qr_y, qr_x + tile_w, qr_y + tile_w)
    scatter_stars(dd, avoid, [(GOLD, 235), (ACCENT, 215), ((255, 255, 255), 190)] if dark
                  else [(GOLD, 170), (ACCENT, 150), (C_TOP, 90)])
    img = Image.alpha_composite(img, deco)

    if dark:
        shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(shadow).rounded_rectangle([px0, py0 + 16, px1, py1 + 16], radius=52, fill=(18, 6, 32, 150))
        img = Image.alpha_composite(img, shadow.filter(ImageFilter.GaussianBlur(22)))
        panel = ImageDraw.Draw(img)
        panel.rounded_rectangle([px0, py0, px1, py1], radius=52, fill=BG + (255,),
                                outline=GOLD + (210,), width=4)

    img.alpha_composite(tile, (qr_x, qr_y))

    d = ImageDraw.Draw(img)
    title_font = load_font(TITLE_SIZE, bold=True) or load_font(TITLE_SIZE)
    url_font = load_font(URL_SIZE)
    if title_font is None or url_font is None:
        print("警告：找不到可用字型，略過文字")
    else:
        text_center(d, TITLE, TITLE_CY, title_font,
                    (TITLE_GOLD if dark else C_TOP) + (255,), TITLE_SPACING)
        text_center(d, URL_TEXT, URL_CY, url_font,
                    (URL_LIGHT if dark else CAPTION_COLOR) + (255,), URL_SPACING)
    return img.convert("RGB")


def save_pair(img, stem):
    png = OUT_DIR / f"{stem}.png"
    jpg = OUT_DIR / f"{stem}.jpg"
    img.save(png, dpi=(DPI, DPI))
    img.save(jpg, quality=95, subsampling=0, dpi=(DPI, DPI))
    print(f"saved {png.name} / {jpg.name}  {img.size}  "
          f"{png.stat().st_size // 1024} KB / {jpg.stat().st_size // 1024} KB")
    return png


def main():
    m, n, version = build_qr(URL)
    tile_w = (n + 2 * QR_QUIET) * QR_S
    print(f"version={version}, modules={n}x{n}, tile={tile_w}px, "
          f"module={QR_S / DPI * 25.4:.2f}mm @{DPI}DPI")

    qr_x = (W - tile_w) // 2
    assert qr_x >= SAFE, f"QR 超出安全區（x={qr_x} < {SAFE}）"
    assert PANEL_TOP + tile_w + PANEL_PAD * 2 <= H - SAFE, "QR 面板超出下方安全區"

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    ok = True
    for stem, dark in (("qr-4x6-dark", True), ("qr-4x6-light", False)):
        # 深色版：QR 貼在乳白面板上，靜區用不透明乳白
        # 淺色版：靜區透明，直接吃底圖光暈，避免出現方形接縫
        tile = render_tile(m, n, QR_S, quiet=QR_QUIET, bg=BG if dark else None)
        png = save_pair(build_card(tile, dark), stem)
        for f in (png, png.with_suffix(".jpg")):
            print(f"--- 驗證 {f.name} ---")
            r = verify(f)
            ok &= (r is not False)
    print("ALL:", "PASS" if ok else "FAIL")


if __name__ == "__main__":
    main()
