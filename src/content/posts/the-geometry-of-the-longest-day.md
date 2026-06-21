---
title: "The geometry of the longest day"
description: "The summer solstice is the extremum of a deterministic signal: the Sun's apparent annual motion. The same spherical geometry that fixes the longest day also explains why, near it, the Sun appears to stand still, and why clock time and sundial time diverge."
date: 2026-06-21
tags: ["physics", "astronomy"]
---

The apparent motion of the Sun across a year is a deterministic, quasi-periodic signal. Its
position is set not by chance but by two fixed geometric facts: the tilt of Earth's rotation
axis relative to the plane of its orbit, and the eccentricity of that orbit. The summer
solstice is not an event so much as an extremum of this signal, the instant at which one of
its components reaches a turning point. The geometry that locates that extremum also fixes the
length of the day at every latitude, explains the origin of the word solstice, and accounts
for the discrepancy between the time told by a clock and the time told by a sundial.

## Declination: the Sun's signed height

It helps to picture the sky as the inside of a vast dome, the celestial sphere, with the stars
fixed to it and the Sun sliding slowly across it over the year. A point on this dome is located
by two angles, much as a point on Earth is located by latitude and longitude. The one that
matters here is the declination $\delta$, the angle of the Sun north (positive) or south
(negative) of the celestial equator, which is simply Earth's equator projected outward onto the
sky. Declination is, in effect, the Sun's latitude. When it is high the Sun climbs higher at
noon and lingers longer above the horizon, the everyday signature of summer; when it is low the
days are short and the Sun stays low, which is winter. Its rise and fall over the year is the
quantity to track.

Earth's axis does not stand upright in its orbit but leans over by the obliquity of the
ecliptic, $\varepsilon \approx 23.44^\circ$. This single tilt is what produces the seasons. As
Earth proceeds along its orbit, the Sun appears to move once around a great circle, the
ecliptic (the yearly path the Sun traces against the background stars), inclined by
$\varepsilon$ to the celestial equator.
Parametrizing the Sun's progress by its ecliptic longitude $\lambda$, measured from the vernal
equinox, spherical trigonometry gives the declination directly [1]:

$$
\sin\delta = \sin\varepsilon \, \sin\lambda .
$$

At the equinoxes ($\lambda = 0^\circ$ and $180^\circ$) the declination is zero; the Sun lies
on the celestial equator. At the June solstice ($\lambda = 90^\circ$) the right-hand side is
maximal, so $\delta = +\varepsilon$, and six months later, at the December solstice, it
reaches $\delta = -\varepsilon$. The declination therefore oscillates between $\pm\varepsilon$
with a one-year period, and the solstices are precisely its extrema.

<figure>
<img src="/posts/solstice/declination-geometry.svg" alt="Schematic of the celestial sphere: the equator and the tilted ecliptic crossing at the equinoxes, with the Sun at the June solstice." />
<figcaption>Fig. 1: The celestial sphere viewed obliquely. The Sun travels once a year around the ecliptic (red), tilted by the obliquity ε from the celestial equator (grey); the two cross at the equinoxes, where the declination is zero. The declination δ is the Sun's angular height above the equator, and it reaches its extreme values of +ε at the June solstice and −ε at the December solstice.</figcaption>
</figure>

<figure>
<img src="/posts/solstice/declination.svg" alt="Solar declination over the year, a smooth oscillation between plus and minus the obliquity." />
<figcaption>Fig. 2: Solar declination δ through the year. It oscillates between +ε and −ε, with the equinoxes at the zero crossings; the June solstice (dashed) is the maximum, where the curve flattens.</figcaption>
</figure>

Treating $\lambda$ as advancing uniformly in time, an adequate approximation for a nearly
circular orbit, makes the declination a smooth, regular rise and fall over the year [2]. The
small departures from that smoothness are exactly what the later sections draw on.

## The length of the day

Declination is not merely a coordinate; through one more application of spherical geometry it
fixes how long the Sun stays above the horizon. For an observer at geographic latitude
$\varphi$, the Sun rises and sets when its altitude is zero, which occurs at the hour angle
$H_0$ satisfying [1]

