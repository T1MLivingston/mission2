#!/usr/bin/env python3
"""Render the landscape used by the JPEG demo and inline it into index.html.

The JPEG card teaches compression by re-encoding a photograph at the chosen
quality, which needs pixels the browser will let us read back.  A remote photo
cannot be re-encoded without CORS headers, and school networks block plenty of
hosts outright, so the page ships with its own alpine lake: generated here at
high detail -- ridge texture, ripples, grain -- because it is that fine detail
that falls apart first when the quality slider comes down.

    python3 tools/build-photo.py          # rebuild assets/photo/lake.jpg + inline it
"""
import base64, io, pathlib, sys
import numpy as np
from PIL import Image, ImageFilter

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "assets" / "photo"
OUT = OUT_DIR / "lake.jpg"
INDEX = ROOT / "index.html"

W, H = 1280, 720          # rendered large, downsampled for clean edges
FINAL = (640, 360)
HORIZON = 0.60            # waterline, as a fraction of height

rng = np.random.default_rng(20260830)


def _smooth(t):
    return t * t * (3 - 2 * t)


def noise2(h, w, fy, fx=None):
    """Value noise: a small random grid, smoothly resampled up to (h, w).

    The two frequencies are separate so water can carry noise that is wide and
    flat -- which is what a ripple looks like -- instead of round blobs."""
    fx = fy if fx is None else fx
    g = rng.random((fy + 1, fx + 1))
    ys = np.linspace(0, fy, h); xs = np.linspace(0, fx, w)
    y0 = np.floor(ys).astype(int); x0 = np.floor(xs).astype(int)
    ty = _smooth(ys - y0)[:, None]; tx = _smooth(xs - x0)[None, :]
    y1 = np.minimum(y0 + 1, fy); x1 = np.minimum(x0 + 1, fx)
    a = g[np.ix_(y0, x0)]; b = g[np.ix_(y0, x1)]
    c = g[np.ix_(y1, x0)]; d = g[np.ix_(y1, x1)]
    return (a * (1 - tx) + b * tx) * (1 - ty) + (c * (1 - tx) + d * tx) * ty


def fbm2(h, w, base=4, octaves=6, ratio=1.0):
    """Stacked noise.  ratio > 1 stretches the features sideways."""
    out = np.zeros((h, w)); amp = 1.0; norm = 0.0
    for i in range(octaves):
        f = base * 2 ** i
        out += amp * noise2(h, w, max(1, int(round(f * ratio))), max(1, int(round(f / ratio))))
        norm += amp; amp *= 0.5
    return out / norm


def noise1(n, freq):
    g = rng.random(freq + 1)
    xs = np.linspace(0, freq, n)
    x0 = np.floor(xs).astype(int); fx = _smooth(xs - x0)
    return g[x0] * (1 - fx) + g[np.minimum(x0 + 1, freq)] * fx


def fbm1(n, base=3, octaves=7):
    out = np.zeros(n); amp = 1.0; norm = 0.0
    for i in range(octaves):
        out += amp * noise1(n, base * 2 ** i)
        norm += amp; amp *= 0.5
    return out / norm


def ridgeline(n, base, octaves, sharpness):
    """A mountain profile: folded noise, so crests come to a point."""
    r = fbm1(n, base, octaves)
    r = 1 - np.abs(2 * r - 1)              # fold -> ridges instead of hills
    return r ** sharpness


def lerp(a, b, t):
    return a + (b - a) * t[..., None]


