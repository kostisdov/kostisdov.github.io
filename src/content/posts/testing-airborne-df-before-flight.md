---
title: "Testing an airborne DF payload before it flies"
description: "On a small drone, the airframe and the site below can set the direction-finding error rather than the noise. Argand Studio, a simulation suite for airborne DF, shows this with a simple example: a small UAV whose circular array is modelled on its airframe and flown over a suburb."
date: 2026-11-18
tags: ["signals", "wireless"]
draft: false
image: "/og/testing-airborne-df-before-flight.png"
---

Finding where a radio signal comes from is the same problem in radio astronomy with arrays
kilometres across and in signals intelligence with a few antennas on a drone. Direction finding
(DF) is usually hardest on the drone. The array is a few wavelengths across at most, the airframe sits a
fraction of a wavelength from the antennas, and the ground and the buildings below return
multipath. An estimator that reaches the Cramér–Rao bound (CRB) on a free-space array can then be
off by degrees, and no amount of signal-to-noise ratio (SNR) brings it back. This post presents
Argand Studio, a simulation suite I built to find these errors before a payload flies, and walks
through one example.

<figure>
<video controls preload="metadata" playsinline poster="/posts/testing-airborne-df-before-flight/poster.jpg" style="width: 100%; height: auto;">
<source src="/posts/testing-airborne-df-before-flight/argand-studio.mp4" type="video/mp4" />
</video>
<figcaption>Argand Studio, from the array on the airframe to a flight over a ray-traced site (2 min 32 s, no sound). Buildings © OpenStreetMap contributors.</figcaption>
</figure>

## Three things the textbook leaves out

**The installed array.** A DF estimator compares the phases and amplitudes received at the
elements against a table of array response vectors, one per direction. The textbook table assumes
identical, uncoupled elements in free space. Mounted on an airframe, each element has its own
embedded pattern shaped by the coupling to the other elements and by the field the structure
scatters. An earlier post, [When the airframe joins the antenna array](/posts/when-the-airframe-joins-the-array),
quantifies this for a quadcopter: with the textbook table, MUSIC reported bearings tens of degrees
off; with the installed table it reached the bound.

**The site.** Over buildings, each emitter reaches the array along several paths: line of sight,
reflections from walls and from the ground. Coherent paths within a dwell bias the estimate
rather than adding noise to it, so the error depends on where the aircraft is, where the emitter
is, and what lies between them.

**The processing chain.** A bearing comes out of a chain: detection in the spectrum, the sample
covariance over a dwell, the estimator, association of detections to emitters, and geolocation.
Each step can fail in its own way, and only the whole chain, run on the signals the array would
actually receive, shows how they combine.

## Argand Studio

Argand Studio brings the three together in one tool with four steps:

- **Platform.** The airframe and the array are modelled in Blender. The embedded pattern of every
  element is computed with a full-wave solver, openEMS (FDTD) [1] for the airframe, or NEC-2
  (method of moments) [2] for wire antennas alone. The result is the installed table of response
  vectors.
- **DF lab.** The estimators, a correlative interferometer, a phase interferometer [3] and
  MUSIC [4], are plain Python, and a new one is a plug-in written from a copy of an existing one. A
  bench scores any of them on the installed array against the CRB [5], with the DF table either
  installed or textbook.
- **Mission.** The aircraft flies a path over a site built from OpenStreetMap buildings. Sionna
  RT [6] traces the paths to every emitter on the GPU. For every 0.1 s dwell, the in-phase and
  quadrature (IQ) samples at each element are synthesised from those paths and the installed
  patterns, then run through FFT-based detection, DF, association and geolocation.
- **Results.** Every bearing and position is scored against the truth and against the bound, and
  runs can be compared side by side: two arrays, two estimators or two sites, on the same flight,
  the same buildings and the same emitters. Each run can be replayed in 3D, with the flight, the
  ray paths and the bearings over time.

The name honours Jean-Robert Argand, who in 1806 drew complex numbers as points in a plane [7], the
plane on which every phase a DF estimator compares is drawn.

## An example: a small UAV over a suburb

### The array on the airframe

The platform is a small fixed-wing UAV with a wingspan of 0.8 m, modelled as a perfect conductor.
Five vertical half-wave dipoles form a uniform circular array at 900 MHz, hanging below the
fuselage (Fig. 1).

<figure>
<img src="/posts/testing-airborne-df-before-flight/fig1-platform.png" alt="An oblique 3D view of the UAV in Argand Studio, with five vertical dipoles below the fuselage, next to a polar plot of each element's installed pattern." />
<figcaption>Fig. 1: The UAV and its five-element circular array in Argand Studio. Left: installed pattern of each element (dB) over azimuth, 15° below the horizon. Right: the airframe and the array in the body frame.</figcaption>
</figure>

