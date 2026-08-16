LELO_TEMP

#### Temperature sensor (tran)

Check temperature accuracy

The Sch rows are the schematic netlist, the Lay rows the parasitic
extraction of the finished layout. Both views run the same sets:
typical, the extreme test condition corners (etc) and mismatch
(mc). Calibration is per corner at Vt (process); the supply
corners reuse their process corner's calibration.



|**Name**|**Parameter**|**Description**| |**Min**|**Typ**|**Max**| Unit|
|:---|:---|:---|---:|:---:|:---:|:---:| ---:|
||**idd\_25** || **Spec**  | **5.000** | **30.000** | **100.000** | **uA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 84.387 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|64.320 | 84.426 | <span style='color:red'>**107.774**</span> | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|73.500 | 83.903 | 94.306 | |
| | | |<a href='results/tran_Lay_typical.html'>Lay_typ</a>| | 83.073 |  | |
| | | |<a href='results/tran_Lay_etc.html'>Lay_etc</a>|62.494 | 83.106 | <span style='color:red'>**107.047**</span> | |
| | | |<a href='results/tran_Lay_mc.html'>Lay_3std</a>|61.574 | 84.804 | <span style='color:red'>**108.034**</span> | |
| | | |<a href='results/tran_Lay_supply.html'>Lay_supply</a>|76.911 | 83.073 | 88.967 | |
||**iddq\_25** || **Spec**  | **0.000** | **10.000** | **50.000** | **nA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 7.140 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|6.943 | 7.488 | 46.459 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|6.872 | 7.148 | 7.424 | |
| | | |<a href='results/tran_Lay_typical.html'>Lay_typ</a>| | 11.061 |  | |
| | | |<a href='results/tran_Lay_etc.html'>Lay_etc</a>|9.956 | 11.751 | <span style='color:orange'>**50.307**</span> | |
| | | |<a href='results/tran_Lay_mc.html'>Lay_3std</a>|10.802 | 11.033 | 11.264 | |
| | | |<a href='results/tran_Lay_supply.html'>Lay_supply</a>|10.164 | 11.061 | 11.753 | |
||**ind\_1p\_max** |Industrial 1 point calibration| **Spec**  | **-15.000** | **0.000** | **15.000** | **C** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 1.113 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|0.689 | 2.138 | 9.675 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|-1.568 | 3.314 | 8.196 | |
| | | |<a href='results/tran_Lay_typical.html'>Lay_typ</a>| | 1.027 |  | |
| | | |<a href='results/tran_Lay_etc.html'>Lay_etc</a>|0.554 | 2.094 | 9.094 | |
| | | |<a href='results/tran_Lay_mc.html'>Lay_3std</a>|-4.234 | 3.326 | 10.886 | |
| | | |<a href='results/tran_Lay_supply.html'>Lay_supply</a>|0.958 | 1.027 | 1.206 | |
||**ind\_1p\_min** |Industrial 1 point calibration| **Spec**  | **-15.000** | **0.000** | **15.000** | **C** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | -0.006 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|-7.027 | -4.939 | 0.237 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|-5.441 | -1.507 | 2.426 | |
| | | |<a href='results/tran_Lay_typical.html'>Lay_typ</a>| | -0.138 |  | |
| | | |<a href='results/tran_Lay_etc.html'>Lay_etc</a>|-6.716 | -4.631 | 0.025 | |
| | | |<a href='results/tran_Lay_mc.html'>Lay_3std</a>|<span style='color:red'>**-16.084**</span> | -3.562 | 8.961 | |
| | | |<a href='results/tran_Lay_supply.html'>Lay_supply</a>|-0.495 | -0.138 | 0.171 | |
||**ind\_2p\_max** |Industrial 2 point calibration| **Spec**  | **-10.000** | **0.000** | **10.000** | **C** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 2.023 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|0.244 | 1.828 | 5.308 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|-3.360 | 1.971 | 7.302 | |
| | | |<a href='results/tran_Lay_typical.html'>Lay_typ</a>| | 2.046 |  | |
| | | |<a href='results/tran_Lay_etc.html'>Lay_etc</a>|0.560 | 1.819 | 5.245 | |
| | | |<a href='results/tran_Lay_mc.html'>Lay_3std</a>|-3.740 | 2.427 | 8.594 | |
| | | |<a href='results/tran_Lay_supply.html'>Lay_supply</a>|1.977 | 1.992 | 2.046 | |
||**ind\_2p\_min** |Industrial 2 point calibration| **Spec**  | **-10.000** | **0.000** | **10.000** | **C** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | -0.738 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|-7.062 | -1.149 | -0.203 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|-2.710 | -0.956 | 0.798 | |
| | | |<a href='results/tran_Lay_typical.html'>Lay_typ</a>| | -1.728 |  | |
| | | |<a href='results/tran_Lay_etc.html'>Lay_etc</a>|-7.278 | -1.998 | -0.230 | |
| | | |<a href='results/tran_Lay_mc.html'>Lay_3std</a>|-6.613 | -2.005 | 2.603 | |
| | | |<a href='results/tran_Lay_supply.html'>Lay_supply</a>|-2.079 | -1.728 | -1.248 | |
||**com\_1p\_max** |Commercial 1 point calibration| **Spec**  | **-10.000** | **0.000** | **10.000** | **C** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 0.596 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|0.007 | 2.138 | 3.241 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|-0.842 | 1.494 | 3.829 | |
| | | |<a href='results/tran_Lay_typical.html'>Lay_typ</a>| | 0.739 |  | |
| | | |<a href='results/tran_Lay_etc.html'>Lay_etc</a>|0.073 | 2.094 | 2.902 | |
| | | |<a href='results/tran_Lay_mc.html'>Lay_3std</a>|-0.772 | 1.242 | 3.256 | |
| | | |<a href='results/tran_Lay_supply.html'>Lay_supply</a>|0.304 | 0.739 | 1.028 | |
||**com\_1p\_min** |Commercial 1 point calibration| **Spec**  | **-10.000** | **0.000** | **10.000** | **C** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | -0.006 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|-4.224 | -2.289 | 0.237 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|-2.474 | -0.701 | 1.072 | |
| | | |<a href='results/tran_Lay_typical.html'>Lay_typ</a>| | -0.044 |  | |
| | | |<a href='results/tran_Lay_etc.html'>Lay_etc</a>|-3.728 | -2.303 | 0.175 | |
| | | |<a href='results/tran_Lay_mc.html'>Lay_3std</a>|-4.159 | -1.016 | 2.127 | |
| | | |<a href='results/tran_Lay_supply.html'>Lay_supply</a>|-0.369 | -0.044 | 0.171 | |
||**com\_2p\_max** |Commercial 2 point calibration| **Spec**  | **-5.000** | **0.000** | **5.000** | **C** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 0.426 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|0.049 | 0.916 | 1.564 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|-0.813 | 0.476 | 1.764 | |
| | | |<a href='results/tran_Lay_typical.html'>Lay_typ</a>| | 0.413 |  | |
| | | |<a href='results/tran_Lay_etc.html'>Lay_etc</a>|0.153 | 1.030 | 1.526 | |
| | | |<a href='results/tran_Lay_mc.html'>Lay_3std</a>|-0.484 | 0.699 | 1.882 | |
| | | |<a href='results/tran_Lay_supply.html'>Lay_supply</a>|0.176 | 0.413 | 0.576 | |
||**com\_2p\_min** |Commercial 2 point calibration| **Spec**  | **-5.000** | **0.000** | **5.000** | **C** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | -0.114 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|-1.901 | -0.587 | 0.358 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|-0.631 | -0.156 | 0.319 | |
| | | |<a href='results/tran_Lay_typical.html'>Lay_typ</a>| | -0.069 |  | |
| | | |<a href='results/tran_Lay_etc.html'>Lay_etc</a>|-1.910 | -0.605 | 0.365 | |
| | | |<a href='results/tran_Lay_mc.html'>Lay_3std</a>|-1.381 | -0.402 | 0.576 | |
| | | |<a href='results/tran_Lay_supply.html'>Lay_supply</a>|-0.503 | -0.069 | 0.236 | |
||**freq\_min** |Frequency| **Spec**  | **1.500** | **3.000** | **4.800** | **MHz** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 1.700 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|<span style='color:red'>**1.345**</span> | 1.700 | 2.207 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|<span style='color:red'>**1.277**</span> | 1.643 | 2.009 | |
| | | |<a href='results/tran_Lay_typical.html'>Lay_typ</a>| | <span style='color:red'>**1.402**</span> |  | |
| | | |<a href='results/tran_Lay_etc.html'>Lay_etc</a>|<span style='color:red'>**1.127**</span> | <span style='color:red'>**1.402**</span> | 1.781 | |
| | | |<a href='results/tran_Lay_mc.html'>Lay_3std</a>|<span style='color:red'>**0.735**</span> | <span style='color:orange'>**1.465**</span> | 2.194 | |
| | | |<a href='results/tran_Lay_supply.html'>Lay_supply</a>|<span style='color:red'>**1.401**</span> | <span style='color:red'>**1.401**</span> | <span style='color:red'>**1.402**</span> | |
||**freq\_max** |Frequency| **Spec**  | **1.500** | **3.000** | **4.800** | **MHz** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 3.895 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|3.081 | 3.891 | <span style='color:orange'>**5.027**</span> | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|3.229 | 3.829 | 4.430 | |
| | | |<a href='results/tran_Lay_typical.html'>Lay_typ</a>| | 3.184 |  | |
| | | |<a href='results/tran_Lay_etc.html'>Lay_etc</a>|2.570 | 3.185 | 4.024 | |
| | | |<a href='results/tran_Lay_mc.html'>Lay_3std</a>|2.243 | 3.263 | 4.282 | |
| | | |<a href='results/tran_Lay_supply.html'>Lay_supply</a>|3.179 | 3.184 | 3.191 | |
||**FOM** |Figure Of Merit| **Spec**  | **10.000** | **40.000** | **400.000** | **nAK** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 17.747 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|<span style='color:red'>**8.627**</span> | 57.347 | 112.072 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|<span style='color:red'>**-34.759**</span> | 20.424 | 75.606 | |
| | | |<a href='results/tran_Lay_typical.html'>Lay_typ</a>| | 17.555 |  | |
| | | |<a href='results/tran_Lay_etc.html'>Lay_etc</a>|<span style='color:red'>**5.851**</span> | 64.320 | 136.601 | |
| | | |<a href='results/tran_Lay_mc.html'>Lay_3std</a>|<span style='color:red'>**-23.865**</span> | 40.845 | 105.556 | |
| | | |<a href='results/tran_Lay_supply.html'>Lay_supply</a>|11.431 | 17.555 | 26.408 | |

