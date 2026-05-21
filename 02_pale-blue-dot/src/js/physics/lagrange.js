/**
 * lagrange.js
 * Computes the 5 Lagrange point positions for a two-body system.
 *
 * Reference: Murray & Dermott, Solar System Dynamics (1999), Chapter 3.
 * All positions returned in the co-rotating reference frame,
 * in units of the primary-secondary separation distance d.
 */

/**
 * Compute all 5 Lagrange point positions for a two-body system.
 *
 * @param {number} M1 - Mass of primary body (kg or any consistent unit)
 * @param {number} M2 - Mass of secondary body (same unit as M1)
 * @param {number} d  - Separation distance (km, AU, or any unit — output in same unit)
 * @param {number} theta - Current angle of secondary in orbit (radians, default 0)
 *
 * @returns {Object} Object with keys L1..L5, each { x, y, z } in frame of primary
 *                   with secondary initially at (d, 0, 0).
 *
 * Coordinate system:
 *   Primary M1 at origin.
 *   Secondary M2 at angle theta in XZ plane (y=0 for flat orbit).
 *   L4 leads M2 by 60°, L5 trails M2 by 60°.
 */
export function lagrangePoints(M1, M2, d, theta = 0) {
  const mu = M2 / (M1 + M2); // mass ratio (0 < mu < 0.5)

  // ── L1: Between primary and secondary ──────────────────────────────────────
  // Approximate formula (exact to O(μ^(1/3))):
  // r_L1 from M1 ≈ d × [1 - (μ/3)^(1/3)]
  const r_L1 = d * (1 - Math.pow(mu / 3, 1 / 3));

  // ── L2: Beyond secondary ───────────────────────────────────────────────────
  // r_L2 from M1 ≈ d × [1 + (μ/3)^(1/3)]
  const r_L2 = d * (1 + Math.pow(mu / 3, 1 / 3));

  // ── L3: Opposite side of primary from secondary ────────────────────────────
  // r_L3 from M1 ≈ d × [1 + 7μ/12]  (slightly beyond d, opposite direction)
  const r_L3 = d * (1 + (7 * mu) / 12);

  // ── L4 & L5: Equilateral triangle positions ────────────────────────────────
  // L4: secondary angle + 60°, same distance d from primary
  // L5: secondary angle - 60°, same distance d from primary
  // These are EXACT solutions (not approximations).

  const cos_theta = Math.cos(theta);
  const sin_theta = Math.sin(theta);

  // Secondary position (for reference)
  const M2x = d * cos_theta;
  const M2z = d * sin_theta;

  // L1 position (along line from M1 toward M2)
  const L1x = r_L1 * cos_theta;
  const L1z = r_L1 * sin_theta;

  // L2 position (along line from M1 away from M2, beyond M2)
  const L2x = r_L2 * cos_theta;
  const L2z = r_L2 * sin_theta;

  // L3 position (opposite direction from M2)
  const L3x = -r_L3 * cos_theta;
  const L3z = -r_L3 * sin_theta;

  // L4 position (equilateral triangle, leading M2 by 60°)
  const theta_L4 = theta + Math.PI / 3;  // +60°
  const L4x = d * Math.cos(theta_L4);
  const L4z = d * Math.sin(theta_L4);

  // L5 position (equilateral triangle, trailing M2 by 60°)
  const theta_L5 = theta - Math.PI / 3;  // -60°
  const L5x = d * Math.cos(theta_L5);
  const L5z = d * Math.sin(theta_L5);

  return {
    L1: { x: L1x, y: 0, z: L1z, r_from_primary: r_L1, stable: false },
    L2: { x: L2x, y: 0, z: L2z, r_from_primary: r_L2, stable: false },
    L3: { x: L3x, y: 0, z: L3z, r_from_primary: r_L3, stable: false },
    L4: { x: L4x, y: 0, z: L4z, r_from_primary: d,    stable: true  },
    L5: { x: L5x, y: 0, z: L5z, r_from_primary: d,    stable: true  },
  };
}

/**
 * Check if L4/L5 are stable for a given mass ratio.
 * Routh's criterion: stable if μ < μ_crit ≈ 0.03852
 *
 * @param {number} M1 - Primary mass
 * @param {number} M2 - Secondary mass
 * @returns {boolean} True if L4/L5 are stable
 */
export function l45Stable(M1, M2) {
  const mu = M2 / (M1 + M2);
  const mu_crit = 0.5 * (1 - Math.sqrt(23 / 27)); // ≈ 0.03852
  return mu < mu_crit;
}

/**
 * Earth-Moon Lagrange points in km from Earth's center.
 * Pre-computed for the visualization.
 */
export const EARTH_MOON_LAGRANGE = {
  // Mass ratio: μ = M_Moon / (M_Earth + M_Moon) ≈ 0.01215
  mu: 0.01215,
  d_km: 384400,  // mean Earth-Moon distance

  L1: {
    r_km: 323100,  // from Earth center
    description: 'Between Earth and Moon. Unstable. Gateway staging point.',
  },
  L2: {
    r_km: 445900,  // from Earth center (beyond Moon)
    description: 'Beyond Moon. Unstable. Lunar far-side relay.',
  },
  L3: {
    r_km: 381620,  // from Earth center (opposite side)
    description: 'Opposite Earth from Moon. Weakly unstable.',
  },
  L4: {
    r_km: 384400,  // same as Moon distance
    theta_from_moon_deg: +60,
    description: 'Stable. Leads Moon by 60°. Kordylewski dust clouds here.',
  },
  L5: {
    r_km: 384400,
    theta_from_moon_deg: -60,
    description: 'Stable. Trails Moon by 60°. L5 Society proposed colony here (1974).',
  },
  stable: true,  // μ = 0.01215 < 0.03852 → L4/L5 are stable
};

/**
 * Compute visualization-unit positions for Earth-Moon Lagrange points.
 * @param {number} moonOrbitR - Moon orbital radius in Three.js units
 * @param {number} moonAngle  - Current Moon angle (radians, default 0 = Moon at +X)
 * @returns {Object} L1..L5 positions as { x, y, z }
 */
export function earthMoonLagrangeViz(moonOrbitR, moonAngle = 0) {
  const mu = EARTH_MOON_LAGRANGE.mu;
  const scale = moonOrbitR;  // 1 unit = moonOrbitR in visualization

  const r_L1_norm = 1 - Math.pow(mu / 3, 1 / 3);   // ≈ 0.840
  const r_L2_norm = 1 + Math.pow(mu / 3, 1 / 3);   // ≈ 1.160

  const cos0 = Math.cos(moonAngle);
  const sin0 = Math.sin(moonAngle);

  return {
    L1: { x: scale * r_L1_norm * cos0,   y: 0, z: scale * r_L1_norm * sin0 },
    L2: { x: scale * r_L2_norm * cos0,   y: 0, z: scale * r_L2_norm * sin0 },
    L3: { x:-scale * cos0,               y: 0, z:-scale * sin0 },
    L4: { x: scale * Math.cos(moonAngle + Math.PI/3), y: 0, z: scale * Math.sin(moonAngle + Math.PI/3) },
    L5: { x: scale * Math.cos(moonAngle - Math.PI/3), y: 0, z: scale * Math.sin(moonAngle - Math.PI/3) },
  };
}
