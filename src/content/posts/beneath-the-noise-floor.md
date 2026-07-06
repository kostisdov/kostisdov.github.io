---
title: "Operating beneath the noise floor"
description: "A long-range radio link can decode a signal whose power sits below the thermal noise. It breaks no law: the signal-to-noise ratio in the occupied band has no lower limit, while the true wall is on energy per bit. The fundamentals, and how they set the design of a weak-signal link."
date: 2026-07-04
tags: ["signals", "wireless"]
image: "/og/beneath-the-noise-floor.png"
---

A radio link built for range or robustness, a deep-space probe, a satellite navigation signal, a
tactical waveform, routinely operates where the received signal power is smaller than the noise in
the same band. A spectrum analyser at the antenna shows only noise, yet the receiver decodes
without error. This seems to contradict the noise floor as a hard limit, but it does not. The
paradox dissolves once two quantities are separated: the signal-to-noise ratio in the occupied
band, which has no lower bound, and the energy per bit relative to the noise density, which does.
Reconciling them is the whole subject of a weak-signal link budget, and it fixes how far beneath
the noise floor a receiver can work.

## The receiver noise floor and sensitivity

Every receiver is preceded by thermal noise. A resistor at temperature $T$ delivers a noise power
spectral density $kT = -174$ dBm/Hz at room temperature. Raised by the front-end noise figure
(NF), it becomes the input-referred noise density $N_0 = kT + \text{NF}$, and over a bandwidth $B$
the noise floor is [1]

$$
\text{floor} = N_0 + 10\log_{10}B = kT + \text{NF} + 10\log_{10}B,
$$

in dBm, with $B$ in hertz. It rises with bandwidth: every doubling of $B$ adds $3$ dB. A modulation
and coding scheme (MCS) decodes once the SNR exceeds the required
$\text{SNR}_\text{req}$, so the sensitivity at this MCS becomes

$$
P_\text{sens} = \text{floor} + \text{SNR}_\text{req}.
$$

Nothing forces $\text{SNR}_\text{req}$ to be positive. A robust MCS can require a negative SNR in
decibels, and then $P_\text{sens}$ lies below the noise floor: the receiver recovers a signal
weaker than the noise sharing its band. What follows is how far $\text{SNR}_\text{req}$ can be
pushed down, by what mechanisms, and against what limit.

## Signal-to-noise ratio, energy per bit, and spectral efficiency

The occupied-band SNR suits the analogue front-end, but the decoder cares about the energy in each
information bit, and the SNR factors cleanly into the two:

$$
\text{SNR} = \frac{P}{N_0 W} = \frac{E_b}{N_0}\,\eta,
$$

a fundamental quantity, the energy per bit $E_b/N_0$, times an architectural one, the spectral
efficiency $\eta$. Here $E_b = P/R_b$ is the energy per information bit, $E_b/N_0$ the detection
figure of merit [2], and $\eta = R_b/W$ the bits per second carried in each hertz of occupied
bandwidth $W$; the factorisation follows from the occupied-band noise power $N_0 W$ and
$P = E_b R_b$.

For a fixed noise floor, sensitivity improves by lowering the required SNR, and there are two ways:

- **Reduce the bit rate $R_b$**: the required signal power drops by $10\log_{10}$ per decade of
  rate, the fall in $\eta$ a byproduct (widening $W$ instead would lift the floor by the same
  amount and cancel). Holding a low rate in a fixed channel, occupying more bandwidth than the
  information needs, is exactly spreading.
- **Lower the required $E_b/N_0$**: by the coding gain of FEC toward the $-1.59$ dB wall, or by
  multi-antenna processing.

Power is conserved along the transmit chain. From information bits through symbols to spreading
chips,

$$
P = E_b R_b = E_s R_s = E_\text{chip} R_\text{chip},
$$

each equality a rate conversion that holds power fixed while diluting it across more degrees of
freedom; expanding the bandwidth, by coding or spreading, spreads the same $P$ over more hertz and
never adds power.

## Spreading: processing gain at fixed bandwidth

Reducing the bit rate is the first lever, and spreading is how a low rate occupies a fixed channel.
In an occupied bandwidth $W$, an information rate $R_b$ needs an information bandwidth of only
$W_\text{info} \approx R_s$, far narrower than $W$; direct-sequence spreading widens each symbol
back to $W$ with a chip sequence [3], at a spreading factor equal to the ratio,

