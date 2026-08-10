

#### Loop stability (lstb)

Check stability



|**Name**|**Parameter**|**Description**| |**Min**|**Typ**|**Max**| Unit|
|:---|:---|:---|---:|:---:|:---:|:---:| ---:|
|**Gain Margin**|**gm\_db** || **Spec**  | **-50.00** | **-10.00** | **-10.00** | **dB** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | -15.36 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|-23.93 | -14.24 | -12.14 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|-16.33 | -15.39 | -14.45 | |
|**DC gain**|**lf\_gain** || **Spec**  | **50.00** | **40.00** | **80.00** | **dB** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | <span style='color:red'>**42.43**</span> |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|<span style='color:red'>**40.77**</span> | <span style='color:red'>**42.53**</span> | <span style='color:red'>**43.59**</span> | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|<span style='color:red'>**40.55**</span> | <span style='color:red'>**42.23**</span> | <span style='color:red'>**43.91**</span> | |
|**Phase Margin**|**pm\_deg** || **Spec**  | **45.00** | **60.00** | **90.00** |  |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 57.98 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|45.15 | 54.46 | 76.15 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|54.39 | 58.28 | 62.18 | |
|**Unity Gain Frequency**|**ug** || **Spec**  | **3.00** | **15.00** | **100.00** | **MHz** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 6.05 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|<span style='color:red'>**2.29**</span> | 6.15 | 9.90 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|4.92 | 5.94 | 6.97 | |
|**PMOS gate**|**v(lpo)** || **Spec**  | **0.45** | **0.70** | **1.10** | **V** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 0.76 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|0.52 | 0.78 | 1.05 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|0.74 | 0.76 | 0.78 | |
|**Delta diode voltage**|**vd** || **Spec**  | **80.00** | **106.00** | **150.00** | **mV** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 109.27 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|84.63 | 115.03 | 145.89 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|104.97 | 108.97 | 112.97 | |
|**Output current**|**i(v1)** || **Spec**  | **0.50** | **1.00** | **2.00** | **uA** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 1.09 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|0.73 | 1.10 | 1.79 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|0.72 | 1.05 | 1.38 | |
|**VD Error**|**vdiff** || **Spec**  | **-6.00** | **0.00** | **6.00** | **mV** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 0.22 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|-0.03 | 0.19 | 0.67 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|<span style='color:red'>**-22.11**</span> | 2.26 | <span style='color:red'>**26.62**</span> | |

#### Transient (tran)

Check settling time and current variation



|**Name**|**Parameter**|**Description**| |**Min**|**Typ**|**Max**| Unit|
|:---|:---|:---|---:|:---:|:---:|:---:| ---:|
||**t\_settle** || **Spec**  | **0.01** | **0.05** | **2.00** | **us** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 0.49 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|0.33 | 0.47 | 1.06 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|0.39 | 0.50 | 0.62 | |
||**i0** || **Spec**  | **0.500** | **1.000** | **2.000** | **uA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 1.186 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|0.829 | 1.196 | 1.706 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|0.811 | 1.142 | 1.473 | |
||**i1** || **Spec**  | **0.500** | **1.000** | **2.000** | **uA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 1.185 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|0.828 | 1.196 | 1.706 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|0.808 | 1.144 | 1.480 | |
||**i2** || **Spec**  | **0.500** | **1.000** | **2.000** | **uA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 1.185 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|0.828 | 1.195 | 1.706 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|0.825 | 1.155 | 1.485 | |
||**i3** || **Spec**  | **0.500** | **1.000** | **2.000** | **uA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 1.185 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|0.828 | 1.195 | 1.705 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|0.802 | 1.152 | 1.503 | |
||**idd** || **Spec**  | **5.000** | **30.000** | **60.000** | **uA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 41.241 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|19.588 | 42.984 | <span style='color:red'>**72.811**</span> | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|37.001 | 40.908 | 44.815 | |

#### DC (dc)

Check temperature performance



|**Name**|**Parameter**|**Description**| |**Min**|**Typ**|**Max**| Unit|
|:---|:---|:---|---:|:---:|:---:|:---:| ---:|
||**ibp\_err\_max** || **Spec**  | **-30.00** | **0.00** | **20.00** | **nA** |
| | | |<a href='results/dc_Sch_typical.html'>Sch_typ</a>| | 8.24 |  | |
| | | |<a href='results/dc_Sch_etc.html'>Sch_etc</a>|7.35 | 8.25 | 9.41 | |
| | | |<a href='results/dc_Sch_mc.html'>Sch_3std</a>|4.59 | 7.76 | 10.93 | |
||**ibp\_err\_min** || **Spec**  | **-30.00** | **0.00** | **20.00** | **nA** |
| | | |<a href='results/dc_Sch_typical.html'>Sch_typ</a>| | -18.35 |  | |
| | | |<a href='results/dc_Sch_etc.html'>Sch_etc</a>|-20.93 | -18.36 | -16.33 | |
| | | |<a href='results/dc_Sch_mc.html'>Sch_3std</a>|-28.23 | -16.22 | -4.20 | |
||**imax** || **Spec**  | **0.50** | **0.00** | **2.00** | **uA** |
| | | |<a href='results/dc_Sch_typical.html'>Sch_typ</a>| | 1.49 |  | |
| | | |<a href='results/dc_Sch_etc.html'>Sch_etc</a>|1.32 | 1.49 | 1.71 | |
| | | |<a href='results/dc_Sch_mc.html'>Sch_3std</a>|1.11 | 1.44 | 1.77 | |
||**imin** || **Spec**  | **0.50** | **0.00** | **2.00** | **uA** |
| | | |<a href='results/dc_Sch_typical.html'>Sch_typ</a>| | 0.94 |  | |
| | | |<a href='results/dc_Sch_etc.html'>Sch_etc</a>|0.83 | 0.94 | 1.07 | |
| | | |<a href='results/dc_Sch_mc.html'>Sch_3std</a>|0.57 | 0.90 | 1.23 | |
||**a\_per\_c** || **Spec**  | **1.00** | **3.00** | **5.00** | **nA** |
| | | |<a href='results/dc_Sch_typical.html'>Sch_typ</a>| | 3.35 |  | |
| | | |<a href='results/dc_Sch_etc.html'>Sch_etc</a>|2.97 | 3.35 | 3.84 | |
| | | |<a href='results/dc_Sch_mc.html'>Sch_3std</a>|2.83 | 3.29 | 3.75 | |