$$
\cos H_0 = -\tan\varphi \, \tan\delta .
$$

The hour angle is just a way of measuring time as an angle: it counts how far the Sun has moved
from the overhead meridian as the Earth turns, at the steady rate of $15^\circ$ per hour
(a full $360^\circ$ turn in $24$ hours). The Sun stands above the horizon for the arc from
$-H_0$ before noon to $+H_0$ after it, so the length of the day in hours is

$$
D = \frac{2 H_0}{15^\circ} = \frac{2}{15^\circ}\arccos\!\big(-\tan\varphi\,\tan\delta\big).
$$

At the equinoxes $\delta = 0$, giving $\cos H_0 = 0$, hence $H_0 = 90^\circ$ and $D = 12$ hours
at every latitude. Away from the equinoxes the day length depends on the sign of the product
$\tan\varphi\,\tan\delta$: in the northern hemisphere ($\varphi > 0$) a positive declination
lengthens the day, and the longest day occurs exactly when $\delta$ is greatest, at the June
solstice. For Athens ($\varphi \approx 38^\circ$N) the solstice declination
$\delta = \varepsilon$ gives $\cos H_0 = -\tan 38^\circ \tan 23.44^\circ \approx -0.339$, so
$H_0 \approx 109.8^\circ$ and $D \approx 14$ h $38$ min.

<figure>
<img src="/posts/solstice/daylight.svg" alt="Length of daylight through the year at the equator, Athens, and 60 degrees north." />
<figcaption>Fig. 3: Length of daylight through the year at three latitudes. All curves cross 12 hours at the equinoxes and reach their northern-hemisphere maximum at the June solstice (dashed); the amplitude grows with latitude, and the maximum is visibly flat.</figcaption>
</figure>

When $|\tan\varphi\,\tan\delta| > 1$ the equation for $H_0$ has no solution: the argument of
the arccosine leaves $[-1, 1]$, and the Sun either never sets or never rises. This first
happens at the polar circles, $\varphi = 90^\circ - \varepsilon \approx 66.6^\circ$, on the
solstice, the geometric definition of the midnight Sun.

## Why the Sun stands still

The word solstice derives from the Latin *sol* (sun) and *sistere* (to stand still). The name
records an observation: near the solstice the Sun's daily extreme height changes
imperceptibly from one day to the next, and the length of the day is nearly constant. This is
a direct consequence of $\delta$ being at an extremum, and it is worth making quantitative,
because an extremum is a point of vanishing first derivative.

Differentiating $\sin\delta = \sin\varepsilon\,\sin\lambda$ with respect to $\lambda$ (in
radians, as differentiation of a sine requires) gives

$$
\frac{d\delta}{d\lambda} = \frac{\sin\varepsilon\,\cos\lambda}{\cos\delta}.
$$

At the solstice $\lambda = 90^\circ$, so $\cos\lambda = 0$ and $d\delta/d\lambda = 0$: the
declination is stationary. To leading order the approach to the extremum is quadratic. Writing
$\lambda = 90^\circ + u$ and expanding, $\sin\lambda = \cos u \approx 1 - u^2/2$, so the
declination falls below its peak by an amount of order $u^2$. A week on either side of the
solstice corresponds to $u \approx 6.9^\circ$, about $0.12$ radians, of ecliptic longitude,
which (using the radian value in the expansion) lowers the declination from $23.44^\circ$ to
about $23.26^\circ$, a change of under a fifth of a degree.
Propagated through the day-length formula at the latitude of Athens, the longest day and the
day a week before or after it differ by roughly one minute. The Sun does not literally stand
still, but the rate of change of its declination passes through zero, and the length of the
day is, to first order, flat across the surrounding weeks. The flat tops of the curves in
Fig. 3 are this stationarity made visible.

## The equation of time: when clocks and sundials disagree

The signal analysed so far has been the declination, the Sun's north-south motion. Its
east-west motion carries a second, subtler structure. Mean solar time, the time kept by a
clock, advances as though the Sun crossed the meridian at a perfectly uniform rate. The true
Sun does not. The difference between apparent solar time (a sundial) and mean solar time is
the equation of time, and over a year it ranges from about $-14$ to $+16$ minutes.

