
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
CELLS = LELO_TEMP

include ../tech/make/core.make

ota:
	cicpy sch2mag  --techlib sky130 ${LIB} LELOTEMP_OTA
mag:
	cicpy sch2mag ${LIB} ${CELL} ${OPT}
#- Two steps, and the order is the point: every subcell is generated and
#- verified before the parent that will hold them is built.
#-
#-   make subcells CELL=X   -> a .mag/.cic/.sch/.sym per subcell of X
#-   make mag      CELL=X   -> X itself
#-
#- This replaces a second `transpile --xschem` with a negative lookahead
#- over the cell name, which had to be described as "not optional"
#- because getting it wrong overwrote the hand-drawn source schematic
#- with a generated one and the next mag died on "Missing group xbl".
#- cicpy takes the list from the subcell plan by name, so there is no
#- regex to get wrong, and it never writes the parent.
subcells:
	cicpy sch2subcells ${LIB} ${CELL}
