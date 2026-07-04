---
title: "Operating beneath the noise floor: fundamentals and design principles"
description: "A long-range radio link can decode a signal whose power sits below the thermal noise. Doing so breaks no law: the signal-to-noise ratio in the occupied band has no lower limit, while the true wall is on energy per bit, Eb/N0 = −1.59 dB. The fundamentals, and how they set the design of a weak-signal link."
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

Every receiver is preceded by thermal noise. A resistor at temperature $T$ delivers a noise
power spectral density $kT$, which at room temperature is $-174$ dBm/Hz. Integrated over a
bandwidth $B$ and raised by the front-end noise figure (NF), the noise floor referred to the
input is [1]

$$
\text{floor} = -174\ \text{dBm/Hz} + 10\log_{10}\!\big(B/\text{Hz}\big) + \text{NF},
$$

in dBm. It rises with bandwidth: every doubling of $B$ adds $3$ dB. A modulation and coding
scheme (MCS) decodes once the signal-to-noise ratio reaches a required value $\text{SNR}_\text{req}$,
set by the modulation order and the code, so the sensitivity, the least recoverable signal power,
is

$$
P_\text{sens} = \text{floor} + \text{SNR}_\text{req}.
$$

Nothing forces $\text{SNR}_\text{req}$ to be positive. A robust MCS can require a negative SNR in
decibels, and then $P_\text{sens}$ lies below the noise floor: the receiver recovers a signal
weaker than the noise sharing its band. What follows is how far $\text{SNR}_\text{req}$ can be
pushed negative, by what mechanisms, and against what limit.

## Signal-to-noise ratio, energy per bit, and spectral efficiency

The occupied-band SNR compares powers over the bandwidth the signal occupies. It suits the
analogue front-end, but the decoder cares about the energy in each information bit. With $R_b$ the
information rate and $P$ the received power, the energy per bit is $E_b = P/R_b$, and the
detection figure of merit is $E_b/N_0$ [2]. The two ratios connect through the spectral efficiency

$$
\eta = \frac{R_b}{W} \quad [\text{bits/s/Hz}],
$$

the bits per second carried in each hertz of occupied bandwidth $W$. Since the occupied-band noise
power is $N_0 W$ and $P = E_b R_b$,

$$
\text{SNR} = \frac{P}{N_0 W} = \frac{E_b R_b}{N_0 W} = \frac{E_b}{N_0}\,\eta .
$$

This factorisation is the pivot: the occupied-band SNR is the product of a fundamental quantity,
$E_b/N_0$, and an architectural one, $\eta$. Lowering $\eta$ at fixed $E_b/N_0$ drives the SNR down
without touching the energy accounting.

Power is conserved along the transmit chain. From information bits through coded bits, symbols,
and chips,

$$
P = E_b R_b = E_c R_{c} = E_s R_s = E_\text{chip} R_\text{chip},
$$

each equality a rate conversion that holds power fixed while spreading it across more degrees of
freedom. Expanding the bandwidth, by coding or spreading, dilutes the same $P$ over more hertz; it
never adds power.

## Spreading: trading SNR for bandwidth at fixed energy per bit

Direct-sequence spreading replaces each symbol with $\text{SF}$ chips, the spreading factor. The
chip rate is $R_\text{chip} = \text{SF}\cdot R_s$, the occupied bandwidth grows by $\text{SF}$,
and, power conserved, $E_\text{chip} = E_s/\text{SF}$ [3]. With $R_b$ fixed and $W$ up by
$\text{SF}$, the spectral efficiency falls to $\eta/\text{SF}$ and the occupied-band SNR falls with
it:

$$
\text{SNR} \;\longrightarrow\; \frac{\text{SNR}}{\text{SF}}, \qquad
\frac{E_b}{N_0}\ \text{unchanged}.
$$

The signal is now spread thinner than the noise, its occupied-band SNR negative. At the receiver,
despreading correlates against the known chip sequence, summing the $\text{SF}$ chips coherently
while the uncorrelated noise adds incoherently; the signal collapses to the information bandwidth
with its SNR multiplied by $\text{SF}$, the processing gain of $10\log_{10}\text{SF}$ decibels.

Take $\text{SF} = 10$ and a pre-despread SNR of $-10$ dB, that is $0.1$. Despreading over ten chips
gives $+10$ dB, and

$$
\text{SNR}_\text{info} = \text{SF}\cdot\text{SNR}_\text{occ} = 10 \times 0.1 = 1 = 0\ \text{dB}.
$$

The signal that sat $10$ dB under the noise emerges level with it, enough for a robust MCS to
decode (Fig. 1).

<figure>
<img src="/posts/beneath-the-noise-floor/below-floor.svg" alt="Two power spectral density panels: a signal below the noise floor over the occupied bandwidth, and the same signal after despreading rising to the floor over the information bandwidth." />
<figcaption>Fig. 1: The effect of despreading on the signal's power spectral density. Left: before despreading the signal fills the occupied bandwidth W_occ and sits 10 dB below the noise floor N₀, an SNR of −10 dB. Right: correlating against the code collapses it to the information bandwidth W_info and lifts it by the processing gain 10·log₁₀ SF = 10 dB, to an SNR of 0 dB. The noise density N₀ is unchanged; only the accounting bandwidth moves.</figcaption>
</figure>

