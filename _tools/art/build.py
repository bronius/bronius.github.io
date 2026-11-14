#!/usr/bin/env python3
"""Art pipeline: redesign/art-src/*.jpg (green-screen masters) -> assets/img/ + _data/art.yml.

Deterministic and re-runnable from masters:
    python3 _tools/art/build.py            # build everything
    python3 _tools/art/build.py sign-plank # build a subset (art.yml is still rewritten from all entries)
    python3 _tools/art/build.py --debug    # also dump keyed PNGs + checker previews to /tmp/art-debug

Steps (see redesign/STATUS.md): key -> clean -> trim -> split -> slice metadata -> encode -> emit.
Needs Pillow (AVIF + WebP), OpenCV, NumPy.
"""
from __future__ import annotations

import hashlib
import sys
from dataclasses import dataclass, field
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "redesign" / "art-src"
OUT = ROOT / "assets" / "img" / "art"  # owned by this script; stale files are swept
DATA = ROOT / "_data" / "art.yml"
URL_PREFIX = "/assets/img/art"
DEBUG_DIR = Path("/tmp/art-debug")

# Encoder settings. Speed/threads are pinned so output is byte-stable across runs.
AVIF_OPAQUE = dict(quality=55, speed=6, max_threads=1, subsampling="4:2:0")
AVIF_ALPHA = dict(quality=50, speed=6, max_threads=1, subsampling="4:4:4")
WEBP_OPAQUE = dict(quality=72, method=6)
WEBP_ALPHA = dict(quality=78, alpha_quality=85, method=6, exact=False)


# --------------------------------------------------------------------------- config
@dataclass
class Asset:
    name: str
    kind: str  # "plate" (opaque, fixed widths) | "prop" (keyed cutout) | "vignette" (opaque, crop to ink border)
    widths: tuple[int, ...] | None = None  # explicit output widths (plates); else derived
    max_w: int | None = None               # cap on the 2x width for props/vignettes
    upscale: int = 1                       # pre-key upscale for low-res masters
    q: int | None = None                   # AVIF quality override
    split: int = 0                         # split a keyed sheet into N components, left->right
    box: str | None = None                 # "wide" | "hole": emit a text/content box (pct)
    slice: str | None = None               # "nine" | "three-v": emit border-image-slice metadata
    inpaint: list[tuple[int, ...]] = field(default_factory=list)  # (x, y, w, h, dx) clone patches, master px


# max_w = 2x width, from the intended rendered box (CSS px x 2). Comments give the box.
ASSETS: list[Asset] = [
    # Plates: paint out the eave hooks. Their spacing (0.28W desktop, 0.6W mobile) would force a
    # sign 0.6-1.3x the viewport wide; the ropes instead run up over the eave, as in the mockup.
    Asset("plate-desktop", "plate", widths=(1376, 2752), inpaint=[(960, 136, 84, 136, 130), (1718, 136, 82, 136, -130)]),
    Asset("plate-mobile", "plate", widths=(768, 1536), inpaint=[(264, 190, 90, 165, 140), (1190, 190, 90, 165, -140)]),
    Asset("sign-plank", "prop", max_w=1040, box="wide"),           # ~520px incl. ropes
    Asset("cloud-bank", "prop", upscale=2, max_w=1400),  # desktop nav row ~700px
    Asset("cloud-puffs", "prop", upscale=2, split=3, max_w=640),  # one link each, <=320px
    Asset("trail-arrow", "prop", max_w=600, box="wide"),           # home pillar ~300px
    Asset("trail-plank", "prop", max_w=600, box="wide"),
    Asset("note-pinned", "prop", max_w=600),
    Asset("scroll-banner", "prop", max_w=1280),        # intro line, <=640px
    Asset("board-small", "prop", max_w=720),           # recent posts ~360px
    Asset("polaroid", "prop", max_w=520, box="hole"),              # ~260px
    Asset("board-frame", "prop", max_w=800, slice="nine"),      # only the ~48px border must resolve at 2x
    Asset("poster-sheet", "prop", max_w=1120, q=42, slice="three-v"),  # smooth parchment tolerates lower q # poster <=560px; mobile 390px full-bleed
    Asset("offsite-tag", "prop", max_w=160),           # ~80px nav cue
    Asset("art-about", "vignette", max_w=800),         # poster vignette ~400px
    Asset("art-music", "vignette", max_w=800),
    Asset("art-professional", "vignette", max_w=800),
    Asset("art-life", "vignette", max_w=800),
]

