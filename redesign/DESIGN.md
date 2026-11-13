# Bronius.com Redesign — Design

The core structure of bronius.com centers on a clean navigation menu, an introductory statement, and three main life pillars—Music, Professional, and Life & Faith—followed by recent posts and a Flickr photo stream.

Website Elements Mapped to Your Scene
Top Hanging Wooden Sign. Displays "Bronius" suspended by ropes from the porch overhang at the top center of the frame.
Cloud Header Navigation. Soft, stylized clouds floating in the upper sky holding the five main links: About, Music, Professional, Life & Faith, and Violin Studio.
Center Content Area. The dusty main street and open vista between the left and right wooden buildings, framing the intro text, the three main sections (Music, Professional, Life & Faith), and recent posts.
Porch Perspective. Wooden porch pillars, overhanging eaves, and floorboards framing the foreground edges as if you just stepped outside into a small Texas one-horse town.
Before I generate the concept image and finalize your reusable prompt, please share a few details on:
How the center content should appear (rendered as readable UI text cards floating over the street, or illustrated as Western props like wooden trail signs, wanted posters, and storefront placards?)
The Tex Avery style intensity (classic 1940s exaggerated cartoon slapstick with wild angles and expressive characters, or a softer vintage hand-painted animation background look?)
Aspect ratio and layout (a wide 16:9 desktop webpage mockup, or a taller 4:3/vertical scroll view?)


## Design Concept
see design mockups in ./mockups folder containing side-by-side website UI mockups for home (redesign/mockups/image_8da82c02.jpg) and subpage (redesign/mockups/image_d3474d18.jpg) comparing a wide desktop layout (left) and a narrow vertical mobile layout (right), rendered in a classic 1940s Tex Avery Droopy Western cartoon background style. Hand-inked dark outlines, warm sepia, ochre, and dusty desert tones, subtle cel-painted watercolor grain, and exaggerated cartoon perspective. First-person perspective standing on a rustic wooden porch looking out onto a quiet, one-horse Texas old West main street with weathered wooden saloons and false-front buildings flanking the left and right edges, and open desert mesas on the horizon. At the top center of the wooden porch overhang, a rough-hewn wooden plank sign reading "Bronius" hangs suspended by two thick ropes. Directly beneath the sign, soft stylized cartoon clouds float in the warm sky holding the navigation links ("About", "Music", "Professional", "Life & Faith", "Violin Studio") in crisp dark serif type.

## Content Modes:

### Home View: Scattered wooden trail signs, parchment scrolls, a weathered notice board, and a pinned Polaroid-style photo frame float across the dusty street to display site sections.


### Subpages

#### Subpage View (Desktop Left):

A large, multi-plank weathered wooden bulletin board mounts to the right porch post, leaving the town street visible to the left. Pinned to the board with iron nails is a deckle-edged sepia parchment sheet featuring a bold slab-serif Western header ("WANTED"), hand-inked spot illustrations (violin and lantern), readable dark-ink serif body copy, and a stylized wooden scrollbar along the right frame.

#### Subpage View (Mobile Right)

Beneath the hanging "Bronius" sign and cloud menu, the deckle-edged sepia parchment sheet expands edge-to-edge across the viewport width, scrolling cleanly over the fixed town background with small peeks of the wooden porch boards at the top and bottom.


