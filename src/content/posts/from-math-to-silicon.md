---
title: "From math to silicon: a DSP block on an FPGA"
description: "One DSP block, z/|z|, taken from a floating-point formula to two FPGA pipelines. The fixed-point golden model sets the performance, and the RTL is verified bit-accurate against it."
date: 2026-10-23
tags: ["signals", "fpga"]
draft: false
image: "/og/from-math-to-silicon.png"
---

A DSP algorithm starts as a formula tested in floating point. There, a square root or a division costs
one line of code. On an FPGA the algorithm must become fixed-point logic that runs at one sample per
clock, and the same square root has to be designed. The work in between has three parts: choosing word
lengths, replacing operations the fabric does not have, and verifying that the hardware computes exactly
what the model computes. This article follows one small block through that flow and measures what each
choice costs.

## The workflow

Fig. 1 shows a typical flow for implementing a DSP block on an FPGA. The algorithm is first developed in
floating point, typically double precision in Python or MATLAB. At this stage word lengths, rounding and
overflow can still be ignored.

The fixed-point model comes next. It fixes the format of every signal and every rounding and saturation
step, and it defines the performance of the final design. It becomes the golden reference model.

The implementation follows in one of two ways. In HLS, the C++ code is first checked in C simulation
(C-sim). C synthesis then turns it into RTL, which is checked again in C/RTL co-simulation. The
alternative is hand-written RTL. In both cases, RTL verification drives the design with test vectors and
requires the outputs to be bit-accurate to the golden model.

Synthesis and implementation then report the resources and the timing. The hardware test closes the loop
on the board. Two feedback paths run through the flow. The error against the float model sets the word
lengths. Resources and timing can send the design back to other word lengths or another architecture.

<figure>
<img src="/posts/from-math-to-silicon/fig0-workflow.svg" alt="Flow diagram: floating-point algorithm, fixed-point golden reference model, then either HLS C++ with C simulation, C synthesis and co-simulation or hand-written RTL, then RTL verification against golden vectors from the fixed-point model, synthesis and implementation, and hardware test, with feedback from the error budget and from resources and timing." />
<figcaption>Fig. 1: A typical flow from algorithm to hardware. The fixed-point model provides the golden vectors for the HLS and RTL testbenches. This article covers the steps up to synthesis. Implementation, timing closure and the hardware test are not included.</figcaption>
</figure>

## The block: z/|z|

The block scales a complex sample to unit magnitude and keeps its phase:

$$
\frac{z}{|z|} = \frac{I + jQ}{\sqrt{I^2 + Q^2}}.
$$

It is used as a limiter ahead of phase and frequency detectors and in clipping for peak-to-average power
reduction. It also computes the phase-only weights of beamformers and equal-gain combiners.

The specification here is typical. $I$ and $Q$ are signed 16-bit samples in Q1.15, and so is the output.
One sample enters every clock. The worst-case error in either output component must stay below one LSB
over all inputs. An input of $z = 0$ maps to zero.

On a CPU the block is the formula:

```cpp
std::complex<float> normalize_cpu(std::complex<float> z) {
    float m = std::abs(z);  // sqrt(re^2 + im^2)
    return m > 0.0f ? z / m : std::complex<float>(0.0f, 0.0f);
}
```

On the test vectors, single precision is within 0.003 LSB of the exact result. The processor has a
multiplier, a square-root unit and a divider. An FPGA has adders, look-up tables (LUTs), small hardware
multipliers (DSP slices) and block RAM. The square root and the division must be built from these. Each
additional bit of accuracy costs logic.

## From float to fixed point

The float model defines the intended behaviour. The fixed-point model defines the behaviour the hardware
will have. Writing it means making every implicit choice explicit: the format of each intermediate value,
where rounding happens, and what happens at the edges.

Here the output is rounded once, half up, and then saturated. Saturation is needed because +1.0 is not
representable in Q1.15 and must become 32767. Rounding half up is not symmetric, and neither is the floor
of an arithmetic shift. For roughly one sample in ten, the result for $-z$ therefore differs from the
negated result for $z$ by one LSB. This stays within the error bound.

The fixed-point model is written in Python with integer arithmetic. It is the golden reference model:
the HLS code and the RTL must be bit-accurate to it, not to the float model.

One property of the block shapes both designs below: $z/|z|$ does not depend on the scale of $z$.
Shifting $I$ and $Q$ left by the same number of bits leaves the result unchanged. The precision available
to the arithmetic improves. Both architectures use this.

The two operations that the fabric lacks can also be merged. Instead of a square root followed by a
division,

$$
\frac{z}{|z|} = z \cdot \left(I^2 + Q^2\right)^{-1/2},
$$

