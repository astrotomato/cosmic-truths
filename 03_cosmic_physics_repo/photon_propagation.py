"""
Photon Propagation in Expanding Universe
=========================================
Simulates photon travel in ΛCDM spacetime.
A photon always travels at c, but the comoving distance it can cover
is limited by the event horizon.

Key physics:
  - Photon travels at c in proper distance
  - Comoving distance covered: dχ = c dt / a(t)
  - Photon can reach target only if it can cover the comoving distance before ∞
  - Event horizon = ∫_t^∞ c dt'/a(t') — FINITE in ΛCDM with Λ > 0

Coordinate note for 3D simulation:
  - Scene space = world space (no parent transform)
  - Clusters in cosmicGroup at local position P appear at world position a(t)·P
  - Photon starts at origin (Milky Way), travels in direction of target
  - Progress clamped to target distance — no overshoot
"""

import numpy as np
import matplotlib.pyplot as plt
from lcdm_physics import (
    T_NOW, C_GLY_GYR, scale_factor, reachable_horizon, observable_horizon,
    recession_velocity
)

def photon_comoving_distance(t_start, t_end, n=500):
    """
    Comoving distance a photon covers from t_start to t_end (Gyr).
    χ = c ∫_{t_start}^{t_end} dt / a(t)
    """
    t_arr = np.linspace(t_start, t_end, n)
    integrand = C_GLY_GYR / scale_factor(t_arr)
    return np.trapezoid(integrand, t_arr)

def can_photon_reach(comoving_dist_gly, t_fire=T_NOW):
    """
    Can a photon fired at t_fire ever reach an object at comoving distance d?
    Compare d to the event horizon (reachable horizon).
    """
    horizon = reachable_horizon(t_fire)
    return comoving_dist_gly <= horizon, horizon

def photon_trajectory(d_target_comoving, t_fire=T_NOW, n_steps=1000):
    """
    Simulate photon trajectory in proper distance vs time.
    
    Returns:
      t_arr      : time array (Gyr)
      proper_pos : photon proper distance from origin (Gly)
      target_pos : target proper distance from origin (grows with expansion)
      caught     : bool, whether photon catches target
    """
    t_max = t_fire + 200
    t_arr = np.linspace(t_fire, t_max, n_steps)
    dt    = t_arr[1] - t_arr[0]

    photon_comoving = 0.0
    comoving_history = [0.0]

    for i in range(1, len(t_arr)):
        dchi = C_GLY_GYR * dt / scale_factor(t_arr[i])
        photon_comoving += dchi
        comoving_history.append(photon_comoving)
        if photon_comoving >= d_target_comoving:
            t_arr = t_arr[:i+1]
            comoving_history = comoving_history[:i+1]
            break

    comoving_history = np.array(comoving_history)
    a_arr   = scale_factor(t_arr)
    photon_proper = comoving_history * a_arr
    target_proper = d_target_comoving * a_arr

    caught = photon_comoving >= d_target_comoving * 0.999
    return t_arr, photon_proper, target_proper, caught


def plot_photon_trajectories():
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor('#03040c')

    distances = [5, 14, 16.5, 20, 30, 46.5]
    colors     = ['#44c878', '#4a9fd4', '#ffd080', '#f0a030', '#e06030', '#c03020']
    labels     = ['5 Gly (inside reach)', 'Hubble radius ~14 Gly',
                  'Reachable limit ~16.5 Gly', '20 Gly',
                  '30 Gly', 'Observable edge ~46.5 Gly']

    horizon = reachable_horizon(T_NOW)

    # Left: proper distance trajectories
    ax1 = axes[0]
    ax1.set_facecolor('#06080f')
    for d, col, lbl in zip(distances, colors, labels):
        t, pp, tp, caught = photon_trajectory(d)
        ls = '-' if caught else '--'
        ax1.plot(t, pp, color=col, lw=1.5, ls=ls, label=f'{lbl}')
        ax1.plot(t, tp, color=col, lw=0.7, ls=':', alpha=0.5)
    ax1.axvline(T_NOW, color='#ffd080', lw=0.7, ls='--', alpha=0.6)
    ax1.set_title('Photon & Target Trajectories\n(solid=photon, dotted=receding target)',
                  color='#e0e8f8', fontsize=10, pad=6)
    ax1.set_xlabel('Time (Gyr)', color='#9098b8', fontsize=8)
    ax1.set_ylabel('Proper distance (Gly)', color='#9098b8', fontsize=8)
    ax1.legend(fontsize=7, facecolor='#0a0e1a', edgecolor='#303860',
               labelcolor='#c0c8d8', loc='upper left')
    ax1.tick_params(colors='#505870', labelsize=7)
    for s in ax1.spines.values(): s.set_edgecolor('#202840')
    ax1.grid(True, alpha=0.12, color='#3050a0')

    # Right: reachable horizon vs comoving distance
    ax2 = axes[1]
    ax2.set_facecolor('#06080f')
    t_arr = np.linspace(T_NOW, 500, 80)
    rh = [reachable_horizon(t) for t in t_arr]
    oh = [observable_horizon(t) for t in t_arr]
    ax2.plot(t_arr, rh, color='#44c878', lw=1.8, label='Reachable horizon')
    ax2.plot(t_arr, oh, color='#3a6cb8', lw=1.8, label='Observable horizon')
    ax2.fill_between(t_arr, rh, 0, alpha=0.08, color='#44c878')
    ax2.fill_between(t_arr, oh, rh, alpha=0.05, color='#3a6cb8')
    ax2.axvline(T_NOW, color='#ffd080', lw=0.7, ls='--', alpha=0.7)
    ax2.set_title('Observable vs Reachable Horizon\n(diverging as dark energy grows)',
                  color='#e0e8f8', fontsize=10, pad=6)
    ax2.set_xlabel('Time (Gyr)', color='#9098b8', fontsize=8)
    ax2.set_ylabel('Distance (Gly, comoving)', color='#9098b8', fontsize=8)
    ax2.legend(fontsize=8, facecolor='#0a0e1a', edgecolor='#303860', labelcolor='#c0c8d8')
    ax2.tick_params(colors='#505870', labelsize=7)
    for s in ax2.spines.values(): s.set_edgecolor('#202840')
    ax2.grid(True, alpha=0.12, color='#3050a0')

    fig.suptitle('Photon Propagation in ΛCDM Spacetime',
                 color='#e8edf8', fontsize=12, y=1.01)
    plt.tight_layout()
    plt.savefig('/home/claude/cosmic_physics_repo/photon_propagation.png',
                dpi=150, bbox_inches='tight', facecolor='#03040c')
    print("Saved photon_propagation.png")


if __name__ == '__main__':
    horizon = reachable_horizon(T_NOW)
    print("Photon Propagation Analysis")
    print("=" * 50)
    print(f"Event horizon at T_NOW: {horizon:.2f} Gly")
    print()
    for d in [5, 10, 14, 16.5, 20, 30, 46.5]:
        can, h = can_photon_reach(d)
        status = '✓ REACHABLE' if can else '✕ UNREACHABLE'
        v = recession_velocity(d, T_NOW)
        print(f"  d = {d:5.1f} Gly → {status}  (v_rec = {v:.2f}c)")
    plot_photon_trajectories()
