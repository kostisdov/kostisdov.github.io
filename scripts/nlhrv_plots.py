"""Figures for the post "The fractal heart: when linear HRV goes blind".

Adapted from the author's nlhrv.py: identical algorithms and seeds (so the reported
alpha-1 values are reproduced), restyled to the site palette and written as SVG into
public/posts/the-fractal-heart-nonlinear-hrv/.

Run with the env that has numpy/scipy/matplotlib:
    /usr/local/Caskroom/miniforge/base/envs/wifi_analyzer/bin/python scripts/nlhrv_plots.py
"""

import os
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import signal, interpolate

# ---- site palette ----------------------------------------------------------
PAPER = "#f6f1e7"; INK = "#221e17"; INK_SOFT = "#5c554a"
ACCENT = "#c34a22"; ACCENT_DEEP = "#1e3d52"; RULE = "#d8cfbc"
SAGE = "#6f8b6a"   # third series colour, harmonised with the warm paper

plt.rcParams.update({
    "figure.facecolor": PAPER, "axes.facecolor": PAPER, "savefig.facecolor": PAPER,
    "font.family": "serif", "font.serif": ["Georgia", "Times New Roman", "DejaVu Serif"],
    "font.size": 11, "text.color": INK, "axes.edgecolor": RULE, "axes.labelcolor": INK_SOFT,
    "xtick.color": INK_SOFT, "ytick.color": INK_SOFT, "axes.linewidth": 0.8,
    "axes.grid": False, "svg.fonttype": "none",
})

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "public", "posts",
                                   "the-fractal-heart-nonlinear-hrv"))
os.makedirs(OUT, exist_ok=True)


def despine(ax, keep=("left", "bottom")):
    for s in ("top", "right", "left", "bottom"):
        ax.spines[s].set_visible(s in keep)


def title(ax, t):
    # Figure titles are rendered as <figcaption> in the post, not baked into the SVG,
    # so this is intentionally a no-op (the call sites document each panel's content).
    return


# ---- synthetic RR via 1/f^beta spectral synthesis (DFA alpha = (beta+1)/2) --
def gen_rr(n, beta, mean=850.0, sd=45.0, seed=None):
    rng = np.random.default_rng(seed)
    f = np.fft.rfftfreq(n); f[0] = f[1]
    amp = 1.0 / (f ** (beta / 2.0))
    spec = amp * np.exp(1j * rng.uniform(0, 2 * np.pi, len(f)))
    x = np.fft.irfft(spec, n=n)
    x = (x - x.mean()) / x.std()
    return mean + sd * x


def dfa(x, scales, order=1):
    x = np.asarray(x, float); N = len(x)
    y = np.cumsum(x - x.mean()); F = []
    for n in scales:
        n = int(n); nb = N // n
        if nb < 1:
            F.append(np.nan); continue
        v = []
        for i in range(nb):
            for seg in (y[i*n:(i+1)*n], y[N-(i+1)*n:N-i*n]):
                t = np.arange(n); c = np.polyfit(t, seg, order)
                v.append(np.mean((seg - np.polyval(c, t)) ** 2))
        F.append(np.sqrt(np.mean(v)))
    return np.array(F)


def dfa_curve(x, smin=4, smax=None, num=22):
    N = len(x); smax = smax or N // 4
    scales = np.unique(np.floor(np.logspace(np.log10(smin), np.log10(smax), num)).astype(int))
    return scales, dfa(x, scales)


def alpha(x, smin, smax, num=12):
    sc = np.unique(np.floor(np.logspace(np.log10(smin), np.log10(smax), num)).astype(int))
    F = dfa(x, sc); ok = np.isfinite(F) & (F > 0)
    return np.polyfit(np.log(sc[ok]), np.log(F[ok]), 1)[0]


def alpha1(x):
    return alpha(x, 4, 16)


