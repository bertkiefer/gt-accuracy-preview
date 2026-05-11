#!/usr/bin/env python3
"""Mask non-white-background product images and composite onto white."""
import glob
import os
import shutil
from PIL import Image
from rembg import remove, new_session

SHOP_DIR = "assets/images/shop"
BACKUP_DIR = "assets/images/shop_originals"
os.makedirs(BACKUP_DIR, exist_ok=True)

# Files that ARE logos/branding by design — never mask
SKIP_NAMES = {"BruxLogo.png", "KreigerBarrels.png"}

session = new_session("u2net")  # general-purpose model


def has_white_bg(img, threshold=235):
    """Sample border pixels — return True if avg brightness > threshold."""
    if img.mode != "RGB":
        img = img.convert("RGB")
    w, h = img.size
    samples = []
    step_x = max(1, w // 30)
    step_y = max(1, h // 30)
    for x in range(0, w, step_x):
        samples.append(img.getpixel((x, min(2, h - 1))))
        samples.append(img.getpixel((x, max(0, h - 3))))
    for y in range(0, h, step_y):
        samples.append(img.getpixel((min(2, w - 1), y)))
        samples.append(img.getpixel((max(0, w - 3), y)))
    avg = sum(sum(p[:3]) / 3 for p in samples) / len(samples)
    return avg > threshold


FORCE_ALL = True  # process every non-logo image, ignore the "already white" detector

def mask_one(path):
    name = os.path.basename(path)
    if name in SKIP_NAMES:
        return "skipped-logo"
    try:
        img = Image.open(path)
        img.load()
    except Exception as e:
        return f"err-open: {e}"

    if not FORCE_ALL and has_white_bg(img, threshold=252):
        return "skipped-already-white"

    # Backup original once
    backup = os.path.join(BACKUP_DIR, name)
    if not os.path.exists(backup):
        shutil.copy2(path, backup)

    # Convert mode for rembg
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGBA")

    # Remove background → RGBA with transparent bg
    out = remove(img, session=session)

    # Composite onto white
    white = Image.new("RGB", out.size, (255, 255, 255))
    if out.mode == "RGBA":
        white.paste(out, mask=out.split()[3])
    else:
        white.paste(out.convert("RGB"))

    # Save back with same extension
    ext = os.path.splitext(path)[1].lower()
    save_path = path
    try:
        if ext in (".jpg", ".jpeg"):
            white.save(save_path, "JPEG", quality=92)
        elif ext == ".png":
            white.save(save_path, "PNG")
        elif ext == ".webp":
            white.save(save_path, "WEBP", quality=92)
        elif ext == ".avif":
            try:
                white.save(save_path, "AVIF", quality=85)
            except Exception:
                # avif support may be missing — fallback to JPEG with new name
                new_path = save_path.replace(".avif", ".jpg")
                white.save(new_path, "JPEG", quality=92)
                os.remove(save_path)
                return f"masked-converted-to-jpg ({os.path.basename(new_path)})"
        else:
            white.save(save_path)
    except Exception as e:
        return f"err-save: {e}"

    return "masked"


files = sorted(glob.glob(f"{SHOP_DIR}/*"))
print(f"Scanning {len(files)} files in {SHOP_DIR}...")
counts = {"masked": 0, "skipped-already-white": 0, "skipped-logo": 0, "err": 0,
          "masked-converted-to-jpg": 0}
for f in files:
    name = os.path.basename(f)
    result = mask_one(f)
    bucket = result.split("(")[0].strip()
    if bucket.startswith("err"):
        counts["err"] += 1
        print(f"  ✗ {name:50s} {result}")
    elif "masked-converted" in bucket:
        counts["masked-converted-to-jpg"] += 1
        print(f"  → {name:50s} {result}")
    elif bucket == "masked":
        counts["masked"] += 1
        print(f"  ✓ {name:50s} masked → white")
    else:
        counts[bucket] += 1
        # Quiet for skips

print()
for k, v in counts.items():
    if v:
        print(f"  {k:35s} {v}")
