"""Generate the figures for the post "When the airframe joins the array".

The data come from the manifold-lab simulations (NEC-2 method of moments for the
installed array, MUSIC direction finding) and are stored in
scripts/data/airframe-array.npz. Run with any Python that has numpy/matplotlib:
    python scripts/airframe_array_plots.py

Outputs SVGs into public/posts/when-the-airframe-joins-the-array/ styled to match
the site's soft off-white paper palette.
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
STONE = "#9a9285"

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
        "legend.frameon": False,
    }
)

HERE = os.path.dirname(__file__)
D = np.load(os.path.join(HERE, "data", "airframe-array.npz"))
OUT = os.path.abspath(os.path.join(HERE, "..", "public", "posts", "when-the-airframe-joins-the-array"))
os.makedirs(OUT, exist_ok=True)

CAL = ["ideal", "chamber", "sim", "flight", "oracle"]
NAME = {"ideal": "Textbook", "chamber": "Chamber (bare array)", "sim": "Simulated airframe",
        "flight": "Flight calibration", "oracle": "Exact installed"}
COLOR = {"ideal": STONE, "chamber": ACCENT_DEEP, "sim": SAGE, "flight": ACCENT, "oracle": INK}
WAVE = LinearSegmentedColormap.from_list("wave", [ACCENT_DEEP, "#9fb3c0", PAPER, "#e2a98f", ACCENT])


def despine(ax, keep=("left", "bottom")):
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(side in keep)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight")
    plt.close(fig)


# ---- Fig. 1: the wave at the array --------------------------------------------
x = D["nf_x"]
ez, inc = D["nf_ez"], D["nf_inc"]
el = D["nf_elements_cm"]
h = float(D["nf_body_half_cm"])
az = float(D["nf_jammer_az"])
est_text, est_inst = D["nf_est"]

fig, axs = plt.subplots(1, 2, figsize=(10.5, 4.9), sharey=True)
ext = [x[0], x[-1], x[0], x[-1]]
perr = D["nf_elem_phase_err"]
panels = [(np.real(inc).T, "Without the drone"), (np.real(ez).T, "Under the drone")]
for j, (ax, (img, title)) in enumerate(zip(axs, panels)):
    im = ax.imshow(img, origin="lower", extent=ext, cmap=WAVE, vmin=-2, vmax=2, interpolation="bilinear")
    if j == 1:
        ax.add_patch(plt.Rectangle((-h, -h), 2 * h, 2 * h, fill=False, ec=INK_SOFT, lw=0.8, ls="--"))
    ax.plot(el[:, 0], el[:, 1], "o", ms=6, color=INK, mec=PAPER, mew=1)
    if j == 1:
        for (ex_, ey_), pe in zip(el, perr):
            u = np.array([ex_, ey_]) / np.hypot(ex_, ey_)
            ax.annotate(f"{pe:+.0f}°".replace("-", "\u2212"), (ex_, ey_), xytext=(ex_ + 10 * u[0], ey_ + 10 * u[1]),
                        ha="center", va="center", fontsize=11, color=INK,
                        bbox=dict(fc=PAPER, ec="none", alpha=0.85, pad=1.2))
    ax.annotate("", xy=(0.92 * 27 * np.cos(np.deg2rad(az)) * 0.3, 0.92 * 27 * np.sin(np.deg2rad(az)) * 0.3),
                xytext=(27 * np.cos(np.deg2rad(az)), 27 * np.sin(np.deg2rad(az))),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.4))
    ax.set_xlabel("x (cm)")
    ax.set_title(title, fontsize=12, color=INK_SOFT)
    despine(ax, keep=())
    ax.set_xticks([-30, 0, 30]); ax.set_yticks([-30, 0, 30])
axs[0].set_ylabel("y (cm)")
cb = fig.colorbar(im, ax=axs, shrink=0.78, pad=0.02)
cb.outline.set_visible(False)
cb.set_label("Vertical electric field (V/m)", color=INK_SOFT)
save(fig, "fig1-wave.svg")

# ---- Fig. 2: what coupling and the airframe do to the response ----------------
az_deg = D["phase_az"]
fig, axs = plt.subplots(1, 2, figsize=(10.5, 3.8), sharey=True)
for ax, k, title in zip(axs, ["coupled", "airframe"], ["Coupling only (array in free space)", "Installed under the airframe"]):
    for m in range(4):
        ax.plot(az_deg, D[f"phase_{k}"][m], color=[ACCENT_DEEP, ACCENT, SAGE, STONE][m], lw=1.3,
                label=f"element {m + 1}")
    ax.axhline(0, color=RULE, lw=0.8)
    ax.set_xlim(0, 360); ax.set_xticks([0, 90, 180, 270, 360])
    ax.set_xlabel("Azimuth (deg)")
    ax.set_title(title, fontsize=12, color=INK_SOFT)
    despine(ax)
axs[0].set_ylabel("Phase error vs textbook (deg)")
fig.legend(*axs[1].get_legend_handles_labels(), loc="upper center", ncol=4, fontsize=10,
           bbox_to_anchor=(0.5, 1.06))
save(fig, "fig2-phase.svg")

# ---- Fig. 3: DF error with the textbook and the installed response -----------
fig, axs = plt.subplots(1, 2, figsize=(10.5, 3.9), gridspec_kw={"width_ratios": [1.35, 1]})
ax = axs[0]
ax.plot(D["bias_az_ideal"], D["bias_err_ideal"], ".", ms=2.2, color=STONE, label="Textbook response", rasterized=True)
ax.plot(D["bias_az_airframe"], D["bias_err_airframe"], ".", ms=2.2, color=ACCENT, label="Installed response", rasterized=True)
ax.set_xlim(0, 360); ax.set_xticks([0, 90, 180, 270, 360]); ax.set_ylim(-150, 150)
ax.set_xlabel("True azimuth (deg)"); ax.set_ylabel("Azimuth error (deg)")
ax.legend(fontsize=9, markerscale=5, loc="lower left")
despine(ax)
ax = axs[1]
jnr = D["jnr"]
ax.semilogy(jnr, D["rmse_ideal"], "-o", ms=3, color=STONE, label="Textbook")
ax.semilogy(jnr, D["rmse_coupled"], "-o", ms=3, color=ACCENT_DEEP, label="Coupling only")
ax.semilogy(jnr, D["rmse_airframe"], "-o", ms=3, color=ACCENT, label="Installed")
ax.semilogy(jnr, D["crb"], "--", color=INK, lw=1, label="CRB")
ax.set_xlabel("SNR per element (dB)"); ax.set_ylabel("RMSE (deg)")
ax.legend(fontsize=9, loc="lower left")
despine(ax)
save(fig, "fig3-df-error.svg")

# ---- Fig. 4: calibration options on realistic drones --------------------------
fig, ax = plt.subplots(figsize=(7.6, 3.6))
order = ["oracle", "flight", "sim", "chamber", "ideal"]
for i, k in enumerate(order):
    e = np.maximum(D[f"cal_err_{k}"], 1e-3)
    q5, q25, q50, q75, q95 = np.percentile(e, [5, 25, 50, 75, 95])
    ax.plot([q5, q95], [i, i], color=COLOR[k], lw=1.2)
    ax.add_patch(plt.Rectangle((q25, i - 0.28), q75 - q25, 0.56, fc=COLOR[k], alpha=0.25, ec=COLOR[k], lw=1))
    ax.plot([q50, q50], [i - 0.28, i + 0.28], color=COLOR[k], lw=2)
    ax.text(2.4e2, i, f"{np.mean(e > 90) * 100:.1f} %", va="center", fontsize=12, color=INK_SOFT)
ax.text(2.4e2, len(order) - 0.3, "> 90°", fontsize=12, color=INK_SOFT)
ax.set_yticks(range(len(order)), [NAME[k] for k in order])
ax.set_xscale("log"); ax.set_xlim(3e-3, 1.5e2)
ax.set_xlabel("Azimuth error magnitude (deg)")
ax.set_ylim(-0.6, len(order) - 0.1)
despine(ax, keep=("bottom",))
ax.tick_params(axis="y", length=0)
save(fig, "fig4-calibration.svg")

# ---- Fig. 5: from bearings to a position --------------------------------------
fig, axs = plt.subplots(1, 2, figsize=(10.5, 4.4), gridspec_kw={"width_ratios": [1.25, 1]})
ax = axs[0]
for k in CAL:
    m = np.sort(D[f"miss3_{k}"])
    ax.plot(np.maximum(m, 0.1), np.linspace(0, 1, len(m)), color=COLOR[k], lw=1.8, label=NAME[k])
ax.set_xscale("log"); ax.set_xlim(0.5, 2e4)
ax.set_xlabel("Miss distance (m)"); ax.set_ylabel("Fraction of geometries")
fig.legend(*ax.get_legend_handles_labels(), loc="upper center", ncol=5, fontsize=10,
           bbox_to_anchor=(0.5, 1.04), handlelength=1.5, columnspacing=1.2)
despine(ax)
ax = axs[1]
xy = D["ex_xy"]
for k in ["ideal", "chamber", "flight"]:
    for p, b in zip(xy, D[f"ex_bearing_{k}"]):
        ax.plot([p[0], p[0] + 7000 * np.cos(b)], [p[1], p[1] + 7000 * np.sin(b)], color=COLOR[k], lw=1, alpha=0.9)
    f = D[f"ex_fix_{k}"]
    ax.plot(*f, "o", ms=9, color=COLOR[k], mec=PAPER, mew=1.2, zorder=5)
    dist = np.linalg.norm(f)
    lab = f"{dist / 1000:.1f} km" if dist >= 1000 else f"{dist:.0f} m"
    off = {"ideal": (10, -4), "chamber": (10, 6), "flight": (10, -14)}[k]
    ax.annotate(lab, f, xytext=off, textcoords="offset points", fontsize=11, color=COLOR[k], zorder=7)
ax.plot(0, 0, "*", ms=15, color=INK, zorder=6)
ax.plot(xy[:, 0], xy[:, 1], "^", ms=8, color=INK, zorder=6)
lim = 1.25 * max(np.linalg.norm(D[f"ex_fix_{k}"]) for k in ["ideal", "chamber", "flight"])
ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_aspect("equal")
t = 1000 * np.floor(lim / 1000)
ax.set_xticks([-t, 0, t]); ax.set_yticks([-t, 0, t])
ax.set_xlabel("x (m)"); ax.set_ylabel("y (m)")
despine(ax)
save(fig, "fig5-localization.svg")

print("figures written to", OUT)
