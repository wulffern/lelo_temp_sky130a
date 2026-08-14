
#- LELOTEMP_CCMP: the comparator plus its integrating cap, on its own.
#-
#- One testbench:
#-   tran  release reset, integrate ibias onto the cap, trip -> half period
#-
#- This is the oscillator's timing element with the bias block replaced
#- by ideal sources, so the period measured here moves only with the
#- comparator and the caps.

TB=tran
VIEW=Sch
#VIEW=Lay
CELL=LELOTEMP_CCMP
LIB =LELO_TEMP_SKY130A
OPT=
THREADS=8
PROGRESS=--progress

.PHONY: all runs report

all: report

report: runs summary

runs: typical etc mc

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
