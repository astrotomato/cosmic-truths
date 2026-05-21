"""
pale_blue_dot_narrative_gif.py
A 5-scene narrative GIF: Universe → Galaxy → Solar System → Earth → Pale Blue Dot.
Each scene has a distinct visual style, scale text, and transitions.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Circle, FancyArrowPatch
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image, ImageDraw, ImageFont
import io, os

W, H = 900, 900
BG = '#010208'

# ── HELPERS ───────────────────────────────────────────────────────────────────

def fig_to_pil(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=fig.get_dpi(),
                facecolor=BG, edgecolor='none', bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    buf.seek(0)
    img = Image.open(buf).copy().convert('RGBA')
    buf.close()
    return img.resize((W, H), Image.LANCZOS)

def new_fig():
    fig = plt.figure(figsize=(W/100, H/100), dpi=100, facecolor=BG)
    return fig

def add_text(fig, text, x, y, size=13, color='#e8f0ff', alpha=1.0,
             style='normal', weight='normal', align='center', family='serif'):
    fig.text(x, y, text, ha=align, va='center', color=color,
             fontsize=size, style=style, fontweight=weight,
             alpha=alpha, fontfamily=family)

def add_scale_tag(fig, scale_text, y=0.06):
    fig.text(0.5, y, scale_text, ha='center', va='center',
             color='#2a4a6a', fontsize=8, fontfamily='monospace')

def lerp(a, b, t):
    return a + (b - a) * np.clip(t, 0, 1)

def ease(t):
    """Smooth ease in/out."""
    return t * t * (3 - 2 * t)

def seeded_rng(seed):
    return np.random.default_rng(seed)

# ── SCENE 1: OBSERVABLE UNIVERSE ──────────────────────────────────────────────

def scene_universe(t, enter_alpha=1.0):
    """Cosmic web. t = 0→1 is time within scene."""
    fig = new_fig()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(BG)
    ax.set_xlim(-1, 1); ax.set_ylim(-1, 1)
    ax.axis('off')

    rng = seeded_rng(42)

    # Voids (dark circles)
    void_data = [(-0.45, 0.1, 0.32), (0.35, -0.2, 0.26), (-0.1, 0.5, 0.22),
                 (0.6, 0.4, 0.18), (-0.6, -0.4, 0.20)]
    for vx, vy, vr in void_data:
        void = Circle((vx, vy), vr, color='#000408', zorder=1)
        ax.add_patch(void)
        void_ring = Circle((vx, vy), vr, color='#0a1820',
                            fill=False, lw=0.5, alpha=0.35, zorder=2)
        ax.add_patch(void_ring)

    # Filaments
    for _ in range(220):
        sx, sy = rng.uniform(-1.1, 1.1), rng.uniform(-1.1, 1.1)
        length = rng.uniform(0.08, 0.35)
        angle  = rng.uniform(0, np.pi)
        ex = sx + np.cos(angle)*length
        ey = sy + np.sin(angle)*length
        bright = rng.uniform(0.0, 0.5)
        col = (0.06+bright*0.12, 0.10+bright*0.16, 0.22+bright*0.28)
        alpha = rng.uniform(0.15, 0.45)
        ax.plot([sx, ex], [sy, ey], color=col, lw=rng.uniform(0.3,1.2),
                alpha=alpha, zorder=3)

    # Galaxy nodes
    nodes = [(0, 0, 1.0, True),  # Laniakea = us
             (-0.52, 0.18, 0.6, False), (0.48, -0.08, 0.55, False),
             (-0.28, 0.55, 0.5, False), (0.62, 0.32, 0.65, False),
             (0.12, -0.58, 0.45, False), (-0.65, -0.35, 0.5, False)]
    for nx, ny, ns, is_us in nodes:
        col = '#c8a050' if is_us else '#5a7aaa'
        s = (70 if is_us else 30) * ns
        ax.scatter([nx], [ny], s=s*enter_alpha, c=[col],
                   zorder=6, alpha=min(enter_alpha*0.9, 0.9))
        # Glow
        for gs, ga in [(s*5, 0.04), (s*2.5, 0.08)]:
            ax.scatter([nx], [ny], s=gs*enter_alpha, c=[col],
                       alpha=ga*enter_alpha, zorder=5)
        if is_us:
            ax.annotate('Laniakea\n(You are here)', (nx, ny),
                        xytext=(nx+0.10, ny+0.10),
                        color='#c8a050', fontsize=7, fontfamily='monospace',
                        alpha=enter_alpha*0.85,
                        arrowprops=dict(arrowstyle='->', color='#c8a050', lw=0.8))

    # Field galaxies
    fgx = rng.uniform(-1.0, 1.0, 2800)
    fgy = rng.uniform(-1.0, 1.0, 2800)
    dist = np.sqrt(fgx**2 + fgy**2)
    fg_col_r = 0.3 + dist*0.4; fg_col_g = 0.35 + dist*0.2; fg_col_b = 0.55 + dist*0.3
    ax.scatter(fgx, fgy, s=0.35*enter_alpha,
               c=np.stack([fg_col_r, fg_col_g, fg_col_b], axis=1).clip(0,1),
               alpha=0.55*enter_alpha, zorder=4)

    # Labels
    a = enter_alpha
    add_text(fig, 'The Observable Universe', 0.5, 0.935, size=19, color='#e8f0ff',
             alpha=a, style='italic', family='serif')
    add_text(fig, '93 billion light-years across  ·  ~2 trillion galaxies  ·  13.8 billion years old',
             0.5, 0.895, size=8.5, color='#3a5878', alpha=a, family='monospace')
    add_text(fig, 'Cosmic web of filaments, voids & galaxy clusters.',
             0.5, 0.86, size=8, color='#2a4060', alpha=a*0.9, family='monospace')
    add_scale_tag(fig, '1 cm ≈ 500 million light-years')

    return fig_to_pil(fig)

# ── SCENE 2: MILKY WAY GALAXY ─────────────────────────────────────────────────

def scene_galaxy(t, enter_alpha=1.0):
    fig = new_fig()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(BG)
    ax.set_xlim(-1.1, 1.1); ax.set_ylim(-1.1, 1.1)
    ax.axis('off')

    rng = seeded_rng(13)

    # Halo glow
    for r, a in [(0.85, 0.04), (0.65, 0.06), (0.45, 0.07)]:
        halo = Circle((0, 0), r, color='#c8b860', alpha=a, zorder=1)
        ax.add_patch(halo)

    # Spiral arms (4)
    arm_colors = ['#aabbdd', '#99aacc', '#bbccee', '#aabbd0']
    arm_starts = [0, np.pi/2, np.pi, 3*np.pi/2]
    for start, col in zip(arm_starts, arm_colors):
        for ii in range(280):
            frac = ii / 280
            angle = start + frac * 2.8 * np.pi
            radius = 0.06 + frac * 0.88
            spread = 0.025 + frac * 0.06
            ox = np.cos(angle)*radius + rng.uniform(-spread, spread)
            oy = np.sin(angle)*radius + rng.uniform(-spread, spread)
            s = (1 - frac) * 3.5 + 0.4
            ax.scatter([ox], [oy], s=s*enter_alpha, c=[col],
                       alpha=(0.3 + frac*0.2)*enter_alpha, zorder=3)

    # Bulge
    bx = rng.normal(0, 0.08, 600)
    by = rng.normal(0, 0.06, 600)
    ax.scatter(bx, by, s=0.8*enter_alpha, c='#ffe0a0',
               alpha=0.5*enter_alpha, zorder=4)

    # Our location marker
    sun_x, sun_y = 0.51, 0.03
    ax.scatter([sun_x], [sun_y], s=60*enter_alpha, c='#ffee80', zorder=8)
    for ss, sa in [(200, 0.06), (100, 0.10)]:
        ax.scatter([sun_x], [sun_y], s=ss*enter_alpha, c='#ffee80',
                   alpha=sa*enter_alpha, zorder=7)
    ax.annotate('You are\nhere', (sun_x, sun_y),
                xytext=(sun_x+0.18, sun_y+0.15),
                color='#ffcc60', fontsize=7, fontfamily='monospace',
                alpha=enter_alpha*0.85,
                arrowprops=dict(arrowstyle='->', color='#ffcc60', lw=0.8))

    # Arm labels
    for label, lx, ly in [('Perseus Arm', -0.3, 0.7), ('Orion Arm (us)', 0.72, 0.22),
                           ('Sagittarius Arm', 0.2, -0.65), ('Norma-Cygnus Arm', -0.6, -0.35)]:
        ax.text(lx, ly, label, color='#445566', fontsize=6.5,
                fontfamily='monospace', ha='center', alpha=enter_alpha*0.75)

    # Sgr A* marker
    ax.scatter([0], [0], s=25*enter_alpha, c='#ffffff', zorder=8, alpha=enter_alpha)
    ax.text(0.04, 0.05, 'Sgr A*', color='#888888', fontsize=6,
            fontfamily='monospace', alpha=enter_alpha*0.7)

    add_text(fig, 'The Milky Way Galaxy', 0.5, 0.935, size=19,
             color='#e8f0ff', alpha=enter_alpha, style='italic', family='serif')
    add_text(fig, '100,000 light-years across  ·  200–400 billion stars  ·  4 spiral arms',
             0.5, 0.895, size=8.5, color='#3a5878', alpha=enter_alpha, family='monospace')
    add_text(fig, 'A barred spiral galaxy  ·  Sgr A* (4M M☉) at centre  ·  ~225 Myr per orbit',
             0.5, 0.86, size=8, color='#2a4060', alpha=enter_alpha*0.9, family='monospace')
    add_scale_tag(fig, '1 cm ≈ 5,000 light-years')
    return fig_to_pil(fig)

# ── SCENE 3: SOLAR SYSTEM (3D Keplerian) ─────────────────────────────────────

def kepler_pos(a, i_d, Om_d, w_d, theta):
    i  = np.radians(i_d);  Om = np.radians(Om_d);  w = np.radians(w_d)
    u  = w + theta
    x = a*(np.cos(Om)*np.cos(u) - np.sin(Om)*np.sin(u)*np.cos(i))
    y = a*(np.sin(i)*np.sin(u))
    z = a*(np.sin(Om)*np.cos(u) + np.cos(Om)*np.sin(u)*np.cos(i))
    return x, y, z

PLANETS = [
    ("Mercury",  0.387,  0.241,  7.005,  48.33,  29.12,  "#c8a070", 0.030, 0.03),
    ("Venus",    0.723,  0.615,  3.395,  76.68,  54.88,  "#e8d070", 0.048, 177.4),
    ("Earth",    1.000,  1.000,  0.000,  0.00,  114.21,  "#3d7dca", 0.052, 23.44),
    ("Mars",     1.524,  1.881,  1.850,  49.56, 286.50,  "#dd5533", 0.035, 25.19),
    ("Jupiter",  5.203, 11.86,   1.303, 100.46, 273.87,  "#ddbb88", 0.160, 3.13),
    ("Saturn",   9.537, 29.46,   2.489, 113.64, 339.39,  "#e8d8a0", 0.135, 26.73),
    ("Uranus",  19.19,  84.01,   0.773,  74.00,  98.99,  "#78e8e0", 0.090, 97.77),
    ("Neptune", 30.07, 164.8,    1.770, 131.78, 276.34,  "#4466ee", 0.085, 28.32),
]

def scene_solar(t, enter_alpha=1.0, azim_offset=0):
    fig = plt.figure(figsize=(9, 9), dpi=100, facecolor=BG)
    ax = fig.add_subplot(111, projection='3d', facecolor=BG)

    time_yr = t * 10.0

    # Starfield — reduced for performance
    rng = seeded_rng(7)
    n = 200
    sx = rng.uniform(-38, 38, n); sy = rng.uniform(-38, 38, n); sz = rng.uniform(-38, 38, n)
    mask = np.sqrt(sx**2+sy**2+sz**2) > 34
    ax.scatter(sx[mask], sy[mask], sz[mask], c='white', s=0.35, alpha=0.30, zorder=0)

    # Ecliptic plane — subtle concentric rings + spokes
    th_grid = np.linspace(0, 2*np.pi, 200)
    for rr in [3,5,8,10,15,20,25,30]:
        ax.plot(np.cos(th_grid)*rr, np.zeros(200), np.sin(th_grid)*rr,
                color='#0d1e2e', lw=0.5, alpha=0.5, zorder=1)
    for spoke_a in np.linspace(0, 2*np.pi, 12, endpoint=False):
        ax.plot([0, np.cos(spoke_a)*32], [0,0], [0, np.sin(spoke_a)*32],
                color='#0d1e2e', lw=0.3, alpha=0.35, zorder=1)

    # Sun
    for ss, sa in [(600,0.05),(350,0.09),(180,0.15)]:
        ax.scatter([0],[0],[0], c='#fff0a0', s=ss, alpha=sa, zorder=9)
    ax.scatter([0],[0],[0], c='#fff8d0', s=80, zorder=10, alpha=1.0)

    # Asteroid belt
    rng2 = seeded_rng(22)
    ar = rng2.uniform(2.2, 3.2, 160)
    at = rng2.uniform(0, 2*np.pi, 160)
    ay = rng2.uniform(-0.08, 0.08, 160)
    ax.scatter(np.cos(at)*ar, ay, np.sin(at)*ar, c='#403830', s=0.6, alpha=0.45, zorder=2)

    # Orbits + planets
    th_orb = np.linspace(0, 2*np.pi, 360)
    for name, a, period, i_d, Om_d, w_d, col, r_v, axial in PLANETS:
        ox, oy, oz = kepler_pos(a, i_d, Om_d, w_d, th_orb)
        ax.plot(ox, oy, oz, color=col, lw=0.9, alpha=0.55, zorder=2)

        # Line of nodes (dashed)
        OmR = np.radians(Om_d)
        nl = a * 0.55
        ax.plot([-np.cos(OmR)*nl, np.cos(OmR)*nl], [0,0],
                [-np.sin(OmR)*nl, np.sin(OmR)*nl],
                color=col, lw=0.4, alpha=0.20, linestyle='--', zorder=2)

        # Planet position
        th_now = (2*np.pi*time_yr/period) % (2*np.pi)
        px, py, pz = kepler_pos(a, i_d, Om_d, w_d, th_now)

        sz_p = (r_v * 2400) * enter_alpha
        for ss, sa in [(sz_p*8,0.05),(sz_p*3,0.10),(sz_p,1.0)]:
            ax.scatter([px],[py],[pz], c=col, s=ss, alpha=sa*enter_alpha, zorder=8)

        # Spin axis — local to planet, shows axial tilt
        tilt_r = np.radians(axial)
        alen = r_v * 1.6 + 0.2
        # Spin axis in ecliptic coords (simplified: tilt in XY ecliptic plane)
        ax.plot([px - np.sin(tilt_r)*alen, px + np.sin(tilt_r)*alen],
                [py - np.cos(tilt_r)*alen, py + np.cos(tilt_r)*alen],
                [pz, pz],
                color=col, lw=1.2, alpha=0.85*enter_alpha, zorder=9)

        # Saturn ring
        if name == "Saturn":
            phi_r = np.linspace(0, 2*np.pi, 100)
            rr = a * 0.052
            tr = np.radians(axial)
            rx = px + rr*np.cos(phi_r)
            ry = py + rr*np.sin(phi_r)*np.sin(tr)
            rz = pz + rr*np.sin(phi_r)*np.cos(tr)
            ax.plot(rx, ry, rz, color='#e8d880', lw=1.5, alpha=0.75*enter_alpha, zorder=9)

        # Label
        off = r_v * 2.8 + 0.25
        ax.text(px+off, py+off*0.35, pz,
                name, color=col, fontsize=6, fontfamily='monospace',
                alpha=0.80*enter_alpha, zorder=11, fontweight='bold')

        # Uranus extra label (its tilt is dramatic — 97.77°)
        if name == "Uranus":
            ax.text(px, py+r_v*2.5, pz,
                    '↑ 97.8° axial tilt', color='#78e8e0',
                    fontsize=5.5, fontfamily='monospace', alpha=0.7*enter_alpha, zorder=11)

    # Camera
    # During this scene: slowly rise to show 3D depth
    elev = 18 + t * 14   # rises from 18° to 32°
    azim = (30 + azim_offset + t * 80) % 360
    ax.view_init(elev=elev, azim=azim)

    lim = 34
    ax.set_xlim(-lim,lim); ax.set_ylim(-lim,lim); ax.set_zlim(-lim,lim)
    ax.set_box_aspect([1,1,1])
    ax.axis('off')
    ax.xaxis.pane.fill=False; ax.yaxis.pane.fill=False; ax.zaxis.pane.fill=False
    ax.xaxis.pane.set_edgecolor('none'); ax.yaxis.pane.set_edgecolor('none'); ax.zaxis.pane.set_edgecolor('none')
    ax.grid(False)

    fig.text(0.5, 0.945, 'The Solar System', ha='center', color='#e8f0ff',
             fontsize=19, style='italic', fontfamily='serif', alpha=enter_alpha)
    fig.text(0.5, 0.910, '8 planets · 4.6 billion years old · Nearly coplanar ecliptic disk',
             ha='center', color='#3a5878', fontsize=8, fontfamily='monospace', alpha=enter_alpha)
    fig.text(0.5, 0.880, 'Orbital elements: JPL DE430  ·  Spin axes shown per planet  ·  True Keplerian 3D paths',
             ha='center', color='#2a4060', fontsize=7.5, fontfamily='monospace', alpha=enter_alpha*0.9)
    fig.text(0.5, 0.060, '1 unit = 1 AU (149.6 million km)  ·  Relative sizes not to scale',
             ha='center', color='#1a3050', fontsize=7.5, fontfamily='monospace', alpha=enter_alpha)
    return fig_to_pil(fig)

# ── SCENE 4: EARTH ─────────────────────────────────────────────────────────────

def scene_earth(t, enter_alpha=1.0):
    fig = new_fig()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(BG)
    ax.set_xlim(-1, 1); ax.set_ylim(-1, 1)
    ax.axis('off')

    rng = seeded_rng(55)

    # Stars
    sx = rng.uniform(-1,1,800); sy = rng.uniform(-1,1,800)
    bri = rng.uniform(0.15,0.7,800)
    cols = [(b,b,b) for b in bri]
    ax.scatter(sx, sy, s=0.5, c=cols, alpha=0.5)

    # Moon
    moon_angle = t * 2 * np.pi * 0.8
    moon_r = 0.62
    mx = np.cos(moon_angle) * moon_r * 0.7
    my = np.sin(moon_angle) * moon_r * 0.5
    ax.scatter([mx],[my], s=60*enter_alpha, c='#b8b4a8', zorder=5, alpha=enter_alpha)
    for ss, sa in [(200,0.04),(100,0.07)]:
        ax.scatter([mx],[my], s=ss*enter_alpha, c='#b8b4a8', alpha=sa*enter_alpha, zorder=4)
    ax.text(mx+0.06, my+0.05, 'Moon\n384,400 km', color='#8a8680',
            fontsize=6.5, fontfamily='monospace', alpha=enter_alpha*0.8, ha='center')

    # Moon orbit path
    mo_th = np.linspace(0, 2*np.pi, 200)
    ax.plot(np.cos(mo_th)*moon_r*0.7, np.sin(mo_th)*moon_r*0.5,
            color='#1a2a3a', lw=0.6, alpha=0.5)

    # Earth
    earth_r = 0.22
    r_size = earth_r * (0.9 + 0.1 * t)  # slight zoom
    earth = Circle((0, 0), r_size, color='#1a3a8a', zorder=6, alpha=enter_alpha)
    ax.add_patch(earth)

    # Continents (rough suggestive shapes)
    for (cx, cy, cr, crot) in [
        (0.04, 0.10, 0.055, 0), (-0.12, 0.00, 0.04, 0.3),
        (0.09, -0.06, 0.035, 0.5), (-0.05, -0.10, 0.028, 0.7),
        (0.13, 0.04, 0.030, 1.2)
    ]:
        # Only draw if within Earth circle
        if np.sqrt(cx**2+cy**2) < r_size * 0.85:
            cont = mpatches.Ellipse((cx, cy), cr*1.5, cr*0.8,
                                    angle=np.degrees(crot), color='#2a6a2a',
                                    alpha=0.55*enter_alpha, zorder=7)
            ax.add_patch(cont)

    # Atmosphere glow
    for ar_r, ar_a in [(r_size*1.15, 0.04), (r_size*1.08, 0.07)]:
        atm = Circle((0, 0), ar_r, color='#3366bb', alpha=ar_a*enter_alpha,
                     fill=True, zorder=5)
        ax.add_patch(atm)

    # Terminator line
    tx = np.cos(np.linspace(-np.pi/2, np.pi/2, 100)) * r_size
    ty = np.sin(np.linspace(-np.pi/2, np.pi/2, 100)) * r_size
    ax.plot(tx, ty, color='#334455', lw=0.5, alpha=0.4*enter_alpha, zorder=8)

    # ISS orbit
    iss_r = r_size * 1.07
    iss_th = np.linspace(0, 2*np.pi, 200)
    ax.plot(np.cos(iss_th)*iss_r, np.sin(iss_th)*iss_r*0.85,
            color='#2244aa', lw=0.4, alpha=0.4*enter_alpha, linestyle='--')

    # Arrow to text
    ax.annotate('12,742 km diameter\n7.9 km/s orbital speed',
                (r_size*0.7, r_size*0.7),
                xytext=(0.50, 0.60),
                color='#5588aa', fontsize=7, fontfamily='monospace',
                alpha=enter_alpha*0.85,
                arrowprops=dict(arrowstyle='->', color='#5588aa', lw=0.7))

    # Lagrange points (L4, L5 faint)
    for lx, lz, ll in [(moon_r*0.35, moon_r*0.6, 'L4'), (moon_r*0.35, -moon_r*0.6, 'L5')]:
        ax.scatter([lx],[lz], s=8*enter_alpha, c='#3a6a4a', alpha=0.5*enter_alpha, zorder=4)
        ax.text(lx+0.04, lz, ll, color='#3a6a4a', fontsize=5.5,
                fontfamily='monospace', alpha=0.6*enter_alpha)

    add_text(fig, 'The Earth–Moon System', 0.5, 0.935, size=19,
             color='#e8f0ff', alpha=enter_alpha, style='italic', family='serif')
    add_text(fig, 'Earth: 12,742 km · Moon: 384,400 km away · ISS at 408 km altitude',
             0.5, 0.895, size=8.5, color='#3a5878', alpha=enter_alpha, family='monospace')
    add_text(fig, '5 Lagrange gravitational equilibrium points (L4, L5 are stable)',
             0.5, 0.860, size=8, color='#2a4060', alpha=enter_alpha*0.9, family='monospace')
    add_scale_tag(fig, '1 cm ≈ 50,000 km')
    return fig_to_pil(fig)

# ── SCENE 5: PALE BLUE DOT ────────────────────────────────────────────────────

def scene_pale_blue_dot(t, enter_alpha=1.0):
    fig = new_fig()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(BG)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis('off')

    rng = seeded_rng(88)

    # Stars
    sx = rng.uniform(0,1,400); sy = rng.uniform(0,1,400)
    bri = rng.uniform(0.1,0.55,400)
    ax.scatter(sx, sy, s=0.4, c=[(b,b,b) for b in bri], alpha=0.4)

    # Voyager sunbeam — diffuse Gaussian scatter column, not a hard stripe
    # The real photo has scattered sunlight creating a soft vertical wash
    beam_alpha = min(t * 2.2, 1.0) * enter_alpha * 0.5
    if beam_alpha > 0.01:
        beam_rng = seeded_rng(101)
        n_beam = 900
        bx = beam_rng.normal(0.506, 0.005, n_beam)
        by = beam_rng.uniform(0.0, 1.0, n_beam)
        dist_c = np.abs(bx - 0.506)
        a_beam = np.exp(-dist_c / 0.0035) * beam_alpha * 0.28
        # vectorised scatter — group into opacity bands
        for opacity_lo, opacity_hi in [(0.05, 0.15), (0.01, 0.05)]:
            mask = (a_beam >= opacity_lo) & (a_beam < opacity_hi)
            if mask.any():
                ax.scatter(bx[mask], by[mask], s=0.5,
                           c=['#c4a858']*int(mask.sum()),
                           alpha=float(np.mean(a_beam[mask])), zorder=3)

    # The Dot — appears with a pulse at t=0.4
    dot_scale = ease(np.clip((t - 0.2) * 2.5, 0, 1)) * enter_alpha
    dot_x, dot_y = 0.506, 0.435
    for ds, da in [(400, 0.03), (180, 0.06), (70, 0.12), (22, 0.40), (6, 1.0)]:
        ax.scatter([dot_x], [dot_y], s=ds*dot_scale,
                   c=['#6090c0'], alpha=da*dot_scale, zorder=8)

    # Quote — lines fade in one by one
    quote_lines = [
        '"Look again at that dot.',
        "That's here. That's home. That's us.",
        'On it everyone you love, everyone you know,',
        'everyone you ever heard of,',
        'every human being who ever was,',
        'lived out their lives."',
    ]
    attr_line = '— Carl Sagan,  Pale Blue Dot,  1994'

    quote_start = 0.30
    for qi, line in enumerate(quote_lines):
        line_t = np.clip((t - quote_start - qi * 0.09) * 6, 0, 1)
        line_alpha = ease(line_t) * enter_alpha
        if line_alpha > 0.01:
            fig.text(0.5, 0.82 - qi * 0.055, line,
                     ha='center', va='center',
                     color='#b8c8e0', fontsize=10.5,
                     style='italic', fontfamily='serif',
                     alpha=line_alpha)

    attr_t = np.clip((t - quote_start - len(quote_lines)*0.09 - 0.05) * 5, 0, 1)
    attr_alpha = ease(attr_t) * enter_alpha
    if attr_alpha > 0.01:
        fig.text(0.5, 0.82 - len(quote_lines)*0.055 - 0.05, attr_line,
                 ha='center', va='center',
                 color='#4a6888', fontsize=7.5,
                 fontfamily='monospace', alpha=attr_alpha)

    # Scale tag
    scale_t = np.clip((t - 0.15) * 3, 0, 1) * enter_alpha
    if scale_t > 0.01:
        fig.text(0.5, 0.09,
                 'Voyager 1 · February 14, 1990 · Distance: 40.5 AU (6.06 billion km)',
                 ha='center', color='#1e3850', fontsize=7, fontfamily='monospace',
                 alpha=scale_t)
        fig.text(0.5, 0.06,
                 'Earth is 0.12 arcseconds across — less than one pixel in the original photograph.',
                 ha='center', color='#162838', fontsize=6.5, fontfamily='monospace',
                 alpha=scale_t*0.8)

    return fig_to_pil(fig)

# ── TRANSITION ────────────────────────────────────────────────────────────────

def blend(img_a, img_b, t):
    """Cross-dissolve two PIL images."""
    t = float(np.clip(t, 0, 1))
    a_arr = np.array(img_a, dtype=np.float32)
    b_arr = np.array(img_b, dtype=np.float32)
    blended = (a_arr * (1-t) + b_arr * t).clip(0,255).astype(np.uint8)
    return Image.fromarray(blended)

# ── MAIN SEQUENCE ──────────────────────────────────────────────────────────────

def generate():
    print("Generating narrative GIF...")
    frames = []
    FPS  = 12
    FADE = 6

    def add_scene(render_fn, n_frames, **kwargs):
        for fi in range(n_frames):
            t = fi / max(n_frames - 1, 1)
            img = render_fn(t, **kwargs)
            frames.append(img)
            if fi % max(n_frames//3, 1) == 0:
                pct = int(fi/n_frames*100)
                print(f"  {render_fn.__name__}  {pct}%")

    def add_fade(fn_a, fn_b, **kw_b):
        for fi in range(FADE):
            t = fi / (FADE - 1)
            frames.append(blend(fn_a(1.0), fn_b(0.0, **kw_b), ease(t)))

    add_scene(scene_universe,       18)
    add_fade(scene_universe,        scene_galaxy)
    add_scene(scene_galaxy,         16)
    add_fade(scene_galaxy,          scene_solar)
    add_scene(scene_solar,          22)   # most expensive — keep low
    add_fade(scene_solar,           scene_earth)
    add_scene(scene_earth,          16)
    add_fade(scene_earth,           scene_pale_blue_dot)
    add_scene(scene_pale_blue_dot,  26)
    last = frames[-1].copy()
    for _ in range(10):
        frames.append(last)

    print(f"Total frames: {len(frames)}")
    out = '/mnt/user-data/outputs/pale_blue_dot.gif'
    frames[0].save(
        out,
        save_all=True,
        append_images=frames[1:],
        duration=int(1000/FPS),
        loop=0,
        optimize=False,
    )
    size_mb = os.path.getsize(out)/1e6
    print(f"Saved → {out}  ({size_mb:.1f} MB, {len(frames)} frames)")

generate()
PYEOF
