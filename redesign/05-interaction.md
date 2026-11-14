# 05 — Interaction & Physics

## Hanging sign

> **Status (2026-11-14):** accepted as built in `reference/preview.html` (D7 revised). The sign is a home link, a click toy, and draggable. The idle sway and spring constants are unchanged. A deeper "feel" rework stays in the backlog.

### Idle breeze
A continuous low-amplitude sway (`--sway-amp` 1.2°, `--sway-period` 6s) via a **CSS keyframe animation on the outer wrapper** (`.sign`). It costs no JS, runs on the compositor, and is disabled by `prefers-reduced-motion`.

### Spring
The inner element (`.sign__body`, an `<a href="/">`) runs a **damped spring-pendulum**. Physics angle and idle sway compose through nested transforms.

```
θ̈ = −k·θ − c·θ̇        k = 18, c = 1.6, impulse = 34°/s
```
- Underdamped (critical damping would be `c = 2√k ≈ 8.5`). τ = 2/c ≈ 1.25 s.
- Integrate with semi-implicit Euler and clamp `dt ≤ 50 ms`. **The rAF loop runs only while there's energy** (stop at `|θ|, |θ̇| < 0.01`).

### Click
Kick (the impulse adds in the direction of travel), then follow the link. If already on home, `preventDefault()` and just kick. On the real site, navigating from a subpage is a page load, so the kick is cut short. That's fine. (Optional later: cross-document View Transitions.)

### Drag
- `pointerdown` records the pivot and start angle. The drag starts only after a **6px slop**, so taps stay clicks. Then `setPointerCapture` and add `.is-dragging` (cursor `grabbing`).
- **Pivot** = top-centre of the sign image: `x = innerWidth/2`, `y = computed top` of `.sign` (negative: the rope is cropped by `--rope-crop`).
- `θ = clamp(θ₀ + angle(pointer) − angle(start), ±12°)`, where `angle = −atan2(dx, dy)` (CSS `rotate(+)` is clockwise, so the minus sign makes the plank follow the hand).
- Release velocity = EMA of `Δθ/Δt` (0.6/0.4), clamped to ±160°/s, then hand off to the spring.
- **A drag swallows the following `click`**, so it never navigates.
- `touch-action: pan-y` on the sign: horizontal drags swing it, vertical pans still scroll. The browser sends `pointercancel` when it takes over a pan, and that's treated as a release. `draggable="false"`, `-webkit-user-drag: none`, `pointer-events: none` on the `<img>`, and `dragstart` is prevented.

### Keyboard & reduced motion
- It's a link, so Enter navigates. There's no toy key binding.
- Reduced motion: no sway, no kick, no drag. Click still navigates.

## Subpage close (D12)
- `<a class="poster__close" href="/" aria-label="Close, back to home"><span aria-hidden="true">X</span></a>`, absolutely positioned in the poster's top cap (`top: calc(100cqi * -.135); right: 15%`).
- **Escape** goes home from any subpage.
- On arrival at a subpage, focus the `<h1 tabindex="-1">` (`preventScroll`). In Jekyll this is a full page load, so only do it when coming from in-site navigation (or skip it, since the browser resets focus anyway).

## Scroll model

| Viewport | Behavior |
|---|---|
| mobile (< 768px) | The board frame disappears, parchment is full width, and **document scroll** moves it over the fixed backdrop. |
| desktop (≥ 768px) | **Spec as written:** the outer scene is locked, and `.poster` scrolls inside the board via `overflow-y: auto`, with a styled scrollbar (`scrollbar-color` + `::-webkit-scrollbar`). |

### Decision (D9): document scroll on desktop too
An inner scroll container traps the wheel (it scrolls only while the pointer is over the board), hides the page's scroll position from the browser, and needs extra care for keyboard and screen readers.

Alternative: keep the board frame `position: fixed` as a visual, and let the parchment column scroll with the document, clipped by a `mask-image` / `clip-path` window matching the board's inner edge. You get the same look with native scroll. (See open question 3 in DESIGN.md.)

If the inner scroll stays, the container needs `tabindex="0"`, `role="region"` and `aria-label` so keyboard users can scroll it.

## Fixed backdrop on iOS
`background-attachment: fixed` is ignored on iOS Safari. Use a `position: fixed; inset: 0` layer holding the `<img>` instead (see 04-assets.md).
