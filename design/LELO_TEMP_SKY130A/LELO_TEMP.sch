v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 460 -300 510 -300 {lab=PWRUP_B_1V8}
N 810 -280 840 -280 {lab=LPI}
N 840 -300 840 -280 {lab=LPI}
N 810 -300 840 -300 {lab=LPI}
N 810 -260 840 -260 {lab=VC}
N 810 -320 840 -320 {lab=IBP_1U[3:0]}
N 480 -320 510 -320 {lab=VDD_1V8}
N 480 -260 510 -260 {lab=VSS}
N 150 -260 150 -250 {lab=VSS}
N 150 -350 150 -340 {lab=VDD_1V8}
N 250 -260 250 -250 {lab=VSS}
N 250 -350 250 -340 {lab=VDD_1V8}
N 190 -300 210 -300 {lab=PWRUP_N_1V8}
N 100 -300 110 -300 {lab=PWRUP_1V8}
N 290 -300 460 -300 {lab=PWRUP_B_1V8}
N 200 -300 200 -220 {lab=PWRUP_N_1V8}
N 200 -220 400 -220 {lab=PWRUP_N_1V8}
N 400 -280 400 -220 {lab=PWRUP_N_1V8}
N 400 -280 510 -280 {lab=PWRUP_N_1V8}
N 1070 -600 1070 -520 {lab=RST_A}
N 970 -650 1070 -600 {lab=RST_A}
N 970 -740 970 -650 {lab=RST_A}
N 970 -740 980 -740 {lab=RST_A}
N 1070 -750 1070 -650 {lab=RST_B}
N 970 -610 1070 -650 {lab=RST_B}
N 970 -610 970 -530 {lab=RST_B}
N 970 -530 980 -530 {lab=RST_B}
N 1070 -750 1130 -750 {lab=RST_B}
N 1070 -520 1130 -520 {lab=RST_A}
N 1020 -790 1040 -790 {lab=VDD_1V8}
N 1020 -710 1040 -710 {lab=VSS}
N 1020 -480 1040 -480 {lab=VSS}
N 1020 -560 1030 -560 {lab=VDD_1V8}
N 1220 -790 1240 -790 {lab=VDD_1V8}
N 1220 -710 1240 -710 {lab=VSS}
N 1130 -750 1180 -750 {lab=RST_B}
N 1260 -750 1320 -750 {lab=OSC_TEMP_1V8}
N 890 -720 910 -720 {lab=VSS}
N 890 -800 910 -800 {lab=VDD_1V8}
N 940 -760 980 -760 {lab=#net1}
N 850 -750 850 -700 {lab=PWRUP_N_1V8}
N 480 -770 510 -770 {lab=VDD_1V8}
N 480 -750 510 -750 {lab=IBP_1U[1:0]}
N 480 -730 510 -730 {lab=PWRUP_N_1V8}
N 480 -710 510 -710 {lab=PWRUP_B_1V8}
N 480 -690 510 -690 {lab=VC}
N 480 -670 510 -670 {lab=RST_A}
N 480 -650 510 -650 {lab=VSS}
N 810 -770 850 -770 {lab=CMPO_B}
N 810 -510 980 -510 {lab=CMPO_A}
N 480 -510 510 -510 {lab=VDD_1V8}
N 480 -490 510 -490 {lab=IBP_1U[3:2]}
N 480 -470 510 -470 {lab=PWRUP_N_1V8}
N 480 -450 510 -450 {lab=PWRUP_B_1V8}
N 480 -430 510 -430 {lab=VC}
N 480 -410 510 -410 {lab=RST_B}
N 480 -390 510 -390 {lab=VSS}
C {cborder/border_xs.sym} 150 -160 0 0 { user="wulff" company="wulff"}
C {devices/ipin.sym} 100 -700 0 0 {name=p1 lab=VDD_1V8}
C {devices/ipin.sym} 100 -200 0 0 {name=p2 lab=VSS}
C {devices/ipin.sym} 100 -300 0 0 {name=p3 lab=PWRUP_1V8}
C {devices/opin.sym} 1320 -750 0 0 {name=p4 lab=OSC_TEMP_1V8}
C {LELO_TEMP_SKY130A/LELOTEMP_BIAS_IBP.sym} 660 -290 0 0 {name=x1_ibp}
C {devices/lab_wire.sym} 840 -300 0 0 {name=p8 sig_type=std_logic lab=LPI}
C {devices/lab_wire.sym} 840 -260 0 0 {name=p9 sig_type=std_logic lab=VC}
C {devices/lab_wire.sym} 840 -320 0 1 {name=p10 sig_type=std_logic lab=IBP_1U[3:0]}
C {devices/lab_wire.sym} 480 -320 0 0 {name=p5 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_wire.sym} 480 -260 0 0 {name=p6 sig_type=std_logic lab=VSS}
C {JNW_TR_SKY130A/JNWTR_IVX1_CV.sym} 110 -300 0 0 {name=x6 }
C {devices/lab_pin.sym} 150 -250 0 1 {name=l13 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 150 -350 0 1 {name=l14 sig_type=std_logic lab=VDD_1V8}
C {JNW_TR_SKY130A/JNWTR_IVX1_CV.sym} 210 -300 0 0 {name=x2 }
C {devices/lab_pin.sym} 250 -250 0 1 {name=l1 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 250 -350 0 1 {name=l2 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_wire.sym} 430 -280 0 0 {name=p7 sig_type=std_logic lab=PWRUP_N_1V8}
C {devices/lab_wire.sym} 430 -300 0 0 {name=p21 sig_type=std_logic lab=PWRUP_B_1V8}
C {JNW_TR_SKY130A/JNWTR_NRX1_CV.sym} 980 -740 0 0 {name=x3 }
C {JNW_TR_SKY130A/JNWTR_NRX1_CV.sym} 980 -510 0 0 {name=x4 }
C {devices/lab_wire.sym} 1110 -750 2 0 {name=p32 sig_type=std_logic lab=RST_B}
C {devices/lab_wire.sym} 1130 -520 2 0 {name=p33 sig_type=std_logic lab=RST_A}
C {devices/lab_pin.sym} 1030 -560 0 1 {name=l3 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} 1040 -480 0 1 {name=l4 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 1040 -790 0 1 {name=l5 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} 1030 -710 0 1 {name=l6 sig_type=std_logic lab=VSS}
C {JNW_TR_SKY130A/JNWTR_BFX1_CV.sym} 1180 -750 0 0 {name=x5 }
C {devices/lab_pin.sym} 1240 -790 0 1 {name=l7 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} 1240 -710 0 1 {name=l8 sig_type=std_logic lab=VSS}
C {JNW_TR_SKY130A/JNWTR_ORX1_CV.sym} 850 -750 0 0 {name=x7 }
C {devices/lab_pin.sym} 910 -720 0 1 {name=l9 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 910 -800 0 1 {name=l10 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_wire.sym} 850 -700 3 0 {name=p34 sig_type=std_logic lab=PWRUP_N_1V8}
C {LELO_TEMP_SKY130A/LELOTEMP_CCMP.sym} 660 -710 0 0 {name=x3_ccmp}
C {LELO_TEMP_SKY130A/LELOTEMP_CCMP.sym} 660 -450 0 0 {name=x2_ccmp}
C {devices/lab_wire.sym} 480 -750 0 0 {name=p11 sig_type=std_logic lab=IBP_1U[1:0]}
C {devices/lab_wire.sym} 480 -490 0 0 {name=p12 sig_type=std_logic lab=IBP_1U[3:2]}
C {devices/lab_wire.sym} 480 -510 0 0 {name=p13 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_wire.sym} 480 -770 0 0 {name=p14 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_wire.sym} 480 -730 0 0 {name=p15 sig_type=std_logic lab=PWRUP_N_1V8}
C {devices/lab_wire.sym} 480 -470 0 0 {name=p16 sig_type=std_logic lab=PWRUP_N_1V8}
C {devices/lab_wire.sym} 480 -450 0 0 {name=p17 sig_type=std_logic lab=PWRUP_B_1V8}
C {devices/lab_wire.sym} 480 -710 0 0 {name=p18 sig_type=std_logic lab=PWRUP_B_1V8}
C {devices/lab_wire.sym} 480 -690 0 0 {name=p19 sig_type=std_logic lab=VC}
C {devices/lab_wire.sym} 480 -670 0 0 {name=p20 sig_type=std_logic lab=RST_A}
C {devices/lab_wire.sym} 480 -650 0 0 {name=p22 sig_type=std_logic lab=VSS}
C {devices/lab_wire.sym} 480 -430 0 0 {name=p23 sig_type=std_logic lab=VC}
C {devices/lab_wire.sym} 480 -410 0 0 {name=p24 sig_type=std_logic lab=RST_B}
C {devices/lab_wire.sym} 480 -390 0 0 {name=p25 sig_type=std_logic lab=VSS}
C {devices/lab_wire.sym} 860 -510 0 0 {name=p26 sig_type=std_logic lab=CMPO_A}
C {devices/lab_wire.sym} 840 -770 0 0 {name=p27 sig_type=std_logic lab=CMPO_B}
