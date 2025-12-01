v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 90 -130 200 -130 {lab=VSS}
N 130 -810 190 -810 {lab=VDD_1V8}
N 190 -810 590 -810 {lab=VDD_1V8}
N 590 -810 630 -810 {lab=VDD_1V8}
N 530 -530 690 -530 {lab=VDD_1V8}
N 530 -580 530 -570 {lab=VS}
N 530 -580 600 -580 {lab=VS}
N 530 -570 530 -560 {lab=VS}
N 600 -580 690 -580 {lab=VS}
N 690 -580 690 -570 {lab=VS}
N 690 -570 690 -560 {lab=VS}
N 490 -130 530 -130 {lab=VSS}
N 530 -130 690 -130 {lab=VSS}
N 200 -130 490 -130 {lab=VSS}
N 670 -810 670 -530 {lab=VDD_1V8}
N 630 -810 670 -810 {lab=VDD_1V8}
N 140 -760 170 -760 {lab=VDD_1V8}
N 140 -810 140 -760 {lab=VDD_1V8}
N 170 -810 170 -790 {lab=VDD_1V8}
N 860 -760 860 -710 {lab=#net1}
N 900 -760 940 -760 {lab=VDD_1V8}
N 940 -810 940 -760 {lab=VDD_1V8}
N 670 -810 940 -810 {lab=VDD_1V8}
N 900 -810 900 -790 {lab=VDD_1V8}
N 900 -240 920 -240 {lab=VSS}
N 690 -130 920 -130 {lab=VSS}
N 730 -240 860 -240 {lab=VD2}
N 670 -240 690 -240 {lab=VSS}
N 450 -240 490 -240 {lab=VD1}
N 530 -240 560 -240 {lab=VSS}
N 170 -730 170 -710 {lab=#net1}
N 170 -710 860 -710 {lab=#net1}
N 210 -760 210 -710 {lab=#net1}
N 170 -710 170 -270 {lab=#net1}
N 210 -240 450 -240 {lab=VD1}
N 140 -240 170 -240 {lab=VSS}
N 470 -300 530 -300 {lab=VD1}
N 470 -300 470 -240 {lab=VD1}
N 690 -300 760 -300 {lab=VD2}
N 760 -300 760 -240 {lab=VD2}
N 900 -730 900 -270 {lab=VO}
N 900 -380 930 -380 {lab=VO}
N 730 -530 750 -530 {lab=VIP}
N 470 -530 490 -530 {lab=VIN}
N 620 -590 620 -580 {lab=VS}
N 360 -760 400 -760 {lab=VDD_1V8}
N 400 -810 400 -760 {lab=VDD_1V8}
N 360 -810 360 -790 {lab=VDD_1V8}
N 360 -730 360 -710 {lab=#net1}
N 300 -760 320 -760 {lab=PWRUP_1V8}
N 620 -600 620 -590 {lab=VS}
N 300 -690 550 -690 {lab=PWRUP_1V8}
N 800 -760 830 -760 {lab=VDD_1V8}
N 830 -810 830 -760 {lab=VDD_1V8}
N 800 -810 800 -790 {lab=VDD_1V8}
N 800 -730 800 -670 {lab=VO}
N 800 -670 900 -670 {lab=VO}
N 760 -760 760 -690 {lab=PWRUP_1V8}
N 550 -690 760 -690 {lab=PWRUP_1V8}
N 140 -240 140 -130 {lab=VSS}
N 170 -210 170 -130 {lab=VSS}
N 530 -210 530 -130 {lab=VSS}
N 690 -210 690 -130 {lab=VSS}
N 670 -240 670 -130 {lab=VSS}
N 560 -240 560 -130 {lab=VSS}
N 920 -240 920 -130 {lab=VSS}
N 900 -210 900 -130 {lab=VSS}
N 340 -180 370 -180 {lab=VSS}
N 370 -180 370 -130 {lab=VSS}
N 340 -150 340 -130 {lab=VSS}
N 830 -180 860 -180 {lab=VSS}
N 860 -180 860 -130 {lab=VSS}
N 830 -150 830 -130 {lab=VSS}
N 830 -240 830 -210 {lab=VD2}
N 340 -240 340 -210 {lab=VD1}
N 530 -500 530 -270 {lab=VD1}
N 690 -500 690 -270 {lab=VD2}
N 300 -760 300 -690 {lab=PWRUP_1V8}
N 240 -690 300 -690 {lab=PWRUP_1V8}
N 240 -690 240 -410 {lab=PWRUP_1V8}
N 110 -410 240 -410 {lab=PWRUP_1V8}
N 110 -450 290 -450 {lab=PWRUP_N_1V8}
N 290 -450 300 -450 {lab=PWRUP_N_1V8}
N 300 -450 300 -180 {lab=PWRUP_N_1V8}
N 300 -450 790 -450 {lab=PWRUP_N_1V8}
N 790 -450 790 -180 {lab=PWRUP_N_1V8}
N 620 -730 620 -600 {lab=VS}
C {devices/opin.sym} 930 -380 0 0 {name=p1 lab=VO}
C {devices/ipin.sym} 750 -530 2 0 {name=p2 lab=VIP}
C {devices/ipin.sym} 470 -530 2 1 {name=p3 lab=VIN}
C {devices/ipin.sym} 130 -810 2 1 {name=p4 lab=VDD_1V8}
C {devices/ipin.sym} 90 -130 2 1 {name=p5 lab=VSS}
C {JNW_ATR_SKY130A/JNWATR_PCH_12C1F2.sym} 490 -530 0 0 {name=xba1[7:0]}
C {JNW_ATR_SKY130A/JNWATR_PCH_12C1F2.sym} 730 -530 0 1 {name=xbb2[7:0]}
C {JNW_ATR_SKY130A/JNWATR_NCH_4C5F0.sym} 490 -240 0 0 {name=xca1[3:0]}
C {JNW_ATR_SKY130A/JNWATR_NCH_4C5F0.sym} 730 -240 0 1 {name=xcb2[3:0]}
C {cborder/border_xs.sym} 270 0 0 0 {user="Carsten Wulff" company="Carsten Wulff Software"}
C {devices/lab_wire.sym} 530 -300 0 0 {name=p8 sig_type=std_logic lab=VD1}
C {JNW_ATR_SKY130A/JNWATR_PCH_12C5F0.sym} 210 -760 0 1 {name=xba6}
C {JNW_ATR_SKY130A/JNWATR_NCH_4C5F0.sym} 210 -240 0 1 {name=xca3}
C {JNW_ATR_SKY130A/JNWATR_PCH_12C5F0.sym} 860 -760 0 0 {name=xbb3}
C {JNW_ATR_SKY130A/JNWATR_NCH_4C5F0.sym} 860 -240 0 0 {name=xcb4}
C {devices/lab_wire.sym} 690 -300 0 1 {name=p6 sig_type=std_logic lab=VD2}
C {devices/ipin.sym} 110 -450 2 1 {name=p9 lab=PWRUP_N_1V8}
C {JNW_ATR_SKY130A/JNWATR_PCH_12C5F0.sym} 320 -760 0 0 {name=xba7}
C {JNW_ATR_SKY130A/JNWATR_PCH_12C5F0.sym} 760 -760 0 0 {name=xba2}
C {JNW_ATR_SKY130A/JNWATR_NCH_4C5F0.sym} 300 -180 0 0 {name=xca1}
C {JNW_ATR_SKY130A/JNWATR_NCH_4C5F0.sym} 790 -180 0 0 {name=xca2}
C {devices/ipin.sym} 110 -410 2 1 {name=p10 lab=PWRUP_1V8}
C {devices/ipin.sym} 620 -730 3 1 {name=p11 lab=IBP_1U}
