---
title: "Decoupling a packed CRPA: elements, ports, or weights"
description: "A controlled reception pattern antenna must shrink for platforms limited in size, weight, and power, and mutual coupling then limits its nulling. A NEC-2 study of decoupled and coupled architectures for a packed GNSS anti-jam array."
date: 2026-11-04
tags: ["wireless"]
draft: false
---

A controlled reception pattern antenna (CRPA) protects a GNSS receiver from jamming, using digital weights that place nulls towards the interferers. Platforms limited in size, weight, and power (SWaP) need a small array, yet closely spaced antennas interact electromagnetically. A current on one element induces a voltage on its neighbours, as described by the impedance matrix $\mathbf{Z}$ at the ports,

$$
\mathbf{v} = \mathbf{Z}\,\mathbf{i}.
$$

Coupling has two consequences. First, port $n$ sees the active impedance

$$
[\mathbf{Z}_a]_{n,n} = \sum_{m=0}^{N-1} [\mathbf{Z}]_{n,m}\,\frac{i_m}{i_n},
$$

which changes with the excitation. A fixed matching circuit is therefore correct for one excitation only, and part of the power is reflected at the others. Second, with $\mathbf{R} = \mathrm{Re}\{\mathbf{Z}\}$, the power at the ports is $P_{\mathrm{in}} = \tfrac{1}{2}\mathbf{i}^{\mathsf H}\mathbf{R}\,\mathbf{i}$, and the gain towards a steering vector $\mathbf{a}$ is maximized by [1]

$$
\mathbf{i}_{\mathrm{opt}} \propto \mathbf{R}^{-1}\mathbf{a}.
$$

These currents are phase-only when $\mathbf{R}$ is a scaled identity. The off-diagonal entries of $\mathbf{R}$ measure how much the element patterns overlap over the sphere. Those of $\mathrm{Im}\{\mathbf{Z}\}$ carry no net radiated power, so a lossless circuit can cancel them.

Mutual coupling is typically addressed by decoupling, yet the word covers three different operations. This post shows that they form two array architectures, and it compares their nulling capability as a CRPA is packed into a smaller footprint.

## A packed CRPA

One published CRPA has seven patches in an array of 36.5 cm, with a spacing close to $0.7\lambda$ at L1, chosen to limit the mutual coupling [2]. The test case keeps seven elements, one at the centre and six on a ring, and reduces the spacing to $0.15\lambda$. At L1, this shrinks the ring from 26.6 to 5.7 cm.

For the NEC-2 simulation [3], the elements are horizontal half-wave copper dipoles a quarter wavelength over a perfect ground, with a gain of 7.5 dBi at zenith. Unlike patches, they share one axis and one linear polarization. The response to a circularly polarized wave therefore varies by 7.8 dB in azimuth at $30^\circ$ of elevation. Their length of 9.5 cm also limits the reduction in total extent, from 35 to 15 cm. Fig. 1 shows the array at two spacings. The neighbouring coupling, with self-conjugate terminations, grows from $-19$ dB at $0.7\lambda$ to $-4$ dB at $\lambda/4$.

<figure>
<img src="/posts/decoupling-an-antenna-array/fig1-crpa.svg" alt="Top views at the same scale of seven horizontal dipoles at a spacing of 0.7 wavelengths, in a ring of 26.6 cm with an extent of 35 cm and neighbouring coupling of minus 19 dB, and at a spacing of a quarter wavelength, in a ring of 9.5 cm with an extent of 19 cm and neighbouring coupling of minus 4 dB. A side view shows dipoles over a ground plane, each with its own low-noise amplifier, and weights from the measured covariance. The reception pattern has a null towards a jammer and covers two satellites." />
<figcaption>Fig. 1: The simulated CRPA at two spacings, at the same scale, and its receive chain. The layout follows the dimensions in [2], with a centre element and six on a ring inferred from them. The reception pattern is illustrative.</figcaption>
</figure>

