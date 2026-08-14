v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
C {devices/iopin.sym} 0 0 0 0 {name=p0 lab=VD1}
C {devices/iopin.sym} 0 20 0 0 {name=p1 lab=VD2}
C {devices/iopin.sym} 0 40 0 0 {name=p2 lab=VSS}
C {LELO_TEMP_SKY130A/LELOTEMP_BIPOLAR.sym} 400 0 0 0 {name=Xxe1}
N 600.0 -100.0 580.0 -100.0 {lab=VD2}
C {devices/lab_pin.sym} 600.0 -100.0 2 0 {name=l0 sig_type=std_logic lab=VD2 }
N 220.0 -100.0 240.0 -100.0 {lab=VD1}
C {devices/lab_pin.sym} 220.0 -100.0 0 0 {name=l1 sig_type=std_logic lab=VD1 }
N 180.0 10.0 200.0 10.0 {lab=VSS}
C {devices/lab_pin.sym} 180.0 10.0 0 0 {name=l2 sig_type=std_logic lab=VSS }