so one reciprocal square root replaces both. Tables with interpolation and Newton–Raphson iteration
compute it directly [3]. Architecture A uses a leading-zero normalisation and an interpolated table.
Architecture B uses CORDIC [1], [2]. It avoids the reciprocal square root and rotates $z$ onto the unit
circle instead.

## Architecture A: normalise, look up, interpolate

The first design computes the reciprocal square root with a table, in four steps:

1. The power $P = I^2 + Q^2$, exact in 32 bits.
2. An even shift $s$: the leading-zero count of $P$, rounded down to an even number. Then $m = P \ll s$
   lies in $[2^{30}, 2^{32})$, and $u = m / 2^{32}$ lies in $[1/4, 1)$. The shift is even so that the
   square root of $2^s$ is again a shift, by $s/2$.
3. $1/\sqrt{u}$ from a table. The top nine bits of $m$ address it, and the next twelve bits interpolate
   linearly. The result $r$ has 17 fractional bits.
4. The products $I \cdot r$ and $Q \cdot r$, shifted right by $18 - s/2$ with a single rounding.

<figure>
<img src="/posts/from-math-to-silicon/fig1-rsqrt-table.svg" alt="Left: the curve one over square root of u for u from a quarter to one, with a coarse piecewise-linear approximation. Right: the error of the 384-entry table, up to about 1000 LSB using the entry below the address alone and about 2 LSB with linear interpolation." />
<figcaption>Fig. 2: Left: 1/√u over the normalised range, with a coarse interpolated table for illustration. Right: error of the 384-entry table actually used, in units of its own LSB (2⁻¹⁷). Grey: the entry below the address alone. Red: with linear interpolation.</figcaption>
</figure>

After normalisation the table only sees $u$ between 1/4 and 1, for any input. So 384 entries cover
the whole range. The entry below the address alone is off by up to 1,018 LSB of $r$. Interpolating to the
next entry brings the error down to 2.4 LSB, at the cost of one small multiplier (Fig. 2). Without
interpolation, the same accuracy would take more than 100,000 entries. Each entry stores a 19-bit base
value and a 10-bit slope.

The table size follows from the error budget. Fig. 3 (left) sweeps it, with the worst case taken over all
$2^{32}$ inputs. Nine address bits (384 entries) is the smallest table tested that keeps the complete
block below one output LSB.

<figure>
<img src="/posts/from-math-to-silicon/fig2-accuracy-vs-cost.svg" alt="Worst-case output error over all inputs against table size for architecture A, falling below one LSB at 384 entries, and against the number of CORDIC micro-rotations for architecture B, falling below one LSB at 18." />
<figcaption>Fig. 3: Worst-case output error over all 2³² inputs against the main cost parameter. Left: table entries for architecture A. Right: micro-rotations for architecture B. Dashed: one output LSB.</figcaption>
</figure>

In HLS C++ the four steps follow the description closely. The types carry explicit widths, and the
rounding is written out. The pragmas request distributed ROM (LUTRAM) for the tables and an initiation
interval (II) of one, so a new sample enters every clock. The rounding helper `round_sat` and the
generated tables are not shown:

```cpp
void normalize_hls(sample_t i, sample_t q, sample_t &x, sample_t &y) {
#pragma HLS PIPELINE II=1
#pragma HLS BIND_STORAGE variable=RSQRT_BASE type=rom_1p impl=lutram
#pragma HLS BIND_STORAGE variable=RSQRT_SLOPE type=rom_1p impl=lutram
    // 1. power, exact: |I|, |Q| <= 2^15, so P <= 2^31
    ap_uint<32> p = ap_uint<32>(i * i) + ap_uint<32>(q * q);
    if (p == 0) { x = 0; y = 0; return; }

    // 2. normalise by an even shift: m = P << s lies in [2^30, 2^32)
    ap_uint<5> s = p.countLeadingZeros() & 0x1E;
    ap_uint<32> m = p << s;

    // 3. table lookup with linear interpolation: r ~ 2^17 / sqrt(m / 2^32)
    ap_uint<9> k = m(31, 23);
    ap_uint<12> f = m(22, 11);
    ap_uint<19> r = RSQRT_BASE[k - 128] - ((RSQRT_SLOPE[k - 128] * f + 2048) >> 12);

    // 4. undo the normalisation: x = i * r / 2^(18 - s/2)
    ap_uint<5> sh = 18 - (s >> 1);
    x = round_sat(i * r, sh);
    y = round_sat(q * r, sh);
}
```

Unlike the CPU version, this code describes hardware. Each declared width sets the size of a register or
an adder, and each operator is implemented as logic. The approximation is written out instead of being
called from a library. HLS tools do provide functions such as `hls::rsqrt` [4]. Using one hands the
choice of word lengths and error to the library.

