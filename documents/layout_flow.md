---
layout: page
title: Layout Flow
---

# Layout Flow

The layout in this repository is schematic driven. The schematic is drawn in
`xschem`, the layout is written by `cicpy`, and `magic` and `netgen` check it.

Nothing here is automatic analog layout. What is automated is the *drawing*:
the design says what the pieces are, where they go and how they are joined,
and `cicpy` turns that into geometry. The saying is a Python file, and it is
the first thing to understand.

## The sidecar

For every cell `<CELL>` in library `<LIB>` there is a file

```
design/<LIB>/<CELL>.py
```

That file **is** the cell. It is a declaration, not a script.

```python
from cicpy.sidecar import SidecarCell, Stack, DiffPair, Mirror

class LELO_TEMP(SidecarCell):

    place = {"groupbreak": 2, "channel": 6}   # placement knobs

    class bias(Stack):                 # class name = piece name
        match = r'^x1_ibp$'            # which instances it claims
        group = "bias"
        order = ['x1_ibp']             # bottom-to-top; this is placement

        def beforeRoute(self, entry):  # self IS the built group
            self.addConnectivityRoute(...)        # group-scoped
            self.layout.addConnectivityRoute(...) # parent-scoped
            return None                # True = "I routed this entirely"

    rows = [[bias, ccmp, dig]]         # the floorplan, bottom row first
    supplies = []                      # rings and straps
    routes = []                        # how the pieces are joined
```

One class per cell, one nested class per piece. The classes are real:
`Stack` subclasses the framework's own `StackGroup` and `SidecarCell`
subclasses `LayoutCell`. A hook's `self` is therefore the group that was
actually built, and a rename in the framework breaks the design file loudly
instead of silently.

`rows` and the drop lists reference the *classes*, not their names, so a typo
is a `NameError` at import time rather than an empty match hours later.

`match` is not optional. A nested class without one, or with a regex that does
not compile, is **dropped with a warning**. It could not claim anything
anyway, and without the check the whole build dies on a typo in one class with
a message naming neither the cell nor the piece.

Instance names are load-bearing, because `match` is a regex over them, and
they arrive lowercase. `Xxfill_...` reaches the tools as `xxfill_...` and
slips past every `xfill_` check.

A cell that needs more than declarations overrides `beforePlace`,
`afterPlace`, `beforeRoute`, `beforePaint`, `place` or `route` and calls
`super()`. The escape hatch is ordinary inheritance.

Searched routes are captured back into the subcell classes as `wires`
declarations, so a rebuild replays them instead of re-running the maze router.
Measured: 74 s down to 0.5 s. `CICPY_NO_ROUTEPLAN=1` forces a fresh search.

## What a cell is made of

A cell either holds child cells or it holds stacks of devices. The two are
mutually exclusive, and **what decides is content, not a flag**: a cell that
declares nested subcell classes is made of subcells, and one that declares
none places devices itself.

Every declared piece is built as a cell of its own, always. `hierarchy()`
splits the cell's own netlist, builds a `LayoutCell` per part from its own
subcircuit and from its own origin, and registers it; the parent is then left
holding one instance of each and tiles them by `rows`.

`routes` does **not** decide this. It says *how the pieces are joined* -- one
`ChannelRoute` per net that crosses between them:

```python
class LELOTEMP_OTAR(SidecarCell):
    ...
    channel = 8            # um between the rows of the assembly
    routes = [             # one ChannelRoute per crossing net
        {"net": "VCP", "track": 6,
         "drops": [[n_mirr, "M2", "left"], [p_bias, "M2", "right"]]},
    ]
```

`LELO_TEMP` itself declares `routes = []`. It is still made of subcells; it
simply has no channel routes of its own to declare, and its crossing nets are
laid by `_signal_routes` instead.

This used to be conditional -- `hierarchy()` ran only for a cell that declared
`routes` -- which made what a cell *was* depend on whether its crossing nets
happened to be written down. The one cell in this design with nothing to
declare stayed flat and grew 150 lines of `Rect` and `Cut` reaching into its
neighbours' instances.

The split itself is a property of the **netlist**, so it is known before
anything is placed:

- **membership** comes from the design's own `match` regexes over the
  netlist's instances, in declaration order -- **first match wins**, so write
  the file specific to general;
- **a net is a port** of a subcell exactly when it is used outside it.

## Building

From `work/`, one command and one pass:

```bash
make mag CELL=<CELL>
```

