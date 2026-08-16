v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -170 -220 -100 -220 {lab=VDPWR}
N -170 -200 -100 -200 {lab=ui_in[0]}
N -170 -180 -100 -180 {lab=VGND}
N 200 -220 270 -220 {lab=uo_out[0]}
N -240 -200 -170 -200 {lab=ui_in[0]}
N -240 -130 -240 -100 {lab=ui_in[0]}
N -240 -40 -240 -10 {lab=VGND}
N 120 -470 180 -470 {lab=VGND}
N 240 -470 310 -470 {lab=uio_oe[7:0]}
C {LELO_TEMP_SKY130A/LELO_TEMP.sym} 50 -200 0 0 {name=x1}
C {devices/lab_wire.sym} -170 -220 0 0 {name=p11 sig_type=std_logic lab=VDPWR}
C {devices/lab_wire.sym} -170 -180 0 0 {name=p9 sig_type=std_logic lab=VGND}
C {devices/lab_wire.sym} -200 -200 0 0 {name=p25 sig_type=std_logic lab=ui_in[0]}
C {devices/lab_wire.sym} 230 -220 0 0 {name=p12 sig_type=std_logic lab=uo_out[0]}
C {sky130_fd_pr/diode.sym} -240 -70 0 0 {name=D1
model=diode_pw2nd_05v5
area=2.025e11
perim=1.8e6
spiceprefix=X
}
C {devices/lab_wire.sym} -240 -110 0 0 {name=p13 sig_type=std_logic lab=ui_in[0]}
C {devices/lab_wire.sym} -240 -10 0 0 {name=p14 sig_type=std_logic lab=VGND}
C {sky130_fd_pr/res_generic_m4.sym} 210 -470 1 0 {name=R1[7:0]
W=0.3
L=0.3
model=res_generic_m4
mult=1}
C {devices/lab_wire.sym} 150 -470 0 0 {name=p7 sig_type=std_logic lab=VGND}
C {devices/opin.sym} 310 -470 0 0 {name=p32 lab=uio_oe[7:0]}
C {devices/ipin.sym} -490 -620 0 0 {name=p1 lab=VDPWR}
N -490 -620 -450 -620 {lab=VDPWR}
C {devices/lab_wire.sym} -450 -620 0 0 {name=p16 sig_type=std_logic lab=VDPWR}
C {devices/ipin.sym} -490 -580 0 0 {name=p2 lab=VGND}
N -490 -580 -450 -580 {lab=VGND}
C {devices/ipin.sym} -490 -540 0 0 {name=p3 lab=ui_in[7:0]}
N -490 -540 -450 -540 {lab=ui_in[7:0]}
C {devices/lab_wire.sym} -450 -545 0 0 {name=p17 sig_type=std_logic lab=ui_in[7:0]}
C {devices/ipin.sym} -490 -500 0 0 {name=p5 lab=uio_in[7:0]}
N -490 -500 -450 -500 {lab=uio_in[7:0]}
C {devices/ipin.sym} -490 -460 0 0 {name=p8 lab=ena}
N -490 -460 -450 -460 {lab=ena}
C {devices/ipin.sym} -490 -420 0 0 {name=p10 lab=rst_n}
N -490 -420 -450 -420 {lab=rst_n}
C {devices/ipin.sym} -490 -380 0 0 {name=p15 lab=clk}
N -490 -380 -450 -380 {lab=clk}
C {devices/opin.sym} -490 -340 0 0 {name=p4 lab=uo_out[7:0]}
N -490 -340 -450 -340 {lab=uo_out[7:0]}
C {devices/opin.sym} -490 -300 0 0 {name=p6 lab=uio_out[7:0]}
N -490 -300 -450 -300 {lab=uio_out[7:0]}

