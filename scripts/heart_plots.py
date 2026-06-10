"""Generate the figures for the post "Reading the heart with a radio engineer's toolbox".

Run with the conda env that has numpy/scipy/matplotlib, e.g.:
    /usr/local/Caskroom/miniforge/base/envs/wifi_analyzer/bin/python scripts/heart_plots.py

Outputs SVGs into public/posts/heart/ styled to match the site's paper palette.
"""

import os
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.signal import welch

# ---- site palette -----------------------------------------------------------
PAPER = "#f6f1e7"
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

OUT = os.path.join(os.path.dirname(__file__), "..", "public", "posts", "heart")
OUT = os.path.abspath(OUT)
os.makedirs(OUT, exist_ok=True)

rng = np.random.default_rng(7)


def despine(ax, keep=("left", "bottom")):
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(side in keep)


# ---------------------------------------------------------------------------
# Figure 1: a noisy ECG-like trace, raw vs band-pass filtered.
# ---------------------------------------------------------------------------
def ecg_beat(t, center, width=0.045, amp=1.0):
    """A crude QRS complex: a sharp positive spike with small flanking dips."""
    x = (t - center) / width
    return amp * (np.exp(-(x**2)) - 0.25 * np.exp(-((x - 1.6) ** 2)) - 0.25 * np.exp(-((x + 1.6) ** 2)))


fs = 500.0
t = np.arange(0, 6.0, 1 / fs)
hr = 1.05  # beats per second
beats = np.arange(0.5, t[-1], 1 / hr)
clean = np.zeros_like(t)
for b in beats:
    clean += ecg_beat(t, b)

# realistic corruption: 50 Hz mains hum + baseline wander + broadband noise
mains = 0.35 * np.sin(2 * np.pi * 50 * t)
wander = 0.6 * np.sin(2 * np.pi * 0.25 * t + 1.0)
noise = 0.12 * rng.standard_normal(t.size)
raw = clean + mains + wander + noise

# band-pass 0.5-40 Hz to kill wander + mains, keep the QRS
from scipy.signal import butter, filtfilt

b_hp, a_hp = butter(2, 0.5 / (fs / 2), btype="high")
b_lp, a_lp = butter(4, 40 / (fs / 2), btype="low")
filt = filtfilt(b_hp, a_hp, raw)
filt = filtfilt(b_lp, a_lp, filt)

fig, axes = plt.subplots(2, 1, figsize=(7.2, 4.2), sharex=True)
axes[0].plot(t, raw, color=INK_SOFT, lw=0.7)
axes[0].set_title("raw recording", loc="left", color=INK, fontsize=12, style="italic")
axes[1].plot(t, filt, color=ACCENT, lw=0.9)
axes[1].set_title("after a 0.5–40 Hz band-pass", loc="left", color=INK, fontsize=12, style="italic")
for ax in axes:
    despine(ax, keep=("bottom",))
    ax.set_yticks([])
axes[1].set_xlabel("time (s)")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "ecg-filtering.svg"))
plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 2: the tachogram — RR intervals over time, with HF (respiratory)
# and LF oscillations baked in so the spectrum has structure.
# ---------------------------------------------------------------------------
n_beats = 320
mean_rr = 0.85  # seconds  (~70 bpm)
k = np.arange(n_beats)

# cumulative time so we can modulate by real elapsed seconds
# build RR iteratively since each interval advances the clock
lf_freq = 0.1   # Hz  (Mayer waves, ~10 s period)
hf_freq = 0.25  # Hz  (respiration, ~4 s period)
rr = np.zeros(n_beats)
clock = 0.0
for i in range(n_beats):
    mod = (
        0.045 * np.sin(2 * np.pi * lf_freq * clock)
        + 0.030 * np.sin(2 * np.pi * hf_freq * clock + 0.7)
        + 0.010 * rng.standard_normal()
    )
    rr[i] = mean_rr + mod
    clock += rr[i]

beat_times = np.cumsum(rr)

fig, ax = plt.subplots(figsize=(7.2, 3.0))
ax.plot(beat_times, rr * 1000, color=ACCENT_DEEP, lw=1.0, marker="o", ms=2.4,
        mfc=ACCENT_DEEP, mec="none")
ax.set_xlabel("time (s)")
ax.set_ylabel("RR interval (ms)")
ax.set_title("the tachogram: time between heartbeats", loc="left", color=INK,
             fontsize=12, style="italic")
despine(ax)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "tachogram.svg"))
plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 3: PSD of the RR series with LF and HF bands shaded.
# Resample RR onto an even grid first (RR is irregularly sampled by nature).
# ---------------------------------------------------------------------------
fs_rr = 4.0  # Hz, standard for HRV
t_even = np.arange(beat_times[0], beat_times[-1], 1 / fs_rr)
rr_even = np.interp(t_even, beat_times, rr)
rr_even = rr_even - rr_even.mean()

f, pxx = welch(rr_even, fs=fs_rr, nperseg=min(256, rr_even.size))

fig, ax = plt.subplots(figsize=(7.2, 3.2))
ax.plot(f, pxx, color=INK, lw=1.2)
# LF band 0.04-0.15, HF band 0.15-0.40
ax.axvspan(0.04, 0.15, color=ACCENT_DEEP, alpha=0.16, lw=0)
ax.axvspan(0.15, 0.40, color=ACCENT, alpha=0.16, lw=0)
ax.set_xlim(0, 0.5)
ax.set_xlabel("frequency (Hz)")
ax.set_ylabel("power spectral density")
ax.set_yticks([])
despine(ax)

ymax = ax.get_ylim()[1]
ax.text(0.058, ymax * 0.92, "LF", color=ACCENT_DEEP, ha="center", fontsize=12,
        style="italic")
ax.text(0.32, ymax * 0.92, "HF", color=ACCENT, ha="center", fontsize=12,
        style="italic")
ax.set_title("the autonomic fingerprint: LF vs HF power", loc="left", color=INK,
             fontsize=12, style="italic")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "hrv-psd.svg"))
plt.close(fig)

print("wrote:")
for name in ("ecg-filtering.svg", "tachogram.svg", "hrv-psd.svg"):
    p = os.path.join(OUT, name)
    print(f"  {p}  ({os.path.getsize(p)} bytes)")
