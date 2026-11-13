# 07 — Art Production (Nano Banana prompts)

The backdrop plates are the **only** raster art. Everything else is SVG, CSS or live HTML (see 04-assets.md). The plates must be **completely free of text and props** so the same two images serve every page.

| Plate | Aspect | Min. export | Use |
|---|---|---|---|
| `town-desktop` | 16:9 | 2560 × 1440 (4K if offered) | All pages, ≥ 768px |
| `town-mobile` | 9:16 | 1080 × 1920 (2K+ if offered) | All pages, < 768px |

## How to run it
1. Use **Nano Banana Pro** if it's available (better resolution and layout control), otherwise Nano Banana.
2. Set the aspect ratio in the UI (16:9, then 9:16). Don't rely on the prompt alone.
3. **Plate A:** attach `mockups/home--desktop-mobile.jpg` as a style reference and paste Prompt A. Editing from the mockup keeps the style locked; generating from scratch tends to drift.
4. **Plate B:** attach *your Plate A result* (not the mockup) and paste Prompt B, so the two crops match.
5. Check every output against the checklist at the bottom. Re-roll or follow up with "remove the ___" until it passes.
6. Download as PNG at full resolution and commit to `redesign/art-src/`. Claude crops, encodes to AVIF/WebP and places the files.

---

## Prompt A — Desktop plate (16:9)

```
Using the attached image ONLY as a style reference (the left, wide panel), create a new clean background plate in exactly the same art style: 1940s Tex Avery "Droopy" Western cartoon background painting, hand-inked dark brown outlines, warm sepia, ochre and dusty desert tones, subtle cel-painted watercolor grain, soft vintage hand-painted animation look, exaggerated cartoon perspective.

Scene: first-person view standing on a rustic wooden porch looking out onto a quiet, empty one-horse Texas Old West main street. Weathered wooden saloons and false-front buildings line the left and right sides and recede to a central vanishing point. Open desert mesas sit on the horizon under a warm, pale-gold late-afternoon sky.

Porch frame (foreground):
- A wooden porch overhang/eave runs across the entire top edge, about the top 12% of the image. Two small iron eye-hooks are fixed to the underside of the eave, centered horizontally and about one fifth of the image width apart. NOTHING hangs from them.
- Thick weathered wooden porch posts stand at the far left and far right edges, each about 6% of the image width.
- A horizontal hitching rail spans between the posts at about two-thirds of the image height, kept low and thin.
- Wooden floorboards fill the bottom 10% of the image, in perspective.

Composition rules (this is a website background; UI will be layered on top):
- The sky directly below the center of the eave, from about 12% to 32% of image height and across the middle 60% of the width, is a calm, smooth gradient with NO clouds, birds or detail. A few soft clouds may appear only near the far left and far right.
- The center of the street, the middle 60% of the width from the horizon down to the hitching rail, is calm, low-detail, dusty open ground with only faint texture. No objects in it.
- Keep the right-hand third of the street fairly simple, because a large panel will cover it on some pages.
- Even lighting, low contrast in the center, richer detail toward the edges.

Strictly exclude: any text, letters, numbers, words, signage, painted lettering on building facades (leave false fronts blank), logos, watermarks, signatures. No hanging sign, no wooden signboards, no trail signs, no posters, no notice boards, no parchment, no picture frames, no photos. No people, no animals, no horses, no vehicles. No user-interface elements. No border or frame around the image.
```

## Prompt B — Mobile plate (9:16)

```
Using the attached image as the exact style and scene reference, recompose the same scene as a tall vertical 9:16 portrait background plate. Same art style, palette, line work, watercolor grain, lighting and buildings; it must look like the same place painted by the same artist.

Porch frame:
- The wooden eave runs across the top edge, about the top 8% of the image, with the same two small iron eye-hooks centered and about one third of the image width apart. NOTHING hangs from them.
- Porch posts appear only as narrow slivers at the extreme left and right edges, each about 5% of the image width.
- Floorboards fill the bottom 6% of the image.
- No hitching rail across the middle.

Composition rules (website background, UI layered on top):
- The street recedes straight up the center of the frame to the horizon at about 40% of the image height, with buildings as narrow wedges along both sides.
- The sky from about 8% to 25% of image height, across the middle 80% of the width, is a calm, smooth gradient with no clouds or detail.
- The middle 85% of the width, from the horizon down to the floorboards, is calm, low-detail dusty ground with only faint texture.

Strictly exclude: any text, letters, numbers, words, signage, painted lettering, logos, watermarks, signatures. No hanging sign, no signboards, no trail signs, no posters, no notice boards, no parchment, no frames, no photos. No people, animals, horses or vehicles. No UI elements. No border.
```

## Follow-up fixes (paste as needed)
- `Remove all lettering from the building facades; leave the false fronts as blank weathered wood.`
- `Remove the clouds from the center of the sky under the eave; keep a smooth gradient there.`
- `Remove the object in the middle of the street; replace it with plain dusty ground.`
- `Remove the sign hanging from the eave; keep only the two empty iron hooks.`
- `Keep everything identical but make the center of the image calmer and lower in contrast.`

## Acceptance checklist
- [ ] Zero text or letterforms anywhere, including fake "scribble" text (zoom in on the facades)
- [ ] Nothing hangs from the eave; two empty hooks only
- [ ] Clear sky band under the eave (the nav goes here)
- [ ] Empty, calm center street (props go here)
- [ ] No people, animals or props
- [ ] Posts at the edges, floorboards at the bottom
- [ ] Mobile and desktop plates read as the same place and palette
- [ ] Full-resolution PNG, no visible AI watermark

## Fallback: raster props
If the SVG props (sign, clouds, board, trail signs) clash with the painted plate, generate them as painted cutouts. Run one prop per request, each **blank** (no text), on a flat pure `#00FF00` background for keying, in the same style, with the same reference attached. Example:

```
Using the attached image as the style reference, paint a single blank rough-hewn wooden plank sign with two rope loops on top, front view, no text or markings on it, centered on a flat solid pure green (#00FF00) background with no shadow on the background. Same 1940s Tex Avery Western cartoon style, hand-inked outlines, watercolor grain.
```
