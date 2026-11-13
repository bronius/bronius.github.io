# Bronius.com Redesign — Design Index

A 1940s Tex Avery–style Western skin for bronius.com: you're standing on a wooden porch looking out at a one-horse Texas main street. The site's content lives on props in the scene, like trail signs, parchment scrolls, a notice board and a wanted poster.

This file is the **entry point**. Each spec below covers one topic and stands alone, so it can be read (by a human or by Claude) without loading the others.

## Spec map

| File | Scope | Read when… |
|---|---|---|
| [01-concept.md](01-concept.md) | Art direction, scene composition, style rules | Making or judging artwork |
| [02-layout.md](02-layout.md) | Home and subpage layouts, breakpoints, content mapping | Building templates and CSS layout |
| [03-tokens.md](03-tokens.md) | Color, type, spacing and motion tokens | Writing any CSS |
| [04-assets.md](04-assets.md) | Raster vs. vector vs. live-DOM split, formats, budgets | Producing or exporting artwork |
| [05-interaction.md](05-interaction.md) | Sign physics, scroll model, reduced motion, a11y | Writing JS or scroll behavior |
| [06-architecture.md](06-architecture.md) | Build and stack, file layout, performance budget | Starting implementation |
| [07-art-production.md](07-art-production.md) | Nano Banana prompts for the backdrop plates, acceptance checklist | Generating artwork |
| [reference/preview.html](reference/preview.html) | Clickable prototype: home + subpages, placeholder art | Previewing on a phone |
| [reference/starter.html](reference/starter.html) | Single-file prototype (corrected) | Sanity-checking the concept in a browser |

## Mockups

| File | Shows |
|---|---|
| [mockups/home--desktop-mobile.jpg](mockups/home--desktop-mobile.jpg) | Home: desktop 16:9 (left) and mobile portrait (right) |
| [mockups/subpage--desktop-mobile.jpg](mockups/subpage--desktop-mobile.jpg) | Subpage (About as "WANTED" poster): desktop (left) and mobile (right) |

The mockups are AI-generated **concept art**, not pixel specs. Any text baked into them is a placeholder. Where a mockup and a spec file disagree, the spec wins. Known mockup artifacts:
- The mobile nav drops "Life & Faith". The real nav always has all five links.
- The mobile home shows a "Professioal Posts" scroll. That's a typo and a merged prop; see 02-layout.md for the actual mobile stacking order.
- The scrollbar and body text on the desktop poster are illustrative only.

## Decisions log

| # | Decision | Source |
|---|---|---|
| D1 | Content is shown as **Western props** (trail signs, scrolls, notice board, polaroid), not floating UI cards | Mockups |
| D2 | Style is a **soft vintage hand-painted animation background**, not wild slapstick angles | Mockups |
| D3 | Layouts are separate **desktop 16:9** and **mobile portrait** compositions, not one scaled layout | Mockups |
| D4 | **No text baked into images.** All copy and nav is live HTML | 04-assets.md |
| D5 | The nav has five items: About, Music, Professional, Life & Faith, Violin Studio | Current site |
| D6 | Raster art = 2 backdrop plates only (Bronius generates them with Nano Banana); all props are SVG/CSS by Claude, with raster props as a fallback only if the styles clash | 07-art-production.md |
| D7 | The "Bronius" sign is a **toy**: a `<button>` that wobbles on every page. It is not a home link (the nav and the browser cover navigation) | Bronius |
| D8 | **Every subpage has its own poster header**, e.g. About "WANTED", Music "NOW PLAYING", Professional "HELP WANTED", Life & Faith "NOTICE", set in front matter | Bronius |
| D9 | **Document scroll everywhere.** The desktop board is a visual frame, not a scroll container | Bronius |
| D10 | Violin Studio **stays external**. Off-site links get a visual cue: body links use a classic `::after` external-link glyph, and main-nav links get a more playful Western treatment (e.g. a "no turning back!" style tag or icon) | Bronius |

## Open questions

None open. All five original questions are resolved (D6–D10).

Still to design: the exact Western off-site treatment for nav links (D10). Claude will propose 2–3 options in the theme skeleton.
