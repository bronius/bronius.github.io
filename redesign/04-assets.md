# 04 — Asset Architecture

Split the artwork into layers instead of using one giant background image. This keeps it sharp on retina screens, fast to load, and interactive.

## Layer → format

| Layer | Format | Notes |
|---|---|---|
| Town street + sky | Raster: AVIF, with WebP fallback | Two crops, desktop 16:9 and mobile 9:16. Export at 2× and serve via `<picture>` + `srcset`. Rendered as a `position: fixed` `<img>` (not a CSS background) so it gets `fetchpriority="high"` and format negotiation. |
| Porch frame (posts, eave, boards) | Transparent WebP/AVIF *or* merged into the street plate | Keep separate only if the frame must move or resize independently of the street. Default is to merge. |
| Hanging sign + ropes | Inline SVG (preferred) or transparent PNG | Isolated from the eave so it can rotate around its top anchor (`transform-origin: top center`). The text "Bronius" is live text over the plank art. |
| Clouds (nav) | Transparent WebP or SVG | One cloud-chain image, or several cloud puffs behind flex items. |
| Notice board | Transparent WebP + CSS `border-image` (9-slice) | The height adapts to the viewport without stretching the wood grain. |
| Trail and plank signs | `border-image` 9-slice on wood texture, plus an SVG arrow tip | Live text label. |
| Parchment | CSS gradients + SVG `feTurbulence` noise + deckle-edge `mask-image` | No raster needed. |
| Nail heads | Inline SVG (data URI) | |
| Spot vignettes (violin, lantern), scrollbar arrows | Inline SVG | Scale without blur. |
| All text | Live HTML + web fonts | **Never baked into images** (D4). |

## Budgets
| Asset | Target |
|---|---|
| Desktop backdrop (AVIF, 2560w) | ≤ 180 KB |
| Mobile backdrop (AVIF, 1080w) | ≤ 100 KB |
| All other raster art combined | ≤ 120 KB |
| Fonts (2 families, subset woff2) | ≤ 80 KB |

## Production notes
- The current mockups have text, nav and props baked in, so they **can't be used as plates**. They need clean, text-free renders of each layer: an empty street, a blank sign plank, empty clouds and an empty board.
- Keep masters (PNG/PSD at 4K) out of the deployed site, either in `redesign/art-src/` (which is excluded from the build) or outside the repo.
- Encode with `avifenc`/`cwebp` or Squoosh, and commit only the outputs to `assets/img/`.
