"""Generate the figures for the post "The geometry of the longest day".

Run with the conda env that has numpy/scipy/matplotlib, e.g.:
    /usr/local/Caskroom/miniforge/base/envs/wifi_analyzer/bin/python scripts/solstice_plots.py

Outputs SVGs into public/posts/solstice/ styled to match the site's paper palette.
"""

import os
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---- site palette -----------------------------------------------------------
PAPER = "#fbfaf8"
INK = "#221e17"
INK_SOFT = "#5c554a"
ACCENT = "#c34a22"
ACCENT_DEEP = "#1e3d52"
RULE = "#d8cfbc"

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

OUT = os.path.join(os.path.dirname(__file__), "..", "public", "posts", "solstice")
OUT = os.path.abspath(OUT)
os.makedirs(OUT, exist_ok=True)

DEG = np.pi / 180.0
EPS = 23.44  # obliquity of the ecliptic, degrees

# month tick positions (day-of-year at the first of each month, non-leap)
MONTH_STARTS = np.array([1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335])
MONTH_LABELS = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]
JUNE_SOLSTICE = 172  # ~21 June


def despine(ax, keep=("left", "bottom")):
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(side in keep)


def month_axis(ax):
    ax.set_xticks(MONTH_STARTS)
    ax.set_xticklabels(MONTH_LABELS)
    ax.set_xlim(1, 365)


# ---------------------------------------------------------------------------
# Low-precision solar position (US Naval Observatory algorithm).
# Returns declination (deg), ecliptic longitude (deg), equation of time (min).
# ---------------------------------------------------------------------------
N = np.arange(1, 366)
D = N - 1.0  # days since 1 Jan, 0h

L = (280.460 + 0.9856474 * D) % 360.0           # mean longitude of the Sun
g = (357.528 + 0.9856003 * D) % 360.0           # mean anomaly
lam = L + 1.915 * np.sin(g * DEG) + 0.020 * np.sin(2 * g * DEG)  # ecliptic longitude

dec = np.arcsin(np.sin(EPS * DEG) * np.sin(lam * DEG)) / DEG     # declination
alpha = np.arctan2(np.cos(EPS * DEG) * np.sin(lam * DEG), np.cos(lam * DEG)) / DEG
alpha = alpha % 360.0                                            # right ascension

eot = (L - alpha + 180.0) % 360.0 - 180.0
eot_min = eot * 4.0                                             # 1 deg = 4 minutes

print(f"declination range: {dec.min():.2f} .. {dec.max():.2f} deg")
print(f"equation of time range: {eot_min.min():.2f} .. {eot_min.max():.2f} min")


# ---------------------------------------------------------------------------
# Figure 1: schematic of declination on the celestial sphere.
# Equator and ecliptic drawn as great circles inclined by the obliquity,
# viewed obliquely; the Sun sits at the June solstice where delta = +eps.
# ---------------------------------------------------------------------------
rho = 28 * DEG            # viewing elevation (lean of the planes)
eps_r = EPS * DEG
t = np.linspace(0, 2 * np.pi, 500)


def project(X, Y, Z):
    """Orthographic projection after a tilt of rho about the x-axis."""
    return X, -Y * np.sin(rho) + Z * np.cos(rho)


# equator: a great circle in the Z = 0 plane
eqx, eqy = project(np.cos(t), np.sin(t), np.zeros_like(t))
# ecliptic: the equator rotated by -eps about the line of equinoxes (x-axis)
ecx, ecy = project(np.cos(t), np.sin(t) * np.cos(eps_r), -np.sin(t) * np.sin(eps_r))

fig, ax = plt.subplots(figsize=(6.2, 5.2))

# celestial-sphere outline
th = np.linspace(0, 2 * np.pi, 300)
ax.plot(np.cos(th), np.sin(th), color=RULE, lw=1.0)

# the two great circles
ax.plot(eqx, eqy, color=INK_SOFT, lw=1.7)
ax.plot(ecx, ecy, color=ACCENT, lw=2.0)

# equinoxes: the two crossings at (+/-1, 0)
for sx in (-1, 1):
    ax.plot(sx, 0, "o", ms=4.5, color=INK, mec="none")
ax.text(-1.07, 0.0, "equinox\n(δ = 0)", color=INK_SOFT, fontsize=9,
        ha="right", va="center")

# solstice points (top and bottom of the ecliptic)
sun_y = np.sin(rho + eps_r)          # June solstice screen height
foot_y = np.sin(rho)                 # its projection onto the equatorial plane
ax.plot(0, sun_y, "o", ms=9, color=ACCENT, mec=PAPER, mew=0.8)
ax.plot(0, -sun_y, "o", ms=5, color=ACCENT, alpha=0.5, mec="none")
ax.text(0.10, sun_y + 0.02, "Sun, June solstice", color=ACCENT, fontsize=10,
        ha="left", va="bottom")
ax.text(0.10, -sun_y - 0.02, "December solstice", color=INK_SOFT, fontsize=9,
        ha="left", va="top")

# declination of the solstice Sun: its angular height above the equatorial
# plane. The gap between the two circles is widest here and equals the
# obliquity, so at the June solstice the declination reaches +eps.
ax.annotate("", xy=(0.0, sun_y), xytext=(0.0, foot_y),
            arrowprops=dict(arrowstyle="<->", color=ACCENT_DEEP, lw=1.3))
ax.text(-0.07, (sun_y + foot_y) / 2, "δ = +ε", color=ACCENT_DEEP, fontsize=11,
        ha="right", va="center")

# small labels for the circles
ax.text(0.62, -0.46, "celestial equator", color=INK_SOFT, fontsize=9.5,
        ha="center", rotation=-15)
