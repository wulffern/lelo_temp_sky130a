
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
#- $(CURDIR), NOT $(PWD). Make exports PWD as the directory it was
#- INVOKED from, so under `make -C work cdl` -- which is how every
#- check runs -- this wrote the netlist to <ip>/cdl/ while lvs reads
#- work/cdl/. xschem then failed on the missing directory with exit
#- 10, the `-` prefix swallowed it, and LVS compared the last netlist
#- that happened to land in work/cdl/. Measured: work/cdl/LELO_TEMP.spice
#- was four days stale while `make check` reported on it daily.
#-
#- AND THE GUARD IS THE ARTEFACT, NOT THE EXIT CODE. xschem exits 10
#- on a successful headless netlist in this environment (measured: exit
#- 10, netlist written, every time) -- which is why the `-` was here and
#- why it hid the wrong-directory bug above. So: delete the netlist
#- first, tolerate the exit code, then REQUIRE the file. A run that
#- writes nothing now stops the build instead of leaving lvs to compare
#- whatever was in the directory.
cdl:
	@test -d cdl || mkdir cdl
	@rm -f cdl/$(PRCELL).spice
	-xschem -q -x -b -s --tcl "set lvs_netlist 1; set netlist_dir $(CURDIR)/cdl/; set bus_replacement_char {<>};" -n ../design/$(LIB)/$(PRCELL).sch
	@test -s cdl/$(PRCELL).spice || { echo "cdl: xschem wrote no netlist for $(PRCELL); lvs would have compared a stale one"; exit 1; }
