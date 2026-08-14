v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 400 0 400 20 {lab=VSS}
N 50 20 400 20 {lab=VSS}
N 50 0 50 20 {lab=VSS}
N -10 -30 10 -30 {lab=VSS}
N -10 -30 -10 20 {lab=VSS}
N -10 20 60 20 {lab=VSS}
N 50 -130 50 -60 {lab=VD1}
N 400 -140 400 -60 {lab=VD2}
N -60 20 -10 20 {lab=VSS}
N 320 -30 360 -30 {lab=VSS}
N 320 -30 320 20 {lab=VSS}
C {sky130_fd_pr/pnp_05v5.sym} 30 -30 0 0 {name=Q1
model=pnp_05v5_W3p40L3p40
spiceprefix=X
}
C {sky130_fd_pr/pnp_05v5.sym} 380 -30 0 0 {name=Q2[7:0]
model=pnp_05v5_W3p40L3p40
spiceprefix=X
}
C {devices/ipin.sym} -60 20 0 0 {name=p1 lab=VSS}
C {devices/ipin.sym} 50 -130 1 0 {name=p2 lab=VD1}
C {devices/ipin.sym} 400 -140 1 0 {name=p3 lab=VD2}
C {cborder/border_xs.sym} -200 70 0 0 {user="Carsten Wulff" company="Carsten Wulff Software"}