## Architecture B: CORDIC without the angle

CORDIC computes rotations with additions and shifts only [1], [2]. In vectoring mode it rotates $z$ onto
the real axis through micro-rotations by $\pm\arctan 2^{-j}$. Each sign is chosen from the sign of the
imaginary part. The signs $d_j$ encode the angle of $z$. A common next step accumulates that angle and
feeds it to a second CORDIC in rotation mode, which turns it into $\cos\theta$ and $\sin\theta$.

The angle itself is not needed. Apply the same sequence of micro-rotations in the opposite direction to
the vector $(1/K, 0)$. Here $K \approx 1.647$ is the CORDIC gain. The result is $e^{j\theta} = z/|z|$,
with no angle register and no arctangent table. CORDIC arrays for QR decomposition pass direction bits
between stages in the same way. Here each pipeline stage applies one micro-rotation to both vectors with
a shared sign. That takes four adder/subtractors; the shifts are by constants and cost only wiring.

```verilog
wire neg = yj[W-1];  // d_j = +1 when y < 0
// shift first, as signed wires: inside an unsigned expression >>> would be a logical shift
wire signed [W-1:0] xsh = xj >>> j, ysh = yj >>> j, ush = uj >>> j, vsh = vj >>> j;
// a - b written as a + ~b + 1, so each output needs one carry chain
wire [W-1:0] sub = {W{neg}}, add = {W{~neg}};
wire [W-1:0] c_sub = {{(W-1){1'b0}}, neg}, c_add = {{(W-1){1'b0}}, ~neg};
always @(posedge clk) begin
    xs[(j+1)*W +: W] <= xj + (ysh ^ sub) + c_sub;  // neg ? x - y' : x + y'
    ys[(j+1)*W +: W] <= yj + (xsh ^ add) + c_add;  // neg ? y + x' : y - x'
    us[(j+1)*W +: W] <= uj + (vsh ^ add) + c_add;  // same signs, reversed,
    vs[(j+1)*W +: W] <= vj + (ush ^ sub) + c_sub;  // on (1/K, 0)
end
```

The fixed-point model required two extra steps. CORDIC converges only for angles within about ±99.9°.
A rotation by ±90° therefore first brings $z$ into the right half-plane, and the output undoes it.

The second step matters more. A small input, for example $z = 1 + 0j$, holds too few bits for the shifts
$2^{-j}$ to act on. After a few stages its components shift to zero, and the remaining signs no longer
depend on the angle. The fix is the scale invariance again. $I$ and $Q$ are shifted left together until
the larger of the two reaches the top of its range. This keeps the error below one LSB at every
magnitude (Fig. 4).

<figure>
<img src="/posts/from-math-to-silicon/fig3-error-vs-magnitude.svg" alt="Worst-case output error against input magnitude from one LSB to full scale: both architectures stay below one LSB everywhere, while CORDIC without block normalisation reaches about 70 LSB at the smallest magnitudes." />
<figcaption>Fig. 4: Worst-case output error against the input magnitude, in half-octave steps with 1024 angles per point. Without block normalisation, CORDIC is accurate only near full scale.</figcaption>
</figure>

With 18 micro-rotations and 8 guard bits, CORDIC meets the same error budget as the table design
(Fig. 3, right). Its datapath is 28 bits wide. Both fixed-point models were checked exhaustively over all $2^{32}$ inputs.
The check uses C++ ports of the models, which match the Python models on every test vector. The
worst-case error in either component is 0.795 LSB for architecture A and 0.797 LSB for architecture B.
The RMS error is 0.296 and 0.306 LSB, against 0.289 LSB for ideal rounding. The saturation of +1.0 to
32767 is not counted as error, since no 16-bit design can avoid it.

## HLS or RTL?

Both architectures are also written by hand in Verilog. Design A becomes a six-stage pipeline: squares,
normalisation, table read, interpolation, multiplication and rounding. Design B becomes twenty stages:
normalisation and pre-rotation, eighteen identical micro-rotations, and the output rounding.

For this block, HLS shortened the exploration of word lengths and table sizes, with verification at
C-simulation speed.
Hand-written RTL gave exact control over the pipeline stages and over which operations map to DSP slices.
The HLS C simulation of A and the RTL of A are both bit-accurate to the golden model.

## RTL verification

RTL verification requires the RTL outputs to be bit-accurate to the golden reference model: equal on
every bit, not within a tolerance. The error analysis already lives in the fixed-point model. Any
difference in the RTL is therefore a bug. The testbench, written in cocotb [5], streams one vector into
the pipeline every clock and checks every output sample:

