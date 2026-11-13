# 03 — Design Tokens

These are CSS custom properties on `:root`. They're the single source of truth, so components consume tokens and never hard-code values.

## Color
| Token | Value | Use |
|---|---|---|
| `--ink` | `#2b1d12` | Outlines, body text |
| `--parchment` | `#f3e4c8` | Poster and scroll fill |
| `--parchment-edge` | `#d9be94` | Parchment vignette and burn |
| `--wood-dark` | `#4a2e18` | Notice board, scrollbar track |
| `--wood-mid` | `#7a4e2d` | Sign plank, scrollbar thumb |
| `--sky` | `#d8a468` | Backdrop fallback color (shown before the image loads) |
| `--cloud` | `rgb(255 249 238 / .92)` | Cloud nav fill |

Contrast check: `--ink` on `--parchment` is about 13:1, which passes AAA.

## Type
| Token | Value | Use |
|---|---|---|
| `--font-display` | `'Rye', 'Alfa Slab One', serif` | Sign, poster headers, prop titles |
| `--font-body` | `'Lora', Georgia, serif` | Body copy, nav |
| `--step-display` | `clamp(2rem, 4vw, 3.2rem)` | Poster header |
| `--step-sign` | `clamp(1.8rem, 3.5vw, 2.8rem)` | Sign |
| `--leading` | `1.65` | Body line-height |

Self-host both fonts as `woff2`, subset to Latin, with `font-display: swap`. Rye is display-only, so it can be subset aggressively.

## Motion
| Token | Value | Use |
|---|---|---|
| `--sway-amp` | `1.5deg` | Idle sign sway amplitude |
| `--sway-period` | `6s` | Idle sign sway cycle |

All motion is disabled under `prefers-reduced-motion: reduce`.
