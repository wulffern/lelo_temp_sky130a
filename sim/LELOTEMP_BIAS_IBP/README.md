

#### Loop stability (lstb)

Check stability



|**Name**|**Parameter**|**Description**| |**Min**|**Typ**|**Max**| Unit|
|:---|:---|:---|---:|:---:|:---:|:---:| ---:|
|**Gain Margin**|**gm\_db** || **Spec**  | **-50.00** | **-10.00** | **-10.00** | **dB** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | -14.68 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|-18.71 | -15.22 | -12.72 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|-16.37 | -14.75 | -13.12 | |
|**DC gain**|**lf\_gain** || **Spec**  | **50.00** | **40.00** | **80.00** | **dB** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 68.80 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|66.53 | 67.45 | 69.92 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|66.79 | 68.95 | 71.12 | |
|**Phase Margin**|**pm\_deg** || **Spec**  | **45.00** | **60.00** | **90.00** |  |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 61.29 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|53.27 | 63.05 | 72.38 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|56.25 | 61.38 | 66.50 | |
|**Unity Gain Frequency**|**ug** || **Spec**  | **3.00** | **15.00** | **100.00** | **MHz** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 7.70 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|3.40 | 6.95 | 12.84 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|5.76 | 7.75 | 9.75 | |
|**PMOS gate**|**v(lpo)** || **Spec**  | **0.45** | **0.70** | **1.10** | **V** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 0.76 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|0.52 | 0.78 | 1.05 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|0.74 | 0.76 | 0.77 | |
|**Delta diode voltage**|**vd** || **Spec**  | **80.00** | **106.00** | **150.00** | **mV** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 109.26 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|84.63 | 115.10 | 145.74 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|105.00 | 108.97 | 112.94 | |
|**Output current**|**i(v1)** || **Spec**  | **0.50** | **1.00** | **2.00** | **uA** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 1.23 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|0.76 | 1.13 | 1.70 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|0.64 | 1.17 | 1.70 | |
|**VD Error**|**vdiff** || **Spec**  | **-6.00** | **0.00** | **6.00** | **mV** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | -0.09 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|-0.33 | -0.10 | 0.93 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|<span style='color:red'>**-19.88**</span> | -0.88 | <span style='color:red'>**18.13**</span> | |

#### Transient (tran)

Check settling time and current variation



|**Name**|**Parameter**|**Description**| |**Min**|**Typ**|**Max**| Unit|
|:---|:---|:---|---:|:---:|:---:|:---:| ---:|
||**t\_settle** || **Spec**  | **0.01** | **0.05** | **2.00** | **us** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 0.70 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|0.63 | 0.91 | <span style='color:red'>**9.00**</span> | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|0.57 | 0.76 | 0.96 | |
||**i0** || **Spec**  | **0.500** | **1.000** | **2.000** | **uA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 1.160 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|0.813 | 1.170 | 1.668 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|0.808 | 1.165 | 1.522 | |
||**i1** || **Spec**  | **0.500** | **1.000** | **2.000** | **uA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 1.160 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|0.812 | 1.169 | 1.667 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|0.794 | 1.162 | 1.530 | |
||**i2** || **Spec**  | **0.500** | **1.000** | **2.000** | **uA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 1.159 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|0.812 | 1.168 | 1.666 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|0.895 | 1.168 | 1.440 | |
||**i3** || **Spec**  | **0.500** | **1.000** | **2.000** | **uA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 1.159 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|0.812 | 1.167 | 1.664 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|0.845 | 1.152 | 1.459 | |
||**idd** || **Spec**  | **5.000** | **30.000** | **60.000** | **uA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 39.668 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|30.705 | 38.660 | 49.364 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|33.285 | 39.945 | 46.605 | |

#### DC (dc)

Check temperature performance



|**Name**|**Parameter**|**Description**| |**Min**|**Typ**|**Max**| Unit|
|:---|:---|:---|---:|:---:|:---:|:---:| ---:|
||**ibp\_err\_max** || **Spec**  | **-30.00** | **0.00** | **20.00** | **nA** |
| | | |<a href='results/dc_Sch_typical.html'>Sch_typ</a>| | 8.42 |  | |
| | | |<a href='results/dc_Sch_etc.html'>Sch_etc</a>|7.48 | 8.43 | 9.82 | |
| | | |<a href='results/dc_Sch_mc.html'>Sch_3std</a>|4.17 | 8.42 | 12.67 | |
||**ibp\_err\_min** || **Spec**  | **-30.00** | **0.00** | **20.00** | **nA** |
| | | |<a href='results/dc_Sch_typical.html'>Sch_typ</a>| | -18.48 |  | |
| | | |<a href='results/dc_Sch_etc.html'>Sch_etc</a>|-21.09 | -18.40 | -16.43 | |
| | | |<a href='results/dc_Sch_mc.html'>Sch_3std</a>|<span style='color:red'>**-30.16**</span> | -18.40 | -6.64 | |
||**imax** || **Spec**  | **0.50** | **0.00** | **2.00** | **uA** |
| | | |<a href='results/dc_Sch_typical.html'>Sch_typ</a>| | 1.46 |  | |
| | | |<a href='results/dc_Sch_etc.html'>Sch_etc</a>|1.29 | 1.46 | 1.67 | |
| | | |<a href='results/dc_Sch_mc.html'>Sch_3std</a>|1.12 | 1.46 | 1.81 | |
||**imin** || **Spec**  | **0.50** | **0.00** | **2.00** | **uA** |
| | | |<a href='results/dc_Sch_typical.html'>Sch_typ</a>| | 0.92 |  | |
| | | |<a href='results/dc_Sch_etc.html'>Sch_etc</a>|0.81 | 0.92 | 1.05 | |
| | | |<a href='results/dc_Sch_mc.html'>Sch_3std</a>|0.56 | 0.92 | 1.28 | |
||**a\_per\_c** || **Spec**  | **1.00** | **3.00** | **5.00** | **nA** |
| | | |<a href='results/dc_Sch_typical.html'>Sch_typ</a>| | 3.27 |  | |
| | | |<a href='results/dc_Sch_etc.html'>Sch_etc</a>|2.90 | 3.27 | 3.75 | |
| | | |<a href='results/dc_Sch_mc.html'>Sch_3std</a>|2.78 | 3.27 | 3.77 | |

