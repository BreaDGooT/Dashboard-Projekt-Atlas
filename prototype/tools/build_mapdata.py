"""Bereitet eine gemalte Dorf-Karte für die Animation vor.

Erzeugt aus assets/dorf.webp:
  assets/lichter.png  – nur die leuchtenden Pixel (Fenster, Laternen, Kristall, Bildschirme)
  assets/mapdata.js   – Lichtpunkte, Wasser-Stichproben und ein grobes Wasser-Raster

Aufruf (aus dem Ordner prototype/):  python3 tools/build_mapdata.py
Benötigt: pip install pillow
"""
import json
import random
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "dorf.webp"
CELL = 8  # Rastergröße für die Wasser-Maske in Bildpixeln

# Bereiche, in denen Cyan-Leuchten gewollt ist (Kristall, Labor-Bildschirme)
CYAN_ZONES = [(740, 375, 815, 470), (240, 600, 500, 760)]


def in_zone(x, y):
    return any(x0 < x < x1 and y0 < y < y1 for x0, y0, x1, y1 in CYAN_ZONES)


def clusters(points, cell=12, min_count=6):
    grid = {}
    for x, y in points:
        grid.setdefault((x // cell, y // cell), []).append((x, y))
    found = [
        [round(sum(p[0] for p in v) / len(v)), round(sum(p[1] for p in v) / len(v)), len(v)]
        for v in grid.values() if len(v) >= min_count
    ]
    found.sort(key=lambda c: -c[2])
    merged = []
    for c in found:
        for m in merged:
            if abs(m[0] - c[0]) < 16 and abs(m[1] - c[1]) < 16:
                m[2] += c[2]
                break
        else:
            merged.append(c)
    return merged


def main():
    im = Image.open(SRC).convert("RGB")
    w, h = im.size
    px = im.load()
    lights = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    lp = lights.load()
    warm, cyan, water = [], [], []
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            if r > 242 and g > 195 and b < 175 and r - b > 85:
                lp[x, y] = (r, g, b, 255)
                warm.append((x, y))
            elif in_zone(x, y) and g > 190 and b > 190 and r < 150:
                lp[x, y] = (r, g, b, 255)
                cyan.append((x, y))
    lights.save(ROOT / "assets" / "lichter.png", optimize=True)

    gw, gh = (w + CELL - 1) // CELL, (h + CELL - 1) // CELL
    bits = []
    for gy in range(gh):
        for gx in range(gw):
            hits = total = 0
            for y in range(gy * CELL, min(h, gy * CELL + CELL), 2):
                for x in range(gx * CELL, min(w, gx * CELL + CELL), 2):
                    r, g, b = px[x, y]
                    total += 1
                    if b > 110 and b > r + 55 and b > g + 12:
                        hits += 1
                        water.append((x, y))
            bits.append("1" if hits / max(1, total) > 0.45 else "0")
    hexmask = "".join(f"{int(''.join(bits[i:i + 4]).ljust(4, '0'), 2):x}" for i in range(0, len(bits), 4))

    random.seed(7)
    sample = random.sample(water, min(900, len(water)))
    data = {
        "size": [w, h],
        "cell": CELL,
        "grid": [gw, gh],
        "waterMask": hexmask,
        "water": [[x, y] for x, y in sample],
        "warm": clusters(warm),
        "cyan": clusters(cyan, 12, 4),
    }
    (ROOT / "assets" / "mapdata.js").write_text(
        "// Automatisch erzeugt von tools/build_mapdata.py – nicht von Hand bearbeiten.\n"
        f"window.MAPDATA = {json.dumps(data, separators=(',', ':'))};\n"
    )
    print(f"Lichter: {len(warm)} warm / {len(cyan)} cyan, Wasser-Stichproben: {len(sample)}")


if __name__ == "__main__":
    main()
