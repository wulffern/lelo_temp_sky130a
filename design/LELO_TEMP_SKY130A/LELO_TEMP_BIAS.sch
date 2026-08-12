v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
C {devices/iopin.sym} 0 0 0 0 {name=p0 lab=IBP_1U<0>}
C {devices/iopin.sym} 0 20 0 0 {name=p1 lab=IBP_1U<1>}
C {devices/iopin.sym} 0 40 0 0 {name=p2 lab=IBP_1U<2>}
C {devices/iopin.sym} 0 60 0 0 {name=p3 lab=IBP_1U<3>}
C {devices/iopin.sym} 0 80 0 0 {name=p4 lab=PWRUP_B_1V8}
C {devices/iopin.sym} 0 100 0 0 {name=p5 lab=PWRUP_N_1V8}
C {devices/iopin.sym} 0 120 0 0 {name=p6 lab=VC}
C {devices/iopin.sym} 0 140 0 0 {name=p7 lab=VDD_1V8}
C {devices/iopin.sym} 0 160 0 0 {name=p8 lab=VSS}
C {LELO_TEMP_SKY130A/LELOTEMP_BIAS_IBP.sym} 400 0 0 0 {name=Xx1_ibp}
N 230.0 -30.0 250.0 -30.0 {lab=VDD_1V8}
C {devices/lab_pin.sym} 230.0 -30.0 0 0 {name=l0 sig_type=std_logic lab=VDD_1V8 }
N 570.0 -10.0 550.0 -10.0 {lab=LPI}
C {devices/lab_pin.sym} 570.0 -10.0 2 0 {name=l1 sig_type=std_logic lab=LPI }
N 570.0 -30.0 550.0 -30.0 {lab=IBP_1U[3:0]}
C {devices/lab_pin.sym} 570.0 -30.0 2 0 {name=l2 sig_type=std_logic lab=IBP_1U[3:0] }
N 570.0 10.0 550.0 10.0 {lab=LPI}
C {devices/lab_pin.sym} 570.0 10.0 2 0 {name=l3 sig_type=std_logic lab=LPI }
N 570.0 30.0 550.0 30.0 {lab=VC}
C {devices/lab_pin.sym} 570.0 30.0 2 0 {name=l4 sig_type=std_logic lab=VC }
N 230.0 -10.0 250.0 -10.0 {lab=PWRUP_B_1V8}
C {devices/lab_pin.sym} 230.0 -10.0 0 0 {name=l5 sig_type=std_logic lab=PWRUP_B_1V8 }
N 230.0 30.0 250.0 30.0 {lab=VSS}
C {devices/lab_pin.sym} 230.0 30.0 0 0 {name=l6 sig_type=std_logic lab=VSS }
N 230.0 10.0 250.0 10.0 {lab=PWRUP_N_1V8}
C {devices/lab_pin.sym} 230.0 10.0 0 0 {name=l7 sig_type=std_logic lab=PWRUP_N_1V8 }
