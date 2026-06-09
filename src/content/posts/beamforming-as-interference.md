---
title: "Beamforming is just interference, weaponized"
description: "The whole trick behind phased arrays fits in one equation — and it's the same physics as ripples in a pond."
date: 2026-06-10
tags: ["signals", "maths"]
---

Drop two pebbles in a pond and watch the ripples cross. In some directions the crests
reinforce; in others they cancel. A phased array is nothing more than this, done on purpose
with $N$ pebbles and a phase knob on each.

## The array factor

Take a uniform linear array of $N$ antennas spaced $d$ apart, and a plane wave arriving from
angle $\theta$. The wave reaches each element with a slightly different delay, so the $n$-th
element sees a phase shift of $n k d \sin\theta$, where $k = 2\pi/\lambda$ is the wavenumber.
Stack these into the **steering vector**:

$$
\mathbf{a}(\theta) = \begin{bmatrix} 1 \\ e^{j k d \sin\theta} \\ \vdots \\ e^{j(N-1) k d \sin\theta} \end{bmatrix}
$$

The receiver combines the element outputs with complex weights $\mathbf{w} \in \mathbb{C}^N$,
so the response toward direction $\theta$ is the inner product

$$
A(\theta) = \mathbf{w}^{\mathsf{H}} \mathbf{a}(\theta).
$$

That's it. That's beamforming. Everything else — nulls, sidelobes, tapering, MIMO precoding —
is commentary on this one inner product.

## Why it works

Choose $\mathbf{w} = \frac{1}{\sqrt{N}}\mathbf{a}(\theta_0)$ and the phases align perfectly at
$\theta = \theta_0$: all $N$ terms add coherently and you collect a factor-$N$ array gain,

$$
|A(\theta_0)|^2 = \left| \frac{1}{\sqrt{N}} \sum_{n=0}^{N-1} 1 \right|^2 = N.
$$

Away from $\theta_0$, the terms become $N$ unit vectors spinning at different rates around the
complex plane — and a sum of out-of-phase phasors is small. For the uniform taper the pattern
collapses to a closed form, the Dirichlet kernel:

$$
|A(\theta)| = \frac{1}{\sqrt{N}} \left| \frac{\sin\!\big(N\psi/2\big)}{\sin\!\big(\psi/2\big)} \right|,
\qquad \psi = kd(\sin\theta - \sin\theta_0).
$$

Constructive interference where you want it, destructive everywhere else. The pond, weaponized.

## The part people forget

The model above silently assumed a *narrowband* signal: one $\lambda$, one $k$, one steering
vector. Make the array large enough — or the bandwidth wide enough — and the approximation
cracks. The phase shift $n k d \sin\theta$ depends on frequency, so each subcarrier in a
wideband waveform sees a slightly different beam direction. The beam *squints*.

For an OFDM signal with subcarrier frequency $f$, the beam points toward

$$
\sin\theta_f = \frac{f_c}{f}\,\sin\theta_0,
$$

drifting away from $\theta_0$ as $f$ moves off the carrier $f_c$. At mmWave with hundreds of
antennas and gigahertz of bandwidth, the edge subcarriers can miss the user entirely. (This
problem ate a good chunk of my PhD.)

---

Next time: what happens when you give up on phase shifters entirely and let true-time delays
do the steering.
