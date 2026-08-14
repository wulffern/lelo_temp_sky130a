---
layout: page
title: Layout Flow
---

# Layout Flow

This repository is using a schematic-driven custom layout flow built around `xschem`, `cicpy`, `magic`, and `netgen`.

## Current Flow

1. Draw the transistor-level schematic in `xschem`. Instance names are
   load-bearing: the sidecar claims devices with regexes over them, and
   they are lowercase (`Xxfill_...` reaches the tools as `xxfill_...`
   and slips past every `xfill_` check).
2. Describe the cell in `design/<LIB>/<CELL>.py` -- the sidecar. See
   below; it is a declaration, not a script.
3. Build, from `work/`:

   ```bash
   make mag CELL=<CELL>
   ```

   ONE command and one pass. If the cell is made of subcells they are
   each built as a cell of their own -- `.mag`, `.cic`, `.sch`, `.sym`
   -- and the top is assembled from them.
4. Verify each subcell standalone, then the top:

   ```bash
   make drc CELL=<CELL>_<SUBCELL>
   make gds cdl lvs CELL=<CELL>_<SUBCELL>   # gds FIRST or extraction is stale
   make drc CELL=<CELL>
   make gds cdl lvs CELL=<CELL>
   ```

Read the LVS verdict from the **`Final result:`** line and nowhere
else. netgen prints "Netlists match uniquely **with port errors**" on
*failing* runs, so grepping for "match uniquely" green-lights broken
cells -- measured, a subcell shipped with its ladder unrouted behind
exactly that.

## Route Debug Flow

`make mag` prints a route-short report: the shorted nets, the route
that created the short, and the Python `file:line` that asked for it.
When a route raises instead, the build names it -- the cell, the net,
the layer and the route type -- because a technology error like
"could not create cut from 1 to M5" says nothing about which of a
hundred routes asked for it, and the answer is usually the one just
added.

`cicpy checkroutes <cic> <tech> <cell>` reports shorts and opens from a
`.cic` already on disk, in about a second and without touching a file.
Use it to *localise*, and two things about it:

- **it flattens, and subcells reuse net names.** `VO`, `VIN` and `LPI`
  are internal to more than one block, so one component carrying two of
  them reads as a short. A bus and its member (`IBP_1U`, `IBP_1U<3>`)
  read as one too. `LELO_TEMP` reported 13 such on a layout netgen
  calls free of shorts.
- **LVS is the verdict; this is a lead.** DRC cannot see a short at
  all, and a DRC improvement can *be* one -- sweeping one net's lane
  gave 2/4/2/0 errors for four lanes, and the lane with the worst count
  was the only one that did not merge two nets.

## The Sidecar Flow

`design/<LIB>/<CELL>.py` **is** the cell. One class per cell, one
nested class per piece, and the classes are real: `Stack` subclasses
the framework's own `StackGroup` and `SidecarCell` subclasses
`LayoutCell`, so a hook's `self` is the group that was actually built
and a rename in the framework breaks the design file loudly instead of
silently.

```python
from cicpy.sidecar import SidecarCell, Stack, DiffPair, Mirror

class LELO_TEMP(SidecarCell):

    place = {"groupbreak": 2, "channel": 6}   # flat-build knobs

    class bias(Stack):                 # class name = piece name
        match = r'^x1_ibp$'            # which instances it claims
        group = "bias"
        order = ['x1_ibp']             # bottom-to-top; this is placement

        def beforeRoute(self, entry):  # self IS the built group
            self.addConnectivityRoute(...)        # group-scoped
            self.layout.addConnectivityRoute(...) # parent-scoped
            return None                # True = "I routed this entirely"

    rows = [[bias, ccmp, dig]]         # the floorplan, bottom row first
    supplies = [{"net": "VDD_1V8", "ring": "t", "strap": "top"}]
```

`match` is not optional. A nested class without one, or with a regex
that does not compile, is **dropped** with a warning -- it could claim
nothing anyway, and the consumer would otherwise die on a typo in one
class with a message naming neither the cell nor the piece.

A cell that needs more than declarations overrides
`beforePlace` / `afterPlace` / `beforeRoute` / `beforePaint` /
`place` / `route` and calls `super()`. The escape hatch is ordinary
inheritance; ask `self.assembled` when an override is only right in one
of the two passes.

Searched routes are captured back into the subcell classes as `wires`
declarations, so a rebuild replays them instead of re-running the maze
router (measured: 74 s to 0.5 s). `CICPY_NO_ROUTEPLAN=1` forces a fresh
search.

## The Hierarchy Flow

**What a cell is made of is not a flag, it is content.** A cell is
either assembled from child cells or it places stacks of devices, and
the two are mutually exclusive:

| the cell declares | it is made of | the recipe |
|:---|:---|:---|
| `routes` | **subcells** -- other cells | `hierarchy()` splits, then assembles |
| no `routes` | **stacks** of devices | flat placement |