All results for a given number of jammers use the same 2,000 random scenes. Satellites lie above $15^\circ$ of elevation, and jammers lie between $5^\circ$ and $40^\circ$, each 50 dB above the noise of an isolated dipole at zenith. All signals are right-hand circularly polarized. The noise combines the first amplifier at 170 K, the sky and ground at 100 K through the radiation resistance, and the ohmic resistance at 290 K. The last two reach the ports through the coupling and any network.

The weights are minimum-variance weights from the measured covariance $\mathbf{R}_y$ [4], $\mathbf{w} \propto \mathbf{R}_y^{-1}\mathbf{h}$, where $\mathbf{h}$ is the calibrated satellite response. With one coefficient per port, they have six degrees of freedom. Power inversion [5], which needs no satellite direction, is also reported.

The metric is the output SINR, relative to the jam-free SNR of an isolated dipole at zenith. The tables also give the share of scenes above $-6$ dB, an illustrative threshold for one satellite rather than a position availability. Without jammers, this share is 89% to 99%, because of the dipole pattern.

Impedance mismatch lowers the received signal directly. For port wave amplitudes $\mathbf{a}$ with $\|\mathbf{a}\| = 1$ and a scattering matrix $\mathbf{S}$, the realized gain factors as

$$
G_r = \left(1 - \|\mathbf{S}\mathbf{a}\|^2\right) e_{\mathrm{rad}}\, D,
$$

where the first factor is the fraction of the power that is not reflected, $e_{\mathrm{rad}}$ is the radiation efficiency, and $D$ is the directivity.

## Three operations, two architectures

The three operations act at different points between the antenna and the receiver.

- **Element decoupling** adds a physical structure, or a larger spacing, that reduces the interaction of the antennas.
- **Port decoupling** adds a network that removes the coupling seen at the ports. The antennas stay coupled.
- **Digital compensation** changes only the weights. The antennas and the circuit stay as they are.

Fig. 2 groups them into two architectures. The decoupled architecture uses element decoupling. The coupled architecture uses port decoupling and digital compensation together. Every array here also uses digital weights for nulling, so the architectures differ in how they treat the coupling.

<figure>
<img src="/posts/decoupling-an-antenna-array/fig2-architectures.svg" alt="Three signal chains between two dipoles and their ports, grouped into two architectures. The decoupled architecture is element decoupling, with one match per port and a loaded parasitic wire between the dipoles. The coupled architecture has two parts: port decoupling, with a lossless network between all ports and all dipoles, and digital compensation, with weights computed from measurements. In both parts the dipoles stay coupled." />
<figcaption>Fig. 2: The three meanings of decoupling and the two architectures, shown for two elements.</figcaption>
</figure>

| | Element decoupling | Port decoupling | Digital compensation |
|---|---|---|---|
| Typical means | Spacing, band-gap surfaces, walls, parasitic elements | Lossless $2N$-port network | Weights from measurements |
| Mutual impedances | Reduced | Unchanged | Unchanged |
| Port coupling $S_{21}$ | Reduced | Zero at the design frequency | Unchanged |
| Mismatch | Can be reduced | Removed at the design frequency | Not addressed |

## The decoupled architecture

### Principle

This architecture reduces the interaction between the antennas themselves. In the ideal case, $\mathbf{Z}$ is diagonal, and a one-port match then holds for every excitation. The optimal currents are phase-only. The textbook steering vectors also apply if the element patterns remain identical, but a packed array cannot satisfy this, because a diagonal $\mathbf{R}$ requires orthogonal patterns.

The simplest means is spacing, which is the choice in [2]. When the footprint does not allow it, a structure is placed between the elements, such as an electromagnetic band-gap (EBG) surface [6], a wall, or a parasitic element. The structure becomes part of the radiator, so both the impedance matrix and the element patterns change. For one wire $p$ between elements 1 and 2, terminated in a reactance $X$, the impedances become

