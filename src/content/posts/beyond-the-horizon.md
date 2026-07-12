---
title: "The geometry of long-range radio links"
description: "A terrestrial link built for range runs into the curvature of the Earth long before it runs out of power. The horizon looks like a hard wall, but it is not. The geometry and propagation that set real beyond-line-of-sight range, and a worked drone budget."
date: 2026-07-11
tags: ["signals", "wireless"]
image: "/og/beyond-the-horizon.png"
---

A long-range terrestrial link, a drone relay, a sensor backhaul, a tactical radio, is limited by
the shape of the Earth as much as by its power budget. The received signal weakens with distance,
but the ground also curves away, and past a certain range the two terminals can no longer see each
other at all. That range, the horizon, is often quoted as the hard limit on a beyond visual line of
sight (BVLoS) link. It is not a wall. Radio bends past the geometric edge, diffracts into the
shadow behind it, and on some days ducts for hundreds of kilometres. This post works through the
geometry and the propagation that set real BVLoS range, and closes with a drone budget tied to the
receiver sensitivity of the previous post.

## The horizon is not the range limit

The geometric horizon follows from a tangent line to a sphere. For an antenna at height $h$ above a
smooth Earth of radius $R$, the tangent grazing distance is $d = \sqrt{2Rh}$. With $R = 6371$ km
and $h$ in metres, this is

$$
d_\text{geo} = 3.57\sqrt{h} \quad [\text{km}].
$$

Radio waves do not travel in straight lines through the atmosphere. The refractive index falls with
altitude, so a ray bends gently downward and follows the curvature a little way past the geometric
tangent. The standard correction replaces $R$ with an effective radius $kR$, where $k = 4/3$ for a
median atmosphere [1]. The radio horizon is then about 15% longer,

$$
d_\text{radio} = 4.12\sqrt{h} \quad [\text{km}],
$$

and for a link between two terminals it is the sum of their horizons,
$d = 4.12(\sqrt{h_t} + \sqrt{h_r})$. Figure 1 shows the two grazing rays from a single elevated
terminal. The radio ray clears the flatter 4/3-Earth surface and reaches further than the geometric
one.

<figure>
<img src="/posts/beyond-the-horizon/earth-bulge.svg" alt="A drone at 120 m with two grazing rays reaching the geometric horizon at 39 km and the radio horizon at 45 km over the curving Earth." />
<figcaption>Fig. 1: The radio horizon from a drone at 120 m. The Earth surface curves away below the antenna base, less steeply for the 4/3-Earth model (green) than for the geometric one (dashed). A grazing ray is tangent to the surface at the horizon. The geometric horizon is at 3.57√h ≈ 39 km; refraction extends the radio horizon to 4.12√h ≈ 45 km, the shaded reach beyond.</figcaption>
</figure>

Two points follow. The horizon depends only on height, not on power or frequency. And even the
radio horizon is where the direct ray grazes, not where the signal ends, because diffraction
carries energy into the region beyond.

## Antenna height dominates

Because range grows as $\sqrt{h}$, height is the strongest lever on a terrestrial link. Doubling the
range requires four times the height. Raising one terminal from a 2 m tripod to a 120 m drone
extends its horizon from about 6 km to 45 km, an eightfold gain from geometry alone. Figure 2 traces
the square-root law.

<figure>
<img src="/posts/beyond-the-horizon/range-vs-height.svg" alt="Horizon range versus drone height, the square-root curve, with the ground terminal fixed at 2 m and mast, drone, and 500 m points marked." />
<figcaption>Fig. 2: Horizon range against the height of one terminal, the other fixed at 2 m. Range follows the √h law, so a mast at 30 m reaches 28 km, a drone at 120 m reaches 51 km, and 500 m reaches 98 km. The shaded band is the refraction gain of the radio horizon over the geometric one.</figcaption>
</figure>

Height is not simply another term in the budget. Transmit power adds decibels of margin to a link
that already closes, but no amount of power creates line of sight where the Earth blocks it. Past
the horizon the direct ray is gone, and the signal that remains has propagated by diffraction or
tropospheric scatter, with tens of decibels of excess loss. Height changes the propagation regime;
power only scales it. This is why a modest transmitter on a high platform outperforms a strong one
on the ground.

## Path loss beyond free space

Within line of sight, the received power still falls with distance, and the rate of that fall is
usually worse than the free-space figure. Free-space loss follows the inverse-square law [2],

$$
L_\text{fs} = 32.44 + 20\log_{10} f_\text{MHz} + 20\log_{10} d_\text{km} \quad [\text{dB}],
$$

