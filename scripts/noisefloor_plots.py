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
axL.text(0, WIDE_LVL - 1.3, "signal, spread over $W_\\text{wide}$",
         color=ACCENT, fontsize=9.5, ha="center", va="top")
axL.set_title("pre-despread (wideband)", fontsize=10.5, color=INK)
axL.set_ylabel("power spectral density (dB)")
despine(axL)

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
axR.text(-3.1, -12.6, "signal, in $W_\\text{sym}$", color=ACCENT,
         fontsize=9.5, ha="center", va="center")
axR.annotate("", xy=(-0.75, -12.0), xytext=(-1.6, -12.6),
             arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.0))
axR.set_title("post-despread (narrowband)", fontsize=10.5, color=INK)
despine(axR, keep=("bottom",))
axR.spines["left"].set_visible(False)
axR.tick_params(left=False)

fig.tight_layout()
save(fig, "below-floor")


# ---------------------------------------------------------------------------
# Figure 3: coding vs diversity. Left (AWGN): uncoded BPSK, which coincides with
# repetition + MRC; the Shannon wall; the coding-gain gap that real FEC recovers.
# Right (Rayleigh): MRC of order L = 1, 2, 4, closed-form BPSK BER, showing the
# diversity slope steepen. Total average Eb/N0 split across L branches.
# ---------------------------------------------------------------------------
fig, (axA, axR2) = plt.subplots(1, 2, figsize=(8.0, 4.2))

# --- AWGN panel ---
ebn0_db_ax = np.linspace(-2, 12, 400)
g = 10.0 ** (ebn0_db_ax / 10.0)
ber_uncoded = Q(np.sqrt(2.0 * g))
axA.semilogy(ebn0_db_ax, ber_uncoded, color=INK, lw=1.9,
             label="uncoded BPSK\n(= repetition + MRC)")
CG = 6.0
ber_coded = Q(np.sqrt(2.0 * 10.0 ** ((ebn0_db_ax + CG) / 10.0)))
axA.semilogy(ebn0_db_ax, ber_coded, color=ACCENT, lw=1.7, ls="--",
             label="representative FEC\n(schematic)")
axA.axvline(WALL, color=ACCENT_DEEP, lw=1.1, ls=":")
axA.text(WALL + 0.2, 3e-6, "wall $-1.59$ dB", color=ACCENT_DEEP, fontsize=8.5,
         rotation=90, va="bottom")
lvl = 1e-4
x_un = np.interp(np.log10(lvl), np.log10(ber_uncoded[::-1]), ebn0_db_ax[::-1])
x_cd = np.interp(np.log10(lvl), np.log10(ber_coded[::-1]), ebn0_db_ax[::-1])
axA.annotate("", xy=(x_cd, lvl), xytext=(x_un, lvl),
             arrowprops=dict(arrowstyle="<->", color=SAGE, lw=1.3))
axA.text((x_un + x_cd) / 2, lvl * 1.5, "coding gain", color=SAGE, fontsize=8.8,
         ha="center", va="bottom")
axA.set_title("AWGN", fontsize=11, color=INK)
axA.set_xlabel(r"$E_b/N_0$ (dB)")
axA.set_ylabel("bit error rate")
axA.set_ylim(1e-6, 0.5)
axA.set_xlim(-2, 12)
axA.legend(loc="upper right", frameon=False, fontsize=8.2, handlelength=1.6)
despine(axA)

# --- Rayleigh panel: MRC diversity, total Eb/N0 split across L branches ---
def mrc_ber(ebn0_db_total, L):
    gtot = 10.0 ** (ebn0_db_total / 10.0)
    gbar = gtot / L                       # per-branch average SNR
    mu = np.sqrt(gbar / (1.0 + gbar))
    s = np.zeros_like(gbar)
    for k in range(L):
        s += comb(L - 1 + k, k) * ((1.0 + mu) / 2.0) ** k
    return ((1.0 - mu) / 2.0) ** L * s


ebn0_r = np.linspace(0, 30, 400)
cols = {1: INK_SOFT, 2: ACCENT, 4: ACCENT_DEEP}
for L in (1, 2, 4):
    axR2.semilogy(ebn0_r, mrc_ber(ebn0_r, L), color=cols[L], lw=1.8,
                  label=f"$L = {L}$")
axR2.set_title("Rayleigh fading, MRC", fontsize=11, color=INK)
axR2.set_xlabel(r"average $E_b/N_0$ (dB)")
axR2.set_ylim(1e-6, 0.5)
axR2.set_xlim(0, 30)
axR2.legend(loc="upper right", frameon=False, fontsize=9.5, title="diversity",
            title_fontsize=9)
despine(axR2)
axR2.tick_params(labelleft=True)

fig.tight_layout()
save(fig, "ber-coding-diversity")


print("wrote:")
for name in ("shannon-plane", "below-floor", "ber-coding-diversity"):
    p = os.path.join(OUT, name + ".svg")
    print(f"  {p}  ({os.path.getsize(p)} bytes)")
