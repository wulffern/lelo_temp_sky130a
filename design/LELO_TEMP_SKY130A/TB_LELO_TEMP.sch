v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
B 2 60 -680 860 -280 {flags=graph
y1=-0.6509986
y2=1.8200014
ypos1=0
ypos2=2
divy=5
subdivy=4
unity=1
x1=2.7686828e-06
x2=3.262102e-06
divx=5
subdivx=4
xlabmag=1.0
ylabmag=1.0
node="osc_temp_1v8
xdut.ibp_1u<0>
xdut.ibp_1u<1>"
color="4 5 6"
dataset=-1
unitx=1
logx=0
logy=0
rawfile=$netlist_dir/TB_LELO_TEMP_tran.raw
legend=1}
B 2 61.08447877947143 -1125 861.0844787794714 -725 {flags=graph
y1=1.3102875e-06
y2=1.3484724e-06
ypos1=0
ypos2=2
divy=5
subdivy=4
unity=1
x1=2.7686828e-06
x2=3.262102e-06
divx=5
subdivx=4
xlabmag=1.0
ylabmag=1.0
node="i(@m.xdut.x1_ibp.xca3<3>.xm1.msky130_fd_pr__pfet_01v8[id])
i(@m.xdut.x1_ibp.xca3<2>.xm1.msky130_fd_pr__pfet_01v8[id])
i(@m.xdut.x1_ibp.xca3<0>.xm1.msky130_fd_pr__pfet_01v8[id])

i(@m.xdut.x1_ibp.xca3<1>.xm1.msky130_fd_pr__pfet_01v8[id])"
color="4 6 7 15"
dataset=-1
unitx=1
logx=0
logy=0
rawfile=$netlist_dir/TB_LELO_TEMP_tran.raw
legend=1}
B 2 -828.9155212205286 -1130 -28.9155212205286 -730 {flags=graph
y1=4.6e-16
y2=1.9
ypos1=0
ypos2=2
divy=5
subdivy=4
unity=1
x1=2.7686828e-06
x2=3.262102e-06
divx=5
subdivx=4
xlabmag=1.0
ylabmag=1.0
dataset=-1
unitx=1
logx=0
logy=0
rawfile=$netlist_dir/TB_LELO_TEMP_tran.raw
legend=1
color="15 4 12"
node="xdut.lpi
xdut.vc
pwrup_1v8"}
B 2 60 -250 860 150 {flags=graph
y1=-0.15679861
y2=2.3142014
ypos1=0
ypos2=2
divy=5
subdivy=4
unity=1
x1=2.7686828e-06
x2=3.262102e-06
divx=5
subdivx=4
xlabmag=1.0
ylabmag=1.0
dataset=-1
unitx=1
logx=0
logy=0
rawfile=$netlist_dir/TB_LELO_TEMP_tran.raw
legend=1
color="4 10"
node="xdut.rst_a
xdut.rst_b"
autoload=1}
B 2 -828.9155212205286 -720 -28.9155212205286 -320 {flags=graph
y1=0.62
y2=0.74
ypos1=0
ypos2=2
divy=5
subdivy=4
unity=1
x1=2.7686828e-06
x2=3.262102e-06
divx=5
subdivx=4
xlabmag=1.0
ylabmag=1.0
dataset=-1
unitx=1
logx=0
logy=0
rawfile=$netlist_dir/TB_LELO_TEMP_tran.raw
legend=1
color="7 13 12"
node="xdut.vc
xdut.x1_ibp.vr1
xdut.x1_ibp.vd2"
hcursor1_y=0.62778329
hcursor2_y=0.73700424}
B 2 56.05499033927435 -680 856.0549903392744 -280 {flags=graph
y1=-0.15679861
y2=2.3142014
ypos1=0
ypos2=2
divy=5
subdivy=4
unity=1
x1=2.7686828e-06
x2=3.262102e-06
divx=5
subdivx=4
xlabmag=1.0
ylabmag=1.0
node="osc_temp_1v8
xdut.ibp_1u<0>
xdut.ibp_1u<1>"
color="4 5 6"
dataset=-1
unitx=1
logx=0
logy=0
rawfile=$netlist_dir/TB_LELO_TEMP_tran.raw
legend=1}
T {Test bench to load current results} -650 -230 0 0 0.4 0.4 {}
N -80 -60 -30 -60 {lab=OSC_TEMP_1V8}
N -640 -110 -640 -80 {lab=VDD_1V8}
N -850 -20 -640 -20 {lab=0}
N -850 -110 -850 -80 {lab=PWRUP_1V8}
N -640 -20 -380 -20 {lab=0}
N -430 -40 -380 -40 {lab=PWRUP_1V8}
N -430 -60 -380 -60 {lab=VDD_1V8}
C {LELO_TEMP_SKY130A/LELO_TEMP.sym} -230 -40 0 0 {name=xdut}
C {devices/lab_wire.sym} -430 -60 0 0 {name=p1 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_wire.sym} -460 -20 0 0 {name=p3 sig_type=std_logic lab=0}
C {devices/lab_wire.sym} -30 -60 0 1 {name=p4 sig_type=std_logic lab=OSC_TEMP_1V8}
C {devices/vsource.sym} -640 -50 0 0 {name=V1 value="pwl 0 0 0.5u 0 1.5u \{VDDA\}" savecurrent=false}
C {devices/code_shown.sym} -1200 -380 0 0 {name=s1 only_toplevel=false value="
.param mc_mm_switch=0
.param mc_pr_switch=0

.lib "../../../tech/ngspice/temperature.spi" Tt
.lib "../../../tech/ngspice/corners.spi" Ktt
.lib "../../../tech/ngspice/supply.spi" Vt
.include ../../../../cpdk/ngspice/ideal_circuits.spi

.option savecurrents
.save all
.control
optran 0 0 0 10n 1u 0


tran 1n 4u
write TB_LELO_TEMP_tran.raw

exit
.endc

"}
C {devices/launcher.sym} -180 80 0 0 {name=h5
descr="load waves" 
tclcommand="xschem raw_read $netlist_dir/TB_LELO_TEMP_tran.raw tran"
}
C {devices/vsource.sym} -850 -50 0 0 {name=V2 value="pwl 0 0 2u 0 2.01u \{VDDA\}" savecurrent=false}
C {devices/lab_wire.sym} -430 -40 0 0 {name=p2 sig_type=std_logic lab=PWRUP_1V8}
C {devices/lab_wire.sym} -640 -110 0 0 {name=p5 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_wire.sym} -850 -110 0 0 {name=p6 sig_type=std_logic lab=PWRUP_1V8}
