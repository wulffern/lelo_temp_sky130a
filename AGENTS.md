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
- Keep route-debug instrumentation concise. The useful output is: shorted nets, one offending route command, and one `file:line` callsite. Avoid flooding the report with internal dummy-route details.
- Internal dummy routes should be treated as implementation detail. If a report is dominated by `xfill_*_dummy_*` nets, suppress them and focus on user-created routes such as `addConnectivityRoute(...)`.
- For quick route debug, checking generated route geometry against exposed terminal/port access is usually enough. Full recursive geometry expansion is only needed for deeper connectivity analysis.
- Run layout generation from `work/` with `cicpy sch2mag <LIB> <CELL>`, then inspect the generated `.mag` to confirm stack order and tap placement.

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
