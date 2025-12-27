

CELL=LELO_TEMP
LIB=LELO_TEMP_SKY130A

all: tb plot


fl:
	echo "//Automatic include file" > tb.fl
	cat "../../design/${LIB}/${CELL}.fl" | xargs -I{} echo "../../design/${LIB}/{}">> tb.fl
	#echo "counter.v" >> tb.fl
	#echo "temp_osc_controller.v" >> tb.fl
	echo "../../rtl/tempCounter.v" >> tb.fl
	echo "../../rtl/tempFsm.v" >> tb.fl

	echo "tb.v" >> tb.fl
	-rm tb.csv

tb: fl
	iverilog  -g2012 -o design -c tb.fl -DANA_TYPE_REAL -DLELO_DESIGN=${CELL}
	vvp -n design


plot:
	python3 tb.py

clean:
	-rm *.vcd
	-rm design
	-rm tb.csv


dot:
	dot -Tsvg ../../rtl/tempFsm.dot -o tempFsm.svg
