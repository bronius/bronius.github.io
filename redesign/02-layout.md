# 02 — Layout

Reference: `mockups/home--desktop-mobile.jpg`, `mockups/subpage--desktop-mobile.jpg`.

## Breakpoints
| Name | Range | Composition |
|---|---|---|
| mobile | `< 768px` | Portrait plate, single column, document scroll |
| desktop | `≥ 768px` | 16:9 plate, props spread across the street |

Use one breakpoint to start. Add a "wide" tweak (≥ 1440px) only if the art needs it.

## Persistent chrome (all pages)
In DOM order, which is also the reading order:
1. **Sign** "Bronius": fixed at top center, hanging from the overhang. See 05-interaction.md.
2. **Cloud nav:** directly below the sign. Desktop shows one row of five links. Mobile wraps to 2 rows (3 + 2) and must still show all five (D5).
3. **Backdrop:** fixed and decorative (`aria-hidden`). Content scrolls over it.

## Home
Content mapping from the current site:

| Slot | Prop | Content |
|---|---|---|
| Intro | Parchment scroll, centered under nav | "I try to live a life where faith, family, music, work, and community fit together" |
| Pillar 1 | Arrow trail sign | **Music** → `/music/` |
| Pillar 2 | Plank sign | **Professional** → `/professional/` |
| Pillar 3 | Pinned parchment note with a teaser line | **Life & Faith** → `/life/` |
| Posts | Dark notice board | **Recent Posts** (latest N from `_posts`) |
| Photo | Pinned polaroid | **Random Flickr Photo** (existing live-refresh behavior) |

**Desktop:** the intro sits at center. The three pillars sit in a row across the mid-street at slightly varied heights and tilts. Posts and Photo sit in a lower row, left of center and right of center.

**Mobile:** a single column in this order: Intro → Music → Professional → Life & Faith → Recent Posts → Photo. Props are full-width minus a gutter, and their tilts shrink to roughly ±1°.

## Subpage (About, Music, Professional, Life & Faith)
**Desktop:** a large multi-plank wooden notice board mounted on the right porch post, about 45–55% of viewport width, so the street stays visible on the left. A deckle-edged parchment poster is nailed to it, containing:
- a slab-serif header (e.g. "WANTED"; see open question 2)
- a subhead (e.g. "BRONIUS MOTEKAITIS")
- an optional framed spot illustration
- body copy from the page's markdown

**Mobile:** the board frame disappears. The parchment runs edge to edge (100% width) beneath the sign and nav, with small peeks of porch boards above and below. Document scroll.

## Semantics
```
body
├─ div.scene[aria-hidden]   backdrop + porch frame (decorative)
├─ header
│   ├─ button.sign           toy, wobble only (D7)
│   └─ nav[aria-label=Main]  cloud nav
└─ main
    ├─ home:    section × N  (each prop = one section with heading)
    └─ subpage: article.poster  h1 = page title
```
