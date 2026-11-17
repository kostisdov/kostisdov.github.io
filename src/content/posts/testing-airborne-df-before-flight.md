---
title: "Testing an airborne DF payload before it flies"
description: "On a drone, the airframe and the site below set the direction-finding error, not the noise. Argand Studio, a simulation suite for airborne DF, and an example: a small UAV with a circular array, calibrated on the airframe and flown over a suburb."
date: 2026-11-17
tags: ["signals", "wireless"]
draft: true
image: "/og/testing-airborne-df-before-flight.png"
---

Direction finding (DF) is used from radio astronomy to spectrum monitoring and signals intelligence.
It is hardest on a small aircraft. The array is a few wavelengths across at most, the airframe sits a
fraction of a wavelength from the antennas, and the ground and the buildings below return
multipath. An estimator that reaches the Cramér–Rao bound (CRB) on a free-space array can then be
off by degrees, and no amount of signal-to-noise ratio (SNR) brings it back. This post presents
Argand Studio, a simulation suite I built to find these errors before a payload flies, and walks
through one example.

<figure>
<video controls preload="metadata" playsinline poster="/posts/testing-airborne-df-before-flight/poster.jpg" style="width: 100%; height: auto;">
<source src="/posts/testing-airborne-df-before-flight/argand-studio.mp4" type="video/mp4" />
</video>
<figcaption>Argand Studio, from calibration on the airframe to a flight over a ray-traced site (2 min 23 s, no sound).</figcaption>
</figure>

## Three things the textbook leaves out

**The installed array.** A DF estimator compares the phases and amplitudes received at the
elements against a table of array response vectors, one per direction. The textbook table assumes
identical, uncoupled elements in free space. Mounted on an airframe, each element has its own
embedded pattern, shaped by the coupling to the other elements and by the field the structure
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

Argand Studio puts the three in one tool. It has four steps:

- **Platform.** The airframe and the array are modelled in Blender. The embedded pattern of every
  element is computed with a full-wave solver, openEMS (FDTD) [1] for the airframe, or NEC-2
  (method of moments) [2] for wire antennas alone. The result is the installed table of response
  vectors.
- **DF lab.** The estimators, correlative, interferometer and MUSIC [3], are plain Python, and a
  new one is a plug-in: copy one, change it, save it. A bench scores any of them on the installed
  array against the CRB [4], with the DF table either installed or textbook.
- **Mission.** The aircraft flies a path over a site built from OpenStreetMap buildings. Sionna
  RT [5] traces the paths to every emitter on the GPU. For every 0.1 s dwell, the in-phase and
  quadrature (IQ) samples at each element are synthesised from those paths and the installed
  patterns, then run through FFT-based detection, DF, association and geolocation.
- **Results.** Every bearing and position is scored against the truth and against the bound, and
  runs can be compared side by side: two arrays, two estimators or two sites, on the same flight,
  the same buildings and the same emitters. Each run can be replayed in 3D, with the flight, the
  ray paths and the bearings over time.

The physics and the geometry come from open tools, openEMS, NEC-2, Sionna RT, Blender and Rerun
for the replay; the DSP, DF, geolocation and the scoring are my own code.

The name honours Jean-Robert Argand, who in 1806 drew complex numbers as points in a plane [6].
Every phase a DF estimator compares lives on his diagram.

## An example: a small UAV over a suburb

### Calibration on the airframe

The platform is a small fixed-wing UAV with a wingspan of 0.8 m, modelled as a perfect conductor.
Five vertical half-wave dipoles form a uniform circular array at 900 MHz, hanging below the
fuselage (Fig. 1).

<figure>
<img src="/posts/testing-airborne-df-before-flight/fig1-platform.png" alt="The UAV seen from the side in Argand Studio's 3D view, with five vertical dipoles below the fuselage, next to the polar plot of each element's installed pattern." />
<figcaption>Fig. 1: The UAV and its five-element circular array in Argand Studio. Left: installed pattern of each element over azimuth, 15° below the horizon.</figcaption>
</figure>

The bench draws directions below the aircraft, synthesises snapshots from the installed response
with noise at a given SNR per element, and runs an estimator on them with each table. Table 1 is for
24 directions and 20 trials per direction and SNR.

| Table | SNR, dB | Median error (°) | Gross | RMSE / CRB |
| :--- | :---: | :---: | :---: | :---: |
| Textbook | 0 | 15.8 / 1.76 | 91 % | — |
| Textbook | 10 | 15.6 / 1.61 | 92 % | — |
| Textbook | 20 | 15.5 / 1.66 | 92 % | — |
| Textbook | 30 | 15.5 / 1.66 | 92 % | — |
| Installed | 0 | 0.35 / 0.35 | 0.2 % | 1.03 / 0.99 |
| Installed | 10 | 0.10 / 0.10 | 0 | 1.02 / 0.97 |
| Installed | 20 | 0.031 / 0.033 | 0 | 0.99 / 0.94 |
| Installed | 30 | 0.009 / 0.010 | 0 | 1.00 / 1.04 |