$$
Z_{12}' = Z_{12} - \frac{Z_{1p}\,Z_{p2}}{Z_{pp} + jX},
\qquad
Z_{11}' = Z_{11} - \frac{Z_{1p}^2}{Z_{pp} + jX}.
$$

The wire can oppose the direct coupling, but it changes the self-impedance at the same time.

The structure tested here has one wire midway between each of the 12 neighbouring pairs. The sweep covers wire lengths from $0.2\lambda$ to $1.0\lambda$ and load reactances from $-1500$ to $+1500$ Ω, about 12,000 designs per spacing. The chosen design has the lowest worst-case $|S_{21}|$ with a self-resistance of at least 20 Ω. The selection uses $S_{21}$ only. It gives a length of $0.38\lambda$ and a load of $+200$ Ω at $0.35\lambda$, and a length of $0.30\lambda$ and a load of $+300$ Ω at $\lambda/4$.

### Result

The wires reduce the coupling without improving the nulling. At $\lambda/4$, $|S_{21}|$ falls from $-4.3$ to $-10.1$ dB. The median SINR with one jammer stays near $0.7$ dB, and with three jammers it falls from $-3.1$ to $-3.7$ dB. At $0.35\lambda$, $|S_{21}|$ falls from $-6.1$ to $-14.3$ dB, whereas the SINR with three jammers falls from $-0.2$ to $-4.0$ dB. A lower $|S_{21}|$ is available at $\lambda/4$, down to $-23$ dB, but only with a self-resistance of 3 Ω.

A low $|S_{21}|$ alone is therefore not sufficient. A decoupler must also preserve the self-resistance and the element pattern, and near-resonant wires add ohmic loss. Over the range swept, this wire structure does not achieve this. The selected design is also sensitive.

## The coupled architecture

This architecture retains the coupling. It has two parts, a network and the weights.

### Port decoupling

A lossless $2N$-port network $\mathbf{Z}_M$ sits between the antenna ports and the amplifiers, an approach studied since the 1970s [7], [8]. The impedance at the outer ports becomes [1]

$$
\mathbf{Z}_T = \mathbf{Z}_{M11} - \mathbf{Z}_{M12}\left(\mathbf{Z} + \mathbf{Z}_{M22}\right)^{-1}\mathbf{Z}_{M21}.
$$

The goal is $\mathbf{Z}_T = Z_s^* \mathbf{I}_N$ for terminations of impedance $Z_s$, with $R_s = \mathrm{Re}\{Z_s\}$. It is met by [1], [9]

$$
\mathbf{Z}_M = \begin{bmatrix} -j\,\mathrm{Im}\{Z_s\}\,\mathbf{I}_N & -j\sqrt{R_s}\,\mathbf{R}^{1/2} \\ -j\sqrt{R_s}\,\mathbf{R}^{1/2} & -j\,\mathrm{Im}\{\mathbf{Z}\} \end{bmatrix}.
$$

The network performs two separate functions. The block $-j\,\mathrm{Im}\{\mathbf{Z}\}$ cancels the reactive coupling. The block $\mathbf{R}^{1/2}$ acts on the radiative coupling, which cannot be tuned out because it is the overlap of the patterns. It changes basis instead, so that each outer port connects to a weighted combination of all the elements. The outer currents $\mathbf{i}_M$ and the element currents are related by

$$
\mathbf{i}_M = \frac{j}{\sqrt{R_s}}\,\mathbf{R}^{1/2}\,\mathbf{i},
\qquad\text{so that}\qquad
P_{\mathrm{in}} = \tfrac{1}{2}R_s\,\|\mathbf{i}_M\|^2.
$$

The power is now a sum over the outer ports, whatever the weights. The ports are decoupled while the elements remain coupled. The matrix $\mathbf{Z}$ has not changed, and a current on one element still induces a voltage on the next. In the simulation, the port scattering matrix is numerically zero at the design frequency. For $N = 7$, the two symmetric blocks of $\mathbf{Z}_M$ contain 56 independent reactive values.

### Digital compensation

