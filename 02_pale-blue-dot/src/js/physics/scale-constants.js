/**
 * scale-constants.js
 * Universal physical constants and unit conversion factors.
 * All values from IAU 2015, NIST CODATA 2018, Planck 2018.
 */

// ── FUNDAMENTAL CONSTANTS ────────────────────────────────────────────────────

export const C_KM_S   = 299792.458;          // Speed of light [km/s] (exact)
export const G        = 6.674e-11;            // Gravitational constant [N·m²/kg²]
export const H0       = 70.0;                 // Hubble constant [km/s/Mpc]
export const OMEGA_L  = 0.6911;               // Dark energy density parameter (Planck 2018)
export const OMEGA_M  = 0.3089;               // Matter density parameter
export const T0_GYR   = 13.799;              // Age of universe [Gyr]

// ── SOLAR SYSTEM MASSES & RADII ──────────────────────────────────────────────

export const M_SUN   = 1.98892e30;            // Solar mass [kg]
export const R_SUN   = 6.957e5;               // Solar radius [km]
export const M_EARTH = 5.9722e24;             // Earth mass [kg]
export const R_EARTH = 6371.0;                // Earth mean radius [km]
export const M_MOON  = 7.342e22;              // Lunar mass [kg]
export const R_MOON  = 1737.4;               // Lunar mean radius [km]
export const A_MOON  = 384400;               // Moon semi-major axis [km]

// ── UNIT CONVERSIONS ─────────────────────────────────────────────────────────

export const AU_KM     = 149597870.7;         // 1 AU in km (exact by definition)
export const LY_KM     = 9.46073e12;          // 1 light-year in km
export const PC_KM     = 3.08568e13;          // 1 parsec in km
export const PC_LY     = 3.26156;             // 1 parsec in light-years
export const MPC_KM    = 3.08568e19;          // 1 megaparsec in km
export const GLY_KM    = 9.46073e21;          // 1 gigalight-year in km

// Hubble radius (recession velocity = c)
export const R_HUBBLE_GLY = (C_KM_S / H0) * (MPC_KM / GLY_KM); // ≈ 14.0 Gly

// ── VISUALIZATION SCALE MAPPING ──────────────────────────────────────────────
//
// Each level maps real distances to Three.js units.
// GLY_TO_UNIT: how many Three.js units = 1 Gly at Level 0
// Other levels derive their own mapping similarly.

export const LEVEL_SCALES = {
  0: { realPerUnit_ly: 500e6,  label: '1 unit ≈ 500 million ly',    camR: 100, camPhi: Math.PI/3   },
  1: { realPerUnit_ly: 10e6,   label: '1 unit ≈ 10 million ly',     camR: 60,  camPhi: Math.PI/3   },
  2: { realPerUnit_ly: 150e3,  label: '1 unit ≈ 150,000 ly',        camR: 20,  camPhi: Math.PI/3   },
  3: { realPerUnit_ly: 2e3,    label: '1 unit ≈ 2,000 ly',          camR: 55,  camPhi: Math.PI/3   },
  4: { realPerUnit_ly: 20,     label: '1 unit ≈ 20 light-years',    camR: 30,  camPhi: Math.PI/3   },
  5: { realPerUnit_ly: null,   label: '1 unit = 1 AU (×10 visual)', camR: 80,  camPhi: Math.PI/9   },
  6: { realPerUnit_km: 50000,  label: '1 unit ≈ 50,000 km',         camR: 30,  camPhi: Math.PI/3   },
};

/**
 * Convert real distance in light-years to Three.js units for a given level.
 * @param {number} ly - Real distance in light-years
 * @param {number} level - Level index (0–6)
 * @returns {number} Three.js units
 */
export function lyToUnits(ly, level) {
  const s = LEVEL_SCALES[level];
  if (!s || !s.realPerUnit_ly) return ly;
  return ly / s.realPerUnit_ly;
}
