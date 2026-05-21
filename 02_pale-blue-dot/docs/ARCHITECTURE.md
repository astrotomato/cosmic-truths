# Architecture — Code Structure & Extension Guide

## Overview

The visualization is a single self-contained HTML file (`index.html`) with all CSS, JS, and inline data. It uses Three.js r128 (loaded from CDN) and Google Fonts. No build step, no bundler.

The `src/` directory contains the same logic factored into ES modules for maintainability and extensibility — use with `npx serve` or any module-aware local server.

---

## Core Concepts

### 1. Level System

Each "level" is a self-contained Three.js scene loaded on demand. Levels are numbered 0–7. Level 7 is the terminal "Pale Blue Dot" screen (no 3D scene).

```
buildLevel(n) → clearScene() → buildLevel{n}() → updateInfoPanel() → updateDepthLadder()
```

On `buildLevel(n)`:
1. All existing Three.js objects are disposed and removed from `sceneGroup`
2. All DOM label elements are removed
3. The builder function for level n is called
4. Camera phi is reset to the per-level default
5. UI panels are updated

### 2. Scene Group

All level objects are added to `sceneGroup` (a `THREE.Group`), not directly to `scene`. This allows:
- Mass disposal on level change: `clearScene()` iterates `sceneGroup.children`
- Future: level transitions via `sceneGroup.scale` animation

The `scene` itself contains only the background color.

### 3. Clickable Objects — `levelObjects` Array

Clickable objects (descent targets) are tracked in `levelObjects[]`. The raycaster tests against this array, not the entire scene, for performance.

```javascript
levelObjects.push(mesh);
mesh.userData = { name: '...', isClickable: true, nextLevel: N, sub: '...' };
```

The `userData` contract:
```typescript
interface ObjectUserData {
  name: string;          // Display name (tooltip + label)
  isClickable: boolean;  // Whether clicking this descends
  nextLevel?: number;    // Level to descend to (required if isClickable)
  sub?: string;          // Subtitle (tooltip)
}
```

### 4. Label System

Labels are DOM `div` elements with class `obj-label` that follow 3D objects by projecting their world position to screen coordinates each frame.

```javascript
// Create: attach label to a 3D mesh
createLabel(mesh, name, sub, clickable, nextLevel)

// Update (called every frame in animate()):
updateLabels()
// → mesh.getWorldPosition(v) → v.project(camera) → div CSS left/top

// Destroy (called in clearScene()):
clearLabels()
```

Labels clip to screen bounds — labels whose projected position is outside the viewport are hidden.

### 5. Boundary Sphere

`makeBoundarySphere(radius, hexColor)` adds a visual "edge of this zoom level" indicator:
- Semi-transparent `DoubleSide` fill mesh (`depthTest: false`)
- Wireframe sphere (`depthTest: false`)
- Equatorial `LineLoop` (precise 1px ring)
- Two meridian `LineLoop` rings

`depthTest: false` on all elements ensures the sphere remains visible when the camera is inside it (zoomed in). Without this, Three.js depth testing would hide the sphere surfaces once inside.

### 6. Orbit Controls (Manual)

No OrbitControls import — implemented directly:

```javascript
// Camera positioned in spherical coordinates:
x = orbitR × sin(orbitPhi) × cos(orbitTheta)
y = orbitR × cos(orbitPhi)
z = orbitR × sin(orbitPhi) × sin(orbitTheta)

// Smooth follow with lerp:
camera.position.lerp(new THREE.Vector3(x,y,z), 0.06)
camera.lookAt(0,0,0)

// Auto-rotate when idle:
orbitTheta += 0.0008 (if !isDrag && !isMouseDown)
```

### 7. Seeded RNG

Procedural geometry (filaments, particle fields, galaxy arms) uses a seeded LCG for reproducible results:

```javascript
function seeded(seed) {
  let s = seed;
  return () => {
    s = (s * 1664525 + 1013904223) & 0xffffffff;
    return (s >>> 0) / 0xffffffff;
  };
}
```

Each level uses a fixed seed — Level 0 uses seed 42, Level 1 uses 7, etc. This ensures the scene looks identical on every load.

### 8. Planet Animation

Planet positions are updated each frame using the `planetMeshes` array, which stores wrapper objects:

```javascript
{ mesh: THREE.Mesh, glow: THREE.Sprite, planet: PlanetDef, angle: number }
```

On each frame:
```javascript
entry.angle += 0.002 / entry.planet.period;
entry.mesh.position.set(cos(entry.angle) × a, 0, sin(entry.angle) × a);
entry.glow.position.copy(entry.mesh.position);
```

Saturn's ring is a separate entry `{ isRing: true, ring: Mesh, planet: Saturn }` that copies Saturn's position each frame.

---

## Adding a New Level

To add Level 7.5 (e.g., "Atmosphere"):

### Step 1: Add to LEVELS array

