"""Optimise source images (Dropbox exports) into web assets.

usage: python3 tools/images.py <photos_src_dir> <plans_src_dir>
Writes assets/img/photos/*.jpg, assets/img/plans/*.jpg (+ -t thumbs).
"""
import os, sys
from PIL import Image, ImageOps
Image.MAX_IMAGE_PIXELS = None
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from data import PHOTOS, PROJECTS

def save(im, path, long_side, q):
    im = im.copy(); im.thumbnail((long_side, long_side), Image.LANCZOS)
    im.save(path, 'JPEG', quality=q, optimize=True, progressive=True)

def flatten(im):
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA'); bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[-1]); return bg
    return im.convert('RGB')

def main(psrc, plsrc):
    po = os.path.join(ROOT, 'assets/img/photos'); pl = os.path.join(ROOT, 'assets/img/plans')
    os.makedirs(po, exist_ok=True); os.makedirs(pl, exist_ok=True)
    for p in PHOTOS:
        im = ImageOps.exif_transpose(Image.open(os.path.join(psrc, f"2019_Referenzen ({p['src']}).jpeg"))).convert('RGB')
        save(im, f"{po}/{p['id']}.jpg", 1600, 80); save(im, f"{po}/{p['id']}-t.jpg", 720, 74)
    for pr in PROJECTS:
        for i, f in enumerate(pr['files']):
            im = Image.open(os.path.join(plsrc, f))
            im.draft('RGB', (2400, 2400))
            if max(im.size) > 6000:
                im = im.reduce(max(1, max(im.size) // 4800))
            im = flatten(im)
            save(im, f"{pl}/{pr['id']}-{i+1}.jpg", 2200, 82); save(im, f"{pl}/{pr['id']}-{i+1}-t.jpg", 800, 76)
        print('plan', pr['id'])

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