PAD = 6  # px of transparent margin kept around trimmed cutouts (master scale)


# --------------------------------------------------------------------------- io
def load_rgb(name: str) -> np.ndarray:
    for ext in (".png", ".jpg", ".jpeg", ".webp"):
        p = SRC / f"{name}{ext}"
        if p.exists():
            return np.asarray(Image.open(p).convert("RGB"), dtype=np.float32)
    raise FileNotFoundError(f"no master for {name} in {SRC}")


# --------------------------------------------------------------------------- 1. key
def masked_blur(values: np.ndarray, mask: np.ndarray, sigma: float) -> tuple[np.ndarray, np.ndarray]:
    """Normalized-convolution blur: average of `values` over `mask`, spread by a Gaussian."""
    m = mask.astype(np.float32)
    den = cv2.GaussianBlur(m, (0, 0), sigma)
    if values.ndim == 3:
        num = cv2.GaussianBlur(values * m[..., None], (0, 0), sigma)
        return num / np.maximum(den, 1e-6)[..., None], den
    num = cv2.GaussianBlur(values * m, (0, 0), sigma)
    return num / np.maximum(den, 1e-6), den


def key_green(rgb: np.ndarray) -> np.ndarray:
    """Return straight-alpha RGBA float32 (0..255) with the green screen removed.

    The key colour is estimated per pixel (a local field), so gradients such as
    the darkening at the bottom of `polaroid` and interior holes key correctly.
    """
    R, G, B = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    g = G - np.maximum(R, B)  # greenness; warm art sits at <= ~0

    # Sure background: strongly green, eroded away from edge mixes.
    sure = (g > 60).astype(np.uint8)
    sure = cv2.erode(sure, np.ones((7, 7), np.uint8))

    # Global fallback key: median of the sure pixels on the image border.
    border = np.zeros_like(sure, dtype=bool)
    border[:8], border[-8:], border[:, :8], border[:, -8:] = True, True, True, True
    pool = rgb[(sure > 0) & border]
    if len(pool) == 0:
        pool = rgb[sure > 0]
    k_global = np.median(pool, axis=0)

    # Local key colour field: wide normalized blur of sure-bg colours.
    sigma = max(rgb.shape[:2]) / 80
    K, den = masked_blur(rgb, sure, sigma)
    w = np.clip(den / 0.02, 0, 1)[..., None]  # trust the field only near real background
    K = K * w + k_global * (1 - w)
    kg = np.maximum(K[..., 1] - np.maximum(K[..., 0], K[..., 2]), 30.0)

    # Coverage from greenness relative to the local key. Two estimates, take the max:
    #  - absolute: g / g_K, ~linear in mix for bright green;
    #  - chromatic: (g/G) / (g_K/G_K), brightness-invariant, so shaded green in narrow
    #    gaps (board-small) and JPEG 4:2:0 chroma bleed into dark ink both key out.
    kr = kg / np.maximum(K[..., 1], 1.0)
    ratio = np.where(G > 24, g / np.maximum(G, 1.0), 0.0)
    t = np.maximum(g / kg, ratio / kr)
    lo, hi = 0.10, 0.85
    alpha = 1.0 - np.clip((t - lo) / (hi - lo), 0, 1)

    # Un-mix the key from edge pixels, then despill (clamp G <= max(R,B)).
    a3 = np.maximum(alpha, 1e-3)[..., None]
    fg = (rgb - (1 - alpha)[..., None] * K) / a3
    fg = np.where(alpha[..., None] > 0.02, fg, rgb)
    fg = np.clip(fg, 0, 255)
    fg[..., 1] = np.minimum(fg[..., 1], np.maximum(fg[..., 0], fg[..., 2]))

    # Choke ~1px and feather to lose the last fringe.
    alpha = cv2.erode(alpha, np.ones((3, 3), np.uint8))
    alpha = cv2.GaussianBlur(alpha, (0, 0), 0.5)

    return np.dstack([fg, alpha * 255.0])


