

all: typical etc mc summary



TB=lstb
VIEW=Sch
#VIEW=Lay
CELL=LELOTEMP_BIAS_IBP
LIB =LELO_TEMP_SKY130A
OPT=
THREADS=16
PROGRESS=--progress

include ../../tech/make/sim.make

all:
	make typical etc mc TB=lstb
	make typical etc mc TB=tran
	make typical etc mc TB=dc
	make summary


test:
	${MAKE} typical OPT="Debug"

typical: netlist
	cicsim run --threads ${THREADS} ${PROGRESS} --replace replace.yaml --name ${VIEW}_typical ${TB} ${OPT} ${VIEW} Gt Ktt Tt Vt

slow: netlist
	cicsim run --threads ${THREADS} ${PROGRESS} --replace replace.yaml --name ${VIEW}_slow ${TB} ${OPT} ${VIEW} Gt Kss "Th,Tl" Vl

fast: netlist
	cicsim run --threads ${THREADS} ${PROGRESS} --replace replace.yaml --name ${VIEW}_fast ${TB} ${OPT} ${VIEW} Gt Kff "Th,Tl" Vh

tfs: netlist
	cicsim run --threads ${THREADS} ${PROGRESS} --replace replace.yaml --name ${VIEW}_tfs ${TB} ${OPT} ${VIEW} Gt "Ktt,Kss,Kff" "Tt,Th,Tl" "Vt,Vl,Vh"

etc: netlist
	cicsim run --threads ${THREADS} ${PROGRESS} --replace replace.yaml --name ${VIEW}_etc ${TB} ${OPT} ${VIEW} Gt "Kss,Kff,Ksf,Kfs" "Th,Tl" "Vl,Vh"

mc: netlist
	cicsim run --threads ${THREADS} ${PROGRESS} --replace replace.yaml --name ${VIEW}_mc --count 30 ${TB} ${OPT} ${VIEW} Gt "Kttmm" "Tt" "Vt"

ntc: netlist
	cicsim run --threads ${THREADS} ${PROGRESS} --replace replace.yaml --name ${VIEW}_ntc ${TB} ${OPT} ${VIEW} Gt "Ktt,Kss,Kff" "Tt" Vt

temp: netlist
	cicsim run --threads ${THREADS} ${PROGRESS} --replace replace.yaml --name ${VIEW}_temp ${TB} ${OPT} ${VIEW} Gt "Ktt" "Tt,Th,Tl" Vt

summary:
	cicsim summary --output "README.md"
	pandoc -o README.html README.md  -s

slide:
	pandoc -s  -t slidy README.md -o README.html


clean:
	-rm -rf output_*
	-rm -rf __pycache__
	-rm *.run
	-rm *.pdf
	-rm *.csv
