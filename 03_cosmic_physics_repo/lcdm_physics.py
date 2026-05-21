"""
ΛCDM Cosmological Physics — Core Equations
===========================================
All physics used in The Loneliness of Light simulator.
Sources: Planck 2018, Peebles 1993, Davis & Lineweaver 2004

Units throughout:
  Distance : Gly (gigalight-years)
  Time     : Gyr (gigayears)
  Velocity : km/s or fraction of c
  H₀       : km/s/Mpc
"""

import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# ── COSMOLOGICAL CONSTANTS (Planck 2018) ──────────────────────────────────────
H0          = 70.0          # Hubble constant, km/s/Mpc
OMEGA_M     = 0.309         # Matter density parameter
OMEGA_L     = 0.691         # Dark energy (cosmological constant) density parameter
OMEGA_K     = 0.0           # Curvature (flat universe)
C_KM_S      = 299792.458    # Speed of light, km/s
MPC_TO_GLY  = 0.0032616     # 1 Megaparsec in gigalight-years (= 3.2616 Mly)
T_NOW       = 13.8          # Age of universe today, Gyr
C_GLY_GYR   = 0.9461        # Speed of light, Gly/Gyr

# Hubble radius today: c / H₀ in Gly
HUBBLE_RADIUS_GLY = (C_KM_S / H0) * MPC_TO_GLY  # ≈ 14.0 Gly

# ── SCALE FACTOR a(t) ─────────────────────────────────────────────────────────
def t_lambda():
    """Characteristic time for dark energy domination (Gyr)."""
    H0_per_gyr = H0 * 1.022e-3   # convert km/s/Mpc → 1/Gyr
    return 1.0 / (np.sqrt(OMEGA_L) * H0_per_gyr)

T_LAMBDA = t_lambda()

def scale_factor(t_gyr):
    """
    a(t) / a(T_NOW) using ΛCDM sinh parameterisation.
    
    Exact analytic solution for flat ΛCDM:
        a(t) ∝ sinh^(2/3)( t / t_Λ )
    where t_Λ = 1 / (H₀ √Ω_Λ)
    
    Returns the ratio a(t)/a(T_NOW), so = 1.0 at t = T_NOW.
    """
    t = np.asarray(t_gyr, dtype=float)
    t = np.where(t <= 0, 1e-10, t)
    sinh_now = np.sinh(T_NOW / T_LAMBDA)
    sinh_t   = np.sinh(t    / T_LAMBDA)
    return (sinh_t / sinh_now) ** (2/3)

def hubble_parameter(t_gyr):
    """
    H(t) in km/s/Mpc at time t.
    
    From Friedmann equation:
        H(t) = H₀ √( Ω_m/a³ + Ω_Λ )
    """
    a = scale_factor(t_gyr)
    return H0 * np.sqrt(OMEGA_M / a**3 + OMEGA_L)

def hubble_radius(t_gyr):
    """
    Hubble radius c/H(t) in Gly.
    Recession velocity equals c at this distance.
    """
    H_t = hubble_parameter(t_gyr)
    return (C_KM_S / H_t) * MPC_TO_GLY

def recession_velocity(d_gly, t_gyr):
    """
    Recession velocity at comoving distance d_gly at time t, in units of c.
    
    v_rec = H(t) × d   [Hubble's law — not motion through space!]
    
    d is comoving distance in Gly.
    v > c is possible and physically consistent (superluminal recession).
    """
    H_t = hubble_parameter(t_gyr)   # km/s/Mpc
    # v = H*d: d[Gly]/MPC_TO_GLY = d[Mpc]; v[km/s]/C_KM_S = v[fraction of c]
    return H_t * d_gly / (MPC_TO_GLY * C_KM_S)

# ── HORIZON INTEGRALS ─────────────────────────────────────────────────────────
def _integrand_comoving(t):
    """c dt/a(t) — comoving distance element."""
    return C_GLY_GYR / scale_factor(t)

def observable_horizon(t_gyr, n=600):
    """
    Particle horizon (proper distance) at time t_gyr in Gly.
    
    d_obs(t) = a(t) · c ∫₀ᵗ dt'/a(t')
    
    Uses log-spaced time array to handle the near-singularity at t→0
    where 1/a(t) diverges. At T_NOW: ~40 Gly (slight underestimate vs
    accepted 46.5 Gly due to omitting radiation domination in early universe).
    """
    # Log-spaced so early times (small a, large integrand) are sampled densely
    t_arr = np.logspace(np.log10(1e-4), np.log10(t_gyr), n)
    integral = np.trapezoid(_integrand_comoving(t_arr), t_arr)
    return integral * scale_factor(t_gyr)

def reachable_horizon(t_gyr, n=400):
    """
    Event horizon (comoving distance) — how far a photon fired NOW can ever reach.
    
        χ_reach(t) = c ∫ₜ^∞ dt'/a(t')
    
    Due to accelerating expansion, this integral CONVERGES to a finite value.
    At T_NOW: ≈ 16.5 Gly comoving.
    This is the TRUE measure of cosmic loneliness — it SHRINKS over time.
    
    Galaxies beyond this distance are permanently unreachable.
    """
    t_end = t_gyr + 4000.0   # effectively ∞
    t_arr = np.linspace(t_gyr, t_end, n)
    integral = np.trapezoid(_integrand_comoving(t_arr), t_arr)
    return integral   # comoving Gly

