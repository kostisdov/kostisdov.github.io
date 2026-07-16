"""Reproduce the numbers in the worked budget and the height-comparison table
of the post "The geometry of long-range radio links".

Free-space loss (ITU-R P.525), plane-earth two-ray loss for line-of-sight paths
past the breakpoint, and spherical-earth diffraction loss (ITU-R P.526-15,
Section 4.2) for beyond-the-horizon paths. Horizontal polarization over average
ground (eps_r = 15, sigma = 0.005 S/m), 4/3-Earth.

Run:
    /usr/local/Caskroom/miniforge/base/envs/wifi_analyzer/bin/python scripts/horizon_budget.py
"""

import numpy as np

f = 900.0                 # MHz
k = 4.0 / 3.0
a = 6371.0                # km, true Earth radius
a_e = k * a               # km, effective radius
c = 3.0e8
lam = c / (f * 1e6)       # m

# link constants
EIRP_plus_Grx = 30 + 2 + 10   # dBm (Ptx 30 dBm, drone 2 dBi, ground 10 dBi)
P_sens = -99.0                # dBm (Rb=1 Mbit/s, NF=5 dB, (Eb/N0)req=8 dB, Limpl=2 dB)
D = 40.0                      # km, range
h_ground = 2.0                # m

# --- ITU-R P.526-15 Section 4.2: spherical-Earth diffraction --------------
eps_r, sigma = 15.0, 0.005
K = 0.36278 * (a_e * f) ** (-1.0 / 3.0) * ((eps_r - 1) ** 2 + (18000 * sigma / f) ** 2) ** (-0.25)
beta = (1 + 1.6 * K ** 2 + 0.67 * K ** 4) / (1 + 4.5 * K ** 2 + 1.53 * K ** 4)


def X_of(d):   # normalized distance, d in km
    return 2.188 * beta * f ** (1.0 / 3.0) * a_e ** (-2.0 / 3.0) * d


def Y_of(h):   # normalized height, h in m
    return 9.575e-3 * beta * f ** (2.0 / 3.0) * a_e ** (-1.0 / 3.0) * h


def F(X):      # distance term
    if X >= 1.6:
        return 11 + 10 * np.log10(X) - 17.6 * X
    return -20 * np.log10(X) - 5.6488 * X ** 1.425


def G(Y):      # height-gain term
    B = beta * Y
    if B > 2:
        return 17.6 * np.sqrt(B - 1.1) - 5 * np.log10(B - 1.1) - 8
    elif B > 10 * K:
        return 20 * np.log10(B + 0.1 * B ** 3)
    elif B > K / 10:
        return 2 + 20 * np.log10(K) + 9 * np.log10(B / K) * (np.log10(B / K) + 1)
    return 2 + 20 * np.log10(K)


def diffraction_loss(d, h1, h2):    # dB over free space
    return -(F(X_of(d)) + G(Y_of(h1)) + G(Y_of(h2)))


# --- deterministic losses -------------------------------------------------
def horizon(h1, h2):                # radio horizon, km
    return 4.12 * (np.sqrt(h1) + np.sqrt(h2))


def free_space(d):                  # ITU-R P.525, dB
    return 32.44 + 20 * np.log10(f) + 20 * np.log10(d)


def two_ray(d, h1, h2):             # plane-earth d^4 loss, dB (d in km)
    return 40 * np.log10(d * 1e3) - 20 * np.log10(h1) - 20 * np.log10(h2)


print(f"beta = {beta:.4f},  free-space @ {D:.0f} km = {free_space(D):.1f} dB\n")
print(f"{'drone (m)':>9} {'horizon':>8} {'regime':>7} {'excess (dB)':>12} "
      f"{'loss (dB)':>10} {'Pr (dBm)':>9} {'margin (dB)':>11}")
for h1 in (120, 40, 15):
    dh = horizon(h1, h_ground)
    if D < dh:                      # line of sight
        excess = two_ray(D, h1, h_ground) - free_space(D)
        regime, tag = "LoS", "two-ray"
    else:                           # beyond horizon
        excess = diffraction_loss(D, h1, h_ground)
        regime, tag = "BVLoS", "diffraction"
    L = free_space(D) + excess
    Pr = EIRP_plus_Grx - L
    print(f"{h1:>9} {dh:>7.0f}  {regime:>6} {excess:>+8.1f} ({tag:>11}) "
          f"{L:>10.1f} {Pr:>9.1f} {Pr - P_sens:>+11.1f}")
