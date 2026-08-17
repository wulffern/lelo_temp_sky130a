
The timing element of the oscillator. One 1U current from the bandgap charges a
capacitor, and LELOTEMP\_CMPR triggers when the capacitor reaches $V_C$. Two of
these alternate through the set/reset latch in LELO\_TEMP, so each one produces
half a period.

The bias input `IBP_1U<0>` is also the integrating node. There is no separate
input pin for the ramp: the current arrives on the same wire that the
capacitors and the comparator input hang on. `IBP_1U<1>` is the comparator's
own bias.

The capacitor is five MIM unit cells. The NMOS gated by RST discharges the node
between cycles, and a second NMOS gated by PWRUP\_N holds it down in power
down, so the oscillator starts from a known state rather than from whatever
charge was left on the plate.

The half period follows from the capacitor relationship,

$$ dt = C \frac{V_C}{I} $$

but the comparator does not switch at the instant the ramp reaches $V_C$. Its
delay $t_d$ lets the ramp continue past the threshold, and that adds to every
half period,

$$ t_{HALF} = C \frac{V_C}{I} + t_d $$

so a delay that drifts over temperature is a temperature error, not a second
order effect.

The integrating node also carries the bandgap-to-pair distribution wire, which
crosses the whole tile, so $C$ is more than the five unit cells: the effective
capacitance fitted from the typical top-level runs is 319 fF (Sch) and 385 fF
(Lay) -- see `FIT` in
[LELO\_TEMP.py](https://github.com/wulffern/lelo_temp_sky130a/blob/main/py/LELO_TEMP.py).
