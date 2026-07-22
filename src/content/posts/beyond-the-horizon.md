---
title: "The geometry of long-range radio links"
description: "How far a beyond visual line of sight (BVLoS) radio link reaches is set by geometry: the radio horizon, the antenna height that fixes it, and the diffraction that carries the signal past it."
date: 2026-07-11
tags: ["signals", "wireless"]
image: "/og/beyond-the-horizon.png"
---

A long-range terrestrial link, a drone relay, a sensor backhaul, a tactical radio, is limited by
the shape of the Earth as much as by its power budget. The received signal weakens with distance,
but the ground also curves away, and past a certain range the two terminals can no longer see each
other at all. That range, the horizon, is often quoted as the hard limit on a beyond visual line of
sight (BVLoS) link. It is not. Radio waves bend past the geometric edge, diffract into the
shadow behind it, and on some days duct for hundreds of kilometres. This post works through the
geometry and the propagation that set real BVLoS range, and closes with a drone budget tied to the
receiver sensitivity of [the previous post](/posts/beneath-the-noise-floor/).

## The radio horizon is not the range limit

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

One point deserves emphasis: even the radio horizon is only where the direct ray grazes, not where
the signal ends. Diffraction carries energy into the region beyond, so the radio horizon bounds line
of sight, not communication.

## The propagation regimes

Within radio line of sight the signal still weakens with distance, and it does so in stages that a
single free-space figure misses. Two distances mark the transitions. Take the running example of this
post: a 120 m drone linking a 2 m ground terminal at 900 MHz. The two terminals' horizons add, the
drone reaching 45 km on its own and the ground station a further 6 km, for a link radio horizon of
about 51 km. In practice this two-terminal figure sets the range, not either terminal alone. Nearer
in, the breakpoint falls at about 2.9 km, where the ground reflection begins to
cancel the direct ray and the loss steepens. The link radio horizon at 51 km is where the direct ray
is finally blocked and only diffraction reaches into the shadow. The two are an order of magnitude
apart, $2.9\ \text{km} \ll 51\ \text{km}$, and they play very different roles. A link passes through three regimes as range grows, measured against free space as
the reference:

| Regime | Distance | What happens | Falloff |
| :--- | :--- | :--- | :---: |
| Free space | reference | direct ray only, first Fresnel zone clear | $d^{2}$ |
| Two-ray, below breakpoint | $d < d_\text{bp}$ | direct and reflected rays oscillate around free space, with deep nulls | $\approx d^{2}$ |
| Two-ray, above breakpoint | $d_\text{bp} < d < d_\text{h}$ | direct and reflected rays nearly cancel | $d^{4}$ |
| Diffraction | $d > d_\text{h}$ | Earth blocks the direct ray, field bends into the shadow | steep |

where $d_\text{bp}$ is the breakpoint and $d_\text{h}$ the radio horizon. The first three regimes are
line of sight; only the last lies beyond it. Later sections put numbers on them: the two-ray loss and
its breakpoint, then the diffraction loss past the horizon.

The term "beyond line of sight" needs care against this map. Visual line of sight, the operator's
eyesight, is only a kilometre or two for a small drone, far shorter than the radio horizon. A BVLoS
drone link is beyond that *visual* limit but is kept within the *radio* horizon by flying high, so
the radio operates in the two-ray regime, not the diffraction regime. Crossing the radio horizon into
diffraction is the costly last resort, not the normal mode.

## Antenna height dominates

Because range grows as $\sqrt{h}$, height is the strongest lever on a terrestrial link. Doubling the
range requires four times the height. Raising one terminal from a 2 m tripod to a 120 m drone
extends its horizon from about 6 km to 45 km, nearly an eightfold gain from geometry alone. Figure 2
traces the square-root law.

<figure>
<img src="/posts/beyond-the-horizon/range-vs-height.svg" alt="Horizon range of a single terminal versus its height, the square-root curve, with mast, drone, and 500 m points marked." />
<figcaption>Fig. 2: The horizon range of a single terminal against its height. Range follows the √h law: a mast at 30 m reaches 23 km, a drone at 120 m reaches 45 km, and 500 m reaches 92 km. The shaded band is the refraction gain of the radio horizon (4.12√h) over the geometric one (3.57√h). A two-terminal link adds the second terminal's horizon, as in the worked budget below.</figcaption>
</figure>

Height is not simply another term in the budget. Transmit power adds decibels of margin to a link
that already closes, but no amount of power creates line of sight where the Earth blocks it. Past
the radio horizon the direct ray is gone, and the signal that remains has propagated by diffraction or
tropospheric scatter, with tens of decibels of excess loss. Height changes the propagation regime;
power only scales it. This is why a modest transmitter on a high platform outperforms a strong one
on the ground.

## Path loss beyond free space

The two line-of-sight regimes differ only in how fast the loss grows with distance. Free-space loss
follows the inverse-square law [2],

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