Processing gain buys a chosen negative occupied-band SNR, and with it a sensitivity below the
noise floor. It leaves $E_b/N_0$ unchanged, which the next section shows is the one quantity that
is actually bounded.

## The energy-per-bit wall

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
<figcaption>Fig. 2: The energy-per-bit bound in the spectral-efficiency plane. At each spectral efficiency η, reliable communication requires an energy per bit of at least Eb/N0 = (2^η − 1)/η (red curve); the region to the right is achievable, the region to the left is not. The requirement rises steeply where bits are packed densely into the band, and descends toward the wall at −1.59 dB (dashed) as η → 0, the infinite-bandwidth limit. The line η = 1, at 0 dB, divides the bandwidth-limited regime above, where hertz are scarce, from the power-limited regime below, where energy per bit is scarce and where low-rate coding and spreading operate.</figcaption>
</figure>

Lowering $\eta$ walks the operating point down the curve toward the wall, which infinite bandwidth
reaches and nothing passes.

## Coding gain versus processing gain

The two levers act on different factors of $\text{SNR} = (E_b/N_0)\,\eta$. Forward error correction
(FEC) lowers the $E_b/N_0$ required for a target error rate, a genuine reduction in energy per bit
that moves the operating point toward the $-1.59$ dB wall. Spreading lowers $\eta$, and with it the
occupied-band SNR, at fixed $E_b/N_0$: it buys headroom and robustness, not a lower fundamental
requirement.

That spreading yields no coding gain in a Gaussian channel is worth proving. A spreading factor
$\text{SF}$ is a rate-$1/\text{SF}$ repetition code: each bit is sent as $\text{SF}$ copies of
energy $E_s = E_b/\text{SF}$. Maximum-ratio combining (MRC) sums the per-copy SNRs,

$$
\frac{E_b}{N_0}\bigg|_\text{combined} = \sum_{i=1}^{\text{SF}} \frac{E_s}{N_0}
= \text{SF}\cdot\frac{E_b/\text{SF}}{N_0} = \frac{E_b}{N_0},
$$

so the combined energy per bit equals that of sending the bit once with all its energy: the
post-combining error rate is the uncoded curve $Q\!\big(\sqrt{2E_b/N_0}\big)$, the
$+10\log_{10}\text{SF}$ processing gain cancelling the $-10\log_{10}\text{SF}$ energy dilution. A
real code of the same rate spreads redundancy across different bits with large minimum distance,
so errors are corrected by structure, not merely averaged. Repetition has minimum distance
$\text{SF}$ at rate $1/\text{SF}$, a rate-distance product of $1$, the same as uncoded; good codes
exceed it. That is the formal sense in which repetition is the worst code of its rate.

The same suboptimality appears in capacity. Despreading discards the degrees of freedom the
occupied bandwidth carried, so the full occupied-bandwidth channel can carry more than the
despread information band it collapses to. A low-rate code over the same bandwidth keeps those
degrees of freedom; plain spreading discards them. Both expand bandwidth, but only coding turns
the expansion into information.

<figure>
<img src="/posts/beneath-the-noise-floor/ber-coding-diversity.svg" alt="Two bit-error-rate panels: an AWGN panel where uncoded BPSK coincides with repetition and MRC, and a Rayleigh fading panel where MRC diversity of order one, two, and four gives progressively steeper slopes." />
<figcaption>Fig. 3: Coding gain and diversity gain are distinct. Left (AWGN): uncoded BPSK, which repetition plus MRC reproduces exactly; a representative FEC curve (schematic) sits several dB to the left, the coding gain, bounded by the Shannon wall at −1.59 dB. Right (Rayleigh fading, MRC): combining L = 1, 2, 4 independently faded copies steepens the error-rate slope, the diversity gain of order L, absent in the non-fading channel on the left.</figcaption>
</figure>

The verdict flips in fading. When the copies fade independently, separated in time, frequency, or
space beyond the coherence interval, MRC over $\text{SF}$ branches yields diversity of order
$\text{SF}$: the error-rate curve steepens from $\sim(E_b/N_0)^{-1}$ to $\sim(E_b/N_0)^{-\text{SF}}$
[6]. This is diversity gain, a change of slope, not coding gain, a shift on the Gaussian curve, and
it needs the copies to be genuinely independent; spreading in a flat, slow channel gives correlated
copies and no diversity, whereas frequency-selective multipath resolved by a RAKE receiver supplies
it. Fig. 3 places the two side by side.

Because real links face both interference and fading, they split the bandwidth expansion between
the two mechanisms,

$$
W_\text{expansion} = \underbrace{\tfrac{1}{R_c}}_{\text{FEC}} \times
\underbrace{\text{SF}}_{\text{spreading}},
$$

giving FEC as much of the budget as the decoder allows, since only FEC buys down $E_b/N_0$, and
spending the rest on spreading for what FEC does not provide: interference rejection, multipath
resolution, multiple access, and a low probability of intercept. Satellite navigation is the
canonical example, heavy spreading for despreading gain and jam resistance alongside FEC for the
coding gain that approaches the wall.

