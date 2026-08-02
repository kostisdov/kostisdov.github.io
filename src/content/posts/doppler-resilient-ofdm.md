---
title: "OFDM vs OTFS: A pragmatic comparison"
description: "Fast fading breaks the orthogonality of OFDM subcarriers and creates inter-carrier interference, for which delay-Doppler waveforms such as OTFS are proposed as the remedy. However, a fair comparison shows that a properly designed OFDM performs on par with OTFS at much lower complexity."
date: 2026-07-27
tags: ["signals", "wireless"]
draft: false
---

A radio link on a fast-moving platform, a low-Earth-orbit satellite or a high-speed train, sees a
channel that changes not only across frequency but potentially within an OFDM symbol. Orthogonal
frequency-division multiplexing (OFDM) rests on the opposite assumption, that the channel is constant
over a symbol so that its subcarriers remain orthogonal. Once the platform moves quickly enough that
assumption fails: each subcarrier drifts during the symbol and leaks energy into adjacent
subcarriers. The result is inter-carrier interference (ICI), and beyond a certain mobility it forms
an error floor that no amount of transmit power can remove.

This impairment has renewed interest in delay-Doppler waveforms, most prominently orthogonal time
frequency space (OTFS) modulation, whose joint detector handles the coupling directly. The common
conclusion is that OTFS outperforms OFDM in high mobility. This post argues that the comparison
behind that conclusion is usually unfair, and that a well-designed OFDM receiver recovers most of the
gap. The advantage that survives belongs to the equalizer, not to the modulation.

## Why fast fading breaks OFDM

OFDM divides a wideband channel into $M$ narrow subcarriers, each of which sees a flat gain as long
as the channel is constant over the symbol. Its receiver is then a single complex division per
subcarrier. Mobility removes that premise. A path with Doppler shift $\nu$ rotates by $2\pi\nu T$
over a symbol of duration $T$, and different paths rotate by different amounts, so the composite
channel is no longer constant across the symbol. The natural measure of severity is the normalized
Doppler,

$$
\varepsilon = \frac{f_D}{\Delta f},
$$

the ratio of the maximum Doppler shift $f_D$ to the subcarrier spacing $\Delta f$. When
$\varepsilon$ is a small fraction the subcarriers remain nearly orthogonal; as it approaches and
exceeds unity they do not.

The effect is clearest in the frequency domain. One OFDM symbol and its time-varying channel form an
$M \times M$ matrix $H$, whose entry $H_{ij}$ is the gain from transmitted subcarrier $j$ to received
subcarrier $i$. For a static channel $H$ is diagonal. For a time-varying one it acquires off-diagonal
terms, an ICI band whose width grows with $\varepsilon$. Figure 1 shows the same channel at low and
high mobility. A single-tap equalizer retains only the diagonal and discards the band, and the
discarded energy becomes an irreducible error floor.

<figure>
<img src="/posts/doppler-resilient-ofdm/fig1_ici.svg" alt="Two heatmaps of the frequency-domain channel matrix magnitude: nearly diagonal at low Doppler, and a wide band around the diagonal at high Doppler." />
<figcaption>Fig. 1: Magnitude of the frequency-domain channel matrix H for one realization of a doubly dispersive channel. At low mobility (left, ε = 0.05) the matrix is nearly diagonal and a single tap per subcarrier suffices. At high mobility (right, ε = 1.2) a band of off-diagonal energy appears, the inter-carrier interference that a single-tap equalizer discards.</figcaption>
</figure>

## The delay-Doppler alternative

OTFS takes the opposite approach. Rather than placing symbols on subcarriers, it places them on a
delay-Doppler grid and spreads each across the entire time-frequency plane through the Zak transform.
In the delay-Doppler domain the doubly dispersive channel becomes a compact, almost time-invariant
coupling, a few taps in delay and Doppler that are common to the whole frame. A detector that inverts
this coupling jointly, typically a linear minimum mean-square-error (LMMSE) or message-passing
detector over the full frame, resolves the interference that defeats the single-tap OFDM receiver
[1], [2].

This capability is not free. The joint delay-Doppler detector is a large coupled inversion over the
whole frame, iterative rather than per-subcarrier, and it carries full-frame latency. OTFS does not
remove the difficulty of a doubly dispersive channel; it relocates that difficulty from the
modulation to the equalizer. Whether the trade is worthwhile is precisely the question a fair
comparison must answer.

## The flaw in the usual comparison

Most published comparisons are constructed against OFDM from the outset. On the OFDM side they place
plain OFDM with a single-tap equalizer, and they measure uncoded bit error rate; on the OTFS side
they place the full joint detector. Against that OFDM, OTFS shows a clear advantage, but that OFDM is
a straw man. No deployed system operates uncoded, and none would meet high mobility with a single-tap
equalizer while the ICI band is available to exploit.

A fair comparison must control three things. It must code the bits, because a real link harvests
diversity through a channel code and an interleaver rather than from raw symbol decisions. It must
match complexity, because a cheap OFDM equalizer set against an expensive OTFS detector is not one
experiment but two. And it must match pilots, because tracking a time-varying channel incurs an
overhead that both waveforms pay.

## A matched-complexity experiment

The three are settled at once by a single observation: both waveforms are unitary precodings of the
same time-domain signal. Write the transmitted block as $s = A x$, where $x$ carries the data symbols
and $A$ is a unitary precoder, so that the received samples are

$$
r = G_t A x + n,
$$

with $G_t$ the physical time-varying channel and $n$ the noise. OFDM and OTFS differ only in $A$: a
per-symbol inverse DFT for OFDM, and an inverse DFT along the Doppler axis for OTFS. The channel
$G_t$ is identical for both. In each waveform's own domain the channel is $H = A^{\mathsf H} G_t A$,
and the same equalizer operation applied to $H$ is, by construction, the same computation for both.

