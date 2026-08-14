

The timing element of the oscillator. One 1U current from the bandgap charges a
capacitor, and LELOTEMP\_CMP triggers when the capacitor reaches $V_C$. Two of
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
order effect. That is why this block is simulated on its own in
sim/LELOTEMP\_CCMP, with the bandgap replaced by ideal 1 uA sources: it
separates the capacitor and the comparator from the current that drives them.

Simulated values at 27 C, typical process:

| View | C_eff [fF] | t_half [ns] | t_d [ns] |
|------|------------|-------------|----------|
| Sch  | 285        | 217.8       | 4.6      |
| Lay  | 316        | 247.9       | 11.7     |

$C_{eff}$ is back calculated from the ramp the circuit actually produced rather
than from the unit cell, so it includes the wiring on the node. The extracted
view adds about 11% to it and roughly doubles the comparator delay, and those
two together are the 14% longer half period.
