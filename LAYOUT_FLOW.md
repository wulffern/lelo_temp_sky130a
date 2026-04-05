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

## What Is New In The Flow

The current work is moving `cicpy` from plain name-based row placement toward analog-aware grouping:

- Devices that belong together are bundled into `CellGroup`s.
- Matched devices are stacked and moved as one physical unit.
- Bounding boxes are recomputed after stack and tap insertion so later `abut*()` placement is correct.
- Dummy devices can be inserted to equalize stack height.
- Terminal access is being promoted to a first-class concept so routing can reuse the legal access that already exists inside the primitive transistor cells.

## Why This Matters

The transistor primitives already contain legal geometry for diffusion, local interconnect, vias, and M1 access. Instead of drawing new metal blindly, the flow is moving toward:

- asking a device where its legal access is
- reusing that access for routing and dummy shorting
- keeping placement intent in Python while leaving device-level DRC details inside the primitive cells

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
make drc CELL=LELOTEMP_CMP
```
