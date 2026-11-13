# 06 — Architecture (PROPOSAL, under discussion)

## Recommendation
**Keep Jekyll on classic GitHub Pages, drop `minima`, and own an in-repo theme.** Use plain modern CSS with no Sass and no bundler, plus one small ES module for the sign.

Why this works:
- The content model (≈6 pages + posts, all markdown) is exactly what Jekyll is good at. Nothing in the design needs components, client-side routing or islands.
- Modern CSS covers what Sass used to: custom properties, native nesting, `@layer`, `clamp()` and container queries. So the GitHub Pages limits (Jekyll 3.10, plugin whitelist, old libsass) stop mattering.
- There's no build to maintain: push markdown, Pages builds it, and there are zero CI minutes and zero lockfile rot.
- The only thing Pages can't do is an image pipeline. That's a one-off offline encode of about 6 plates (04-assets.md), so it doesn't justify a build system.

**Escape hatch:** if we later want Jekyll 4, `jekyll-picture-tag` or any non-whitelisted plugin, add one `actions/deploy-pages` workflow. The content and theme stay unchanged.

## File layout
```
_config.yml                  nav via _data, minima removed
_data/
  nav.yml                    the 5 nav items (replaces header_pages)
  home.yml                   home props: type, title, url, teaser
_layouts/
  base.html                  <head>, scene, sign, nav, {{ content }}
  home.html                  extends base: props grid from _data/home.yml
  page.html                  extends base: board + poster wrapping {{ content }}
  post.html                  extends page
_includes/
  head.html                  meta, preload hints, single CSS link, SEO
  scene.html                 <picture> backdrop + porch frame (aria-hidden)
  sign.html
  nav.html
  props/
    trail-sign.html  plank-sign.html  note.html
    scroll.html      board.html       polaroid.html
  css/                       CSS partials, concatenated by Liquid
    tokens.css  reset.css  scene.css  sign.css  nav.css
    props.css   poster.css  board.css  utilities.css
assets/
  css/site.css               front-matter file that {% include %}s css/* inside @layer blocks; one request, zero tooling
  js/sign.js                 ES module, ~1 KB, deferred
  js/flickr.js               existing live-refresh logic, ported
  img/                       encoded AVIF/WebP plates + SVGs
  fonts/                     rye.woff2, lora-*.woff2 (subset)
redesign/                    specs + mockups (excluded from build)
```

Per-page front matter selects the poster's header and art:
```yaml
layout: page
title: About
poster:
  header: WANTED
  subhead: BRONIUS MOTEKAITIS
  art: violin-lantern      # → _includes/art/violin-lantern.svg
```

## CSS layering
```css
@layer reset, tokens, scene, components, utilities;
```
Cascade order is explicit, so specificity fights don't happen. Components get one partial each with BEM-ish class names (`.poster`, `.poster__header`, `.prop--trail`).

## Performance budget
| Metric | Target |
|---|---|
| First-load transfer (home, mobile) | ≤ 350 KB |
| LCP (backdrop) | ≤ 1.8 s on 4G |
| CLS | 0. Every image has intrinsic dimensions and fonts use `size-adjust` fallbacks |
| JS | ≤ 5 KB, nothing render-blocking |
| Third-party requests on load | 0 (self-hosted fonts, Flickr only on interaction or idle) |

Techniques: `<link rel=preload as=image imagesrcset=… fetchpriority=high>` for the backdrop, preloading the display font, and `content-visibility: auto` on below-fold props on mobile.

## Migration
1. Scaffold the theme on the `redesign` branch with flat placeholder colors instead of art. Get the structure, semantics and a11y right first.
2. Port the pages' front matter and content. Retire the `minima` overrides (`_includes/header.html`, `head.html`, `css/*`).
3. Drop in art plates as they're produced.
4. Lighthouse and axe pass, then merge to `main`.
