# Cosmic Journey — 13.8 Billion Years Interactive 3D Visualization

A single-file interactive Three.js (r128) visualization of the entire history of the universe, from the Big Bang to the present day.

## Quick Start

Open `index.html` in any modern browser. No build step, no dependencies to install — Three.js loads from CDN.

## Controls

- **▶ Begin Journey** — auto-play through 13.8 billion years
- **🌍 Earth View** — jump to present day, Earth-centered vantage
- **◀◀ Restart** — reset to Big Bang
- **Timeline bar** — click/drag to scrub to any era
- **Mouse drag** — orbit camera
- **Scroll wheel** — zoom in/out
- **Click [brackets]** — enter immersive view of any highlighted object
- **Speed slider** — 1×–10× playback speed

## Architecture

### Single HTML File (~130KB)
All code is in `index.html`: HTML structure, CSS, and JavaScript in one `<script>` block.

### Core Systems

| System | Description |
|--------|-------------|
| `animT` (0→1) | Master timeline parameter driving everything |
| `SG{}` (Scene Groups) | Each era is an `addSG()` group that fades via `sceneFade()` |
| `KF_P/KF_C` | 9-keyframe particle system interpolating positions and colors |
| `CLKB[]` | Clickable object registry with 2D bracket overlay |
| `cosmicS` | Dynamic cosmic scale factor — objects move outward as universe expands |
| `oR` | Observable universe sphere radius — tracks content tightly |
| `camCenter` | Camera orbit center shifts from MW (origin) to solar system |
| `ensureObjScene()` | Lazy-built immersive scenes for 30+ clickable objects |

### Scene Pipeline

```
frame() → updateScenes(animT) → updateCamera() → renderer.render() → draw2D() → updateUI()
```

Each frame:
1. `animT` interpolates toward `targetT`
2. `updateScenes` sets visibility, runs animFns, computes `cosmicS` and `oR`
3. Scene groups scale with `cosmicS` (objects move outward)
4. Camera orbits `camCenter` at radius `defCamR` (interpolated from TL keyframes)
5. 2D overlay draws brackets, labels, and dynamic legend

## File Structure

```
cosmic-journey-repo/
├── index.html              # Complete visualization (single file)
├── README.md               # This file
└── docs/
    ├── TIMELINE.md          # All 15 eras with aT ranges
    ├── EVENTS.md            # All 33 events with views
    ├── CALCULATIONS.md      # Scale math, oR formula, cosmicS
    ├── SCENES.md            # Scene group architecture
    ├── IMMERSIVE_VIEWS.md   # All 25+ immersive scene descriptions
    └── REQUIREMENTS.md      # Original 21-item specification
```

## Technology

- **Three.js r128** (CDN)
- **Canvas 2D overlay** for labels, brackets, legend
- **No frameworks** — vanilla JS, no build tools
- **~130KB** total (uncompressed)

## License

Educational / demonstration project.
