
TB=tran
VIEW=Sch
#VIEW=Lay
CELL=LELO_TEMP
LIB =LELO_TEMP_SKY130A
OPT=
THREADS=16
PROGRESS=--progress

.PHONY: all calib runs report plotall

all: report plotall

runs: typical etc mc

#- The same sets on the extracted netlist. Hours, not minutes.
lay:
	${MAKE} process VIEW=Lay TB=calibrate
	${MAKE} mc      VIEW=Lay TB=calibrate
	${MAKE} typical VIEW=Lay TB=calibrate
	${MAKE} typical VIEW=Lay TB=tran
	${MAKE} etc     VIEW=Lay TB=tran
	${MAKE} mc      VIEW=Lay TB=tran

report: calib runs summary

calib: ctyp cproc cmc

ctyp:
	${MAKE} typical TB=calibrate OPT=${OPT}
cproc:
	${MAKE} process TB=calibrate OPT=${OPT}
cmc:
	${MAKE} mc TB=calibrate OPT=${OPT}

#- plot_results.py redoes the post-processing tran.py did (and writes
#- the same derived values into the run yamls, so `make summary` agrees
#- with the figures), then draws one figure per run-set with Sch and
#- Lay as rows and the two calibrations as columns.
plotall:
	python3 plot_results.py

#- The RC extraction, on the worst etc corners. `make lper` in work/
#- first; fix_lper.py repairs what magic emits (duplicate device
#- names, pm^2 diode areas). The lvsr check on that netlist fails
#- STRUCTURALLY (the norc stripping leaves resistor fragments), so
#- the netlist is verified by use, against the Lay view: dt_RC/dt_C
#- = 0.92 flat over temperature and corner -- same total C, spread
#- along the wiring instead of lumped on the ramp node.
layr:
	python3 fix_lper.py ../../work/lpe/LELO_TEMP_lper.spi
	cicsim run --threads 3 ${PROGRESS} --replace replace_rc.yaml --name LayR_worst tran ${OPT} LayR Gt "Kss,Khh,Ktt" Tt Vt

include ../../tech/make/sim.make

test:
	${MAKE} typical OPT="Debug"

typical: netlist
	cicsim run --threads ${THREADS} ${PROGRESS} --replace replace.yaml --name ${VIEW}_typical ${TB} ${OPT} ${VIEW} Gt Ktt Tt Vt

slow_1:
	cicsim run --threads ${THREADS} ${PROGRESS} --replace replace.yaml --name ${VIEW}_slow ${TB} ${OPT} ${VIEW} Gt Kss "Tl" Vl

slow_2:
	cicsim run --threads ${THREADS} ${PROGRESS} --replace replace.yaml --name ${VIEW}_slow ${TB} ${OPT} ${VIEW} Gt Kss "Th" Vl

slow: netlist slow_1 slow_2

fast_1:
	cicsim run --threads ${THREADS} ${PROGRESS} --replace replace.yaml --name ${VIEW}_fast ${TB} ${OPT} ${VIEW} Gt Kff "Th" Vh

fast_2:
	cicsim run --threads ${THREADS} ${PROGRESS} --replace replace.yaml --name ${VIEW}_fast ${TB} ${OPT} ${VIEW} Gt Kff "Tl" Vh

fast: netlist fast_1 fast_2

tfs: netlist
	cicsim run --threads ${THREADS} ${PROGRESS} --replace replace.yaml --name ${VIEW}_tfs ${TB} ${OPT} ${VIEW} Gt "Ktt,Kss,Kff" "Tt" "Vt,Vl,Vh"

etc: netlist
	cicsim run --threads ${THREADS} ${PROGRESS} --replace replace.yaml --name ${VIEW}_etc ${TB} ${OPT} ${VIEW} Gt "Kss,Kff,Ksf,Kfs,Khh,Kll" "Tt" "Vt,Vl,Vh"

process: netlist
	cicsim run --threads ${THREADS} ${PROGRESS} --replace replace.yaml --name ${VIEW}_etc ${TB} ${OPT} ${VIEW} Gt "Kss,Kff,Ksf,Kfs,Khh,Kll" "Tt" "Vt"

mc: netlist
	cicsim run --threads ${THREADS} ${PROGRESS} --replace replace.yaml --name ${VIEW}_mc --count 10 ${TB} ${OPT} ${VIEW} Gt "Kttmm" "Tt" "Vt"

ntc: netlist
	cicsim run --threads ${THREADS} ${PROGRESS} --replace replace.yaml --name ${VIEW}_ntc ${TB} ${OPT} ${VIEW} Gt "Ktt,Kss,Kff" "Tt" Vt

temp: netlist
	cicsim run --threads ${THREADS} ${PROGRESS} --replace replace.yaml --name ${VIEW}_temp ${TB} ${OPT} ${VIEW} Gt "Ktt" "Tt,Th,Tl" Vt

#- Named _supply, not _temp: this used to share the `temp` target's run
#- name, so whichever ran second silently overwrote the other's .run and
#- results/, and a supply sweep would be reported as a temperature sweep.
supply: netlist
	cicsim run --threads ${THREADS} ${PROGRESS} --replace replace.yaml --name ${VIEW}_supply ${TB} ${OPT} ${VIEW} Gt "Ktt" "Tt" "Vt,Vl,Vh"

rc: netlist
	cicsim run --threads ${THREADS} ${PROGRESS} --replace replace.yaml --name ${VIEW}_temp ${TB} ${OPT} ${VIEW} Gt "Kll,Ktt,Khh" "Tt" "Vt"

summary:
	cicsim summary --output "README.md"
	pandoc -s  README.md -o README.html




clean:
	-rm -rf output_*
	-rm -rf __pycache__
	-rm *.run
	-rm *.pdf
	-rm *.csv