## Asset Architecture: Raster Graphics vs. Vectors & Live DOM
To keep the site sharp across retina screens, fast-loading, and interactive, split the artwork into layered assets rather than one giant background image.
Layer / Element	Format	Implementation Notes
Town Street, Sky & Porch Frame	Raster (WebP / AVIF)	Export at 2x resolution with separate desktop (16:9) and mobile (9:16) crops. Use background-attachment: fixed (or a position: fixed layer) so content scrolls over it.
Hanging "Bronius" Sign & Ropes	Inline SVG or Transparent PNG	Keep isolated from the porch roof so CSS/JS can rotate it around the top rope anchor points (transform-origin: top center).
Clouds & Porch Notice Board	Transparent PNG / WebP	Use border-image (9-slice) on the wooden notice board so its height adapts cleanly to different desktop viewport heights without stretching the wood grain.
Parchment Sheet & Nail Heads	CSS + SVG Filter / Data-URI	Render the parchment background with CSS gradients and a subtle SVG turbulence noise filter, plus inline SVG nail heads pinned to the top corners.
Navigation, Headers & Body Copy	Live HTML + Web Fonts	Never bake text into images. Pair a Western slab-serif display font (e.g., Rye or Alfa Slab One) with a readable editorial serif (e.g., Lora or Merriweather).
Spot Vignettes & Scrollbar Arrows	Inline SVG	Hand-inked violin/lantern icons and custom scrollbar track buttons scale infinitely with zero blur.
Interaction & Physics Specification
Idle Gentle Breeze: The hanging "Bronius" sign runs a continuous, low-amplitude harmonic oscillation (± 1.5°) on a slow 6-second cycle so the porch feels alive.
Click / Tap Wobble Impulse: Clicking or tapping the sign injects angular velocity into a damped spring-pendulum simulation. Instead of a stiff CSS keyframe reset, a lightweight requestAnimationFrame physics loop adds momentum to the current angle, creating a snappy wooden clatter and realistic decay back to the idle sway.
Desktop Viewport Scroll: On desktop subpages, the outer town scene remains locked while the .parchment-scroll container inside the wooden notice board scrolls independently via overflow-y: auto with custom -webkit-scrollbar and scrollbar-color styling.
Mobile Native Scroll: Below 768px, the wooden board frame disappears, the parchment sheet spans 100vw, and standard document scrolling moves the sheet smoothly over the fixed town backdrop.