which rises 20 dB per decade of distance. Over real ground a second ray reaches the receiver, the
reflection off the surface. It arrives with a phase set by the extra path length, and at long range,
where the grazing angle is small, the reflection coefficient approaches $-1$. Direct and reflected
rays then nearly cancel, and the received power falls as $d^{4}$ rather than $d^{2}$. The plane-earth
loss is [3]

$$
L_\text{2-ray} = 40\log_{10} d - 20\log_{10} h_t - 20\log_{10} h_r \quad [\text{dB}],
$$

with $d$ and the heights in metres. It rises 40 dB per decade and, notably, does not depend on
frequency. The crossover between the two regimes is the breakpoint,

$$
d_\text{bp} \approx \frac{4 h_t h_r}{\lambda},
$$

where the first Fresnel zone first touches the ground. Below it the two rays interfere and the loss
oscillates around the free-space curve. Above it the $d^{4}$ law takes over. Figure 3 shows both.

<figure>
<img src="/posts/beyond-the-horizon/path-loss.svg" alt="Path loss versus distance, the two-ray model oscillating below the breakpoint and settling onto the d-to-the-fourth asymptote above it, diverging from free space." />
<figcaption>Fig. 3: Path loss against distance at 900 MHz, drone at 120 m, ground at 2 m. The two-ray model (red) oscillates around free space (dashed) below the breakpoint at 2.9 km, then settles onto the d⁴ asymptote (dotted, 40 dB/decade). Beyond a few kilometres the honest exponent is 4, not 2.</figcaption>
</figure>

For long range with modest antenna heights the breakpoint sits at a few kilometres, so a link of
tens of kilometres is deep in the $d^{4}$ regime. The free-space number quoted for such a link
understates the loss by 20 dB per decade past the breakpoint. That is the first correction a BVLoS
budget needs.

## Diffraction past the horizon

Beyond the horizon the direct ray is blocked, yet a link can still close. Radio diffracts around the
Earth's curvature and over terrain, filling the geometric shadow with a field that decays smoothly
rather than vanishing. The loss relative to free space is governed by the Fresnel-Kirchhoff
diffraction parameter,

$$
\nu = h\sqrt{\frac{2(d_1 + d_2)}{\lambda\, d_1 d_2}},
$$

where $h$ is the height of the obstruction above the direct ray, negative when the ray clears it,
and $d_1, d_2$ are the distances to the obstruction. A single ridge is modelled as a knife edge,
whose loss depends only on $\nu$ [4]. Figure 4 plots it.

<figure>
<img src="/posts/beyond-the-horizon/diffraction.svg" alt="Knife-edge diffraction loss versus the parameter nu, near zero at clearance, 6 dB at grazing, and rising into the shadow." />
<figcaption>Fig. 4: Knife-edge diffraction loss against the parameter ν. For ν below about −0.8 the ray has 0.6 of the first Fresnel zone clear and the loss is negligible. At grazing (ν = 0) the loss is 6 dB, and it climbs steadily into the shadow (ν > 0). "No line of sight" is not "no link"; it is a predictable excess loss.</figcaption>
</figure>

Two thresholds matter in practice. Grazing incidence, where the ray just touches the obstruction,
already costs 6 dB, so an unobstructed Fresnel zone is not free. Full free-space behaviour needs the
ray to clear the obstruction by about 0.6 of the first Fresnel zone radius,
$F_1 = \sqrt{\lambda d_1 d_2 / (d_1 + d_2)}$. Below that clearance the diffraction loss grows, and a
BVLoS link operating past the horizon pays it on top of the path loss. Smooth-sphere diffraction
over the bulge itself is heavier than a single knife edge, but the principle is the same: the
shadow is illuminated, at a cost that the geometry predicts.

## The atmosphere and the 4/3 fiction

The $k = 4/3$ factor rests on a standard refractivity gradient of about $-39$ N-units per kilometre.
That gradient is a long-term median, and the real atmosphere departs from it hour to hour. When the
gradient is weaker, the horizon shortens (sub-refraction). When it is stronger, the horizon extends,
and beyond a critical gradient the atmosphere traps the wave against the surface entirely. This is
ducting, a super-refractive layer that can carry a signal hundreds of kilometres past its nominal
horizon, common over water and in coastal and evening conditions [5]. Figure 5 shows the horizon
sliding with $k$.

<figure>
<img src="/posts/beyond-the-horizon/k-factor.svg" alt="Horizon range versus the effective-Earth factor k, growing from sub-refraction through the standard 4/3 to super-refraction and ducting." />
<figcaption>Fig. 5: Horizon range for a 120 m terminal against the effective-Earth factor k. The standard 4/3 is one point on a curve that the atmosphere slides along, from sub-refraction (shortened horizon) through super-refraction toward ducting (greatly extended). The neat √h formula assumes a value of k that holds only on average.</figcaption>
</figure>