$$
\text{SF} = \frac{W}{W_\text{info}} = \frac{R_\text{chip}}{R_s},
\qquad \text{processing gain} = 10\log_{10}\text{SF}.
$$

Spread across $W$, the signal's power is diluted over $\text{SF}$ times more hertz than it needs, so
its occupied-band SNR is $\text{SF}$ times smaller than in the information band, at unchanged
$E_b/N_0$: the harder the spread, the deeper below the noise it sinks. Despreading correlates
against the known chip sequence, summing the $\text{SF}$ chips coherently while the uncorrelated
noise adds incoherently, and the signal collapses back to $W_\text{info}$ with its SNR lifted by
$\text{SF}$,

$$
\text{SNR}_\text{info} = \text{SF}\cdot\text{SNR}_\text{occ}.
$$

Take $\text{SF} = 10$: a signal at $-10$ dB in the occupied band ($0.1$) despreads over ten chips to
$10 \times 0.1 = 1 = 0$ dB in the information band, level with the noise and decodable (Fig. 1).
Because the low rate is what set the narrow information band, the $10\log_{10}\text{SF}$ of
processing gain and the rate reduction are one and the same number: spreading is the mechanism, the
low $R_b$ is the sensitivity, and $E_b/N_0$ never moves. The processing gain is an integration gain:
despreading coherently sums the $\text{SF}$ chips of each symbol, so a lower rate integrates over
more chips and lifts the signal further.

<figure>
<img src="/posts/beneath-the-noise-floor/below-floor.svg" alt="Two power spectral density panels within a fixed channel bandwidth: a signal spread below the noise floor, and the same signal after despreading rising to the floor in the narrow information band." />
<figcaption>Fig. 1: Despreading in the power spectral density; the channel bandwidth W is fixed. A low data rate needs only the narrow information bandwidth W_info, and spreading fills the channel with it at SF = W/W_info. Left: spread across W, the signal sits 10 dB below the noise floor N₀, an occupied-band SNR of −10 dB. Right: correlating against the code collapses it back to W_info and lifts it by the processing gain 10·log₁₀ SF = 10 dB, to 0 dB. N₀ is unchanged; only the accounting bandwidth moves.</figcaption>
</figure>

These are not deep-space abstractions. LoRa is built on exactly this lever: its chirp spread
spectrum holds a fixed channel (typically $125$ kHz) and selects a spreading factor from SF7 to
SF12, each step doubling the symbol length and buying roughly $2.5$ dB, so sensitivity runs from
about $-123$ dBm (SF7) to $-137$ dBm (SF12) in the same channel. GPS goes further: a $1.023$ Mchip/s coarse/acquisition code
carrying a $50$ bit/s message is a processing gain of $10\log_{10}(1.023\times10^6/50) \approx 43$
dB, so the signal arrives roughly $20$ dB below the thermal noise and is recovered by despreading.
Both trade rate for range in a fixed band, exactly the lever of this section.

Processing gain buys a chosen negative occupied-band SNR, and with it a sensitivity below the noise
floor. It leaves $E_b/N_0$ unchanged, which the next section shows is the one quantity that is
actually bounded.

## Coding gain and the energy-per-bit wall

The Shannon capacity of an additive white Gaussian noise channel of bandwidth $W$, power $P$, and
noise density $N_0$ is [4]

$$
C = W\log_2\!\Big(1 + \frac{P}{N_0 W}\Big) \quad [\text{bits/s}].
$$

Reliable communication needs $R_b \le C$. Dividing by $W$ recasts this in spectral efficiency:

$$
\eta = \frac{R_b}{W} \le \log_2(1 + \text{SNR})
\quad\Longrightarrow\quad \text{SNR} \ge 2^{\eta} - 1.
$$

Substituting $\text{SNR} = (E_b/N_0)\,\eta$ gives the energy-per-bit bound,

$$
\frac{E_b}{N_0} \ge \frac{2^{\eta} - 1}{\eta},
$$

