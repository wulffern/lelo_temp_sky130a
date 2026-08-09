# LELOTEMP_OTAR, what is left

`LELOTEMP_OTAR` is `LELOTEMP_OTA` on the REY_ATR_SKY130A transistors. Same
netlist: same instances, same nets, same connectivity, same device sizes.
It exists because the OTA could not be finished on the JNWATR cells —
`VD3` has pins in both rows and three columns, and on those cells the only
way across a column landed on another net's access pads.

## State, 2026-08-06

- placement: 0 shorts, 0 DRC
- power: rings on M1, sources tied to their own guard, one strap per
  column off the body pin out to the ring
- routed: the five ladder nets, plus VIN, VIP, VS, VD1, VD2, net1,
  PWRUP_1V8
- **0 shorts, 6 opens, 36 DRC** (met2.2 and met3.2 between bars)

Open: `VD3 VBP VCP VO PWRUP_N_1V8`, plus VDD at `xbs6` (see below).

### What each of the seven cost

Free, no DRC change: VIN and VIP (all pins inside one input column each,
one vertical), net1 (two pins), PWRUP_1V8 (three gates in the bias
column).

VS wanted the two column verticals *and* one orthogonal M4/M3 across the
channel; the verticals alone left three components.

VD1 and VD2 are the expensive pair: they close, and DRC goes 4 -> 36.
Four track and side combinations tried, two shorted, none beat 36.
Splitting them into per column verticals plus a channel bar, the shape
that worked for VS, gives 4 shorts and 112 errors, because the vertical
in the input column runs the stack's length and meets VBP.

### The four that were tried and taken back out

- **VO** reaches from the bias column to the mirror drain below. On every
  track and side tried its trunk lands on VIN's in the input column:
  shorts VD2, VIN, VO.
- **PWRUP_N_1V8** is one gate in bias, three along the nmos row. A
  horizontal along that row shorts to VD2 and VSS, a vertical shorts too.
  It needs the row bar to dodge VD2's channel crossing, which is a
  placement question.
- **VCP** is every ladder gate plus the mirror column. A vertical down the
  switch column runs the ladder's own length and merges net2..net6 with
  VCP and VDD.
- The pattern in all three: a net whose pins span columns cannot take a
  trunk through a column that already carries another net's trunk. The
  channel is the only free crossing and it now has six bars in it.

## The three that need a decision, not just more routing

**`xbs6` has no power connection.** It is the one VDD source in the ladder
column and its jog to the guard crosses VCP: 1 short with it in, 0 with it
excluded. `addPowerGuardConnection` picks the *nearest* guard, and nearest
is not safe on its own — the jog has to be told which pins it may not
cross, or be clipped at the pin edge instead of run to the centre. Fixing
that in cicpy removes the `excludeInstances` here.

**No matched-pair mirroring.** `LELOTEMP_OTA` mirrors the left half of
each pair, and it can because JNWATR carries S left of centre and D right,
so the halves meet source against source. REYATR overlaps S (x 324..1404)
and D (468..1548) with G at the right edge, so a mirrored device maps D
onto where S was: 11 placement shorts with the two mirror calls, 0
without. The pair symmetry has to come from somewhere else — a common
centroid arrangement, or a cell that puts its pins where mirroring works.

**4 met3.2 between M3 bars.** Not chased. The related single error in
`REYNORES` is a via pad hanging off its trunk, and these may share a
cause; see the note in that pycell before treating it as placement.

## What is known to work, and is worth reusing

- signals on **M4 vertical, M3 horizontal**. M1 is the pins' own layer
  (cicpy M1 is magic locali) and M2 is left for power.
- two nets whose pins share rows need their trunks sent in **opposite
  directions**, `left` against the default right. With both on the same
  side the outer net's bar crosses the inner net's trunk and lands on its
  via pad. No track, cut or branchtrack value avoids it.
- a net landing on a **drain and the gate beside it** — any diode
  connection here — wants `branchtrack` to collapse its branches into one
  bar. Two bars 20 units apart is met2.2, and the gap enclosed between
  them is met2.7.
- the ladder is five separate nets in one column: one regex for all of
  them puts every trunk in the same place. One route each, own track.

## Route rings, 2026-08-06

Rings are the answer for a net whose pins span columns when the channel
is full: it goes around instead of through. They work here. Three things
had to be right first, and two of them were wrong the first time.

**`addRouteConnection` needs its instance filters.** Called with an empty
`includeInstances` it gives *every* pin on the net its own run to the
rail, dummy fill included, and a net whose groups sit at one end of the
row then has runs crossing the whole cell. `LELOTEMP_START` gets this
right and is the model:

