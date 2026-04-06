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

Each cell may have a companion `<CELL>.py` in `design/LELO_TEMP_SKY130A/` that cicpy executes as hooks. Hook call order:

1. `beforePlace(layout)` — flags, spacing (`noPowerRoute`, `place_xspace`, `place_groupbreak`)
2. `afterPlace(layout)` — build `CellGroup`/`Stack` hierarchy, add taps, add dummy fill, call `routeDummyDevices()` (**do not remove**)
3. `beforeRoute(layout)` — all `addConnectivityRoute(...)`, `addRouteRing(...)`, `addPowerConnection(...)` calls
4. `afterPaint(layout)` — post-processing (e.g. `resetOrigins`)

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

### Route debug

`cicpy sch2mag` always prints a **Route short report**. Each entry names the shorted nets, the offending route command, and the `file:line` callsite in the `.py`. Fix that line and regenerate.

`--check-connectivity` additionally reports OPEN (split) nets; use it when shorts are clear but opens need diagnosis.