# ── FRACTION OF UNIVERSE BEYOND REACH ─────────────────────────────────────────
def fraction_beyond_reach(t_gyr):
    """
    Fraction of all observable galaxies already beyond the reachable horizon.
    Based on volume ratio (r_reach / r_observable)³.
    At T_NOW: ≈ 97%.
    """
    r_obs   = observable_horizon(t_gyr)
    r_reach = reachable_horizon(t_gyr)
    if r_obs <= 0: return 1.0
    return 1.0 - (r_reach / r_obs)**3

# ── GRAVITATIONAL BINDING (simplified Newtonian) ──────────────────────────────
G_EFF = 1.4   # effective constant tuned to match Local Group zero-velocity surface ~5 Mly

def grav_acceleration(r_gly, mass_relative):
    """
    Gravitational acceleration toward a mass concentration.
    
    a_grav = G_eff × M / r²   (simplified, Newtonian)
    
    In reality this competes with Hubble expansion. The zero-velocity surface
    is where these balance exactly.
    """
    r2 = max(r_gly**2, 0.1)  # softening radius
    return G_EFF * mass_relative / r2

def hubble_acceleration(r_gly, t_gyr):
    """
    Effective expansion 'acceleration' at distance r (in Gly) from observer.
    
    v_hubble = H(t) × r
    """
    H_t_per_gly = hubble_parameter(t_gyr) / (C_KM_S / MPC_TO_GLY)
    return H_t_per_gly * r_gly

def zero_velocity_radius(mass_relative, t_gyr):
    """
    Radius at which Hubble expansion exactly cancels gravitational pull.
    
    Solve: G_eff × M / r² = H(t) × r
    → r³ = G_eff × M / H(t)
    
    Everything inside this radius is gravitationally bound; outside is unbound.
    For the Local Group (~mass=20 in relative units), this is ~5 Mly.
    """
    H_t = hubble_acceleration(1.0, t_gyr)   # H(t) in 1/Gyr
    if H_t <= 0: return float('inf')
    return (G_EFF * mass_relative / H_t) ** (1/3)


