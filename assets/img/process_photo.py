#!/usr/bin/env python3
"""
Crop graduation photo: remove watermark, keep head + upper body.

Usage:
  1. Save the original photo as:  assets/img/portrait_original.jpg
  2. Run:  python3 assets/img/process_photo.py
  3. Output saved to:  assets/img/portrait.jpg
"""
from PIL import Image, ImageDraw
import numpy as np

input_path = 'assets/img/portrait_original.jpg'
output_path = 'assets/img/portrait.jpg'

img = Image.open(input_path).convert('RGB')
w, h = img.size
print(f"Original size: {w}x{h}")

# Sample background blue from the clean top-right area (no watermark there)
sx1, sx2 = int(w * 0.68), int(w * 0.95)
sy1, sy2 = int(h * 0.03), int(h * 0.13)
bg_arr = np.array(img.crop((sx1, sy1, sx2, sy2)))
bg_color = tuple(int(v) for v in bg_arr.mean(axis=(0, 1))[:3])
print(f"Background colour: {bg_color}")

# Paint over the University of Nottingham watermark (top-left region)
draw = ImageDraw.Draw(img)
draw.rectangle([(0, 0), (int(w * 0.52), int(h * 0.145))], fill=bg_color)

# Crop: full width, from ~6% top (above hair) to ~65% height (just above hands)
crop_top    = int(h * 0.06)
crop_bottom = int(h * 0.65)
img_out = img.crop((0, crop_top, w, crop_bottom))

img_out.save(output_path, quality=95, optimize=True)
print(f"Saved → {output_path}  ({img_out.width}x{img_out.height})")
