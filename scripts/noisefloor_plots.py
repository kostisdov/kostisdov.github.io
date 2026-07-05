"""Generate the figures for the post "Beneath the noise floor".

Run with the conda env that has numpy/scipy/matplotlib, e.g.:
    /usr/local/Caskroom/miniforge/base/envs/wifi_analyzer/bin/python scripts/noisefloor_plots.py

Outputs SVGs into public/posts/beneath-the-noise-floor/ styled to match the
site's soft off-white paper palette.
"""

import os
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.special import erfc, comb

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
                   "beneath-the-noise-floor")
OUT = os.path.abspath(OUT)
os.makedirs(OUT, exist_ok=True)


def despine(ax, keep=("left", "bottom")):
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(side in keep)


def Q(x):
    """Gaussian tail probability."""
    return 0.5 * erfc(x / np.sqrt(2.0))


def save(fig, name):
    fig.savefig(os.path.join(OUT, name + ".svg"))
    fig.savefig(os.path.join(OUT, name + ".png"), dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 1: the Shannon plane. Spectral efficiency eta vs the minimum
# Eb/N0 (dB) required for reliable communication, from Eb/N0 = (2^eta - 1)/eta.
# The curve asymptotes to the -1.59 dB wall as eta -> 0.
# ---------------------------------------------------------------------------
eta = np.linspace(0.02, 8.0, 1200)
ebn0 = (np.power(2.0, eta) - 1.0) / eta   # linear
ebn0_db = 10.0 * np.log10(ebn0)
WALL = 10.0 * np.log10(np.log(2.0))       # -1.5917 dB

fig, ax = plt.subplots(figsize=(7.2, 4.6))

# achievable region: to the right of the bound curve
ax.fill_betweenx(eta, ebn0_db, 30, color=ACCENT, alpha=0.06, zorder=0)
ax.plot(ebn0_db, eta, color=ACCENT, lw=2.0, zorder=3,
        label=r"$E_b/N_0 = (2^{\eta}-1)/\eta$")

# the -1.59 dB wall
ax.axvline(WALL, color=ACCENT_DEEP, lw=1.2, ls="--", zorder=2)
ax.text(WALL + 0.4, 6.95, "Shannon wall  $-1.59$ dB", color=ACCENT_DEEP,
        fontsize=10, ha="left", va="top")

# eta = 1 divider between power- and bandwidth-limited regimes
ax.axhline(1.0, color=RULE, lw=0.9, zorder=1)
ax.text(20.5, 1.18, "bandwidth-limited  ($\\eta > 1$)", color=INK_SOFT,
        fontsize=9.5, ha="right", va="bottom")
ax.text(20.5, 0.82, "power-limited  ($\\eta < 1$)", color=INK_SOFT,
        fontsize=9.5, ha="right", va="top")

ax.text(11.5, 4.4, "achievable", color=ACCENT, fontsize=11, style="italic",
        ha="center")
ax.text(-1.0, 3.2, "not achievable", color=INK_SOFT, fontsize=10,
        style="italic", ha="right", rotation=90)

ax.set_xlim(-3, 21)
ax.set_ylim(0, 7.2)
ax.set_xlabel(r"$E_b/N_0$ required (dB)")
ax.set_ylabel(r"spectral efficiency  $\eta = R_b/W$  (bits/s/Hz)")
despine(ax)
save(fig, "shannon-plane")


# ---------------------------------------------------------------------------
# Figure 2: below the noise floor. Two PSD panels. Left: a signal spread over
# a wide band sits below the noise floor (negative in-band SNR). Right: after
# despreading it collapses to the symbol band and rises above the floor; the
# lift equals the processing gain 10 log10(SF). Signal PSDs are drawn as filled
# spectral shelves (Rectangle patches), whose top edge is the PSD level.
# ---------------------------------------------------------------------------
from matplotlib.patches import Rectangle

FLOOR = 0.0            # noise floor level (dB, arbitrary datum)
WIDE_LVL = -10.0       # pre-despread signal PSD, 10 dB below the floor
BASE = -15.0           # shelf baseline

fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.6, 3.6), sharey=True)