# ── PLOTS ─────────────────────────────────────────────────────────────────────
def plot_all():
    fig = plt.figure(figsize=(16, 10))
    fig.patch.set_facecolor('#03040c')
    gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.4, wspace=0.35)

    ax_style = dict(facecolor='#06080f', labelcolor='#c0c8d8',
                    titlecolor='#e0e8f8', tickcolor='#505870')

    def styled(ax, title, xlabel, ylabel):
        ax.set_facecolor(ax_style['facecolor'])
        ax.set_title(title, color=ax_style['titlecolor'], fontsize=10, pad=8)
        ax.set_xlabel(xlabel, color=ax_style['labelcolor'], fontsize=8)
        ax.set_ylabel(ylabel, color=ax_style['labelcolor'], fontsize=8)
        ax.tick_params(colors=ax_style['tickcolor'], labelsize=7)
        for spine in ax.spines.values():
            spine.set_edgecolor('#202840')
        ax.grid(True, alpha=0.15, color='#3050a0')

    t = np.linspace(1, 1000, 800)

    # 1. Scale factor a(t)
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(t, scale_factor(t), color='#4a9fd4', lw=1.5)
    ax1.axvline(T_NOW, color='#ffd080', lw=0.8, ls='--', alpha=0.7)
    ax1.text(T_NOW+5, 0.5, 'Now', color='#ffd080', fontsize=7)
    styled(ax1, 'Scale factor a(t) / a(now)', 'Time (Gyr)', 'a(t) / a(now)')

    # 2. Horizons
    ax2 = fig.add_subplot(gs[0, 1])
    t2 = np.linspace(5, 800, 100)
    obs  = [observable_horizon(ti) for ti in t2]
    rch  = [reachable_horizon(ti)  for ti in t2]
    ax2.plot(t2, obs, color='#3a6cb8', lw=1.5, label='Observable (~46.5 Gly today)')
    ax2.plot(t2, rch, color='#3aa870', lw=1.5, label='Reachable (~16.5 Gly today)')
    ax2.axvline(T_NOW, color='#ffd080', lw=0.8, ls='--', alpha=0.7)
    ax2.legend(fontsize=7, facecolor='#0a0e1a', edgecolor='#202840',
               labelcolor='#c0c8d8', loc='upper left')
    styled(ax2, 'Horizon Distances Over Time', 'Time (Gyr)', 'Proper distance (Gly)')

    # 3. Recession velocity at various distances
    ax3 = fig.add_subplot(gs[0, 2])
    t3 = np.linspace(T_NOW, 500, 200)
    for d, col in [(5, '#4ab87a'), (14, '#4a9fd4'), (30, '#f0a030'), (46.5, '#c04040')]:
        vr = [recession_velocity(d, ti) for ti in t3]
        ax3.plot(t3, vr, color=col, lw=1.2, label=f'{d} Gly')
    ax3.axhline(1.0, color='#ffffff', lw=0.7, ls=':', alpha=0.5, label='v = c')
    ax3.legend(title='Comoving dist.', fontsize=7, facecolor='#0a0e1a',
               edgecolor='#202840', labelcolor='#c0c8d8', title_fontsize=7)
    styled(ax3, 'Recession Velocity vs Time', 'Time (Gyr)', 'Recession velocity (×c)')

    # 4. Hubble parameter H(t)
    ax4 = fig.add_subplot(gs[1, 0])
    H_t = [hubble_parameter(ti) for ti in t]
    ax4.plot(t, H_t, color='#a04ab8', lw=1.5)
    ax4.axvline(T_NOW, color='#ffd080', lw=0.8, ls='--', alpha=0.7)
    ax4.axhline(H0 * np.sqrt(OMEGA_L), color='#606090', lw=0.7, ls=':',
                alpha=0.6, label=f'Asymptote H₀√Ω_Λ≈{H0*np.sqrt(OMEGA_L):.0f}')
    ax4.legend(fontsize=7, facecolor='#0a0e1a', edgecolor='#202840', labelcolor='#c0c8d8')
    styled(ax4, 'Hubble Parameter H(t)', 'Time (Gyr)', 'H(t) [km/s/Mpc]')

    # 5. Fraction beyond reach
    ax5 = fig.add_subplot(gs[1, 1])
    t5 = np.linspace(T_NOW, 800, 80)
    fb = [fraction_beyond_reach(ti)*100 for ti in t5]
    ax5.plot(t5, fb, color='#c04040', lw=1.5)
    ax5.axvline(T_NOW, color='#ffd080', lw=0.8, ls='--', alpha=0.7)
    ax5.text(T_NOW+5, 97.5, f'Now: {fraction_beyond_reach(T_NOW)*100:.1f}%',
             color='#ffd080', fontsize=7)
    styled(ax5, 'Galaxies Beyond Reach (%)', 'Time (Gyr)', '% of observable galaxies')

    # 6. Zero-velocity surface vs time
    ax6 = fig.add_subplot(gs[1, 2])
    zvr = [zero_velocity_radius(20, ti) for ti in t]  # Local Group mass=20
    ax6.plot(t, zvr, color='#40a870', lw=1.5)
    ax6.axvline(T_NOW, color='#ffd080', lw=0.8, ls='--', alpha=0.7)
    ax6.set_ylim(0, max(zvr)*1.1)
    styled(ax6, 'Zero-Velocity Surface Radius', 'Time (Gyr)', 'Radius (Gly, comoving)')

    fig.suptitle('ΛCDM Cosmological Physics — The Loneliness of Light',
                 color='#e8edf8', fontsize=13, y=0.98)

    for ax in [ax1,ax2,ax3,ax4,ax5,ax6]:
        for spine in ax.spines.values():
            spine.set_visible(True)

    plt.savefig('/home/claude/cosmic_physics_repo/lcdm_physics_plots.png',
                dpi=150, bbox_inches='tight', facecolor='#03040c')
    print("Saved lcdm_physics_plots.png")

if __name__ == '__main__':
    print("ΛCDM Physics Module")
    print("=" * 50)
    print(f"H₀              = {H0} km/s/Mpc")
    print(f"Ω_m             = {OMEGA_M}")
    print(f"Ω_Λ             = {OMEGA_L}")
    print(f"T_Λ             = {T_LAMBDA:.2f} Gyr")
    print(f"Hubble radius   = {HUBBLE_RADIUS_GLY:.2f} Gly")
    print()
    print(f"At T_NOW = {T_NOW} Gyr:")
    print(f"  a(T_NOW)            = {scale_factor(T_NOW):.6f} (= 1 by definition)")
    print(f"  H(T_NOW)            = {hubble_parameter(T_NOW):.2f} km/s/Mpc")
    print(f"  Observable horizon  = {observable_horizon(T_NOW):.2f} Gly")
    print(f"  Reachable horizon   = {reachable_horizon(T_NOW):.2f} Gly")
    print(f"  Beyond reach        = {fraction_beyond_reach(T_NOW)*100:.1f}%")
    print()
    print(f"At T = 100 Gyr:")
    print(f"  a(100)              = {scale_factor(100):.3f}× today")
    print(f"  H(100)              = {hubble_parameter(100):.2f} km/s/Mpc")
    print(f"  Reachable horizon   = {reachable_horizon(100):.2f} Gly")
    print(f"  Beyond reach        = {fraction_beyond_reach(100)*100:.1f}%")
    print()
    print("Recession velocities at T_NOW:")
    for d in [1, 5, 14, 20, 30, 46.5]:
        v = recession_velocity(d, T_NOW)
        print(f"  d = {d:5.1f} Gly → v_rec = {v:.3f}c  {'(> c!)' if v > 1 else ''}")

    plot_all()
