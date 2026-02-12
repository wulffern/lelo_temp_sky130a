v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
B 2 170 -590 970 -190 {flags=graph
y1=-1.3143006e-06
y2=-4.02814e-08
ypos1=0
ypos2=2
divy=5
subdivy=4
unity=1
x1=-40
x2=125
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
node=i(v1)
color=4
dataset=-1
unitx=1
logx=0
logy=0
rawfile=$netlist_dir/TB_RES_TEMP.raw
autoload=1
sim_type=dc}
N 100 -120 100 -100 {lab=#net1}
N 50 -160 80 -160 {lab=0}
N 50 -160 50 -60 {lab=0}
N 50 -60 80 -60 {lab=0}
N -60 -200 -60 -130 {lab=#net2}
N -60 -200 100 -200 {lab=#net2}
N -60 -70 -60 -20 {lab=0}
N -60 -20 100 -20 {lab=0}
N 50 -60 50 -20 {lab=0}
C {JNW_TR_SKY130A/JNWTR_RPPO4.sym} 100 -100 1 0 {name=xac2}
C {JNW_TR_SKY130A/JNWTR_RPPO8.sym} 100 -200 1 0 {name=xac3}
C {devices/vsource.sym} -60 -100 0 0 {name=V1 value=1 savecurrent=false}
C {devices/lab_wire.sym} -60 -20 0 0 {name=p1 sig_type=std_logic lab=0}
C {devices/code_shown.sym} -410 -430 0 0 {name=s1 only_toplevel=false value="
.param mc_mm_switch=0
.param mc_pr_switch=0

.lib "../../../tech/ngspice/temperature.spi" Tt
.lib "../../../tech/ngspice/corners.spi" Ktt
.lib "../../../tech/ngspice/supply.spi" Vt
.include ../../../../cpdk/ngspice/ideal_circuits.spi

Bt1 vtemp 0 V=TEMPER

.option savecurrents
.save all
.control
optran 0 0 0 10n 1u 0



dc TEMP -40 125 5
write TB_RES_TEMP.raw

exit
.endc

"}
C {devices/launcher.sym} -20 -550 0 0 {name=h5
descr="load waves" 
tclcommand="xschem raw_read $netlist_dir/TB_RES_TEMP.raw dc"
}