ax.text(-0.46, 0.60, "ecliptic", color=ACCENT, fontsize=10.5, ha="center",
        rotation=24)

# observer at the centre
ax.plot(0, 0, "o", ms=3.5, color=INK, mec="none")

ax.set_xlim(-1.25, 1.25)
ax.set_ylim(-1.2, 1.2)
ax.set_aspect("equal")
ax.axis("off")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "declination-geometry.svg"))
fig.savefig(os.path.join(OUT, "declination-geometry.png"), dpi=150)
plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 2: solar declination over the year, with the extrema marked.
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.2, 3.2))
ax.plot(N, dec, color=ACCENT, lw=1.6)
ax.axhline(0, color=RULE, lw=0.8)
ax.axhline(EPS, color=INK_SOFT, lw=0.7, ls=":")
ax.axhline(-EPS, color=INK_SOFT, lw=0.7, ls=":")
ax.axvline(JUNE_SOLSTICE, color=ACCENT_DEEP, lw=0.8, ls="--")
ax.set_ylim(-28, 28)
ax.set_yticks([-EPS, 0, EPS])
ax.set_yticklabels([r"$-\varepsilon$", "0", r"$+\varepsilon$"])
ax.set_ylabel("declination $\\delta$")
month_axis(ax)
despine(ax)
ax.text(JUNE_SOLSTICE - 4, 24.6, "June solstice", color=ACCENT_DEEP, ha="right",
        fontsize=10.5, style="italic")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "declination.svg"))
fig.savefig(os.path.join(OUT, "declination.png"), dpi=150)
plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 2: length of daylight over the year at several latitudes.
# ---------------------------------------------------------------------------
def day_length(phi_deg):
    x = -np.tan(phi_deg * DEG) * np.tan(dec * DEG)
    x = np.clip(x, -1.0, 1.0)
    H0 = np.arccos(x) / DEG          # half-day arc, degrees
    return 2.0 * H0 / 15.0           # hours (Earth turns 15 deg per hour)


lats = [(0, "Equator (0°)", INK_SOFT),
        (38, "Athens (38°N)", ACCENT),
        (60, "60°N", ACCENT_DEEP)]

fig, ax = plt.subplots(figsize=(7.2, 3.4))
for phi, label, col in lats:
    ax.plot(N, day_length(phi), color=col, lw=1.6, label=label)
ax.axhline(12, color=RULE, lw=0.8)
ax.axvline(JUNE_SOLSTICE, color=ACCENT_DEEP, lw=0.8, ls="--")
ax.set_ylim(7, 19)
ax.set_ylabel("daylight (hours)")
month_axis(ax)
despine(ax)
ax.legend(loc="upper right", frameon=False, fontsize=10, handlelength=1.4)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "daylight.svg"))
fig.savefig(os.path.join(OUT, "daylight.png"), dpi=150)
plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 3: the equation of time as the sum of two harmonics.
#   obliquity term  -> semiannual (period 6 months)
#   eccentricity term -> annual   (period 12 months)
# ---------------------------------------------------------------------------
B = (360.0 * (N - 81) / 365.0) * DEG
obl = 9.87 * np.sin(2 * B)                       # obliquity, semiannual
ecc = -7.53 * np.cos(B) - 1.5 * np.sin(B)        # eccentricity, annual
eot2 = obl + ecc

fig, ax = plt.subplots(figsize=(7.2, 3.4))
ax.axhline(0, color=RULE, lw=0.8)
ax.plot(N, obl, color=ACCENT_DEEP, lw=1.1, ls="--",
        label="obliquity (semiannual)")
ax.plot(N, ecc, color=INK_SOFT, lw=1.1, ls=":",
        label="eccentricity (annual)")
ax.plot(N, eot2, color=ACCENT, lw=1.8, label="equation of time (sum)")
ax.set_ylim(-18, 18)
ax.set_ylabel("minutes")
month_axis(ax)
despine(ax)
ax.legend(loc="lower center", frameon=False, fontsize=9.5, ncol=1,
          handlelength=1.8)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "equation-of-time.svg"))
fig.savefig(os.path.join(OUT, "equation-of-time.png"), dpi=150)
plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 4: the analemma — declination against the equation of time.
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(4.6, 5.4))
# close the annual loop so the curve does not break at the year boundary
ax.plot(np.append(eot_min, eot_min[0]), np.append(dec, dec[0]),
        color=ACCENT, lw=1.6)
ax.axvline(0, color=RULE, lw=0.8)
ax.axhline(0, color=RULE, lw=0.8)

# mark the solstices and equinoxes around the loop
marks = [(JUNE_SOLSTICE, "Jun solstice", "bottom"),
         (355, "Dec solstice", "top"),
         (80, "Mar equinox", "bottom"),
         (266, "Sep equinox", "top")]
for n, name, va in marks:
    i = n - 1
    ax.plot(eot_min[i], dec[i], "o", ms=4.5, color=ACCENT_DEEP, mec="none")
    dy = 1.6 if va == "bottom" else -1.6
    ax.text(eot_min[i] + 1.2, dec[i] + dy, name, color=ACCENT_DEEP,
            fontsize=9, va=va)

ax.set_xlim(-20, 20)
ax.set_ylim(-30, 30)
ax.set_xlabel("equation of time (min)")
ax.set_ylabel("declination $\\delta$ (deg)")
despine(ax)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "analemma.svg"))
fig.savefig(os.path.join(OUT, "analemma.png"), dpi=150)
plt.close(fig)


print("wrote:")
for name in ("declination-geometry.svg", "declination.svg", "daylight.svg",
             "equation-of-time.svg", "analemma.svg"):
    p = os.path.join(OUT, name)
    print(f"  {p}  ({os.path.getsize(p)} bytes)")
