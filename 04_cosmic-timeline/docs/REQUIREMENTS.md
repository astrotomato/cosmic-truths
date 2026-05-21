# Original 21-Item Specification & Status

## The Vision

An interactive 3D journey through 13.8 billion years of cosmic history:
- Big Bang → particle era → first stars → galaxies → Milky Way → Solar System → Present
- Smooth camera zooms between scales (universe → galaxy → solar system → planet)
- Universe sphere expands; objects move outward creating room for MW formation
- Nothing disappears — all content persists and scales with cosmic expansion
- Clickable objects with immersive deep-dive views

## 21 Items

| #  | Requirement | Status | Implementation |
|----|------------|--------|----------------|
| 1  | Big Bang explosive expansion, inflation, 3-phase growth | ✅ | 3-phase oR formula, inflation glow, bigbang particles |
| 2  | QGP quarks/gluons colored (red/green/orange) | ✅ | colA vertex colors in particles IIFE |
| 3  | Protons forming (blue/grey/yellow) | ✅ | colB vertex colors |
| 4  | BBN H and He nuclei | ✅ | colC vertex colors |
| 5  | CMB flash — universe becomes transparent | ✅ | cmbGlow sprite (oR×4+60 scale), bg warm tint |
| 6  | Dark ages — cold neutral gas | ✅ | darkages scene: 4000+ particles + 12 DM halos |
| 7  | Gas condensing → star ignition | ✅ | condT shrinks gasPts, stars ignite with 0.18 aT delay |
| 8  | Blue giants, yellow dwarfs, red dwarfs | ✅ | starCol=i<4 branch, 3 glow colors |
| 9  | First supernova explosion | ✅ | 800 burst particles with stored velocities |
| 10 | Neutron star/pulsar spinning beams | ✅ | Tilted TorusGeometry discs + 600 jet particles |
| 11 | Stellar BH accretion disk | ✅ | 4-ring bhDiskGrp rotating |
| 12 | First galaxies as orb-like clumps, stars as dots | ✅ | protogal (8 clumps) + stars as THREE.Points |
| 13 | First quasar BH + spinning disk + jets | ✅ | 7-ring disk + jet streams, offset from origin |
| 14 | Multiple supernovae enriching gas | ✅ | SN2 (aT=0.35) + SN3 (aT=0.38) |
| 15 | Camera shift from galaxy to solar system | ✅ | camCenter lerps from (0,0,0) to (ssX,0,ssZ) |
| 16 | MW arms assembling (center-out) | ✅ | buildSpiral sorted by radius + setDrawRange |
| 17 | Local group: 12 galaxies in correct positions | ✅ | Andromeda, M33, LMC, SMC, + 8 dwarfs |
| 18 | Andromeda approach ongoing | ✅ | Position drifts 18 units toward MW |
| 19 | Orion arm identification + zoom | ✅ | Orion dot marker + prompt + immersive scene |
| 20 | Solar system formation | ✅ | Protodisk → planets staggered → belts |
| 21 | NOW view with galaxy shapes + constellation lines | ✅ | Galaxy spirals + LineSegments + clickable |

## Key Architecture Decisions

### Scale System
- Early universe (aT 0-0.35): cosmicS=1.0, everything compact
- Expansion (aT 0.35+): cosmicS grows to 7.0, old content moves outward
- MW forms in cleared center at origin
- Solar system at (12×gwS, 0, 8×gwS) at 20% scale

### Nothing Disappears
All 12 addSG scenes end at aT=1.01. Content persists throughout.
Scene opacity fades via sceneFade() but groups remain visible at low opacity.

### Camera Narrative
- Big Bang: camR=180 (wide view)
- Galaxy Web: camR=352 (see full local group)
- Milky Way: camR=288 (MW fills view)
- Solar System: camR=25 (zoomed into arm)
- Present: camR=6 (Earth neighbourhood)
- camCenter shifts from (0,0,0) to solar system position

## Open Items / Known Issues

- Dark ages scene could use more particles for visual density
- MW accretion animation could be more dramatic (particles need visible convergence)
- Constellation lines only connect a few star pairs (need more IAU patterns)
- Solar system planet collision visuals not yet implemented
- Comet trails not yet implemented
- Camera zoom can feel jarring at era transitions
- User scroll overrides defCamR permanently (by design, but can lose the narrative)