def poincare_sd(rr):
    d = np.diff(rr)
    sd1 = np.sqrt(0.5 * np.var(d, ddof=1))
    sd2 = np.sqrt(2 * np.var(rr, ddof=1) - 0.5 * np.var(d, ddof=1))
    return sd1, sd2


def inject_ectopics(rr, rate, seed=0):
    rng = np.random.default_rng(seed); rr = rr.copy()
    idx = rng.choice(np.arange(2, len(rr)-2), int(len(rr)*rate), replace=False)
    for i in idx:
        rr[i] *= 0.45; rr[i+1] *= 1.55
    return rr


def inject_drops(rr, rate, seed=1):
    rng = np.random.default_rng(seed)
    skip = set(rng.choice(np.arange(1, len(rr)-1), int(len(rr)*rate), replace=False))
    out, i = [], 0
    while i < len(rr):
        if i in skip and i+1 < len(rr):
            out.append(rr[i]+rr[i+1]); i += 2
        else:
            out.append(rr[i]); i += 1
    return np.array(out)


# ======================================================================
N = 2000
rr_health = gen_rr(N, beta=1.0, seed=11)
rr_brown  = gen_rr(N, beta=2.0, seed=12)
rr_white  = gen_rr(N, beta=0.0, seed=13)
rr_shuf   = rr_health.copy(); np.random.default_rng(99).shuffle(rr_shuf)

a_h, a_s = alpha1(rr_health), alpha1(rr_shuf)
print(f"alpha1: healthy={a_h:.2f} shuffled={a_s:.2f} "
      f"white={alpha1(rr_white):.2f} brownian={alpha1(rr_brown):.2f}")
print(f"healthy mean={rr_health.mean():.0f} SDNN={rr_health.std(ddof=1):.0f}; "
      f"shuffled mean={rr_shuf.mean():.0f} SDNN={rr_shuf.std(ddof=1):.0f}")

# ---- Fig 1: linear blind spot -------------------------------------------
fig, ax = plt.subplots(3, 1, figsize=(7.4, 6.6))
ax[0].plot(rr_health[:400], color=ACCENT_DEEP, lw=0.9); title(ax[0], "healthy 1/f rhythm")
ax[0].set_ylabel("RR (ms)")
ax[1].plot(rr_shuf[:400], color=ACCENT, lw=0.9); title(ax[1], "same values, shuffled")
ax[1].set_ylabel("RR (ms)"); ax[1].set_xlabel("beat #")
sh, Fh = dfa_curve(rr_health); ss, Fs = dfa_curve(rr_shuf)
ax[2].loglog(sh, Fh, 'o-', color=ACCENT_DEEP, ms=4, label=f"healthy  α₁={a_h:.2f}")
ax[2].loglog(ss, Fs, 's-', color=ACCENT, ms=4, label=f"shuffled α₁={a_s:.2f}")
ax[2].set_xlabel("scale n (beats)"); ax[2].set_ylabel("F(n)")
title(ax[2], "DFA fluctuation curves")
ax[2].legend(frameon=False)
for a in ax:
    despine(a)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "fig1_blindspot.svg"), bbox_inches="tight")
plt.close(fig)

# ---- Fig 2: Poincare -----------------------------------------------------
fig, ax = plt.subplots(figsize=(5.4, 5.2))
rr = rr_health
ax.scatter(rr[:-1], rr[1:], s=6, color=ACCENT_DEEP, alpha=0.35, edgecolors="none")
sd1, sd2 = poincare_sd(rr); c = rr.mean()
th = np.linspace(0, 2*np.pi, 200)
ex = c + sd2*np.cos(th)*np.cos(np.pi/4) - sd1*np.sin(th)*np.sin(np.pi/4)
ey = c + sd2*np.cos(th)*np.sin(np.pi/4) + sd1*np.sin(th)*np.cos(np.pi/4)
ax.plot(ex, ey, color=ACCENT, lw=2)
ax.plot([c-sd2*np.cos(np.pi/4), c+sd2*np.cos(np.pi/4)],
        [c-sd2*np.sin(np.pi/4), c+sd2*np.sin(np.pi/4)], color=INK, lw=1)