This reduces "OFDM versus OTFS" to a controlled experiment. Under the full inversion of $G_t$ the two
are identical, which already shows that the modulation alone changes nothing. Under a single tap both
floor. Under a banded equalizer at an equal tap budget, a frequency-domain band for OFDM and a
delay-Doppler band for OTFS, the comparison is at last even-handed.

The OFDM receiver appropriate to that experiment is a banded, multi-tap frequency-domain equalizer
that accounts for the ICI [3], [4]. Rather than retain only the diagonal of $H$, it retains a band of
half-width $Q$ about the diagonal and inverts that band. The band is sized to the mobility,

$$
Q = \left\lceil \frac{f_D}{\Delta f} \right\rceil + \Delta,
$$

read from the Doppler spread of the channel estimate, while the coefficients within the band follow
the fast fading, tracked from time-domain pilots. The band widens as the platform accelerates and
narrows as it slows, so equalizer complexity is spent only where the Doppler requires it.

## Where the diversity is won

Under this matched comparison the outcome is consistent, and it holds even in the extreme. At a
normalized Doppler of $\varepsilon = 1.2$, where the maximum Doppler shift exceeds the subcarrier
spacing outright, the ICI-aware OFDM receiver comes within about 1 dB of the full delay-Doppler OTFS
detector, at up to two orders of magnitude fewer equalizer taps. Standard single-tap OFDM, on the
same channel, never leaves its floor. Figure 2 shows the four receivers together.

<figure>
<img src="/posts/doppler-resilient-ofdm/fig2_ber.svg" alt="Coded BER against SNR at normalized Doppler 1.2: single-tap OFDM is a flat floor; ICI-aware OFDM, FDE-OTFS, and joint OTFS fall together within about 1 dB." />
<figcaption>Fig. 2: Coded bit error rate against signal-to-noise ratio on a doubly dispersive channel at ε = 1.2 (QPSK, rate-1/2 LDPC). Standard single-tap CP-OFDM never leaves its ICI floor. The proposed ICI-aware OFDM tracks the full delay-Doppler OTFS detector within about 1 dB. FDE-OTFS, the OTFS waveform equalized at OFDM complexity, coincides with the OFDM curve rather than with joint OTFS.</figcaption>
</figure>

A single control experiment locates the source of the OTFS advantage. Take the OTFS waveform, its
full delay-Doppler spreading intact, and equalize it with the cheap per-symbol band rather than the
joint detector. Its curve does not follow joint OTFS; it coincides with the OFDM curve. The spreading,
on its own, confers no gain. The advantage that OTFS displays comes from the joint equalizer that the
spreading makes convenient, not from the spreading itself.

What remains is a clean division of labour. A doubly dispersive channel carries a fixed amount of
diversity, and that diversity can be harvested in one of two places: in the equalizer, as OTFS does
with a complex joint detector, or in the code and interleaver, as coded OFDM does with a simple one.
The two reach the same diversity order. The question is therefore not which waveform is fundamentally
superior, but where to spend the complexity, and OFDM spends it in components a modern link already
contains, the code and the pilots.

## Why it matters

This is not merely an academic question. High-mobility OFDM is already in service: 5G non-terrestrial
networks (NTN) operate OFDM against the several-kilohertz Doppler of low-Earth-orbit satellites [5].
And in 2025 the 3GPP standardization effort settled the 6G waveform in OFDM's favour, adopting
cyclic-prefix OFDM in the downlink and adding discrete Fourier transform spread OFDM as an uplink
option. A departure from OFDM was available, and was not taken.

Against that background the result is reassuring rather than surprising. If a well-designed equalizer
closes most of the gap to OTFS, then the flexibility that makes OFDM the incumbent, its clean
multi-user MIMO, its orthogonal frequency-division multiple access, its scheduling granularity, and
its backward compatibility with deployed hardware, is worth retaining. The honest reading of the
delay-Doppler literature is not that OFDM must be replaced, but that it needs a better receiver in
high mobility, a far more modest requirement.

None of this is the final word. This comparison aims to provide a grounded baseline. The
delay-Doppler view remains an elegant way to reason about doubly dispersive channels. But for an
engineer deciding where to invest, the lever is the equalizer, not the waveform. The full derivation,
the matched-complexity framework, and reproducible code are in the
[preprint and repository](https://github.com/kostisdov/ofdm_vs_otfs) [6].

## References

[1] R. Hadani, S. Rakib, M. Tsatsanis, A. Monk, A. J. Goldsmith, A. F. Molisch, and R. Calderbank,
"Orthogonal time frequency space modulation," in *Proc. IEEE Wireless Communications and Networking
Conference (WCNC)*, 2017, pp. 1–6.

[2] P. Raviteja, K. T. Phan, Y. Hong, and E. Viterbo, "Interference cancellation and iterative
detection for orthogonal time frequency space modulation," *IEEE Trans. Wireless Commun.*, vol. 17,
no. 10, pp. 6501–6515, 2018.

[3] L. Rugini, P. Banelli, and G. Leus, "Simple equalization of time-varying channels for OFDM,"
*IEEE Commun. Lett.*, vol. 9, no. 7, pp. 619–621, 2005.

[4] Y. Mostofi and D. C. Cox, "ICI mitigation for pilot-aided OFDM mobile systems," *IEEE Trans.
Wireless Commun.*, vol. 4, no. 2, pp. 765–774, 2005.

[5] 3GPP TR 38.811, "Study on New Radio (NR) to support non-terrestrial networks," 3rd Generation
Partnership Project, 2020.

[6] K. Dovelos, "OFDM with adaptive ICI-aware equalization for doubly dispersive channels,"
preprint, 2026.