the least energy per bit any modulation and code can spend at spectral efficiency $\eta$, the
curve of Fig. 2. It rises with $\eta$ ($\eta = 1$ needs $0$ dB, $\eta = 2$ needs $1.76$ dB) and is
smallest as $\eta \to 0$. Expanding $2^{\eta} = 1 + \eta\ln 2 + O(\eta^2)$,

$$
\frac{2^{\eta} - 1}{\eta} = \ln 2 + O(\eta) \;\longrightarrow\;
\ln 2 \approx 0.693 \equiv -1.59\ \text{dB}.
$$

This is the wall: no bandwidth, coding, or spreading beats $E_b/N_0 = -1.59$ dB, approached only
as $\eta \to 0$, that is with infinite bandwidth [5].

<figure>
<img src="/posts/beneath-the-noise-floor/shannon-plane.svg" alt="Spectral efficiency versus the minimum required Eb/N0 in dB, with the achievable region to the right of the bound curve and a vertical asymptote at minus 1.59 dB." />
<figcaption>Fig. 2: The energy-per-bit bound in the spectral-efficiency plane. Reliable communication at spectral efficiency η needs an energy per bit of at least Eb/N0 = (2<sup>η</sup> − 1)/η (red curve); the region to its right is achievable, the left is not. The requirement climbs steeply as bits are packed more densely, and falls to the wall at −1.59 dB (dashed) as η → 0, the infinite-bandwidth limit. The line η = 1 (0 dB) separates the bandwidth-limited regime above, where hertz are the scarce resource, from the power-limited regime below, where energy per bit is scarce and low-rate coding and spreading operate.</figcaption>
</figure>

Lowering $\eta$ walks the operating point down the curve toward the wall, which infinite bandwidth
reaches and nothing passes. Coding gain is what walks a finite-bandwidth system toward it, and how
close it gets, against what it costs, is the next section.

## Coding gain versus processing gain

Two mechanisms expand the bandwidth, doing different jobs. Coding gain, from forward error
correction (FEC), lowers the required $E_b/N_0$ toward the $-1.59$ dB wall, the only lever that
moves the fundamental requirement. Processing gain, from spreading, lowers the occupied-band SNR at
fixed $E_b/N_0$: it buys robustness rather than range, since a spreading code is only a repetition
code and adds no coding gain in a Gaussian channel. In fading it earns more, its independently
faded copies giving diversity, a steepening of the error-rate curve that coding alone does not
provide [6].

A real link spends its bandwidth budget on both,

$$
W_\text{expansion} = \underbrace{\tfrac{1}{R_c}}_{\text{FEC}} \times
\underbrace{\text{SF}}_{\text{spreading}},
$$

giving FEC as much as the decoder complexity allows, since only FEC buys down $E_b/N_0$, and the
rest to spreading for the robustness FEC cannot provide: interference rejection, multipath
resolution, multiple access, and low probability of intercept. Satellite navigation is the
canonical balance, heavy spreading for jam resistance and multiple access alongside FEC for the
coding gain that approaches the wall. The split is an implementation-complexity trade, not a
fundamental one.

## Designing a long-range link

The pieces assemble into a design procedure. Consider a telemetry link that must close over a long
range within a fixed channel of $W = 400$ kHz, with noise figure $\text{NF} = 3$ dB, so the input
noise density is $N_0 = -174 + 3 = -171$ dBm/Hz. Take BPSK with a rate-$1/2$ low-density
parity-check (LDPC) code, decoding at $(E_b/N_0)_\text{req} \approx 1.5$ dB.

Range is bought by sensitivity, and sensitivity by a low rate. The input noise density is
$N_0 = kT + \text{NF}$, and a real receiver also pays an implementation loss $L_\text{impl}$, the
gap from the ideal: carrier and timing synchronization error, phase noise, channel-estimation
error, filter and pulse-shaping mismatch, and quantization, typically $1$ to $3$ dB in all. Since
$E_b/N_0 = P/(N_0 R_b)$,

$$
\begin{aligned}
P_\text{sens} = {}& \underbrace{-174 + \text{NF}}_{\text{noise density}}
+ \underbrace{10\log_{10}\!\big(R_b/\text{Hz}\big)}_{\text{data rate}} \\[6pt]
&+ \underbrace{(E_b/N_0)_\text{req}}_{\text{coding, antennas}}
+ \underbrace{L_\text{impl}}_{\text{implementation}}
\quad [\text{dBm}].
\end{aligned}
$$