Streamlined HTML / CSS / JS Starter
html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Bronius Motekaitis</title>
<link href="https://googleapis.com" rel="stylesheet">
<style>
  :root {
    --ink: #2b1d12;
    --parchment: #f3e4c8;
    --parchment-edge: #d9be94;
    --wood-dark: #4a2e18;
    --wood-mid: #7a4e2d;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: 'Lora', Georgia, serif;
    color: var(--ink);
    background: #d8a468 url('town-desktop.webp') center/cover fixed no-repeat;
    min-height: 100vh;
    overflow-x: hidden;
  }

  /* Hanging Wooden Sign */
  .sign-anchor {
    position: fixed;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    z-index: 20;
    cursor: pointer;
    user-select: none;
    transform-origin: 50% 0%;
    will-change: transform;
  }

  .sign-board {
    margin-top: 24px;
    padding: 10px 36px;
    background: var(--wood-mid);
    border: 3px solid var(--ink);
    border-radius: 6px;
    box-shadow: 0 8px 16px rgba(0,0,0,0.35);
    font-family: 'Rye', serif;
    font-size: clamp(1.8rem, 3.5vw, 2.8rem);
    color: var(--ink);
    position: relative;
  }

  /* Ropes */
  .sign-anchor::before, .sign-anchor::after {
    content: "";
    position: absolute;
    top: 0;
    width: 6px;
    height: 28px;
    background: repeating-linear-gradient(45deg, #c99e67, #c99e67 4px, #6e4c23 4px, #6e4c23 8px);
    border: 2px solid var(--ink);
  }
  .sign-anchor::before { left: 22%; }
  .sign-anchor::after { right: 22%; }

  /* Cloud Navigation */
  .cloud-nav {
    position: fixed;
    top: 105px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 15;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 14px 22px;
    padding: 12px 28px;
    background: rgba(255, 249, 238, 0.92);
    border: 2px solid var(--ink);
    border-radius: 999px;
    box-shadow: 0 4px 10px rgba(43, 29, 18, 0.2);
  }

  .cloud-nav a {
    text-decoration: none;
    color: var(--ink);
    font-weight: 600;
    font-size: 0.95rem;
  }

  /* Desktop Porch Notice Board Viewport */
  .notice-board {
    position: fixed;
    top: 175px;
    right: 6vw;
    width: min(560px, 52vw);
    bottom: 48px;
    background: var(--wood-dark);
    border: 4px solid var(--ink);
    border-radius: 8px;
    padding: 18px;
    box-shadow: -10px 12px 24px rgba(0,0,0,0.45);
    z-index: 10;
  }

  .parchment-sheet {
    height: 100%;
    background: radial-gradient(circle at center, var(--parchment) 65%, var(--parchment-edge) 100%);
    border: 2px solid var(--ink);
    padding: 28px 32px;
    overflow-y: auto;
    position: relative;
    line-height: 1.65;
  }

  /* Stylized Western Scrollbar */
  .parchment-sheet::-webkit-scrollbar { width: 14px; }
  .parchment-sheet::-webkit-scrollbar-track {
    background: var(--wood-dark);
    border-left: 2px solid var(--ink);
  }
  .parchment-sheet::-webkit-scrollbar-thumb {
    background: var(--wood-mid);
    border: 2px solid var(--ink);
    border-radius: 4px;
  }

  .wanted-title {
    font-family: 'Rye', serif;
    font-size: clamp(2rem, 4vw, 3.2rem);
    text-align: center;
    letter-spacing: 0.06em;
    margin-bottom: 4px;
  }

  .wanted-sub {
    font-family: 'Rye', serif;
    font-size: 1.1rem;
    text-align: center;
    margin-bottom: 18px;
  }

  /* Mobile Full-Viewport Sheet */
  @media (max-width: 768px) {
    body {
      background-image: url('town-mobile.webp');
      padding-top: 175px;
      padding-bottom: 40px;
    }
    .notice-board {
      position: static;
      width: 100%;
      border-left: none;
      border-right: none;
      border-radius: 0;
      padding: 0;
      background: transparent;
      box-shadow: none;
    }
    .parchment-sheet {
      height: auto;
      overflow-y: visible;
      border-left: none;
      border-right: none;
      padding: 24px 20px;
    }
  }
</style>
</head>
<body>

  <div class="sign-anchor" id="broniusSign" role="button" tabindex="0" aria-label="Bronius wooden sign">
    <div class="sign-board">Bronius</div>
  </div>

  <nav class="cloud-nav" aria-label="Main Navigation">
    <a href="#about">About</a>
    <a href="#music">Music</a>
    <a href="#professional">Professional</a>
    <a href="#life-faith">Life &amp; Faith</a>
    <a href="#violin">Violin Studio</a>
  </nav>

  <main class="notice-board">
    <article class="parchment-sheet">
      <h1 ABOUT
      <p class="wanted-sub">BRONIUS MOTEKAITIS</p>
      <p><strong>A man of God, a family man, a musician, an artist, an IT professional, and an aspiring product manager.</strong></p>
      <p style="margin-top: 14px;">Growing up in College Station, Texas, I have always wanted to know how the people around me experience the world: what is hard, what opens doors, what builds confidence, and what makes ordinary life better.</p>
    </article>
  </main>

<script>
  // Damped spring-pendulum physics with continuous idle breeze
  const sign = document.getElementById('broniusSign');
  let angle = 0;
  let velocity = 0;
  let lastTime = performance.now();

  const stiffness = 18;   // Rope tension
  const damping = 1.6;    // Air/rope friction

  function kickSign(impulse = 28) {
    // Alternate or amplify direction for playful Tex Avery wobble
    const dir = velocity >= 0 ? 1 : -1;
    velocity += impulse * dir;
  }

  sign.addEventListener('click', () => kickSign(32));
  sign.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      kickSign(32);
    }
  });

  function animateSign(now) {
    const dt = Math.min((now - lastTime) / 1000, 0.05);
    lastTime = now;

    // Gentle idle breeze target angle (-1.4 deg to +1.4 deg)
    const idleTarget = Math.sin(now * 0.0011) * 1.4;

    // Hooke's law toward idle target + velocity damping
    const force = -stiffness * (angle - idleTarget) - damping * velocity;
    velocity += force * dt;
    angle += velocity * dt;

    sign.style.transform = `translateX(-50%) rotate(${angle.toFixed(3)}deg)`;
    requestAnimationFrame(animateSign);
  }

  requestAnimationFrame(animateSign);
</script>
</body>
</html>
