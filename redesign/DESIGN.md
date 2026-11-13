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

## Open questions

1. **Sign semantics.** Should the "Bronius" sign be the home link (`<a href="/">`) that also wobbles, or a pure toy (`<button>`)? Proposal: link on subpages, wobble-only button on home.

A: Toy with wobble only.


2. **Poster headers per page.** The About page is "WANTED". Do the other subpages get their own headers (e.g. Music "NOW PLAYING", Professional "HELP WANTED", Life & Faith "NOTICE")?

A: Yes, you got it: Separate header for each.


3. **Desktop inner scroll vs. document scroll.** See 05-interaction.md §Scroll model. Proposal: use document scroll everywhere.

A: Agreed. document scroll.


4. **Violin Studio.** It currently links out to violinstudio.bronius.com. Keep it external, or skin it?

A: keep it. Add a small visual indication of going off-site for this and other off-site links in the main menu and elsewhere. Most body external links can have the traditional "external link" :content-after, but we can be a little more creative on main nav. maybe a simple, cowboy style "no turning back!" kind of imagery or text treatment.


5. **Artwork production.** Who makes the clean, text-free layered plates (backdrop, porch frame, sign, clouds, board)? See 04-assets.md.

A: more question: what do you mean by "who?"