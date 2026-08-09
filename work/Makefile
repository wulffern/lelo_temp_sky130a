
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
#- SUBCELL=<name> narrows what is WRITTEN, never what is built: the cell
#- is placed and routed exactly as always, so a subcell taken on its own
#- is the same subcell a full run produces. On a design this size it
#- saves no time -- everything here is under two seconds -- but only the
#- artefact being worked on moves, so a diff shows what the edit did and
#- nothing else.
#-
#-   make subcells CELL=X                 all of them
#-   make subcells CELL=X SUBCELL=p_sw    just that one, and its .py
subcells:
	cicpy sch2subcells ${LIB} ${CELL} $(if ${SUBCELL},--subcell ${SUBCELL},)

#- The top as eight instances instead of seventy devices: place the
#- generated hierarchical netlist with the <CELL>_HIER hooks and
#- publish the result as <CELL> itself. Every subcell passes LVS
#- standalone, so this IS the cell -- gds/cdl/lvs run on it as
#- LELOTEMP_OTAR like any other.
hier:
	cicpy spi2mag ../design/${LIB}/${CELL}_HIER.spice ${LIB} ${CELL}_HIER --outcell ${CELL} ${OPT}
