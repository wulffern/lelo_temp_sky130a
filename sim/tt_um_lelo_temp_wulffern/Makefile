TB=tran
VIEW=Sch
CELL=tt_um_lelo_temp_wulffern
LIB =LELO_TEMP_SKY130A
OPT=
THREADS=8
PROGRESS=--progress

include ../../tech/make/sim.make

#- THE TWO VIEWS MUST SPELL THE PORTS THE SAME WAY. xschem netlists
#- the tree with <> buses (the core cells' own convention), but the
#- layout's port labels are the TinyTapeout DEF names with [] -- so
#- the Lay netlist says ui_in[0] where the Sch netlist says ui_in<0>,
#- and one testbench cannot force both. As in cdl_tt: only the five
#- TT port prefixes are mapped to [], the core's own buses keep <>.
netlist: netlist_cell
	perl -pi -e 's/\b(ui_in|uio_in|uio_out|uio_oe|uo_out)<(\d+)>/$$1\[$$2\]/g' ../../work/xsch/${CELL}.spice
	perl ../../tech/script/genxdut ../../work/xsch/${CELL}.spice ${CELL}
#- the LPE diode-unit conversion lives in tech/make/sim.make now,
#- beside the netlist step that makes the file

#- FUNCTION SIM, both views: does the tile power up through the TT
#- pins and oscillate on uo_out[0]. The exhaustive corner work lives
#- with LELO_TEMP; this bench owns only what the WRAPPER adds -- the
#- pad routing, the tie-low resistors, the antenna diode, the supply
#- straps and the power stacks.
typical: netlist
	cicsim run --threads ${THREADS} ${PROGRESS} --replace replace.yaml --name ${VIEW}_typical ${TB} ${OPT} ${VIEW} Gt Ktt Tt Vt

both:
	${MAKE} typical VIEW=Sch
	${MAKE} typical VIEW=Lay
