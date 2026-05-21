# Scene Architecture

## Main Scene Groups (addSG)

Each scene is an IIFE that creates a `THREE.Group`, populates it with meshes/particles,
registers it with `addSG()`, and defines an `animFn` for per-frame animation.

### bigbang
- 3,000 particles exploding from origin
- `sc` factor: 0.1 → 4.5 (inflation burst then slower expansion)
- Colors: white-hot core → yellow → orange → red at edges

### particles
- 800 particles interpolating through 9 keyframe states (KF_P, KF_C)
- kf0: QGP (red/green/orange quarks+gluons)
- kf1: Protons (blue/grey/yellow)
- kf2: BBN atoms (blue H, yellow He)
- kf3-kf8: Dark ages through star formation

### darkages
- 4,000+ cold neutral gas particles (very dark blue-grey)
- 12 dark matter halo clumps (200 particles each)

### firststars
- 16 stars as THREE.Points dots (3 types: 4 blue, 7 yellow, 5 red)
- Gas cloud (gasPts) that condenses (scale shrinks via condT)
- 3 supernovae: SN1 (aT=0.32), SN2 (aT=0.35), SN3 (aT=0.38)
- Each SN: 600-800 burst particles with stored velocities

### starfield
- 15,000 background stars in sph(10,60)
- 3 color groups: blue giants, yellow dwarfs, red dwarfs
- Particle size scales with sqrt(cosmicS) for visibility at distance

### protogal
- 8 orb-like proto-galaxy clumps (350-1200 particles each)
- Blue halos — represent primitive galaxies before spiral structure

### compact
- Pulsar: tilted TorusGeometry discs spinning at 0.28 rad/frame
- Stellar BH: 4-ring accretion disk spinning at 0.012 rad/frame

### quasar
- Group positioned at (28,4,18) — NOT at origin
- Black hole sphere + 7-ring spinning accretion disk
- 600 jet particles streaming from poles
- Position scales with cosmicS to move outward during expansion

### galaxyweb
- **Sgr A* accretion**: 3,500 particles spiraling inward, flattening into disk
- **MW spiral**: 800 points sorted by radius (center-out reveal via setDrawRange)
- **12 local group galaxies**: Andromeda, Triangulum, LMC, SMC, Sagittarius Dwarf,
  Sculptor, Fornax, Leo I, Leo II, NGC 6822, IC 1613, Phoenix Dwarf
- Orion arm dot marker at (12,0,8)
- Group scales with gwS factor

### solarsystem
- Group at dynamic position (ssX, 0, ssZ) on Orion arm, scale 0.20
- Sun (r=0.45) + glow (28 units)
- 8 planets with orbits, Saturn rings, Moon
- Proto-planetary disk (800 particles, fades as planets appear)
- Asteroid belt (2,200 particles) + Kuiper belt (1,600 particles)
- Planets appear one-by-one at staggered aT triggers

### pillars
- 4 particle columns (800 particles each) — tapered, organic dust shapes
- Orange ionised-gas glow at tips, red Hα mist at base
- 3,000 background ionised haze particles

### now
- 29 real star/galaxy positions (log-scaled, k=6.0)
- Galaxies rendered as 500-point flat spirals (not spheres)
- Stars as small spheres with glows
- Constellation line segments (LineSegments geometry)
- Invisible click meshes for galaxy targets

## Dynamic Scaling in updateScenes

```
cosmicS applied to: bigbang, particles, firststars, darkages,
                     starfield, protogal, compact, quasar
gwS applied to: galaxyweb
Solar/NOW: position = (12*gwS, 0, 8*gwS), scale = 0.20
Pillars: position = (10*gwS, -2*gwS, 6*gwS)
```

# Immersive Views (ensureObjScene)

25+ dedicated immersive scenes built lazily on first click.

| viewId       | Content |
|--------------|---------|
| bigbang      | 2000 colored particles (white/yellow/red), central glow |
| qgp          | Red/green/orange quarks+gluons, rotating |
| protons      | Blue protons, grey neutrons, yellow photons |
| bbn          | Blue H, yellow He nuclei |
| cmb          | 3000-particle CMB sphere at r=30, warm wireframe, inside-the-sphere camera |
| darkages     | 1500 very dark gas particles |
| firststars   | 3 stellar type glows (blue/yellow/red) + background gas |
| supernova    | 3000 particles flying outward, central flash, neutron star remnant |
| pulsar       | NS core, 3 tilted spinning discs, 600 jet particles, dipole field lines |
| stellarbh    | Dark sphere, 5-ring accretion disk, photon ring |
| firstgal     | Same as quasar (first galaxies hosted AGN) |
| quasar       | 7-ring spinning disk, bipolar jet streams |
| mwform       | 2000 particles morphing sphere→spiral, central BH |
| merger       | MW + Andromeda + M33 triple collision with tidal streams |
| andromeda    | Same as merger |
| sgra         | Dark BH sphere, 5-ring orange accretion disk, S-star cluster |
| alphacen     | Binary stars A+B orbiting, Proxima Centauri, star field |
| sunform      | Proto-star, converging gas cloud, proto-planetary disk |
| solarsystem  | Full system: Sun, 8 planets orbiting, asteroid+Kuiper belts |
| moonimpact   | Same system, closer camera |
| protodisk    | Same system |
| pillars      | 4 particle dust columns, ionised gas glow, Hα mist |
| crabneb      | Pulsar + 3-layer expanding filament shell |
| betelgeuse   | Large red pulsating sphere, expelled gas shell |
| sirius       | Binary star orbit (A1V white-blue + white dwarf) |
| orionarm     | Sun at center, nearby star glows, 800 arm stars |
| now          | Generic particle field with event name |
