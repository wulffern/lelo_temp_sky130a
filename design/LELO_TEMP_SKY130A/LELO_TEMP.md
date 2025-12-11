
Bandgap (LEOTEMP\_BIAS\_IPB) is used to provide a PTAT current for the frequency
conversion and the comparator. The VD is the CTAT diode voltage in the bandgap.
The output current is approximately 1 uA.

The current charges the capacitor. When the voltage on the capacitor reaches VC
the comparator will trigger (low to high).

The CPMO is delayed through an inverter chain, and is fed to the RST of the
capacitor. The loop delay of comparator and inverters result in a short reset
pulse.

The reset pulse is also used for a divide-by-two circuit with the flip flop. An
inverter is used from the Q output to the D input to ensure the hold time is not
violated.

The output frequency can be calculated from the voltage/current relationship of
a capacitor. 

$$ I = C \frac{dV}{dt}  \Rightarrow f = \frac{1}{dt} = \frac{I}{C dV} $$

From the bandgap documentation we can find the current.

$$ f_{OSC} = \frac{kT}{q} ln(64) \frac{1}{R C VC} $$

The CTAT voltage will have a slope of approximately 

$$ \frac{d VC}{dT} = -3\frac{k}{q}ln(T)  = 1.5\text{ mV }$$

