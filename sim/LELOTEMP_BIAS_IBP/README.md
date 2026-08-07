

#### Loop stability (lstb)

Check stability



|**Name**|**Parameter**|**Description**| |**Min**|**Typ**|**Max**| Unit|
|:---|:---|:---|---:|:---:|:---:|:---:| ---:|
|**Gain Margin**|**gm\_db** || **Spec**  | **-50.00** | **-10.00** | **-10.00** | **dB** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | -15.24 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|-31.04 | -16.50 | -12.85 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|-18.71 | -15.65 | -12.60 | |
|**DC gain**|**lf\_gain** || **Spec**  | **50.00** | **40.00** | **80.00** | **dB** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 69.07 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|65.77 | 67.28 | 69.86 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|66.68 | 68.81 | 70.95 | |
|**Phase Margin**|**pm\_deg** || **Spec**  | **45.00** | **60.00** | **90.00** |  |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 58.63 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|48.41 | 62.56 | 70.99 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|50.86 | 59.70 | 68.53 | |
|**Unity Gain Frequency**|**ug** || **Spec**  | **3.00** | **15.00** | **100.00** | **MHz** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 5.76 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|<span style='color:red'>**2.59**</span> | 5.36 | 10.12 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|3.65 | 5.65 | 7.65 | |
|**PMOS gate**|**v(lpo)** || **Spec**  | **0.45** | **0.70** | **1.10** | **V** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 0.76 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|0.52 | 0.77 | 1.05 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|0.73 | 0.76 | 0.78 | |
|**Delta diode voltage**|**vd** || **Spec**  | **80.00** | **106.00** | **150.00** | **mV** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 109.25 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|81.57 | 115.01 | 145.76 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|104.82 | 108.95 | 113.09 | |
|**Output current**|**i(v1)** || **Spec**  | **0.50** | **1.00** | **2.00** | **uA** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 1.08 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|0.87 | 1.26 | 1.74 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|0.75 | 1.12 | 1.50 | |
|**VD Error**|**vdiff** || **Spec**  | **-6.00** | **0.00** | **6.00** | **mV** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | -0.08 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|<span style='color:red'>**-97.25**</span> | -0.13 | 0.06 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|<span style='color:red'>**-22.99**</span> | 0.99 | <span style='color:red'>**24.96**</span> | |

#### Transient (tran)

Check settling time and current variation



|**Name**|**Parameter**|**Description**| |**Min**|**Typ**|**Max**| Unit|
|:---|:---|:---|---:|:---:|:---:|:---:| ---:|
||**t\_settle** || **Spec**  | **0.01** | **0.05** | **2.00** | **us** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 0.37 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|0.31 | 0.40 | <span style='color:red'>**8.84**</span> | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|0.35 | 0.37 | 0.40 | |
||**i0** || **Spec**  | **0.500** | **1.000** | **2.000** | **uA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 1.160 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|0.692 | 1.169 | 1.667 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|0.720 | 1.115 | 1.511 | |
||**i1** || **Spec**  | **0.500** | **1.000** | **2.000** | **uA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 1.160 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|0.692 | 1.169 | 1.666 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|0.690 | 1.143 | 1.596 | |
||**i2** || **Spec**  | **0.500** | **1.000** | **2.000** | **uA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 1.159 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|0.692 | 1.168 | 1.666 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|0.720 | 1.122 | 1.525 | |
||**i3** || **Spec**  | **0.500** | **1.000** | **2.000** | **uA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 1.159 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|0.692 | 1.167 | 1.665 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|0.725 | 1.114 | 1.502 | |
||**idd** || **Spec**  | **5.000** | **30.000** | **60.000** | **uA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 42.766 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|33.372 | 40.889 | 53.123 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|34.902 | 41.982 | 49.062 | |

#### DC (dc)

Check temperature performance



|**Name**|**Parameter**|**Description**| |**Min**|**Typ**|**Max**| Unit|
|:---|:---|:---|---:|:---:|:---:|:---:| ---:|
||**ibp\_err\_max** || **Spec**  | **-30.00** | **0.00** | **20.00** | **nA** |
| | | |<a href='results/dc_Sch_typical.html'>Sch_typ</a>| | 8.38 |  | |
| | | |<a href='results/dc_Sch_etc.html'>Sch_etc</a>|7.45 | 8.39 | <span style='color:red'>**496.21**</span> | |
| | | |<a href='results/dc_Sch_mc.html'>Sch_3std</a>|<span style='color:red'>**-247.30**</span> | <span style='color:red'>**24.70**</span> | <span style='color:red'>**296.71**</span> | |
||**ibp\_err\_min** || **Spec**  | **-30.00** | **0.00** | **20.00** | **nA** |
| | | |<a href='results/dc_Sch_typical.html'>Sch_typ</a>| | -18.43 |  | |
| | | |<a href='results/dc_Sch_etc.html'>Sch_etc</a>|<span style='color:red'>**-62.25**</span> | -18.47 | -16.39 | |
| | | |<a href='results/dc_Sch_mc.html'>Sch_3std</a>|<span style='color:red'>**-53.14**</span> | -19.39 | 14.35 | |
||**imax** || **Spec**  | **0.50** | **0.00** | **2.00** | **uA** |
| | | |<a href='results/dc_Sch_typical.html'>Sch_typ</a>| | 1.46 |  | |
| | | |<a href='results/dc_Sch_etc.html'>Sch_etc</a>|1.29 | 1.46 | 1.67 | |
| | | |<a href='results/dc_Sch_mc.html'>Sch_3std</a>|1.00 | 1.41 | 1.82 | |
||**imin** || **Spec**  | **0.50** | **0.00** | **2.00** | **uA** |
| | | |<a href='results/dc_Sch_typical.html'>Sch_typ</a>| | 0.92 |  | |
| | | |<a href='results/dc_Sch_etc.html'>Sch_etc</a>|0.81 | 0.91 | 1.05 | |
| | | |<a href='results/dc_Sch_mc.html'>Sch_3std</a>|<span style='color:orange'>**0.49**</span> | 0.87 | 1.25 | |
||**a\_per\_c** || **Spec**  | **1.00** | **3.00** | **5.00** | **nA** |
| | | |<a href='results/dc_Sch_typical.html'>Sch_typ</a>| | 3.27 |  | |
| | | |<a href='results/dc_Sch_etc.html'>Sch_etc</a>|2.90 | 3.27 | 3.75 | |
| | | |<a href='results/dc_Sch_mc.html'>Sch_3std</a>|2.74 | 3.25 | 3.76 | |

