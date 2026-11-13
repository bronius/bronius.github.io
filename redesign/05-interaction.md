# 05 — Interaction & Physics

## Hanging sign

### Idle breeze
A continuous low-amplitude sway of `±1.5°` on a `6s` cycle, so the porch feels alive.

Implementation: a **CSS keyframe animation on an outer wrapper**. It costs no JS, runs on the compositor, and is trivially disabled by `prefers-reduced-motion`.

### Click/tap wobble
Clicking or tapping injects angular velocity into a **damped spring-pendulum** running on an **inner element**. Physics angle and idle sway compose through nested transforms, so neither has to know about the other.

```
θ̈ = −k·θ − c·θ̇        k ≈ 18 (rope tension), c ≈ 1.6 (friction)
```
- The system is underdamped (critical damping would be `c = 2√k ≈ 8.5`), so the sign swings several times and the amplitude decays with τ = 2/c ≈ 1.25 s. That's the snappy Tex Avery clatter.
- Each impulse adds to the current velocity in its direction of travel, so repeated taps pump the swing.
- Integrate with semi-implicit Euler and clamp `dt ≤ 50 ms` (to survive tab-switch stalls).
- **The rAF loop only runs while there's energy.** Stop when `|θ| < 0.01°` and `|θ̇| < 0.01°/s`, and restart on the next impulse. This avoids a forever-loop that drains battery.
- Keyboard: Enter or Space triggers the same impulse.
- Reduced motion: no idle sway and no wobble (or at most a single ≤ 2° nudge).
- Semantics: a `<button>` toy on every page, not a home link (D7).

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
