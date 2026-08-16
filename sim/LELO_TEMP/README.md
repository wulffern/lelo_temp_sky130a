LELO_TEMP

#### Temperature sensor (tran)

Check temperature accuracy

The Sch rows are the schematic netlist, the Lay rows the parasitic
extraction of the finished layout. Lay is typical process only:
the extracted netlist carries the full parasitic capacitance, and
the whole corner matrix on it is not worth the runtime while the
Sch corners already bound the process spread.



|**Name**|**Parameter**|**Description**| |**Min**|**Typ**|**Max**| Unit|
|:---|:---|:---|---:|:---:|:---:|:---:| ---:|
||**idd\_25** || **Spec**  | **5.000** | **30.000** | **100.000** | **uA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 84.387 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|64.320 | 84.426 | <span style='color:red'>**107.774**</span> | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|73.500 | 83.903 | 94.306 | |
| | | |<a href='results/tran_Lay_typical.html'>Lay_typ</a>| | 83.073 |  | |
| | | |<a href='results/tran_Lay_supply.html'>Lay_supply</a>|76.911 | 83.073 | 88.967 | |
||**iddq\_25** || **Spec**  | **0.000** | **10.000** | **50.000** | **nA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 7.140 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|6.943 | 7.488 | 46.459 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|6.872 | 7.148 | 7.424 | |
| | | |<a href='results/tran_Lay_typical.html'>Lay_typ</a>| | 11.061 |  | |
| | | |<a href='results/tran_Lay_supply.html'>Lay_supply</a>|10.164 | 11.061 | 11.753 | |
||**ind\_1p\_max** |Industrial 1 point calibration| **Spec**  | **-15.000** | **0.000** | **15.000** | **C** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 3.686 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|2.274 | 3.747 | 12.542 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|-2.193 | 4.196 | 10.584 | |
| | | |<a href='results/tran_Lay_typical.html'>Lay_typ</a>| | 11.241 |  | |
| | | |<a href='results/tran_Lay_supply.html'>Lay_supply</a>|11.184 | 11.197 | 11.241 | |
||**ind\_1p\_min** |Industrial 1 point calibration| **Spec**  | **-15.000** | **0.000** | **15.000** | **C** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | -0.372 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|-8.457 | -5.056 | 0.250 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|-3.057 | -0.772 | 1.513 | |
| | | |<a href='results/tran_Lay_typical.html'>Lay_typ</a>| | -8.171 |  | |
| | | |<a href='results/tran_Lay_supply.html'>Lay_supply</a>|-8.529 | -8.171 | -7.681 | |
||**ind\_2p\_max** |Industrial 2 point calibration| **Spec**  | **-10.000** | **0.000** | **10.000** | **C** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 3.584 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|-0.139 | 3.392 | 6.364 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|-1.739 | 3.440 | 8.620 | |
| | | |<a href='results/tran_Lay_typical.html'>Lay_typ</a>| | 5.706 |  | |
| | | |<a href='results/tran_Lay_supply.html'>Lay_supply</a>|5.643 | 5.657 | 5.706 | |
||**ind\_2p\_min** |Industrial 2 point calibration| **Spec**  | **-10.000** | **0.000** | **10.000** | **C** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | -0.327 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|-5.069 | -0.768 | 0.112 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|-0.819 | -0.390 | 0.040 | |
| | | |<a href='results/tran_Lay_typical.html'>Lay_typ</a>| | -0.584 |  | |
| | | |<a href='results/tran_Lay_supply.html'>Lay_supply</a>|-1.022 | -0.584 | -0.271 | |
||**com\_1p\_max** |Commercial 1 point calibration| **Spec**  | **-10.000** | **0.000** | **10.000** | **C** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 0.917 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|0.430 | 2.704 | 4.272 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|-0.480 | 1.353 | 3.186 | |
| | | |<a href='results/tran_Lay_typical.html'>Lay_typ</a>| | 3.686 |  | |
| | | |<a href='results/tran_Lay_supply.html'>Lay_supply</a>|3.482 | 3.686 | 3.826 | |
||**com\_1p\_min** |Commercial 1 point calibration| **Spec**  | **-10.000** | **0.000** | **10.000** | **C** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | -0.372 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|-5.760 | -1.970 | 0.250 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|-2.719 | -0.669 | 1.382 | |
| | | |<a href='results/tran_Lay_typical.html'>Lay_typ</a>| | -4.582 |  | |
| | | |<a href='results/tran_Lay_supply.html'>Lay_supply</a>|-4.977 | -4.582 | -4.319 | |
||**com\_2p\_max** |Commercial 2 point calibration| **Spec**  | **-5.000** | **0.000** | **5.000** | **C** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 0.877 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|-0.139 | 0.990 | 1.868 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|-0.510 | 0.861 | 2.231 | |
| | | |<a href='results/tran_Lay_typical.html'>Lay_typ</a>| | 1.491 |  | |
| | | |<a href='results/tran_Lay_supply.html'>Lay_supply</a>|1.267 | 1.491 | 1.646 | |
||**com\_2p\_min** |Commercial 2 point calibration| **Spec**  | **-5.000** | **0.000** | **5.000** | **C** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | -0.327 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|-1.173 | -0.687 | 0.179 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|-0.862 | -0.308 | 0.245 | |
| | | |<a href='results/tran_Lay_typical.html'>Lay_typ</a>| | -0.584 |  | |
| | | |<a href='results/tran_Lay_supply.html'>Lay_supply</a>|-1.022 | -0.584 | -0.271 | |
||**freq\_min** |Frequency| **Spec**  | **1.500** | **3.000** | **4.800** | **MHz** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 1.700 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|<span style='color:red'>**1.345**</span> | 1.700 | 2.207 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|<span style='color:red'>**1.277**</span> | 1.643 | 2.009 | |
| | | |<a href='results/tran_Lay_typical.html'>Lay_typ</a>| | <span style='color:red'>**1.402**</span> |  | |
| | | |<a href='results/tran_Lay_supply.html'>Lay_supply</a>|<span style='color:red'>**1.401**</span> | <span style='color:red'>**1.401**</span> | <span style='color:red'>**1.402**</span> | |
||**freq\_max** |Frequency| **Spec**  | **1.500** | **3.000** | **4.800** | **MHz** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 3.895 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|3.081 | 3.891 | <span style='color:orange'>**5.027**</span> | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|3.229 | 3.829 | 4.430 | |
| | | |<a href='results/tran_Lay_typical.html'>Lay_typ</a>| | 3.184 |  | |
| | | |<a href='results/tran_Lay_supply.html'>Lay_supply</a>|3.179 | 3.184 | 3.191 | |
||**FOM** |Figure Of Merit| **Spec**  | **10.000** | **40.000** | **400.000** | **nAK** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 39.619 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|26.409 | 56.920 | 100.304 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|<span style='color:red'>**-22.911**</span> | 37.986 | 98.882 | |
| | | |<a href='results/tran_Lay_typical.html'>Lay_typ</a>| | 75.563 |  | |
| | | |<a href='results/tran_Lay_supply.html'>Lay_supply</a>|64.467 | 75.563 | 89.063 | |