The bench draws directions below the aircraft, synthesises snapshots from the installed response
with noise at a given SNR per element, and runs an estimator on them with each table. Table 1 is for
24 directions, uniform in azimuth and 10° to 60° below the horizon, 20 trials per direction and SNR,
and 1042 snapshots (one 0.1 s dwell).

| Table | SNR, dB | Median error (°) | Gross | RMSE / CRB |
| :--- | :---: | :---: | :---: | :---: |
| Textbook | 0 | 15.8 / 1.76 | 91 % | — |
| Textbook | 10 | 15.6 / 1.61 | 92 % | — |
| Textbook | 20 | 15.5 / 1.66 | 92 % | — |
| Textbook | 30 | 15.5 / 1.66 | 92 % | — |
| Installed | 0 | 0.35 / 0.35 | 0.2 % | 1.03 / 0.99 |
| Installed | 10 | 0.10 / 0.10 | 0 % | 1.02 / 0.97 |
| Installed | 20 | 0.031 / 0.033 | 0 % | 0.99 / 0.94 |
| Installed | 30 | 0.009 / 0.010 | 0 % | 1.00 / 1.03 |

*Table 1: Correlative interferometer on the installed array of Fig. 1, with each DF table: median
error in elevation / azimuth, the share of gross errors (beyond five standard deviations of the
bound and 5°), and RMSE / CRB in elevation / azimuth over the rest, where RMSE / CRB is the RMSE over
the square root of the CRB (1 is efficient). MUSIC gives the same figures to within 1 %.*

With the textbook table the elevation estimate is off by about 15° (median), and the error does not
fall with SNR: it is a bias set by the model. Azimuth, which sets the bearing, is off by about 1.7°.
More than 90 % of the estimates are gross errors. With the installed table the same estimator
reaches the bound at every SNR. Here the table is the exact response of the model, so this is the
best case and tests the estimator rather than the table. In practice the table comes from a model, a
measurement of the installed array or a calibration flight, and each carries its own error. In the
earlier post, a model of the airframe still left about 2° of median error on a realistic drone, and
only a calibration flight came close to the bound.

Fig. 2 shows why the textbook table fails. For one emitter 30° below the horizon, the textbook table's score peaks 12° too
close to the horizon, because the phases the airframe imposes on the elements match a different
direction of the free-space array. With the installed table the peak falls on the true direction.

<figure>
<img src="/posts/testing-airborne-df-before-flight/spectrum.svg" alt="Two maps of the correlative score over azimuth and elevation below the horizon: with the textbook table the peak lies 12 degrees above the true direction, with the installed table it lies on it." />
<figcaption>Fig. 2: Correlative-interferometer score for one emitter at azimuth 40°, 30° below the horizon, at 20 dB SNR per element, on the 2° search grid (half of the azimuth range shown). Circle: true direction; cross: peak. Left: textbook table. Right: installed table.</figcaption>
</figure>

### An estimator against the bound

Estimators are developed in the DF lab. In the video, a copy of the correlative interferometer
loses one line, the normalisation of each response vector. On the bench it shows an elevation bias
of about 8° with every estimate a gross error, so the mistake is caught before any flight.

### A pass over a suburb

The site is 800 m by 800 m of low-rise housing, with building footprints from OpenStreetMap and
heights set to 9 m where OpenStreetMap gives none, as for most of them. Two emitters stand 1.5 m
above the street, each radiating −10 dBm in 25 kHz near 915 MHz. The aircraft flies a straight
300 m pass at 120 m and 15 m/s, 200 dwells of 0.1 s. Sionna RT traces up to three specular
reflections per path (no diffraction or diffuse scattering); over the pass there are about four
paths per emitter and dwell. The line of sight to E1 is blocked for about a quarter of the pass, while
E2 stays in view. To isolate the effect of the site, the array is modelled alone here, without the
airframe.

The same pass is flown twice, with the five-element circular array and with a five-element line
array along the fuselage, both at half-wavelength spacing between neighbours. Table 2 compares them
and repeats the pass in free space as a control.

| Array | Emitter | Error (°) | Error / CRB | Error / CRB, free space |
| :--- | :---: | :---: | :---: | :---: |
| Circle | E1 | 0.90 | 169 | 1.05 |
| Circle | E2 | 0.50 | 102 | 0.97 |
| Line | E1 | 0.56 | 140 | 1.08 |
| Line | E2 | 0.40 | 229 | 0.98 |

