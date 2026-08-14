v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {dummy} 1240 -960 0 0 0.5 0.5 {}
T {PTAT
Current Source} 1100 -650 0 0 1 1 {}
T {Startup
Two diode connected pmos in series from VDD into VD1.
With no current VD1 sits near VSS, the stack sees the
full supply and injects current into the diode branch.
Once the loop runs VD1 rises, VDD-VD1 falls below the
two gate-source drops, and the stack turns itself off.} 130 -670 0 0 0.2 0.2 {}
N 310 -100 550 -100 {
lab=VSS}
N 790 -480 790 -410 {
lab=VD1}
N 840 -780 860 -780 {
lab=LPO}
N 830 -810 860 -810 {
lab=LPI}
N 980 -470 980 -410 {
lab=VR1}
N 810 -410 870 -410 {
lab=VR1}
N 750 -410 790 -410 {
lab=VD1}
N 870 -410 980 -410 {
lab=VR1}
N 800 -780 840 -780 {
lab=LPO}
N 800 -810 830 -810 {
lab=LPI}
N 290 -970 310 -970 {
lab=VDD_1V8}
N 340 -970 980 -970 {
lab=VDD_1V8}
N 980 -970 980 -920 {
lab=VDD_1V8}
N 980 -890 1010 -890 {
lab=VDD_1V8}
N 1010 -950 1010 -890 {
lab=VDD_1V8}
N 980 -950 1010 -950 {
lab=VDD_1V8}
N 640 -970 640 -920 {
lab=VDD_1V8}
N 600 -890 640 -890 {
lab=VDD_1V8}
N 600 -970 600 -890 {
lab=VDD_1V8}
N 310 -970 340 -970 {
lab=VDD_1V8}
N 680 -890 680 -830 {
lab=LPI}
N 1180 -970 1180 -920 {
lab=VDD_1V8}
N 980 -970 1180 -970 {
lab=VDD_1V8}
N 1180 -890 1220 -890 {
lab=VDD_1V8}
N 1220 -940 1220 -890 {
lab=VDD_1V8}
N 1180 -940 1220 -940 {
lab=VDD_1V8}
N 1140 -890 1140 -850 {
lab=LPI}
N 890 -850 1140 -850 {
lab=LPI}
N 890 -890 890 -850 {
lab=LPI}
N 1180 -750 1250 -750 {
lab=IBP_1U[3:0]}
N 830 -560 830 -510 {
lab=VDD_1V8}
N 810 -480 810 -410 {
lab=VR1}
N 810 -560 810 -480 {
lab=VR1}
N 790 -560 790 -480 {
lab=VD1}
N 680 -830 680 -810 {lab=LPI}
N 680 -810 800 -810 {lab=LPI}
N 770 -560 770 -510 {lab=VSS}
N 640 -410 640 -210 {lab=VD1}
N 640 -410 750 -410 {lab=VD1}
N 550 -100 600 -100 {lab=VSS}
N 1090 -370 1120 -370 {lab=VSS}
N 1050 -400 1050 -370 {lab=VR1}
N 1050 -400 1090 -400 {lab=VR1}
N 980 -460 1090 -460 {lab=VR1}
N 980 -210 1090 -210 {lab=VD2}
N 770 -510 770 -270 {lab=VSS}
N 920 -970 920 -510 {lab=VDD_1V8}
N 830 -510 920 -510 {lab=VDD_1V8}
N 1090 -460 1090 -400 {lab=VR1}
N 1090 -340 1090 -210 {lab=VD2}
N 1270 -890 1300 -890 {lab=VDD_1V8}
N 1270 -920 1270 -890 {lab=VDD_1V8}
N 1270 -920 1340 -920 {lab=VDD_1V8}
N 1340 -890 1370 -890 {lab=VDD_1V8}
N 1370 -920 1370 -890 {lab=VDD_1V8}
N 1340 -920 1370 -920 {lab=VDD_1V8}
N 1270 -860 1340 -860 {lab=VDD_1V8}
N 1270 -890 1270 -860 {lab=VDD_1V8}
N 1340 -970 1340 -920 {lab=VDD_1V8}
N 1070 -970 1340 -970 {lab=VDD_1V8}
N 620 -520 640 -520 {lab=VD1}
N 320 -570 340 -570 {lab=PWRUP_1V8}
N 800 -780 800 -770 {lab=LPO}
N 860 -670 890 -670 {lab=PWRUP_N_1V8}
N 860 -650 890 -650 {lab=PWRUP_1V8}
N 860 -690 890 -690 {lab=VCP}
N 1180 -860 1180 -810 {lab=IBD[3:0]}
N 1180 -780 1220 -780 {lab=VDD_1V8}
N 1220 -890 1220 -780 {lab=VDD_1V8}
N 980 -780 1010 -780 {lab=VDD_1V8}
N 1010 -890 1010 -780 {lab=VDD_1V8}
N 980 -860 980 -810 {lab=VBD2}
N 980 -750 980 -470 {lab=VR1}
N 640 -860 640 -790 {lab=VBD1}
N 600 -760 640 -760 {lab=VDD_1V8}
N 600 -890 600 -760 {lab=VDD_1V8}
N 640 -730 640 -410 {lab=VD1}
N 940 -780 940 -750 {lab=VCP}
N 1140 -780 1140 -750 {lab=VCP}
N 680 -760 680 -730 {lab=VCP}
N 970 -890 980 -890 {lab=VDD_1V8}
N 710 -900 710 -760 {lab=VCP}
N 680 -760 710 -760 {lab=VCP}
N 680 -890 940 -890 {lab=LPI}
N 830 -900 830 -890 {lab=LPI}
N 490 -600 530 -600 {lab=VDD_1V8}
N 530 -970 530 -600 {lab=VDD_1V8}
N 490 -700 530 -700 {lab=VDD_1V8}
N 490 -970 490 -730 {lab=VDD_1V8}
N 450 -700 450 -640 {lab=VSU}
N 450 -640 490 -640 {lab=VSU}
N 490 -640 490 -630 {lab=VSU}
N 490 -670 490 -630 {lab=VSU}
N 450 -600 450 -570 {lab=VD1}
N 450 -570 490 -570 {lab=VD1}
N 490 -570 490 -550 {lab=VD1}
N 490 -550 640 -550 {lab=VD1}
N 950 -360 980 -360 {lab=VR1,R1[4:0]}
N 940 -320 960 -320 {lab=VSS}
N 950 -280 980 -280 {lab=R1[4:0],VD2}
N 1930 -3050 1930 -3030 {lab=VDD_1V8}
N 1870 -3000 1890 -3000 {lab=VDD_1V8}
N 1930 -2970 1930 -2950 {lab=VDD_1V8}
N 1930 -3000 1950 -3000 {lab=VDD_1V8}
N 1930 -2850 1930 -2830 {lab=VDD_1V8}
N 1870 -2800 1890 -2800 {lab=VDD_1V8}
N 1930 -2770 1930 -2750 {lab=VDD_1V8}
N 1930 -2800 1950 -2800 {lab=VDD_1V8}
N 1930 -2650 1930 -2630 {lab=VDD_1V8}
N 1870 -2600 1890 -2600 {lab=VDD_1V8}
N 1930 -2570 1930 -2550 {lab=VDD_1V8}
N 1930 -2600 1950 -2600 {lab=VDD_1V8}
N 1930 -2450 1930 -2430 {lab=VDD_1V8}
N 1870 -2400 1890 -2400 {lab=VDD_1V8}
N 1930 -2370 1930 -2350 {lab=VDD_1V8}
N 1930 -2400 1950 -2400 {lab=VDD_1V8}
N 1930 -2250 1930 -2230 {lab=VDD_1V8}
N 1870 -2200 1890 -2200 {lab=VDD_1V8}
N 1930 -2170 1930 -2150 {lab=VDD_1V8}
N 1930 -2200 1950 -2200 {lab=VDD_1V8}
N 1930 -2050 1930 -2030 {lab=VDD_1V8}
N 1870 -2000 1890 -2000 {lab=VDD_1V8}
N 1930 -1970 1930 -1950 {lab=VDD_1V8}
N 1930 -2000 1950 -2000 {lab=VDD_1V8}
N 1930 -1850 1930 -1830 {lab=VDD_1V8}
N 1870 -1800 1890 -1800 {lab=VDD_1V8}
N 1930 -1770 1930 -1750 {lab=VDD_1V8}
N 1930 -1800 1950 -1800 {lab=VDD_1V8}
N 1930 -1650 1930 -1630 {lab=VDD_1V8}
N 1870 -1600 1890 -1600 {lab=VDD_1V8}
N 1930 -1570 1930 -1550 {lab=VDD_1V8}
N 1930 -1600 1950 -1600 {lab=VDD_1V8}
N 1930 -1450 1930 -1430 {lab=VDD_1V8}
N 1870 -1400 1890 -1400 {lab=VDD_1V8}
N 1930 -1370 1930 -1350 {lab=VDD_1V8}
N 1930 -1400 1950 -1400 {lab=VDD_1V8}
N 1930 -1250 1930 -1230 {lab=VDD_1V8}
N 1870 -1200 1890 -1200 {lab=VDD_1V8}
N 1930 -1170 1930 -1150 {lab=VDD_1V8}
N 1930 -1200 1950 -1200 {lab=VDD_1V8}
N 1930 -1050 1930 -1030 {lab=VDD_1V8}
N 1870 -1000 1890 -1000 {lab=VDD_1V8}
N 1930 -970 1930 -950 {lab=VDD_1V8}
N 1930 -1000 1950 -1000 {lab=VDD_1V8}
N 1930 -850 1930 -830 {lab=VDD_1V8}
N 1870 -800 1890 -800 {lab=VDD_1V8}
N 1930 -770 1930 -750 {lab=VDD_1V8}
N 1930 -800 1950 -800 {lab=VDD_1V8}
N 1930 -650 1930 -630 {lab=VDD_1V8}
N 1870 -600 1890 -600 {lab=VDD_1V8}
N 1930 -570 1930 -550 {lab=VDD_1V8}
N 1930 -600 1950 -600 {lab=VDD_1V8}
N 1930 -450 1930 -430 {lab=VDD_1V8}
N 1870 -400 1890 -400 {lab=VDD_1V8}
N 1930 -370 1930 -350 {lab=VDD_1V8}
N 1930 -400 1950 -400 {lab=VDD_1V8}
N 1930 -250 1930 -230 {lab=VDD_1V8}
N 1870 -200 1890 -200 {lab=VDD_1V8}
N 1930 -170 1930 -150 {lab=VDD_1V8}
N 1930 -200 1950 -200 {lab=VDD_1V8}
N 1930 -50 1930 -30 {lab=VDD_1V8}
N 1870 0 1890 0 {lab=VDD_1V8}
N 1930 30 1930 50 {lab=VDD_1V8}
N 1930 0 1950 0 {lab=VDD_1V8}
N 1930 150 1930 170 {lab=VDD_1V8}
N 1870 200 1890 200 {lab=VDD_1V8}
N 1930 230 1930 250 {lab=VDD_1V8}
N 1930 200 1950 200 {lab=VDD_1V8}
N 1930 350 1930 370 {lab=VDD_1V8}
N 1870 400 1890 400 {lab=VDD_1V8}
N 1930 430 1930 450 {lab=VDD_1V8}
N 1930 400 1950 400 {lab=VDD_1V8}
N 1930 550 1930 570 {lab=VDD_1V8}
N 1870 600 1890 600 {lab=VDD_1V8}
N 1930 630 1930 650 {lab=VDD_1V8}
N 1930 600 1950 600 {lab=VDD_1V8}
C {devices/ipin.sym} 300 -970 0 0 {name=p4 lab=VDD_1V8}
C {devices/ipin.sym} 313.9889709803555 -100 0 0 {name=p5 lab=VSS}
C {devices/ipin.sym} 860 -810 2 0 {name=p7 lab=LPI}
C {devices/opin.sym} 860 -780 0 0 {name=p8 lab=LPO}
C {devices/opin.sym} 1250 -750 0 0 {name=p9 lab=IBP_1U[3:0]}
C {devices/lab_pin.sym} 640 -370 0 1 {name=l2 sig_type=std_logic lab=VD1}
C {devices/lab_pin.sym} 1090 -210 0 1 {name=l4 sig_type=std_logic lab=VD2}
C {devices/lab_pin.sym} 980 -410 0 1 {name=l5 sig_type=std_logic lab=VR1}
C {REY_ATR_SKY130A/REYATR_PCH_4C5F0.sym} 940 -890 0 0 {name=xca2}
C {REY_ATR_SKY130A/REYATR_PCH_4C5F0.sym} 680 -890 0 1 {name=xca1[7:0]}
C {REY_ATR_SKY130A/REYATR_CAPX1.sym} 830 -960 2 1 {name=xd1[9:0]}
C {LELO_TEMP_SKY130A/LELOTEMP_OTAR.sym} 800 -710 1 1 {name=xad6}
C {REY_ATR_SKY130A/REYATR_PCH_4C5F0.sym} 1140 -890 0 0 {name=xca3[3:0]}
C {cborder/border_xs.sym} 250 -40 0 0 {user="Carsten Wulff" company="Carsten Wulff Software"}
C {JNW_BIAS_SKY130A/JNWBIAS_BIPOLAR.sym} 800 -110 0 0 {name=xe1}
C {REY_ATR_SKY130A/REYATR_NCH_4C5F0.sym} 1050 -370 0 0 {name=xg1 }
C {devices/lab_pin.sym} 1120 -370 0 1 {name=l1 sig_type=std_logic lab=VSS}
C {REY_ATR_SKY130A/REYATR_PCH_4C5F0.sym} 1300 -890 0 0 {name=xcc[4:0]}
C {devices/opin.sym} 620 -520 0 1 {name=p2 lab=VD1}
C {devices/ipin.sym} 320 -570 0 0 {name=p3 lab=PWRUP_1V8}
C {devices/lab_pin.sym} 890 -670 0 1 {name=l10 sig_type=std_logic lab=PWRUP_N_1V8}
C {devices/lab_pin.sym} 890 -650 0 1 {name=l11 sig_type=std_logic lab=PWRUP_1V8}
C {devices/ipin.sym} 340 -770 0 0 {name=p1 lab=PWRUP_N_1V8}
C {devices/lab_pin.sym} 770 -270 0 0 {name=l7 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 890 -690 0 1 {name=l14 sig_type=std_logic lab=VCP}
C {REY_ATR_SKY130A/REYATR_PCH_4C1F2.sym} 1140 -780 0 0 {name=xca2[3:0]}
C {devices/lab_pin.sym} 1180 -830 0 0 {name=l15 sig_type=std_logic lab=IBD[3:0]}
C {REY_ATR_SKY130A/REYATR_PCH_4C1F2.sym} 940 -780 0 0 {name=xca4}
C {REY_ATR_SKY130A/REYATR_PCH_4C1F2.sym} 680 -760 0 1 {name=xca5[7:0]}
C {devices/lab_pin.sym} 940 -750 1 1 {name=l16 sig_type=std_logic lab=VCP}
C {devices/lab_pin.sym} 1140 -750 1 1 {name=l17 sig_type=std_logic lab=VCP}
C {devices/lab_pin.sym} 640 -840 0 0 {name=l19 sig_type=std_logic lab=VBD1}
C {devices/lab_pin.sym} 980 -840 0 0 {name=l20 sig_type=std_logic lab=VBD2}
C {devices/lab_pin.sym} 680 -730 1 1 {name=l21 sig_type=std_logic lab=VCP}
C {REY_ATR_SKY130A/REYATR_CAPX1.sym} 710 -960 2 1 {name=xd2[2:0]}
C {REY_ATR_SKY130A/REYATR_PCH_2C5F0.sym} 450 -700 0 0 {name=xsu1}
C {devices/lab_pin.sym} 450 -700 0 0 {name=l33 sig_type=std_logic lab=VSU}
C {REY_ATR_SKY130A/REYATR_PCH_2C5F0.sym} 450 -600 0 0 {name=xsu2}
C {REY_ATR_SKY130A/REYATR_RES_36C2F0.sym} 980 -280 1 1 {name=xd3[5:0]}
C {devices/lab_wire.sym} 950 -360 0 0 {name=p6 sig_type=std_logic lab=VR1,R1[4:0]}
C {devices/lab_wire.sym} 940 -320 0 0 {name=p10 sig_type=std_logic lab=VSS}
C {devices/lab_wire.sym} 950 -280 0 0 {name=p11 sig_type=std_logic lab=R1[4:0],VD2}
C {REY_ATR_SKY130A/REYATR_PCH_2C5F0.sym} 1890 -3000 0 0 {name=xfill_p_su[10:0]}
C {devices/lab_pin.sym} 1930 -3050 2 0 {name=lfsu01 sig_type=std_logic lab=VDD_1V8 }
C {devices/lab_pin.sym} 1930 -2950 2 0 {name=lfsu02 sig_type=std_logic lab=VDD_1V8 }
C {devices/lab_pin.sym} 1870 -3000 2 1 {name=lfsu03 sig_type=std_logic lab=VDD_1V8 }
C {devices/lab_pin.sym} 1950 -3000 2 0 {name=lfsu04 sig_type=std_logic lab=VDD_1V8 }
C {REY_ATR_SKY130A/REYATR_PCH_4C5F0.sym} 1890 -800 0 0 {name=xfill_p_cc[7:0]}
C {devices/lab_pin.sym} 1930 -850 2 0 {name=lfcc01 sig_type=std_logic lab=VDD_1V8 }
C {devices/lab_pin.sym} 1930 -750 2 0 {name=lfcc02 sig_type=std_logic lab=VDD_1V8 }
C {devices/lab_pin.sym} 1870 -800 2 1 {name=lfcc03 sig_type=std_logic lab=VDD_1V8 }
C {devices/lab_pin.sym} 1950 -800 2 0 {name=lfcc04 sig_type=std_logic lab=VDD_1V8 }
