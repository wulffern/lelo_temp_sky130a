v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
C {devices/iopin.sym} 0 0 0 0 {name=p0 lab=A1}
C {devices/iopin.sym} 0 20 0 0 {name=p1 lab=B1}
C {devices/iopin.sym} 0 40 0 0 {name=p2 lab=A2}
C {devices/iopin.sym} 0 60 0 0 {name=p3 lab=B2}
C {LELO_TEMP_SKY130A/REYATR_CAPX1.sym} 400 0 0 0 {name=XXC1}
N 400.0 -80.0 400.0 -60.0 {lab=A1}
C {devices/lab_pin.sym} 400.0 -80.0 3 0 {name=l0 sig_type=std_logic lab=A1 }
N 400.0 30.0 400.0 10.0 {lab=B1}
C {devices/lab_pin.sym} 400.0 30.0 1 0 {name=l1 sig_type=std_logic lab=B1 }
C {LELO_TEMP_SKY130A/REYATR_CAPX1.sym} 400 180.0 0 0 {name=XXC2}
N 400.0 100.0 400.0 120.0 {lab=A2}
C {devices/lab_pin.sym} 400.0 100.0 3 0 {name=l2 sig_type=std_logic lab=A2 }
N 400.0 210.0 400.0 190.0 {lab=B2}
C {devices/lab_pin.sym} 400.0 210.0 1 0 {name=l3 sig_type=std_logic lab=B2 }
