# Temperature sensor


## Tools 

- Schematic : xschem
- Layout : magic 
- layout versus schematic : netgen
- Layout engine : cicpy sch2mag

## Commands

All commands run from `work/`. The default `CELL` is `LELO_TEMP`; always pass `CELL=` explicitly.

```bash
make mag CELL=LELOTEMP_CMP                          # regenerate .mag from schematic + .py
make mag CELL=LELOTEMP_CMP OPT=--check-connectivity # regenerate + full connectivity report
make cdl lvs CELL=LELOTEMP_CMP                      # extract CDL from .sch, then run netgen LVS
make drc CELL=LELOTEMP_CMP                          # run Magic DRC
make gds CELL=LELOTEMP_CMP                          # export GDS
```

**A cell with a `hier_cell` is NOT built by `make mag`.** `make mag`
builds it flat, which produces a different -- and worse -- layout than
the committed one. Every subcell is generated and verified first, then
the parent that holds them:

```bash
make subcells hier gds cdl lvs drc CELL=LELOTEMP_BIAS_IBP
```

That is the whole loop for `LELOTEMP_BIAS_IBP` and `LELOTEMP_OTAR`. It
reproduces the committed layout exactly, timestamp aside; if a rebuild
disagrees with what is checked in, suspect the command before the
design.

## Layout flow

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

## cicpy placement API (used in `afterPlace`)

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

## cicpy routing API (used in `beforeRoute`)

```python
layout.addConnectivityRoute(layer, regex, routeType, options, cuts, excludeInstances, includeInstances)
# routeType: "-" horizontal | "||" vertical | "-|--" L-shape LEFT | "--|-" L-shape RIGHT
# includeInstances / excludeInstances: regex on instanceName (e.g. "^xb" = PMOS, "^xa" = NMOS)

layout.addRouteRing("M1", "VDD_1V8", "t", widthmult=3, spacemult=2)
layout.addPowerConnection("VDD_1V8", "^xb", "top")
```

