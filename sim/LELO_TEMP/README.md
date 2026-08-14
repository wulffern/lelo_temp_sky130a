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
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 76.304 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|50.720 | 76.415 | <span style='color:red'>**105.687**</span> | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|66.503 | 75.053 | 83.604 | |
| | | |<a href='results/tran_Lay_typical.html'>Lay_typ</a>| | 75.585 |  | |
| | | |<a href='results/tran_Lay_supply.html'>Lay_supply</a>|64.334 | 75.585 | 85.807 | |
||**iddq\_25** || **Spec**  | **0.000** | **10.000** | **50.000** | **nA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 5.981 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|5.914 | 6.267 | 45.647 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|5.870 | 6.014 | 6.158 | |
| | | |<a href='results/tran_Lay_typical.html'>Lay_typ</a>| | 8.730 |  | |
| | | |<a href='results/tran_Lay_supply.html'>Lay_supply</a>|8.186 | 8.730 | 9.154 | |
||**ind\_1p\_max** |Industrial 1 point calibration| **Spec**  | **-15.000** | **0.000** | **15.000** | **C** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 2.087 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|-0.907 | 2.329 | 7.975 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|-2.308 | 4.140 | 10.589 | |
| | | |<a href='results/tran_Lay_typical.html'>Lay_typ</a>| | 4.400 |  | |
| | | |<a href='results/tran_Lay_supply.html'>Lay_supply</a>|-0.761 | 4.400 | 8.313 | |
||**ind\_1p\_min** |Industrial 1 point calibration| **Spec**  | **-15.000** | **0.000** | **15.000** | **C** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | -3.268 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|<span style='color:red'>**-70.054**</span> | -6.776 | -1.079 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|-14.512 | -4.879 | 4.753 | |
| | | |<a href='results/tran_Lay_typical.html'>Lay_typ</a>| | -6.528 |  | |
| | | |<a href='results/tran_Lay_supply.html'>Lay_supply</a>|<span style='color:red'>**-15.808**</span> | -6.987 | -6.528 | |
||**ind\_2p\_max** |Industrial 2 point calibration| **Spec**  | **-10.000** | **0.000** | **10.000** | **C** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 0.150 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|-0.045 | 1.407 | 4.740 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|-1.667 | 0.673 | 3.014 | |
| | | |<a href='results/tran_Lay_typical.html'>Lay_typ</a>| | 0.898 |  | |
| | | |<a href='results/tran_Lay_supply.html'>Lay_supply</a>|0.735 | 0.898 | 4.211 | |
||**ind\_2p\_min** |Industrial 2 point calibration| **Spec**  | **-10.000** | **0.000** | **10.000** | **C** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | -1.503 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|<span style='color:red'>**-65.339**</span> | -7.051 | -0.398 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|-5.901 | -1.982 | 1.938 | |
| | | |<a href='results/tran_Lay_typical.html'>Lay_typ</a>| | -0.224 |  | |
| | | |<a href='results/tran_Lay_supply.html'>Lay_supply</a>|<span style='color:red'>**-21.655**</span> | -0.393 | -0.224 | |
||**com\_1p\_max** |Commercial 1 point calibration| **Spec**  | **-10.000** | **0.000** | **10.000** | **C** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 1.546 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|-0.907 | 1.975 | 2.923 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|-1.268 | 2.662 | 6.593 | |
| | | |<a href='results/tran_Lay_typical.html'>Lay_typ</a>| | 2.221 |  | |
| | | |<a href='results/tran_Lay_supply.html'>Lay_supply</a>|-0.761 | 2.221 | 3.062 | |
||**com\_1p\_min** |Commercial 1 point calibration| **Spec**  | **-10.000** | **0.000** | **10.000** | **C** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | -0.822 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|-8.434 | -2.859 | 0.011 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|-4.477 | -1.489 | 1.499 | |
| | | |<a href='results/tran_Lay_typical.html'>Lay_typ</a>| | -3.165 |  | |
| | | |<a href='results/tran_Lay_supply.html'>Lay_supply</a>|-3.394 | -3.385 | -3.165 | |
||**com\_2p\_max** |Commercial 2 point calibration| **Spec**  | **-5.000** | **0.000** | **5.000** | **C** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 0.150 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|-0.318 | 0.812 | 1.887 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|-0.207 | 0.377 | 0.960 | |
| | | |<a href='results/tran_Lay_typical.html'>Lay_typ</a>| | 0.573 |  | |
| | | |<a href='results/tran_Lay_supply.html'>Lay_supply</a>|-0.373 | 0.573 | 1.475 | |
||**com\_2p\_min** |Commercial 2 point calibration| **Spec**  | **-5.000** | **0.000** | **5.000** | **C** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | -0.047 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|<span style='color:red'>**-7.267**</span> | -0.807 | 0.080 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|-1.042 | -0.297 | 0.447 | |
| | | |<a href='results/tran_Lay_typical.html'>Lay_typ</a>| | -0.224 |  | |
| | | |<a href='results/tran_Lay_supply.html'>Lay_supply</a>|-2.646 | -0.393 | -0.224 | |
||**freq\_min** |Frequency| **Spec**  | **1.500** | **3.000** | **4.800** | **MHz** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 1.877 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|<span style='color:red'>**1.136**</span> | 1.881 | 2.527 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|<span style='color:orange'>**1.451**</span> | 1.838 | 2.226 | |
| | | |<a href='results/tran_Lay_typical.html'>Lay_typ</a>| | <span style='color:orange'>**1.458**</span> |  | |
| | | |<a href='results/tran_Lay_supply.html'>Lay_supply</a>|<span style='color:red'>**1.249**</span> | <span style='color:orange'>**1.458**</span> | <span style='color:orange'>**1.499**</span> | |
||**freq\_max** |Frequency| **Spec**  | **1.500** | **3.000** | **4.800** | **MHz** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 4.354 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|3.402 | 4.349 | <span style='color:red'>**5.741**</span> | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|3.701 | 4.369 | <span style='color:orange'>**5.036**</span> | |
| | | |<a href='results/tran_Lay_typical.html'>Lay_typ</a>| | 3.395 |  | |
| | | |<a href='results/tran_Lay_supply.html'>Lay_supply</a>|3.387 | 3.395 | 3.402 | |
||**FOM** |Figure Of Merit| **Spec**  | **10.000** | **40.000** | **400.000** | **nAK** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | <span style='color:red'>**5.754**</span> |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|<span style='color:red'>**8.516**</span> | 56.437 | 190.246 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|<span style='color:red'>**-9.296**</span> | 19.448 | 48.193 | |
| | | |<a href='results/tran_Lay_typical.html'>Lay_typ</a>| | 25.339 |  | |
| | | |<a href='results/tran_Lay_supply.html'>Lay_supply</a>|25.339 | 63.221 | 66.004 | |

