

Current mirror OTA, and the amplifier that closes the bandgap loop. It is the
same circuit idea as LELOTEMP\_OTA, rebuilt from the REY\_ATR library. The name
changed because the cells did, not because the function did.

The inputs sit across the two bandgap branches, $V_{R1}$ on VIP and $V_{D1}$ on
VIN, and the output LPO drives the gates of the PMOS current mirror. The loop
settles when the OTA has forced the two branches to the same voltage, which is
what makes $\Delta V$ appear across the resistor between VR1 and VD2.

The bias is a resistor from the tail of the differential pair to VDD, not a
current from the bandgap. Same reason as in the other OTAs: taking the bias
from the loop the OTA is closing complicates startup, and the point of a
resistor here is that the OTA keeps working before the bandgap does. The tail
resistor is four segments of high sheet poly in series, so

$$ I_{TAIL} = \frac{V_{DD} - V_{S}}{4 R_{PPO}} $$

where $V_S$ is the source of the input pair, one $V_{SG}$ above the input
common mode.

The input pair is low threshold PMOS. The inputs are a diode voltage above VSS
and the sources are near VDD, so at the low supply corner the $V_{SG}$ the pair
needs is a large fraction of what the supply has left after the tail resistor
drop. The LVT devices buy that headroom back. This is the part of the circuit
that the 1.7 V corner leans on hardest.

Both branches are loaded with diode connected NMOS, and the two branch voltages
are then mirrored into the output stage: VD1 drives an NMOS into the diode
connected PMOS at VBP, and VD2 drives an NMOS at VO against the PMOS mirrored
from VBP. The gain is therefore taken in the second stage rather than at the
drains of the input pair.

The output is pulled high in power down, so that the PMOS current mirror in the
bandgap is turned off. VD1, VD2 and VD3 are pulled to VSS, and the tail switch
between VDD and the resistor is opened, so no current flows.

The circuit on the right side generates the VCP cascode bias for the main
bandgap, from a replica input pair into a diode connected NMOS at VD3 and a
series PMOS string down from VDD.
