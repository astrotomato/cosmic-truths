"""
Vector Field Simulation: Hubble Expansion vs Gravitational Binding
==================================================================
Models the competition between Hubble expansion and gravity at every
point in space. The zero-velocity surface (where they cancel) is the
true boundary of gravitationally bound structures.

Physics:
  v_hubble(r) = H(t) · r              [outward, linear in distance]
  v_grav(r)   = G_eff · M / r²        [inward, inverse-square]
  v_net(r)    = v_hubble - v_grav

Key insight: there is NO centre of the universe.
Every observer sees the same Hubble flow radiating outward from themselves.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from lcdm_physics import (
    H0, OMEGA_M, OMEGA_L, C_KM_S, MPC_TO_GLY, T_NOW,
    scale_factor, hubble_parameter, recession_velocity, zero_velocity_radius
)

G_EFF   = 1.4    # effective gravitational constant (display units)
MASS_LG = 20.0   # Local Group mass (relative units, ~5×10¹² M_sun)

# Real mass concentrations (display units, comoving coordinates)
ATTRACTORS = [
    dict(name='Local Group',      pos=np.array([0.0,   0.0 ]), mass=20,  bound=True ),
    dict(name='Virgo Cluster',    pos=np.array([8.3,   6.1 ]), mass=80,  bound=False),
    dict(name='Hydra-Centaurus',  pos=np.array([-6.2,  8.1 ]), mass=60,  bound=False),
    dict(name='Shapley Attractor',pos=np.array([14.2,  13.0]), mass=300, bound=False),
    dict(name='Coma Cluster',     pos=np.array([13.9, -9.8 ]), mass=30,  bound=False),
]

def hubble_vec(point, observer, t_gyr):
    """
    Hubble velocity vector at `point` as seen by `observer`.
    
    v = H(t) · (point - observer)
    
    Crucially: the origin is the OBSERVER, not any special cosmic centre.
    Every point in the universe sees the same flow radiating from itself.
    """
    H_t = hubble_parameter(t_gyr)
    H_norm = H_t / (C_KM_S / MPC_TO_GLY)   # convert to 1/Gyr
    relative = point - observer
    return relative * H_norm * 0.022   # 0.022 = display scale factor

def grav_vec(point, t_gyr):
    """
    Net gravitational acceleration at `point` from all mass concentrations.
    
    a = Σ_i  G_eff · M_i / |r_i|² · r̂_i
    
    Falls off as 1/r². Gravity weakens as matter dilutes: ∝ 1/a(t)^0.5
    """
    a = scale_factor(t_gyr)
    grav_scale = G_EFF / (a ** 0.5)   # dilution with expansion
    net = np.zeros(2)
    for att in ATTRACTORS:
        delta = att['pos'] - point
        dist2 = max(np.dot(delta, delta), 0.5)
        mag   = grav_scale * att['mass'] / dist2
        net  += mag * delta / np.sqrt(dist2)
    return net

def net_vec(point, observer, t_gyr):
    """Net force = Hubble expansion − gravitational binding."""
    return hubble_vec(point, observer, t_gyr) - grav_vec(point, t_gyr)

def find_zero_velocity_surface(observer, t_gyr, n_angles=360, r_max=40):
    """
    Find the zero-velocity surface — where net radial force = 0.
    Returns array of (x, y) points on the surface.
    """
    surface_pts = []
    for deg in range(n_angles):
        angle = np.radians(deg)
        direction = np.array([np.cos(angle), np.sin(angle)])
        # Binary search for zero crossing
        lo, hi = 0.5, r_max
        for _ in range(25):
            mid = (lo + hi) / 2
            pt  = observer + direction * mid
            nv  = net_vec(pt, observer, t_gyr)
            # Project net velocity onto radial direction
            radial = np.dot(nv, direction)
            if radial > 0:   # expansion winning
                hi = mid
            else:            # gravity winning
                lo = mid
        surface_pts.append(observer + direction * ((lo + hi) / 2))
    return np.array(surface_pts)


def plot_vector_fields(t_gyr=T_NOW):
    fig, axes = plt.subplots(1, 3, figsize=(18, 7))
    fig.patch.set_facecolor('#03040c')

    observer = np.array([0.0, 0.0])
    grid_r = np.linspace(-35, 35, 22)
    X, Y = np.meshgrid(grid_r, grid_r)
    U_hub = np.zeros_like(X); V_hub = np.zeros_like(X)
    U_grv = np.zeros_like(X); V_grv = np.zeros_like(X)
    U_net = np.zeros_like(X); V_net = np.zeros_like(X)
    SPD_h = np.zeros_like(X); SPD_g = np.zeros_like(X); SPD_n = np.zeros_like(X)

    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            pt = np.array([X[i,j], Y[i,j]])
            if np.linalg.norm(pt) < 1.5: continue
            hv = hubble_vec(pt, observer, t_gyr)
            gv = grav_vec(pt, t_gyr)
            nv = net_vec(pt, observer, t_gyr)
            U_hub[i,j], V_hub[i,j] = hv; SPD_h[i,j] = np.linalg.norm(hv)
            U_grv[i,j], V_grv[i,j] = gv; SPD_g[i,j] = np.linalg.norm(gv)
            U_net[i,j], V_net[i,j] = nv; SPD_n[i,j] = np.linalg.norm(nv)

    # Find zero-velocity surface
    zvs = find_zero_velocity_surface(observer, t_gyr)

    titles  = ['Hubble Expansion Field', 'Gravitational Binding Field', 'Net Force Field']
    Us      = [U_hub, U_grv, U_net]
    Vs      = [V_hub, V_grv, V_net]
    SPDs    = [SPD_h, SPD_g, SPD_n]
    colors  = ['Blues',  'Oranges', 'Greens']
    acolors = ['#4a9fd4', '#d45030', '#44c878']

    for idx, (ax, title, U, V, SPD, cmap, ac) in enumerate(
            zip(axes, titles, Us, Vs, SPDs, colors, acolors)):
        ax.set_facecolor('#06080f')
        ax.set_aspect('equal')
        norm_spd = SPD / (SPD.max() + 1e-9)
        ax.quiver(X, Y, U, V, norm_spd, cmap=cmap, alpha=0.75,
                  scale=3.5, width=0.003, headwidth=4, headlength=5)
        # Zero-velocity surface (net field only)
        if idx == 2:
            ax.plot(zvs[:,0], zvs[:,1], 'w-', lw=1.2, alpha=0.6,
                    label='Zero-velocity surface')
            ax.legend(fontsize=8, facecolor='#0a0e1a', edgecolor='#303860',
                      labelcolor='white', loc='upper right')
        # Attractors
        for att in ATTRACTORS:
            sz = max(40, att['mass'] / 5)
            col = '#ffd080' if att['name'] == 'Local Group' else '#d4a050'
            ax.scatter(*att['pos'], s=sz, c=col, zorder=5, alpha=0.9)
            ax.annotate(att['name'].split()[0], att['pos'],
                        fontsize=6, color='#909ab8', ha='center',
                        xytext=(0, 8), textcoords='offset points')
        # Observer
        ax.scatter(*observer, s=80, c='#ffffff', marker='*', zorder=10)
        ax.set_xlim(-36, 36); ax.set_ylim(-36, 36)
        ax.set_title(title, color='#e0e8f8', fontsize=10, pad=6)
        ax.set_xlabel('Comoving distance (Gly)', color='#9098b8', fontsize=8)
        ax.tick_params(colors='#505870', labelsize=7)
        for spine in ax.spines.values():
            spine.set_edgecolor('#202840')
        ax.grid(True, alpha=0.1, color='#3050a0')

    a_now = scale_factor(t_gyr)
    fig.suptitle(
        f'Hubble vs Gravity Vector Fields  ·  T = {t_gyr:.1f} Gyr  ·  a = {a_now:.3f}',
        color='#e8edf8', fontsize=12, y=0.98)
    plt.savefig('/home/claude/cosmic_physics_repo/vector_fields.png',
                dpi=150, bbox_inches='tight', facecolor='#03040c')
    print("Saved vector_fields.png")


def plot_zvs_over_time():
    """Show how the zero-velocity surface shrinks as dark energy takes over."""
    fig, ax = plt.subplots(figsize=(10, 7))
    fig.patch.set_facecolor('#03040c')
    ax.set_facecolor('#06080f')

    times = [T_NOW, 30, 60, 100, 200, 500]
    colors = ['#ffd080', '#e0a040', '#c06030', '#a04020', '#802010', '#601008']

    observer = np.array([0.0, 0.0])
    for t, col in zip(times, colors):
        try:
            zvs = find_zero_velocity_surface(observer, t, n_angles=180)
            ax.plot(zvs[:,0], zvs[:,1], '-', color=col, lw=1.4,
                    label=f'T = {t:.0f} Gyr  (a={scale_factor(t):.2f}×)', alpha=0.85)
        except Exception as e:
            print(f"ZVS failed at T={t}: {e}")

    ax.scatter(0, 0, s=100, c='white', marker='*', zorder=10, label='Observer (Milky Way)')
    ax.set_aspect('equal')
    ax.set_xlim(-15, 15); ax.set_ylim(-15, 15)
    ax.set_title('Zero-Velocity Surface Over Time\n'
                 'Inside: gravity wins (bound). Outside: expansion wins (unbound).',
                 color='#e0e8f8', fontsize=11, pad=8)
    ax.set_xlabel('Comoving distance (Gly)', color='#9098b8', fontsize=9)
    ax.set_ylabel('Comoving distance (Gly)', color='#9098b8', fontsize=9)
    ax.tick_params(colors='#505870', labelsize=8)
    ax.grid(True, alpha=0.12, color='#3050a0')
    for spine in ax.spines.values(): spine.set_edgecolor('#202840')
    ax.legend(fontsize=8, facecolor='#0a0e1a', edgecolor='#303860', labelcolor='#c0c8d8')
    plt.savefig('/home/claude/cosmic_physics_repo/zero_velocity_surface.png',
                dpi=150, bbox_inches='tight', facecolor='#03040c')
    print("Saved zero_velocity_surface.png")


if __name__ == '__main__':
    print("Hubble vs Gravity Vector Fields")
    print("=" * 50)
    observer = np.array([0., 0.])
    zvs = find_zero_velocity_surface(observer, T_NOW, n_angles=36)
    radii = np.linalg.norm(zvs, axis=1)
    print(f"Zero-velocity surface radius (T_NOW): {radii.mean():.2f} ± {radii.std():.2f} Gly")
    print(f"Approx ZVS from analytic formula: {zero_velocity_radius(MASS_LG, T_NOW):.2f} Gly")
    print()
    for d in [1, 3, 5, 10, 20]:
        pt = np.array([d, 0.])
        hv = hubble_vec(pt, observer, T_NOW)
        gv = grav_vec(pt, T_NOW)
        nv = net_vec(pt, observer, T_NOW)
        print(f"  r={d:2d} Gly: |Hubble|={np.linalg.norm(hv):.4f}  |Grav|={np.linalg.norm(gv):.4f}  |Net|={np.linalg.norm(nv):.4f}  ({'BOUND' if np.dot(nv,[1,0])<0 else 'UNBOUND'})")
    plot_vector_fields()
    plot_zvs_over_time()
