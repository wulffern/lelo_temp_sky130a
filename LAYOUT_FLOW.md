# Layout Flow

This repository is using a schematic-driven custom layout flow built around `xschem`, `cicpy`, `magic`, and `netgen`.

## Current Flow

1. Draw the transistor-level schematic in `xschem`.
2. Name instances by function so placement groups are implicit in the schematic.
3. Generate SPICE from the schematic.
4. Run `cicpy sch2mag <LIB> <CELL>` from `work/`.
5. Let `cicpy` instantiate the primitive layout cells and do a first placement.
6. Refine placement in `<CELL>.py` with:
   - `CellGroup`
   - `StackGroup`
   - `abutTop/Bottom/Left/Right`
   - per-stack taps
   - optional dummy fill
7. Open the generated `.mag` in `magic` and inspect the result.
8. Run DRC in `magic`.
9. Run LVS in `netgen`.

## Route Debug Flow

For day-to-day routing debug, the flow now uses a fast route-short pass inside `cicpy`:

1. Run `cicpy sch2mag <LIB> <CELL>` from `work/`.
2. Let `cicpy` print a `Route short report` at the end of `sch2mag`.
3. Use that report to identify:
   - the shorted nets
   - the route command that created the short
   - the Python `file:line` callsite
4. Fix the offending route command in `<CELL>.py`.

This fast pass is intentionally narrower than a full connectivity extraction. It is aimed at answering: "which route statement in the Python created this short?"

If broader analysis is needed, `sch2mag` also supports a slower full connectivity check:

```bash
/opt/eda/python3/bin/python3 -m cicpy.cic sch2mag --check-connectivity LELO_TEMP_SKY130A LELOTEMP_CMP
```

That mode is useful for split nets and opens, but it is not the default path for routing iteration.

## The Sidecar Flow

`<CELL>.py` is a declaration, not a script. A cell describes its stacks
as classes and lets the recipe build them:

```python
class LELO_TEMP(SidecarCell):
    place = {"groupbreak": 2, "channel": 6}

    class bias(Stack):
        match = r'^x1_ibp$'
        group = "bias"
        order = ['x1_ibp']

    rows = [[bias, ccmp_a, dig]]
```

A subcell class may carry `beforePlace(self, entry)` and
`beforeRoute(self, entry)` hooks where `self` IS the built group;
returning `True` from `beforeRoute` claims the stack **entirely**, so
the built-in router leaves its boundary nets alone too. The cell itself
overrides `afterPlace` / `beforeRoute` / `beforePaint` and calls
`super()` -- the escape hatch is ordinary inheritance.

Searched routes are captured as `wires` declarations in the subcell
classes so a rebuild replays them instead of re-running the maze
router. `CICPY_NO_ROUTEPLAN=1` forces a fresh search.

## Integrating Blocks At The Top

A top level that places finished blocks obeys different rules than a
cell full of transistors. What this repository learned building
`LELO_TEMP`:

**Do not call `addPowerConnection` at a block-integration top.** It
stretches *every* published supply rectangle to the ring, mid-cell tap
bars included, and each stretched copy slices through the core it came
from. Tie each block's own edge bar instead.

**`addRouteRing` wraps the layout bounding box, which does not count
physical-only instances.** Build a rectangle spanning every instance
and use `addRouteRingOnRect`, or the ring lands inside the content.

**Attach to rings in `beforePaint`, not `beforeRoute`.** The rings
re-lay as routes grow the bounding box, so a cut placed at the
`beforeRoute` position ends up off by the difference.

**Route over the standard cells, not beside them.** The JNWTR logic
cells carry li, poly and their two M4 supply columns and nothing else,
so M2, M3 and M5 are free the full height of a strip. A corridor beside
the strip has a handful of lanes; the strip itself has as many columns
as you need. Two traps go with it: the Y-pin column *is* the AVSS
column, an M1-M4 cut stack in every cell, so a vertical there ties
every output to AVSS; and the pin rows are 4 um apart, so the stubs
reaching them must run at minimum width.

**Give every riser the highest lane in its band.** A riser that climbs
from its lane into a block passes through every lane above it.

**Order parallel risers so no lane crosses another riser.** Lanes that
run east must be assigned right to left.

### Spacing the lanes

The pitches are set by rules that are easy to guess wrong:

| Rule | What it actually asks |
|:-----|:----------------------|
| met4.5a/b | a long M4/M5 run is *large metal*: 0.4 um to its neighbours, not the 0.3 um of met4.2 |
| met3.6, met4.4a | a via stack's pass-through pad is 0.19 um^2, under the 0.24 minimum; patch it long and narrow, never as a square wider than the lane |
| met1.2 | the M2-M3 cut pad is 4.4 um, wider than a 3 um column |
| capm.11 | a MiM cap claims 1.34 um from unrelated M4, including from outside its own cell |

### The collision report

`_signal_routes` in `LELO_TEMP.py` records every wire and via stack it
draws and reports colliding nets by name, layer and coordinate at build
time:

```
ERROR: ROUTE SHORT PWRUP_N_1V8 x PWRUP_B_1V8 on M5 at (1260600,19500)..(1266600,22500)
```

It sees shorts, not opens. An open still needs the netlist -- when the
device counts match but the layout has one net *more* than the
schematic, something is split, not shorted.

## What Is New In The Flow

The current work is moving `cicpy` from plain name-based row placement toward analog-aware grouping:

- Devices that belong together are bundled into `CellGroup`s.
- Matched devices are stacked and moved as one physical unit.
- Bounding boxes are recomputed after stack and tap insertion so later `abut*()` placement is correct.
- Dummy devices can be inserted to equalize stack height.
- Terminal access is being promoted to a first-class concept so routing can reuse the legal access that already exists inside the primitive transistor cells.
- Route-debug metadata is attached to generated routes so `sch2mag` can point back to the exact Python route statement that created a short.

## Why This Matters

The transistor primitives already contain legal geometry for diffusion, local interconnect, vias, and M1 access. Instead of drawing new metal blindly, the flow is moving toward:

- asking a device where its legal access is
- reusing that access for routing and dummy shorting
- keeping placement intent in Python while leaving device-level DRC details inside the primitive cells

The same idea applies to debugging:

- use route geometry plus exposed terminal access to detect route-created shorts quickly
- reserve the heavier full-cell connectivity walk for explicit deeper checks

That is the bridge between schematic-driven generation and a more robust analog layout compiler.

## Current Comparator Example

`LELOTEMP_CMP` is the working example of this flow:

- NMOS and PMOS devices are grouped separately.
- Each functional branch is a stack.
- Taps are added per stack.
- PMOS is abutted above NMOS with an explicit branch gap.
- Dummy devices are added to square up shorter stacks.

## Commands

Run from `work/`:

```bash
/opt/eda/python3/bin/python3 -m cicpy.cic sch2mag LELO_TEMP_SKY130A LELOTEMP_CMP
/opt/eda/python3/bin/python3 -m cicpy.cic sch2mag --check-connectivity LELO_TEMP_SKY130A LELOTEMP_CMP
make drc CELL=LELOTEMP_CMP
```
