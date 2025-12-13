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
N 170 -730 340 -730 {lab=IBP_1U[0]}
N 340 -670 340 -640 {lab=VSS}
N 170 -640 340 -640 {lab=VSS}
N 170 -660 170 -640 {lab=VSS}
N 300 -700 340 -700 {lab=VSS}
N 300 -700 300 -640 {lab=VSS}
N 230 -760 480 -760 {lab=IBP_1U[0]}
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
N 570 -830 570 -810 {lab=PWRUP_B_1V8}
N 590 -830 590 -810 {lab=PWRUP_N_1V8}
N 610 -830 610 -810 {lab=IBP_1U[2]}
N 450 -780 480 -780 {lab=VDD_1V8}
N 450 -740 480 -740 {lab=VC}
N 450 -720 480 -720 {lab=VSS}
N 380 -700 420 -700 {lab=RST_A}
N 230 -760 230 -730 {lab=IBP_1U[0]}
N 170 -480 340 -480 {lab=IBP_1U[1]}
N 340 -420 340 -390 {lab=VSS}
N 170 -390 340 -390 {lab=VSS}
N 170 -410 170 -390 {lab=VSS}
N 300 -450 340 -450 {lab=VSS}
N 300 -450 300 -390 {lab=VSS}
N 230 -510 480 -510 {lab=IBP_1U[1]}
N 570 -580 570 -560 {lab=PWRUP_B_1V8}
N 590 -580 590 -560 {lab=PWRUP_N_1V8}
N 610 -580 610 -560 {lab=IBP_1U[3]}
N 450 -530 480 -530 {lab=VDD_1V8}
N 450 -490 480 -490 {lab=VC}
N 450 -470 480 -470 {lab=VSS}
N 380 -450 420 -450 {lab=RST_B}
N 230 -510 230 -480 {lab=IBP_1U[1]}
N 750 -500 890 -500 {lab=CMPO_B}
N 980 -590 980 -510 {lab=RST_A}
N 880 -640 980 -590 {lab=RST_A}
N 880 -730 880 -640 {lab=RST_A}
N 880 -730 890 -730 {lab=RST_A}
N 980 -740 980 -640 {lab=RST_B}
N 880 -600 980 -640 {lab=RST_B}
N 880 -600 880 -520 {lab=RST_B}
N 880 -520 890 -520 {lab=RST_B}
N 980 -740 1040 -740 {lab=RST_B}
N 980 -510 1040 -510 {lab=RST_A}
N 930 -780 950 -780 {lab=VDD_1V8}
N 930 -700 950 -700 {lab=VSS}
N 930 -470 950 -470 {lab=VSS}
N 930 -550 940 -550 {lab=VDD_1V8}
N 1130 -780 1150 -780 {lab=VDD_1V8}
N 1130 -700 1150 -700 {lab=VSS}
N 1040 -740 1090 -740 {lab=RST_B}
N 1170 -740 1230 -740 {lab=OSC_TEMP_1V8}
N 710 -500 750 -500 {lab=CMPO_B}
N 800 -710 820 -710 {lab=VSS}
N 800 -790 820 -790 {lab=VDD_1V8}
N 850 -750 890 -750 {lab=#net1}
N 710 -760 760 -760 {lab=CMPO_A}
N 710 -760 710 -750 {lab=CMPO_A}
N 760 -740 760 -690 {lab=PWRUP_N_1V8}
C {cborder/border_xs.sym} 150 -160 0 0 { user="wulff" company="wulff"}
C {devices/ipin.sym} 100 -880 0 0 {name=p1 lab=VDD_1V8}
C {devices/ipin.sym} 100 -220 0 0 {name=p2 lab=VSS}
C {devices/ipin.sym} 100 -300 0 0 {name=p3 lab=PWRUP_1V8}
C {devices/opin.sym} 1230 -740 0 0 {name=p4 lab=OSC_TEMP_1V8}
C {LELO_TEMP_SKY130A/LELOTEMP_BIAS_IBP.sym} 660 -290 0 0 {name=x1_ibp}
C {devices/lab_wire.sym} 840 -300 0 0 {name=p8 sig_type=std_logic lab=LPI}
C {devices/lab_wire.sym} 840 -260 0 0 {name=p9 sig_type=std_logic lab=VC}
C {devices/lab_wire.sym} 840 -320 0 1 {name=p10 sig_type=std_logic lab=IBP_1U[3:0]}
C {JNW_TR_SKY130A/JNWTR_CAPX1.sym} 170 -720 2 1 {name=xd1[4:0]}
C {JNW_ATR_SKY130A/JNWATR_NCH_4C5F0.sym} 380 -700 0 1 {name=xg1}
C {devices/lab_wire.sym} 230 -745 0 0 {name=p14 sig_type=std_logic lab=IBP_1U[0]}
C {devices/lab_wire.sym} 450 -740 0 0 {name=p15 sig_type=std_logic lab=VC}
C {devices/lab_wire.sym} 250 -640 0 0 {name=p16 sig_type=std_logic lab=VSS}
C {devices/lab_wire.sym} 480 -320 0 0 {name=p5 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_wire.sym} 480 -260 0 0 {name=p6 sig_type=std_logic lab=VSS}
C {JNW_TR_SKY130A/JNWTR_IVX1_CV.sym} 110 -300 0 0 {name=x6 }
C {devices/lab_pin.sym} 150 -250 0 1 {name=l13 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 150 -350 0 1 {name=l14 sig_type=std_logic lab=VDD_1V8}
C {JNW_TR_SKY130A/JNWTR_IVX1_CV.sym} 210 -300 0 0 {name=x2 }
C {devices/lab_pin.sym} 250 -250 0 1 {name=l1 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 250 -350 0 1 {name=l2 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_wire.sym} 400 -280 0 0 {name=p7 sig_type=std_logic lab=PWRUP_N_1V8}
C {devices/lab_wire.sym} 590 -830 1 0 {name=p20 sig_type=std_logic lab=PWRUP_N_1V8}
C {devices/lab_wire.sym} 400 -300 0 0 {name=p21 sig_type=std_logic lab=PWRUP_B_1V8}
C {devices/lab_wire.sym} 570 -830 1 0 {name=p22 sig_type=std_logic lab=PWRUP_B_1V8}
C {LELO_TEMP_SKY130A/LELOTEMP_CMP.sym} 630 -750 0 0 {name=x1_cmp}
C {devices/lab_wire.sym} 610 -830 1 0 {name=p23 sig_type=std_logic lab=IBP_1U[2]}
C {devices/lab_wire.sym} 710 -760 1 0 {name=p24 sig_type=std_logic lab=CMPO_A}
C {devices/lab_wire.sym} 410 -700 2 0 {name=p25 sig_type=std_logic lab=RST_A}
C {devices/lab_wire.sym} 450 -780 0 0 {name=p11 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_wire.sym} 450 -720 0 0 {name=p12 sig_type=std_logic lab=VSS}
C {JNW_TR_SKY130A/JNWTR_CAPX1.sym} 170 -470 2 1 {name=xd2[4:0]}
C {JNW_ATR_SKY130A/JNWATR_NCH_4C5F0.sym} 380 -450 0 1 {name=xg2}
C {devices/lab_wire.sym} 230 -495 0 0 {name=p13 sig_type=std_logic lab=IBP_1U[1]}
C {devices/lab_wire.sym} 450 -490 0 0 {name=p17 sig_type=std_logic lab=VC}
C {devices/lab_wire.sym} 250 -390 0 0 {name=p18 sig_type=std_logic lab=VSS}
C {devices/lab_wire.sym} 590 -580 1 0 {name=p19 sig_type=std_logic lab=PWRUP_N_1V8}
C {devices/lab_wire.sym} 570 -580 1 0 {name=p26 sig_type=std_logic lab=PWRUP_B_1V8}
C {LELO_TEMP_SKY130A/LELOTEMP_CMP.sym} 630 -500 0 0 {name=x1}
C {devices/lab_wire.sym} 610 -580 1 0 {name=p27 sig_type=std_logic lab=IBP_1U[3]}
C {devices/lab_wire.sym} 720 -500 1 0 {name=p28 sig_type=std_logic lab=CMPO_B}
C {devices/lab_wire.sym} 410 -450 2 0 {name=p29 sig_type=std_logic lab=RST_B}
C {devices/lab_wire.sym} 450 -530 0 0 {name=p30 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_wire.sym} 450 -470 0 0 {name=p31 sig_type=std_logic lab=VSS}
C {JNW_TR_SKY130A/JNWTR_NRX1_CV.sym} 890 -730 0 0 {name=x3 }
C {JNW_TR_SKY130A/JNWTR_NRX1_CV.sym} 890 -500 0 0 {name=x4 }
C {devices/lab_wire.sym} 1020 -740 2 0 {name=p32 sig_type=std_logic lab=RST_B}
C {devices/lab_wire.sym} 1040 -510 2 0 {name=p33 sig_type=std_logic lab=RST_A}
C {devices/lab_pin.sym} 940 -550 0 1 {name=l3 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} 950 -470 0 1 {name=l4 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 950 -780 0 1 {name=l5 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} 940 -700 0 1 {name=l6 sig_type=std_logic lab=VSS}
C {JNW_TR_SKY130A/JNWTR_BFX1_CV.sym} 1090 -740 0 0 {name=x5 }
C {devices/lab_pin.sym} 1150 -780 0 1 {name=l7 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} 1150 -700 0 1 {name=l8 sig_type=std_logic lab=VSS}
C {JNW_TR_SKY130A/JNWTR_ORX1_CV.sym} 760 -740 0 0 {name=x7 }
C {devices/lab_pin.sym} 820 -710 0 1 {name=l9 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 820 -790 0 1 {name=l10 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_wire.sym} 760 -690 3 0 {name=p34 sig_type=std_logic lab=PWRUP_N_1V8}
