

all: typical etc mc summary



TB=tran
VIEW=Sch
#VIEW=Lay
CELL=LELO_TEMP
LIB =LELO_TEMP_SKY130A
OPT=

all:
#- Run calibration corners
	${MAKE} process TB=calibrate
	${MAKE} mc TB=calibrate
#- Run corners
	${MAKE} typical
	${MAKE} etc
	${MAKE} mc
	${MAKE} summary
	${MAKE} plotall

plotall:
	python3 tran.py tran_Sch_typical.run
	python3 tran.py tran_Sch_etc.run
	python3 tran.py tran_Sch_mc.run

include ../../tech/make/sim.make

test:
	${MAKE} typical OPT="Debug"

typical: netlist
	cicsim run --replace replace.yaml --name ${VIEW}_typical ${TB} ${OPT} ${VIEW} Gt Ktt Tt Vt

slow_1:
	cicsim run --replace replace.yaml --name ${VIEW}_slow ${TB} ${OPT} ${VIEW} Gt Kss "Tl" Vl

slow_2:
	cicsim run --replace replace.yaml --name ${VIEW}_slow ${TB} ${OPT} ${VIEW} Gt Kss "Th" Vl

slow: netlist slow_1 slow_2

fast_1:
	cicsim run --replace replace.yaml --name ${VIEW}_fast ${TB} ${OPT} ${VIEW} Gt Kff "Th" Vh

fast_2:
	cicsim run --replace replace.yaml --name ${VIEW}_fast ${TB} ${OPT} ${VIEW} Gt Kff "Tl" Vh

fast: netlist fast_1 fast_2


tfs: netlist
	cicsim run --replace replace.yaml --name ${VIEW}_tfs ${TB} ${OPT} ${VIEW} Gt "Ktt,Kss,Kff" "Tt" "Vt,Vl,Vh"

etc: netlist
	cicsim run --replace replace.yaml --name ${VIEW}_etc ${TB} ${OPT} ${VIEW} Gt "Kss,Kff,Ksf,Kfs,Khh,Kll" "Tt" "Vt,Vl,Vh"

process: netlist
	cicsim run --replace replace.yaml --name ${VIEW}_etc ${TB} ${OPT} ${VIEW} Gt "Kss,Kff,Ksf,Kfs,Khh,Kll" "Tt" "Vt"

mc: netlist
	cicsim run --replace replace.yaml --name ${VIEW}_mc --count 30 ${TB} ${OPT} ${VIEW} Gt "Kttmm" "Tt" "Vt"

ntc: netlist
	cicsim run --replace replace.yaml --name ${VIEW}_ntc ${TB} ${OPT} ${VIEW} Gt "Ktt,Kss,Kff" "Tt" Vt

temp: netlist
	cicsim run --replace replace.yaml --name ${VIEW}_temp ${TB} ${OPT} ${VIEW} Gt "Ktt" "Tt,Th,Tl" Vt

supply: netlist
	cicsim run --replace replace.yaml --name ${VIEW}_temp ${TB} ${OPT} ${VIEW} Gt "Ktt" "Tt" "Vl,Vt,Vh"

rc: netlist
	cicsim run --replace replace.yaml --name ${VIEW}_temp ${TB} ${OPT} ${VIEW} Gt "Kll,Ktt,Khh" "Tt" "Vt"

summary:
	cicsim summary --output "README.md"
	pandoc -s  README.md -o README.html




clean:
	-rm -rf output_*
	-rm -rf __pycache__
	-rm *.run
	-rm *.pdf
	-rm *.csv