Digital compensation changes neither the antennas nor the circuit. It is beamforming that accounts for the coupling, and it does not address the impedance mismatch. One classical form corrects the excitation with a coupling matrix, which can be computed or measured [10], [11]. A CRPA goes further, because the measured covariance already contains the coupling, the element patterns, and the mismatch. No knowledge of $\mathbf{Z}$ is needed to place a null, although the satellite response $\mathbf{h}$ still has to be calibrated.

Measured weights matter at every spacing. With nulls computed from the textbook steering vectors, the median SINR with one jammer is $-19$ dB at $0.7\lambda$ and $-38$ dB at $\lambda/4$, because the true response differs from the model. The measured covariance brings these to $3.0$ and $0.7$ dB.

### Result

The two parts are complementary. With the network, the response becomes $\mathbf{h} \propto \mathbf{R}^{-1/2}\mathbf{a}^*$ [1], [9]. Matched weights then give $\mathbf{i} \propto \mathbf{R}^{-1}\mathbf{a}$, the optimal currents above, with no reflection for any excitation. This is the superdirective architecture [1], [12]. The benefit here arises mainly from the weak modes of $\mathbf{R}$, which the network lifts above the amplifier noise. At $\lambda/4$, the eigenvalues of $\mathbf{R}$ span 1.1 to 488 Ω. A lossless network is an invertible map, so without amplifier noise it would not change the SINR.

The network improves the nulling at this spacing. The median SINR rises from $0.7$ to $4.4$ dB with one jammer, and from $-3.1$ to $1.8$ dB with three.

## Nulling against footprint

Fig. 3 and the tables below give the result for narrowband jammers. "Weights only" terminates each port in the conjugate of its self-impedance. This gave a higher SINR than a match to the active impedance at zenith, which reaches only $-5.6$ dB with three jammers at $\lambda/4$. The textbook model has no coupling, with isolated patterns and array phases, so it shows what the footprint alone would cost.

<figure>
<img src="/posts/decoupling-an-antenna-array/fig3-nulling.svg" alt="Two panels of median output SINR against the element spacing from 0.15 to 0.7 wavelengths, for one and for three jammers. With a network and weights the SINR stays between about minus 1 and 5 dB at all spacings. With weights only it falls to about minus 2 dB with one jammer and minus 9 dB with three jammers at the smallest spacing. The uncoupled textbook model is similar to the case with weights only. The wire decoupler has points at 0.25 and 0.35 wavelengths, at or below the case with weights only." />
<figcaption>Fig. 3: Median output SINR against the element spacing, with narrowband jammers and one coefficient per port.</figcaption>
</figure>

| One jammer | Ring / extent | Weights only | With wires | Network | Textbook model |
|---|---|---|---|---|---|
| $0.7\lambda$ | 27 / 35 cm | 3.0 (89%) | – | 3.1 (89%) | 3.0 (88%) |
| $\lambda/2$ | 19 / 28 cm | 4.1 (94%) | – | 4.6 (94%) | 3.3 (90%) |
| $0.35\lambda$ | 13 / 22 cm | 2.9 (91%) | 0.2 (88%) | 4.8 (96%) | 2.8 (88%) |
| $\lambda/4$ | 10 / 19 cm | 0.7 (86%) | 0.8 (88%) | 4.4 (95%) | 1.9 (84%) |
| $0.15\lambda$ | 6 / 15 cm | −2.4 (74%) | – | 2.9 (92%) | −1.0 (75%) |

| Three jammers | Ring / extent | Weights only | With wires | Network | Textbook model |
|---|---|---|---|---|---|
| $0.7\lambda$ | 27 / 35 cm | −0.8 (70%) | – | −0.7 (70%) | −0.8 (70%) |
| $\lambda/2$ | 19 / 28 cm | 1.0 (80%) | – | 1.5 (81%) | 0.7 (76%) |
| $0.35\lambda$ | 13 / 22 cm | −0.2 (76%) | −4.0 (63%) | 2.0 (82%) | −1.0 (71%) |
| $\lambda/4$ | 10 / 19 cm | −3.1 (64%) | −3.7 (62%) | 1.8 (82%) | −4.8 (56%) |
| $0.15\lambda$ | 6 / 15 cm | −9.2 (33%) | – | −0.1 (75%) | −12.4 (21%) |