If the cell is made of subcells they are each built as a cell of their own --
`.mag`, `.cic`, `.sch`, `.sym` -- and the top is assembled from them. There is
no second command, no generated `<CELL>_HIER.spice` between two passes and no
role to pass in.

`mag` is defined in this IP's `work/Makefile`, not in the shared
`tech/make/core.make`; it is one line, `cicpy sch2mag ${LIB} ${CELL}`.

## Verifying

Verify each subcell standalone, then the top:

```bash
make drc CELL=LELO_TEMP_BIAS
make cdl lvs CELL=LELO_TEMP_BIAS
make drc CELL=LELO_TEMP
make cdl lvs CELL=LELO_TEMP
```

`cdl` netlists the schematic, `lvs` extracts `design/<LIB>/<CELL>.mag` with
magic and hands both to netgen. GDS is not part of that path -- `make gds` is
for delivery and for the klayout deck, and can be run whenever.

Read the LVS verdict from the **`Final result:`** line of
`lvs/<CELL>_lvs.log` and nowhere else. netgen prints "Netlists match uniquely
**with port errors**" on *failing* runs, so grepping for "match uniquely"
green-lights broken cells -- measured, a subcell shipped with its ladder
unrouted behind exactly that.

## Debugging routes

`make mag` prints a route-short report: the shorted nets, the route that
created the short, and the Python `file:line` that asked for it. When a route
raises instead, the build names the cell, the net, the layer and the route
type, because a technology error like "could not create cut from 1 to M5" says
nothing about which of a hundred routes asked for it -- and the answer is
usually the one just added.

```bash
cicpy checkroutes <cic> <tech> <cell>
```

reports shorts and opens from a `.cic` already on disk, in about a second and
without touching a file. Use it to *localise*, and mind two things:

- **it flattens, and subcells reuse net names.** `VO`, `VIN` and `LPI` are
  internal to more than one block, so one component carrying two of them reads
  as a short. A bus and its member (`IBP_1U`, `IBP_1U<3>`) read as one too.
  `LELO_TEMP` reported 13 such on a layout netgen calls free of shorts.
- **LVS is the verdict; this is a lead.** DRC cannot see a short at all, and a
  DRC improvement can *be* one -- sweeping one net's lane gave 2/4/2/0 errors
  for four lanes, and the lane with the worst count was the only one that did
  not merge two nets.

The technology file is `tech/cic/sky130A.tech`. `tech/` is a directory of
tooling, not of technology files -- given a path that does not exist, some
tools used to answer "clean".

## Routing rules learned here

### A block publishes on an EDGE

This one rule decides whether a top level can be routed at all.
`LELO_TEMP`'s last open net cost eight routing attempts and none of them was a
routing problem: the comparator pair published `PWRUP_B_1V8` a third of the
way into the block and seven eighths of the way up, inside its own routing.
**A port in the middle of a block cannot be left without crossing the block.**

The fix is a placement one -- move the port, not the route. Two ways that
worked here:

- **under the MiM.** A cap bank owns the upper metals (M4 and up) and carries
  almost nothing beneath it -- one via stack in the whole bank. A run east on
  M3 goes under it to the block edge.
- **through a tapcell row.** A tapcell carries no signal pin, so no row is
  booked in it and no via pad sits in it, and the strip's lanes cross it as
  bare wire. It is the one place a leg can cross a lane it does not own.

### Aim at a channel, never at a coordinate

A step takes something *named* in the design -- a channel track, a pin, a
landing -- and `resolveAnchor` rejects a raw integer outright. Register the
gaps the placement makes in `afterPlace` and route to them by name. The
registration holds the only numbers, and they come from the placement that
just ran.

### Letting the search route a net

For a net the lane plan cannot place, hand it to the maze router. It runs at
*draw* time, so everything the design has already told is metal it can see:

```python
layout.addMazeRoute("^PWRUP_B_1V8$", layers=["M2", "M3", "M5"],
                    rects=[pb, P(ccmp, "PWRUP_B_1V8")])
```

- **narrow the stack.** Left to the technology's own chain the search runs
  verticals on the pin layer, which is the supply layer, and its own via check
  then calls the descent blocked.
- **each leg gets the stack that leg needs.** A leg passing a MiM must not
  have M4 (capm.11 holds 1.34 um off a MiM); a leg between two low M3 ports is
  happy on M3/M4.
- **name the rects.** Left to discovery the search starts on metal *inside* a
  block and is walled in before it begins.

## Integrating blocks at the top