ax.plot([c+sd1*np.sin(np.pi/4), c-sd1*np.sin(np.pi/4)],
        [c-sd1*np.cos(np.pi/4), c+sd1*np.cos(np.pi/4)], color=SAGE, lw=1.5)
ax.set_xlabel(r"$RR_n$ (ms)"); ax.set_ylabel(r"$RR_{n+1}$ (ms)")
title(ax, f"Poincaré plot   SD1={sd1:.0f} ms   SD2={sd2:.0f} ms")
ax.set_aspect("equal"); despine(ax)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "fig2_poincare.svg"), bbox_inches="tight")
plt.close(fig)

# ---- Fig 3: DFA for three regimes ---------------------------------------
fig, ax = plt.subplots(1, 2, figsize=(9.6, 4.0))
for rr, col, lab in [(rr_white, SAGE, "white"), (rr_health, ACCENT_DEEP, "1/f"),
                     (rr_brown, ACCENT, "Brownian")]:
    ax[0].plot(rr[:300] - rr[:300].mean(), color=col, lw=0.8, alpha=0.85, label=lab)
title(ax[0], "three rhythms"); ax[0].set_xlabel("beat #"); ax[0].set_ylabel("RR − mean (ms)")
ax[0].legend(frameon=False)
for rr, col, lab in [(rr_white, SAGE, "white"), (rr_health, ACCENT_DEEP, "1/f"),
                     (rr_brown, ACCENT, "Brownian")]:
    s, F = dfa_curve(rr)
    ax[1].loglog(s, F, 'o-', color=col, ms=3.5, label=f"{lab}: α₁={alpha1(rr):.2f}")
ax[1].set_xlabel("scale n (beats)"); ax[1].set_ylabel("F(n)")
title(ax[1], "DFA: slope = scaling exponent α")
ax[1].legend(frameon=False)
for a in ax:
    despine(a)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "fig3_dfa.svg"), bbox_inches="tight")
plt.close(fig)

# ---- Fig 4: the wearable reckoning --------------------------------------
rr_ect = inject_ectopics(rr_health, 0.015)
rr_drp = inject_drops(rr_health, 0.06)
a_clean, a_ect, a_drp = alpha1(rr_health), alpha1(rr_ect), alpha1(rr_drp)
fig, ax = plt.subplots(1, 2, figsize=(9.6, 4.0))
ax[0].plot(rr_health[:250], color=ACCENT_DEEP, lw=0.9, label="clean")
ax[0].plot(rr_ect[:250], color=ACCENT, lw=0.8, alpha=0.85, label="1.5% ectopics")
title(ax[0], "a 1.5% ectopic rate"); ax[0].set_xlabel("beat #"); ax[0].set_ylabel("RR (ms)")
ax[0].legend(frameon=False)
for rr, col, lab, a in [(rr_health, ACCENT_DEEP, "clean", a_clean),
                        (rr_ect, ACCENT, "1.5% ectopics", a_ect),
                        (rr_drp, SAGE, "6% drops", a_drp)]:
    s, F = dfa_curve(rr)
    ax[1].loglog(s, F, 'o-', color=col, ms=3.5, label=f"{lab}: α₁={a:.2f}")
ax[1].set_xlabel("scale n (beats)"); ax[1].set_ylabel("F(n)")
title(ax[1], "α₁ corrupted by tiny artifact rates")
ax[1].legend(frameon=False)
for a in ax:
    despine(a)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "fig4_reckoning.svg"), bbox_inches="tight")
plt.close(fig)

print(f"reckoning: clean={a_clean:.2f} ectopic(1.5%)={a_ect:.2f} drops(6%)={a_drp:.2f}")
print("wrote SVGs to", OUT)
