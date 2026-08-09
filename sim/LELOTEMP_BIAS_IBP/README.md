

#### Loop stability (lstb)

Check stability



|**Name**|**Parameter**|**Description**| |**Min**|**Typ**|**Max**| Unit|
|:---|:---|:---|---:|:---:|:---:|:---:| ---:|
|**Gain Margin**|**gm\_db** || **Spec**  | **-50.00** | **-10.00** | **-10.00** | **dB** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | -19.55 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|-26.53 | -18.94 | -16.01 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|-20.64 | -19.51 | -18.37 | |
|**DC gain**|**lf\_gain** || **Spec**  | **50.00** | **40.00** | **80.00** | **dB** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | <span style='color:red'>**42.50**</span> |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|<span style='color:red'>**39.89**</span> | <span style='color:red'>**42.76**</span> | <span style='color:red'>**44.19**</span> | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|<span style='color:red'>**40.70**</span> | <span style='color:red'>**42.58**</span> | <span style='color:red'>**44.47**</span> | |
|**Phase Margin**|**pm\_deg** || **Spec**  | **45.00** | **60.00** | **90.00** |  |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 70.55 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|59.93 | 68.21 | 80.96 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|67.47 | 70.36 | 73.25 | |
|**Unity Gain Frequency**|**ug** || **Spec**  | **3.00** | **15.00** | **100.00** | **MHz** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 3.76 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|<span style='color:red'>**1.35**</span> | 4.06 | 6.78 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|3.14 | 3.80 | 4.47 | |
|**PMOS gate**|**v(lpo)** || **Spec**  | **0.45** | **0.70** | **1.10** | **V** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 0.76 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|0.52 | 0.78 | 1.05 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|0.74 | 0.76 | 0.78 | |
|**Delta diode voltage**|**vd** || **Spec**  | **80.00** | **106.00** | **150.00** | **mV** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 109.27 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|84.62 | 115.02 | 145.84 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|104.95 | 108.99 | 113.03 | |
|**Output current**|**i(v1)** || **Spec**  | **0.50** | **1.00** | **2.00** | **uA** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 1.06 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|0.71 | 1.09 | 1.74 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|0.67 | 1.06 | 1.46 | |
|**VD Error**|**vdiff** || **Spec**  | **-6.00** | **0.00** | **6.00** | **mV** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 0.60 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|0.25 | 0.61 | 1.02 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|<span style='color:red'>**-29.05**</span> | -1.49 | <span style='color:red'>**26.07**</span> | |

#### Transient (tran)

Check settling time and current variation



|**Name**|**Parameter**|**Description**| |**Min**|**Typ**|**Max**| Unit|
|:---|:---|:---|---:|:---:|:---:|:---:| ---:|
||**t\_settle** || **Spec**  | **0.01** | **0.05** | **2.00** | **us** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 0.37 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|0.33 | 0.62 | 1.78 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|0.48 | 0.62 | 0.77 | |
||**i0** || **Spec**  | **0.500** | **1.000** | **2.000** | **uA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 1.160 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|0.806 | 1.162 | 1.658 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|0.759 | 1.153 | 1.546 | |
||**i1** || **Spec**  | **0.500** | **1.000** | **2.000** | **uA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 1.160 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|0.805 | 1.162 | 1.658 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|0.732 | 1.140 | 1.548 | |
||**i2** || **Spec**  | **0.500** | **1.000** | **2.000** | **uA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 1.159 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|0.804 | 1.162 | 1.658 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|0.835 | 1.161 | 1.486 | |
||**i3** || **Spec**  | **0.500** | **1.000** | **2.000** | **uA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 1.159 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|0.804 | 1.161 | 1.657 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|0.815 | 1.168 | 1.520 | |
||**idd** || **Spec**  | **5.000** | **30.000** | **60.000** | **uA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 42.766 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|15.579 | 30.087 | 48.886 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|25.153 | 29.247 | 33.341 | |

#### DC (dc)

Check temperature performance



|**Name**|**Parameter**|**Description**| |**Min**|**Typ**|**Max**| Unit|
|:---|:---|:---|---:|:---:|:---:|:---:| ---:|
||**ibp\_err\_max** || **Spec**  | **-30.00** | **0.00** | **20.00** | **nA** |
| | | |<a href='results/dc_Sch_typical.html'>Sch_typ</a>| | 8.15 |  | |
| | | |<a href='results/dc_Sch_etc.html'>Sch_etc</a>|7.26 | 8.17 | 9.31 | |
| | | |<a href='results/dc_Sch_mc.html'>Sch_3std</a>|4.96 | 8.50 | 12.04 | |
||**ibp\_err\_min** || **Spec**  | **-30.00** | **0.00** | **20.00** | **nA** |
| | | |<a href='results/dc_Sch_typical.html'>Sch_typ</a>| | -17.94 |  | |
| | | |<a href='results/dc_Sch_etc.html'>Sch_etc</a>|-20.47 | -17.84 | -15.92 | |
| | | |<a href='results/dc_Sch_mc.html'>Sch_3std</a>|<span style='color:red'>**-37.62**</span> | -19.34 | -1.06 | |
||**imax** || **Spec**  | **0.50** | **0.00** | **2.00** | **uA** |
| | | |<a href='results/dc_Sch_typical.html'>Sch_typ</a>| | 1.45 |  | |
| | | |<a href='results/dc_Sch_etc.html'>Sch_etc</a>|1.28 | 1.45 | 1.66 | |
| | | |<a href='results/dc_Sch_mc.html'>Sch_3std</a>|1.05 | 1.45 | 1.85 | |
||**imin** || **Spec**  | **0.50** | **0.00** | **2.00** | **uA** |
| | | |<a href='results/dc_Sch_typical.html'>Sch_typ</a>| | 0.91 |  | |
| | | |<a href='results/dc_Sch_etc.html'>Sch_etc</a>|0.81 | 0.91 | 1.04 | |
| | | |<a href='results/dc_Sch_mc.html'>Sch_3std</a>|0.54 | 0.91 | 1.27 | |
||**a\_per\_c** || **Spec**  | **1.00** | **3.00** | **5.00** | **nA** |
| | | |<a href='results/dc_Sch_typical.html'>Sch_typ</a>| | 3.26 |  | |
| | | |<a href='results/dc_Sch_etc.html'>Sch_etc</a>|2.89 | 3.26 | 3.73 | |
| | | |<a href='results/dc_Sch_mc.html'>Sch_3std</a>|2.87 | 3.29 | 3.70 | |

