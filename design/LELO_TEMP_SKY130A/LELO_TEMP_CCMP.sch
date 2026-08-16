v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
C {devices/iopin.sym} 0 0 0 0 {name=p0 lab=CMPO_A}
C {devices/iopin.sym} 0 20 0 0 {name=p1 lab=CMPO_B}
C {devices/iopin.sym} 0 40 0 0 {name=p2 lab=IBP_1U<0>}
C {devices/iopin.sym} 0 60 0 0 {name=p3 lab=IBP_1U<1>}
C {devices/iopin.sym} 0 80 0 0 {name=p4 lab=IBP_1U<2>}
C {devices/iopin.sym} 0 100 0 0 {name=p5 lab=IBP_1U<3>}
C {devices/iopin.sym} 0 120 0 0 {name=p6 lab=PWRUP_B_1V8}
C {devices/iopin.sym} 0 140 0 0 {name=p7 lab=PWRUP_N_1V8}
C {devices/iopin.sym} 0 160 0 0 {name=p8 lab=RST_A}
C {devices/iopin.sym} 0 180 0 0 {name=p9 lab=RST_B}
C {devices/iopin.sym} 0 200 0 0 {name=p10 lab=VC}
C {devices/iopin.sym} 0 220 0 0 {name=p11 lab=VDD_1V8}
C {devices/iopin.sym} 0 240 0 0 {name=p12 lab=VSS}
C {LELO_TEMP_SKY130A/LELOTEMP_CCMPR.sym} 400 0 0 0 {name=Xx2_ccmp}
N 230.0 -40.0 250.0 -40.0 {lab=IBP_1U[3:2]}
C {devices/lab_pin.sym} 230.0 -40.0 0 0 {name=l0 sig_type=std_logic lab=IBP_1U[3:2] }
N 230.0 -60.0 250.0 -60.0 {lab=VDD_1V8}
C {devices/lab_pin.sym} 230.0 -60.0 0 0 {name=l1 sig_type=std_logic lab=VDD_1V8 }
N 230.0 -20.0 250.0 -20.0 {lab=PWRUP_N_1V8}
C {devices/lab_pin.sym} 230.0 -20.0 0 0 {name=l2 sig_type=std_logic lab=PWRUP_N_1V8 }
N 230.0 0.0 250.0 0.0 {lab=PWRUP_B_1V8}
C {devices/lab_pin.sym} 230.0 0.0 0 0 {name=l3 sig_type=std_logic lab=PWRUP_B_1V8 }
N 570.0 -60.0 550.0 -60.0 {lab=CMPO_A}
C {devices/lab_pin.sym} 570.0 -60.0 2 0 {name=l4 sig_type=std_logic lab=CMPO_A }
N 230.0 20.0 250.0 20.0 {lab=VC}
C {devices/lab_pin.sym} 230.0 20.0 0 0 {name=l5 sig_type=std_logic lab=VC }
N 230.0 40.0 250.0 40.0 {lab=RST_B}
C {devices/lab_pin.sym} 230.0 40.0 0 0 {name=l6 sig_type=std_logic lab=RST_B }
N 230.0 60.0 250.0 60.0 {lab=VSS}
C {devices/lab_pin.sym} 230.0 60.0 0 0 {name=l7 sig_type=std_logic lab=VSS }
C {LELO_TEMP_SKY130A/LELOTEMP_CCMPR.sym} 400 220.0 0 0 {name=Xx3_ccmp}
N 230.0 180.0 250.0 180.0 {lab=IBP_1U[1:0]}
C {devices/lab_pin.sym} 230.0 180.0 0 0 {name=l8 sig_type=std_logic lab=IBP_1U[1:0] }
N 230.0 160.0 250.0 160.0 {lab=VDD_1V8}
C {devices/lab_pin.sym} 230.0 160.0 0 0 {name=l9 sig_type=std_logic lab=VDD_1V8 }
N 230.0 200.0 250.0 200.0 {lab=PWRUP_N_1V8}
C {devices/lab_pin.sym} 230.0 200.0 0 0 {name=l10 sig_type=std_logic lab=PWRUP_N_1V8 }
N 230.0 220.0 250.0 220.0 {lab=PWRUP_B_1V8}
C {devices/lab_pin.sym} 230.0 220.0 0 0 {name=l11 sig_type=std_logic lab=PWRUP_B_1V8 }
N 570.0 160.0 550.0 160.0 {lab=CMPO_B}
C {devices/lab_pin.sym} 570.0 160.0 2 0 {name=l12 sig_type=std_logic lab=CMPO_B }
N 230.0 240.0 250.0 240.0 {lab=VC}
C {devices/lab_pin.sym} 230.0 240.0 0 0 {name=l13 sig_type=std_logic lab=VC }
N 230.0 260.0 250.0 260.0 {lab=RST_A}
C {devices/lab_pin.sym} 230.0 260.0 0 0 {name=l14 sig_type=std_logic lab=RST_A }
N 230.0 280.0 250.0 280.0 {lab=VSS}
C {devices/lab_pin.sym} 230.0 280.0 0 0 {name=l15 sig_type=std_logic lab=VSS }
