#!/usr/bin/env python3
"""Aggressive cleanup for the Borden rail images.
Strategy: rembg with alpha matting → composite on white → threshold residual
near-whites to pure #FFFFFF. The subject is essentially black so this is safe."""
import os
import shutil
from PIL import Image
from rembg import remove, new_session

SHOP_DIR = "assets/images/shop"
BACKUP_DIR = "assets/images/shop_originals"

TARGETS = [
    "Borden-BR-Rails.webp",
    "Borden-Rem700_Rail.webp",
]

session = new_session("u2net")


def clean(src, dst):
    img = Image.open(src).convert("RGBA")
    # Aggressive rembg: alpha matting with tight thresholds
    out = remove(
        img,
        session=session,
        alpha_matting=True,
        alpha_matting_foreground_threshold=240,
        alpha_matting_background_threshold=10,
        alpha_matting_erode_size=10,
    )
    # Composite onto pure white
    white = Image.new("RGB", out.size, (255, 255, 255))
    if out.mode == "RGBA":
        white.paste(out, mask=out.split()[3])
    else:
        white.paste(out.convert("RGB"))

    # Post-threshold: any near-white pixel → pure white. Subject is black
    # so this only cleans residual halos / soft shadows.
    px = white.load()
    w, h = white.size
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            if (r + g + b) / 3 > 180:
                px[x, y] = (255, 255, 255)

    ext = os.path.splitext(dst)[1].lower()
    if ext in (".jpg", ".jpeg"):
        white.save(dst, "JPEG", quality=92)
    elif ext == ".webp":
        white.save(dst, "WEBP", quality=92)
    elif ext == ".png":
        white.save(dst, "PNG")
    else:
        white.save(dst)


for name in TARGETS:
    src = os.path.join(BACKUP_DIR, name)
    dst = os.path.join(SHOP_DIR, name)
    if not os.path.exists(src):
        print(f"  ✗ missing original: {name}")
        continue
    clean(src, dst)
    print(f"  ✓ {name:40s} cleaned")
