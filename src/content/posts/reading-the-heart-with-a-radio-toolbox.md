---
title: "Reading the heart with a radio engineer's toolbox"
description: "An ECG is just a noisy one-dimensional signal. The same DSP that pulls a voice out of static pulls a story about your nervous system out of a heartbeat."
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

A raw recording is a mess. Ride-along noise from the mains hums at 50 Hz, the electrode
baseline drifts as the patient breathes and moves, and broadband noise sits on top of
everything. The heartbeat we actually want — the sharp **QRS complex** — lives in a band
of roughly 0.5 to 40 Hz. Everything outside that band is someone else's signal.

The fix is the first thing any radio engineer reaches for: a band-pass filter. Knock out
the slow baseline wander with a high-pass, knock out the mains hum and high-frequency
fuzz with a low-pass, and the heartbeat snaps into focus.

![A raw ECG-like recording buried in mains hum and baseline wander, and the same trace after a 0.5–40 Hz band-pass filter, showing clean QRS peaks.](/posts/heart/ecg-filtering.svg)

That is the entire denoising step. The top trace is unreadable; the bottom one has six
clean spikes you could count from across the room. Nothing here is specific to
medicine — it is the same filtering that cleans a noisy audio channel.

## Step two: throw away the waveform, keep the rhythm

Here is where it gets interesting. For a lot of cardiology, the *shape* of each beat
matters less than the *timing between* beats. Mark the peak of each QRS complex, take the
gaps, and you get the sequence of **RR intervals**:

$$
\text{RR}_n = t_{n} - t_{n-1},
$$

the time from one heartbeat to the next. Plot those gaps against time and you get a
*tachogram* — a brand-new signal, sampled irregularly once per beat, that throws away the
voltage waveform entirely and keeps only the rhythm.

![A tachogram: RR interval in milliseconds plotted over several minutes, oscillating around 850 ms.](/posts/heart/tachogram.svg)

A healthy heart is not a metronome. Look at the wobble — the interval breathes up and down
by tens of milliseconds. That variability is not noise. It is the autonomic nervous system
leaning on the pacemaker in real time, and it turns out to carry a remarkable amount of
information about stress, recovery, and health. This is **heart-rate variability**, or HRV.

## Step three: a Fourier window into the nervous system

The wobble looks random in time. But it is not — it is a sum of oscillations, and the way
you find oscillations hiding in a signal is, of course, the Fourier transform. Estimate the
power spectral density of the RR series (after resampling it onto an even grid, since it
arrives one sample per beat),

$$
S(f) = \lim_{T \to \infty} \frac{1}{T}\, \mathbb{E}\!\left[\,\big|\hat{x}_T(f)\big|^2\,\right],
$$

in practice via Welch's method, and the structure jumps out.

![Power spectral density of the RR-interval series, with a low-frequency peak near 0.1 Hz and a high-frequency peak near 0.25 Hz, the LF and HF bands shaded.](/posts/heart/hrv-psd.svg)

Two peaks, two stories. The **high-frequency** band (0.15–0.4 Hz) is driven by your
breathing — the heart speeds up on the inhale and slows on the exhale, a parasympathetic,
"rest and digest" reflex. The **low-frequency** band (0.04–0.15 Hz) reflects slower
control loops with a strong sympathetic, "fight or flight" contribution. Their ratio,

$$
\frac{\text{LF}}{\text{HF}} = \frac{\displaystyle\int_{0.04}^{0.15} S(f)\,df}{\displaystyle\int_{0.15}^{0.40} S(f)\,df},
$$

is a crude but genuinely useful dial for autonomic balance. A heart under chronic stress
and one deep in recovery look different here — not in the waveform, not even in the average
heart rate, but in how the power splits between two bands of a spectrum.

## The same machinery, pointed somewhere new

Step back and look at what we did. We took a weak signal, band-pass filtered it to reject
interference, extracted a derived sequence, and read its power spectrum to recover hidden
structure. Swap a few nouns and that is a description of a radio receiver estimating channel
statistics. The filters, the spectral estimators, the habit of asking *which band carries
the information* — all of it transfers.

That is the quiet thrill of signal processing: it does not actually care what the signal
*is*. A waveform from an antenna and a waveform from an artery are, to the math, the same
kind of object. Learn the toolbox once and the heart becomes just another channel worth
decoding — which is more or less the bet behind everything I am building in health right now.
