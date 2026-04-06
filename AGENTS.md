# Temperature sensor


## Tools 

See work/Makefile for commands
- Schematic : xschem
- Layout : magic 
- layout versus schematic : netgen
- Layout engine : cicpy sch2mag

## Folder
- commands needs to be run in work/

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

## Layout rules
- Always connect diode connected transistor gate/drain in lowest possible metal layer
- M1 cannot be used for signal routing
- M2 is vertical
- M3 is horizontal
- M4 is vertical

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
