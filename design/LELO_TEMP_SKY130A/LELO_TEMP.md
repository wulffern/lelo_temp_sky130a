
Bandgap (LEOTEMP\_BIAS\_IPB) is used to provide a PTAT current for the frequency
conversion and the comparator. The $V_C$ is the CTAT diode voltage in the bandgap.
The output current is approximately 1 uA.

The current charges the capacitor inside CCMP. When the voltage on the capacitor reaches $V_C$
the comparator inside CCMP will trigger (low to high).

The two comparators alternate to trigger the set/reset latch made by the NOR
gates. As such, the two capacitors are alternatively charged.

The output frequency can be calculated from the voltage/current relationship of
a capacitor. 

A single charge cycle is given by 

$$ I = C \frac{dV}{dt}  \Rightarrow dt = C \frac{V_C}{I} $$

Inserting for the bandgap current ($I_R$)

$$ dt = RC \frac{V_C}{\Delta V} $$

As such, the frequency will be 

$$ f_{OSC} = \frac{1}{2 dt} = \frac{1}{2RC} \frac{\Delta V}{V_C} $$

The $\Delta V$ increases with temperature and $V_C$ decreases with temperature,
turns out the $\Delta V$ increases faster than $V_C$ drops, so the overall
gradient is positive.

The estimated frequency is shown in the table below (the table was generated from [model.ipynb](model.ipynb)))

| Temperature [C] | Frequency [MHz] |
|-----------------|-----------------|
| -40             | 1.681           |
| 25              | 2.406           |
| 125             | 3.954           |
|                 |                 |

| Temperature [C]           | -40  | 25 | 125 |
|---------------------------|------|----|-----|
| Estimated frequency [MHz] | 2.16 | 3  | 4.8 |





