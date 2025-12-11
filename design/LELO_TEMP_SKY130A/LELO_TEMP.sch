v {xschem version=3.4.6 file_version=1.2}
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
N 170 -520 340 -520 {lab=IBP_1U[0]}
N 340 -460 340 -430 {lab=VSS}
N 170 -430 340 -430 {lab=VSS}
N 170 -450 170 -430 {lab=VSS}
N 300 -490 340 -490 {lab=VSS}
N 300 -490 300 -430 {lab=VSS}
N 700 -570 830 -570 {lab=VSS}
N 700 -650 830 -650 {lab=VDD_1V8}
N 770 -610 790 -610 {lab=#net1}
N 430 -580 430 -430 {lab=VSS}
N 340 -430 430 -430 {lab=VSS}
N 430 -880 430 -640 {lab=VDD_1V8}
N 430 -880 700 -880 {lab=VDD_1V8}
N 700 -880 700 -650 {lab=VDD_1V8}
N 1220 -670 1280 -670 {lab=OSC_TEMP_1V8}
N 1210 -840 1250 -840 {lab=OSC_TEMP_1V8}
N 1250 -840 1250 -670 {lab=OSC_TEMP_1V8}
N 1080 -840 1130 -840 {lab=#net2}
N 1080 -840 1080 -670 {lab=#net2}
N 1170 -800 1220 -800 {lab=VSS}
N 180 -620 430 -620 {lab=IBP_1U[0]}
N 180 -620 180 -520 {lab=IBP_1U[0]}
N 350 -600 430 -600 {lab=VC}
N 1080 -670 1120 -670 {lab=#net2}
N 1180 -580 1180 -530 {lab=VSS}
N 1180 -750 1180 -700 {lab=VDD_1V8}
N 1180 -750 1220 -750 {lab=VDD_1V8}
N 1150 -580 1150 -530 {lab=VDD_1V8}
N 700 -570 700 -430 {lab=VSS}
N 430 -430 700 -430 {lab=VSS}
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
N 520 -690 520 -670 {lab=PWRUP_B_1V8}
N 540 -690 540 -670 {lab=PWRUP_N_1V8}
N 560 -690 560 -670 {lab=IBP_1U[3:1]}
N 660 -610 690 -610 {lab=CMPO}
N 870 -610 940 -610 {lab=CLK}
N 700 -430 700 -420 {lab=VSS}
N 100 -880 430 -880 {lab=VDD_1V8}
N 700 -880 1170 -880 {lab=VDD_1V8}
N 380 -490 880 -490 {lab=RST}
N 920 -450 1050 -450 {lab=VSS}
N 920 -530 1050 -530 {lab=VDD_1V8}
N 960 -490 980 -490 {lab=#net3}
N 980 -880 980 -530 {lab=VDD_1V8}
N 700 -450 920 -450 {lab=VSS}
N 940 -610 1120 -610 {lab=CLK}
N 1060 -490 1080 -490 {lab=CLK}
N 1080 -610 1080 -490 {lab=CLK}
C {cborder/border_xs.sym} 150 -160 0 0 { user="wulff" company="wulff"}
C {devices/ipin.sym} 100 -880 0 0 {name=p1 lab=VDD_1V8}
C {devices/ipin.sym} 100 -220 0 0 {name=p2 lab=VSS}
C {devices/ipin.sym} 100 -300 0 0 {name=p3 lab=PWRUP_1V8}
C {devices/opin.sym} 1270 -670 0 0 {name=p4 lab=OSC_TEMP_1V8}
C {LELO_TEMP_SKY130A/LELOTEMP_BIAS_IBP.sym} 660 -290 0 0 {name=x1_ibp}
C {devices/lab_wire.sym} 840 -300 0 0 {name=p8 sig_type=std_logic lab=LPI}
C {devices/lab_wire.sym} 840 -260 0 0 {name=p9 sig_type=std_logic lab=VC}
C {devices/lab_wire.sym} 840 -320 0 1 {name=p10 sig_type=std_logic lab=IBP_1U[3:0]}
C {JNW_TR_SKY130A/JNWTR_CAPX1.sym} 170 -510 2 1 {name=xd1[9:0]}
C {JNW_ATR_SKY130A/JNWATR_NCH_4C5F0.sym} 380 -490 0 1 {name=xg3[1:0]}
C {JNW_TR_SKY130A/JNWTR_IVX1_CV.sym} 690 -610 0 0 {name=x7 }
C {JNW_TR_SKY130A/JNWTR_IVX1_CV.sym} 790 -610 0 0 {name=x8 }
C {JNW_TR_SKY130A/JNWTR_IVX1_CV.sym} 1210 -840 0 1 {name=x10 }
C {devices/lab_wire.sym} 1220 -800 0 1 {name=p13 sig_type=std_logic lab=VSS}
C {devices/lab_wire.sym} 270 -520 0 0 {name=p14 sig_type=std_logic lab=IBP_1U[0]}
C {devices/lab_wire.sym} 350 -600 0 0 {name=p15 sig_type=std_logic lab=VC}
C {devices/lab_wire.sym} 410 -430 0 0 {name=p16 sig_type=std_logic lab=VSS}
C {devices/lab_wire.sym} 1180 -530 0 1 {name=p18 sig_type=std_logic lab=VSS}
C {devices/lab_wire.sym} 1220 -750 0 1 {name=p19 sig_type=std_logic lab=VDD_1V8}
C {JNW_TR_SKY130A/JNWTR_DFRNQNX1_CV.sym} 1120 -610 0 0 {name=x9 }
C {devices/lab_wire.sym} 1150 -530 1 1 {name=p17 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_wire.sym} 480 -320 0 0 {name=p5 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_wire.sym} 480 -260 0 0 {name=p6 sig_type=std_logic lab=VSS}
C {JNW_TR_SKY130A/JNWTR_IVX1_CV.sym} 110 -300 0 0 {name=x6 }
C {devices/lab_pin.sym} 150 -250 0 1 {name=l13 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 150 -350 0 1 {name=l14 sig_type=std_logic lab=VDD_1V8}
C {JNW_TR_SKY130A/JNWTR_IVX1_CV.sym} 210 -300 0 0 {name=x2 }
C {devices/lab_pin.sym} 250 -250 0 1 {name=l1 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 250 -350 0 1 {name=l2 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_wire.sym} 400 -280 0 0 {name=p7 sig_type=std_logic lab=PWRUP_N_1V8}
C {devices/lab_wire.sym} 540 -690 1 0 {name=p20 sig_type=std_logic lab=PWRUP_N_1V8}
C {devices/lab_wire.sym} 400 -300 0 0 {name=p21 sig_type=std_logic lab=PWRUP_B_1V8}
C {devices/lab_wire.sym} 520 -690 1 0 {name=p22 sig_type=std_logic lab=PWRUP_B_1V8}
C {LELO_TEMP_SKY130A/LELOTEMP_CMP.sym} 580 -610 0 0 {name=x1_cmp}
C {devices/lab_wire.sym} 560 -690 1 0 {name=p23 sig_type=std_logic lab=IBP_1U[3:1]}
C {devices/lab_wire.sym} 670 -610 1 0 {name=p24 sig_type=std_logic lab=CMPO}
C {devices/lab_wire.sym} 530 -490 1 0 {name=p25 sig_type=std_logic lab=RST}
C {devices/lab_wire.sym} 880 -610 0 1 {name=p27 sig_type=std_logic lab=CLK}
C {JNW_TR_SKY130A/JNWTR_IVX1_CV.sym} 1060 -490 0 1 {name=x1 }
C {JNW_TR_SKY130A/JNWTR_IVX1_CV.sym} 960 -490 0 1 {name=x3 }
