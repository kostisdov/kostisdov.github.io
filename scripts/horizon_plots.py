"""Generate the figures for the post "Beyond the horizon".

Run with the conda env that has numpy/scipy/matplotlib, e.g.:
    /usr/local/Caskroom/miniforge/base/envs/wifi_analyzer/bin/python scripts/horizon_plots.py

Outputs SVGs into public/posts/beyond-the-horizon/ styled to match the site's
soft off-white paper palette.
"""

import os
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# ---- site palette -----------------------------------------------------------
PAPER = "#fbfaf8"
INK = "#221e17"
INK_SOFT = "#5c554a"
ACCENT = "#c34a22"
ACCENT_DEEP = "#1e3d52"
RULE = "#d8cfbc"
SAGE = "#6f8b6a"

plt.rcParams.update(
    {
        "figure.facecolor": PAPER,
        "axes.facecolor": PAPER,
        "savefig.facecolor": PAPER,
        "font.family": "serif",
        "font.serif": ["Georgia", "Times New Roman", "DejaVu Serif"],
        "font.size": 12,
        "text.color": INK,
        "axes.edgecolor": RULE,
        "axes.labelcolor": INK_SOFT,
        "xtick.color": INK_SOFT,
        "ytick.color": INK_SOFT,
        "axes.linewidth": 0.8,
        "axes.grid": False,
        "svg.fonttype": "none",
    }
)

OUT = os.path.join(os.path.dirname(__file__), "..", "public", "posts",
                   "beyond-the-horizon")
OUT = os.path.abspath(OUT)
os.makedirs(OUT, exist_ok=True)

R_EARTH = 6371.0e3   # mean Earth radius, m


