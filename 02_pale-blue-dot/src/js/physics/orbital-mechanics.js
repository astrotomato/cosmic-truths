/**
 * orbital-mechanics.js
 * Kepler's laws, orbital velocity, escape velocity, and related calculations.
 * All equations from Murray & Dermott "Solar System Dynamics" (1999).
 */

import { G, M_SUN, AU_KM } from './scale-constants.js';

// ── KEPLER'S LAWS ─────────────────────────────────────────────────────────────

/**
 * Kepler's Third Law: orbital period from semi-major axis.
 * T² = (4π²/GM) × a³
 *
 * @param {number} a_AU - Semi-major axis in AU
 * @param {number} centralMass_kg - Mass of central body (default: M_SUN)
 * @returns {number} Period in years
 */
export function orbitalPeriod(a_AU, centralMass_kg = M_SUN) {
  const a_m = a_AU * AU_KM * 1000; // convert AU → metres
  const T_s = 2 * Math.PI * Math.sqrt(a_m ** 3 / (G * centralMass_kg));
  return T_s / (365.25 * 24 * 3600); // convert seconds → years
}

/**
 * Circular orbital velocity.
 * v = √(GM/r)
 *
 * @param {number} r_AU - Orbital radius in AU
 * @param {number} centralMass_kg - Mass of central body
 * @returns {number} Velocity in km/s
 */
export function circularVelocity(r_AU, centralMass_kg = M_SUN) {
  const r_m = r_AU * AU_KM * 1000;
  return Math.sqrt(G * centralMass_kg / r_m) / 1000; // m/s → km/s
}

/**
 * Vis-viva equation: velocity at any point on an elliptical orbit.
 * v² = GM(2/r - 1/a)
 *
 * @param {number} r_AU - Current radius in AU
 * @param {number} a_AU - Semi-major axis in AU
 * @param {number} centralMass_kg - Mass of central body
 * @returns {number} Velocity in km/s
 */
export function visViva(r_AU, a_AU, centralMass_kg = M_SUN) {
  const r_m = r_AU * AU_KM * 1000;
  const a_m = a_AU * AU_KM * 1000;
  return Math.sqrt(G * centralMass_kg * (2 / r_m - 1 / a_m)) / 1000;
}

/**
 * Escape velocity from surface.
 * v_esc = √(2GM/r)
 *
 * @param {number} r_km - Body radius in km
 * @param {number} mass_kg - Body mass in kg
 * @returns {number} Escape velocity in km/s
 */
export function escapeVelocity(r_km, mass_kg) {
  const r_m = r_km * 1000;
  return Math.sqrt(2 * G * mass_kg / r_m) / 1000;
}

/**
 * Perihelion and aphelion distances from semi-major axis and eccentricity.
 *
 * @param {number} a_AU - Semi-major axis in AU
 * @param {number} e - Eccentricity
 * @returns {{ peri: number, apo: number }} Perihelion and aphelion in AU
 */
export function periApo(a_AU, e) {
  return {
    peri: a_AU * (1 - e),
    apo:  a_AU * (1 + e),
  };
}

/**
 * Synodic period between two bodies orbiting the same center.
 * 1/T_syn = |1/T_inner - 1/T_outer|
 *
 * @param {number} T1_yr - Period of inner body (years)
 * @param {number} T2_yr - Period of outer body (years)
 * @returns {number} Synodic period in years
 */
export function synodicPeriod(T1_yr, T2_yr) {
  return 1 / Math.abs(1 / T1_yr - 1 / T2_yr);
}

// ── ANGULAR MOTION ────────────────────────────────────────────────────────────

/**
 * Angular velocity for circular orbit.
 * ω = 2π / T
 *
 * @param {number} T_yr - Orbital period in years
 * @returns {number} Angular velocity in radians/year
 */
export function angularVelocity(T_yr) {
  return (2 * Math.PI) / T_yr;
}

/**
 * Planet position on circular orbit at time t.
 * x = a·cos(ω·t + θ₀),  z = a·sin(ω·t + θ₀),  y = 0 (ecliptic plane)
 *
 * @param {number} a_units - Orbital radius in visualization units
 * @param {number} T_yr - Orbital period in years
 * @param {number} t_yr - Current time in years
 * @param {number} theta0 - Initial angle in radians (default 0)
 * @returns {{ x: number, y: number, z: number }}
 */
export function planetPosition(a_units, T_yr, t_yr, theta0 = 0) {
  const angle = theta0 + (2 * Math.PI * t_yr) / T_yr;
  return {
    x: a_units * Math.cos(angle),
    y: 0,
    z: a_units * Math.sin(angle),
  };
}

// ── VERIFICATION TABLE ────────────────────────────────────────────────────────
// Uncomment and run in browser console to verify:
//
// import { orbitalPeriod } from './orbital-mechanics.js';
// const planets = [
//   { name: 'Mercury', a: 0.38710 },
//   { name: 'Venus',   a: 0.72333 },
//   { name: 'Earth',   a: 1.00000 },
//   { name: 'Mars',    a: 1.52368 },
//   { name: 'Jupiter', a: 5.20260 },
//   { name: 'Saturn',  a: 9.55491 },
//   { name: 'Uranus',  a: 19.2184 },
//   { name: 'Neptune', a: 30.0700 },
// ];
// planets.forEach(p => console.log(p.name, orbitalPeriod(p.a).toFixed(4), 'yr'));
//
// Expected output (Kepler's Third Law):
//   Mercury  0.2408 yr
//   Venus    0.6151 yr
//   Earth    1.0000 yr
//   Mars     1.8814 yr
//   Jupiter  11.864 yr
//   Saturn   29.447 yr
//   Uranus   84.07  yr
//   Neptune  164.9  yr
