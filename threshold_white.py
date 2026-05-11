#!/usr/bin/env python3
"""Threshold-based background cleanup for dark-subject-on-light-bg photos.
Use this for the rail images that rembg couldn't fully clean — pure threshold
gives a clean #FFFFFF background while preserving the all-black subject."""
import os
import shutil
from PIL import Image

SHOP_DIR = "assets/images/shop"
BACKUP_DIR = "assets/images/shop_originals"

# Images to process (start from backed-up originals, write to shop/)
TARGETS = [
    "Borden-BR-Rails.webp",
    "Borden-Rem700_Rail.webp",
]

THRESHOLD = 200  # mean(R,G,B) > THRESHOLD → snap to pure white


def threshold_to_white(src, dst, threshold=THRESHOLD):
    img = Image.open(src).convert("RGB")
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            if (r + g + b) / 3 > threshold:
                px[x, y] = (255, 255, 255)
    ext = os.path.splitext(dst)[1].lower()
    if ext in (".jpg", ".jpeg"):
        img.save(dst, "JPEG", quality=92)
    elif ext == ".png":
        img.save(dst, "PNG")
    elif ext == ".webp":
        img.save(dst, "WEBP", quality=92)
    else:
        img.save(dst)


for name in TARGETS:
    src = os.path.join(BACKUP_DIR, name)
    dst = os.path.join(SHOP_DIR, name)
    if not os.path.exists(src):
        print(f"  ✗ {name:35s} missing original — skipping")
        continue
    threshold_to_white(src, dst)
    print(f"  ✓ {name:35s} threshold-cleaned → white")
