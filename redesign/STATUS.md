# Redesign — STATUS (start here)

_Last updated: 2026-11-14._ This is the single handoff file: read it first, then only the spec files the next task needs.

## Where things are
- **Repo/branch:** `bronius/bronius.github.io`, branch **`redesign`**. `main` is the live bronius.com (classic GitHub Pages, deploy-from-branch, `minima` theme) and is **untouched**.
- **Specs:** `redesign/DESIGN.md` is the index (spec map, decisions D1–D11, no open questions). Topic specs are `01`–`07`.
- **Art masters:** `redesign/art-src/*.jpg`, 18 assets on green chroma plus the 2 original mockups. The caveats are in `07-art-production.md` § Status.
- **Prototype:** `redesign/reference/preview.html` is a greybox with CSS stand-in art and hash routes (`#about`, `#music`…). It's published as a private claude.ai artifact, slug `64c2f82a-b261-4489-9292-1331f4bee533`; republish with `publish_files` (mode `patch`).
- **Build excludes:** `redesign/` and `CLAUDE.md` are in `_config.yml` `exclude`. Underscore dirs (e.g. `_tools/`) are ignored by Jekyll automatically.

## Key decisions (details in DESIGN.md)
- **Stack:** Jekyll on classic Pages with an in-repo theme. Plain modern CSS (`@layer`, nesting, custom props), no Sass, no bundler, one ES module (06).
- **Art (D11):** all visuals are painted raster (Nano Banana Pro) and **all text is live HTML** (D4). Props are blank cutouts with text overlaid.
- **Sign** is a `<button>` toy (D7). Every subpage has its own poster header (D8). Document scroll everywhere (D9). Off-site links get a cue, with a playful one in the nav (D10).
- **Preview:** a local, hand-built static HTML preview is fine for now (no Cloudflare/Netlify yet).

## Phase now: art processing pipeline (NEXT)
Raw art is about 9.3 MB of green-screen JPGs and must become small, transparent, responsive assets.

**Decision: no sprite sheets.** Ship individual files instead:
- The site is on HTTP/2, so request count is cheap and a sprite saves almost nothing.
- A sprite forces every page to download every prop, which breaks per-page loading and `loading="lazy"`.
- Per-asset `srcset`/`<picture>` (1×/2×, AVIF→WebP) doesn't work with sprite regions.
- `border-image` 9/3-slice needs a standalone image.
- Any edit busts the whole sheet's cache.

Build `_tools/art/build.py` (Python: Pillow with AVIF/WebP plus OpenCV, all available locally). It should be deterministic and committed, and re-runnable from masters:
1. **Key:** sample the key color per image from the corners (greens vary). Build a soft alpha from color distance with a ramp, **despill** the edges (clamp G ≤ max(R,B)), and erode/feather about 1px. Handle the `polaroid` bottom gradient. Its photo window and the `board-small` plank gaps become transparent.
2. **Clean:** paint out any corner Gemini sparkle watermark on the plates.
3. **Trim** to the alpha bounding box plus a small pad. Crop `art-*` to their inked border (these are opaque, so no key).
4. **Split** `cloud-puffs` into 3 files. Upscale the clouds 2× (1024px source).
5. **Slice metadata, not files:** measure the `border-image-slice` insets for `board-frame` (9-slice) and `poster-sheet` (3-slice vertical).
6. **Encode** two widths each (1× and 2×) to **AVIF + WebP** in `assets/img/`. Plates: desktop 1376/2752w, mobile 768/1536w. Props: 50% and 100% of the trimmed size. Budgets are in 04-assets.md (desktop plate ≤ 200 KB, props ≤ 40 KB @2×).
7. **Emit** `_data/art.yml` with each asset's widths, heights, file paths and slice insets, so templates can write `width`/`height` attributes (CLS 0) and CSS slice values.

Then rebuild `reference/preview.html` with the real assets (relative paths), screenshot it at 1440×900 and 390×844 (headless Chrome via Playwright is available), and republish the artifact.

## After that
1. Theme skeleton on `redesign`: `_layouts/` (base → home | page → post), `_includes/` (scene, sign, nav, props/*), `_includes/css/*` concatenated by Liquid into `assets/css/site.css`, `_data/nav.yml` and `home.yml`, and a `poster:` block in each page's front matter (06).
2. Port the page content, then retire the `minima` overrides.
3. Lighthouse + axe pass, then merge to `main`.

## Backlog
- **Hanging-sign toy rework.** The current wobble feels weird. Keep it as-is; redo it as its own effort (05-interaction.md).
- Off-site nav treatment (D10): propose 2–3 options using `offsite-tag`.
- Optional: branch previews via Cloudflare Pages/Netlify (needs Bronius's account).

## Conventions
- Bronius edits on github.com from his phone, so **always `git pull --rebase` before working** and fold his edits in rather than overwriting them.
- Commit as `bronius <bronius.motekaitis@gmail.com>`, with the session attribution lines. Push with `git -c push.negotiate=true push`. Commit only to `redesign`.
- Bronius is a veteran engineer: talk technical, and favor modular, semantic, maintainable and fast.
- Keep specs chunked and terse. Update this file at the end of each work session.