Every term is a design lever, and bandwidth is not among them: the only ways to buy sensitivity are
a lower noise figure, a lower bit rate ($10\log_{10}$ per decade, unbounded), a lower required
$E_b/N_0$ from coding gain toward the wall or from multi-antenna processing (maximum-ratio combining
of $M$ antennas sums the branch SNRs for a $10\log_{10}M$ gain in $E_b/N_0$), or less implementation
loss. In one view:

| Lever | Sensitivity term it moves | Bandwidth cost | Ceiling |
| :--- | :---: | :---: | :---: |
| Lower noise figure | NF | none | hardware |
| Reduce bit rate | 10·log₁₀ Rb | none (spread to fill W) | unbounded |
| Coding gain (FEC) | (Eb/N0) required | expands W | −1.59 dB wall |
| Multi-antenna processing | (Eb/N0) required | none | 10·log₁₀ M, plus diversity |
| Spreading at fixed Rb | in-band SNR only | expands W | 0 dB (robustness only) |

Run the numbers at two rates in the same $400$ kHz channel, taking $L_\text{impl} = 0$. Filling the
channel with data at $R_b = 200$ kbit/s gives $P_\text{sens} = -174 + 3 + 53.0 + 1.5 = -116.5$ dBm.
Dropping the rate a hundredfold, to $R_b = 2$ kbit/s, gives $-174 + 3 + 33.0 + 1.5 = -136.5$ dBm,
$20$ dB better, purely through the $10\log_{10}$ of the rate. The low-rate signal now occupies an
information bandwidth of only $4$ kHz, so filling the $400$ kHz channel spreads it by
$\text{SF} = W/R_s = 100$; the $20$ dB of sensitivity and the $20$ dB of processing gain are the
same number.

Suppose the geometry delivers a received power $P_r = -133$ dBm at the design range. The received
energy per bit is

$$
\begin{aligned}
\frac{E_b}{N_0} &= P_r - N_0 - 10\log_{10}\!\big(R_b/\text{Hz}\big) \\
&= -133 + 171 - 33.0 = 5.0\ \text{dB},
\end{aligned}
$$

so the low-rate link closes with $3.5$ dB of margin, while the high-rate one, at $E_b/N_0 = -15$
dB, does not come close. Over the $400$ kHz channel the noise floor is $N_0 + 10\log_{10}W = -115.0$
dBm, so the received signal at $-133$ dBm sits $18$ dB beneath it: a spectrum analyser shows only
noise. Despreading recovers the $20$ dB of processing gain, lifting the information-band SNR from
$-18$ dB to $+2$ dB, and the rate-$1/2$ code supplies the last $3$ dB, for $E_b/N_0 = 5$ dB. An
occupied-band SNR of $-18$ dB and an energy per bit of $+5$ dB coexist without contradiction; the
analyser reading is an artefact of the spread, and the decoder lives on $E_b/N_0$.

The mirror image is worth stating. Had the rate stayed fixed and the bandwidth been expanded by
spreading, rather than the rate lowered inside a fixed band, sensitivity would not have moved at
all: at fixed $R_b$ the $10\log_{10}R_b$ term is fixed, and spreading then buys only robustness. The
two cases are the two readings of $\text{SF}\cdot R_b$, and the sensitivity lives entirely in the
rate. Charging the spreading bandwidth to the link budget, or reading the buried SNR as a
shortfall, is the most common error in weak-signal design.

The link closes on paper, but a digital receiver adds one more noise floor, set by the
analogue-to-digital converter (ADC) and the gain ahead of it. With the automatic gain control (AGC)
applying a gain $G_\text{AGC}$ and the ADC full scale taken as $0$ dBm, the thermal noise referred
to the converter is

$$
P_\text{therm} = kT + \text{NF} + 10\log_{10}B + G_\text{AGC}
\quad [\text{dBFS}],
$$

so the AGC gain lifts the thermal floor to a usable level inside the converter's range.
Quantization is the second floor. With complex I/Q sampling the Nyquist rate equals the channel
bandwidth, so no oversampling gain spreads the quantization noise, and the
signal-to-quantization-noise ratio (SQNR) of an $N$-bit converter is

