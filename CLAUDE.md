# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

All commands run from `work/`. The default `CELL` is `LELO_TEMP`; always pass `CELL=` explicitly.

```bash
make mag CELL=LELOTEMP_CMP                          # regenerate .mag from schematic + .py
make mag CELL=LELOTEMP_CMP OPT=--check-connectivity # regenerate + full connectivity report
make cdl lvs CELL=LELOTEMP_CMP                      # extract CDL from .sch, then run netgen LVS
make drc CELL=LELOTEMP_CMP                          # run Magic DRC
make gds CELL=LELOTEMP_CMP                          # export GDS
```

## Architecture

This is a temperature sensor IP (Skywater 130 nm). The oscillator frequency is temperature-dependent; a digital FSM (`rtl/`) counts pulses against a 32 kHz reference. The main analog blocks live in `design/LELO_TEMP_SKY130A/`.

### Layout flow

`xschem .sch` → **cicpy** → `magic .mag` → **netgen** LVS

Each cell has a companion `<CELL>.py` in `design/LELO_TEMP_SKY130A/`. New cells are **declarative sidecars** — a `SidecarCell` subclass whose nested `Stack` classes describe the stacks and whose `rows` lists the floorplan. The recipe builds them; a subcell class may add `beforePlace(self, entry)` / `beforeRoute(self, entry)` hooks where `self` IS the built group. Returning `True` from a subcell's `beforeRoute` claims that stack **entirely**, boundary nets included.

The cell itself overrides the recipe by ordinary inheritance — `afterPlace`, `beforeRoute`, `beforePaint`, `afterPaint` — and calls `super()`. Call order:

1. `beforePlace(layout)` — flags, spacing (`noPowerRoute`, `place_xspace`, `place_groupbreak`)
2. `afterPlace(layout)` — group hierarchy, taps, dummy fill, `routeDummyDevices()` (**do not remove**)
3. `beforeRoute(layout)` — routes, rings, connections
4. `beforePaint(layout)` — anything that must see the FINAL bounding box, e.g. attaching to rings
5. `afterPaint(layout)` — post-processing (e.g. `resetOrigins`)

Searched routes are captured as `wires` declarations in the subcell classes and replayed on rebuild. `CICPY_NO_ROUTEPLAN=1` forces a fresh maze search.

`make mag` calls `cicpy sch2mag <LIB> <CELL>` which reads the SPICE from the `.sch`, looks up primitive `.mag` cells from the symlinked transistor libraries, runs the hooks, and writes the output `.mag`.

### cicpy placement API (used in `afterPlace`)

```python
nmos = layout.makeCellGroup("nmos")
stack = nmos.addStack("n_bias_ref", [inst1, inst2])
stack.addTaps()                          # CTAPBOT + CTAPTOP around the stack
nmos.fillDummyTransistors(direction="top")
nmos.routeDummyDevices()                 # M1 dummy-fill routing (internal; do not route over it)

p_stack.abutTop(n_stack, space=branch_gap)
group.updateBoundingRect()
```

Get an instance by name: `layout.getInstanceFromInstanceName("xaa_bias_ref<0>")`

### cicpy routing API (used in `beforeRoute`)

```python
layout.addConnectivityRoute(layer, regex, routeType, options, cuts, excludeInstances, includeInstances)
# routeType: "-" horizontal | "||" vertical | "-|--" L-shape LEFT | "--|-" L-shape RIGHT
# includeInstances / excludeInstances: regex on instanceName (e.g. "^xb" = PMOS, "^xa" = NMOS)

layout.addRouteRing("M1", "VDD_1V8", "t", widthmult=3, spacemult=2)
layout.addPowerConnection("VDD_1V8", "^xb", "top")
```

### Routing rules

- **M1 is reserved** for power rings, tap connections, and `routeDummyDevices()`. Never use M1 for signal `addConnectivityRoute` calls.
- M2 = vertical, M3 = horizontal, M4 = vertical.
- Cross-domain (NMOS↔PMOS) nets need an L-shaped route (`"-|--"` or `"--|-"`).
- Diode-connected gate/drain: connect in the lowest available metal layer.

### Top-level integration

`LELO_TEMP` places three finished blocks plus a logic strip into a TinyTapeout 1x1 tile. Rules that only show up at this level:

- **Never `addPowerConnection` here.** It stretches every published supply rect to the ring — tap bars included — and each copy slices through the core it came from. Tie each block's own edge bar.
- **`addRouteRing` wraps the layout bbox, which excludes physical-only instances.** Build a rect spanning every instance and use `addRouteRingOnRect`.
- **Attach to rings in `beforePaint`.** The rings re-lay as routes grow the bbox.
- **Route over the logic strip, not beside it.** JNWTR cells hold li, poly and two M4 supply columns; M2/M3/M5 are free the full height. But the **Y-pin column is the AVSS via-stack column** — a vertical there ties every output to AVSS — and pin rows are 4 um apart, so stubs run at minimum width.
- **A riser takes the highest lane in its band**, or it climbs through the lanes above it.
- **Lane pitch:** long M4/M5 runs are large metal and want 0.4 um (met4.5a/b), not 0.3. A via stack's pass-through pad is under the 0.24 um^2 minimum area — patch it long and narrow, never as a square wider than the lane.

### Route debug

`_signal_routes` in `LELO_TEMP.py` reports colliding nets by name, layer and coordinate at build time (`ROUTE SHORT <net> x <net> on <layer> at ...`). It sees shorts, not opens: if device counts match but the layout has one net **more** than the schematic, something is split.

`cicpy sch2mag` always prints a **Route short report**. Each entry names the shorted nets, the offending route command, and the `file:line` callsite in the `.py`. Fix that line and regenerate.

`--check-connectivity` additionally reports OPEN (split) nets; use it when shorts are clear but opens need diagnosis.