def drop_islands(rgba: np.ndarray, keep_frac: float = 0.01) -> np.ndarray:
    """Zero out alpha components smaller than keep_frac of the largest (specks, sparkles)."""
    solid = (rgba[..., 3] > 8).astype(np.uint8)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(solid, connectivity=8)
    if n <= 2:
        return rgba
    areas = stats[1:, cv2.CC_STAT_AREA]
    keep = np.zeros(n, bool)
    keep[1:] = areas >= areas.max() * keep_frac
    # Grow the kept region slightly so soft edges belonging to kept parts survive.
    kept = cv2.dilate(keep[lab].astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
    out = rgba.copy()
    out[..., 3] = np.where(kept, out[..., 3], 0)
    return out


# --------------------------------------------------------------------------- 2. clean
def inpaint(rgb: np.ndarray, rects: list[tuple[int, ...]]) -> np.ndarray:
    """Paint out features with a feathered clone patch: (x, y, w, h, dx) copies the same rows
    from dx px to the side. Plates are horizontally coherent (beam grain, sky gradient), so this
    continues ink lines exactly where diffusion inpainting (Telea) smears them."""
    out = rgb.copy()
    for x, y, w, h, dx in rects:
        m = np.zeros(rgb.shape[:2], np.float32)
        m[y : y + h, x : x + w] = 1.0
        m = cv2.GaussianBlur(m, (0, 0), 6)
        src = np.roll(rgb, -dx, axis=1)
        y0, y1 = max(0, y - 30), min(rgb.shape[0], y + h + 30)
        x0, x1 = max(0, x - 30), min(rgb.shape[1], x + w + 30)
        mm = m[y0:y1, x0:x1, None]
        out[y0:y1, x0:x1] = out[y0:y1, x0:x1] * (1 - mm) + src[y0:y1, x0:x1] * mm
    return out


# --------------------------------------------------------------------------- 3. trim
def alpha_bbox(a: np.ndarray, thresh: float = 4) -> tuple[int, int, int, int]:
    ys, xs = np.nonzero(a > thresh)
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def trim(rgba: np.ndarray, pad: int = PAD) -> np.ndarray:
    x0, y0, x1, y1 = alpha_bbox(rgba[..., 3])
    h, w = rgba.shape[:2]
    return rgba[max(0, y0 - pad) : min(h, y1 + pad), max(0, x0 - pad) : min(w, x1 + pad)]


def crop_ink_border(rgb: np.ndarray) -> np.ndarray:
    """Vignettes: crop to the thin dark inked rectangle drawn around the picture."""
    lum = rgb @ np.array([0.299, 0.587, 0.114], np.float32)
    dark = lum < 95
    h, w = dark.shape
    rows = dark.mean(axis=1)
    cols = dark.mean(axis=0)

    def first(profile: np.ndarray, frac: float, rng: range) -> int:
        for i in rng:
            if profile[i] > frac:
                return i
        raise ValueError("ink border not found")

    # A border line spans most of the picture; scan inward from each edge.
    y0 = first(rows, 0.45, range(0, h // 3))
    y1 = first(rows, 0.45, range(h - 1, 2 * h // 3, -1))
    x0 = first(cols, 0.45, range(0, w // 3))
    x1 = first(cols, 0.45, range(w - 1, 2 * w // 3, -1))
    return rgb[y0 : y1 + 1, x0 : x1 + 1]


# --------------------------------------------------------------------------- 4. split
def split_components(rgba: np.ndarray, n: int) -> list[np.ndarray]:
    solid = (rgba[..., 3] > 8).astype(np.uint8)
    solid = cv2.morphologyEx(solid, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    cnt, lab, stats, _ = cv2.connectedComponentsWithStats(solid, connectivity=8)
    order = np.argsort(-stats[1:, cv2.CC_STAT_AREA])[:n] + 1
    order = sorted(order, key=lambda i: stats[i, cv2.CC_STAT_LEFT])
    parts = []
    for i in order:
        x, y, w, h = (int(stats[i, k]) for k in (cv2.CC_STAT_LEFT, cv2.CC_STAT_TOP, cv2.CC_STAT_WIDTH, cv2.CC_STAT_HEIGHT))
        mask = cv2.dilate((lab == i).astype(np.uint8), np.ones((7, 7), np.uint8)) > 0
        part = rgba.copy()
        part[..., 3] = np.where(mask, part[..., 3], 0)
        parts.append(trim(part))
    if len(parts) != n:
        raise ValueError(f"expected {n} components, found {len(parts)}")
    return parts


# --------------------------------------------------------------------------- 5. slice metadata
def inner_window(rgba: np.ndarray) -> tuple[int, int, int, int]:
    """Bounding box (x, y, w, h) of the largest transparent region not touching the border."""
    a = rgba[..., 3]
    h, w = a.shape
    hole = (a < 128).astype(np.uint8)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(hole, connectivity=4)
    best, best_area = None, 0
    for i in range(1, n):
        x, y, bw, bh, area = stats[i]
        if x > 0 and y > 0 and x + bw < w and y + bh < h and area > best_area:
            best, best_area = i, area
    if best is None:
        raise ValueError("no inner window found")
    return tuple(int(v) for v in stats[best][:4])


def box_wide(rgba: np.ndarray) -> tuple[int, int, int, int]:
    """The plank of a sign: longest run of rows whose opaque coverage is near the max
    (excludes ropes and posts), with the median left/right extent over those rows."""
    a = rgba[..., 3] > 128
    cover = a.sum(axis=1).astype(np.float32)
    good = np.concatenate([[0], (cover > cover.max() * 0.7).astype(np.int8), [0]])
    edges = np.flatnonzero(np.diff(good))  # alternating run starts / ends
    runs = list(zip(edges[::2], edges[1::2]))
    best = max(runs, key=lambda r: r[1] - r[0])
    y0, y1 = best
    lefts = [np.argmax(a[y]) for y in range(y0, y1)]
    rights = [a.shape[1] - np.argmax(a[y][::-1]) for y in range(y0, y1)]
    x0, x1 = int(np.median(lefts)), int(np.median(rights))
    return x0, y0, x1 - x0, y1 - y0


def slice_nine(rgba: np.ndarray) -> dict:
    """board-frame: insets = distance from each image edge to the transparent inner window."""
    h, w = rgba.shape[:2]
    x, y, bw, bh = inner_window(rgba)
    return dict(top=y, right=w - (x + bw), bottom=h - (y + bh), left=x)


def slice_three_v(rgba: np.ndarray) -> dict:
    """poster-sheet: find the featureless middle run for a vertical 3-slice.

    Signal per row: mean luminance of the sheet interior (inset from the deckle
    edges, whose extent is noise) and ink density (nails, curl outline). Rows whose
    smoothed values leave the band set by the central 40% belong to the caps.
    """
    a = rgba[..., 3]
    h, w = a.shape
    lum = rgba[..., :3] @ np.array([0.299, 0.587, 0.114], np.float32)
    inset = int(w * 0.04)
    mean_l = np.full(h, np.nan, np.float32)
    ink = np.zeros(h, np.float32)
    for yy in range(h):
        xs = np.nonzero(a[yy] > 128)[0]
        if len(xs) < 2 * inset + 2:
            continue
        inner = lum[yy, xs[0] + inset : xs[-1] - inset]
        mean_l[yy] = inner.mean()
        ink[yy] = (inner < 90).mean()
    mean_l = np.nan_to_num(mean_l, nan=0.0)
    k = max(3, h // 100) | 1
    sm = lambda v: np.convolve(v, np.ones(k) / k, mode="same")
    mean_l, ink = sm(mean_l), sm(ink)
    band = slice(int(h * 0.3), int(h * 0.7))
    med_l = float(np.median(mean_l[band]))
    ink_lim = float(np.percentile(ink[band], 95)) * 2 + 0.002
    bad = (np.abs(mean_l - med_l) > 8) | (ink > ink_lim)
    top = next((y for y in range(int(h * 0.45), -1, -1) if bad[y]), 0) + 1
    bot = next((y for y in range(int(h * 0.55), h) if bad[y]), h)
    pad = int(h * 0.01)  # step away from the transition
    return dict(top=top + pad, right=0, bottom=h - bot + pad, left=0)


# --------------------------------------------------------------------------- 6. encode
def to_pil(arr: np.ndarray) -> Image.Image:
    arr = np.clip(np.rint(arr), 0, 255).astype(np.uint8)
    if arr.shape[2] == 4:
        arr[arr[..., 3] == 0, :3] = 0  # flatten invisible pixels: smaller, stable files
        return Image.fromarray(arr, "RGBA")
    return Image.fromarray(arr, "RGB")


def resize(img: Image.Image, width: int) -> Image.Image:
    if width == img.width:
        return img
    h = round(img.height * width / img.width)
    if img.mode == "RGBA":  # resample premultiplied to avoid dark halos
        pm = img.convert("RGBa").resize((width, h), Image.LANCZOS)
        return pm.convert("RGBA")
    return img.resize((width, h), Image.LANCZOS)


def encode(img: Image.Image, stem: str, alpha: bool, q: int | None = None) -> list[dict]:
    files = []
    avif = dict(AVIF_ALPHA if alpha else AVIF_OPAQUE)
    if q:
        avif["quality"] = q
    for fmt, opts in (("avif", avif), ("webp", WEBP_ALPHA if alpha else WEBP_OPAQUE)):
        p = OUT / f"{stem}.{fmt}"
        img.save(p, fmt.upper(), **opts)
        files.append(dict(fmt=fmt, path=p, bytes=p.stat().st_size))
    return files


def widths_for(a: Asset, natural_w: int) -> tuple[int, int]:
    w2 = min(natural_w, a.max_w) if a.max_w else natural_w
    w2 -= w2 % 2
    return w2 // 2, w2


# --------------------------------------------------------------------------- pipeline
def process(a: Asset, debug: bool) -> list[dict]:
    """Return one or more art.yml entries for an asset."""
    rgb = load_rgb(a.name)
    rgb = inpaint(rgb, a.inpaint)

    if a.kind == "plate":
        img = to_pil(rgb)
        return [emit(a.name, img, a.widths, alpha=False, extra={})]

    if a.kind == "vignette":
        img = to_pil(crop_ink_border(rgb))
        return [emit(a.name, img, widths_for(a, img.width), alpha=False, extra={})]

    if a.upscale > 1:
        h, w = rgb.shape[:2]
        rgb = cv2.resize(rgb, (w * a.upscale, h * a.upscale), interpolation=cv2.INTER_LANCZOS4)
        rgb = np.clip(rgb, 0, 255)
    rgba = drop_islands(key_green(rgb))
    if debug:
        dump_debug(a.name, rgba)

    pieces = split_components(rgba, a.split) if a.split else [trim(rgba)]
    entries = []
    for i, piece in enumerate(pieces, 1):
        name = f"{a.name}-{i}" if a.split else a.name
        img = to_pil(piece)
        extra = {}
        widths = widths_for(a, img.width)
        if a.slice:
            ins = slice_nine(piece) if a.slice == "nine" else slice_three_v(piece)
            scale = widths[-1] / img.width  # measured on the master; report in largest-output px
            extra["slice"] = dict(
                kind=a.slice,
                px={k: round(v * scale) for k, v in ins.items()},
                pct={k: round(100 * v / (img.height if k in ("top", "bottom") else img.width), 2) for k, v in ins.items()},
            )
        if a.box:
            x, y, bw, bh = box_wide(piece) if a.box == "wide" else inner_window(piece)
            extra["box"] = dict(kind=a.box, x=round(100 * x / img.width, 2), y=round(100 * y / img.height, 2),
                                w=round(100 * bw / img.width, 2), h=round(100 * bh / img.height, 2))
        entries.append(emit(name, img, widths, alpha=True, extra=extra, q=a.q))
    return entries


def emit(name: str, img: Image.Image, widths: tuple[int, ...], alpha: bool, extra: dict, q: int | None = None) -> dict:
    sizes = []
    for w in widths:
        r = resize(img, w)
        files = encode(r, f"{name}-{w}", alpha, q)
        sizes.append(dict(w=r.width, h=r.height, files=files))
    entry = dict(name=name, alpha=alpha, ratio=round(img.width / img.height, 4), sizes=sizes, **extra)
    report(entry)
    return entry


def report(e: dict) -> None:
    parts = []
    for s in e["sizes"]:
        kb = " ".join(f"{f['fmt']}={f['bytes'] / 1024:.0f}K" for f in s["files"])
        parts.append(f"{s['w']}x{s['h']} {kb}")
    sl = f"  slice={e['slice']['px']}" if "slice" in e else ""
    print(f"  {e['name']:<20} " + " | ".join(parts) + sl)


def dump_debug(name: str, rgba: np.ndarray) -> None:
    DEBUG_DIR.mkdir(parents=True, exist_ok=True)
    to_pil(rgba).save(DEBUG_DIR / f"{name}.png")


# --------------------------------------------------------------------------- 7. emit yaml
def write_yaml(entries: list[dict]) -> None:
    """Hand-rolled YAML (no PyYAML dependency); keys sorted, stable output."""
    L = [
        "# GENERATED by _tools/art/build.py — do not edit by hand.",
        "# Each asset: intrinsic sizes (for width/height attrs, CLS 0), file URLs, optional border-image slice.",
        "# slice.px is in pixels of the LARGEST size; prefer slice.pct in CSS (resolution-independent).",
    ]
    for e in sorted(entries, key=lambda e: e["name"]):
        L.append(f"{e['name']}:")
        L.append(f"  alpha: {str(e['alpha']).lower()}")
        L.append(f"  ratio: {e['ratio']}")
        big = e["sizes"][-1]
        L.append(f"  width: {big['w']}")
        L.append(f"  height: {big['h']}")
        L.append("  sizes:")
        for s in e["sizes"]:
            L.append(f"    - w: {s['w']}")
            L.append(f"      h: {s['h']}")
            for f in s["files"]:
                L.append(f"      {f['fmt']}: {URL_PREFIX}/{f['path'].name}")
        if "box" in e:
            b = e["box"]
            L.append(f"  box: {{kind: {b['kind']}, x: {b['x']}, y: {b['y']}, w: {b['w']}, h: {b['h']}}}  # pct of image")
        if "slice" in e:
            sl = e["slice"]
            L.append("  slice:")
            L.append(f"    kind: {sl['kind']}")
            for unit in ("px", "pct"):
                v = sl[unit]
                L.append(f"    {unit}: {{top: {v['top']}, right: {v['right']}, bottom: {v['bottom']}, left: {v['left']}}}")
    DATA.parent.mkdir(parents=True, exist_ok=True)
    DATA.write_text("\n".join(L) + "\n")


def main(argv: list[str]) -> None:
    debug = "--debug" in argv
    only = {x for x in argv if not x.startswith("-")}
    OUT.mkdir(parents=True, exist_ok=True)
    entries = []
    for a in ASSETS:
        if only and a.name not in only:
            continue
        print(a.name)
        entries += process(a, debug)
    if only:
        print("(subset build: _data/art.yml not rewritten)")
        return
    # Remove stale outputs from previous configs.
    produced = {f["path"].name for e in entries for s in e["sizes"] for f in s["files"]}
    for p in OUT.glob("*"):
        if p.suffix in (".avif", ".webp") and p.name not in produced:
            p.unlink()
    write_yaml(entries)
    total = sum(f["bytes"] for e in entries for s in e["sizes"] for f in s["files"])
    digest = hashlib.sha256(b"".join(sorted((OUT / n).read_bytes() for n in produced))).hexdigest()[:12]
    print(f"\n{len(produced)} files, {total / 1024:.0f} KB total, digest {digest}")


if __name__ == "__main__":
    main(sys.argv[1:])