## Designing a long-range link, end to end

The pieces assemble into a design procedure, and one example fixes the order of the decisions.
Consider a telemetry link that must close over a long range, at a low data rate, and survive both
interference and interception. Fix the information rate at $R_b = 2$ kbit/s and the noise figure at
$\text{NF} = 3$ dB, so the noise density at the input is $N_0 = -174 + 3 = -171$ dBm/Hz.

The MCS sets the required energy per bit. Take BPSK with a rate-$1/2$ low-density parity-check
(LDPC) code, decoding at $(E_b/N_0)_\text{req} \approx 1.5$ dB, a few decibels inside the wall.
Sensitivity then follows from the energy accounting alone, since $E_b/N_0 = P/(N_0 R_b)$:

$$
\begin{aligned}
P_\text{sens} &= \Big(\frac{E_b}{N_0}\Big)_\text{req} + N_0 + 10\log_{10}\!\big(R_b/\text{Hz}\big) \\
&= 1.5 - 171 + 33.0 = -136.5\ \text{dBm}.
\end{aligned}
$$

This is the thesis in one line: sensitivity is set by the required $E_b/N_0$, the noise density,
and the bit rate, and by nothing else. No bandwidth and no spreading factor appears, and the
ultimate sensitivity floor is $N_0 R_b \ln 2$, the same expression at the wall.

Suppose the link geometry, transmit power, antenna gains, and path loss deliver a received power
$P_r = -133$ dBm at the design range. The received energy per bit is

$$
\begin{aligned}
\frac{E_b}{N_0} &= P_r - N_0 - 10\log_{10}\!\big(R_b/\text{Hz}\big) \\
&= -133 + 171 - 33.0 = 5.0\ \text{dB},
\end{aligned}
$$

exceeding the requirement by $3.5$ dB, so the link closes. Nothing so far has mentioned bandwidth.

Robustness is a separate decision, and where the spreading factor enters. To bury the emission and
resist a jammer, spread with $\text{SF} = 100$. The coded symbol rate is $R_s = R_b/R_c = 4$
ksym/s, so the occupied bandwidth is $W = \text{SF}\cdot R_s = 400$ kHz, and the noise over it is

$$
\text{floor}_\text{occ} = N_0 + 10\log_{10}\!\big(W/\text{Hz}\big) = -171 + 56.0 = -115.0\ \text{dBm}.
$$

The received signal, at $-133$ dBm, now sits $18$ dB beneath this occupied-bandwidth floor: a
spectrum analyser shows only noise. Yet it carries $E_b/N_0 = 5.0$ dB, far above the wall, because
despreading recovers $10\log_{10}100 = 20$ dB of processing gain, lifting the information-band SNR
from $-18$ dB to $+2$ dB, and the rate-$1/2$ code supplies the remaining $3$ dB. An occupied-band
SNR of $-18$ dB and an energy per bit of $+5$ dB coexist without contradiction.

The same link without spreading sharpens the point. It would occupy just $4$ kHz, read $+2$ dB on
the analyser ($\eta = 0.5$), and close on the same $E_b/N_0 = 5$ dB. Spreading by $100$ swings the
analyser reading $20$ dB, from $+2$ to $-18$, and changes nothing the decoder depends on. The
reading is an artefact of how wide the signal is spread; the decoder lives on $E_b/N_0$.

The design principle is the separation of the two decisions. The bit rate and the coded modulation
fix the sensitivity, and with it the range; the spreading factor is chosen independently, for
interference rejection and low probability of intercept, and it is what carries the emission below
the noise at no cost in sensitivity [1]. Conflating them, by charging the spreading bandwidth to
the link budget or reading the buried SNR as a shortfall, is the most common error in weak-signal
design.

The link closes on paper, but a digital receiver adds one more noise floor, set by the
analogue-to-digital converter (ADC) and the gain ahead of it. With the automatic gain control (AGC)
applying a gain $G_\text{AGC}$ and the ADC full scale taken as $0$ dBm, the thermal noise referred
to the converter is

$$
P_\text{therm} = -174 + 10\log_{10}\!\big(B/\text{Hz}\big) + \text{NF} + G_\text{AGC}
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
residual misalignment is an implementation loss added straight onto the required $E_b/N_0$.

## The two things that never move

A weak-signal receiver decodes beneath the noise floor because the occupied-band SNR has no lower
bound: spreading drives it as negative as $\text{SF}$ allows, and despreading recovers the loss
coherently. Two quantities do not move. The noise floor over the true detection bandwidth is set by
temperature, bandwidth, and noise figure. The energy-per-bit wall sits at $E_b/N_0 = -1.59$ dB, the
$\eta \to 0$ limit of the Shannon bound, and no bandwidth expansion crosses it. Operating below the
noise floor is a statement about power and SNR, always achievable; operating below $-1.59$ dB of
energy per bit is a statement about information, never achievable. Keeping the two apart, coding to
buy down energy per bit and spreading to buy robustness, is the whole discipline of weak-signal
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
