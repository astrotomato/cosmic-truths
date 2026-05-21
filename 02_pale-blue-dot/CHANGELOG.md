## [1.1.0] — Fixes & Improvements

### Fixed

**Boundary sphere visibility**
- Was using near-black colors (0x1a3a5c etc.) indistinguishable from the 0x010208 background
- Changed to visible cyan-blues (0x00b4d8, 0x60b0d0 per level)
- Added `renderOrder` 900–902 to guarantee render above particle fields
- Reduced to navigation-aid opacity: fill 0.012, wireframe 0.07, equatorial ring 0.30
- Sparse wireframe (10×8 segments) — reads as a hint, not a cage

**True 3D Keplerian orbital mechanics**
- Added full J2000 orbital elements per planet from JPL DE430: i, Ω (ascending node), ω (arg. perihelion)
- `keplerPos(a, i, Om, w, theta)` applies complete 3D rotation matrix (not just single-axis tilt)
- Every planet's orbital plane is now geometrically unique in ecliptic space
- Animation loop updated to use keplerPos for live planet positions

**Solar system scene geometry**
- Added ecliptic reference plane: concentric rings + radial spokes in y=0 plane
- Spin axes attached as children of planet meshes (follow planet through orbit)
- Orbital plane patches (tilted disc at planet) show each orbit's unique inclination
- Camera default changed to 36° elevation (PI/5) for legible 3D geometry
- Planet sphere axial tilts applied: Uranus 97.77°, Venus 177.4°, etc.
- Orbit lines: distinct per-planet colors at 0.55 opacity with line-of-nodes dashes
- Saturn rings updated with correct tilt

**Lagrange point positions**
- L1 was incorrectly at Moon's position; now at correct 0.85× Moon distance
- L2 at 1.17× Moon distance (beyond Moon)
- L4/L5 at proper equilateral triangle positions (60° ±, moonOrbitR)
- Each point has descriptive tooltip with stability and spacecraft notes

**Depth ladder navigation**
- Container had `pointer-events: none` blocking all clicks
- All non-active levels now directly navigable (no visited-state restriction)
- Uses `addEventListener` instead of `onclick` for reliable event handling

**GIF — complete rebuild**
- Previous version was a single rotating scene (no storytelling)
- New version: 5-scene narrative (Universe → Galaxy → Solar System → Earth → Pale Blue Dot)
- Voyager sunbeam: replaced solid `fill_betweenx` stripe with diffuse Gaussian scatter column
- Quote: Sagan's words fade in line by line in the final scene
- 132 frames, 12fps, ~11 seconds, 1.5MB

### Added

- `assets/pale_blue_dot_showcase.gif` — narrative showcase GIF
- `scripts/generate_gif.py` — full GIF generation script (matplotlib/Pillow)
- Ecliptic plane reference grid in solar system level
- Planet axial tilt indicators (spin axis lines as planet mesh children)
- Orbital plane patches per planet
- `keplerPos()` function with full Euler angle rotation
- Orbital inclinations for all 8 planets from JPL DE430

# Changelog

All notable changes to the Pale Blue Dot visualization.

---

## [1.0.0] — Initial release

### Added

**Core visualization**
- 8-level fractal descent: Observable Universe → Laniakea → Local Group → Milky Way → Orion Arm → Solar System → Earth-Moon → Pale Blue Dot terminal screen
- Three.js r128 3D rendering with orbit controls (manual implementation, no OrbitControls import)
- Level transitions with flash overlay and loading indicator
- Auto-rotation when idle; manual drag-to-orbit

**Navigation**
- Left sidebar depth ladder — click any level name to navigate directly
- In-scene clickable objects (glow sprites + mesh cores) as descent targets
- Back button (top right) to ascend one level
- Depth ladder shows visited (gold), active (blue), unvisited (dim) states

**Label system**
- DOM-based labels projected from 3D world positions to screen coordinates each frame
- Gold-coloured animated arrow on clickable targets
- Labels clip to screen bounds (hidden when behind camera or off-edge)
- Labels cleared and re-created on each level change

**Boundary sphere**
- Per-level glowing sphere marking the spatial extent of each zoom level
- LineLoop rings (zero-thickness) for equatorial and meridian circles
- `depthTest: false` on all elements — sphere remains visible when camera is inside it
- Distinct colour per level (steel blue tones)

