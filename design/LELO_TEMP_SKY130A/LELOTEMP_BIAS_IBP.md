

Bandgap core. The voltage across the resistor between VR1 and VD2 will be

$$ \Delta V = V_{R1} - V_{D2} = \frac{k T}{q} ln(8 \times 8) $$

since there is a 1-to-8 ratio between the bipolars, and a 1-to-8 ratio in the
current mirror.

The current in the resistor will be

$$ I_{R} = \frac{\Delta V}{(4 + 8) \times RPPO}$$

Where $RPPO$ is the unit resistor.

The $V_C$ is a bit more complicated, but can be calculated to be 

$$ V_C = \frac{kT}{q}(\ell  - 3 \ln T) + V_G $$ 

where

$$ \ell= \ln{I_D} - \ln{\left (Aq\frac{D_n}{L_n N_A} +
\frac{D_p}{L_p N_D}\right)}  - 2 \ln{\sqrt{B_c B_v}} $$

where $A$ is the area of the diode, $I_D$ the current in the diode, $D_n,D_p$ are the diffusion constants for
electrons and holes. $L_n,L_p$ are the diffusion lengths, $N_A,N_D$ are the
acceptor and donor concentration.  and $B_c,B_v$ are

$$ B_c = 2 \left[\frac{2 \pi  k m_n^*}{h^2}\right]^{3/2} \text{  } B_v = 2
\left[\frac{2 \pi  k m_p^*}{h^2}\right]^{3/2} $$

where $m_n,m_p$ are the effective mass of electrons and holes and $h$ is
Planck's constant.

Obviously. 

Not really. 

But it is understandable. 

See [Diodes](https://analogicus.com/aic2026/2024/10/25/Diodes.html#forward-voltage-temperature-dependence)

Estimated values from the model in [LELO\_TEMP.py](py/LELO_TEMP.py) are shown in table below.


| Temperature [C] | Current [uA] | Vc [V] | DeltaV [mV] |
|-----------------|--------------|--------|-------------|
| -40             | 0.902        | 0.8386 | 83.6        |
| 25              | 1.133        | 0.7412 | 106.9       |
| 125             | 1.470        | 0.5844 | 142.7       |

The table was generated from [model.ipynb](model.ipynb)

The startup circuit on the left side will ensure that the LPI node is pulled
down when the circuit starts up. The PWRUP will enable the NMOS between LPI and
VS2. The diode connected NMOS between VS1 and VS2 lmits the current.  The PMOS
will eventually turn off the startup path when VR1 is high enough.

The diode connected transistor on the right side is to clamp the voltage between
VR1 and VD2. If the current is too high, then a high voltage on VR1 can turn off
the PMOS in the OTA, and increase settling time.

