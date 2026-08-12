# LELO_TEMP top level, what is left

The sensor is three blocks in a TinyTapeout 1x1 tile. All three
verify on their own; nothing joins them yet.

## State, 2026-08-13

| cell | LVS | DRC | what it is |
|:-----|:----|----:|:-----------|
| `LELO_TEMP_BIAS` | Circuits match uniquely | 8 | `LELOTEMP_BIAS_IBP` and its LPI loop |
| `LELO_TEMP_CCMP` | Circuits match uniquely | 0 | both comparators, mirrored about their seam |
| `LELO_TEMP_DIG` | Circuits match uniquely | 16 | the oscillator's logic strip |
| `LELO_TEMP` | **Netlists do not match** — 39 layout nets against 24 | — | the three, placed and unrouted |

The 39-against-24 is not a defect to hunt: the top declares
`routes = []`, so every block-to-block net exists as one fragment per
block. That is the work below.

**This file used to describe a flat top with 778 lines of hand
routing, 93 DRC and "one LVS line left".** None of it survived the
subcell conversion (`970c23e`), and the numbers in it were measured
against a netlist that was itself wrong — the generated subcell
schematics wired bus pins by the symbol's name rather than the nets
they hang on, so LVS was comparing against `IBP_1U[1:0]` on both
comparators. Fixed in cicpy `26a159f`.

## The floorplan, as placed

```
        x 0            960000  1010000        1419800   1459800  1605200
  y 1064600  +-----------------+                                          tile 161.00 x 111.52 um
             |                 |        (empty)              (empty)       cell 160.52 x 109.46
             |   xbias         |
             |   96 x 106.5    +---------------+
    768000   |                 |   xccmp       |
             |                 |   41 x 76.8   |
    189700   |                 |               |          +--------+
             |                 |               |          | xdig   |
         0   +-----------------+---------------+----------+ 14.5x19+
                               ^               ^          ^
                          lband 5 um      dband 4 um
```

Two vertical gaps (5 um and 4 um) and a large free area above `xccmp`
and `xdig` — 30 um over the comparators, 87 um over the strip. There
is room; what there is not is a plan.

## The nets

Every one of these is a fragment per block today.

| net | from | to |
|:----|:-----|:---|
| `IBP_1U<0>` `<1>` `<2>` `<3>` | bias | ccmp |
| `VC` | bias (`VD1`) | ccmp |
| `PWRUP_N_1V8` | bias | ccmp, dig |
| `PWRUP_B_1V8` | bias (`PWRUP_1V8`) | ccmp, dig |
| `CMPO_A` `CMPO_B` | ccmp | dig |
| `RST_A` `RST_B` | dig | ccmp |
| `VDD_1V8` `VSS` | the rings | all three |
| `PWRUP_1V8` `OSC_TEMP_1V8` | dig | the tile's own pins |

Ports, as published (`cell_info`):

* **bias** `IBP_1U<0..3>`, `PWRUP_B_1V8`, `PWRUP_N_1V8`, `VC`,
  `VDD_1V8` (M1, top edge), `VSS` (M1, bottom edge)
* **ccmp** the same signal set plus `CMPO_A/B`, `RST_A/B`; `VDD_1V8`
  is a full width M1 bar mid cell, `VSS` a full width M1 bar at the
  bottom edge
* **dig** `CMPO_A/B`, `OSC_TEMP_1V8`, `PWRUP_1V8`, `PWRUP_B/N`,
  `RST_A/B` all on M1 pads; `VDD_1V8` and `VSS` are M4 columns

## The mechanism is already there

`SidecarCell` routes an assembly from `routes`: each entry lays one
`ChannelRoute` on a named channel track and **discovers** its drops —
every placed subcell whose ports expose the net gets one, and the
`drops:` list only overrides layer/align/cuts for the columns that
need it. That is exactly the shape of this problem.

```python
    channel = 8
    routes = [
        {"net": "IBP_1U<0>", "track": 6, "drops": [[bias, "M2", "right"],
                                                   [ccmp, "M2", "left"]]},
    ]
```

So the work is to declare the channels the floorplan opens and one
route per net, then iterate. Three things to fix on the way in:

1. **`afterPlace` registers its channels off `x2_ccmp` and `x3_ccmp`**,
   which are inside `LELO_TEMP_CCMP` now and not instances of this
   cell. The whole `addRoutingChannel` block is guarded by
   `if None not in (...)` and so registers *nothing* today. `lband`,
   `dband` and the bands above the blocks have to come off `xbias`,
   `xccmp`, `xdig`.
2. **The same block has a latent `NameError`**: `ca` is used before it
   is defined, reached only when the `dig` group is found. It is not
   found today, which is the only reason the build runs.
3. **`beforePaint` returns immediately**, so no block is tied to a
   ring. The rings themselves are laid correctly, on an explicit rect
   over all three instances (`addRouteRingOnRect`) — the bias block's
   own edge bars meet them, and `xccmp`/`xdig` do not.

## What the blocks taught, and applies here

* **Ask `tracks` before choosing a lane, and `blockers` before
  dropping a via column.** Every routing failure in `LELO_TEMP_CCMP`
  was a via column landing on another net's pin, and none of them
  showed up as a same-layer conflict.
* **A pin is 3200 wide and the default cut is 8800.** `1cuts,2vcuts`
  turns the same two cuts on their side and they fit.
* **A lane's pad is 8800 wide**, so two lanes want 12000 between them
  unless their nets' y spans are disjoint.
* **`checkroutes` names nets by whichever level it reached**, so a
  child's `PWRUP_1V8` bonded to the parent's `PWRUP_B_1V8` reads as a
  short. Only components attributed to a route (`routes=X[ ~ ]`) are
  worth chasing; LVS is the authority.

## The one thing that cannot be checked before the GDS

`LELO_TEMP_DIG`'s 16 remaining DRC errors are all in its two pin
columns, and they are not a routing mistake so much as a blind spot:

**a JNWTR standard cell publishes only M1, M4 and POB.** Its two
M1-M4 cut stacks — which carry M2 and M3 pads at every rail — live
inside a `use JNWTR_cut_M1M4_2x1`, and the magic reader does not
expand it. A cell that places standard cells therefore cannot see the
M2 or M3 it must avoid, and `tracks`, `blockers` and `checkroutes`
all report those columns as free. The GDS is the first thing that
knows.

Two ways out, neither tried yet:

* teach the reader to expand a `use` into the parent's obstacle set,
  which fixes it for every design at once; or
* keep M2 and M3 out of the supply columns entirely — outputs leave
  their pin eastward on M2 at their own row and via up only past the
  column edge. That costs the middle lane (an M2-M5 cut's M4 pad is
  10800 wide and does not fit between the two bars), which is the one
  the strip cannot spare.

## Loop

```bash
cd work
make mag CELL=LELO_TEMP              # builds all three subcells and the top
make gds cdl lvs CELL=LELO_TEMP      # gds FIRST or the extraction is stale
make drc CELL=LELO_TEMP
```

Read the LVS verdict from the **`Final result:`** line and nowhere
else — netgen prints "match uniquely with port errors" on failing
runs.
