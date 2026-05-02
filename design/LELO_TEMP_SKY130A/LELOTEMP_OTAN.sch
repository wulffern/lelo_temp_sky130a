v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {Current Mirror OTA} 440 -660 0 0 1 1 {}
N 100 -100 210 -100 {lab=VSS}
N 90 -500 150 -500 {lab=VDD_1V8}
N 590 -330 800 -330 {lab=VBP1}
N 590 -310 800 -310 {lab=VBP2}
N 260 -340 290 -340 {lab=VDD_1V8}
N 260 -320 290 -320 {lab=PWRUP_1V8}
N 260 -300 290 -300 {lab=PWRUP_N_1V8}
N 230 -280 290 -280 {lab=VIN}
N 230 -260 290 -260 {lab=VIP}
N 260 -200 290 -200 {lab=VSS}
N 590 -270 630 -270 {lab=VO}
N 260 -240 290 -240 {lab=VCP}
N 260 -220 290 -220 {lab=VCN}
N 440 -530 470 -530 {lab=VDD_1V8}
N 440 -490 470 -490 {lab=PWRUP_N_1V8}
N 440 -470 470 -470 {lab=VSS}
N 770 -350 800 -350 {lab=PWRUP_1V8}
N 770 -370 800 -370 {lab=VDD_1V8}
N 770 -290 800 -290 {lab=PWRUP_N_1V8}
N 770 -270 800 -270 {lab=VSS}
N 1100 -340 1130 -340 {lab=VCP}
N 1100 -300 1130 -300 {lab=VCN}
N 770 -510 800 -510 {lab=VCP}
N 770 -530 800 -530 {lab=VO}
C {devices/ipin.sym} 90 -500 2 1 {name=p4 lab=VDD_1V8}
C {devices/ipin.sym} 100 -100 2 1 {name=p5 lab=VSS}
C {devices/ipin.sym} 150 -310 2 1 {name=p9 lab=PWRUP_N_1V8}
C {devices/ipin.sym} 150 -330 2 1 {name=p10 lab=PWRUP_1V8}
C {cborder/border_xs.sym} 60 10 0 0 {user="Carsten Wulff" company="Carsten Wulff Software"}
C {devices/opin.sym} 630 -270 0 0 {name=p25 lab=VO}
C {devices/ipin.sym} 230 -260 2 1 {name=p33 lab=VIP}
C {devices/ipin.sym} 230 -280 2 1 {name=p34 lab=VIN}
C {LELO_TEMP_SKY130A/LELOTEMP_OTACMN.sym} 440 -270 0 0 {name=x1}
C {LELO_TEMP_SKY130A/LELOTEMP_CASCBIAS.sym} 950 -320 0 0 {name=x2}
C {devices/lab_wire.sym} 260 -340 0 0 {name=p3 sig_type=std_logic lab=VDD_1V8
}
C {devices/lab_wire.sym} 260 -320 0 0 {name=p1 sig_type=std_logic lab=PWRUP_1V8
}
C {devices/lab_wire.sym} 260 -300 0 0 {name=p2 sig_type=std_logic lab=PWRUP_N_1V8
}
C {devices/lab_wire.sym} 260 -240 0 0 {name=p6 sig_type=std_logic lab=VCP
}
C {devices/lab_wire.sym} 260 -220 0 0 {name=p7 sig_type=std_logic lab=VCN
}
C {LELO_TEMP_SKY130A/LELOTEMP_START.sym} 620 -500 0 0 {name=x3}
C {devices/lab_wire.sym} 440 -530 0 0 {name=p8 sig_type=std_logic lab=VDD_1V8
}
C {devices/lab_wire.sym} 440 -490 0 0 {name=p12 sig_type=std_logic lab=PWRUP_N_1V8
}
C {devices/lab_wire.sym} 260 -200 0 0 {name=p13 sig_type=std_logic lab=VSS
}
C {devices/lab_wire.sym} 440 -470 0 0 {name=p14 sig_type=std_logic lab=VSS
}
C {devices/lab_wire.sym} 690 -330 0 0 {name=p15 sig_type=std_logic lab=VBP1
}
C {devices/lab_wire.sym} 690 -310 0 0 {name=p16 sig_type=std_logic lab=VBP2
}
C {devices/lab_wire.sym} 770 -350 0 0 {name=p17 sig_type=std_logic lab=PWRUP_1V8
}
C {devices/lab_wire.sym} 770 -370 0 0 {name=p18 sig_type=std_logic lab=VDD_1V8
}
C {devices/lab_wire.sym} 770 -290 0 0 {name=p19 sig_type=std_logic lab=PWRUP_N_1V8
}
C {devices/lab_wire.sym} 770 -270 0 0 {name=p20 sig_type=std_logic lab=VSS
}
C {devices/lab_wire.sym} 1130 -340 0 1 {name=p21 sig_type=std_logic lab=VCP
}
C {devices/lab_wire.sym} 1130 -300 0 1 {name=p22 sig_type=std_logic lab=VCN
}
C {devices/lab_wire.sym} 800 -510 0 1 {name=p23 sig_type=std_logic lab=VCP
}
C {devices/lab_wire.sym} 800 -530 0 1 {name=p24 sig_type=std_logic lab=VO
}
C {devices/opin.sym} 850 -510 0 0 {name=p53 lab=VCP}