**Level 0 — Observable Universe**
- 180 procedural cosmic web filaments with seeded RNG (seed 42)
- 4 major void spheres (Boötes, Sculptor, Eridanus, Capricornus)
- 9 named supercluster nodes with labels (Laniakea, Coma, Shapley, Hercules, etc.)
- 6,000 field galaxy particles with cosmological redshift colouring

**Level 1 — Laniakea Supercluster**
- 80 galaxy stream lines converging toward Great Attractor
- Great Attractor labelled as hidden behind galactic plane
- 8 named major galaxies with labels (Milky Way, Andromeda, Virgo Cluster, etc.)
- 80 procedural dwarf galaxy sprites

**Level 2 — Local Group**
- Procedural spiral galaxy renders for Andromeda (M31) and Triangulum (M33)
- Milky Way centre glow as descent target
- 6 named dwarf galaxies with labels (LMC, SMC, Sagittarius Dwarf, etc.)

**Level 3 — Milky Way Galaxy**
- 4 spiral arms rendered as procedural point clouds (Perseus, Orion, Sagittarius, Norma-Cygnus)
- Arm name labels on all four arms
- Sgr A* at galactic centre with label
- Galactic bulge particle cloud, halo particle cloud

**Level 4 — Orion Arm / Local Bubble**
- Local Bubble shell (wireframe sphere)
- ISM dust particle field (low opacity)
- 10 named nearby stars with real spectral types and distances:
  Sol, Proxima Cen, α Cen A/B, Sirius A, ε Eridani, τ Ceti, 40 Eri, Altair, Vega, Fomalhaut

**Level 5 — Solar System**
- All 8 planets on circular orbits with correct relative periods (Kepler's Third Law)
- Live orbit animation (planets moving each frame)
- Saturn ring geometry
- Per-planet labels with AU distance and orbital period
- Sun label
- Asteroid belt (1,500 particles, 2.2–3.2 AU)
- Kuiper belt (800 particles, 30–50 AU)
- Asteroid Belt and Kuiper Belt zone labels
- Camera default: near top-down (20° from vertical) so orbits read as flat/2D

**Level 6 — Earth-Moon System**
- Earth sphere with atmospheric glow
- Moon in live orbit (angle updated each frame)
- ISS orbital path with label
- 5 Lagrange points with accurate positions:
  - L1: 0.85× Moon distance (between Earth and Moon)
  - L2: 1.17× Moon distance (beyond Moon)
  - L3: opposite Earth from Moon
  - L4/L5: equilateral triangle positions (60° ahead/behind Moon)
- Lagrange point labels with description of each point's stability and use

**Level 7 — Pale Blue Dot terminal screen**
- Carl Sagan quote (full text)
- 3-pixel pale blue dot with glow
- 6 cosmic statistics
- Ascend button returning to Level 0

**Physics panel (all levels)**
- Level-specific fact sheet in right panel
- Scale bar showing 1 unit = N real units
- Narrative text describing each level

**Info system**
- Per-level info panel (right) with facts table, description, navigation hint
- Tooltip on hover showing object name and sub-label

**Data**
- `assets/data/planets.json` — Planetary orbital elements from JPL DE430
- `assets/data/stars.json` — 14 named nearby stars from HYG/HIPPARCOS/Gaia
- `assets/data/clusters.json` — Galaxy clusters, Local Group, voids from NED

**Documentation**
- `docs/PHYSICS.md` — Complete equation reference (orbital mechanics, Lagrange points, cosmology, stellar physics, simulation approximations)
- `docs/LEVELS.md` — Per-level object catalog with sources
- `docs/ARCHITECTURE.md` — Code structure, extension guide, performance notes
- `docs/COSMOLOGY.md` — Scientific narrative background and reading list

### Known issues / future work
- Orbital eccentricity not rendered (circular orbits only)
- Orbital plane inclinations omitted (all planets in y=0 plane)
- Earth/Moon/planets use solid colors, not texture maps
- Cosmic web filaments are procedural, not from SDSS survey data
- No WebXR support
- Moon glow sprite does not track Moon mesh during animation (static at initial position)