*Table 2: RMS DF error over the pass (azimuth for the circle, cone angle for the line), at a
free-space SNR of about 34 dB per element, its ratio to the single-path CRB, and that ratio for the
same pass flown in free space.*

In free space both arrays sit at the bound, while over the suburb the errors are 100 to 230 times
the bound at the same SNR. At 34 dB the noise contributes almost nothing, so the error comes from the
multipath, which no free-space bench would show.

Fig. 3 follows the error dwell by dwell. E2 stays in view, yet from about 6 s on its error swings back
and forth about once a second, the pattern a direct path and a reflection produce as their relative phase turns with
the motion of the aircraft. While the line of sight to E1 is blocked, the bearing follows the
reflections and carries a steady bias. In free space the same pass gives an error that stays at zero
on this scale.

<figure>
<img src="/posts/testing-airborne-df-before-flight/error-along-pass.svg" alt="Azimuth error per dwell for the two emitters along the 20 second pass: over the suburb it oscillates by up to a few degrees, with a steady bias for E1 while its line of sight is blocked; in free space it stays at zero." />
<figcaption>Fig. 3: Azimuth error of the circular array per 0.1 s dwell along the pass, over the suburb and in free space. Shaded: line of sight to the emitter blocked.</figcaption>
</figure>

The line array looks more accurate, but the two angles are not directly comparable: it measures only
the cone angle about its axis and cannot tell left from right. On this straight pass its geolocation
keeps two mirror-image positions for each emitter with equal probability until a turn or a second
pass separates them. The circular array measures a direction and locates the two emitters to 1.4 m and 0.4 m at the end of the
pass, from slant ranges of about 160 to 400 m, against a predicted CEP50 of about 1 m.

<figure>
<img src="/posts/testing-airborne-df-before-flight/fig2-replay.png" alt="The replay dashboard at the end of the pass: on the left the suburb in 3D with the aircraft and the ray paths to the two emitters; on the right the position error against the predicted CEP50 for each track, the probability of the true position, the angle error over time, and a summary table." />
<figcaption>Fig. 4: Replay of the pass with the circular array, at its end. Left: the buildings, the aircraft and the ray paths to the two emitters. Right, from the top: each track's position error and predicted CEP50 (log10 of metres), the probability of the true position, the angle error over the pass, and the summary: DF RMSE / CRB, the position error (1.41 m and 0.42 m), the estimated and predicted CEP50, and the NEES. The aircraft is not to scale. Buildings © OpenStreetMap contributors.</figcaption>
</figure>

## Limitations

The example uses one airframe modelled as a perfect conductor, and on the bench the installed table
is the exact response of that model. The site runs use the array without the airframe, specular
reflections only and default building heights. Receiver channels are ideal, the heading and attitude
are known exactly, and geolocation is given the emitters' height above the ground. Each result comes
from one pass with one seed, and nothing here has been flown.

## Where it stands

Argand Studio is a working prototype, and it already makes DF testing much more realistic than a
free-space bench: the array is modelled on its airframe, estimators are scored against the bound,
and the whole chain runs over the site where the payload will fly. It is available for consulting
and pilot projects. If you are building an airborne DF or RF sensing payload and want to
test it before it flies, [get in touch](mailto:konstantinos.dovelos@gmail.com).

## References

[1] T. Liebig, "openEMS – Open Electromagnetic Field Solver," University of Duisburg-Essen.
[Online]. Available: https://www.openems.de

[2] G. J. Burke and A. J. Poggio, "Numerical Electromagnetics Code (NEC)—Method of Moments,"
Lawrence Livermore National Laboratory, Tech. Rep. UCID-18834, 1981.

[3] P. J. D. Gething, *Radio Direction Finding and Superresolution*, 2nd ed. London: Peter
Peregrinus, 1991.

[4] R. O. Schmidt, "Multiple emitter location and signal parameter estimation," *IEEE Transactions
on Antennas and Propagation*, vol. 34, no. 3, pp. 276–280, 1986.

[5] P. Stoica and A. Nehorai, "Performance study of conditional and unconditional direction-of-arrival
estimation," *IEEE Transactions on Acoustics, Speech, and Signal Processing*, vol. 38, no. 10,
pp. 1783–1795, 1990.

[6] J. Hoydis *et al.*, "Sionna RT: Differentiable ray tracing for radio propagation modeling,"
in *Proc. IEEE Globecom Workshops*, 2023.

[7] J.-R. Argand, *Essai sur une manière de représenter les quantités imaginaires dans les
constructions géométriques*, Paris, 1806.