```javascript
LEVELS.push({
  id: 8,
  name: 'Atmosphere',
  sub: '~100 km above surface',
  facts: [
    ['Height', '~100 km (Kármán line)'],
    ['Composition', '78% N₂, 21% O₂'],
    // ...
  ],
  desc: '...',
  hint: 'Click ...',
  bgColor: 0x000510,
});
```

### Step 2: Write the builder

```javascript
function buildLevel8() {
  scene.background = new THREE.Color(0x000510);

  // Add objects...
  const earth = new THREE.Mesh(
    new THREE.SphereGeometry(2, 32, 32),
    new THREE.MeshBasicMaterial({ color: 0x1a3a8a })
  );
  earth.userData = { name: 'Earth surface', isClickable: true, nextLevel: 9, sub: 'Descend further' };
  sceneGroup.add(earth);
  levelObjects.push(earth);
  createLabel(earth, 'Earth', 'Lv.8 → Lv.9', true, 9);

  // Add boundary
  makeBoundarySphere(20, 0x1a2840);

  orbitR = 25; targetR = 25;
}
```

### Step 3: Register in buildLevel switch

```javascript
case 8: buildLevel8(); break;
```

### Step 4: Add camera phi

```javascript
const LEVEL_CAM_PHI = [..., Math.PI/4]; // index 8
```

### Step 5: Add to depth ladder

```javascript
const names = [..., 'Atmosphere', 'Surface'];
```

---

## Modular Source (`src/`)

The `src/` directory contains the same code split into ES modules. Use with:

```bash
npx serve .
# Open http://localhost:3000/src/index.html
```

### Module graph

```
src/js/main.js
  ├── physics/scale-constants.js     (unit conversions, GLY_TO_UNIT etc.)
  ├── physics/orbital-mechanics.js   (Kepler, Lagrange computations)
  ├── physics/lagrange.js            (Lagrange point calculator)
  ├── ui/labels.js                   (createLabel, clearLabels, updateLabels)
  ├── ui/depth-ladder.js             (updateDepthLadder)
  ├── ui/boundary-sphere.js          (makeBoundarySphere)
  ├── ui/info-panel.js               (updateInfoPanel, updateScaleBar)
  ├── levels/level0-universe.js      (buildLevel0)
  ├── levels/level1-laniakea.js      (buildLevel1)
  ├── levels/level2-local-group.js   (buildLevel2)
  ├── levels/level3-milky-way.js     (buildLevel3)
  ├── levels/level4-orion-arm.js     (buildLevel4)
  ├── levels/level5-solar-system.js  (buildLevel5, PLANETS, planetMeshes)
  └── levels/level6-earth-moon.js    (buildLevel6, moonMesh, moonAngle)
```

Each level module exports a single `buildLevelN(sceneGroup, levelObjects, createLabel, makeBoundarySphere)` function with its dependencies injected.

---

## Performance Notes

### Geometry disposal

All geometry and materials are disposed on level change:

```javascript
function clearScene() {
  clearLabels();
  while (sceneGroup.children.length) {
    const child = sceneGroup.children[0];
    sceneGroup.remove(child);
    child.geometry?.dispose();
    if (Array.isArray(child.material)) {
      child.material.forEach(m => m.dispose());
    } else {
      child.material?.dispose();
    }
  }
  levelObjects = [];
}
```

Textures used for glow sprites (canvas-generated) are disposed via the material: `SpriteMaterial.map` (the `THREE.CanvasTexture`) is garbage collected when the material is disposed.

### Particle counts

| Level | Particles | Real count | Compression |
|-------|-----------|-----------|-------------|
| 0 (field galaxies) | 6,000 | ~2 × 10¹² | 1:3.3 × 10⁸ |
| 5 (asteroids) | 1,500 | ~10⁹ | 1:666,667 |
| 5 (Kuiper belt) | 800 | ~100,000 | 1:125 |
| 4 (ISM dust) | 2,000 | — | visualization only |

### Raycasting

The raycaster tests only `levelObjects[]` (5–20 objects), not the full scene (thousands of particles). This keeps hover detection at O(n_clickable) not O(n_total).

---

## Known Limitations & Future Work

1. **No actual texture maps**: Earth, Moon, planets use solid colors. Could be replaced with NASA PDS imagery.

2. **Simplified orbital mechanics**: Circular orbits only. Could use true Keplerian ellipses with eccentric anomaly solving.

3. **No precession or axial tilt**: Earth's 23.44° tilt and orbital plane inclinations are omitted.

4. **Cosmic web is procedural**: Real filament positions from SDSS/DES redshift surveys could replace the seeded-RNG filaments at Level 0.

5. **No gravitational lensing**: At cosmological scales, lensing effects (Einstein rings, distortion around massive clusters) are not rendered.

6. **Single-threaded**: Heavy particle builds block the main thread momentarily. Could be moved to a Web Worker with transferable buffers.

7. **No WebXR**: The scene would work well in VR — Three.js supports WebXR with minimal changes.
