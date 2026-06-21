---
title: "What statistical physics sees in the heartbeat"
description: "Detrended fluctuation analysis (DFA) was invented to find long-range correlations in DNA. Applied to cardiac rhythm, it measures the fractal scaling that standard HRV metrics are blind to, and that deteriorates before the linear statistics change."
date: 2026-06-12
tags: ["signals", "biomedical"]
draft: true
---

The [first post](https://kostisdov.github.io/posts/reading-the-heart-with-a-radio-toolbox/)
in this series analysed an ECG with a linear signal processing pipeline: a band-pass filter,
R-peak detection to form a tachogram of RR intervals, and Welch's method to estimate the
spectrum, yielding the low- and high-frequency bands and the LF/HF ratio.

That pipeline rests on an implicit assumption: that the information of interest resides in the
amplitude and the spectrum of the variability, specifically how much it varies (the standard
deviation of the intervals, SDNN), at what rates (the spectral bands), and in what balance
(LF/HF). This
post concerns what that assumption omits. A healthy heart is not a noisy metronome but a
fractal, self-organizing system, and the salient property of its rhythm is not the magnitude
of the wandering but the way the wandering is structured across time scales. Linear measures
are largely blind to that structure; nonlinear measures are not.

The distinction is clinically consequential. In failing hearts, in autonomic neuropathy, and
in the slow progression toward decompensation, the variability can appear unchanged to the
linear measures while its temporal architecture deteriorates. A summary restricted to SDNN and
LF/HF can therefore miss the change entirely.

## Fractal physiology and self-similarity

Two physiological ideas frame the problem.

The first is a refinement of homeostasis: a healthy organism is not held at a fixed set-point
but in a restless, fluctuating equilibrium. The fluctuations are not noise to
be removed; they constitute the regulation. An excessively steady heart rate is a warning sign
rather than a sign of health.

The second is fractal physiology [1]: these fluctuations are self-similar across time scales.
A healthy RR series examined at the scale of seconds, of minutes, and of tens of minutes
exhibits statistically similar structure at each, the signature of a control system with no
single characteristic time, operating across many coupled loops simultaneously. This self-similarity
appears as a 1/f (pink-noise) spectrum and a power-law scaling of fluctuations. Pathology
tends to move the heart away from 1/f, either toward rigid, random-walk dynamics (loss of
responsiveness) or toward uncorrelated noise (loss of integration).

The amplitude statistics of Part I cannot resolve this. The most direct demonstration is to
destroy the structure deliberately.

## What linear measures miss

Consider a healthy, 1/f-like RR series, and a second series formed by shuffling it: the same
values in random order. Shuffling preserves every amplitude statistic that does not depend on
order. The mean is unchanged, and so is SDNN, the most frequently reported heart-rate variability (HRV) measure [2];
the histogram is identical. By those measures the two recordings are indistinguishable.
Dynamically they are not.

<figure>
<img src="/posts/the-fractal-heart-nonlinear-hrv/fig1_blindspot.svg?v=2" alt="Healthy 1/f rhythm versus the same values shuffled, and their DFA curves." />
<figcaption>Fig. 1: A healthy 1/f rhythm (top) and the same values shuffled (middle). The mean and SDNN are identical (850 ms, 45 ms), yet the DFA fluctuation curves (bottom; α₁ is the DFA scaling exponent, defined in the DFA section below) give α₁ = 1.03 for the healthy series and 0.55 for the shuffled one.</figcaption>
</figure>

The upper trace shows slow undulations and drift that persist across hundreds of beats; the
middle trace, the same values reordered, is uncorrelated and structureless. The mean and SDNN
are identical (850 ms and 45 ms). Yet one is a correlated fractal process and the other is white noise. The lower panel shows
the DFA scaling exponent (defined in full below): it falls from $\alpha_1 = 1.03$ for the
healthy series to $0.55$ for the shuffled one.

This is the central motivation. The magnitude of the variability is conserved; its
organization is destroyed; the standard measures do not respond. A measure of the
organization is required.

One caveat sharpens the claim. The power spectrum is not itself blind to order: by the
Wiener–Khinchin theorem it is the Fourier transform of the autocorrelation, so the shuffle
that whitens the autocorrelation also flattens the spectrum. Two things, however, escape the
linear pipeline of Part I. SDNN is order-independent and registers nothing; and the reported
LF/HF summary compresses the spectrum into a few fixed bands, discarding the broadband 1/f
slope in which the scaling actually lives. The nonlinear measures that follow recover that
scaling directly and, beyond it, capture higher-order dependence that no power spectrum, a
purely second-order quantity, can express.

## Poincaré plots: beat-to-beat geometry

The simplest nonlinear view is geometric. Each interval is plotted against the next, $RR_n$ on
the horizontal axis and $RR_{n+1}$ on the vertical axis. A perfectly regular rhythm collapses to a single point; a healthy rhythm forms an elongated
cloud. The cloud's shape is captured by fitting an ellipse [3]. SD1 measures the width
perpendicular to the line of identity, picking out the beat-to-beat differences; it is
dominated by vagal (parasympathetic) activity. SD2 measures the length along the line of
identity, capturing longer-range trends. Formally:

$$
\mathrm{SD1} = \sqrt{\tfrac{1}{2}\,\mathrm{Var}(RR_{n+1}-RR_n)}, \qquad
\mathrm{SD2} = \sqrt{2\,\mathrm{Var}(RR) - \tfrac{1}{2}\,\mathrm{Var}(\Delta RR)}.
$$

Their ratio SD1/SD2 is a compact descriptor of the balance between short- and long-term
regulation.

<figure>
<img src="/posts/the-fractal-heart-nonlinear-hrv/fig2_poincare.svg?v=2" alt="Poincaré plot of the healthy rhythm with the SD1/SD2 ellipse." />
<figcaption>Fig. 2: Poincaré plot of the healthy rhythm, with the fitted SD1/SD2 ellipse (SD1 = 21 ms, SD2 = 60 ms).</figcaption>
</figure>

The Poincaré description is intuitive and clinically common, but it remains essentially
second-order: SD1 and SD2 are functions of variances. The method detects the presence of
structure without quantifying it across scales. Before arriving at a measure that does, it is worth
posing a simpler question: how predictable is the next beat from the ones before it? The
answer illuminates exactly what a scale-resolved measure must add.

## Sample entropy: the predictability of the next beat

Sample entropy (SampEn) [4] poses an information-theoretic question: given two short segments
of the rhythm that match for $m$ beats, how often do they continue to match for $m+1$ beats?
Frequent continuation indicates a regular, predictable signal; infrequent continuation
indicates a complex, irregular one. With tolerance $r$ (commonly $0.2$ times the standard
deviation) and embedding length $m$ (commonly $2$),

$$
\mathrm{SampEn}(m,r) = -\ln \frac{A}{B},
$$

where $B$ is the number of template pairs (length-$m$ windows that agree beat-by-beat within
tolerance $r$) and $A$ the subset that still agree when extended to length $m+1$. Higher
SampEn corresponds to lower predictability.

A caution is warranted, because the point is easily misread: irregularity is not health. A
Brownian (random-walk) rhythm is smooth and highly predictable, giving low SampEn, and is
pathological. White noise is maximally unpredictable, giving high SampEn, and is also
pathological. Health lies between the two, at the 1/f regime. SampEn is therefore informative
but non-monotonic; greater entropy is not uniformly better. This non-monotonicity motivates a
measure that locates the rhythm on the continuum between rigid and random, which is what
DFA provides.

## Detrended fluctuation analysis

DFA [5] estimates the spectral exponent of the rhythm. A fractal time series has a power
spectral density that obeys $S(f) \propto f^{-\beta}$, where $\beta$ is the spectral exponent:
$\beta \approx 0$ for white noise (flat spectrum), $\beta \approx 1$ for a healthy 1/f rhythm,
$\beta \approx 2$ for Brownian motion. In principle one could estimate $\beta$ directly from
the periodogram. In practice, physiological recordings are short and non-stationary, and the
spectral estimate is correspondingly unreliable. DFA estimates the equivalent exponent $\alpha$
(related to $\beta$ by $\alpha = (\beta + 1)/2$) from the time domain, robustly even when the
signal drifts. The method was not developed in a cardiology laboratory: introduced in the early
1990s by Peng, Havlin, Stanley, and Goldberger at Boston University to detect long-range
correlations in non-stationary DNA nucleotide sequences [6], it reached cardiac rhythm by the
same mathematical route. The procedure has three steps.

First, integrate. The RR series is converted into a profile, the cumulative sum of the
mean-removed intervals:

$$
y(k) = \sum_{i=1}^{k} \big(RR_i - \overline{RR}\big).
$$

Second, detrend in windows. The profile $y(k)$ is divided into boxes of size $n$; within each
box a local polynomial trend (linear here) is fitted and subtracted, which is what makes DFA
robust to nonstationarity. The root-mean-square of the residuals is

$$
F(n) = \sqrt{\frac{1}{N}\sum_{k=1}^{N}\big(y(k) - y_{\mathrm{fit},n}(k)\big)^2}.
$$

Third, scale. The computation is repeated across box sizes, and $F(n)$ is examined against $n$
on logarithmic axes. For a self-similar process the relationship is a straight line,
$F(n) \sim n^{\alpha}$, whose slope $\alpha$ is the scaling exponent. The short-term exponent
over $4 \le n \le 16$ beats is denoted $\alpha_1$.

| $\alpha_1$ | dynamics | interpretation |
|------------|----------|----------------|
| $\approx 0.5$ | uncorrelated (white) | each beat independent of the previous one; loss of integration |
| $\approx 1.0$ | 1/f (pink) | scale-free, fractal; the healthy regime |
| $\approx 1.5$ | Brownian (random walk) | over-smooth, sluggish; loss of complexity |

<figure>
<img src="/posts/the-fractal-heart-nonlinear-hrv/fig3_dfa.svg?v=2" alt="Three synthetic rhythms and their DFA fluctuation curves." />
<figcaption>Fig. 3: Three synthetic rhythms (left) and their DFA fluctuation curves (right). The slope on log-log axes is the scaling exponent, recovering α₁ ≈ 0.59 (white), 1.03 (1/f), and 1.54 (Brownian).</figcaption>
</figure>

On the synthetic series DFA recovers the planted exponents, $0.59$, $1.03$, and $1.54$,
confirming the estimator before it is applied to real data. It also accounts for the shuffling
result: shuffling whitens the spectrum and drives $\alpha_1$ from approximately $1.0$ toward
$0.5$, while leaving the mean and SDNN unchanged.

The clinical relevance is that a reduced or drifting $\alpha_1$ has been associated with
autonomic dysfunction and with adverse outcomes in heart failure [7]: the failing heart tends
to lose its 1/f signature, moving toward either over-regular ($\alpha_1 \to 1.5$) or
disorganized ($\alpha_1 \to 0.5$) dynamics before the linear summaries change. This is the kind
of early structural drift that a longitudinal monitor would aim to detect.

## Sensitivity to artifacts

The preceding methods all assume a clean RR series. In practice that assumption frequently
fails. DFA, SampEn, and the Poincaré indices all read the fine temporal structure of the
intervals, which makes them acutely sensitive to the two artifacts that dominate real-world
heart-rate data: ectopic beats (a premature beat followed by a compensatory pause, which
injects a large artificial step) and dropped beats (a missed detection that merges two
intervals into one). The effect of even a small rate of each on $\alpha_1$ is severe.

<figure>
<img src="/posts/the-fractal-heart-nonlinear-hrv/fig4_reckoning.svg?v=2" alt="Effect of ectopic and dropped beats on the DFA exponent." />
<figcaption>Fig. 4: A 1.5% ectopic rate against the clean rhythm (left) and the resulting DFA curves (right): α₁ collapses from the clean value of 1.03 to 0.35 with ectopics and to 0.64 with a 6% drop rate.</figcaption>
</figure>

The clean rhythm has $\alpha_1 = 1.03$. Ectopic beats at $1.5\%$ of the total reduce it to
$0.35$; a $6\%$ drop rate reduces it to $0.64$. A measurement that should indicate healthy
fractal organization instead indicates disorganization, not because the underlying dynamics
changed but because a small number of intervals are incorrect. The signal is intact; the
acquisition corrupts the estimate.

This has a direct implication for consumer wearables. The beat-to-beat timing these methods
require is reliably obtained from a chest-strap ECG under controlled conditions. The
wrist-worn optical sensor (photoplethysmography, PPG) in a consumer watch, the sensor that
most patients possess, is precisely the source that produces ectopic-like spikes and
dropped beats under motion, poor perfusion, or low peripheral temperature. The most prognostic
HRV measures are thus the most fragile, and they depend on the least reliable hardware
available to the patient. This is the constraint that frames the engineering problem
downstream.

## Summary

The heart is not a metronome, the variability is the regulation, and its fractal organization,
quantified by $\alpha_1$, carries information that the linear summaries cannot retrieve. The
remaining difficulty is measurement: obtaining the artifact-free interval sequences that the
nonlinear measures require.

## References

[1] A. L. Goldberger, L. A. N. Amaral, J. M. Hausdorff, P. Ch. Ivanov, C.-K. Peng, and H. E.
Stanley, "Fractal dynamics in physiology: alterations with disease and aging," *Proceedings of
the National Academy of Sciences*, vol. 99, suppl. 1, pp. 2466–2472, 2002.

[2] Task Force of the European Society of Cardiology and the North American Society of Pacing
and Electrophysiology, "Heart rate variability: standards of measurement, physiological
interpretation, and clinical use," *Circulation*, vol. 93, no. 5, pp. 1043–1065, 1996.

[3] M. Brennan, M. Palaniswami, and P. Kamen, "Do existing measures of Poincaré plot geometry
reflect nonlinear features of heart rate variability?," *IEEE Transactions on Biomedical
Engineering*, vol. 48, no. 11, pp. 1342–1347, 2001.

[4] J. S. Richman and J. R. Moorman, "Physiological time-series analysis using approximate
entropy and sample entropy," *American Journal of Physiology-Heart and Circulatory
Physiology*, vol. 278, no. 6, pp. H2039–H2049, 2000.

[5] C.-K. Peng, S. Havlin, H. E. Stanley, and A. L. Goldberger, "Quantification of scaling
exponents and crossover phenomena in nonstationary heartbeat time series," *Chaos*, vol. 5,
no. 1, pp. 82–87, 1995.

[6] C.-K. Peng, S. V. Buldyrev, A. L. Goldberger, S. Havlin, F. Sciortino, M. Simons, and
H. E. Stanley, "Long-range correlations in nucleotide sequences," *Nature*, vol. 356,
pp. 168–170, 1992.

[7] H. V. Huikuri et al., "Fractal correlation properties of R-R interval dynamics and
mortality in patients with depressed left ventricular function after an acute myocardial
infarction," *Circulation*, vol. 101, no. 1, pp. 47–53, 2000.