```python
layout.addRouteRing("M2", "VCP", "l", widthmult=1, spacemult=4)
layout.addRouteConnection("VCP", "xn_vp3", "M3", "left", "",
                          excludeInstances="^xfill_")
```

**The rail belongs on the side the pins are already on.** VCP's groups
end at the right of both rows, so a left rail meant crossing the cell;
a right rail is short runs.

**`ignoreBoundaryRouting` has to be set,** or the ring joins the cell's
bounding box and drags it: measured 0..460.7 um before, 500.9..976.8 um
after adding the ring. That flag turned out to be broken in cicpy, the
predicate skipped instances instead of routing, and setting it emptied
the box outright. Fixed in cicpy 6ba5ccc; with it the box stays
0..474.2 um and the ring sits outside the edge.

State with the VCP ring in: **0 shorts, 6 opens, 36 DRC**, and VCP down
from eleven components to nine.

What is left on VCP is the ladder column. Its own five nets own M3 and
M4 there, so a run from a ladder gate out to the rail crosses them
whichever track it takes. Layers tried for that run: M3 and M4 short
against net4, M5 shorts and costs 130 DRC, M2 shorts. Moving the ladder
itself from M4 to M2 does not help either, it just moves the collision.
The ladder gates need either their own rail on the column's own side, or
the ladder's tracks re-planned to leave a corridor.

## A router, started 2026-08-06

`cicpy addTrackRoute(net)` is a first attempt at searching for a
corridor instead of naming one. cicpy b18c750. It is not used by any
design yet.

It borrows magic's `mzrouter` cost model: per layer hcost and vcost per
unit distance, per contact cost, Manhattan estimate, A*. The house
convention becomes a price rather than a rule, so a route can break it
where it must. It does not borrow magic's windowed search or tile plane
geometry; a coarse grid at the ROUTE pitch is enough here.

What it can do: read the drawn geometry as obstacles, search, and
validate the result before drawing. Pointed at VO it drew a short first
time; once the checks were right it declined to draw anything and left
the cell at its clean baseline, which is the behaviour to keep.

What it cannot do yet: reach every pin. A cut is a cell, not a point,
and its enclosure on the layer being left is taller than a 4 um pin, so
insisting the enclosure clear every neighbouring pin left two of three
VO pins with no legal exit at all. Checking only the layer being entered
finds a path but is optimistic about the layer being left. Pin access in
a dense field is the thing to solve next, and it is the same problem the
hand routes hit from the other side.

Also worth knowing before touching this: magic's own routers are in the
binary but not usable here. `iroute` says "Need irouter style in
mzrouter section of technology file", and sky130A ships `mzrouter` and
`router` as empty stubs, at lines 4152 and 6196 of sky130A.tech. Turning
them on is a tech file authoring job, layer set and via costs and
spacing, not a switch.

## A trap worth knowing

`addOrthogonalConnectivityRoute` takes `excludeInstances` and
`includeInstances` positionally on `layout`, and omitting them raises
TypeError inside `beforeRoute`. sch2mag then exits *without* printing a
connectivity report, so a check that counts OPEN warnings sees none and
reads it as success. Check that the report exists, never that warnings
are absent.

## Loop

```bash
cd work
cicpy sch2mag LELO_TEMP_SKY130A LELOTEMP_OTAR --check-connectivity
make drc CELL=LELOTEMP_OTAR
cicpy svg ../design/LELO_TEMP_SKY130A/LELOTEMP_OTAR.cic ../tech/cic/sky130A.tech \
    LELOTEMP_OTAR --I ../../rey_atr_sky130a/design/REY_ATR_SKY130A.cic
```

Add one route, check, keep it or change it. Do not add a second on top of
a short.

---

**STATUS 2026-08-09: DONE.** LELOTEMP_OTAR is DRC OK and LVS
"Circuits match uniquely" — the top and all eight subcells, each
verified standalone. The method that finished it is not the flat flow
this plan describes but the sidecar flow: `LELOTEMP_OTAR.yaml` holds
subcells/rows/supplies/hier, `make subcells CELL=LELOTEMP_OTAR` then
`make hier CELL=LELOTEMP_OTAR` builds everything, and the only python
left is the p_sw ladder's stack pycell. The current method is
documented in cicpy `docs/agent_layout.md` ("The sidecar flow").
Verify with `make drc` / `make gds cdl lvs` and read the LVS
`Final result:` line only — "match uniquely with port errors" is a
failure that greps as success.