*Table 1: Correlative estimator on the installed array of Fig. 1, with each DF table: median
error in elevation / azimuth, the share of gross errors (beyond five standard deviations of the
bound and 5°), and RMSE / CRB in elevation / azimuth over the rest. MUSIC gives the same figures to
within 1 %.*

With the textbook table the elevation estimate is off by about 15° (median; the quick check in the
video, over four directions, shows 14°), and the error does not fall with SNR: it is a bias set by
the model. More than 90 % of the estimates are gross errors. With the installed table the same
estimator is efficient at every SNR. In practice the installed table comes from a model like this
one, from a measurement of the installed array, or from a calibration flight; the earlier post
compares them.

### Your estimator against the bound

The DF lab is where an estimator is developed. In the video, a copy of the correlative estimator
loses one line, the normalisation of each response vector. On the bench it reports elevation with a
bias of about 8°, every estimate an outlier, before it reaches a flight.

### A pass over a suburb

The site is 800 m by 800 m of low-rise housing from OpenStreetMap, with two emitters 1.5 m
above the street, each radiating −10 dBm in 25 kHz near 915 MHz. The aircraft flies a straight
300 m pass at 120 m and 15 m/s, 200 dwells of 0.1 s. Sionna RT traces up to three interactions per
path; over the pass there are about four paths per emitter and dwell, and the line of sight is
blocked for about 14 % of them. To isolate the effect of the site, the array is modelled alone
here, without the airframe.

The same pass is flown twice: with the five-element circular array, and with a five-element line
array along the fuselage at half-wavelength spacing. Table 2 compares them, and repeats the pass in
free space as a control.

| Array | Emitter | Error (°) | Error / CRB | In free space |
| :--- | :---: | :---: | :---: | :---: |
| Circle | E1 | 0.90 | 169 | 1.05 |
| Circle | E2 | 0.50 | 102 | 0.97 |
| Line | E1 | 0.56 | 140 | 1.08 |
| Line | E2 | 0.40 | 229 | 0.98 |

*Table 2: RMS DF error over the pass (azimuth for the circle, cone angle for the line), at an SNR of
34 dB per element, its ratio to the CRB, and that ratio for the same pass flown in free space.*

In free space both arrays sit at the bound. Over the suburb the errors are 100 to 230 times the
bound at the same SNR. At 34 dB the noise contributes almost nothing; the error is the multipath.
A bench in free space, however long, would not show it.

The line array looks more accurate, but it measures only the cone angle about its axis and cannot
tell left from right. On this straight pass, its geolocation keeps two mirror-image positions for
each emitter, with equal probability, until a turn or a second pass separates them. The circular
array measures a direction, and locates the two emitters to 1.4 m and 0.4 m.

<figure>
<img src="/posts/testing-airborne-df-before-flight/fig2-replay.png" alt="The replay dashboard at the end of the pass: on the left the suburb in 3D with the aircraft and the ray paths to the two emitters; on the right the position error against the predicted CEP50 for each track, the probability of the true position, the angle error over time, and a summary table." />
<figcaption>Fig. 2: Replay of the pass with the circular array, at its end. Left: the buildings, the aircraft and the ray paths to the two emitters. Right, from the top: each track's position error and predicted CEP50 (log10 of metres), the probability of the true position, the angle error over the pass, and the summary: DF RMSE / CRB, the position error (1.41 m and 0.42 m), the estimated and predicted CEP50, and the NEES.</figcaption>
</figure>

## Where it stands

Argand Studio is a working prototype, not yet a product, and I use it in consulting and pilot
projects: the array on the airframe, the estimator against the bound, and the whole chain over the
site where it will fly. If you are building an airborne DF or RF sensing payload and want to test it before it
flies, [get in touch](mailto:konstantinos.dovelos@gmail.com).

## References

[1] T. Liebig, "openEMS – Open Electromagnetic Field Solver," University of Duisburg-Essen.
[Online]. Available: https://www.openems.de

[2] G. J. Burke and A. J. Poggio, "Numerical Electromagnetics Code (NEC)—Method of Moments,"
Lawrence Livermore National Laboratory, Tech. Rep. UCID-18834, 1981.

[3] R. O. Schmidt, "Multiple emitter location and signal parameter estimation," *IEEE Transactions
on Antennas and Propagation*, vol. 34, no. 3, pp. 276–280, 1986.

[4] P. Stoica and A. Nehorai, "MUSIC, maximum likelihood, and Cramér–Rao bound," *IEEE Transactions
on Acoustics, Speech, and Signal Processing*, vol. 37, no. 5, pp. 720–741, 1989.

[5] J. Hoydis *et al.*, "Sionna RT: Differentiable ray tracing for radio propagation modeling,"
in *Proc. IEEE Globecom Workshops*, 2023.

[6] J.-R. Argand, *Essai sur une manière de représenter les quantités imaginaires dans les
constructions géométriques*, Paris, 1806.