Each entry gives the median SINR in dB and, in parentheses, the share of scenes above $-6$ dB. Ring and extent are at L1.

Without a network, packing costs nulling capability, as the tables show. A spacing of $\lambda/2$ is the best of these cases, and $0.7\lambda$ is no better.

For narrowband jammers, the network removes most of this cost, and the SINR stays comparable with the largest array. With three jammers, the network adds $4.9$ dB at $\lambda/4$ and $9.1$ dB at $0.15\lambda$, against $0.5$ dB at $\lambda/2$ and $0.1$ dB at $0.7\lambda$. This margin limits the acceptable insertion loss of a real network. Each decibel of loss costs about $1.5$ dB here, because the loss also adds noise. At $\lambda/4$, the network is therefore worthwhile only with a loss below about 3 dB.

Coupling is not only a loss. At $\lambda/4$, the textbook model overstates the jam-free gain at zenith by $7.6$ dB, yet its SINR with three jammers is lower than that of the real array. With one jammer and one satellite at $30^\circ$ of elevation, the SINR comes within 3 dB of its jam-free level at $55^\circ$ of azimuth from the jammer in the textbook model, at $35^\circ$ in the real array, and at $30^\circ$ with the network.

Coverage also differs. The table gives the jam-free response, in dB relative to the reference. Packing without a network loses gain everywhere. The network gives up gain at zenith, compared with a large array, but its gain stays nearly flat, so at low elevation it exceeds the large array. The textbook model predicts $8.5$ dB at zenith and $2.8$ dB at $30^\circ$ of elevation at every spacing.

| Spacing | Weights only, zenith | Weights only, 30° elevation | Network, zenith | Network, 30° elevation |
|---|---|---|---|---|
| $0.7\lambda$ | 8.0 | 2.5 | 8.3 | 2.7 |
| $\lambda/2$ | 5.9 | 3.5 | 6.8 | 4.4 |
| $0.35\lambda$ | 3.1 | 2.1 | 6.0 | 5.1 |
| $\lambda/4$ | 0.9 | 0.4 | 5.4 | 5.2 |
| $0.15\lambda$ | −1.4 | −2.1 | 3.5 | 4.0 |

Power inversion also benefits. It does not steer towards the satellite, and it depends on the reference element. With a ring element as the reference and one jammer at $\lambda/4$, its median SINR is $-9.1$ dB without a network and $-4.1$ dB with one.

Not all six degrees of freedom are usable. With six jammers, the median SINR is $-14.4$ dB at $0.7\lambda$, $-14.8$ dB at $\lambda/4$, and $-9.4$ dB at $\lambda/4$ with the network. With four jammers at $\lambda/4$, it is $-5.0$ dB without a network and $0.3$ dB with one.

## Wideband jammers and tolerance

These results assume narrowband jammers and ideal circuits at one frequency. A real jammer may occupy the whole GNSS band, and 20 MHz at L1 is 1.3%. The table below holds the circuits at their values at L1 and spreads three jammers over the band. The last column adds five taps per element at the Nyquist rate of the band, as in space-time adaptive processing [13].

| Spacing | Array | Narrowband | 2 MHz | 20 MHz | 20 MHz, 5 taps |
|---|---|---|---|---|---|
| $\lambda/2$ | Weights only | 1.0 | 0.8 | −2.9 | 0.7 |
| $\lambda/2$ | Network | 1.5 | 0.3 | −4.2 | 0.9 |
| $\lambda/4$ | Weights only | −3.1 | −3.5 | −7.5 | −3.5 |
| $\lambda/4$ | With wires | −3.7 | −7.8 | −22.2 | −5.1 |
| $\lambda/4$ | Network | 1.8 | −4.5 | −20.9 | 0.2 |
| $0.15\lambda$ | Weights only | −9.2 | −9.3 | −12.1 | −9.4 |
| $0.15\lambda$ | Network | −0.1 | −14.5 | −29.8 | −3.4 |