for ax in (axL, axR):
    ax.axhline(FLOOR, color=INK_SOFT, lw=1.3)
    ax.text(-5.8, FLOOR + 0.5, "noise floor  $N_0$", color=INK_SOFT, fontsize=9)
    ax.set_xlim(-6, 6)
    ax.set_ylim(-16, 14)
    ax.set_xlabel("frequency")
    ax.set_xticks([])

# --- left: wideband, pre-despread -----------------------------------------
axL.add_patch(Rectangle((-5, BASE), 10, WIDE_LVL - BASE, facecolor=ACCENT,
                        alpha=0.25, edgecolor=ACCENT, lw=1.6))
axL.annotate("", xy=(0, FLOOR), xytext=(0, WIDE_LVL),
             arrowprops=dict(arrowstyle="<->", color=ACCENT_DEEP, lw=1.1))
axL.text(0.3, (FLOOR + WIDE_LVL) / 2, r"SNR $=-10$ dB", color=ACCENT_DEEP,
         fontsize=9.5, ha="left", va="center")
axL.text(0, WIDE_LVL - 1.3, "signal over occupied band $W$",
         color=ACCENT, fontsize=9.5, ha="center", va="top")
axL.set_title("spread across $W$", fontsize=10.5, color=INK)
axL.set_ylabel("power spectral density (dB)")
despine(axL)
# bandwidth bracket: the full channel W
axL.annotate("", xy=(-5, 11.5), xytext=(5, 11.5),
             arrowprops=dict(arrowstyle="<->", color=INK_SOFT, lw=1.0))
axL.text(0, 12.1, "$W$", color=INK_SOFT, fontsize=10, ha="center", va="bottom")

# --- right: narrowband, post-despread -------------------------------------
# faint ghost of the pre-despread level, for the lift reference
axR.plot([-5, 5], [WIDE_LVL, WIDE_LVL], color=ACCENT, lw=1.0, ls=":",
         alpha=0.7)
axR.text(-5, WIDE_LVL + 0.5, "pre-despread level", color=ACCENT, fontsize=8.5,
         alpha=0.9, ha="left", va="bottom")
# despread signal: narrow shelf rising to the floor (SNR = 0 dB)
axR.add_patch(Rectangle((-0.7, BASE), 1.4, FLOOR - BASE, facecolor=ACCENT,
                        alpha=0.28, edgecolor=ACCENT, lw=1.6))
# processing-gain lift arrow
axR.annotate("", xy=(2.3, FLOOR), xytext=(2.3, WIDE_LVL),
             arrowprops=dict(arrowstyle="->", color=SAGE, lw=1.7))
axR.text(2.6, (FLOOR + WIDE_LVL) / 2,
         "processing gain\n" + r"$+10\log_{10}\text{SF}$", color=SAGE,
         fontsize=9.2, ha="left", va="center")
axR.text(0, FLOOR + 0.7, r"SNR $=0$ dB", color=ACCENT_DEEP, fontsize=9.5,
         ha="center", va="bottom")
axR.text(-3.1, -12.6, "signal in $W_\\text{info}$", color=ACCENT,
         fontsize=9.5, ha="center", va="center")
axR.annotate("", xy=(-0.75, -12.0), xytext=(-1.6, -12.6),
             arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.0))
axR.set_title("despread to $W_\\text{info}$", fontsize=10.5, color=INK)
despine(axR, keep=("bottom",))
axR.spines["left"].set_visible(False)
axR.tick_params(left=False)
# bandwidth bracket: the narrow information band (compare with W on the left)
axR.annotate("", xy=(-0.7, 11.5), xytext=(0.7, 11.5),
             arrowprops=dict(arrowstyle="<->", color=INK_SOFT, lw=1.2))
axR.text(1.1, 11.5, "$W_\\text{info}=W/\\text{SF}$", color=INK_SOFT, fontsize=9,
         ha="left", va="center")

fig.tight_layout()
save(fig, "below-floor")


print("wrote:")
for name in ("shannon-plane", "below-floor"):
    p = os.path.join(OUT, name + ".svg")
    print(f"  {p}  ({os.path.getsize(p)} bytes)")
