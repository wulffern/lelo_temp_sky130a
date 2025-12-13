
Bandgap (LEOTEMP\_BIAS\_IPB) is used to provide a PTAT current for the frequency
conversion and the comparator. The VD is the CTAT diode voltage in the bandgap.
The output current is approximately 1 uA.

The current charges the capacitor. When the voltage on the capacitor reaches $V_C$
the comparator will trigger (low to high).

The two comparators alternate to trigger the set/reset latch made by the NOR
gates. As such, the two capacitors are alternatively charged.

The output frequency can be calculated from the voltage/current relationship of
a capacitor. 

$$ I = C \frac{dV}{dt}  \Rightarrow f = \frac{2}{dt} = 2\frac{I}{C dV} $$

From the bandgap documentation we can find the current.

$$ f_{OSC} = \frac{2}{RC} \frac{\Delta V}{V_C} $$

The $\Delta V$ increases with temperature and $V_C$ decreases with temperature,
turns out the $\Delta V$ increases faster than $V_C$ drops, so the overall
gradient is positive.

| Temperature [C]           | -40  | 25 | 125 |
|---------------------------|------|----|-----|
| Estimated frequency [MHz] | 2.16 | 3  | 4.8 |





