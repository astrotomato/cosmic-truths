# The Loneliness of Light — Physics Repository

Companion Python physics package for the interactive cosmological
horizon simulator. Every equation in the 3D simulation is implemented
and testable here.

## Modules

### `lcdm_physics.py`
Core ΛCDM cosmological equations.

| Function | What it models |
|---|---|
| `scale_factor(t)` | a(t)/a(now) via sinh parameterisation |
| `hubble_parameter(t)` | H(t) in km/s/Mpc |
| `hubble_radius(t)` | c/H(t) in Gly |
| `recession_velocity(d, t)` | v_rec in units of c |
| `observable_horizon(t)` | Particle horizon (proper Gly) |
| `reachable_horizon(t)` | Event horizon — shrinks with dark energy |
| `fraction_beyond_reach(t)` | % of observable galaxies forever unreachable |
| `zero_velocity_radius(M, t)` | Where Hubble and gravity exactly cancel |

### `hubble_flow_gravity_fields.py`
Vector field simulation of Hubble expansion vs gravitational binding.

Key insight: **There is no centre.** Every observer sees Hubble flow
radiating outward from their own position — `hubble_vec(point, observer, t)`
takes the observer position explicitly.

| Function | What it models |
|---|---|
| `hubble_vec(point, observer, t)` | Expansion velocity vector |
| `grav_vec(point, t)` | Net gravitational pull from all attractors |
| `net_vec(point, observer, t)` | Hubble minus gravity |
| `find_zero_velocity_surface(observer, t)` | True bound/unbound boundary |

### `photon_propagation.py`
Photon trajectories in ΛCDM spacetime.

| Function | What it models |
|---|---|
| `photon_comoving_distance(t_start, t_end)` | χ = c∫dt/a(t) |
| `can_photon_reach(d, t_fire)` | Compare d to event horizon |
| `photon_trajectory(d, t_fire)` | Full proper-distance trajectory |

## Key physics

```
Scale factor (flat ΛCDM):
  a(t) ∝ sinh²/³(t / t_Λ)   where t_Λ = 1/(H₀√Ω_Λ) ≈ 16.8 Gyr

Hubble law:
  v_rec = H(t) · d    [not motion through space — space itself expands]

Hubble parameter:
  H(t) = H₀ √(Ω_m/a³ + Ω_Λ)

Event horizon (reachable universe):
  χ_reach = c ∫_t^∞ dt'/a(t')  [FINITE because Λ > 0 — this is why 97% is unreachable]

Observable horizon:
  d_obs = a(t) · c ∫_0^t dt'/a(t')

Zero-velocity surface:
  G·M/r² = H(t)·r  →  r_zvs = (G·M/H(t))^(1/3)
```

## Constants (Planck 2018)
```
H₀    = 70.0 km/s/Mpc
Ω_m   = 0.309
Ω_Λ   = 0.691
T_now = 13.8 Gyr
```

## Run
```bash
pip install numpy scipy matplotlib
python lcdm_physics.py              # prints all key values + saves plot
python hubble_flow_gravity_fields.py  # vector field plots
python photon_propagation.py          # photon trajectory plots
```
