// bronius.com: hanging sign (spring + drag), Escape-to-home, subpage focus. ES module, deferred by default.
// Physics: damped spring-pendulum θ'' = -kθ - cθ' (redesign/05-interaction.md).

const HOME = document.querySelector('.sign__body')?.getAttribute('href') ?? '/';
const isHome = document.body.hasAttribute('data-home');
const reduce = matchMedia('(prefers-reduced-motion: reduce)');
const KICK_KEY = 'sign-kick';

// ---- Subpage: focus the poster heading on arrival (D12); Escape closes back home. ----
if (!isHome) {
  const h = document.querySelector('.poster__header');
  if (h && !location.hash) h.focus({ preventScroll: true });
  addEventListener('keydown', e => {
    if (e.key !== 'Escape' || e.defaultPrevented || e.isComposing) return;
    if (e.target.closest?.('input, textarea, select, [contenteditable]')) return;
    location.href = HOME;
  });
}

// ---- Sign: click kicks + goes home (on home: kick only). Drag swings within ±MAX; release flings. ----
const signWrap = document.querySelector('.sign');
const sign = document.querySelector('.sign__body');
if (sign) {
  const K = 18, C = 1.6, IMPULSE = 34, EPS = 0.01;
  const MAX = 12, MAX_OMEGA = 160, DRAG_SLOP = 6;   // deg, deg/s, px
  let theta = 0, omega = 0, last = 0, running = false, drag = null, swallowClick = false;
  const clamp = (v, m) => Math.max(-m, Math.min(m, v));
  const paint = () => { sign.style.transform = theta ? `rotate(${theta.toFixed(3)}deg)` : ''; };

  function step(now) {
    if (drag?.moved) { running = false; return; }          // the hand owns the sign
    const dt = Math.min((now - last) / 1000, 0.05);
    last = now;
    omega += (-K * theta - C * omega) * dt;
    theta += omega * dt;
    paint();
    if (Math.abs(theta) < EPS && Math.abs(omega) < EPS) { theta = omega = 0; paint(); running = false; return; }
    requestAnimationFrame(step);
  }
  const wake = () => { if (!running) { running = true; last = performance.now(); requestAnimationFrame(step); } };
  const kick = () => { if (reduce.matches) return; omega += IMPULSE * (omega >= 0 ? 1 : -1); wake(); };

  // Pivot = top-centre of the sign image (partly off-screen: the rope is cropped by --rope-crop).
  const pivot = () => ({ x: innerWidth / 2, y: parseFloat(getComputedStyle(signWrap).top) });
  // Angle of the pointer about the pivot; CSS rotate(+) is clockwise (moves the plank LEFT), hence the minus.
  const angleAt = (e, p) => -Math.atan2(e.clientX - p.x, e.clientY - p.y) * 180 / Math.PI;

  sign.addEventListener('pointerdown', e => {
    swallowClick = false;
    if (reduce.matches || e.button !== 0) return;
    const p = pivot();
    drag = { id: e.pointerId, p, a0: angleAt(e, p), t0: theta, x: e.clientX, y: e.clientY, moved: false, t: performance.now() };
  });
  sign.addEventListener('pointermove', e => {
    if (!drag || e.pointerId !== drag.id) return;
    if (!drag.moved) {
      if (Math.hypot(e.clientX - drag.x, e.clientY - drag.y) < DRAG_SLOP) return;
      drag.moved = true; omega = 0;
      sign.setPointerCapture(e.pointerId);
      sign.classList.add('is-dragging');
    }
    const now = performance.now(), prev = theta;
    theta = clamp(drag.t0 + angleAt(e, drag.p) - drag.a0, MAX);
    const dt = (now - drag.t) / 1000;
    if (dt > 0) omega = 0.6 * omega + 0.4 * ((theta - prev) / dt);  // smoothed release velocity
    drag.t = now;
    paint();
  });
  function release(e) {
    if (!drag || e.pointerId !== drag.id) return;
    if (drag.moved) {
      swallowClick = true;                                   // a drag is not a click
      omega = clamp(omega, MAX_OMEGA);
      sign.classList.remove('is-dragging');
      drag = null; wake();
    } else drag = null;
  }
  sign.addEventListener('pointerup', release);
  sign.addEventListener('pointercancel', release);           // e.g. the browser took over for a vertical pan
  sign.addEventListener('dragstart', e => e.preventDefault());

  sign.addEventListener('click', e => {
    if (swallowClick) { e.preventDefault(); swallowClick = false; return; }
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;   // new tab/window: leave it to the browser
    kick();
    if (isHome) e.preventDefault();                          // already home: just a wobble
    else try { sessionStorage.setItem(KICK_KEY, '1'); } catch {}    // carry the swing across the page load
  });

  // Arrived home via the sign: finish the kick here so the swing reads as continuous.
  try {
    if (isHome && sessionStorage.getItem(KICK_KEY)) { sessionStorage.removeItem(KICK_KEY); kick(); }
  } catch {}
}