with $d$ and the heights in metres. It rises 40 dB per decade and does not depend on
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

## Diffraction and Fresnel clearance

Beyond the radio horizon the direct ray is blocked, yet a link can still close. Radio waves diffract around the
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

Two thresholds matter in practice. The first Fresnel zone is the ellipsoid around the direct ray
within which a secondary path is less than half a wavelength longer than the direct one, so an
obstruction inside it interferes with the signal. Its radius is
$F_1 = \sqrt{\lambda d_1 d_2 / (d_1 + d_2)}$, widest at midpath, and full free-space behaviour needs
the ray to clear the obstruction by about 0.6 of it; at grazing, where the ray just touches the
obstruction, a knife edge already costs 6 dB. This clearance is a line-of-sight criterion and applies
well within the radio horizon. The obstruction may be a hilltop or the Earth's own bulge rising into
the zone as the path lengthens. Clearance shrinks with range until the bulge grazes the ray at the
radio horizon; beyond it the direct ray is blocked, and the smooth-sphere diffraction loss, heavier
than a single knife edge, adds to the free-space path loss. The principle is the same throughout: the
shadow is illuminated at a cost that the geometry predicts.

## The atmosphere and the 4/3 fiction

The $k = 4/3$ factor rests on a standard refractivity gradient of about $-39$ N-units per kilometre.
That gradient is a long-term median, and the real atmosphere departs from it hour to hour. When the
gradient is weaker, the radio horizon shortens (sub-refraction). When it is stronger, it extends,
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

## A worked BVLoS budget

The pieces combine into a range budget for the running example. The drone at 120 m carries a 2 dBi
antenna and 30 dBm (1 W) of transmit power; the ground station at 2 m has a 10 dBi directional
antenna. The target range is 40 km, inside the two-terminal radio horizon of
$4.12(\sqrt{120} + \sqrt{2}) \approx 51$ km and well past the 2.9 km breakpoint, so by the map above
the link is line of sight, deep in the two-ray regime.

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

Whether the link closes is decided by the receiver sensitivity. From
[the previous post](/posts/beneath-the-noise-floor/), sensitivity is the noise density, the rate,
the required energy per bit, and the implementation loss, with no dependence on bandwidth [6]:

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

The design levers are visible in the budget. Raising the drone lifts the horizon, and in the two-ray
regime it also lowers the path loss by 20 dB for every tenfold increase in height, on top of protecting the Fresnel
clearance and buying margin against sub-refraction. A lower data rate lowers the sensitivity
directly, as the previous post showed. A
higher gain antenna helps, at the cost of pointing. Transmit power is the weakest lever because it
scales the margin without changing the geometry that sets whether a link is possible at all.

The height dependence makes this concrete. Fix the range at 40 km, along with the transmit power,
gains, and rate, and vary only the drone height, holding the ground terminal at 2 m. Within line of
sight the excess over free space is the two-ray figure; beyond the radio horizon it is the spherical-earth
diffraction loss of ITU-R P.526 [4], computed here for horizontal polarization over average ground,
which deepens quickly into the shadow.

| Drone height (ground 2 m) | Radio horizon | 40 km path | Excess over free space | Margin |
| :--- | :---: | :---: | :---: | :---: |
| 120 m | 51 km | within radio horizon | +12.9 dB (two-ray) | **+4.5 dB** |
| 40 m | 32 km | 8 km beyond radio horizon | +35.6 dB (diffraction) | **−18.2 dB** |
| 15 m | 22 km | 18 km beyond radio horizon | +46.1 dB (diffraction) | **−28.7 dB** |

At 120 m the radio horizon reaches 51 km, so the path is comfortably within line of sight and the
link closes with 4.5 dB of margin. Drop the drone to 40 m and the radio horizon falls to 32 km,
putting the
path 8 km into the diffraction shadow, where P.526 adds 36 dB and the link fails by 18 dB. At 15 m
the shadow is 18 km deep, the diffraction loss reaches 46 dB, and only far more height, gain, or a
far lower rate could recover it. Height does not merely trim the budget: it decides whether the link
is line of sight or diffraction-limited, a difference of tens of decibels.

## What the radio horizon formula hides

The $4.12\sqrt{h}$ radio horizon is a useful first number and a poor last one. It assumes a fixed
atmosphere when $k$ swings from sub-refraction to ducting. It assumes a smooth sphere when real
terrain both blocks the signal and diffracts it past the geometric edge. It treats the radio horizon
as a boundary when the field beyond it is a predictable diffraction loss, not zero. And it says
nothing about path loss, which past the breakpoint follows the $d^{4}$ law rather than the free-space
figure most budgets quote.

Real BVLoS range is set by the full budget: the $d^{4}$ path loss, plus any diffraction loss beyond
the radio horizon, plus a fade margin, measured against the receiver sensitivity. The radio horizon
marks where free space ends, not where the link ends. The signal that survives past it, weak and diffracted,
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
