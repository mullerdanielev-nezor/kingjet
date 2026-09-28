"""Új képek feldolgozása: python optimize_images.py

Az images/ mappában lévő minden nem .webp képet (png, jpg, jpeg) átalakít:
  - 4:3 arányúra igazítja (a háttér színével kiegészítve, ha kell),
  - legfeljebb 1200 px szélesre méretezi,
  - .webp fájlként menti (a megadott vagy a fájlnévből képzett névvel),
  - az eredetit az images/eredeti/ mappába helyezi.
Használat névvel: python optimize_images.py "fájl.png" "uj-nev"
"""
import os, re, shutil, sys, unicodedata
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(ROOT, 'images')
ORIG = os.path.join(IMG, 'eredeti')
W, H = 1200, 900


def slug(t):
    t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-') or 'kep'


def to_webp(src, name=None, dst_dir=IMG):
    im = Image.open(src).convert('RGB')
    if abs(im.width / im.height - 4 / 3) > 0.05:
        bg = im.getpixel((2, 2))
        scale = min(W / im.width, H / im.height)
        r = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
        canvas = Image.new('RGB', (W, H), bg)
        canvas.paste(r, ((W - r.width) // 2, (H - r.height) // 2))
        im = canvas
    elif im.width > W:
        im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    name = slug(name or os.path.splitext(os.path.basename(src))[0])
    out = os.path.join(dst_dir, name + '.webp')
    im.save(out, 'WEBP', quality=82, method=6)
    return out


def main():
    os.makedirs(ORIG, exist_ok=True)
    if len(sys.argv) >= 2:
        files = [(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)]
    else:
        files = [(os.path.join(IMG, f), None) for f in os.listdir(IMG)
                 if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    for src, name in files:
        out = to_webp(src, name)
        base = os.path.basename(src)
        if os.path.dirname(os.path.abspath(src)) == IMG:
            shutil.move(src, os.path.join(ORIG, base))
        print(base, '->', os.path.relpath(out, ROOT), os.path.getsize(out) // 1024, 'KB')


if __name__ == '__main__':
    main()
