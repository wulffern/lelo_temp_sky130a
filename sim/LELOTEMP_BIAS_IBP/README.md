

#### Loop stability (lstb)

Check stability



|**Name**|**Parameter**|**Description**| |**Min**|**Typ**|**Max**| Unit|
|:---|:---|:---|---:|:---:|:---:|:---:| ---:|
|**Gain Margin**|**gm\_db** || **Spec**  | **-50.00** | **-10.00** | **-10.00** | **dB** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | -12.00 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|-16.58 | -12.55 | <span style='color:red'>**-9.17**</span> | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|-13.59 | -12.28 | -10.97 | |
|**DC gain**|**lf\_gain** || **Spec**  | **50.00** | **40.00** | **80.00** | **dB** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 69.75 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|<span style='color:red'>**43.72**</span> | 67.99 | 71.06 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|66.85 | 69.38 | 71.91 | |
|**Phase Margin**|**pm\_deg** || **Spec**  | **45.00** | **60.00** | **90.00** |  |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 50.81 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|<span style='color:red'>**37.40**</span> | 53.43 | 67.56 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|46.66 | 52.00 | 57.33 | |
|**Unity Gain Frequency**|**ug** || **Spec**  | **3.00** | **15.00** | **100.00** | **MHz** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 8.84 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|3.99 | 7.86 | 14.09 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|6.84 | 8.52 | 10.19 | |
|**PMOS gate**|**v(lpo)** || **Spec**  | **0.45** | **0.70** | **1.10** | **V** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 0.76 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|0.52 | 0.78 | 1.05 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|0.75 | 0.76 | 0.77 | |
|**Delta diode voltage**|**vd** || **Spec**  | **80.00** | **106.00** | **150.00** | **mV** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 109.29 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|84.63 | 114.99 | 145.78 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|104.92 | 108.99 | 113.05 | |
|**Output current**|**i(v1)** || **Spec**  | **0.50** | **1.00** | **2.00** | **uA** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 1.23 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|0.81 | 1.12 | 1.73 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|0.85 | 1.20 | 1.54 | |
|**VD Error**|**vdiff** || **Spec**  | **-6.00** | **0.00** | **6.00** | **mV** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | -0.04 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|-0.37 | -0.08 | 0.10 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|<span style='color:red'>**-14.15**</span> | 1.91 | <span style='color:red'>**17.97**</span> | |

#### Transient (tran)

Check settling time and current variation



|**Name**|**Parameter**|**Description**| |**Min**|**Typ**|**Max**| Unit|
|:---|:---|:---|---:|:---:|:---:|:---:| ---:|
||**t\_settle** || **Spec**  | **0.01** | **0.05** | **2.00** | **us** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | <span style='color:red'>**2.12**</span> |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|0.55 | <span style='color:red'>**2.91**</span> | <span style='color:red'>**8.98**</span> | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|1.73 | <span style='color:red'>**2.15**</span> | <span style='color:red'>**2.56**</span> | |
||**i0** || **Spec**  | **0.500** | **1.000** | **2.000** | **uA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 1.160 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|<span style='color:red'>**0.000**</span> | 1.169 | 1.667 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|0.789 | 1.129 | 1.468 | |
||**i1** || **Spec**  | **0.500** | **1.000** | **2.000** | **uA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 1.159 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|<span style='color:red'>**0.000**</span> | 1.169 | 1.667 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|0.829 | 1.122 | 1.414 | |
||**i2** || **Spec**  | **0.500** | **1.000** | **2.000** | **uA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 1.159 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|<span style='color:red'>**0.000**</span> | 1.168 | 1.666 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|0.827 | 1.124 | 1.421 | |
||**i3** || **Spec**  | **0.500** | **1.000** | **2.000** | **uA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 1.159 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|<span style='color:red'>**0.000**</span> | 1.168 | 1.666 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|0.894 | 1.136 | 1.378 | |
||**idd** || **Spec**  | **5.000** | **30.000** | **60.000** | **uA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 37.527 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|<span style='color:red'>**0.474**</span> | 35.672 | 49.636 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|30.925 | 36.712 | 42.498 | |

#### DC (dc)

Check temperature performance



|**Name**|**Parameter**|**Description**| |**Min**|**Typ**|**Max**| Unit|
|:---|:---|:---|---:|:---:|:---:|:---:| ---:|
||**ibp\_err\_max** || **Spec**  | **-30.00** | **0.00** | **20.00** | **nA** |
| | | |<a href='results/dc_Sch_typical.html'>Sch_typ</a>| | 8.34 |  | |
| | | |<a href='results/dc_Sch_etc.html'>Sch_etc</a>|7.43 | 8.31 | 9.50 | |
| | | |<a href='results/dc_Sch_mc.html'>Sch_3std</a>|4.21 | 8.50 | 12.79 | |
||**ibp\_err\_min** || **Spec**  | **-30.00** | **0.00** | **20.00** | **nA** |
| | | |<a href='results/dc_Sch_typical.html'>Sch_typ</a>| | -18.35 |  | |
| | | |<a href='results/dc_Sch_etc.html'>Sch_etc</a>|-20.95 | -18.33 | -16.02 | |
| | | |<a href='results/dc_Sch_mc.html'>Sch_3std</a>|-29.22 | -18.48 | -7.74 | |
||**imax** || **Spec**  | **0.50** | **0.00** | **2.00** | **uA** |
| | | |<a href='results/dc_Sch_typical.html'>Sch_typ</a>| | 1.46 |  | |
| | | |<a href='results/dc_Sch_etc.html'>Sch_etc</a>|1.29 | 1.46 | 1.67 | |
| | | |<a href='results/dc_Sch_mc.html'>Sch_3std</a>|1.09 | 1.43 | 1.77 | |
||**imin** || **Spec**  | **0.50** | **0.00** | **2.00** | **uA** |
| | | |<a href='results/dc_Sch_typical.html'>Sch_typ</a>| | 0.91 |  | |
| | | |<a href='results/dc_Sch_etc.html'>Sch_etc</a>|0.81 | 0.92 | 1.05 | |
| | | |<a href='results/dc_Sch_mc.html'>Sch_3std</a>|0.55 | 0.88 | 1.21 | |
||**a\_per\_c** || **Spec**  | **1.00** | **3.00** | **5.00** | **nA** |
| | | |<a href='results/dc_Sch_typical.html'>Sch_typ</a>| | 3.27 |  | |
| | | |<a href='results/dc_Sch_etc.html'>Sch_etc</a>|2.90 | 3.28 | 3.76 | |
| | | |<a href='results/dc_Sch_mc.html'>Sch_3std</a>|2.82 | 3.30 | 3.78 | |

