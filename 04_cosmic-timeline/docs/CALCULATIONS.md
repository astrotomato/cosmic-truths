# Calculations & Scale Mathematics

## Three-Phase Cosmic Expansion

The observable universe sphere radius `oR` follows three physically motivated phases:

### Phase 1: Inflation (aT 0 → 0.012)
```javascript
oR = 0.3 + 22 * (1 - exp(-aT / 0.003))
```
- Exponential growth modeling cosmic inflation (~10^-32 seconds after Big Bang)
- Reaches ~22 units at end of inflation
- Matches Big Bang particle content (basePos * sc ≈ 8 * 3.3 = 26.4 units)

### Phase 2: Content-Tracking (aT 0.012 → 0.35)
```javascript
earlyT = (aT - 0.012) / (0.35 - 0.012)
oR = 22 + 26 * pow(earlyT, 0.7)
```
- Grows from 22 → 48 units
- Tracks actual particle/star content radius (~45-50 units max)
- t^0.7 approximates matter-dominated expansion a(t) ∝ t^(2/3)

### Phase 3: Expansion Era (aT > 0.35)
```javascript
oR = 48 * cosmicS
if (aT > 0.64):
    aT2 = (aT - 0.64) / 0.36
    oR += 900 * (exp(aT2 * 1.4) - 1) / (exp(1.4) - 1)
```
- `oR = content_max × cosmicScale` — sphere always wraps content
- Acceleration bonus after aT=0.64 (dark energy era)

### oR Values at Key Moments

| aT   | Era          | oR (units) | Content Max | Ratio |
|------|--------------|------------|-------------|-------|
| 0.005| Inflation    | 23         | 21          | 1.10  |
| 0.05 | QGP          | 31         | 30          | 1.03  |
| 0.30 | First Stars  | 48         | 45          | 1.07  |
| 0.46 | MW Start     | 225        | 212         | 1.06  |
| 0.64 | Solar System | 300        | 280         | 1.07  |
| 1.00 | Present Day  | 1285       | 320         | 4.02  |

## Dynamic Cosmic Scale Factor (cosmicS)

```javascript
cosmicS = 1.0  // for aT ≤ 0.35
cosmicS = 1.0 + 6.0 * pow(min(1, (aT - 0.35) / 0.55), 0.30)  // for aT > 0.35
```

### Purpose
All early-universe scene groups scale by `cosmicS`. This MOVES existing content outward, creating room for the Milky Way to form at the center.

### cosmicS Values

| aT   | cosmicS | Effect |
|------|---------|--------|
| 0.00 | 1.00    | Universe compact, all content dense |
| 0.35 | 1.00    | Expansion begins |
| 0.46 | 4.70    | Old content at 4.7× distance — MW zone clear |
| 0.50 | 5.06    | Stars at 230+ units, MW forming at 0-65 |
| 0.64 | 5.95    | Old content at 270+ units |
| 1.00 | 7.00    | Maximum expansion |

### Clearance Calculation
MW + local group need ~65 units radius.
Old content (max 50 units at scale 1) × cosmicS must be >> 65.
At aT=0.46: 50 × 4.70 = 235 units. Gap ratio: 235/65 = 3.6×. ✓

## Galaxy Web Scale Factor (gwS)

```javascript
gwS = 1.0  // for aT ≤ 0.50
gwS = 1.0 + 2.5 * pow(min(1, (aT - 0.50) / 0.50), 0.4)  // for aT > 0.50
```

Galaxyweb group scales independently. MW spiral grows from 24 → 84 unit radius. Andromeda drifts from 58 → 203 units.

## Solar System Positioning

```javascript
ssX = 12 * gwS    // Orion arm x-position scales with galaxy
ssZ = 8 * gwS     // Orion arm z-position
scale = 0.20      // 20% of galaxy scale
```

### Scale Ratios
- Sun radius: 0.45 × 0.20 = 0.09 world units
- MW center (Sgr A*): 0.6 world units
- Sgr A* / Sun = 6.7×
- Earth orbit: 5 × 0.20 = 1.0 world units from Sun
- Jupiter: 25 × 0.20 = 5.0 world units
- Neptune: 150 × 0.20 = 30 world units
- Kuiper belt: 200 × 0.20 = 40 world units

## Camera Center Shift

```javascript
shiftT = max(0, min(1, (animT - 0.60) / 0.06))
camCenter.set(ssX * shiftT, 0, ssZ * shiftT)
```

Camera orbit center smoothly transitions from MW center (0,0,0) to solar system position between aT=0.60 and 0.66.

## Particle Counts

| System          | Count  | Distribution          |
|-----------------|--------|-----------------------|
| Big Bang        | 3,000  | sph(r, 0.5, 8)       |
| Main Particles  | 800    | 9 keyframe positions  |
| Dark Ages       | 4,000+ | sph(r, 0, 55) + halos |
| First Stars     | 16     | sph(r, 8, 45) dots    |
| Starfield       | 15,000 | sph(r, 10, 60)        |
| Proto-galaxies  | ~5,600 | 8 orb clumps          |
| MW Accretion    | 3,500  | Spiraling inward      |
| MW Spiral       | 800    | 4-arm sorted by radius|
| Local Group     | 12×800 | buildSpiral per galaxy |
| NOW Stars       | 29     | Log-scaled real positions|
