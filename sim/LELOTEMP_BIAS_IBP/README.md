

#### Loop stability (lstb)

Check stability



|**Name**|**Parameter**|**Description**| |**Min**|**Typ**|**Max**| Unit|
|:---|:---|:---|---:|:---:|:---:|:---:| ---:|
|**Gain Margin**|**gm\_db** || **Spec**  | **-50.00** | **-10.00** | **-10.00** | **dB** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | -15.21 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|-23.43 | -15.39 | -12.64 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|-21.01 | -17.10 | -13.20 | |
|**DC gain**|**lf\_gain** || **Spec**  | **25.00** | **40.00** | **55.00** | **dB** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 42.73 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|39.81 | 42.69 | 43.82 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|40.40 | 42.87 | 45.34 | |
|**Phase Margin**|**pm\_deg** || **Spec**  | **45.00** | **60.00** | **90.00** |  |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 59.47 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|48.87 | 59.69 | 76.89 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|56.88 | 62.53 | 68.18 | |
|**Unity Gain Frequency**|**ug** || **Spec**  | **0.40** | **15.00** | **100.00** | **MHz** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 5.38 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|1.92 | 5.63 | 9.02 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|4.11 | 5.51 | 6.91 | |
|**PMOS gate**|**v(lpo)** || **Spec**  | **0.45** | **0.70** | **1.10** | **V** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 0.76 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|0.52 | 0.78 | 1.05 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|0.73 | 0.76 | 0.79 | |
|**Delta diode voltage**|**vd** || **Spec**  | **80.00** | **106.00** | **150.00** | **mV** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 109.24 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|84.62 | 115.01 | 145.74 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|104.90 | 108.98 | 113.05 | |
|**Output current**|**i(v1)** || **Spec**  | **0.50** | **1.00** | **2.00** | **uA** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 1.24 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|0.70 | 1.09 | 1.75 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|0.67 | 1.10 | 1.54 | |
|**VD Error**|**vdiff** || **Spec**  | **-6.00** | **0.00** | **6.00** | **mV** |
| | | |<a href='results/lstb_Sch_typical.html'>Sch_typ</a>| | 0.64 |  | |
| | | |<a href='results/lstb_Sch_etc.html'>Sch_etc</a>|0.25 | 0.60 | 1.02 | |
| | | |<a href='results/lstb_Sch_mc.html'>Sch_3std</a>|<span style='color:red'>**-32.30**</span> | -0.01 | <span style='color:red'>**32.29**</span> | |

#### Transient (tran)

Check settling time and current variation



|**Name**|**Parameter**|**Description**| |**Min**|**Typ**|**Max**| Unit|
|:---|:---|:---|---:|:---:|:---:|:---:| ---:|
||**t\_settle** || **Spec**  | **0.01** | **0.05** | **2.00** | **us** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 0.91 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|0.71 | 1.12 | <span style='color:red'>**2.23**</span> | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|0.68 | 0.91 | 1.13 | |
||**i0** || **Spec**  | **0.500** | **1.000** | **2.000** | **uA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 1.153 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|0.806 | 1.162 | 1.657 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|0.690 | 1.139 | 1.588 | |
||**i1** || **Spec**  | **0.500** | **1.000** | **2.000** | **uA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 1.152 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|0.805 | 1.162 | 1.657 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|0.697 | 1.146 | 1.594 | |
||**i2** || **Spec**  | **0.500** | **1.000** | **2.000** | **uA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 1.152 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|0.804 | 1.162 | 1.656 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|0.726 | 1.131 | 1.537 | |
||**i3** || **Spec**  | **0.500** | **1.000** | **2.000** | **uA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 1.152 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|0.804 | 1.161 | 1.656 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|0.664 | 1.152 | 1.639 | |
||**idd** || **Spec**  | **5.000** | **30.000** | **60.000** | **uA** |
| | | |<a href='results/tran_Sch_typical.html'>Sch_typ</a>| | 29.134 |  | |
| | | |<a href='results/tran_Sch_etc.html'>Sch_etc</a>|15.579 | 30.086 | 48.825 | |
| | | |<a href='results/tran_Sch_mc.html'>Sch_3std</a>|23.875 | 28.985 | 34.095 | |

#### DC (dc)

Check temperature performance



|**Name**|**Parameter**|**Description**| |**Min**|**Typ**|**Max**| Unit|
|:---|:---|:---|---:|:---:|:---:|:---:| ---:|
||**ibp\_err\_max** || **Spec**  | **-30.00** | **0.00** | **20.00** | **nA** |
| | | |<a href='results/dc_Sch_typical.html'>Sch_typ</a>| | 8.23 |  | |
| | | |<a href='results/dc_Sch_etc.html'>Sch_etc</a>|7.33 | 8.26 | 9.40 | |
| | | |<a href='results/dc_Sch_mc.html'>Sch_3std</a>|5.26 | 8.35 | 11.45 | |
||**ibp\_err\_min** || **Spec**  | **-30.00** | **0.00** | **20.00** | **nA** |
| | | |<a href='results/dc_Sch_typical.html'>Sch_typ</a>| | -18.01 |  | |
| | | |<a href='results/dc_Sch_etc.html'>Sch_etc</a>|-20.64 | -18.04 | -15.92 | |
| | | |<a href='results/dc_Sch_mc.html'>Sch_3std</a>|<span style='color:red'>**-35.11**</span> | -18.10 | -1.08 | |
||**imax** || **Spec**  | **0.50** | **0.00** | **2.00** | **uA** |
| | | |<a href='results/dc_Sch_typical.html'>Sch_typ</a>| | 1.45 |  | |
| | | |<a href='results/dc_Sch_etc.html'>Sch_etc</a>|1.28 | 1.45 | 1.66 | |
| | | |<a href='results/dc_Sch_mc.html'>Sch_3std</a>|0.99 | 1.43 | 1.87 | |
||**imin** || **Spec**  | **0.50** | **0.00** | **2.00** | **uA** |
| | | |<a href='results/dc_Sch_typical.html'>Sch_typ</a>| | 0.91 |  | |
| | | |<a href='results/dc_Sch_etc.html'>Sch_etc</a>|0.81 | 0.91 | 1.04 | |
| | | |<a href='results/dc_Sch_mc.html'>Sch_3std</a>|<span style='color:red'>**0.46**</span> | 0.90 | 1.33 | |
||**a\_per\_c** || **Spec**  | **1.00** | **3.00** | **5.00** | **nA** |
| | | |<a href='results/dc_Sch_typical.html'>Sch_typ</a>| | 3.25 |  | |
| | | |<a href='results/dc_Sch_etc.html'>Sch_etc</a>|2.89 | 3.25 | 3.73 | |
| | | |<a href='results/dc_Sch_mc.html'>Sch_3std</a>|2.84 | 3.23 | 3.62 | |

