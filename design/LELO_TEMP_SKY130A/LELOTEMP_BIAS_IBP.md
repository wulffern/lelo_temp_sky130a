

Bandgap core. The voltage across the resistor between VR1 and VD2 will be

$$ \Delta V = V_{R1} - V_{D2} = \frac{k T}{q} ln(8 \times 8) $$

since there is a 1-to-8 ratio between the bipolars, and a 1-to-8 ratio in the
current mirror.

The current in the resistor will be

$$ I_{R} = \frac{\Delta V}{(4 + 8) \times RPPO}$$

Where $RPPO$ is the unit resistor, nominally 7.53 k $\Omega$.

The startup circuit on the left side will ensure that the LPI node is pulled
down when the circuit starts up. The PWRUP will enable the NMOS between LPI and
VS2. The diode connected NMOS between VS1 and VS2 lmits the current.  The PMOS
will eventually turn off the startup path when VR1 is high enough.