For a link designed to a fixed range this variability cuts both ways. Ducting is an opportunity for
occasional long reach and a hazard for co-channel interference from distant transmitters. Sub-
refraction is a fade mechanism that a static budget does not capture. The $4.12\sqrt{h}$ horizon is
a planning figure, not a guarantee for any given hour.

## A worked beyond-line-of-sight budget

The pieces combine into a range budget. Consider a drone relay at 900 MHz. The drone flies at 120 m
with a 2 dBi antenna and 30 dBm (1 W) transmit power. The ground station sits at 2 m with a 10 dBi
directional antenna. The target range is 40 km, inside the two-terminal radio horizon of
$4.12(\sqrt{120} + \sqrt{2}) \approx 51$ km, so the link is line of sight, though well past the
2.9 km breakpoint.

The path loss uses the $d^{4}$ regime. At 40 km the free-space figure is 123.6 dB, and the two-ray
loss is

$$
L_\text{2-ray} = 40\log_{10}(40000) - 20\log_{10}(120) - 20\log_{10}(2) = 136.5 \ \text{dB},
$$

an excess of 12.9 dB over free space. The received power is the transmitted power plus the two
antenna gains minus the path loss,

$$
P_r = 30 + 2 + 10 - 136.5 = -94.5 \ \text{dBm}.
$$

Whether the link closes is decided by the receiver sensitivity. From the previous post, sensitivity
is the noise density, the rate, the required energy per bit, and the implementation loss, with no
dependence on bandwidth [6]:

$$
P_\text{sens} = kT + \text{NF} + 10\log_{10} R_b + (E_b/N_0)_\text{req} + L_\text{impl}.
$$

At a data rate $R_b = 1$ Mbit/s, noise figure 5 dB, required $E_b/N_0$ of 8 dB, and 2 dB of
implementation loss,

$$
P_\text{sens} = -174 + 5 + 60 + 8 + 2 = -99 \ \text{dBm}.
$$

The link closes with a margin of $-94.5 - (-99) = 4.5$ dB. The full budget:

| Term | Value |
| :--- | ---: |
| Transmit power, $P_t$ | 30 dBm |
| Drone antenna gain | 2 dBi |
| Ground antenna gain | 10 dBi |
| Free-space loss at 40 km | −123.6 dB |
| Two-ray ($d^4$) excess | −12.9 dB |
| **Received power, $P_r$** | **−94.5 dBm** |
| Receiver sensitivity, $P_\text{sens}$ | −99.0 dBm |
| **Margin** | **4.5 dB** |

The design levers are visible in the budget. Raising the drone lifts the horizon and, for a fixed
range, does not change the path loss, but it protects the Fresnel clearance and buys margin against
sub-refraction. A lower data rate lowers the sensitivity directly, as the previous post showed. A
higher gain antenna helps, at the cost of pointing. Transmit power is the weakest lever, because it
scales the margin without changing the geometry that sets whether a link is possible at all.

## What the horizon formula hides

The $4.12\sqrt{h}$ horizon is a useful first number and a poor last one. It assumes a fixed
atmosphere, when $k$ swings from sub-refraction to ducting. It assumes a smooth sphere, when real
terrain both blocks and, through diffraction, carries the signal past the geometric edge. It treats
the horizon as a boundary, when the field beyond it is a predictable diffraction loss, not zero. And
it says nothing about path loss, which past the breakpoint follows the $d^{4}$ law rather than the
free-space figure most budgets quote.

Real BVLoS range is set by the full budget: the $d^{4}$ path loss, plus any diffraction loss beyond
the horizon, plus a fade margin, measured against the receiver sensitivity. The horizon marks where
free space ends, not where the link ends. The signal that survives past it, weak and diffracted,
still has to be pulled out of the noise, which is where the accounting of a later post on operating
under interference will begin.

## References

[1] J. D. Parsons, *The Mobile Radio Propagation Channel*, 2nd ed. Wiley, 2000.

[2] ITU-R Recommendation P.525, "Calculation of free-space attenuation," International
Telecommunication Union, Geneva, 2019.

[3] T. S. Rappaport, *Wireless Communications: Principles and Practice*, 2nd ed. Prentice Hall,
2002.

[4] ITU-R Recommendation P.526, "Propagation by diffraction," International Telecommunication
Union, Geneva, 2019.

[5] ITU-R Recommendation P.453, "The radio refractive index: its formula and refractivity data,"
International Telecommunication Union, Geneva, 2019.

[6] B. Razavi, *RF Microelectronics*, 2nd ed. Prentice Hall, 2011.
