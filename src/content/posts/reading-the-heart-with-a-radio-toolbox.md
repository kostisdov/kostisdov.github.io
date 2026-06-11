---
title: "Reading the heart with a radio engineer's toolbox"
description: "An electrocardiogram is a noisy one-dimensional signal. The same signal processing used in radio receivers, filtering and spectral estimation, turns it into a measure of autonomic health."
date: 2026-06-10
tags: ["signals", "biomedical"]
---

Signal recovery in wireless communications and signal analysis in cardiology pose the same
underlying problem: a weak waveform of interest is buried in interference, and the task is to
recover meaningful information from it. The mathematical toolbox is largely shared. An
electrocardiogram (ECG) is a one-dimensional signal $x(t)$ sampled at a rate $f_s$,
structurally identical to the baseband stream of a radio receiver, so the standard processing
techniques transfer with little modification. The pipeline described below underlies two
health tools in development, [Pyxida](https://pyxida.io) and FindMyHeart.

## Filtering: isolating the heartbeat

A raw ECG recording contains several noise sources: power-line interference at 50 Hz,
low-frequency baseline wander caused by respiration and electrode motion, and wideband
measurement noise. The diagnostically relevant component is the QRS complex, the
large, sharp deflection of each beat. Its name denotes three successive deflections, a small
negative Q wave, a tall positive R wave, and a subsequent negative S wave, and it corresponds
to depolarization and contraction of the ventricles, the heart's main pumping chambers. The
QRS complex occupies a band of approximately 0.5 to 40 Hz; energy outside this band belongs
to other sources.

Removing that out-of-band energy requires a band-pass filter: a high-pass stage suppresses
the baseline wander, and a low-pass stage attenuates the mains interference and high-frequency
noise.

![A raw ECG-like recording dominated by mains interference and baseline wander, and the same trace after a 0.5 to 40 Hz band-pass filter, showing clean QRS peaks.](/posts/heart/ecg-filtering.svg)

The effect is substantial. The unfiltered trace is uninterpretable, whereas the filtered
trace exhibits clearly delineated QRS peaks. This step is not specific to electrocardiography;
it is the same filtering applied to any noisy communication channel.

## From waveform to rhythm: the RR-interval series

For many cardiological purposes the morphology of each beat is less informative than the
intervals between beats. Detecting the R wave of each QRS complex (the Pan–Tompkins
algorithm [1] is the classic method) and measuring the time between successive R waves yields
the sequence of RR intervals,

$$
\text{RR}_n = t_{n} - t_{n-1},
$$

where $t_n$ denotes the time of the $n$-th R wave. An RR interval of 850 ms corresponds to
0.85 s between beats, or a heart rate of approximately 70 beats per minute. Plotting the RR
intervals against time produces the tachogram, a signal sampled once per beat that discards
the voltage waveform and retains only the timing.

![A tachogram: RR interval in milliseconds plotted over several minutes, oscillating around 850 ms.](/posts/heart/tachogram.svg)

The healthy heart is not periodic. The RR interval varies by tens of milliseconds from beat
to beat. This variation is not measurement noise; it reflects continuous modulation of the
cardiac pacemaker by the autonomic nervous system and is quantified as heart-rate variability
(HRV).

## Spectral analysis of heart-rate variability

The RR-interval fluctuations are not random but consist of superimposed oscillations, which
the Fourier transform resolves into their constituent frequencies. The relevant quantity is
the power spectral density (PSD), which describes how the variance of the signal is
distributed over frequency.

Let $x[n]$ denote the tachogram after resampling onto a uniform grid (discussed below) and
removal of its mean and slow trend, so that the spectrum reflects the fluctuations rather than
a component at zero frequency. For a wide-sense stationary process the PSD is defined, through
the Wiener–Khinchin theorem, as the discrete-time Fourier transform (DTFT) of the
autocorrelation sequence [2]:

$$
S\!\left(e^{j\omega}\right) = \sum_{m=-\infty}^{\infty} r[m]\, e^{-j\omega m},
\qquad r[m] = \mathbb{E}\big\{\,x[n]\,x[n-m]\,\big\}.
$$

The PSD is a continuous function of the normalized angular frequency $\omega \in [-\pi, \pi]$,
in radians per sample, because the underlying process is of indefinite length; no block size
$N$ appears in the definition. The normalized frequency maps to physical frequency through
$f = \omega f_s / 2\pi$. At $f_s = 4$ Hz the representable band extends to the Nyquist
frequency of 2 Hz, well above the 0.4 Hz upper limit of the bands of interest.

The true autocorrelation is unavailable; only a finite record of $N$ samples is observed, so
the PSD must be estimated. The naive estimate, a single squared DFT of the whole record (the
periodogram), is inconsistent: its variance does not decrease as the record grows, so genuine
peaks stay buried in large random fluctuations. Welch's method [3] removes this defect by
averaging windowed periodograms over shorter, overlapping segments.

The record is split into $K$ segments of length $L$; each segment $x_i[n]$ is multiplied by a
window $w[n]$ (a Hann window here) to limit spectral leakage, and its modified periodogram is

$$
\hat{S}_i[k] = \frac{1}{\sum_{n=0}^{L-1} w[n]^2}\left|\,\sum_{n=0}^{L-1} w[n]\,x_i[n]\,e^{-j 2\pi k n / L}\,\right|^2 ,
$$

an $L$-point DFT whose bin $k$ maps to the physical frequency $f_k = k f_s / L$. Welch's
estimate is the average over the $K$ segments, $\hat{S}^{\mathrm{W}}[k] = \frac{1}{K}\sum_{i=1}^{K}\hat{S}_i[k]$.
Normalizing by the window energy $\sum_n w[n]^2$ keeps each segment estimate unbiased: for a
rectangular window $\sum_n w[n]^2 = L$, i.e., one over the segment length, whereas for the
Hann window $\sum_n w[n]^2 = \tfrac{3}{8}L$, i.e., $8/(3L)$.

The segments overlap, typically by 50%: because the window
attenuates each segment toward its edges, overlapping lets those edge samples still
contribute, giving about $K \approx 2N/L$ segments from a record of length $N$, against $N/L$
for non-overlapping blocks. Averaging lowers the variance roughly in proportion to the number
of segments, though by somewhat less than a factor of $K$, since overlapping segments are not
fully independent. The cost is coarser frequency resolution, set by the segment length $L$,
which is acceptable here because only the distribution of power between bands is required.

Resampling onto a uniform grid is necessary because the tachogram is sampled irregularly, once
per beat, whereas the DFT assumes uniform sampling.

![Power spectral density of the RR-interval series, with a low-frequency peak near 0.1 Hz and a high-frequency peak near 0.25 Hz, the LF and HF bands shaded.](/posts/heart/hrv-psd.svg?v=2)

The spectrum exhibits two distinct bands, whose boundaries follow the standard HRV
conventions [4]. The high-frequency band (HF, 0.15 to 0.4 Hz)
coincides with the respiratory rhythm: heart rate increases during inspiration and decreases
during expiration, an effect termed respiratory sinus arrhythmia and mediated by the vagus
nerve, the parasympathetic branch of the autonomic nervous system. Greater HF power indicates
higher vagal tone.

The low-frequency band (LF, 0.04 to 0.15 Hz) is centred near 0.1 Hz, the characteristic
frequency of the baroreflex, the blood-pressure regulation loop, and reflects a combination of
sympathetic and parasympathetic activity.

The two bands are frequently summarized by their ratio,

$$
\frac{\text{LF}}{\text{HF}} = \frac{\displaystyle\int_{0.04}^{0.15} S(f)\,df}{\displaystyle\int_{0.15}^{0.40} S(f)\,df},
$$

interpreted as an index of sympathovagal balance, with resting values typically between 1 and
2, increasing under stress. This interpretation should be treated with caution, as the
identification of LF power with sympathetic activity is an oversimplification. A more robust
indicator is the total power of the spectrum, that is, overall HRV, which is an established
marker of autonomic function [5]. Reduced variability is associated with stress, fatigue,
overtraining, and, over the long term, adverse cardiovascular outcomes, whereas increased
variability is associated with recovery and fitness.

## The shared toolbox

The procedure can be summarized as follows: a weak signal is band-pass filtered to reject
interference, a derived sequence is extracted, and its power spectrum is estimated to reveal
latent structure. This is, with minor changes in terminology, the same procedure a radio
receiver applies when estimating channel statistics. The filtering, the spectral estimators,
and the principle of identifying the band that carries the information are common to both
domains.

Signal processing is indifferent to the physical origin of the signal: a waveform from an
antenna and a waveform from an artery are, mathematically, the same kind of object. That
equivalence is the quiet beauty of the discipline: the mathematics does not change, only the
signal does.

## References

[1] J. Pan and W. J. Tompkins, "A real-time QRS detection algorithm," *IEEE Transactions on
Biomedical Engineering*, vol. 32, no. 3, pp. 230–236, 1985.

[2] A. V. Oppenheim and R. W. Schafer, *Discrete-Time Signal Processing*, 3rd ed. Pearson,
2009.

[3] P. D. Welch, "The use of fast Fourier transform for the estimation of power spectra: a
method based on time averaging over short, modified periodograms," *IEEE Transactions on
Audio and Electroacoustics*, vol. 15, no. 2, pp. 70–73, 1967.

[4] Task Force of the European Society of Cardiology and the North American Society of Pacing
and Electrophysiology, "Heart rate variability: standards of measurement, physiological
interpretation, and clinical use," *Circulation*, vol. 93, no. 5, pp. 1043–1065, 1996.

[5] F. Shaffer and J. P. Ginsberg, "An overview of heart rate variability metrics and norms,"
*Frontiers in Public Health*, vol. 5, art. 258, 2017.