def despine(ax, keep=("left", "bottom")):
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(side in keep)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name + ".svg"))
    fig.savefig(os.path.join(OUT, name + ".png"), dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 1: the radio horizon from a single elevated terminal. The Earth
# surface curves away below the horizontal tangent at the antenna base by
# x^2/(2kR). A grazing ray from the antenna top is tangent to the surface at
# the horizon, at distance sqrt(2kRh). The 4/3-Earth (k=4/3) surface curves
# less than the geometric (k=1) one, so the radio horizon reaches further.
# ---------------------------------------------------------------------------
h_ant = 120.0                       # antenna height, m
xk = np.linspace(0, 52, 500)        # km


def drop_m(x_km, k):
    """Drop of the Earth surface (m) below the antenna-base tangent."""
    return -(x_km * 1e3) ** 2 / (2.0 * k * R_EARTH)


d_geo = 3.57 * np.sqrt(h_ant)       # geometric horizon, km
d_rad = 4.12 * np.sqrt(h_ant)       # radio horizon, km

fig, ax = plt.subplots(figsize=(7.4, 4.0))

# Earth surfaces
ax.fill_between(xk, drop_m(xk, 4.0 / 3.0), -260, color=RULE, alpha=0.30, lw=0)
ax.plot(xk, drop_m(xk, 4.0 / 3.0), color=SAGE, lw=1.8,
        label="4/3-Earth ($k=4/3$)")
ax.plot(xk, drop_m(xk, 1.0), color=INK_SOFT, lw=1.3, ls="--",
        label="geometric ($k=1$)")

# extra reach band
ax.axvspan(d_geo, d_rad, color=ACCENT, alpha=0.07, lw=0)

# antenna mast
ax.plot([0, 0], [0, h_ant], color=INK, lw=2.4)
ax.plot(0, h_ant, "o", ms=5, color=ACCENT, mec=PAPER, mew=0.8)
ax.text(0.9, 132, "drone, $h=120$ m", color=INK, fontsize=9, ha="left",
        va="bottom")

# grazing rays to each horizon
ax.plot([0, d_rad], [h_ant, drop_m(d_rad, 4.0 / 3.0)], color=ACCENT, lw=1.6)
ax.plot([0, d_geo], [h_ant, drop_m(d_geo, 1.0)], color=ACCENT_DEEP, lw=1.3,
        ls="--")

# horizon markers, labelled in the open sky above the rays (no overlap)
ax.plot(d_geo, drop_m(d_geo, 1.0), "o", ms=5, color=ACCENT_DEEP, mec=PAPER,
        mew=0.8, zorder=5)
ax.plot(d_rad, drop_m(d_rad, 4.0 / 3.0), "o", ms=5, color=ACCENT, mec=PAPER,
        mew=0.8, zorder=5)
ax.text(31, 98, f"radio horizon  $4.12\\sqrt{{h}}={d_rad:.0f}$ km",
        color=ACCENT, fontsize=9, ha="left", va="center")
ax.text(31, 66, f"geometric  $3.57\\sqrt{{h}}={d_geo:.0f}$ km",
        color=ACCENT_DEEP, fontsize=9, ha="left", va="center")
ax.text(d_rad * 0.40, h_ant * 0.42, "grazing ray", color=ACCENT, fontsize=9.5,
        rotation=-38, ha="center")

ax.set_xlim(-1.5, 52)
ax.set_ylim(-200, 155)
ax.set_xlabel("ground distance (km)")
ax.set_ylabel("height above / below antenna base (m)")
ax.legend(loc="lower left", frameon=False, fontsize=9, handlelength=1.8)
despine(ax, keep=("left",))
ax.spines["bottom"].set_visible(False)
ax.axhline(0, color=RULE, lw=0.8)
ax.tick_params(bottom=False, labelbottom=True)
fig.tight_layout()
save(fig, "earth-bulge")


# ---------------------------------------------------------------------------
# Figure 2: range versus antenna height. Radio horizon d = 4.12*sqrt(h) vs
# geometric 3.57*sqrt(h), for a drone-to-ground link with the ground terminal
# fixed at 2 m. The sqrt(h) law: doubling range needs 4x height.
# ---------------------------------------------------------------------------
h = np.linspace(1, 1000, 600)     # drone height, m
h_ground = 2.0
d_radio = 4.12 * (np.sqrt(h) + np.sqrt(h_ground))
d_geo = 3.57 * (np.sqrt(h) + np.sqrt(h_ground))

fig, ax = plt.subplots(figsize=(7.2, 4.0))
ax.fill_between(h, d_geo, d_radio, color=SAGE, alpha=0.12, lw=0)
ax.plot(h, d_radio, color=ACCENT, lw=2.0, label="radio horizon ($4.12\\sqrt{h}$)")
ax.plot(h, d_geo, color=INK_SOFT, lw=1.4, ls="--",
        label="geometric ($3.57\\sqrt{h}$)")

markers = [(30, "mast 30 m", 120, 14), (120, "drone 120 m", 250, 34),
           (500, "500 m", 620, 80)]
for hh, lbl, tx, ty in markers:
    dd = 4.12 * (np.sqrt(hh) + np.sqrt(h_ground))
    ax.plot(hh, dd, "o", ms=5, color=ACCENT_DEEP, mec=PAPER, mew=0.8, zorder=5)
    ax.annotate(f"{lbl}\n{dd:.0f} km", xy=(hh, dd), xytext=(tx, ty),
                color=ACCENT_DEEP, fontsize=8.6, ha="center", va="center",
                arrowprops=dict(arrowstyle="-", color=INK_SOFT, lw=0.7))

ax.set_xlim(0, 1000)
ax.set_ylim(0, 140)
ax.set_xlabel("drone height above ground (m), ground terminal at 2 m")
ax.set_ylabel("horizon range (km)")
ax.legend(loc="lower right", frameon=False, fontsize=9.5, handlelength=1.8)
despine(ax)
fig.tight_layout()
save(fig, "range-vs-height")


# ---------------------------------------------------------------------------
# Figure 3: path loss versus distance. Free-space (20 dB/decade) vs the full
# two-ray model, which oscillates below the breakpoint and settles onto the
# 40 dB/decade (d^4) asymptote above it. f = 900 MHz, h_t = 120 m, h_r = 2 m.
# ---------------------------------------------------------------------------
f_hz = 900e6
c = 3e8
lam = c / f_hz
ht, hr = 120.0, 2.0
d = np.logspace(np.log10(100), np.log10(100e3), 800)   # m, 0.1 .. 100 km

# free-space path loss (dB)
pl_fs = 20 * np.log10(4 * np.pi * d / lam)

# two-ray model: |1 + Gamma * exp(-j*dphi)|^2, Gamma = -1 (grazing)
d_los = np.sqrt(d**2 + (ht - hr) ** 2)
d_ref = np.sqrt(d**2 + (ht + hr) ** 2)
dphi = 2 * np.pi * (d_ref - d_los) / lam
E = np.abs(1.0 - 1.0 * np.exp(-1j * dphi))   # Gamma = -1
E = np.maximum(E, 1e-3)
pl_2ray = 20 * np.log10(4 * np.pi * d / lam) - 20 * np.log10(E)

d_bp = 4 * ht * hr / lam    # breakpoint distance, m

fig, ax = plt.subplots(figsize=(7.2, 4.2))
ax.plot(d / 1e3, pl_2ray, color=ACCENT, lw=1.3, alpha=0.9, label="two-ray")
ax.plot(d / 1e3, pl_fs, color=INK_SOFT, lw=1.6, ls="--", label="free space (20 dB/dec)")
# d^4 asymptote line for reference
pl_d4 = 40 * np.log10(d) - 20 * np.log10(ht) - 20 * np.log10(hr)
mask = d > d_bp
ax.plot(d[mask] / 1e3, pl_d4[mask], color=ACCENT_DEEP, lw=1.4, ls=":",
        label="$d^4$ asymptote (40 dB/dec)")

ax.axvline(d_bp / 1e3, color=SAGE, lw=1.0)
ax.text(d_bp / 1e3 * 1.1, 165, f"breakpoint\n$d_\\mathrm{{bp}}\\approx{d_bp/1e3:.1f}$ km",
        color=SAGE, fontsize=9, va="top")

ax.set_xscale("log")
ax.set_xlim(0.1, 100)
ax.set_ylim(70, 175)
ax.invert_yaxis()
ax.set_xlabel("distance (km)")
ax.set_ylabel("path loss (dB)")
ax.legend(loc="lower left", frameon=False, fontsize=9, handlelength=1.8)
despine(ax)
fig.tight_layout()
save(fig, "path-loss")


# ---------------------------------------------------------------------------
# Figure 4: knife-edge diffraction loss vs the Fresnel-Kirchhoff parameter nu
# (ITU-R P.526). nu < 0 is clearance, nu = 0 is grazing (6 dB), nu > 0 is
# obstruction (the shadow). 0.6 of the first Fresnel zone clear is nu ~ -0.8.
# ---------------------------------------------------------------------------
nu = np.linspace(-3, 5, 600)
# J(nu) diffraction loss in dB, ITU-R P.526 approximation for nu > -0.7
J = 6.9 + 20 * np.log10(np.sqrt((nu - 0.1) ** 2 + 1) + nu - 0.1)
J = np.where(nu > -0.78, J, 0.0)   # negligible loss well into clearance

fig, ax = plt.subplots(figsize=(7.2, 4.0))
ax.axvspan(0, 5, color=ACCENT, alpha=0.05, lw=0)
ax.plot(nu, J, color=ACCENT, lw=2.0)
ax.axvline(0, color=RULE, lw=0.9)

# grazing point
ax.plot(0, 6.0, "o", ms=5, color=ACCENT_DEEP, mec=PAPER, mew=0.8)
ax.text(0.18, 3.8, "grazing: 6 dB", color=ACCENT_DEEP, fontsize=9.5, ha="left",
        va="bottom")
# 0.6 F1 clearance, labelled below with a leader to avoid the top axis
ax.plot(-0.8, 0.3, "o", ms=5, color=SAGE, mec=PAPER, mew=0.8)
ax.annotate("0.6 F$_1$ clear\n(free space)", xy=(-0.8, 0.3), xytext=(-2.2, 11),
            color=SAGE, fontsize=8.8, ha="center", va="center",
            arrowprops=dict(arrowstyle="-", color=SAGE, lw=0.7))

ax.text(3.7, 9, "shadow\n(obstructed)", color=ACCENT, fontsize=10,
        style="italic", ha="center")
ax.text(-2.4, 26, "clearance", color=INK_SOFT, fontsize=10, style="italic",
        ha="center")

ax.set_xlim(-3, 5)
ax.set_ylim(-2, 34)
ax.invert_yaxis()
ax.set_xlabel(r"diffraction parameter  $\nu$")
ax.set_ylabel("diffraction loss (dB)")
despine(ax)
fig.tight_layout()
save(fig, "diffraction")


# ---------------------------------------------------------------------------
# Figure 5: the k-factor and the horizon. Horizon distance d = sqrt(2 k R h)
# vs k for a fixed height, showing sub-refraction (shortened), the standard
# 4/3 point, and super-refraction / ducting (extended). The 4/3 value is one
# point on a curve that the atmosphere slides along.
# ---------------------------------------------------------------------------
k = np.linspace(0.5, 3.0, 500)
h_fix = 120.0
d_h = np.sqrt(2 * k * R_EARTH * h_fix) / 1e3    # km

fig, ax = plt.subplots(figsize=(7.2, 4.0))
# regime shading
ax.axvspan(0.5, 1.0, color=ACCENT_DEEP, alpha=0.06, lw=0)
ax.axvspan(2.0, 3.0, color=SAGE, alpha=0.10, lw=0)
ax.plot(k, d_h, color=ACCENT, lw=2.0)

for kk, lbl, col in [(1.0, "no refraction\n($k=1$)", INK_SOFT),
                     (4.0 / 3.0, "standard\n($k=4/3$)", ACCENT_DEEP),
                     (2.0, "super-refraction", SAGE)]:
    dd = np.sqrt(2 * kk * R_EARTH * h_fix) / 1e3
    ax.plot(kk, dd, "o", ms=5, color=col, mec=PAPER, mew=0.8, zorder=5)
    ax.text(kk, dd + 3, lbl, color=col, fontsize=8.6, ha="center", va="bottom")

ax.text(0.72, 20, "sub-refraction\n(shortened)", color=ACCENT_DEEP,
        fontsize=8.8, ha="center", style="italic")
ax.text(2.6, 72, "ducting", color=SAGE, fontsize=9.5, ha="center",
        style="italic")

ax.set_xlim(0.5, 3.0)
ax.set_ylim(30, 80)
ax.set_xlabel(r"effective-Earth factor  $k$")
ax.set_ylabel("horizon range at $h=120$ m (km)")
despine(ax)
fig.tight_layout()
save(fig, "k-factor")


# ---------------------------------------------------------------------------
# Worked-budget numbers (printed for the post table; no figure).
# f = 900 MHz, d = 40 km, drone 120 m (P_tx 30 dBm, 2 dBi), ground yagi 10 dBi.
# Rb = 1 Mbit/s, NF = 5 dB, (Eb/N0)req = 8 dB, L_impl = 2 dB.
# ---------------------------------------------------------------------------
d0 = 40e3
pl_fs0 = 20 * np.log10(4 * np.pi * d0 / lam)
pl_2ray0 = 40 * np.log10(d0) - 20 * np.log10(ht) - 20 * np.log10(hr)
excess = pl_2ray0 - pl_fs0
P_r = 30.0 + 2.0 + 10.0 - pl_fs0 - excess
P_sens = -174.0 + 5.0 + 10 * np.log10(1e6) + 8.0 + 2.0
margin = P_r - P_sens

print("wrote:")
for name in ("earth-bulge", "range-vs-height", "path-loss", "diffraction",
             "k-factor"):
    p = os.path.join(OUT, name + ".svg")
    print(f"  {p}  ({os.path.getsize(p)} bytes)")

print(f"\nkey numbers: d_bp={d_bp/1e3:.2f} km, PL_fs(40km)={pl_fs0:.1f} dB, "
      f"PL_2ray(40km)={pl_2ray0:.1f} dB, excess={excess:.1f} dB, "
      f"P_r={P_r:.1f} dBm, P_sens={P_sens:.1f} dBm, margin={margin:.1f} dB, "
      f"radio horizon={4.12*(np.sqrt(ht)+np.sqrt(hr)):.1f} km")