## Layout Hints
- Prefer functional instance names in `.sch` files. Use names like `xpd_input[1:0]`, `xnd_bias_mirror[3:0]`, `xne_load[1:0]` instead of opaque `xca*`/`xpd*`.
- In `cicpy`, placement columns are controlled by the instance group name, which is the non-numeric prefix of the instance name. Choose prefixes intentionally in the schematic so default `place()` produces the desired stack order.
- Treat placement as routing-driven. Align devices that share high-fanout or sensitive nets in the same vertical column so drains/gates can be connected mostly with straight vertical metal.
- For matched devices, keep the members adjacent and on the same row/column style. In this project that usually means stacking bused instances vertically in one column.
- Do not add arbitrary X spacing between `JNW_ATR_SKY130A` transistor stacks. NMOS and PMOS stacks are intended to abut or overlap horizontally for compact layout.
- When choosing column pitch for transistor stacks, start from overlap-first placement and only open X spacing if routing proves it necessary.
- Prefer fixing placement by renaming schematic instances to the right groups before adding custom coordinate moves in `<CELL>.py`.
- For coupled analog branches, prefer `layout.makeCellGroup(...)` and `group.addStack(...)` in the cell Python file. Use the default `cicpy` placement for stack X order, then place groups with `abutTop(...)`, `abutBottom(...)`, `abutLeft(...)`, or `abutRight(...)` and a `space=` argument.
- Use `stack.addTaps()` to place one `CTAPBOT` and one `CTAPTOP` for a whole physical stack. If tap clearance matters for later `abut*()` placement, add the taps before abutting groups so the stack bounding box includes them. Use `group.fillDummyTransistors()` when sibling stacks should be equalized in height with physical-only dummy devices.
- Before drawing custom metal to a device terminal, check whether the device already exposes legal access on that layer. In `cicpy`, prefer `instance.getTerminalAccess("D"|"G"|"S"|"B", target_layer="M1")` over guessing where to place M1.
- Treat terminal access as physical geometry, not just schematic naming. For transistor dummies in particular, reuse the device's existing M1 access rectangles instead of stamping generic bars that may violate local spacing.
- Use `CTAPBOT` and `CTAPTOP` physical cells as end-caps around vertical transistor stacks when needed. They are physical-only, so warnings about missing SPICE subckts are expected when generating layout.
- Put startup or enable devices under the branch they assist if that shortens a critical branch net. Put output pull-up/pull-down devices in a column that keeps the `VO` route short and direct.
- In custom `cicpy` Python placers, disable the default `AVDD/AVSS` paint step with `layout.noPowerRoute = True` when the cell instead uses `VDD_1V8`/`VSS`.
- `<CELL>.py` is a **declarative sidecar**: a `SidecarCell` subclass whose nested `Stack` classes describe the stacks and whose `rows` list the floorplan. A subcell hook's `self` IS the built group; returning `True` from its `beforeRoute` claims that stack entirely, boundary nets included. The cell overrides `afterPlace`/`beforeRoute`/`beforePaint` by ordinary inheritance and calls `super()`.
- Searched routes are captured as `wires` declarations in the subcell classes and replayed on rebuild; `CICPY_NO_ROUTEPLAN=1` forces a fresh maze search.
- A hand-routed cell should record what it draws and check itself. `_signal_routes` in `LELO_TEMP.py` logs every wire and via stack and reports colliding nets by name, layer and coordinate at build time. It finds shorts, not opens.
- When debugging routing, prefer the fast route-short report from `cicpy sch2mag`. It now runs automatically and is intended to point back to the Python route statement that caused the short.
- Use full connectivity checking only when needed. `cicpy sch2mag --check-connectivity <LIB> <CELL>` is slower and better suited for broader open/split-net analysis than day-to-day route debugging.
- `sch2mag` writes a top-cell `.cic` plus generated cut cells. Child library cells are not embedded in that file. When rendering or inspecting such a cell outside Magic, include dependent library `.cic` files explicitly.
- `cicpy` commands that read `.cic` now support `--I <lib.cic>` to merge additional library files before processing. Use that for `svg`, `transpile`, `jcell`, `minecraft`, and similar design readers when the top cell references external primitive libraries.
- For `LELOTEMP_CMP` SVG/debug outside Magic, include at least `JNW_ATR_SKY130A.cic` and `JNW_TR_SKY130A.cic`, and use `tech/cic/sky130A.tech` rather than `sky130.tech` because the rendered libraries use layers like `POR`.
- Keep route-debug instrumentation concise. The useful output is: shorted nets, one offending route command, and one `file:line` callsite. Avoid flooding the report with internal dummy-route details.
- Internal dummy routes should be treated as implementation detail. If a report is dominated by `xfill_*_dummy_*` nets, suppress them and focus on user-created routes such as `addConnectivityRoute(...)`.
- For quick route debug, checking generated route geometry against exposed terminal/port access is usually enough. Full recursive geometry expansion is only needed for deeper connectivity analysis.
- Run layout generation from `work/` with `cicpy sch2mag <LIB> <CELL>`, then inspect the generated `.mag` to confirm stack order and tap placement.
- A short that shorts many nets is worse than a few opens
- M1 = locali, M2 = metal1, read sky130A.tech for details
- Keep the Magic vs `cicpy` layer naming straight when inspecting `.mag`: Magic `metal3` = `cicpy M4`, Magic `metal4` = `cicpy M5`. For `JNWTR_CAPX1`, terminal `A` is on Magic `metal3` and terminal `B` is on Magic `metal4`.
- In hierarchical cells like `LELOTEMP_CCMP`, prefer routing to exposed child instance ports and `addConnectivityRoute(...)` / `addOrthogonalConnectivityRoute(...)` over custom rectangle gathering. If a parent route still needs raw terminal access, that usually means the child or primitive should expose a better port instead.
- `addOrthogonalConnectivityRoute(...)` should be allowed to discover ports from the net graph. Use `includeInstances` to limit scope instead of manually searching rectangles in the cell Python when possible.
- `OrthogonalLayerRoute` currently expects at least two access rectangles to create real route metal. If only one access is discovered, it will not form a useful connection; fix the port exposure or the `includeInstances` scope rather than trying to patch around it in the parent cell.
- `OrthogonalLayerRoute` now enforces a minimum cut array of 2, so orthogonal routes should generate `1x2` or `2x1` cuts, never `1x1`.
- When using `addPortOnEdge(...)`, `offset_trackN` moves the endpoint rectangle on the edge, while `trackN` controls the route corridor. `offset_track` shifts X for top/bottom edges and Y for left/right edges.
- Future routing is easier if child cells export every parent-used net to the boundary on a legal preferred layer. For `LELOTEMP_CMP`, that means `IBP_1U`, `PWRUP_N_1V8`, `PWRUP_1V8`, `VIN`, `VIP`, `VO`, `CMPO`, and `VC` should be reachable as intentional edge ports rather than incidental internal access.
- For parent integration, separate “distribution spines” from “local stitches”. Good pattern: first connect repeated devices internally within a local group, then connect the group to the rest of the cell with one short API-routed branch.
- For `LELOTEMP_CCMP`, keep `x1_cmp`, the NMOS helper branch, and the cap bank on one baseline, and avoid introducing a second Y band unless it solves a specific routing conflict.
- When a cap bank participates in a bias net, route the cap stack internally first on the cap’s native top metal, then connect that stack to the rest of the circuit. Do not drop vias through the MIM body to reach lower metals.
- If a hierarchical route keeps collapsing to one discovered access, treat that as a port-exposure problem first. Fix the child edge port or primitive port visibility before adding custom parent routing logic.
- For analog parent cells, reserve distinct corridors for unrelated control/bias nets early. In this block, `IBP_1U<0>` and `PWRUP_N_1V8` should not be forced through the same side corridor near `x1_cmp`.

