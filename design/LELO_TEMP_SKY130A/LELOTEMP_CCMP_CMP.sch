v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
C {devices/iopin.sym} 0 0 0 0 {name=p0 lab=CMPO}
C {devices/iopin.sym} 0 20 0 0 {name=p1 lab=IBP_1U<0>}
C {devices/iopin.sym} 0 40 0 0 {name=p2 lab=IBP_1U<1>}
C {devices/iopin.sym} 0 60 0 0 {name=p3 lab=PWRUP_B_1V8}
C {devices/iopin.sym} 0 80 0 0 {name=p4 lab=PWRUP_N_1V8}
C {devices/iopin.sym} 0 100 0 0 {name=p5 lab=VC}
C {devices/iopin.sym} 0 120 0 0 {name=p6 lab=VDD_1V8}
C {devices/iopin.sym} 0 140 0 0 {name=p7 lab=VSS}
C {LELO_TEMP_SKY130A/LELOTEMP_CMP.sym} 400 0 0 0 {name=Xx1_cmp}
N 230.0 -30.0 250.0 -30.0 {lab=VDD_1V8}
C {devices/lab_pin.sym} 230.0 -30.0 0 0 {name=l0 sig_type=std_logic lab=VDD_1V8 }
N 230.0 -10.0 250.0 -10.0 {lab=IBP_1U<0>}
C {devices/lab_pin.sym} 230.0 -10.0 0 0 {name=l1 sig_type=std_logic lab=IBP_1U<0> }
N 500.0 0.0 480.0 0.0 {lab=CMPO}
C {devices/lab_pin.sym} 500.0 0.0 2 0 {name=l2 sig_type=std_logic lab=CMPO }
N 230.0 10.0 250.0 10.0 {lab=VC}
C {devices/lab_pin.sym} 230.0 10.0 0 0 {name=l3 sig_type=std_logic lab=VC }
N 230.0 30.0 250.0 30.0 {lab=VSS}
C {devices/lab_pin.sym} 230.0 30.0 0 0 {name=l4 sig_type=std_logic lab=VSS }
N 340.0 -80.0 340.0 -60.0 {lab=PWRUP_B_1V8}
C {devices/lab_pin.sym} 340.0 -80.0 3 0 {name=l5 sig_type=std_logic lab=PWRUP_B_1V8 }
N 360.0 -80.0 360.0 -60.0 {lab=PWRUP_N_1V8}
C {devices/lab_pin.sym} 360.0 -80.0 3 0 {name=l6 sig_type=std_logic lab=PWRUP_N_1V8 }
N 380.0 -80.0 380.0 -60.0 {lab=IBP_1U<1>}
C {devices/lab_pin.sym} 380.0 -80.0 3 0 {name=l7 sig_type=std_logic lab=IBP_1U<1> }
