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
INTRO_SRC = "Beta_Wave.gif"
INTRO_SIZE = 300


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


def build_intro():
    """Shrink the waving Beta GIF that greets a team before they pick a chassis.

    Keeps every other frame and a small palette, with the background left
    transparent so the team's colour shows through the plate behind it.
    """
    from PIL import Image, ImageSequence
    src = os.path.join(ORIG, INTRO_SRC)
    if not os.path.isfile(src):
        return None
    frames, colors = [], 48
    for i, frame in enumerate(ImageSequence.Iterator(Image.open(src))):
        if i % 2:
            continue
        f = frame.convert("RGBA")
        f.thumbnail((INTRO_SIZE, INTRO_SIZE), Image.LANCZOS)
        clear = f.getchannel("A").point(lambda a: 255 if a < 128 else 0)
        p = f.convert("RGB").quantize(colors=colors - 1, method=Image.FASTOCTREE)
        p.paste(colors - 1, clear)          # park every transparent pixel on one index
        frames.append(p)
    out = os.path.join(WEB, "intro.gif")
    frames[0].save(out, "GIF", save_all=True, append_images=frames[1:], duration=80,
                   loop=0, disposal=2, transparency=colors - 1, optimize=True)
    print("intro gif: {} frames, {} KB".format(len(frames), os.path.getsize(out) // 1024))
    return out


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

    intro = os.path.join(WEB, "intro.gif")
    if os.path.isfile(intro):
        with open(intro, "rb") as fh:
            gif = base64.b64encode(fh.read()).decode("ascii")
        gblock = ('/* INTRO_START */\nconst INTRO_GIF = "data:image/gif;base64,'
                  + gif + '";\n/* INTRO_END */')
        page, n = re.subn(r"/\* INTRO_START \*/.*?/\* INTRO_END \*/", lambda m: gblock, page, flags=re.S)
        if n != 1:
            sys.exit("could not find the INTRO markers in index.html")
        total += len(gif)

    open(PAGE, "w", encoding="utf-8").write(page)
    print("inlined {} bots, {} KB of base64".format(len(entries), total // 1024))


if __name__ == "__main__":
    if os.path.isdir(ORIG):
        optimize()
        build_intro()
    inline()
