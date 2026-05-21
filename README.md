# cosmic-truths

Four interactive visualizations that attempt to make the scale, history, and loneliness of the universe *felt* rather than just known.

---

## Why this exists

There's a difference between knowing the universe is 13.8 billion years old and *feeling* what that means — watching quarks become atoms become stars become you, and understanding that this chain of emergence is the most improbable thing that has ever happened.

There's a difference between knowing the observable universe is 93 billion light-years across and *feeling* the vertigo of drilling down from supercluster filaments to a single pale blue pixel, forty orders of magnitude below where you started.

There's a difference between knowing the expansion of space is accelerating and *feeling* what it means that the night sky is slowly going dark — that in 150 billion years, the Local Group will be an island of light in an infinite, empty void, and every other galaxy will have redshifted into nothing.

These four projects are attempts to close those gaps. They are not textbooks. They are instruments for awe.

---

## The four parts

### Part 1 — Ladder of Complexity
**A 3D matrix of emergent complexity across scale, time, and integration.**

Maps the universe's hierarchy of structure — quarks → atoms → molecules → cells → organisms → societies → civilizations — onto three axes:

| Axis | What it measures | Scale |
|------|-----------------|-------|
| **x** | Physical scale | Log, femtometers to megaparsecs |
| **y** | Time of first appearance | Big Bang to present |
| **z** | Integration | Number of distinct sub-components cooperating |

Each node is a layer of complexity. Each edge is an emergence event — a jump where new properties appear that were not predictable from the layer below. The 3D rotation reveals that these jumps cluster at strange inflection points, not evenly in time or scale. The "complexity frontier" is a curve in this space, and we are on it. Everything beyond it is unknown possibility space.

### Part 2 — Pale Blue Dot
**A fractal particle simulator spanning 40 orders of magnitude.**

A drill-down level-of-detail system where each click doesn't just zoom — it loads a new universe of things that were invisible before:

```
Great Attractor → Laniakea Supercluster → Virgo Cluster → Local Group
→ Milky Way → Orion Arm → Local Bubble → Solar System → Earth-Moon
```

The honest challenge: the ratio from the Milky Way to the Solar System is 1:10⁹. You cannot represent that at pixel resolution. The approach is to make the ratio *felt* — at supercluster scale, particles are galaxies drifting in dark matter filaments; at solar system scale, they're planets on Keplerian orbits. Same physics engine, completely different universes of structure, separated by nothing but a click.

### Part 3 — The Loneliness Physics
**A cosmological horizon simulation showing the universe going dark.**

The most emotionally resonant piece. The physics:

- The Hubble constant (~70 km/s/Mpc) means any galaxy beyond ~14 billion light-years is already receding faster than light
- That horizon is shrinking
- In ~150 billion years, the Local Group will be the only thing visible
- Everything else will have redshifted into invisibility

The simulation shows:
- The observable universe as a sphere with you at center
- Light cones — what we can see now, what we could theoretically reach, what is already gone forever
- The Hubble flow — every galaxy receding, the rate accelerating
- The "cosmic loneliness" trajectory: the shrinking of the observable horizon in real time

The key physical intuition this makes visceral: we're not moving through space away from other galaxies. Space itself is expanding between us. A photon fired at Andromeda today will arrive. A photon fired at a galaxy 20 Mpc away will also arrive, eventually. But a photon fired at anything beyond ~46 billion light-years can never arrive — even traveling at *c* forever — because the space it must cross is growing faster than it can traverse it.

### Part 4 — Cosmic Timeline
**13.8 billion years as an interactive 3D journey. The one we built.**

A single-file Three.js visualization that plays through every major epoch of cosmic history:

```
Big Bang → Inflation → QGP → Protons → Nucleosynthesis → CMB → Dark Ages
→ First Stars → Supernovae → Pulsars → Black Holes → First Galaxies
→ Quasars → Sgr A* Accretion → Milky Way Formation → Local Group
→ Orion Arm → Solar Nebula → Sun Ignition → Planets → Earth → Moon
→ Present Day
```

Core mechanics:
- **`animT` (0→1)** drives the entire 13.8 Gyr timeline
- **Dynamic cosmic expansion**: early content is compact, then physically moves outward as the universe grows, clearing room for the Milky Way to form at the center
- **Scale transitions**: camera orbits shift from universe scale (camR=350) through galaxy scale (camR=288) to solar system scale (camR=25) to Earth neighbourhood (camR=6)
- **Nothing disappears**: all 12 scene groups persist to the end — pulsars, black holes, quasars, galaxies all remain visible, spread across the expanded universe
- **33 clickable events** with 25+ immersive deep-dive scenes (supernova explosions, pulsar jets, BH accretion disks, galaxy collisions, solar system orbits)
- **12 local group galaxies** in physically motivated positions

See `part4-cosmic-timeline/` for full documentation:
- `docs/CALCULATIONS.md` — all formulas (oR, cosmicS, gwS, scale ratios)
- `docs/TIMELINE.md` — 15 eras with aT ranges
- `docs/EVENTS.md` — 33 events with routing
- `docs/SCENES.md` — scene architecture + immersive views
- `docs/REQUIREMENTS.md` — 21-item spec with status
- `docs/LOCAL_GROUP.md` — galaxy positions and real distances

---

## Repo structure

```
cosmic-truths/
├── README.md                          # This file
├── part1-ladder-of-complexity/        # 3D complexity matrix
├── part2-pale-blue-dot/               # Fractal particle drill-down
├── part3-loneliness-physics/          # Cosmological horizon sim
└── part4-cosmic-timeline/             # 13.8 Gyr interactive journey
    ├── index.html                     # The visualization (~130KB, self-contained)
    ├── README.md                      # Quick start + controls
    └── docs/
        ├── CALCULATIONS.md
        ├── EVENTS.md
        ├── LOCAL_GROUP.md
        ├── REQUIREMENTS.md
        ├── SCENES.md
        └── TIMELINE.md
```

## Technology

All four parts are designed as self-contained browser experiences:
- **Three.js r128** for 3D rendering (CDN, no install)
- **Canvas 2D** for overlays, labels, UI
- **Vanilla JavaScript** — no frameworks, no build tools
- **Single HTML files** — open in browser, that's it

## The thread connecting them

These four pieces are not separate projects. They are four views of the same truth:

1. **Ladder** asks: *how did simple things become complex things?*
2. **Pale Blue Dot** asks: *where are we in all of this?*
3. **Loneliness** asks: *what happens to all of this?*
4. **Timeline** asks: *what did it look like along the way?*

Together they form a complete arc — from the emergence of structure, through our place in it, to its ultimate fate, told through the specific history that got us here. The universe made atoms, atoms made stars, stars made heavier atoms, heavier atoms made planets, planets made chemistry, chemistry made life, life made minds, and minds made these four visualizations trying to understand the whole chain. That recursion is the point.
