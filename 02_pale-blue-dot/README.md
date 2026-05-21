# Pale Blue Dot
### A Fractal Descent Through the Cosmos — Observable Universe to Earth

An interactive 3D cosmological visualization built with Three.js descending through 8 zoom levels — from the Observable Universe to Earth — with real physics, accurate orbital mechanics, and named objects at every scale. Includes a companion narrative GIF for standalone sharing.

---

## Quick Start

```bash
open index.html
# or:
npx serve .         # → http://localhost:3000
python3 -m http.server 8080
```

No build step. No npm install. Three.js r128 loaded from cdnjs.

---

## The 8 Levels

| # | Name | Scale | Key objects |
|---|------|-------|-------------|
| 0 | Observable Universe | ~93 Gly | Cosmic web, 4 voids, 9 supercluster nodes |
| 1 | Laniakea Supercluster | ~520 Mly | Great Attractor, galaxy streams |
| 2 | Local Group | ~3 Mly | Milky Way, Andromeda, Triangulum, 6 dwarfs |
| 3 | Milky Way Galaxy | ~100 kly | 4 spiral arms, Sgr A*, bulge, halo |
| 4 | Orion Arm / Local Bubble | ~1 kly | 14 named nearby stars |
| 5 | Solar System | ~100 AU | 8 planets, true 3D Keplerian orbits, ecliptic plane, spin axes |
| 6 | Earth–Moon | ~800,000 km | Earth, Moon, ISS, 5 Lagrange points |
| 7 | Pale Blue Dot | — | Sagan quote, Voyager 1 facts |

**Navigate**: drag to orbit · scroll to zoom · click gold-labelled objects to descend · click any level in the left sidebar to jump directly.

---

## Solar System — True 3D Keplerian Orbits

Full J2000 orbital elements from JPL DE430 per planet:
- **i** — inclination, **Ω** — ascending node, **ω** — argument of perihelion

`keplerPos(a, i, Ω, ω, θ)` applies the complete 3D rotation matrix. Every planet occupies a unique orbital plane. The ecliptic reference grid, spin axes on each planet, and orbital plane patches make the geometry immediately legible. All planets are within 7° of the ecliptic — this is physically correct (angular momentum conservation from the protoplanetary disk).

---

## Repository Structure

```
pale-blue-dot/
├── index.html                      # Full visualization (68KB, self-contained)
├── README.md / LICENSE / CHANGELOG.md
├── package.json / .gitignore
├── assets/
│   ├── pale_blue_dot_showcase.gif  # Narrative showcase GIF (1.5MB)
│   └── data/
│       ├── planets.json            # JPL DE430 orbital elements
│       ├── stars.json              # HYG/Gaia nearby star catalog
│       └── clusters.json          # NED galaxy clusters & voids
├── docs/
│   ├── PHYSICS.md                  # All equations: Kepler, Lagrange, ΛCDM
│   ├── LEVELS.md                   # Per-level object catalog with citations
│   ├── ARCHITECTURE.md             # Code structure, extension guide
│   └── COSMOLOGY.md                # Scientific background, reading list
├── scripts/
│   └── generate_gif.py             # Narrative GIF generator (matplotlib)
└── src/js/physics/
    ├── scale-constants.js          # Physical constants as ES module
    ├── orbital-mechanics.js        # Kepler, vis-viva, escape velocity
    └── lagrange.js                 # Full L1–L5 calculator + Routh stability
```

---

## GIF (`assets/pale_blue_dot_showcase.gif`)

5-scene narrative, 132 frames, 12fps, ~11s, 1.5MB:
1. Observable Universe — cosmic web, voids, Laniakea "you are here"
2. Milky Way — spiral arms, Sgr A*, Sun annotated
3. Solar System — Keplerian orbits, spin axes, Saturn rings, camera revealing disk geometry
4. Earth-Moon — live Moon orbit, ISS path, Lagrange points
5. Pale Blue Dot — diffuse sunbeam, dot appears, Sagan's quote fades in line by line

Regenerate: `python3 scripts/generate_gif.py`

---

## Data Sources

Planck 2018 · JPL DE430 · HYG Database v3 · Gaia DR3 · NED · Tully et al. 2014 (Laniakea) · Zucker et al. 2022 (Local Bubble) · Reid et al. 2019 (BeSSeL)

---

## License

MIT — see `LICENSE`. Inspired by Carl Sagan, *Pale Blue Dot* (1994).
