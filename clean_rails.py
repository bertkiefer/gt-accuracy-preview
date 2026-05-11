#!/usr/bin/env python3
"""Pure-threshold cleanup for the Borden rail images.
The rails are essentially pure black (brightness < 50). The gray shadow
between them is 100-180 brightness. A 130-threshold cleans the shadow
completely while leaving the rails intact."""
import os
from PIL import Image

SHOP_DIR = "assets/images/shop"
BACKUP_DIR = "assets/images/shop_originals"

TARGETS = [
    "Borden-BR-Rails.webp",
    "Borden-Rem700_Rail.webp",
]

THRESHOLD = 130  # mean(R,G,B) > THRESHOLD → snap to pure white


def threshold_clean(src, dst):
    img = Image.open(src).convert("RGB")
    w, h = img.size
    px = img.load()
    cleaned = 0
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            if (r + g + b) / 3 > THRESHOLD:
                px[x, y] = (255, 255, 255)
                cleaned += 1
    ext = os.path.splitext(dst)[1].lower()
    if ext in (".jpg", ".jpeg"):
        img.save(dst, "JPEG", quality=92)
    elif ext == ".webp":
        img.save(dst, "WEBP", quality=92)
    elif ext == ".png":
        img.save(dst, "PNG")
    else:
        img.save(dst)
    return cleaned, w * h


for name in TARGETS:
    src = os.path.join(BACKUP_DIR, name)
    dst = os.path.join(SHOP_DIR, name)
    if not os.path.exists(src):
        print(f"  ✗ missing original: {name}")
        continue
    cleaned, total = threshold_clean(src, dst)
    pct = 100 * cleaned / total
    print(f"  ✓ {name:35s} {cleaned}/{total} px → white ({pct:.1f}%)")
