"""Schneidet Deko-Objekte aus einem von ChatGPT gemalten Bogen auf Magenta aus.

Nutzung: python3 tools/cut_sprites.py bogen.png assets/deko/name.webp
Ergebnis: ein Sprite-Atlas (WebP mit Transparenz) und die Rechtecke als JSON-Zeile
(Reihenfolge: zeilenweise von links oben), die in index.html eingetragen wird.
"""
import sys, json
from PIL import Image
import numpy as np
from scipy import ndimage

src, dst = sys.argv[1], sys.argv[2]
im = np.asarray(Image.open(src).convert('RGB')).astype(np.int32)
r, g, b = im[..., 0], im[..., 1], im[..., 2]
# Hintergrund: reines Magenta und magentastichige Kantenpixel
bg = (r > 150) & (b > 150) & (g < 110) & (np.abs(r - b) < 90)
fringe = (r - g > 70) & (b - g > 70) & (np.abs(r - b) < 110)
near_bg = ndimage.binary_dilation(bg, iterations=2)
alpha = ~(bg | (fringe & near_bg))
alpha = ndimage.binary_opening(alpha, iterations=1)
lab, n = ndimage.label(ndimage.binary_dilation(alpha, iterations=6))
objs = []
for i, sl in enumerate(ndimage.find_objects(lab), 1):
    ys, xs = sl
    if (ys.stop - ys.start) * (xs.stop - xs.start) < 2500: continue  # Krümel
    objs.append((ys.start, ys.stop, xs.start, xs.stop))
# zeilenweise sortieren (Zeile = obere/untere Hälfte des Bogens)
H = im.shape[0]
objs.sort(key=lambda o: (0 if (o[0] + o[1]) / 2 < H / 2 else 1, o[2]))
rgba = np.dstack([im.astype(np.uint8), (alpha * 255).astype(np.uint8)])
pad, x, rects, tiles = 2, 0, [], []
for (y0, y1, x0, x1) in objs:
    t = rgba[y0:y1, x0:x1].copy()
    m = t[..., 3] > 0
    ys, xs = np.where(m)
    t = t[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    tiles.append(t)
W = sum(t.shape[1] + pad for t in tiles); Hh = max(t.shape[0] for t in tiles)
atlas = np.zeros((Hh, W, 4), np.uint8)
for t in tiles:
    h, w = t.shape[:2]
    atlas[Hh - h:, x:x + w] = t          # unten ausgerichtet
    rects.append([x, Hh - h, w, h]); x += w + pad
Image.fromarray(atlas, 'RGBA').save(dst, 'WEBP', quality=92, method=6)
print(len(rects), 'Objekte'); print(json.dumps(rects))
