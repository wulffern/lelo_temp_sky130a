
#- Core makefile provides the following commands:
# -----------------------------------------------------------
# ip: generate ../design/<LIB> from ../cic/ip.json
# gds: generate gds/<CELL>.gds
# cdl: generate cdl/<CELL>.cdl
# lvs: Check cdl/<CELL>.cdl versus ../design/<LIB>/<CELL>.mag
# lpe: Extract parasitics lpe/<CELL>.spi
# drc: Run design rule checks on ../design/<LIB>/<CELL>.mag
# -----------------------------------------------------------

PREFIX=
LIB=LELO_TEMP_SKY130A
CELL=LELO_TEMP

#- Provide cells you want to check for the lvsall drcall commands
CELLS = LELOTEMP_CMPR LELOTEMP_CCMPR LELOTEMP_OTAR LELOTEMP_BIAS_IBP LELO_TEMP

#- Leaf first, because each of these has a sidecar of its own and the
#- one above it instantiates the result: CMP sits inside CCMP, OTAR
#- inside BIAS_IBP, and both inside LELO_TEMP. `make rebuildall` walks
#- this order and then checks every cell.
MAGCELLS = LELOTEMP_CMPR LELOTEMP_CCMPR LELOTEMP_OTAR LELOTEMP_BIAS_IBP LELO_TEMP

include ../tech/make/core.make

#- ONE command for every cell, and one pass. sch2mag reads <CELL>.py
#- and the cell decides what it is made of: a sidecar holding subcell
#- classes is made of SUBCELLS -- it splits its own netlist, builds a
#- cell per part and assembles them -- and one holding none is made of
#- devices. Both are `make mag`.
#-
#- There used to be a second and third command here (`make subcells`,
#- `make hier`) with a generated <CELL>_HIER.spice between them, and
#- nothing in the cell to say which command it needed: built the flat
#- way a hierarchical cell SUCCEEDED, wrote a .mag and failed LVS with
#- split nets, which reads as the design having broken rather than the
#- command being wrong.
mag:
	cicpy sch2mag ${LIB} ${CELL} ${OPT}

#- the hand schematics netlist buses as [] while the layout labels
#- carry <> everywhere; netgen breaks symmetric-net ties by NAME, so
#- the CDL must use the same delimiters (measured: four topologically
#- identical IBP_1U outputs paired arbitrarily)
cdl:
	@test -d cdl || mkdir cdl
	-xschem -q -x -b -s --tcl "set lvs_netlist 1; set netlist_dir $(PWD)/cdl/; set bus_replacement_char {<>};" -n ../design/$(LIB)/$(PRCELL).sch