$$
\text{SQNR} = 6.02\,N + 1.76\ \text{dB}, \qquad P_\text{quant} = -\text{SQNR}\quad [\text{dBFS}],
$$

bandwidth-independent, at $-74.0$ dBFS for $12$ bits and $-98.1$ dBFS for $16$. The two add in
power to give the digital noise floor the decoder sees,

$$
P_\text{total} = 10\log_{10}\!\big(10^{P_\text{therm}/10} + 10^{P_\text{quant}/10}\big)
\quad [\text{dBFS}].
$$

Whether $P_\text{total}$ collapses onto $P_\text{therm}$, leaving the receiver thermal-limited,
depends on the margin between the two floors, which the ADC resolution and the AGC gain set
together. For a representative front end, $\text{NF} = 2$ dB and $G_\text{AGC} = 40$ dB:

| BW (MHz) | Bits | Thermal (dBFS) | Quant. (dBFS) | Margin (dB) | Combined (dBFS) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 2.5 | 12 | −68.0 | −74.0 | 6.0 | −67.0 |
| 2.5 | 16 | −68.0 | −98.1 | 30.1 | −68.0 |
| 5 | 12 | −65.0 | −74.0 | 9.0 | −64.5 |
| 5 | 16 | −65.0 | −98.1 | 33.1 | −65.0 |
| 10 | 12 | −62.0 | −74.0 | 12.0 | −61.7 |
| 10 | 16 | −62.0 | −98.1 | 36.1 | −62.0 |

At $16$ bits the quantization floor sits $30$ dB or more below thermal, the combined floor equals
the thermal one, and the receiver is thermal-limited at every bandwidth. At $12$ bits the margin
narrows to $6$ dB at $2.5$ MHz, where quantization lifts the floor by nearly a decibel, a direct
loss of sensitivity that eases at wider bandwidth only because the thermal floor itself rises. This
is the practical content of "enough AGC gain and enough bits": the gain lifts thermal clear of
quantization and the resolution keeps it there, so the digital floor falls back onto the analogue
one the rest of the article assumed [1].

Digitisation is only half of realizing the processing gain; the other half is synchronization,
since the receiver must acquire and track the code and carrier at the operating SNR, and any
residual misalignment is the implementation loss $L_\text{impl}$ of the sensitivity equation, paid
straight onto the required $E_b/N_0$.

## The two things that never move

A weak-signal receiver decodes beneath the noise floor because the occupied-band SNR has no lower
bound: spreading drives it as negative as $\text{SF}$ allows, and despreading recovers the loss
coherently. Two quantities do not move. The noise floor over the true detection bandwidth is set by
temperature, bandwidth, and noise figure. The energy-per-bit wall sits at $E_b/N_0 = -1.59$ dB, the
$\eta \to 0$ limit of the Shannon bound, and no bandwidth expansion crosses it. Operating below the
noise floor is a statement about power and SNR, always achievable; operating below $-1.59$ dB of
energy per bit is a statement about information, never achievable. Keeping the two apart, a low rate
and coding to buy sensitivity, spreading to buy robustness, is the whole discipline of weak-signal
design. The same accounting decides whether a waveform can be hidden under the noise while still
being read, where a later post on low-probability-of-intercept design will begin.

## References

[1] B. Razavi, *RF Microelectronics*, 2nd ed. Prentice Hall, 2011.

[2] J. G. Proakis and M. Salehi, *Digital Communications*, 5th ed. McGraw-Hill, 2008.

[3] R. L. Pickholtz, D. L. Schilling, and L. B. Milstein, "Theory of spread-spectrum
communications: a tutorial," *IEEE Transactions on Communications*, vol. 30, no. 5,
pp. 855–884, 1982.

[4] C. E. Shannon, "A mathematical theory of communication," *The Bell System Technical
Journal*, vol. 27, no. 3, pp. 379–423, 1948.

[5] S. Verdú, "Spectral efficiency in the wideband regime," *IEEE Transactions on Information
Theory*, vol. 48, no. 6, pp. 1319–1343, 2002.

[6] D. Tse and P. Viswanath, *Fundamentals of Wireless Communication*. Cambridge University
Press, 2005.