def render():
    yy, xx = np.mgrid[0:H, 0:W]
    v = yy / H
    horizon_px = int(H * HORIZON)

    # --- sky: deep at the top, hazy where it meets the peaks -----------------
    top = np.array([38., 88., 152.]); low = np.array([202., 219., 232.])
    t = np.clip(v / HORIZON, 0, 1) ** 0.8
    img = lerp(top, low, t)

    cloud = fbm2(H, W, base=2, octaves=6, ratio=2.4)
    cloud = np.clip((cloud - 0.50) * 3.0, 0, 1) * np.clip(1 - v / HORIZON * 1.05, 0, 1)
    cloud *= 0.45 + 0.55 * fbm2(H, W, base=10, octaves=4, ratio=1.8)
    img = lerp(img, np.array([250., 249., 245.]), cloud * 0.85)

    # --- ridges, far to near -------------------------------------------------
    # snow is a height on the picture, not a depth below each crest, so only the
    # peaks that get up there wear it -- which is what makes a range read as tall
    layers = [
        dict(top=0.10, amp=0.30, base=2, oct=8, sharp=2.6,
             rock=(118, 132, 154), haze=0.58, snow=0.24, trees=0.0),
        dict(top=0.26, amp=0.26, base=3, oct=8, sharp=2.9,
             rock=(74,  84, 104), haze=0.30, snow=0.20, trees=0.0),
        dict(top=0.44, amp=0.16, base=5, oct=8, sharp=2.4,
             rock=(40,  48,  56), haze=0.10, snow=0.00, trees=0.85),
    ]
    haze_col = np.array([196., 214., 230.])

    for L in layers:
        prof = ridgeline(W, L["base"], L["oct"], L["sharp"])
        crest = (L["top"] + L["amp"] * (1 - prof)) * H
        depth = yy - crest[None, :]
        mask = depth > 0
        if not mask.any():
            continue

        rock = np.array(L["rock"], dtype=float)
        tex = fbm2(H, W, base=14, octaves=7)
        gx = np.gradient(tex, axis=1); gy = np.gradient(tex, axis=0)
        shade = np.clip(0.5 + 34 * (gx * 0.75 - gy * 0.65), 0.30, 1.6)   # sun, upper left
        body = rock[None, None, :] * (0.55 + 0.70 * tex)[..., None] * shade[..., None]
        body *= np.clip(1 - depth / (H * 0.75), 0.40, 1)[..., None]

        if L["snow"] > 0:
            snow_y = (L["snow"] + 0.10 * fbm1(W, 6, 5))[None, :] * H
            band = H * 0.10
            snow = np.clip((snow_y + band - yy) / band, 0, 1) ** 1.5
            snow *= np.clip(depth / 6.0, 0, 1)                    # never spills past the crest
            grit = fbm2(H, W, base=30, octaves=4)
            snow *= np.clip(1.35 - 1.5 * np.abs(grit - 0.5) * 2, 0, 1)   # broken, not painted on
            snow *= np.clip(1.7 * shade - 0.55, 0, 1)             # gullies stay bare rock
            body = lerp(body, np.array([244., 247., 251.]), np.clip(snow, 0, 1) * 0.95)

        if L["trees"] > 0:
            fur = fbm2(H, W, base=90, octaves=3, ratio=0.35)      # tall, thin: conifers
            tline = np.clip((depth - 4) / 26.0, 0, 1)
            conif = np.clip((fur - 0.42) * 3.2, 0, 1) * tline * L["trees"]
            body = lerp(body, np.array([26., 40., 34.]) * (0.6 + 0.8 * fur)[..., None], conif)

        body = lerp(body, haze_col, np.full((H, W), L["haze"]))
        img = np.where(mask[..., None], body, img)

    # --- the water -----------------------------------------------------------
    water = np.array([36., 106., 114.])
    below = yy >= horizon_px
    d = np.clip((yy - horizon_px) / max(H - horizon_px, 1), 0, 1)

    src_y = np.clip(horizon_px - (yy - horizon_px) * 0.95, 0, horizon_px - 1).astype(int)
    ripple = (np.sin(yy * 0.55 + fbm2(H, W, base=3, octaves=3, ratio=3.0) * 9) * (1 + 14 * d)
              + (fbm2(H, W, base=6, octaves=4, ratio=4.0) - 0.5) * (3 + 22 * d))
    src_x = np.clip(xx + ripple, 0, W - 1).astype(int)
    refl = img[src_y, src_x]

    surf = lerp(refl * 0.60, water, np.clip(0.18 + 0.62 * d, 0, 1))
    # ripples: wide and thin, so they read as lines of light on a surface
    glint = fbm2(H, W, base=4, octaves=5, ratio=7.0)
    glint = np.clip((glint - 0.55) * 4.0, 0, 1) * (0.15 + 0.85 * d)
    surf = lerp(surf, np.array([222., 238., 243.]), np.clip(glint, 0, 0.75))
    img = np.where(below[..., None], surf, img)

    seam = np.exp(-((yy - horizon_px) ** 2) / 4.0)
    img = lerp(img, np.array([230., 240., 244.]), seam * 0.45)

    # --- shoreline rock across the bottom corner ----------------------------
    lip = H * (0.93 + 0.06 * ridgeline(W, 4, 6, 1.6)) - np.clip(0.55 - xx / W, 0, 1) * H * 0.16
    fg = yy > lip
    tex = fbm2(H, W, base=26, octaves=7)
    gx = np.gradient(tex, axis=1); gy = np.gradient(tex, axis=0)
    sh = np.clip(0.55 + 30 * (gx * 0.7 - gy * 0.7), 0.25, 1.7)
    fgcol = np.array([62., 58., 54.])[None, None, :] * (0.35 + 1.05 * tex)[..., None] * sh[..., None]
    img = np.where(fg[..., None], fgcol, img)

    # --- finish: vignette, grain ---------------------------------------------
    cx, cy = (xx / W - 0.5), (yy / H - 0.5)
    vig = 1 - 0.38 * np.clip((cx ** 2 * 1.15 + cy ** 2) * 2.1, 0, 1) ** 1.3
    img *= vig[..., None]
    warm = np.exp(-((v - HORIZON * 0.92) ** 2) / 0.02)[..., None] * np.array([16., 7., -6.])
    img += warm * 0.9                                    # late light along the range
    img += rng.normal(0, 2.6, img.shape)                 # grain: what JPEG hates most

    out = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGB")
    out = out.resize(FINAL, Image.LANCZOS)
    return out.filter(ImageFilter.UnsharpMask(radius=1.3, percent=80, threshold=2))


START, END = "/* PHOTO_START */", "/* PHOTO_END */"


def inline(jpg_bytes):
    uri = "data:image/jpeg;base64," + base64.b64encode(jpg_bytes).decode("ascii")
    block = (START + "\nconst PHOTO_LOCAL = \"" + uri + "\";\n" + END)
    s = INDEX.read_text()
    a = s.index("\n" + START)
    b = s.index("\n" + END, a)
    assert a < b, "photo markers out of order"
    INDEX.write_text(s[:a + 1] + block + s[b + 1 + len(END):])
    return len(uri)


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    photo = render()
    buf = io.BytesIO()
    photo.save(buf, "JPEG", quality=92, subsampling=0, optimize=True)
    data = buf.getvalue()
    OUT.write_bytes(data)
    print(f"{OUT.relative_to(ROOT)}  {len(data)/1024:.0f} KB  {photo.size[0]}x{photo.size[1]}")
    if "--no-inline" not in sys.argv:
        print(f"inlined {inline(data)/1024:.0f} KB of data URI into index.html")
