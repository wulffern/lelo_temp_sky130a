

UNAME_S := $(shell uname -s)
VLNGGEN_ENV :=
ifeq ($(UNAME_S),Darwin)
VLNGGEN_ENV := CPPFLAGS='-DVL_TIME_CONTEXT'
endif

all: typical etc mc summary

mynetlist: netlist
	$(VLNGGEN_ENV) ngspice vlnggen ../../rtl/tempFsm.v
	perl ../../tech/script/gensvinst ../../rtl/tempFsm.v tempFsm
	mv svinst.spi svinst_tfsm.spi
	$(VLNGGEN_ENV) ngspice vlnggen ../../rtl/tempCounter.v
	perl ../../tech/script/gensvinst ../../rtl/tempCounter.v tempCounter
	mv svinst.spi svinst_tc.spi


TB=tran
VIEW=Sch
#VIEW=Lay
CELL=LELO_TEMP
LIB =LELO_TEMP_SKY130A
COPT=

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
	${MAKE} typical COPT="Debug"

typical: mynetlist
	cicsim run --replace replace.yaml --name ${VIEW}_typical ${TB} ${COPT} ${VIEW} Gt Ktt Tt Vt

slow_1:
	cicsim run --replace replace.yaml --name ${VIEW}_slow ${TB} ${COPT} ${VIEW} Gt Kss "Tl" Vl

slow_2:
	cicsim run --replace replace.yaml --name ${VIEW}_slow ${TB} ${COPT} ${VIEW} Gt Kss "Th" Vl

slow: mynetlist slow_1 slow_2

fast_1:
	cicsim run --replace replace.yaml --name ${VIEW}_fast ${TB} ${COPT} ${VIEW} Gt Kff "Th" Vh

fast_2:
	cicsim run --replace replace.yaml --name ${VIEW}_fast ${TB} ${COPT} ${VIEW} Gt Kff "Tl" Vh

fast: mynetlist fast_1 fast_2


tfs: mynetlist
	cicsim run --replace replace.yaml --name ${VIEW}_tfs ${TB} ${COPT} ${VIEW} Gt "Ktt,Kss,Kff" "Tt" "Vt,Vl,Vh"

etc: mynetlist
	cicsim run --replace replace.yaml --name ${VIEW}_etc ${TB} ${COPT} ${VIEW} Gt "Kss,Kff,Ksf,Kfs,Khh,Kll" "Tt" "Vt,Vl,Vh"

process: mynetlist
	cicsim run --replace replace.yaml --name ${VIEW}_etc ${TB} ${COPT} ${VIEW} Gt "Kss,Kff,Ksf,Kfs,Khh,Kll" "Tt" "Vt"

mc: mynetlist
	cicsim run --replace replace.yaml --name ${VIEW}_mc --count 30 ${TB} ${COPT} ${VIEW} Gt "Kttmm" "Tt" "Vt"

ntc: mynetlist
	cicsim run --replace replace.yaml --name ${VIEW}_ntc ${TB} ${COPT} ${VIEW} Gt "Ktt,Kss,Kff" "Tt" Vt

temp: mynetlist
	cicsim run --replace replace.yaml --name ${VIEW}_temp ${TB} ${COPT} ${VIEW} Gt "Ktt" "Tt,Th,Tl" Vt

supply: mynetlist
	cicsim run --replace replace.yaml --name ${VIEW}_temp ${TB} ${COPT} ${VIEW} Gt "Ktt" "Tt" "Vl,Vt,Vh"

rc: mynetlist
	cicsim run --replace replace.yaml --name ${VIEW}_temp ${TB} ${COPT} ${VIEW} Gt "Kll,Ktt,Khh" "Tt" "Vt"

summary:
	cicsim summary --output "README.md"
	pandoc -s  README.md -o README.html




clean:
	-rm -rf output_*
	-rm -rf __pycache__
	-rm -rf *_obj_dir
	-rm *.run
	-rm *.pdf
	-rm *.csv
	-rm *.o
	-rm *.so