## Top-level integration
These only show up when a cell places finished blocks rather than transistors. All measured on `LELO_TEMP`.
- **Never call `addPowerConnection` at a block-integration top.** It stretches *every* published supply rect to the ring, mid-cell tap bars included, and each stretched copy slices through the core it came from. The first top extraction came back as one VSS blob. Tie each block's own edge bar instead.
- **`addRouteRing` wraps the layout bounding box, which does not count physical-only instances.** Build a rect spanning every instance and use `addRouteRingOnRect`. The default put the bottom ring 2 um inside the content, where its 9 um li bar shorted the logic strip's AVDD to AVSS.
- **Attach to rings in `beforePaint`, not `beforeRoute`.** The rings re-lay as routes grow the bbox; a cut placed at the `beforeRoute` position lands off by the difference.
- **Route fan-out verticals OVER a standard-cell strip, not beside it.** JNWTR cells carry li, poly and their two M4 supply columns and nothing else, so M2/M3/M5 are free the strip's full height. A corridor beside the strip has a handful of lanes; the strip has as many columns as needed.
- **The Y-pin column IS the AVSS column.** Every JNWTR cell puts an M1-M4 cut stack there, so an M2 vertical down that column ties every output to AVSS. Same for the AVDD column.
- **Pin rows in the strip are 4 um apart**, so the stubs reaching them run at minimum width; 3 um stubs on neighbouring rows leave 1 um where met2.2 wants 1.4.
- **A riser takes the highest lane in its band.** Climbing from a lower lane means passing through every lane above it.
- **Order parallel risers so no lane crosses another riser.** Lanes running east must be assigned right to left.
- **Base a lane on the block's real metal extent, not on its pins.** Basing the IBP rows on the pin tops ran two of them through the block's own source bars, 1.5 um higher.
- A riser or lane that must reach several attach rows has to span all of them — when the device counts match but the layout has one net **more** than the schematic, something is open, not shorted.

## Spacing rules that are easy to guess wrong
- A long M4/M5 run is **large metal**: met4.5a/b ask 0.4 um to its neighbours, not the 0.3 um of met4.2. Parallel lanes need a 7 um pitch, not 6.
- A via stack's pad on a layer it only *passes through* is 0.44 um square = 0.19 um^2, under the 0.24 um^2 of met3.6/met4.4a. Patch it **long and narrow** (0.3 x 0.85 um); a 0.5 um square is wider than the lane and eats the spacing on both sides.
- The M2-M3 cut pad is 4.4 um, wider than a 3 um column — columns need a 6 um pitch even though the metal is 3.
- A MiM cap claims 1.34 um from unrelated M4 (capm.11), including from metal outside its own cell.