With one coefficient per port, the network loses its advantage from about 2 MHz, and at 20 MHz it falls below the array without a network. The weak modes change quickly with frequency, so a single weight cannot hold a deep null across the band. The wire structure falls in the same way.

With five taps per element, the network recovers its advantage. The result depends on the number of taps. At $\lambda/4$, three taps give $-4.5$ dB, below the $-3.7$ dB without a network, and seven give $0.7$ dB. The coupled architecture therefore needs space-time processing, with its higher digital cost, against jammers of about 2 MHz or more.

Fig. 4 shows these effects in the reception patterns of one scene, with three jammers and a satellite at $30^\circ$ of elevation. The response is relative to the output noise, so a jammer 50 dB above the noise stays below the noise when the response towards it is below $-50$ dB. For narrowband jammers, all four arrays place nulls below $-100$ dB, which is optimistic because the covariance is exact. They differ only in the rest of the pattern. Over 20 MHz with one coefficient per port, the nulls fill in. The response towards the jammers is $-46$ dB or lower at $\lambda/2$ and $-47$ dB or lower at $\lambda/4$ with weights only, but only $-32$ dB with the network and $-22$ dB with wires. With five taps per port, all nulls return to $-64$ dB or lower, and the network keeps the highest response towards the satellite.

<figure>
<img src="/posts/decoupling-an-antenna-array/fig4-patterns.svg" alt="Three panels of the reception pattern against azimuth at 30 degrees of elevation, with jammers at 60, 150, and 240 degrees and a satellite at 330 degrees, for an array at half a wavelength with weights only, and at a quarter wavelength with weights only, with wires, and with a network. With narrowband jammers all arrays have deep nulls at the three jammers. Over 20 MHz with one coefficient per port, the nulls fill in, most for the wires and the network. With five taps per port, all nulls are deep again, and the network has the highest response towards the satellite." />
<figcaption>Fig. 4: Reception patterns of one scene, as the response per unit incident power over the output noise. Over 20 MHz, the response is averaged over the band of the jammers. The axis is clipped at $-75$ dB. The nulls are sampled on a $5^\circ$ grid.</figcaption>
</figure>

The taps column holds for a narrowband signal at L1, because the weights are constrained on a single tone. For a coherent signal of 2 MHz at $\lambda/4$, the values are $-0.9$ dB with the network and $-4.7$ dB without. For a signal of 20 MHz, this constraint fails for all arrays, at about $-20$ dB. Wideband signals such as P(Y) or M-code need other constraints, which are not studied here.

Measured weights also compensate for part of the tolerance of the network, if the satellite response is recalibrated. With three jammers at $\lambda/4$, the median SINR is $2.1$ dB with 1% rms random errors on the network values and $1.3$ dB with 5%, or $0.6$ dB with the design response. At $0.15\lambda$, 5% errors reduce it to $-3.0$ dB.

## Key takeaways

**Packing a CRPA costs nulling capability, and measured weights are essential at any spacing. If the array must be smaller than about $0.35\lambda$, keep the coupling and add a multi-port network, but only if its loss stays below about 3 dB and space-time taps can be added against wideband jammers.**

The three operations reduce to two design options, keeping the coupling or removing it. Three cases follow.

