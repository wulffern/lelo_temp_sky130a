v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
B 2 90 -440 890 -40 {flags=graph
y1=-1.26e-05
ypos1=0
ypos2=2
divy=5
subdivy=4
unity=1
x1=21.21825
x2=181.21825
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
rawfile=$netlist_dir/res_tempco.raw
autoload=1
y2=-9.6e-06}
N 10 0 10 20 {lab=#net1}
N -70 60 -10 60 {lab=0}
N -70 60 -70 120 {lab=0}
N -70 120 10 120 {lab=0}
N 10 100 10 120 {lab=0}
N -70 -40 -10 -40 {lab=0}
N -70 -40 -70 60 {lab=0}
N 10 -130 10 -80 {lab=#net2}
N -110 -130 10 -130 {lab=#net2}
N -160 -130 -160 -20 {lab=#net2}
N -160 -130 -110 -130 {lab=#net2}
N -160 40 -160 120 {lab=0}
N -160 120 -70 120 {lab=0}
C {JNW_TR_SKY130A/JNWTR_RPPO4.sym} 10 20 1 0 {name=xac2}
C {JNW_TR_SKY130A/JNWTR_RPPO8.sym} 10 -80 1 0 {name=xac3}
C {devices/vsource.sym} -160 10 0 0 {name=V1 value=1 savecurrent=false}
C {devices/lab_wire.sym} -110 120 0 0 {name=p1 sig_type=std_logic lab=0}
C {devices/code_shown.sym} -690 -310 0 0 {name=s1 only_toplevel=false value="
.param mc_mm_switch=0
.param mc_pr_switch=0

.lib "../../../tech/ngspice/corners.spi" Ktt
.lib "../../../tech/ngspice/temperature.spi" Tl
.lib "../../../tech/ngspice/supply.spi" Vl
.include ../../../../cpdk/ngspice/ideal_circuits.spi


.save all
.control
optran 0 0 0 10n 10u 0
op

dc TEMP -40 125 5
print i(V1)
write res_tempco.raw
exit
.endc
.end

"}
