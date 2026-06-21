"""Generate Open Graph / social-preview cards (1200x630 PNG) for the site.

Run with the conda env that has numpy/matplotlib, e.g.:
    /usr/local/Caskroom/miniforge/base/envs/wifi_analyzer/bin/python scripts/social_cards.py

Outputs:
    public/og/default.png   site-wide fallback card
    public/og/solstice.png  card for "The geometry of the longest day"

Cards are raster (PNG) because LinkedIn/Twitter will not render SVG og:images.
Palette matches the site (soft off-white background).
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
RULE = "#e5e3dd"

plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["Georgia", "Times New Roman", "DejaVu Serif"],
        "text.color": INK,
    }
)

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "public", "og"))
os.makedirs(OUT, exist_ok=True)

DEG = np.pi / 180.0
EPS = 23.44

# 1200x630 at 100 dpi
W, H = 12.0, 6.30
DPI = 100


def new_card():
    fig = plt.figure(figsize=(W, H), dpi=DPI)
    fig.patch.set_facecolor(PAPER)
    # a thin accent rule along the very top
    fig.add_artist(plt.Line2D([0, 1], [0.985, 0.985], color=ACCENT, lw=4,
                              transform=fig.transFigure))
    return fig


# ---------------------------------------------------------------------------
# Solstice card: title block on the left, the analemma on the right.
# ---------------------------------------------------------------------------
N = np.arange(1, 366)
D = N - 1.0
L = (280.460 + 0.9856474 * D) % 360.0
g = (357.528 + 0.9856003 * D) % 360.0
lam = L + 1.915 * np.sin(g * DEG) + 0.020 * np.sin(2 * g * DEG)
dec = np.arcsin(np.sin(EPS * DEG) * np.sin(lam * DEG)) / DEG
alpha = (np.arctan2(np.cos(EPS * DEG) * np.sin(lam * DEG), np.cos(lam * DEG)) / DEG) % 360.0
eot = ((L - alpha + 180.0) % 360.0 - 180.0) * 4.0

fig = new_card()
fig.text(0.062, 0.86, "KOSTIS  DOVELOS", fontsize=15, color=INK_SOFT,
         family="monospace", va="center")
fig.text(0.060, 0.66, "The geometry of\nthe longest day", fontsize=52, color=INK,
         va="center", linespacing=1.05)
fig.text(0.062, 0.30, "What the summer solstice really is: the extremum\n"
                      "of a deterministic signal, the Sun's motion through the year.",
         fontsize=20, color=INK_SOFT, style="italic", va="center", linespacing=1.3)
fig.text(0.062, 0.10, "kostisdov.github.io", fontsize=15, color=ACCENT,
         family="monospace", va="center")

# analemma on the right
ax = fig.add_axes([0.685, 0.14, 0.265, 0.72])
ax.plot(np.append(eot, eot[0]), np.append(dec, dec[0]), color=ACCENT, lw=2.4)
for n, va in ((172, "bottom"), (355, "top")):
    ax.plot(eot[n - 1], dec[n - 1], "o", ms=7, color=ACCENT_DEEP, mec=PAPER, mew=1.2)
ax.set_xlim(-20, 20)
ax.set_ylim(-32, 32)
ax.set_facecolor(PAPER)
ax.axis("off")
fig.savefig(os.path.join(OUT, "solstice.png"), facecolor=PAPER)
plt.close(fig)


# ---------------------------------------------------------------------------
# Default site card: wordmark + tagline, with a faint interference ridgeline
# echoing the home-page hero art.
# ---------------------------------------------------------------------------
fig = new_card()
fig.text(0.062, 0.86, "KOSTIS  DOVELOS", fontsize=15, color=INK_SOFT,
         family="monospace", va="center")
fig.text(0.060, 0.60, "Signals, systems,\nand other curiosities.", fontsize=54,
         color=INK, va="center", linespacing=1.05)
fig.text(0.062, 0.20, "Notes on waves, signals, and the physics of everyday phenomena.",
         fontsize=21, color=INK_SOFT, style="italic", va="center")

# faint ridgeline band across the lower third
ax = fig.add_axes([0.0, 0.0, 1.0, 0.30])
ax.set_xlim(0, 1)
ax.set_ylim(-1, 1)
ax.axis("off")
sources = [(0.18, 0.7, 34), (0.55, 0.9, 46), (0.82, 0.6, 28)]
x = np.linspace(0, 1, 600)
for j, base in enumerate(np.linspace(0.85, -0.85, 11)):
    v = np.zeros_like(x)
    for sx, amp, k in sources:
        r = np.abs(x - sx) + 0.04
        v += amp * np.sin(k * r - 0.6 * j) / (1 + 6 * r)
    col = ACCENT if j % 4 == 1 else INK_SOFT
    a = 0.55 if j % 4 == 1 else 0.22
    ax.plot(x, base + 0.07 * v, color=col, lw=1.0, alpha=a)
fig.savefig(os.path.join(OUT, "default.png"), facecolor=PAPER)
plt.close(fig)

print("wrote:")
for name in ("solstice.png", "default.png"):
    p = os.path.join(OUT, name)
    print(f"  {p}  ({os.path.getsize(p)} bytes)")
