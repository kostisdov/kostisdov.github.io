---
title: "Reading the heart with a radio engineer's toolbox"
description: "An ECG is just a noisy one-dimensional signal. The same DSP that pulls a voice out of static pulls a story about your nervous system out of your heartbeats."
date: 2026-06-10
tags: ["signals", "biomedical"]
---

Spend a decade pulling faint signals out of noisy radio channels and you start to see
the same problem everywhere. A radio receiver gets a weak waveform smothered in
interference and has to recover what was sent. A cardiologist gets a weak waveform
smothered in interference and has to recover what the heart is doing. Same problem.
Mostly the same math.

So when I started building [Pyxida](https://pyxida.io) and FindMyHeart, I was surprised
how little I had to relearn. An electrocardiogram is a one-dimensional signal $x(t)$
sampled at some rate $f_s$, exactly like the baseband stream coming off a radio. The
toolbox transfers almost intact.

## Step one: clean the channel

A raw recording is a mess. Mains interference hums at 50 Hz (60 Hz across the Atlantic),
the electrode baseline drifts as the patient breathes and moves, and broadband noise sits
on top of everything. The heartbeat we actually want is the **QRS complex**, the
tall, spiky part of each beat. The name is just the labels for its three consecutive
deflections (a small dip Q, a tall peak R, another dip S), and physiologically it marks the
moment the heart's main pumping chambers, the ventricles, depolarize and contract to push
blood out to the body. That sharp spike lives in a band of roughly 0.5 to 40 Hz. Everything
outside that band is someone else's signal.

The fix is the first thing any radio engineer reaches for: a band-pass filter. Knock out
the slow baseline wander with a high-pass, knock out the mains hum and high-frequency
fuzz with a low-pass, and the heartbeat snaps into focus.

![A raw ECG-like recording buried in mains hum and baseline wander, and the same trace after a 0.5 to 40 Hz band-pass filter, showing clean QRS peaks.](/posts/heart/ecg-filtering.svg)

That is the entire denoising step. The top trace is unreadable; the bottom one has six
clean spikes you could count from across the room. Nothing here is specific to medicine;
it is the same filtering that cleans a noisy audio channel.

## Step two: throw away the waveform, keep the rhythm

Here is where it gets interesting. For a lot of cardiology, the shape of each beat
matters less than the timing between beats. Mark the tall R peak of each QRS complex,
measure the time from one R peak to the next, and you get the sequence of **RR intervals**,
the beat-to-beat durations, named after the R waves at each end:

$$
\text{RR}_n = t_{n} - t_{n-1},
$$

where $t_n$ is the time of the $n$-th R peak. So an RR interval of 850 ms simply means
0.85 seconds elapsed between two heartbeats, a heart rate of about 70 beats per minute.
Plot those gaps against time and you get a tachogram: a brand-new signal, sampled
irregularly once per beat, that throws away the voltage waveform entirely and keeps only
the rhythm.

![A tachogram: RR interval in milliseconds plotted over several minutes, oscillating around 850 ms.](/posts/heart/tachogram.svg)

A healthy heart is not a metronome. Look at the wobble: the interval breathes up and down
by tens of milliseconds. That variability is not noise. It is the autonomic nervous system
leaning on the pacemaker in real time, and it turns out to carry a remarkable amount of
information about stress, recovery, and health. This is **heart-rate variability**, or HRV.

## Step three: a Fourier window into the nervous system

The wobble looks random in time. It is not: it is a sum of oscillations layered on top of
one another, and the tool for pulling oscillations out of a signal is, of course, the
Fourier transform. It re-expresses the wiggling tachogram as a recipe of sinusoids and
tells you how much power sits at each frequency. The quantity we want is the **power
spectral density** (PSD): a description of how the variance of the signal, how much it
wobbles, is distributed across frequency.

We are working with a discrete-time signal $x[n]$, the tachogram resampled onto an even
grid (more on that below). The cleanest definition of its PSD comes from the
Wiener–Khinchin theorem: the PSD is the discrete-time Fourier transform of the
autocorrelation sequence,

$$
S\!\left(e^{j\omega}\right) = \sum_{m=-\infty}^{\infty} r[m]\, e^{-j\omega m},
\qquad r[m] = \mathbb{E}\big\{\,x[n]\,x[n-m]\,\big\},
$$

where $r[m]$ measures how much a sample resembles the one $m$ steps away, and $\omega$ is
the normalized angular frequency in radians per sample. We first remove the slow trend and
mean, so the spectrum reflects the fluctuations rather than a spike at zero frequency. Since
we resampled at $f_s = 4$ Hz, a normalized $\omega$ corresponds to a physical frequency
$f = \omega f_s / 2\pi$ in hertz. That rate is deliberately generous: by Nyquist it captures
frequencies up to 2 Hz, comfortably above the 0.4 Hz ceiling of the bands we care about.

In practice we never have the true autocorrelation; we have a finite record. The obvious
estimate is the **periodogram**: take the discrete Fourier transform of the $N$ samples and
square it,

$$
\hat{S}\!\left(e^{j\omega}\right) = \frac{1}{N}\left|\,\sum_{n=0}^{N-1} x[n]\, e^{-j\omega n}\,\right|^2 .
$$

The $|\cdot|^2$ turns amplitude into power. It is technically correct but uselessly noisy:
its variance does not shrink as you collect more data, so the spectrum comes out looking
like grass, real peaks buried in spikes. **Welch's method** is the standard fix. Chop the
record into overlapping segments, taper each one with a window (a Hann window here) to stop
energy leaking between frequencies, compute the periodogram of each segment, and average them. Averaging
$K$ roughly-independent estimates cuts the variance by about a factor of $K$, trading a
little frequency resolution for a far smoother, more trustworthy spectrum. Here that trade
is exactly right: we do not need pinpoint resolution, we just need to see reliably which
band the power lives in. (And the resampling onto an even grid matters because the raw
tachogram arrives one irregular sample per beat, while the DFT assumes uniform spacing.)

![Power spectral density of the RR-interval series, with a low-frequency peak near 0.1 Hz and a high-frequency peak near 0.25 Hz, the LF and HF bands shaded.](/posts/heart/hrv-psd.svg)

Two peaks, two stories. The high-frequency band (HF, 0.15–0.4 Hz) sits right at the
rhythm of normal breathing. Your heart speeds up slightly as you inhale and slows as you
exhale, an effect called respiratory sinus arrhythmia, and it is driven by the vagus
nerve, the parasympathetic "rest and digest" branch of the nervous system. A tall HF peak
means strong vagal tone: the signature of a calm, well-recovered heart.

The low-frequency band (LF, 0.04–0.15 Hz) is messier. It centres near 0.1 Hz, the
natural period of the baroreflex, the feedback loop that keeps your blood pressure steady,
and it carries a blend of both sympathetic ("fight or flight") and parasympathetic activity.

People often compress the two into a single number, their ratio,

$$
\frac{\text{LF}}{\text{HF}} = \frac{\displaystyle\int_{0.04}^{0.15} S(f)\,df}{\displaystyle\int_{0.15}^{0.40} S(f)\,df},
$$

read as a dial for "sympathovagal balance"; at rest it typically sits somewhere around 1 to
2, climbing as stress shifts the balance. It is a handy shorthand, though the tidy
"LF equals sympathetic" story is an oversimplification and worth treating with some caution. The
far more robust signal is the bigger picture: the total power under this curve, overall
heart-rate variability, is a well-established marker of autonomic health. Depressed
variability tracks with stress, fatigue, overtraining, and, over the long run, worse
cardiovascular outcomes; rising variability tracks with recovery and fitness. A heart under
chronic stress and one deep in recovery look genuinely different here: not in the waveform,
not even in the average heart rate, but in how the power splits across a spectrum.

## The same machinery, pointed somewhere new

Step back and look at what we did. We took a weak signal, band-pass filtered it to reject
interference, extracted a derived sequence, and read its power spectrum to recover hidden
structure. Swap a few nouns and that is a description of a radio receiver estimating channel
statistics. The filters, the spectral estimators, the habit of asking which band carries
the information: all of it transfers.

That is the quiet thrill of signal processing: it does not actually care what the signal
is. A waveform from an antenna and a waveform from an artery are, to the math, the same
kind of object. Learn the toolbox once and the heart becomes just another channel worth
decoding, which is more or less the bet behind everything I am building in health right now.

Next time: detecting arrhythmias the way a radio detects a dropped packet, where a missed or
malformed beat is just an error in a stream you were expecting to be regular.

## References

1. Task Force of the European Society of Cardiology and the North American Society of Pacing
   and Electrophysiology, "Heart rate variability: standards of measurement, physiological
   interpretation, and clinical use," *Circulation*, vol. 93, no. 5, pp. 1043–1065, 1996.
2. F. Shaffer and J. P. Ginsberg, "An overview of heart rate variability metrics and norms,"
   *Frontiers in Public Health*, vol. 5, art. 258, 2017.
3. P. D. Welch, "The use of fast Fourier transform for the estimation of power spectra: a
   method based on time averaging over short, modified periodograms," *IEEE Transactions on
   Audio and Electroacoustics*, vol. 15, no. 2, pp. 70–73, 1967.
4. J. Pan and W. J. Tompkins, "A real-time QRS detection algorithm," *IEEE Transactions on
   Biomedical Engineering*, vol. 32, no. 3, pp. 230–236, 1985.
5. A. V. Oppenheim and R. W. Schafer, *Discrete-Time Signal Processing*, 3rd ed. Pearson,
   2009.
