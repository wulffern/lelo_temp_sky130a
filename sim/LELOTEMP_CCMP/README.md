LELOTEMP_CCMP, the timing element of the LELO_TEMP relaxation
oscillator: the comparator plus its five MIM caps and reset device,
simulated with the bias block replaced by ideal current sources.


#### Integrating half cycle (tran)

Release the reset, let ibias charge the cap, and wait for CMPO to
trip as the ramp passes VC. t_half is one half period of the
oscillator; c_eff is the integrating capacitance back-calculated
from the ramp it actually produced; t_delay and v_over are the
comparator's contribution, and should agree with the LELOTEMP_CMP
transient testbench.



|**Name**|**Parameter**|**Description**| |**Min**|**Typ**|**Max**| Unit|
|:---|:---|:---|---:|:---:|:---:|:---:| ---:|
||**t\_half** |Half period, reset release to comparator trip| **Spec**  | **100.000** | **218.000** | **340.000** | **ns** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 217.798 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|187.791 | 218.470 | 248.961 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|202.402 | 216.716 | 231.030 | |
||**freq** |Equivalent oscillator frequency if both halves match| **Spec**  | **1.500** | **2.300** | **4.800** | **MHz** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 2.296 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|2.008 | 2.289 | 2.663 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|2.156 | 2.308 | 2.460 | |
||**t\_delay** |Comparator delay from the ramp crossing VC to CMPO rising| **Spec**  | **-20.000** | **4.600** | **20.000** | **ns** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 4.600 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|3.481 | 4.629 | 9.385 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|-11.299 | 3.485 | 18.269 | |
||**v\_over** |Ramp overshoot past VC caused by the comparator delay| **Spec**  | **-80.000** | **17.000** | **80.000** | **mV** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 16.802 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|12.741 | 17.565 | 34.287 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|-41.248 | 12.755 | 66.758 | |
||**v\_reset** |Residual level on the integrating node while RST is high| **Spec**  | **-5.000** | **2.000** | **20.000** | **mV** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 1.977 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|1.638 | 1.997 | 2.504 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|1.958 | 1.976 | 1.994 | |
||**c\_eff** |Effective integrating capacitance, back-calculated from the ramp| **Spec**  | **200.000** | **285.000** | **380.000** | **fF** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 285.015 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|245.293 | 284.943 | 324.534 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|283.261 | 285.059 | 286.857 | |
||**idd\_avg** |Average supply current including both injected bias legs| **Spec**  | **5.000** | **16.800** | **40.000** | **uA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 16.754 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|11.122 | 16.774 | 20.430 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|14.506 | 16.677 | 18.849 | |

