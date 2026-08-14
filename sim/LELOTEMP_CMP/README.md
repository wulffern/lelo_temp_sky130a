LELOTEMP_CMP, the comparator of the LELO_TEMP relaxation oscillator,
simulated on its own with the bias block replaced by ideal current
sources.


#### DC transfer (dc)

Sweep VIP with VIN held at the nominal threshold. Gives the trip
point, the input referred offset and the small signal gain. The
mismatch run is the one that matters: random offset here is a
threshold error the one point calibration has to absorb.



|**Name**|**Parameter**|**Description**| |**Min**|**Typ**|**Max**| Unit|
|:---|:---|:---|---:|:---:|:---:|:---:| ---:|
||**voffset** |Input referred offset at the trip point| **Spec**  | **-50.00** | **0.00** | **50.00** | **mV** |
| | | |<a href='results/dc_Sch_typical.html'>Sch_typ</a>| | 2.45 |  | |
| | | |<a href='results/dc_Sch_etc.html'>Sch_etc</a>|0.89 | 2.59 | 4.14 | |
| | | |<a href='results/dc_Sch_mc.html'>Sch_3std</a>|<span style='color:red'>**-50.31**</span> | -3.97 | 42.36 | |
||**vtrip** |Input voltage at which VO crosses its own midpoint| **Spec**  | **0.6000** | **0.7500** | **0.9000** | **V** |
| | | |<a href='results/dc_Sch_typical.html'>Sch_typ</a>| | 0.7524 |  | |
| | | |<a href='results/dc_Sch_etc.html'>Sch_etc</a>|0.7509 | 0.7526 | 0.7541 | |
| | | |<a href='results/dc_Sch_mc.html'>Sch_3std</a>|0.6997 | 0.7460 | 0.7924 | |
||**gain** |Small signal gain dVO/dVIP at the trip point| **Spec**  | **50.0** | **600.0** | **5000.0** | **V/V** |
| | | |<a href='results/dc_Sch_typical.html'>Sch_typ</a>| | 627.6 |  | |
| | | |<a href='results/dc_Sch_etc.html'>Sch_etc</a>|487.2 | 588.2 | 696.9 | |
| | | |<a href='results/dc_Sch_mc.html'>Sch_3std</a>|570.6 | 618.7 | 666.8 | |
||**vo\_low** |Output low level| **Spec**  | **-0.0500** | **0.0000** | **0.2000** | **V** |
| | | |<a href='results/dc_Sch_typical.html'>Sch_typ</a>| | -0.0004 |  | |
| | | |<a href='results/dc_Sch_etc.html'>Sch_etc</a>|-0.0019 | -0.0004 | -0.0001 | |
| | | |<a href='results/dc_Sch_mc.html'>Sch_3std</a>|-0.0005 | -0.0004 | -0.0003 | |
||**vo\_high** |Output high level| **Spec**  | **1.5000** | **1.8000** | **2.0000** | **V** |
| | | |<a href='results/dc_Sch_typical.html'>Sch_typ</a>| | 1.8000 |  | |
| | | |<a href='results/dc_Sch_etc.html'>Sch_etc</a>|1.7000 | 1.8000 | 1.9000 | |
| | | |<a href='results/dc_Sch_mc.html'>Sch_3std</a>|1.8000 | 1.8000 | 1.8000 | |
||**idd\_hi** |Supply current including the injected bias| **Spec**  | **4.000** | **11.000** | **25.000** | **uA** |
| | | |<a href='results/dc_Sch_typical.html'>Sch_typ</a>| | 11.438 |  | |
| | | |<a href='results/dc_Sch_etc.html'>Sch_etc</a>|6.384 | 11.430 | 16.116 | |
| | | |<a href='results/dc_Sch_mc.html'>Sch_3std</a>|10.010 | 11.475 | 12.941 | |

#### Propagation delay (tran)

VIP driven with a ramp at the slope it really sees in LELOTEMP_CCMP
(ibias into the 5x MIM cap, about 4 V/us). The delay is added to
every half period of the oscillator, so v_overshoot -- the delay
expressed as an input voltage -- is directly comparable to the
offset from the dc testbench.



|**Name**|**Parameter**|**Description**| |**Min**|**Typ**|**Max**| Unit|
|:---|:---|:---|---:|:---:|:---:|:---:| ---:|
||**t\_delay** |Delay from the ramp crossing VC to VO switching| **Spec**  | **-20.000** | **4.500** | **20.000** | **ns** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 4.511 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|3.411 | 4.557 | 9.190 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|-8.810 | 2.881 | 14.573 | |
||**v\_overshoot** |How far past VC the ramp travels before VO responds| **Spec**  | **-80.000** | **18.000** | **80.000** | **mV** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 18.042 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|13.644 | 18.227 | 36.760 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|-35.240 | 11.525 | 58.291 | |
||**t\_rise** |Output 10-90 rise time| **Spec**  | **0.000** | **1.700** | **10.000** | **ns** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 1.669 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|1.635 | 1.782 | 1.899 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|1.506 | 1.679 | 1.852 | |
||**idd\_avg** |Average supply current including the injected bias| **Spec**  | **4.000** | **13.800** | **30.000** | **uA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 13.789 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|8.426 | 13.802 | 17.879 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|11.872 | 13.797 | 15.722 | |