It splits into two contributions of comparable size but different period [3]. The first is the
obliquity. Even if Earth's orbit were a perfect circle, traversed at
constant angular speed along the ecliptic, projecting that uniform motion onto the celestial
equator (where time is measured) would not be uniform, because the ecliptic is tilted. This
projection introduces a component with a period of six months. The second is the eccentricity:
Earth's orbit is an ellipse, and by Kepler's second law the planet moves faster near
perihelion (early January) than near aphelion, so the Sun's apparent motion speeds up and
slows down once per year. This component has a period of one year.

Written out, with $N$ the day of the year, the two add to a compact approximation:

$$
E(t) \approx \underbrace{A_2 \sin 2\beta}_{\text{obliquity}} \; + \;
\underbrace{A_1 \sin(\beta + \phi_1)}_{\text{eccentricity}},
\qquad \beta = \frac{2\pi (N - 81)}{365},
$$

where the obliquity term has amplitude $A_2 \approx 9.9$ minutes and the eccentricity term
$A_1 \approx 7.7$ minutes. Each on its own is a smooth, symmetric wobble; because the two repeat
at different rates they drift in and out of step, reinforcing here and partly cancelling there,
and that is what gives the full curve its lopsided shape, dipping and peaking by different
amounts.

<figure>
<img src="/posts/solstice/equation-of-time.svg" alt="The equation of time decomposed into a semiannual obliquity component, an annual eccentricity component, and their sum." />
<figcaption>Fig. 4: The equation of time (solid) as the sum of a twice-yearly obliquity term (dashed) and a once-yearly eccentricity term (dotted). The two are of comparable size; adding them produces the lopsided annual curve.</figcaption>
</figure>

## The analemma

The two motions can be displayed together. Photographing the Sun from a fixed location at the
same clock time on many days through the year, or simply plotting declination against the
equation of time, traces a closed figure-eight, the analemma [4]. Its height is the Sun's
north-south swing, from $+\varepsilon$ at the top to $-\varepsilon$ at the bottom; its width is
the half-hour spread of the equation of time. The vertical motion repeats just once a year,
while the sideways motion repeats partly twice a year, and a slow up-and-down combined with a
faster side-to-side is exactly what draws a figure-eight. The two loops come out unequal
because the once- and twice-yearly contributions to the sideways motion are differently timed,
the same lopsidedness already seen in Fig. 4.

<figure>
<img src="/posts/solstice/analemma.svg" alt="The analemma, a figure-eight of declination plotted against the equation of time, with solstices and equinoxes marked." />
<figcaption>Fig. 5: The analemma, declination plotted against the equation of time over a year. The solstices sit at the top and bottom, the equinoxes near the crossing; the larger lower lobe corresponds to the months around perihelion.</figcaption>
</figure>

The solstice occupies the top of the figure, the single point where the upper loop turns over.
That turning point is the same stationarity established earlier: it is where $d\delta/d\lambda$
vanishes, and it is the longest day.

## A signal like any other

The longest day is the visible consequence of a small number of geometric constants: an axial
tilt of $23.44^\circ$, an orbital eccentricity of a few percent, and the spherical
trigonometry that connects them to the horizon. Declination, day length, the equation of time,
and the analemma are not separate phenomena but different projections of one deterministic
signal, and the methods that make sense of them, finding a peak by asking where a rate of
change vanishes, or splitting a complicated curve into a few simple repeating pieces, are the
same ones used to read any other. A radio antenna, a beating heart, and the turning sky give
off signals of utterly different origin, yet the same handful of methods reads them all; the
mathematics does not care where the pattern comes from.

## References

[1] W. M. Smart, *Textbook on Spherical Astronomy*, 6th ed. Cambridge University Press, 1977.

[2] P. I. Cooper, "The absorption of radiation in solar stills," *Solar Energy*, vol. 12,
no. 3, pp. 333–346, 1969.

[3] M. Müller, "Equation of time: problem in astronomy," *Acta Physica Polonica A*, vol. 88,
supplement, pp. S-49–S-66, 1995.

[4] J. Meeus, *Astronomical Algorithms*, 2nd ed. Willmann-Bell, 1998.
