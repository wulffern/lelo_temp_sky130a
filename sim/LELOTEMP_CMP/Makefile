
#- LELOTEMP_CMP: the comparator, simulated on its own.
#-
#- Two testbenches:
#-   dc    transfer curve -> trip point, input referred offset, gain
#-   tran  ramp response  -> propagation delay at the real input slope
#-
#- The delay matters because it adds to every half period of the
#- relaxation oscillator in LELO_TEMP, so a delay that drifts with
#- temperature shows up directly as a temperature error.

TB=dc
VIEW=Sch
#VIEW=Lay
CELL=LELOTEMP_CMP
LIB =LELO_TEMP_SKY130A
OPT=
THREADS=8
PROGRESS=--progress

.PHONY: all runs report dc tran

all: report

report: runs summary

#- Both testbenches over the same corner sets.
runs: dc tran

dc:
	${MAKE} typical TB=dc
	${MAKE} etc     TB=dc
	${MAKE} mc      TB=dc

tran:
	${MAKE} typical TB=tran
	${MAKE} etc     TB=tran
	${MAKE} mc      TB=tran

include ../../tech/make/sim.make

test:
	${MAKE} typical OPT="Debug"

typical: netlist
	cicsim run --threads ${THREADS} ${PROGRESS} --replace replace.yaml --name ${VIEW}_typical ${TB} ${OPT} ${VIEW} Gt Ktt Tt Vt

#- Process and supply spread at nominal temperature.
etc: netlist
	cicsim run --threads ${THREADS} ${PROGRESS} --replace replace.yaml --name ${VIEW}_etc ${TB} ${OPT} ${VIEW} Gt "Kss,Kff,Ksf,Kfs" "Tt" "Vt,Vl,Vh"

#- Temperature spread at nominal process.
temp: netlist
	cicsim run --threads ${THREADS} ${PROGRESS} --replace replace.yaml --name ${VIEW}_temp ${TB} ${OPT} ${VIEW} Gt "Ktt" "Tt,Th,Tl" Vt

#- Mismatch. This is the run that gives the random offset, which is the
#- number the one point calibration has to absorb.
mc: netlist
	cicsim run --threads ${THREADS} ${PROGRESS} --replace replace.yaml --name ${VIEW}_mc --count 30 ${TB} ${OPT} ${VIEW} Gt "Kttmm" "Tt" "Vt"

summary:
	cicsim summary --output "README.md"

clean:
	-rm -rf output_*
	-rm -rf __pycache__
	-rm -f *.run
	-rm -f *.csv