A top level that places finished blocks obeys different rules than a cell full
of transistors. What this repository learned building `LELO_TEMP`:

**Do not call `addPowerConnection` at a block-integration top.** It stretches
*every* published supply rectangle to the ring, mid-cell tap bars included,
and each stretched copy slices through the core it came from. Tie each block's
own edge bar instead.

**`addRouteRing` wraps the layout bounding box, which does not count
physical-only instances.** Build a rectangle spanning every instance and use
`addRouteRingOnRect`, or the ring lands inside the content.

**Attach to rings in `beforePaint`, not `beforeRoute`.** The rings re-lay as
routes grow the bounding box, so a cut placed at the `beforeRoute` position
ends up off by the difference.

**Route over the standard cells, not beside them.** The JNWTR logic cells
carry li, poly and their two M4 supply columns and nothing else, so M2, M3 and
M5 are free the full height of a strip. A corridor beside the strip has a
handful of lanes; the strip itself has as many columns as you need. Two traps
go with it: the Y-pin column *is* the AVSS column, an M1-M4 cut stack in every
cell, so a vertical there ties every output to AVSS; and the pin rows are
4 um apart, so the stubs reaching them must run at minimum width.

**Give every riser the highest lane in its band.** A riser that climbs from
its lane into a block passes through every lane above it.

**Order parallel risers so no lane crosses another riser.** Lanes that run
east must be assigned right to left.

### Spacing the lanes

The pitches are set by rules that are easy to guess wrong:

| Rule | What it actually asks |
|:-----|:----------------------|
| met4.5a/b | a long M4/M5 run is *large metal*: 0.4 um to its neighbours, not the 0.3 um of met4.2 |
| met3.6, met4.4a | a via stack's pass-through pad is 0.19 um^2, under the 0.24 minimum; patch it long and narrow, never as a square wider than the lane |
| met1.2 | the M2-M3 cut pad is 4.4 um, wider than a 3 um column |
| capm.11 | a MiM cap claims 1.34 um from unrelated M4, including from outside its own cell |

### The collision report

`_signal_routes` in `LELO_TEMP.py` records every wire and via stack it draws
and reports colliding nets by name, layer and coordinate at build time:

```
ERROR: ROUTE SHORT PWRUP_N_1V8 x PWRUP_B_1V8 on M5 at (1260600,19500)..(1266600,22500)
```

It sees shorts, not opens. An open still needs the netlist -- when the device
counts match but the layout has one net *more* than the schematic, something
is split, not shorted.

## Where the flow stands

`LELO_TEMP` is the worked example of all of the above and it verifies:

```
LELO_TEMP        DRC OK   Circuits match uniquely.
LELO_TEMP_BIAS   DRC OK   Circuits match uniquely.
LELO_TEMP_CCMP   DRC OK   Circuits match uniquely.
LELO_TEMP_DIG    DRC OK   Circuits match uniquely.
```

Three blocks -- a bias block, a comparator pair and a logic strip -- each
split out of the top's own netlist by the sidecar, each built and verified as
a cell of its own, and assembled by the top.

What the flow now asks a design to state, rather than to draw:

- which devices form a piece, and what kind of piece (`match`, the base
  class);
- the floorplan, as `rows`;
- the supplies, as rings and straps;
- how the pieces are joined, as `routes`;
- and, where the lane plan runs out, *which net the search should take and on
  which layers*.

What it asks the tools, rather than spelling: where a block is free
(`addBlockChannel`, and always **for a net** -- a net's own metal is not in
its way), which lanes are occupied (`tracks`), what stops a via (`blockers`),
and whether there is a way through at all (`findroute`).

## Commands

Run from `work/`:

```bash
make mag CELL=LELO_TEMP          # build: subcells and the top, one pass
make drc CELL=LELO_TEMP          # magic DRC
make cdl lvs CELL=LELO_TEMP      # netlist the schematic, extract, compare
make gds CELL=LELO_TEMP          # GDS out
```

Debugging aids:

```bash
CICPY_TRACE=<net> make mag CELL=X    # where every step of that net resolved
CICPY_NO_ROUTEPLAN=1 make mag CELL=X # ignore replayed wires, search afresh
cicpy checkroutes <cic> <tech> <cell>
cicpy tracks    <cic> <tech> <cell> --layer M3
cicpy blockers  <cic> <tech> <cell> --net N --box X1:X2:Y1:Y2
cicpy findroute <cic> <tech> <cell> --net N --start X,Y,L --stop X,Y,L
```