- **The footprint allows about $\lambda/2$.** Remove the coupling with spacing, and use measured weights. A network adds only $0.5$ dB.
- **The array must be packed to $\lambda/4$ or below.** Keep the coupling. Port decoupling and digital compensation together form the superdirective architecture. With three narrowband jammers, the network adds $4.9$ dB at $\lambda/4$ and $9.1$ dB at $0.15\lambda$. It has 56 reactive values, and each decibel of its loss costs about $1.5$ dB. Against jammers of about 2 MHz or more, it needs taps. With five taps at $\lambda/4$ and a narrowband signal, its margin falls to $3.6$ dB, so the acceptable loss falls to about 2 dB.
- **A physical structure at small spacing.** The wire decoupler tested here lowered $|S_{21}|$ but did not improve the nulling. This covers one wire structure, and other structures may behave differently.

## Limitations

This is a simulation of dipoles over a perfect ground, with no measurement. Real packed CRPAs use small patches, and the wire decoupler does not represent EBG surfaces or metasurface walls. The network is lossless, except where stated, and frequency-independent, which favours it. The weights use a calibrated satellite response and an exact covariance. The SINR does not capture carrier-phase and group-delay biases.

The simulation code and the data behind these results are available on [GitHub](https://github.com/kostisdov/array-decoupling).

## References

[1] K. Dovelos, S. D. Assimonis, H. Q. Ngo, and M. Matthaiou, "Superdirective antenna pairs for energy-efficient terahertz massive MIMO," *IEEE Transactions on Communications*, 2023. [arXiv:2207.00697](https://arxiv.org/abs/2207.00697).

[2] F. Leveau, S. Boucher, E. Goron, and H. Lattard, "Anti-jam protection by antenna," *GPS World*, Feb. 2013.

[3] G. J. Burke and A. J. Poggio, "Numerical Electromagnetics Code (NEC): Method of moments," Lawrence Livermore National Laboratory, Tech. Rep. UCID-18834, 1981.

[4] J. Capon, "High-resolution frequency-wavenumber spectrum analysis," *Proceedings of the IEEE*, vol. 57, no. 8, pp. 1408–1418, 1969.

[5] R. T. Compton, "The power-inversion adaptive array: Concept and performance," *IEEE Transactions on Aerospace and Electronic Systems*, vol. 15, no. 6, pp. 803–814, 1979.

[6] F. Yang and Y. Rahmat-Samii, "Microstrip antennas integrated with electromagnetic band-gap structures: A low mutual coupling design for array applications," *IEEE Transactions on Antennas and Propagation*, vol. 51, no. 10, pp. 2936–2946, 2003.

[7] J. B. Andersen and H. H. Rasmussen, "Decoupling and descattering networks for antennas," *IEEE Transactions on Antennas and Propagation*, vol. 24, no. 6, pp. 841–846, 1976.

[8] C. Volmer, J. Weber, R. Stephan, K. Blau, and M. A. Hein, "An eigen-analysis of compact antenna arrays and its application to port decoupling," *IEEE Transactions on Antennas and Propagation*, vol. 56, no. 2, pp. 360–370, 2008.

[9] M. T. Ivrlač and J. A. Nossek, "Toward a circuit theory of communication," *IEEE Transactions on Circuits and Systems I: Regular Papers*, vol. 57, no. 7, pp. 1663–1683, 2010.

[10] I. J. Gupta and A. A. Ksienski, "Effect of mutual coupling on the performance of adaptive arrays," *IEEE Transactions on Antennas and Propagation*, vol. 31, no. 5, pp. 785–791, 1983.

[11] H. Steyskal and J. S. Herd, "Mutual coupling compensation in small array antennas," *IEEE Transactions on Antennas and Propagation*, vol. 38, no. 12, pp. 1971–1975, 1990.

[12] K. Dovelos, S. D. Assimonis, H. Q. Ngo, and M. Matthaiou, "Superdirective arrays with finite-length dipoles: Modeling and new perspectives," in *Proc. IEEE GLOBECOM*, 2022. [arXiv:2208.01422](https://arxiv.org/abs/2208.01422).

[13] R. L. Fante and J. J. Vaccaro, "Wideband cancellation of interference in a GPS receive array," *IEEE Transactions on Aerospace and Electronic Systems*, vol. 36, no. 2, pp. 549–564, 2000.
