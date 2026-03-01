

#### Loop stability (lstb)

Check stability



|**Name**|**Parameter**|**Description**| |**Min**|**Typ**|**Max**| Unit|
|:---|:---|:---|---:|:---:|:---:|:---:| ---:|
|**Gain Margin**|**gm\_db** || **Spec**  | **-50.00** | **-10.00** | **-10.00** | **dB** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | -16.06 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|-19.61 | -16.09 | -12.33 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|-18.73 | -15.78 | -12.83 | |
|**DC gain**|**lf\_gain** || **Spec**  | **50.00** | **40.00** | **80.00** | **dB** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 69.02 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|66.27 | 67.43 | 70.29 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|66.46 | 68.89 | 71.31 | |
|**Phase Margin**|**pm\_deg** || **Spec**  | **45.00** | **60.00** | **90.00** |  |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 60.84 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|46.37 | 61.01 | 71.78 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|51.32 | 60.05 | 68.78 | |
|**Unity Gain Frequency**|**ug** || **Spec**  | **3.00** | **15.00** | **100.00** | **MHz** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 5.79 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|<span style='color:red'>**2.57**</span> | 5.26 | 9.50 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|3.62 | 5.66 | 7.71 | |
|**PMOS gate**|**v(lpo)** || **Spec**  | **0.45** | **0.70** | **1.10** | **V** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 0.76 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|0.52 | 0.78 | 1.05 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|0.73 | 0.76 | 0.78 | |
|**Delta diode voltage**|**vd** || **Spec**  | **80.00** | **106.00** | **150.00** | **mV** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 109.24 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|84.63 | 115.00 | 145.74 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|104.79 | 108.96 | 113.13 | |
|**Output current**|**i(v1)** || **Spec**  | **0.50** | **1.00** | **2.00** | **uA** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 1.09 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|0.81 | 1.13 | 1.75 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|0.63 | 1.15 | 1.67 | |
|**VD Error**|**vdiff** || **Spec**  | **-6.00** | **0.00** | **6.00** | **mV** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | -0.08 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|-0.32 | -0.10 | 0.06 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|<span style='color:red'>**-22.99**</span> | 0.96 | <span style='color:red'>**24.91**</span> | |

#### Transient (tran)

Check settling time and current variation



|**Name**|**Parameter**|**Description**| |**Min**|**Typ**|**Max**| Unit|
|:---|:---|:---|---:|:---:|:---:|:---:| ---:|
||**t\_settle** || **Spec**  | **0.01** | **0.05** | **2.00** | **us** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 0.32 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|0.28 | 0.35 | 0.58 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|0.29 | 0.32 | 0.34 | |
||**i0** || **Spec**  | **0.500** | **1.000** | **2.000** | **uA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 1.160 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|0.813 | 1.169 | 1.667 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|0.698 | 1.131 | 1.564 | |
||**i1** || **Spec**  | **0.500** | **1.000** | **2.000** | **uA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 1.160 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|0.812 | 1.169 | 1.666 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|0.705 | 1.123 | 1.541 | |
||**i2** || **Spec**  | **0.500** | **1.000** | **2.000** | **uA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 1.159 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|0.812 | 1.168 | 1.666 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|0.699 | 1.114 | 1.528 | |
||**i3** || **Spec**  | **0.500** | **1.000** | **2.000** | **uA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 1.159 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|0.812 | 1.167 | 1.665 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|0.731 | 1.115 | 1.499 | |
||**idd** || **Spec**  | **5.000** | **30.000** | **60.000** | **uA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 41.990 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|32.794 | 40.880 | 51.902 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|33.968 | 41.259 | 48.550 | |

#### DC (dc)

Check temperature performance



|**Name**|**Parameter**|**Description**| |**Min**|**Typ**|**Max**| Unit|
|:---|:---|:---|---:|:---:|:---:|:---:| ---:|
||**ibp\_err\_max** || **Spec**  | **-30.00** | **0.00** | **20.00** | **nA** |
| | | |<a href='results/dc_Sch_typical.html'>Sch_typ</a>| | 8.36 |  | |
| | | |<a href='results/dc_Sch_etc.html'>Sch_etc</a>|7.45 | 8.37 | 9.54 | |
| | | |<a href='results/dc_Sch_mc.html'>Sch_3std</a>|4.00 | 8.23 | 12.47 | |
||**ibp\_err\_min** || **Spec**  | **-30.00** | **0.00** | **20.00** | **nA** |
| | | |<a href='results/dc_Sch_typical.html'>Sch_typ</a>| | -18.42 |  | |
| | | |<a href='results/dc_Sch_etc.html'>Sch_etc</a>|-21.04 | -18.43 | -16.39 | |
| | | |<a href='results/dc_Sch_mc.html'>Sch_3std</a>|-28.36 | -17.72 | -7.09 | |
||**imax** || **Spec**  | **0.50** | **0.00** | **2.00** | **uA** |
| | | |<a href='results/dc_Sch_typical.html'>Sch_typ</a>| | 1.46 |  | |
| | | |<a href='results/dc_Sch_etc.html'>Sch_etc</a>|1.29 | 1.46 | 1.67 | |
| | | |<a href='results/dc_Sch_mc.html'>Sch_3std</a>|1.02 | 1.43 | 1.85 | |
||**imin** || **Spec**  | **0.50** | **0.00** | **2.00** | **uA** |
| | | |<a href='results/dc_Sch_typical.html'>Sch_typ</a>| | 0.92 |  | |
| | | |<a href='results/dc_Sch_etc.html'>Sch_etc</a>|0.81 | 0.92 | 1.05 | |
| | | |<a href='results/dc_Sch_mc.html'>Sch_3std</a>|0.52 | 0.90 | 1.28 | |
||**a\_per\_c** || **Spec**  | **1.00** | **3.00** | **5.00** | **nA** |
| | | |<a href='results/dc_Sch_typical.html'>Sch_typ</a>| | 3.27 |  | |
| | | |<a href='results/dc_Sch_etc.html'>Sch_etc</a>|2.90 | 3.27 | 3.75 | |
| | | |<a href='results/dc_Sch_mc.html'>Sch_3std</a>|2.75 | 3.24 | 3.73 | |

