v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 260 -200 430 -200 {lab=IBP_1U[0]}
N 430 -140 430 -110 {lab=VSS}
N 260 -110 430 -110 {lab=VSS}
N 260 -130 260 -110 {lab=VSS}
N 390 -170 430 -170 {lab=VSS}
N 390 -170 390 -110 {lab=VSS}
N 320 -230 570 -230 {lab=IBP_1U[0]}
N 660 -300 660 -280 {lab=PWRUP_B_1V8}
N 680 -300 680 -280 {lab=PWRUP_N_1V8}
N 700 -300 700 -280 {lab=IBP_1U[1]}
N 540 -250 570 -250 {lab=VDD_1V8}
N 540 -210 570 -210 {lab=VC}
N 540 -190 570 -190 {lab=VSS}
N 470 -170 510 -170 {lab=RST}
N 320 -230 320 -200 {lab=IBP_1U[0]}
N 160 -160 190 -160 {lab=VSS}
N 190 -160 190 -110 {lab=VSS}
N 160 -110 190 -110 {lab=VSS}
N 160 -130 160 -110 {lab=VSS}
N 160 -200 160 -190 {lab=IBP_1U[0]}
N 160 -200 260 -200 {lab=IBP_1U[0]}
N 190 -110 260 -110 {lab=VSS}
N 100 -160 120 -160 {lab=PWRUP_N_1V8}
N 510 -150 510 -90 {lab=RST}
N 510 -170 510 -150 {lab=RST}
N 430 -110 540 -110 {lab=VSS}
N 540 -190 540 -110 {lab=VSS}
N 540 -310 540 -250 {lab=VDD_1V8}
N 120 -310 540 -310 {lab=VDD_1V8}
N 800 -220 950 -220 {lab=CMPO}
C {JNW_TR_SKY130A/JNWTR_CAPX1.sym} 260 -190 2 1 {name=xd1[4:0]}
C {JNW_ATR_SKY130A/JNWATR_NCH_2C5F0.sym} 470 -170 0 1 {name=xg1}
C {devices/lab_wire.sym} 320 -215 0 0 {name=p14 sig_type=std_logic lab=IBP_1U[0]}
C {devices/lab_wire.sym} 340 -110 0 0 {name=p16 sig_type=std_logic lab=VSS}
C {LELO_TEMP_SKY130A/LELOTEMP_CMP.sym} 720 -220 0 0 {name=x1_cmp}
C {devices/lab_wire.sym} 700 -300 1 0 {name=p23 sig_type=std_logic lab=IBP_1U[1]}
C {JNW_ATR_SKY130A/JNWATR_NCH_2C5F0.sym} 120 -160 0 0 {name=xg4}
C {devices/lab_wire.sym} 100 -160 1 0 {name=p35 sig_type=std_logic lab=PWRUP_N_1V8}
C {cborder/border_xs.sym} 0 10 0 0 { user="wulff" company="wulff"}
C {devices/ipin.sym} 120 -310 0 0 {name=p1 lab=VDD_1V8}
C {devices/ipin.sym} 660 -300 1 0 {name=p3 lab=PWRUP_B_1V8}
C {devices/ipin.sym} 680 -300 1 0 {name=p2 lab=PWRUP_N_1V8}
C {devices/ipin.sym} 120 -70 0 0 {name=p4 lab=VSS}
C {devices/ipin.sym} 120 -370 0 0 {name=p5 lab=IBP_1U[1:0]}
C {devices/opin.sym} 950 -220 0 0 {name=p6 lab=CMPO}
C {devices/ipin.sym} 540 -210 0 0 {name=p7 lab=VC}
C {devices/ipin.sym} 510 -90 3 0 {name=p8 lab=RST}
