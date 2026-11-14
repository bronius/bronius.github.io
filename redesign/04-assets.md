# 04 — Asset Architecture

Split the artwork into layers instead of using one giant background image. Every layer is painted, so the site matches the mockups, and layering keeps it fast, reusable and interactive.

## Layer → format (D11: painted raster, live text)

| Layer | Format | Notes |
|---|---|---|
| Backdrop plates (street, sky, porch frame) | AVIF + WebP fallback, opaque | `plate-desktop` 16:9 and `plate-mobile` 9:16, 2× resolution. A `position: fixed` `<picture>`/`<img>` (not a CSS background) so it gets `fetchpriority="high"` and format negotiation. |
| Hanging sign | AVIF/WebP with alpha | `sign-plank` cutout. "Bronius" is live Rye text centered over the plank. Rotates around the top rope anchor (`transform-origin: top center`). |
| Nav clouds | AVIF/WebP with alpha | `cloud-bank` behind the desktop nav row; `cloud-puffs` sliced into 3 images for the wrapping mobile nav. Links are live text. |
| Home props | AVIF/WebP with alpha | `trail-arrow`, `trail-plank`, `note-pinned`, `scroll-banner`, `board-small`, `polaroid`. Each is a positioned box with the painted image as a background and live text laid over it. The polaroid window is transparent, and the Flickr `<img>` sits behind it. |
| Subpage board | AVIF/WebP with alpha, **9-slice** | `board-frame` via CSS `border-image`. The corners stay fixed and the sides stretch to any height. |
| Poster parchment | AVIF/WebP with alpha, **3-slice** vertical | `poster-sheet`: top cap + repeatable middle + bottom cap (`border-image` with `round`), so it fits any length of copy. |
| Poster vignettes | AVIF/WebP, opaque | `art-*`, one per subpage, picked in front matter. |
| Off-site cue | AVIF/WebP with alpha | `offsite-tag`, a small painted tag beside off-site nav links (D10). Body links use a CSS `::after` glyph. |
| All text | Live HTML + web fonts | **Never baked into images** (D4). Poster headers, sign name, nav and copy are all HTML. |

Masters live in `redesign/art-src/` (excluded from the build). **`_tools/art/build.py`** keys, cleans, trims, splits, measures and encodes them into `assets/img/art/`, and writes `_data/art.yml` (dims, srcset URLs, content `box`, `slice` insets). Templates read geometry from `site.data.art`; never hand-type it.

## Budgets
| Asset | Target |
|---|---|
| Desktop plate (AVIF, 2560w) | ≤ 200 KB |
| Mobile plate (AVIF, 1080w) | ≤ 110 KB |
| Each cutout prop (AVIF, 1× and 2×) | ≤ 40 KB at 2× |
| Above-the-fold total, home (plate, sign, clouds, scroll, 3 pillars) | ≤ 450 KB |
| Whole home page | ≤ 700 KB. Below-the-fold props use `loading="lazy"` |
| Fonts (2 families, subset woff2) | ≤ 80 KB |

## Production notes
- The current mockups have text, nav and props baked in, so they **can't be used as art**. 07-art-production.md has prompts for every clean layer.
- Keep masters (PNG/PSD at 4K) out of the deployed site, either in `redesign/art-src/` (which is excluded from the build) or outside the repo.
- Encoding is Pillow AVIF (q50 alpha / q55 opaque, speed 6, 1 thread, so output is byte-stable) plus WebP. The poster uses q42 (smooth parchment). The pipeline output is committed.
