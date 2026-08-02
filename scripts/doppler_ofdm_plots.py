"""Figures for the post "Doppler-resilient OFDM".

Fig 1  ICI mechanism: magnitude of the frequency-domain channel matrix
       H = F Ht F^H for one doubly-selective realization, at low and high
       normalized Doppler. Self-contained (numpy only), fast.

Fig 2  Coded BER vs SNR at eps=1.2 for four receivers. The BER arrays are the
       output of the reproducible simulation in
       https://github.com/kostisdov/ofdm_vs_otfs (run_waveforms.py); they are
       stored here so the figure is regenerable without the full Monte-Carlo.

Run:
    /usr/local/Caskroom/miniforge/base/envs/wifi_analyzer/bin/python scripts/doppler_ofdm_plots.py
"""

import os
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

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
        "svg.fonttype": "none",
    }
)

OUT = os.path.join(os.path.dirname(__file__), "..", "public", "posts", "doppler-resilient-ofdm")
os.makedirs(OUT, exist_ok=True)

CMAP = LinearSegmentedColormap.from_list("paperheat", [PAPER, "#e7c9a0", ACCENT, ACCENT_DEEP, INK])


# ---------------------------------------------------------------------------
def ici_matrix(M, delays, gains, dopplers):
    """Frequency-domain channel matrix H = F Ht F^H over one M-sample symbol.
    h_p(n) = gains[p] * exp(j 2 pi dopplers[p] n), circular delay by delays[p]."""
    F = np.fft.fft(np.eye(M), norm="ortho")
    Fh = F.conj().T
    n = np.arange(M)
    Ht = np.zeros((M, M), dtype=complex)
    for lp, g, nu in zip(delays, gains, dopplers):
        h = g * np.exp(1j * 2 * np.pi * nu * n)          # time-varying tap gain
        cols = (n - lp) % M
        Ht[n, cols] += h
    return F @ Ht @ Fh


def fig1_ici():
    M = 64
    rng = np.random.default_rng(3)
    delays = [0, 3, 7, 12]
    gains = (rng.standard_normal(4) + 1j * rng.standard_normal(4)) / np.sqrt(2)
    gains *= np.array([1.0, 0.7, 0.5, 0.35])
    gains /= np.linalg.norm(gains)
    shape = np.array([1.0, -0.6, 0.35, -0.85])            # Doppler pattern across taps

    fig, axes = plt.subplots(1, 2, figsize=(9.4, 4.5))
    for ax, eps, tag in [(axes[0], 0.05, "low mobility"), (axes[1], 1.2, "high mobility")]:
        fD = eps / M                                      # cyc/sample (Delta f = 1/M)
        H = ici_matrix(M, delays, gains, shape * fD)
        mag = np.abs(H)
        mag /= mag.max()
        im = ax.imshow(mag, cmap=CMAP, vmin=0, vmax=1, interpolation="nearest")
        ax.set_title(f"{tag}   (ε = {eps:g})", color=INK, fontsize=13, pad=10)
        ax.set_xlabel("transmitted subcarrier")
        if ax is axes[0]:
            ax.set_ylabel("received subcarrier")
        ax.set_xticks([0, 32, 63]); ax.set_yticks([0, 32, 63])
        for sp in ax.spines.values():
            sp.set_edgecolor(RULE)
    cbar = fig.colorbar(im, ax=axes, fraction=0.046, pad=0.03)
    cbar.set_label("normalized |H|", color=INK_SOFT)
    cbar.outline.set_edgecolor(RULE)
    fig.savefig(os.path.join(OUT, "fig1_ici.svg"), bbox_inches="tight")
    plt.close(fig)
    print("wrote fig1_ici.svg")


# ---------------------------------------------------------------------------
# Fig 2 data: coded BER from run_waveforms.py at eps=1.2, QPSK, rate-1/2 LDPC,
# 150 frames on a Jakes/TDL-C channel (M=64, N=8, Q=3, Kd=4). Real Monte-Carlo
# output of https://github.com/kostisdov/ofdm_vs_otfs, stored so the figure is
# regenerable without re-running the ~15 min simulation.
SNR = np.array([0, 1, 2, 3, 4, 5])
BER = {
    "CP-OFDM, single-tap": [3.71e-1, 3.62e-1, 3.54e-1, 3.46e-1, 3.38e-1, 3.40e-1],
    "ZP-OFDM, ICI-aware (proposed)": [2.04e-1, 1.75e-1, 1.46e-1, 1.04e-1, 4.82e-2, 3.26e-3],
    "FDE-OTFS (OTFS at OFDM cost)": [2.00e-1, 1.76e-1, 1.44e-1, 1.03e-1, 3.93e-2, 1.50e-3],
    "OTFS, joint delay-Doppler": [1.96e-1, 1.65e-1, 1.34e-1, 8.35e-2, 2.41e-2, 1.21e-3],
}


def fig2_ber():
    if any(v is None for v in BER.values()):
        print("fig2: BER arrays not populated yet; skipping.")
        return
    fig, ax = plt.subplots(figsize=(7.6, 5.0))
    styles = {
        "CP-OFDM, single-tap": (INK_SOFT, "o:", 1.4),
        "ZP-OFDM, ICI-aware (proposed)": (ACCENT, "s-", 1.9),
        "FDE-OTFS (OTFS at OFDM cost)": (SAGE, "D-.", 1.6),
        "OTFS, joint delay-Doppler": (ACCENT_DEEP, "^--", 1.7),
    }
    for name, (c, st, lw) in styles.items():
        ax.semilogy(SNR, BER[name], st, color=c, label=name, linewidth=lw, markersize=6)
    ax.set_xlabel("SNR [dB]"); ax.set_ylabel("Coded BER")
    ax.grid(True, which="both", color=RULE, alpha=0.5)
    ax.legend(frameon=False, fontsize=10.5)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    fig.savefig(os.path.join(OUT, "fig2_ber.svg"), bbox_inches="tight")
    plt.close(fig)
    print("wrote fig2_ber.svg")


if __name__ == "__main__":
    fig1_ici()
    fig2_ber()