## Layout rules
- Always connect diode connected transistor gate/drain in lowest possible metal layer
- Cross-domain (NMOS<->PMOS) nets need an L-shaped route (`"-|--"` or `"--|-"`)
- **M1 is reserved** for power rings, tap connections and `routeDummyDevices()` — never for signal routing
- M2 is vertical
- M3 is horizontal
- M4 is vertical

## Route debug

`_signal_routes` in `LELO_TEMP.py` reports colliding nets by name, layer and coordinate at build time (`ROUTE SHORT <net> x <net> on <layer> at ...`). It sees shorts, not opens: if device counts match but the layout has one net **more** than the schematic, something is split.

`cicpy sch2mag` always prints a **Route short report**. Each entry names the shorted nets, the offending route command, and the `file:line` callsite in the `.py`. Fix that line and regenerate.

`--check-connectivity` additionally reports OPEN (split) nets; use it when shorts are clear but opens need diagnosis.

## Files 
```bash 
├── config.yaml  # Dependencies
├── design
│   ├── JNW_ATR_SKY130A -> ../../jnw_atr_sky130a/design/JNW_ATR_SKY130A  #Analog Transistor library
│   ├── JNW_TR_SKY130A -> ../../jnw_tr_sky130a/design/JNW_TR_SKY130A # Transistor library and standard cells
│   ├── LELO_ATR_SKY130A -> ../../lelo_atr_sky130a/design/LELO_ATR_SKY130A #Analog Transistor library
│   └── LELO_TEMP_SKY130A #Main library for all files that belong to this module: Schematic = .sch, Layout = .mag, description = .md, layout engine = .py
├── info.yaml # About this module 
├── py
│   ├── LELO_TEMP.py # How the temperature sensor works
├── rtl
│   ├── tempCounter.v # Counter to count the output oscillations
│   └── tempFsm.v # Statemachine
├── sim #testbenches
│   ├── LELOTEMP_BIAS_IBP 
│   ├── LELO_TEMP
│   ├── cicsim.yaml -> ../tech/cicsim/cicsim.yaml # Spice libaries
│   ├── tb_ams_lelo_temp
│   └── tb_lelo_temp
├── tech -> ../tech_sky130A # Technology library 
└── work
    ├── Makefile # How to run commands
```

---
LELOTEMP_CMP Layout Routing (added 2026-04-05)

Workflow

- Regenerate layout from schematic + .py: make mag CELL=LELOTEMP_CMP (from work/)
- Check routing connectivity: make mag CELL=LELOTEMP_CMP OPT=--check-connectivity
- Run LVS: make cdl lvs CELL=LELOTEMP_CMP (from work/)

cicpy Routing API (beforeRoute function)

layout.addConnectivityRoute(layer, regex, routeType, options, cuts, excludeInstances, includeInstances)
- Route types: "-" horizontal, "||" vertical, "-|--" L-shaped (LEFT), "--|-" R-shaped (RIGHT)
- includeInstances: regex to limit which instances contribute rectangles (e.g. "^xb" = PMOS, "^xa" = NMOS)
- --check-connectivity reports OPEN (split nets) and SHORT (merged nets) after routing

LELOTEMP_CMP Net Topology

- NMOS group (prefix xa): n_bias_ref, n_bias_mirror, n_left, n_right, n_out
- PMOS group (prefix xb): p_bias_ref, p_bias_mirror, p_left, p_right, p_out
- Cross-domain nets (need M2 -|--): VBP2, net1, net2, VO
- PMOS-only horizontal (M1 -, includeInstances="^xb"): VS, VIN, VIP, PWRUP_1V8
- NMOS-only horizontal (M1 -, includeInstances="^xa"): IBP_1U, PWRUP_N_1V8

---