`routes` says *how the pieces are joined*, not whether they exist. A
child ends the recursion by having stacks and no subcells.

The split itself is a property of the **netlist**, so it is known
before anything is placed:

- **membership** comes from the design's own `match` regexes over the
  netlist's instances, in declaration order -- **first match wins**, so
  write the file specific to general;
- **a net is a port** of a subcell exactly when it is used outside it.

That is what lets a subcell be *built* as a cell from its own
subcircuit, from its own origin, rather than copied out of a placed
parent.

```python
class LELO_TEMP(SidecarCell):
    ...
    channel = 8            # um between the rows of the assembly
    routes = [             # one ChannelRoute per crossing net
        {"net": "VCP", "track": 6,
         "drops": [[n_mirr, "M2", "left"], [p_bias, "M2", "right"]]},
    ]
```

Drops are **discovered**: every placed subcell whose ports expose the
net gets one. The `drops:` list only *overrides* -- for columns where
pins share an x and must split by layer or alignment.

### A block publishes on an EDGE

The one rule that decides whether a top level can be routed at all.
`LELO_TEMP`'s last open net cost eight routing attempts and none of
them was a routing problem: the comparator pair published
`PWRUP_B_1V8` a third of the way into the block and seven eighths of
the way up, inside its own routing. **A port in the middle of a block
cannot be left without crossing the block.**

The fix is a placement one -- move the port, not the route. Two ways
that worked here:

- **under the MiM.** A cap bank owns the upper metals (M4 and up) and
  carries almost nothing beneath it -- one via stack in the whole bank.
  A run east on M3 goes under it to the block edge.
- **through a tapcell row.** A tapcell carries no signal pin, so no row
  is booked in it and no via pad sits in it, and the strip's lanes
  cross it as bare wire. It is the one place a leg can cross a lane it
  does not own.

### Letting the search route a net

For a net that the lane plan cannot place, hand it to the maze router.
It runs at *draw* time, so everything the design has already told is
metal it can see:

```python
layout.addMazeRoute("^PWRUP_B_1V8$", layers=["M2", "M3", "M5"],
                    rects=[pb, P(ccmp, "PWRUP_B_1V8")])
```

- **narrow the stack.** Left to the technology's own chain the search
  runs verticals on the pin layer, which is the supply layer, and its
  own via check then calls the descent blocked.
- **each leg gets the stack that leg needs.** A leg passing a MiM must
  not have M4 (capm.11 holds 1.34 um off a MiM); a leg between two low
  M3 ports is happy on M3/M4.
- **name the rects.** Left to discovery the search starts on metal
  *inside* a block and is walled in before it begins.

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

## Where The Flow Stands

`LELO_TEMP` is the worked example of all of the above and it verifies:

```
LELO_TEMP        DRC OK   Circuits match uniquely.
LELO_TEMP_BIAS   DRC OK   Circuits match uniquely.
LELO_TEMP_CCMP   DRC OK   Circuits match uniquely.
LELO_TEMP_DIG    DRC OK   Circuits match uniquely.
```

Three blocks -- a bias block, a comparator pair and a logic strip --
each split out of the top's own netlist by the sidecar, each built and
verified as a cell of its own, and assembled by the top.

What the flow now asks a design to state, rather than to draw:

- which devices form a piece, and what kind of piece (`match`, the
  base class);
- the floorplan, as `rows`;
- the supplies, as rings and straps;
- how the pieces are joined, as `routes`;
- and, where the lane plan runs out, *which net the search should take
  and on which layers*.

What it asks the tools, rather than spelling: where a block is free
(`addBlockChannel`, and always **for a net** -- a net's own metal is
not in its way), which lanes are occupied (`tracks`), what stops a via
(`blockers`), and whether there is a way through at all (`findroute`).

**Aim at a channel, never at a coordinate.** A step takes something
*named* in the design -- a channel track, a pin, a landing -- and
`resolveAnchor` rejects a raw integer outright. Register the gaps the
placement makes in `afterPlace` and route to them by name; the
registration holds the only numbers, and they come from the placement
that just ran.

## Commands

Run from `work/`:

```bash
make mag CELL=LELO_TEMP              # build: subcells and the top, one pass
make drc CELL=LELO_TEMP              # magic DRC
make gds cdl lvs CELL=LELO_TEMP      # gds FIRST, then extract and compare
```

Debugging aids:

```bash
CICPY_TRACE=<net> make mag CELL=X    # where every step of that net resolved
CICPY_NO_ROUTEPLAN=1 make mag CELL=X # ignore replayed wires, search afresh
cicpy tracks   <cic> <tech> <cell> --layer M3
cicpy blockers <cic> <tech> <cell> --net N --box X1:X2:Y1:Y2
cicpy findroute <cic> <tech> <cell> --net N --start X,Y,L --stop X,Y,L
```

The technology file is `tech/cic/sky130A.tech`. `tech/` is a directory
of tooling, not of technology files -- given a path that does not
exist, some tools used to answer "clean".
