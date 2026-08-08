
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

#- Schematics for the generated stack cells, so each stack can be
#- netlisted and LVS'd on its own.
#-
#- A separate target, run AFTER mag and from the design directory, and
#- both of those matter. Chained onto mag it re-enters the pycell, whose
#- afterPlace wants schematic groups a .cic does not carry
#- ("Missing group xbl"). And the stack cells only exist in the .cic
#- once mag has written it.
#-
#- Not done from inside the flow either: driving XschemPrinter by hand
#- there emits every symbol and silently omits every wire, because
#- symbolAndWrite returns quietly when a referenced cell is not in
#- printer.cells and at that point design.cells holds only the top cell.
#- --exclude is not optional. transpile writes a schematic for EVERY
#- cell in the .cic, and that includes ${CELL} itself: without this it
#- overwrites the hand-drawn source schematic with a generated one that
#- has no groups, and the next mag fails with "Missing group xbl". The
#- regex keeps everything whose name is not ${CELL}_<stack>.
stacksch:
	cd ../design && cicpy transpile ${LIB}/${CELL}.cic \
		../../tech_sky130A/cic/sky130.tech ${LIB} --xschem \
		--exclude '^(?!${CELL}_).*' \
		--I ../../rey_atr_sky130a/design/REY_ATR_SKY130A.cic
