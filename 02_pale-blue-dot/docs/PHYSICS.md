# Physics — Complete Equation Reference

All equations, constants, approximations, and derivations used in the Pale Blue Dot visualization. Organized by domain.

---

## Table of Contents

1. [Universal Constants](#1-universal-constants)
2. [Scale & Unit Conversions](#2-scale--unit-conversions)
3. [Orbital Mechanics](#3-orbital-mechanics)
4. [Lagrange Points](#4-lagrange-points)
5. [Cosmological Scales](#5-cosmological-scales)
6. [Hubble Flow & Recession](#6-hubble-flow--recession)
7. [Light Travel & Redshift](#7-light-travel--redshift)
8. [Galactic Structure](#8-galactic-structure)
9. [Stellar Physics](#9-stellar-physics)
10. [Simulation Approximations](#10-simulation-approximations)

---

## 1. Universal Constants

```
c   = 299,792.458 km/s          (speed of light, exact)
G   = 6.674 × 10⁻¹¹ N·m²/kg²  (gravitational constant)
H₀  = 70.0 km/s/Mpc            (Hubble constant, Planck 2018)
Ω_Λ = 0.6911                    (dark energy density parameter)
Ω_m = 0.3089                    (matter density parameter)
Ω_k ≈ 0                         (spatial curvature, consistent with flat)
t₀  = 13.799 Gyr                (age of the universe)

Solar constants:
M_☉ = 1.989 × 10³⁰ kg
R_☉ = 6.957 × 10⁵ km
L_☉ = 3.828 × 10²⁶ W

Earth constants:
M_⊕ = 5.972 × 10²⁴ kg
R_⊕ = 6,371 km (mean)
a_⊕ = 1.000 AU (semi-major axis)

Moon constants:
M_☾ = 7.342 × 10²² kg
R_☾ = 1,737.4 km
a_☾ = 384,400 km (mean)
T_☾ = 27.321 days (sidereal period)
```

---

## 2. Scale & Unit Conversions

### Fundamental length units

```
1 AU  = 149,597,870.7 km        (astronomical unit, exact by definition)
1 ly  = 9.4607 × 10¹² km       (light-year = c × 1 Julian year)
     = 63,241.077 AU
     = 0.30660 pc

1 pc  = 3.08568 × 10¹³ km      (parsec — parallax of 1 arcsecond)
     = 3.26156 ly
     = 206,265 AU

1 kpc = 10³ pc = 3.086 × 10¹⁶ km
1 Mpc = 10⁶ pc = 3.086 × 10¹⁹ km
1 Gpc = 10⁹ pc = 3.086 × 10²² km

1 Gly = 10⁹ ly = 9.461 × 10²¹ km
```

### Visualization scale mapping

Each level maps real distances to Three.js units (1 unit = N real units):

```
Level 0 (Observable Universe):  1 unit ≈ 500 million ly
  Observable radius ≈ 46,500 Mly → rendered as ~93 units radius
  Display radius set to 90 units; boundary sphere at R=90

Level 1 (Laniakea Supercluster): 1 unit ≈ 10 million ly
  Laniakea diameter ≈ 520 Mly → rendered as ~52 units across

Level 2 (Local Group):           1 unit ≈ 150,000 ly
  Andromeda at 2.537 Mly → rendered at ~17 units

Level 3 (Milky Way):             1 unit ≈ 2,000 ly
  Galaxy disk radius ~50 kly → rendered as ~25 units radius

Level 4 (Local Bubble):          1 unit ≈ 20 ly
  Local Bubble radius ~150 ly → rendered as ~18 units

Level 5 (Solar System):          1 unit = 1 AU
  Neptune at 30.07 AU → rendered at 30.07 × 10 = 300.7 units
  (scaled ×10 for visual clarity; relative ratios preserved)

Level 6 (Earth-Moon):            1 unit ≈ 50,000 km
  Moon at 384,400 km → rendered at 384,400/50,000 ≈ 7.7 units
  (rendered as 15 units for visual clarity)
```

### Orders of magnitude traversed

```
Observable Universe diameter:  ~8.8 × 10²³ km
Earth diameter:                ~1.27 × 10⁴ km
Ratio:                         ~7 × 10¹⁹

log₁₀(ratio) ≈ 19.85 orders of magnitude

The visualization descends approximately 20 orders of magnitude
from Level 0 to Level 6.
```

---

## 3. Orbital Mechanics

### Kepler's First Law
Planets orbit the Sun in ellipses with the Sun at one focus.

```
Ellipse equation (polar, Sun at focus):
  r(θ) = a(1 - e²) / (1 + e·cos θ)

where:
  a = semi-major axis
  e = orbital eccentricity  (0 = circle, 1 = parabola)
  θ = true anomaly (angle from perihelion)
```

### Kepler's Second Law
A line from the Sun to a planet sweeps equal areas in equal times (conservation of angular momentum).

```
dA/dt = L / 2m = constant

where L = m·r² · dθ/dt = angular momentum
```

### Kepler's Third Law
The square of the orbital period is proportional to the cube of the semi-major axis.

```
T² = (4π²/GM) × a³

In solar system units (M = M_☉, a in AU, T in years):
  T² = a³     (i.e., T = a^(3/2))

Verification with simulation planets:
  Mercury: T = 0.387^1.5 = 0.2408 yr ✓ (actual: 0.2408 yr)
  Venus:   T = 0.723^1.5 = 0.6151 yr ✓ (actual: 0.6152 yr)
  Earth:   T = 1.000^1.5 = 1.0000 yr ✓
  Mars:    T = 1.524^1.5 = 1.8814 yr ✓ (actual: 1.8809 yr)
  Jupiter: T = 5.203^1.5 = 11.864 yr ✓ (actual: 11.862 yr)
  Saturn:  T = 9.537^1.5 = 29.447 yr ✓ (actual: 29.457 yr)
  Uranus:  T = 19.19^1.5 = 84.07  yr ✓ (actual: 84.011 yr)
  Neptune: T = 30.07^1.5 = 164.9  yr ✓ (actual: 164.8 yr)
```

### Orbital velocity

```
Circular orbit velocity:
  v_circ = √(GM/r)

For Earth around Sun:
  v = √(G × M_☉ / 1 AU) = 29.78 km/s

Vis-viva equation (elliptical orbit):
  v² = GM(2/r - 1/a)

At perihelion (r = a(1-e)):  v_max = √[GM/a × (1+e)/(1-e)]
At aphelion  (r = a(1+e)):   v_min = √[GM/a × (1-e)/(1+e)]
```

### Escape velocity

```
v_esc = √(2GM/r)

From Earth's surface: v_esc = √(2 × G × M_⊕ / R_⊕)
                            = 11.186 km/s

From Sun's surface:   v_esc = 617.5 km/s

Relation to circular velocity: v_esc = √2 × v_circ
```

### Simulation angular velocity

The visualization advances planet angles each frame:

```javascript
// Angular velocity in radians per simulation frame
// dt = 0.016s (60fps), at 1× speed
ω = 0.002 / T_years    (radians per frame × speed multiplier)

// True angular velocity for Earth:
ω_earth = 2π / T_earth = 2π rad/yr = 1.991 × 10⁻⁷ rad/s

// Simulation compression factor ≈ 3.14 × 10⁸ 
// (one Earth orbit completes in ~314 frames at 1× speed)
```

### Synodic period (for reference)

```
1/T_synodic = |1/T_inner - 1/T_outer|

Earth-Mars synodic period:
  1/T = 1/1.000 - 1/1.881 → T = 2.135 years (780 days)
  (Mars oppositions occur every ~26 months)
```

### Moon's orbit

```
Semi-major axis:  a_☾ = 384,400 km = 0.002570 AU
Eccentricity:     e_☾ = 0.0549
Inclination:      i_☾ = 5.145° to ecliptic
Period (sidereal):T_sid = 27.321 days
Period (synodic): T_syn = 29.530 days  (full moon to full moon)

Perigee:  363,296 km
Apogee:   405,503 km

Angular velocity (mean): ω_☾ = 2π / 27.321 days
                               = 2.662 × 10⁻⁶ rad/s
                               ≈ 13.18°/day

Moon recession rate: ṙ = +3.82 cm/yr (laser ranging)
  Caused by tidal dissipation transferring angular momentum
  from Earth's rotation to Moon's orbit.
  
  In ~50 billion years (if Sun hasn't engulfed Earth):
  Moon would reach stable orbit ~600,000 km out.
```

---

## 4. Lagrange Points

Lagrange points are equilibrium positions in the co-rotating reference frame of a two-body gravitational system. At each point, the net force (gravity from both bodies + centrifugal) equals zero.

### Setup

```
Two bodies: M₁ (primary, e.g. Earth) and M₂ (secondary, e.g. Moon)
Mass ratio: μ = M₂ / (M₁ + M₂)

For Earth-Moon system:
  μ = M_☾ / (M_⊕ + M_☾)
    = 7.342×10²² / (5.972×10²⁴ + 7.342×10²²)
    = 7.342×10²² / 6.046×10²⁴
    = 0.01215

Separation: d = 384,400 km
```

### L1 — Between the bodies

L1 lies on the line connecting M₁ and M₂, between them. Solved from the quintic equation:

```
Approximate distance from M₁:
  r_L1 ≈ d × [1 - (μ/3)^(1/3)]

For Earth-Moon:
  r_L1 ≈ 384,400 × [1 - (0.01215/3)^(1/3)]
        ≈ 384,400 × [1 - (0.00405)^(1/3)]
        ≈ 384,400 × [1 - 0.1594]
        ≈ 384,400 × 0.8406
        ≈ 323,100 km from Earth

In visualization units (moonOrbitR = 15):
  L1_x = moonOrbitR × 0.85   (since 323,100/384,400 ≈ 0.84)

Stability: UNSTABLE. Objects near L1 slowly drift away.
           Requires station-keeping thrust.
```

### L2 — Beyond the secondary

L2 lies on the M₁-M₂ line, on the far side of M₂:

```
Approximate distance from M₁:
  r_L2 ≈ d × [1 + (μ/3)^(1/3)]

For Earth-Moon:
  r_L2 ≈ 384,400 × [1 + 0.1594]
        ≈ 384,400 × 1.1594
        ≈ 445,900 km from Earth

In visualization: L2_x = moonOrbitR × 1.17

Stability: UNSTABLE. Same as L1.

Note: The famous "Earth-Sun L2" is different — it's 1.5 million km
from Earth toward/away the Sun. JWST orbits the Sun-Earth L2.
```

### L3 — Opposite the secondary

L3 lies on the M₁-M₂ line, on the far side of M₁ from M₂:

```
Approximate distance from M₁:
  r_L3 ≈ d × [1 + 7μ/12]  (≈ d for small μ)

For Earth-Moon: r_L3 ≈ 384,400 × 1.0071 ≈ 387,100 km
(slightly beyond the Moon's orbital radius, opposite side)

In visualization: L3_x = -moonOrbitR

Stability: UNSTABLE. Weakly unstable with very long instability timescale.
           Not useful for spacecraft.
```

### L4 & L5 — Equilateral triangle positions

L4 and L5 form equilateral triangles with M₁ and M₂. They are:
- L4: 60° ahead of M₂ in its orbit
- L5: 60° behind M₂ in its orbit

```
Position of L4 (if M₂ is at angle θ):
  x_L4 = d × cos(θ + 60°)
  z_L4 = d × sin(θ + 60°)

With Moon at (d, 0, 0) [θ = 0°]:
  L4: ( d·cos60°,  0,  d·sin60°) = ( d/2,  0,  d√3/2)
  L5: ( d·cos60°,  0, -d·sin60°) = ( d/2,  0, -d√3/2)

In visualization units (moonOrbitR = 15):
  L4_x = 15 × 0.5    = 7.5
  L4_z = 15 × 0.866  = 12.99 ≈ 13
  L5_z = -12.99 ≈ -13

Stability: STABLE (for mass ratio μ < 0.0385)

Stability condition (Routh criterion):
  μ < (1/2)(1 - √(23/27)) ≈ 0.03852

For Earth-Moon: μ = 0.01215 < 0.03852 → L4 and L5 ARE stable ✓

Real objects at L4/L5 of Earth-Moon system:
  - Clouds of dust (Kordylewski clouds) may exist here.
  - No large captured objects confirmed (unlike Jupiter Trojans).

Jupiter's Trojan asteroids occupy Jupiter-Sun L4 and L5:
  - >9,800 known Trojans
  - Comparable mass to asteroid belt
```

### Effective potential at Lagrange points

The effective potential in the rotating frame:

```
U_eff(x,y) = -GM₁/r₁ - GM₂/r₂ - ½ω²(x² + y²)

where:
  r₁ = distance from M₁
  r₂ = distance from M₂
  ω  = orbital angular velocity = 2π/T

At Lagrange points: ∇U_eff = 0

Energy ordering: U(L4) = U(L5) > U(L3) > U(L2) > U(L1)
```

---

## 5. Cosmological Scales

### Observable Universe

```
Age of universe: t₀ = 13.799 ± 0.021 Gyr (Planck 2018)

Proper distance to particle horizon (observable radius):
  d_p = c × ∫₀^t₀ dt/a(t)  ×  a(t₀)
      ≈ 46.5 Gly (proper/comoving distance, Planck 2018)

Observable diameter: ~93 Gly

Number of observable galaxies: ~2 × 10¹²  (Conselice et al. 2016)
Number of stars (estimate):    ~10²⁴

Hubble volume (sphere within Hubble radius):
  R_H = c/H₀ = 299,792 / (70 km/s/Mpc × 1 Mpc/3.086×10¹⁹ km)
      = 299,792 / (2.268 × 10⁻¹⁸ s⁻¹)
      = 1.322 × 10²⁶ m
      = 13.97 × 10⁹ ly
      ≈ 14.0 Gly

V_Hubble = (4/3)π × R_H³
```

### Laniakea Supercluster

```
Discovered/named: Tully, Courtois, Hoffman, Pomarède (2014)
                  Nature 513, 71–73

Diameter:        ~500 Mly (comoving)
Mass:            ~10¹⁷ M_☉
Galaxy groups:   ~100,000
Redshift range:  z ≲ 0.05 (expansion-corrected flows)

Constituent galaxy groups include:
  - Virgo Supercluster (our local supercluster)
  - Hydra-Centaurus Supercluster
  - Pavo-Indus Supercluster
  - Southern Supercluster

Great Attractor coordinates:
  Galactic longitude: l = 307°
  Galactic latitude:  b = +9°
  Distance:           ~75 Mly (uncertain — obscured by Milky Way)
  Mass:               ~10¹⁶ M_☉ (rough)
```

### Local Group

```
Diameter:          ~3 Mly
Total mass:        ~2 × 10¹² M_☉ (virial mass)
Number of members: 54+ confirmed

Major members:
  Milky Way:    d = 0 (us)            M ≈ 1.5 × 10¹² M_☉
  Andromeda:    d = 2.537 ± 0.006 Mly  M ≈ 1.0 × 10¹² M_☉  (McConnachie 2012)
  Triangulum:   d = 2.73 ± 0.13 Mly   M ≈ 5 × 10¹⁰ M_☉

Milky Way-Andromeda merger:
  Relative velocity: ~120 km/s (approach)
  Estimated collision: ~4.5 Gyr from now
  First pass:         ~3.9 Gyr
  Full merger:        ~7 Gyr (simulations: Cox & Loeb 2008)
```

### Milky Way Galaxy

```
Type:            SBbc (barred spiral, intermediate winding)
Disk diameter:   ~100 kly (disk stars)
Disk thickness:  ~1 kly (thin disk); ~3.5 kly (thick disk)
Bulge diameter:  ~10 kly
Halo diameter:   ~200 kly (stellar halo); >1 Mly (dark matter halo)

Mass components:
  Stellar mass:    ~6 × 10¹⁰ M_☉
  Dark matter:     ~1 × 10¹² M_☉ (total virial)
  Gas + dust:      ~1.5 × 10¹⁰ M_☉

Number of stars: 100–400 billion

Central black hole:
  Name:            Sagittarius A* (Sgr A*)
  Mass:            4.154 ± 0.014 × 10⁶ M_☉ (Event Horizon Telescope 2022)
  Schwarzschild radius: 2GM/c² = 12.3 × 10⁶ km ≈ 0.082 AU

Spiral arms (4 major):
  Perseus Arm:       R ≈ 9.9 kpc from center, outer arm
  Sagittarius Arm:   R ≈ 6.0 kpc, prominent arm
  Orion Arm (spur):  R ≈ 8.0 kpc, our local arm
  Norma-Cygnus Arm:  R ≈ 4.5 kpc, inner arm

Sun's position:
  R_☉ = 8.178 ± 0.013 kpc from center (GRAVITY Collaboration 2019)
  z_☉ ≈ +25 pc above mid-plane
  θ_☉ ≈ 27.5° from galactic north (toward Cygnus)

Galactic rotation:
  Orbital velocity at Sun: v_☉ ≈ 240 km/s (Reid et al. 2019)
  Orbital period (galactic year): P = 2πR/v ≈ 225 Myr
  Age of universe in galactic years: 13,800 / 225 ≈ 61 orbits
```

---

## 6. Hubble Flow & Recession

### Hubble's Law

```
v_rec = H₀ × d

where:
  v_rec = recession velocity [km/s]
  H₀    = Hubble constant ≈ 70.0 km/s/Mpc (Planck 2018: 67.4 ± 0.5)
  d     = proper distance [Mpc]

Hubble radius (recession velocity = c):
  R_H = c / H₀ = 299,792 / 70.0 = 4,282.7 Mpc = 13.97 Gly ≈ 14.0 Gly

Any object beyond ~14 Gly is currently receding faster than light.
This does NOT violate special relativity — space itself is expanding.
```

### Recession vs. peculiar velocity

```
Total observed velocity = Hubble flow + peculiar velocity
v_obs = H₀ × d + v_pec

Peculiar velocities typically: 100–1000 km/s
  (Local Group: ~620 km/s toward Great Attractor)

At d = 100 Mpc: Hubble flow = 7,000 km/s >> v_pec
At d = 1 Mpc:   Hubble flow = 70 km/s ≈ v_pec  (velocities comparable)
At d < 1 Mpc:   Peculiar motions dominate (Local Group is gravitationally bound)
```

### ΛCDM Scale Factor

```
The Friedmann equation in ΛCDM cosmology:

  (ȧ/a)² = H₀² [Ω_m/a³ + Ω_k/a² + Ω_Λ]

For flat universe (Ω_k = 0):
  H(a) = H₀ √[Ω_m × a⁻³ + Ω_Λ]

Analytic solution for matter + dark energy (flat):
  a(t) = (Ω_m/Ω_Λ)^(1/3) × sinh^(2/3)[t/t_Λ × 3/2]

where:
  t_Λ = 2 / (3 × H₀ × √Ω_Λ) = 2/(3 × 70.0 × 0.8315) / (km/s/Mpc to Gyr)
      ≈ 17.3 Gyr

At t = t₀ = 13.8 Gyr: a = 1 (by definition)
At t = 100 Gyr: a ≈ 13.8 (universe 14× larger in linear scale)

This is used in the companion "Loneliness of Light" simulation
to compute how horizons shrink as dark energy dominates.
```

---

## 7. Light Travel & Redshift

### Light travel time

```
d_light = c × t

1 light-second = 299,792.458 km
1 light-minute = 17,987,547 km
1 light-hour   = 1.079 × 10⁹ km

Earth to Moon:    384,400 km / 299,792 km/s = 1.282 seconds
Earth to Sun:     1 AU / 299,792 km/s        = 499.0 seconds = 8.317 minutes
Sun to Neptune:   30.07 AU × 499.0 s         = 4.16 hours
Sun to α Centauri: 4.37 ly                  = 4.37 years
Sun to galactic center: 26,000 ly            = 26,000 years
Sun to Andromeda: 2.537 Mly                  = 2.537 million years
```

### Cosmological redshift

```
z = (λ_observed - λ_emitted) / λ_emitted = a(t_obs)/a(t_emit) - 1

Redshift↔distance (approximate, for small z):
  z ≈ H₀ × d / c = d / R_H

Notable redshifts:
  z = 0.0005: Virgo Cluster       (~23 Mly)
  z = 0.017:  Coma Cluster        (~321 Mly)
  z = 0.2:    ~2.4 Gly
  z = 1.0:    ~5.2 Gly  (lookback)
  z = 2.0:    ~7.5 Gly
  z = 6.0:    ~12.5 Gly (end of reionization)
  z = 13:     ~13.4 Gly (JWST galaxy candidates, 2022–2024)
  z = 1089:   ~13.77 Gly (CMB surface of last scattering)
```

### Angular diameter distance

```
For small angles:
  θ = d_physical / d_A

Angular diameter distance:
  d_A = d_comoving / (1 + z)

As z → ∞, d_A → 0 (the CMB "surface" subtends a finite angle)

Angular size of Earth as seen from 6 billion km (Voyager 1 distance, 1990):
  θ = 2R_⊕ / d_Voyager
    = 2 × 6,371 km / (6 × 10⁹ km)
    = 2.12 × 10⁻⁶ radians
    = 0.436 arcseconds
    ≈ 0.12° / 1000
    (fits within a single pixel of Voyager's camera)
```

---

## 8. Galactic Structure

### Spiral arm geometry

Logarithmic spiral model for Milky Way arms:

```
r(θ) = r₀ × exp(θ × tan(α))

where:
  r₀    = arm radius at reference angle
  θ     = azimuthal angle
  α     = pitch angle (~12–15° for Milky Way)

In the simulation (simplified linear approximation):
  r(t) = r_min + t × r_max    where t ∈ [0,1]
  θ(t) = θ_start + t × 2.2π  (2.2 windings per arm)
```

### Rotation curve (Milky Way)

```
Observed: v_rot(R) ≈ 220–240 km/s for R ∈ [3, 18] kpc
          (nearly flat — evidence for dark matter)

Expected for point-mass Sun: v ∝ 1/√R (Keplerian decline)
Actual:                       v ≈ constant → M_enclosed ∝ R

Dark matter density (NFW profile):
  ρ(r) = ρ_s / [(r/r_s)(1 + r/r_s)²]

where ρ_s and r_s are characteristic density and scale radius.
```

### Stellar density

```
Thin disk density:
  ρ_thin(R,z) = ρ₀ × exp(-R/R_d) × exp(-|z|/z_d)

  R_d (scale radius)  ≈ 2.6 kpc
  z_d (scale height)  ≈ 300 pc (thin disk)
                      ≈ 900 pc (thick disk)

Bulge (de Vaucouleurs profile):
  Σ(R) ∝ exp(-b × [(R/R_e)^(1/4) - 1])
  R_e (effective radius) ≈ 0.5 kpc
```

---

## 9. Stellar Physics

### Main sequence luminosity-mass relation

```
L ∝ M^α

α ≈ 4.0 for M ∈ [0.5, 10] M_☉
α ≈ 3.5 for higher masses

Lifetime on main sequence:
  τ_MS ≈ (M/M_☉) / (L/L_☉) × 10¹⁰ yr
        ≈ M^(-2.5) × 10¹⁰ yr  [for solar-type stars]

Nearby star lifetimes:
  Proxima Cen (M5V, 0.12 M_☉): τ ≈ 4 × 10¹² yr (4 trillion years)
  Sun (G2V, 1.0 M_☉):          τ ≈ 10¹⁰ yr (10 billion years)
  Sirius A (A1V, 2.0 M_☉):     τ ≈ 1.2 × 10⁹ yr
  Vega (A0V, 2.1 M_☉):         τ ≈ 1.0 × 10⁹ yr
```

### Spectral classification

```
O B A F G K M  (hottest to coolest)
"Oh Be A Fine Girl/Guy, Kiss Me"

Type  T_eff (K)    Color           Example
O     30,000–50,000  Blue           ζ Orionis
B     10,000–30,000  Blue-white     Rigel, Sirius B
A     7,500–10,000   White          Sirius A, Vega
F     6,000–7,500    Yellow-white   Procyon
G     5,200–6,000    Yellow         Sun, α Cen A
K     3,700–5,200    Orange         ε Eridani, τ Ceti
M     2,400–3,700    Red            Proxima Cen, Betelgeuse
```

### Stefan-Boltzmann law

```
L = 4πR²σT⁴

σ = 5.670 × 10⁻⁸ W/m²/K⁴ (Stefan-Boltzmann constant)

Color from Wien's displacement law:
  λ_max = b / T    (b = 2.898 × 10⁻³ m·K)

For Sun (T = 5778 K):
  λ_max = 501 nm (green — but the Sun appears yellow-white
          because we see integrated spectrum)
```

---

## 10. Simulation Approximations

### What is exact

- Planetary orbital periods (from Kepler's Third Law, exact in units)
- Relative orbital distances (semi-major axes from JPL DE430)
- Lagrange point positions (computed from μ formula above)
- Light travel times (cited in labels)
- Named star distances (from HIPPARCOS parallax measurements)
- Galaxy distances (NED database)

### What is approximated

1. **Orbital eccentricity**: Planets are rendered on circular orbits. Actual eccentricities are small (Mercury e=0.206 being the exception) and visually negligible at the scales shown.

2. **Orbital inclinations**: All planets are rendered in the ecliptic plane (y=0). Real inclinations relative to the invariable plane: Mercury 6.34°, Venus 2.19°, Earth 1.57°, Mars 1.67°, Jupiter 0.32°, Saturn 0.93°, Uranus 1.02°, Neptune 0.72°. Negligible for visualization purposes.

3. **Galaxy morphology**: Galaxies are rendered as procedural point clouds using logarithmic spiral models. Real spiral structure is derived from H II region surveys (Hou & Han 2014) and is more complex.

4. **Cosmic web filaments**: Generated with seeded Perlin-like noise. Real filament positions come from redshift surveys (2dF, SDSS, DES).

5. **Hubble constant**: Planck 2018 value (67.4 km/s/Mpc) is in tension with local measurements (SH0ES: 73.0 km/s/Mpc). We use 70 km/s/Mpc as a compromise pending resolution of the "Hubble tension."

6. **Scale rendering**: Many levels use a non-linear visual scale (objects rendered larger than physical size for visibility). The *relative* positions and distances are preserved; absolute sizes are not.

### Seeded random number generator

```javascript
// Linear congruential generator (Knuth)
function seeded(seed) {
  let s = seed;
  return () => {
    s = (s * 1664525 + 1013904223) & 0xffffffff;
    return (s >>> 0) / 0xffffffff;
  };
}
// Produces deterministic, reproducible pseudo-random numbers
// Period: 2³² ≈ 4.3 billion values before cycling
```

### Performance notes

- Particle counts are reduced from physically realistic values for 60fps target
- Level 0: 6,000 field galaxies (real: ~2 × 10¹² — rendered as statistical sample)
- Level 5: 1,500 asteroid particles (real: ~10⁶ large + 10⁹ small)
- Geometry is disposed on level change to prevent memory leaks

---

## References

1. Planck Collaboration (2020). "Planck 2018 results. VI: Cosmological parameters." A&A 641, A6. arXiv:1807.06209

2. Tully, R.B., Courtois, H., Hoffman, Y., Pomarède, D. (2014). "The Laniakea supercluster of galaxies." Nature 513, 71–73.

3. GRAVITY Collaboration (2019). "A geometric distance measurement to the Galactic center black hole with 0.3% uncertainty." A&A 625, L10.

4. Reid, M.J., et al. (2019). "Trigonometric Parallaxes of High-mass Star-forming Regions: Our View of the Milky Way." ApJ 885, 131. (BeSSeL Survey)

5. Conselice, C.J., et al. (2016). "The Evolution of Galaxy Number Density at z < 8 and Its Implications." ApJ 830, 83. (2 trillion galaxies estimate)

6. Cox, T.J., Loeb, A. (2008). "The collision between the Milky Way and Andromeda." MNRAS 386, 461–474.

7. Zucker, C., et al. (2022). "Star formation near the Sun is driven by expansion of the Local Bubble." Nature 601, 334–337.

8. McConnachie, A.W. (2012). "The Observed Properties of Dwarf Galaxies in and around the Local Group." AJ 144, 4.

9. Murray, C.D., Dermott, S.F. (1999). Solar System Dynamics. Cambridge University Press. (Lagrange point derivations, Chapter 3)

10. Murray, Z., Holman, M. (2001). "The role of chaotic resonances in the solar system." Nature 410, 773–779.
