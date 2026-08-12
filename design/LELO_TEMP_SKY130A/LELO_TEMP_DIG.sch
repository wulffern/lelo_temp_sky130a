v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
C {devices/iopin.sym} 0 0 0 0 {name=p0 lab=CMPO_A}
C {devices/iopin.sym} 0 20 0 0 {name=p1 lab=CMPO_B}
C {devices/iopin.sym} 0 40 0 0 {name=p2 lab=OSC_TEMP_1V8}
C {devices/iopin.sym} 0 60 0 0 {name=p3 lab=PWRUP_1V8}
C {devices/iopin.sym} 0 80 0 0 {name=p4 lab=PWRUP_B_1V8}
C {devices/iopin.sym} 0 100 0 0 {name=p5 lab=PWRUP_N_1V8}
C {devices/iopin.sym} 0 120 0 0 {name=p6 lab=RST_A}
C {devices/iopin.sym} 0 140 0 0 {name=p7 lab=RST_B}
C {devices/iopin.sym} 0 160 0 0 {name=p8 lab=VDD_1V8}
C {devices/iopin.sym} 0 180 0 0 {name=p9 lab=VSS}
C {JNW_TR_SKY130A/JNWTR_BFX1_CV.sym} 400 0 0 0 {name=Xx1}
N 380.0 0.0 400.0 0.0 {lab=CMPO_A}
C {devices/lab_pin.sym} 380.0 0.0 0 0 {name=l0 sig_type=std_logic lab=CMPO_A }
N 500.0 0.0 480.0 0.0 {lab=net2}
C {devices/lab_pin.sym} 500.0 0.0 2 0 {name=l1 sig_type=std_logic lab=net2 }
N 440.0 -60.0 440.0 -40.0 {lab=VDD_1V8}
C {devices/lab_pin.sym} 440.0 -60.0 3 0 {name=l2 sig_type=std_logic lab=VDD_1V8 }
N 440.0 60.0 440.0 40.0 {lab=VSS}
C {devices/lab_pin.sym} 440.0 60.0 1 0 {name=l3 sig_type=std_logic lab=VSS }
C {JNW_TR_SKY130A/JNWTR_IVX1_CV.sym} 400 190.0 0 0 {name=Xx2}
N 380.0 190.0 400.0 190.0 {lab=PWRUP_N_1V8}
C {devices/lab_pin.sym} 380.0 190.0 0 0 {name=l4 sig_type=std_logic lab=PWRUP_N_1V8 }
N 500.0 190.0 480.0 190.0 {lab=PWRUP_B_1V8}
C {devices/lab_pin.sym} 500.0 190.0 2 0 {name=l5 sig_type=std_logic lab=PWRUP_B_1V8 }
N 440.0 130.0 440.0 150.0 {lab=VDD_1V8}
C {devices/lab_pin.sym} 440.0 130.0 3 0 {name=l6 sig_type=std_logic lab=VDD_1V8 }
N 440.0 250.0 440.0 230.0 {lab=VSS}
C {devices/lab_pin.sym} 440.0 250.0 1 0 {name=l7 sig_type=std_logic lab=VSS }
C {JNW_TR_SKY130A/JNWTR_NRX1_CV.sym} 400 380.0 0 0 {name=Xx3}
N 380.0 360.0 400.0 360.0 {lab=net1}
C {devices/lab_pin.sym} 380.0 360.0 0 0 {name=l8 sig_type=std_logic lab=net1 }
N 380.0 380.0 400.0 380.0 {lab=RST_A}
C {devices/lab_pin.sym} 380.0 380.0 0 0 {name=l9 sig_type=std_logic lab=RST_A }
N 510.0 370.0 490.0 370.0 {lab=RST_B}
C {devices/lab_pin.sym} 510.0 370.0 2 0 {name=l10 sig_type=std_logic lab=RST_B }
N 440.0 310.0 440.0 330.0 {lab=VDD_1V8}
C {devices/lab_pin.sym} 440.0 310.0 3 0 {name=l11 sig_type=std_logic lab=VDD_1V8 }
N 440.0 430.0 440.0 410.0 {lab=VSS}
C {devices/lab_pin.sym} 440.0 430.0 1 0 {name=l12 sig_type=std_logic lab=VSS }
C {JNW_TR_SKY130A/JNWTR_NRX1_CV.sym} 400 570.0 0 0 {name=Xx4}
N 380.0 550.0 400.0 550.0 {lab=RST_B}
C {devices/lab_pin.sym} 380.0 550.0 0 0 {name=l13 sig_type=std_logic lab=RST_B }
N 380.0 570.0 400.0 570.0 {lab=net2}
C {devices/lab_pin.sym} 380.0 570.0 0 0 {name=l14 sig_type=std_logic lab=net2 }
N 510.0 560.0 490.0 560.0 {lab=RST_A}
C {devices/lab_pin.sym} 510.0 560.0 2 0 {name=l15 sig_type=std_logic lab=RST_A }
N 440.0 500.0 440.0 520.0 {lab=VDD_1V8}
C {devices/lab_pin.sym} 440.0 500.0 3 0 {name=l16 sig_type=std_logic lab=VDD_1V8 }
N 440.0 620.0 440.0 600.0 {lab=VSS}
C {devices/lab_pin.sym} 440.0 620.0 1 0 {name=l17 sig_type=std_logic lab=VSS }
C {JNW_TR_SKY130A/JNWTR_BFX1_CV.sym} 400 760.0 0 0 {name=Xx5}
N 380.0 760.0 400.0 760.0 {lab=RST_B}
C {devices/lab_pin.sym} 380.0 760.0 0 0 {name=l18 sig_type=std_logic lab=RST_B }
N 500.0 760.0 480.0 760.0 {lab=OSC_TEMP_1V8}
C {devices/lab_pin.sym} 500.0 760.0 2 0 {name=l19 sig_type=std_logic lab=OSC_TEMP_1V8 }
N 440.0 700.0 440.0 720.0 {lab=VDD_1V8}
C {devices/lab_pin.sym} 440.0 700.0 3 0 {name=l20 sig_type=std_logic lab=VDD_1V8 }
N 440.0 820.0 440.0 800.0 {lab=VSS}
C {devices/lab_pin.sym} 440.0 820.0 1 0 {name=l21 sig_type=std_logic lab=VSS }
C {JNW_TR_SKY130A/JNWTR_IVX1_CV.sym} 400 950.0 0 0 {name=Xx6}
N 380.0 950.0 400.0 950.0 {lab=PWRUP_1V8}
C {devices/lab_pin.sym} 380.0 950.0 0 0 {name=l22 sig_type=std_logic lab=PWRUP_1V8 }
N 500.0 950.0 480.0 950.0 {lab=PWRUP_N_1V8}
C {devices/lab_pin.sym} 500.0 950.0 2 0 {name=l23 sig_type=std_logic lab=PWRUP_N_1V8 }
N 440.0 890.0 440.0 910.0 {lab=VDD_1V8}
C {devices/lab_pin.sym} 440.0 890.0 3 0 {name=l24 sig_type=std_logic lab=VDD_1V8 }
N 440.0 1010.0 440.0 990.0 {lab=VSS}
C {devices/lab_pin.sym} 440.0 1010.0 1 0 {name=l25 sig_type=std_logic lab=VSS }
C {JNW_TR_SKY130A/JNWTR_ORX1_CV.sym} 900 0 0 0 {name=Xx7}
N 880.0 -20.0 900.0 -20.0 {lab=CMPO_B}
C {devices/lab_pin.sym} 880.0 -20.0 0 0 {name=l26 sig_type=std_logic lab=CMPO_B }
N 880.0 0.0 900.0 0.0 {lab=PWRUP_N_1V8}
C {devices/lab_pin.sym} 880.0 0.0 0 0 {name=l27 sig_type=std_logic lab=PWRUP_N_1V8 }
N 1010.0 -10.0 990.0 -10.0 {lab=net1}
C {devices/lab_pin.sym} 1010.0 -10.0 2 0 {name=l28 sig_type=std_logic lab=net1 }
N 940.0 -70.0 940.0 -50.0 {lab=VDD_1V8}
C {devices/lab_pin.sym} 940.0 -70.0 3 0 {name=l29 sig_type=std_logic lab=VDD_1V8 }
N 940.0 50.0 940.0 30.0 {lab=VSS}
C {devices/lab_pin.sym} 940.0 50.0 1 0 {name=l30 sig_type=std_logic lab=VSS }
C {JNW_TR_SKY130A/JNWTR_TAPCELLB_CV.sym} 900 190.0 0 0 {name=Xxtap_dig_0}
N 900.0 150.0 900.0 170.0 {lab=VDD_1V8}
C {devices/lab_pin.sym} 900.0 150.0 3 0 {name=l31 sig_type=std_logic lab=VDD_1V8 }
N 900.0 230.0 900.0 210.0 {lab=VSS}
C {devices/lab_pin.sym} 900.0 230.0 1 0 {name=l32 sig_type=std_logic lab=VSS }