```python
if str(dut.out_valid.value) == "1":
    i, q, ex, ey = pending.popleft()
    gx, gy = dut.x.value.to_signed(), dut.y.value.to_signed()
    if (gx, gy) != (ex, ey):
        mismatches += 1
```

The stimulus covers every octave of magnitude equally, from one LSB to full scale, with uniform angles.
Corner cases are added: full-scale negative values, single-LSB inputs and zero. On 100,015 vectors, both
RTL designs and the HLS C simulation are bit-accurate to the golden model.

The testbench catches small changes. Each change below was injected alone into a copy of the RTL:

- A one-LSB change in the interpolation rounding constant of design A: 921 of 100,015 samples flagged.
- The output rounding removed: 71,739 samples flagged in design A and 70,323 in design B.
- The sign of the last micro-rotation of design B inverted: 57,762 samples flagged.

It also detected an actual design error during this work. The first add/subtract version of the CORDIC stage mixed
signed and unsigned operands in one Verilog expression. This turned the arithmetic shift `>>>` into a
logical shift, and 100,014 of the 100,015 samples failed.

## What it costs

<figure>
<img src="/posts/from-math-to-silicon/fig4-resources.svg" alt="Horizontal bars of LUTs, flip-flops and DSP slices as a share of an Artix-7 XC7A35T: the table design uses 796 LUTs, 139 flip-flops and 5 DSP slices; the CORDIC design uses 2,514 LUTs, 1,926 flip-flops and no DSP slices." />
<figcaption>Fig. 5: Resources at one sample per clock, as a share of an Artix-7 XC7A35T (20,800 LUTs, 41,600 flip-flops, 90 DSP slices). Labels give the absolute counts. Neither design uses block RAM. Yosys synthesis for the 7-series family [6]: estimates, not Vivado results.</figcaption>
</figure>

| | Latency (cycles) | LUT | Flip-flops | DSP48 | Block RAM |
|---|---|---|---|---|---|
| A: table | 6 | 796 | 139 | 5 | 0 |
| B: CORDIC | 20 | 2,514 | 1,926 | 0 | 0 |

LUT counts include inverter cells (7 and 123) and exclude shift-register LUTs (6 and 4).

At one sample per clock, the multiplier-free CORDIC uses 3.2 times the LUTs and 14 times the flip-flops
of the table design. Each of its eighteen stages holds four 28-bit adder/subtractors and their registers.
The flip-flop ratio overstates the difference. Part of design A's pipeline sits in the internal
registers of its five DSP slices. These serve the two squares, the interpolation and the two final
products.

CORDIC is the better choice when DSP slices are the scarce resource, as on small devices or in designs
with many filters. An iterative CORDIC, one stage reused eighteen times, would be much smaller at an
eighteenth of the throughput. The comparison also says nothing about the clock rate. Each CORDIC stage is
a single 28-bit carry chain and will likely reach a higher Fmax than the multiply-add stages of design A.

## Limitations

The resource figures come from Yosys, not from Vivado, and include no timing. Vivado may also place the
384-entry table in block RAM rather than LUTs. In design A, the clock rate is most likely limited by
the single-cycle multiply-add, the leading-zero count with its barrel shift, or the rounding shift. In design B, they are the normalisation and pre-rotation stage and the
output stage. The HLS code was verified in C simulation only and not synthesised, so no C/RTL
co-simulation was run. The RTL was simulated on 100,015 vectors; only the fixed-point models were checked
over all $2^{32}$ inputs.

## Summary

The FPGA version needed an error budget and two approximations of a reciprocal square root. It needed a
normalisation that both architectures depend on. The fixed-point golden models were checked exhaustively,
and both RTL designs were verified bit-accurate to them. Both designs keep the worst-case error below
0.8 LSB over all inputs. The table design does it with a third of the LUTs, at the cost of five DSP
slices. The code, models and testbenches are on [GitHub](https://github.com/kostisdov/dsp-to-silicon).

## References

[1] J. E. Volder, "The CORDIC trigonometric computing technique," *IRE Transactions on Electronic
Computers*, vol. EC-8, no. 3, pp. 330–334, 1959.

[2] R. Andraka, "A survey of CORDIC algorithms for FPGA based computers," in *Proc. ACM/SIGDA
International Symposium on FPGAs*, 1998, pp. 191–200.

[3] J.-M. Muller, *Elementary Functions: Algorithms and Implementation*, 3rd ed. Boston, MA, USA:
Birkhäuser, 2016.

[4] AMD, *Vitis High-Level Synthesis User Guide*, UG1399, accessed October 2026.

[5] cocotb, a coroutine-based cosimulation library for writing testbenches in Python,
https://www.cocotb.org.

[6] C. Wolf, *Yosys Open SYnthesis Suite*, https://yosyshq.net/yosys/.
