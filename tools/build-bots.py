#!/usr/bin/env python3
"""Rebuild the inlined bot artwork inside index.html.

Reads the full-size art from assets/bots/original/, writes optimized 320px
grayscale copies to assets/bots/web/, then rewrites the BOT_IMG block in
index.html with base64 data URIs so the page stays a single self-contained
file that works from a Chromebook's Downloads folder with no server.

    python3 tools/build-bots.py
"""
import base64, glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIG = os.path.join(ROOT, "assets", "bots", "original")
WEB  = os.path.join(ROOT, "assets", "bots", "web")
PAGE = os.path.join(ROOT, "index.html")
SIZE = 320
COLORS = 48


def optimize():
    """Downscale each bot, keeping the transparent background.

    Transparency matters: the page paints the team's chosen colour behind every
    bot, so a flattened white background would hide it.
    """
    from PIL import Image
    os.makedirs(WEB, exist_ok=True)
    for src in sorted(glob.glob(os.path.join(ORIG, "*.png"))):
        im = Image.open(src).convert("RGBA")
        im.thumbnail((SIZE, SIZE), Image.LANCZOS)
        # FASTOCTREE is the one Pillow quantizer that carries alpha through.
        im.quantize(colors=COLORS, method=Image.FASTOCTREE).save(
            os.path.join(WEB, os.path.basename(src)), optimize=True)


def inline():
    entries, total = [], 0
    for f in sorted(glob.glob(os.path.join(WEB, "*.png"))):
        name = os.path.splitext(os.path.basename(f))[0]
        with open(f, "rb") as fh:
            b64 = base64.b64encode(fh.read()).decode("ascii")
        total += len(b64)
        entries.append('  {}: "data:image/png;base64,{}",'.format(name, b64))
    block = "/* BOT_IMG_START */\nconst BOT_IMG = {\n" + "\n".join(entries) + "\n};\n/* BOT_IMG_END */"
    page = open(PAGE, encoding="utf-8").read()
    page, n = re.subn(r"/\* BOT_IMG_START \*/.*?/\* BOT_IMG_END \*/", lambda m: block, page, flags=re.S)
    if n != 1:
        sys.exit("could not find the BOT_IMG markers in index.html")
    open(PAGE, "w", encoding="utf-8").write(page)
    print("inlined {} bots, {} KB of base64".format(len(entries), total // 1024))


if __name__ == "__main__":
    if os.path.isdir(ORIG):
        optimize()
    inline()
