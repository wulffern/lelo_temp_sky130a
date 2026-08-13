# LELOTEMP_CCMP: the last flat cell -- DONE

`LELOTEMP_CCMP` was the one sidecar in this design that declared no
`routes`, so its three pieces -- `cmp`, `n_g`, `caps` -- stayed groups
inside one cell while every other cell's pieces were built as cells.
It is converted:

```
LELOTEMP_CCMP: building LELOTEMP_CCMP_CMP   (1 instances, 8 ports)
LELOTEMP_CCMP: building LELOTEMP_CCMP_N_G   (2 instances, 4 ports)
LELOTEMP_CCMP: building LELOTEMP_CCMP_CAPS  (5 instances, 2 ports)
```

| cell | LVS | DRC |
|:-----|:----|:----|
| `LELOTEMP_CCMP_CMP` / `_N_G` / `_CAPS` | match uniquely | OK |
| `LELOTEMP_CCMP` | match uniquely | OK |
| `LELO_TEMP_CCMP` (the pair) | match uniquely | OK |
| `LELO_TEMP` | pending, see [top_plan](top_plan.md) | OK |

The parent's 150 lines of `Rect`/`Cut` reaching into `x1_cmp`, `xg1`,
`xg4` and `xd1<0>` are gone -- none of those instances belong to this
cell any more. What crosses is three nets, and each is either a
`routes` entry or a story.

## What it took

**The subcells needed their own rails.** As groups they were tied by
the parent's `addPowerConnection`, which stretches every published
supply rect to the ring; as cells they are strapped where they are. A
`supplies` entry WITHOUT `ring` does exactly that and nothing at the
parent, which is the split this cell wants -- it lays its rings by
hand and its pieces want their own straps.

**The cap bank is approached from the west.** A MiM claims 1.34 um
from unrelated metal3 (capm.11) and counts anything under its halo, so
the `IBP_1U<0>` channel bar running the cell's width picked up the
whole bank. The bank's drop is skipped and told as a story instead,
turning in a `capgap` channel registered between the pull and the
bank.

**The cap bank's VSS needs no story at all.** Its plate rail is a
published supply rect and `addPowerConnection` already stretches it to
the ring; a second stack at the same x put four via layers 2400 from
the first (via.2, via2.2, via3.2 and nine mcon.2).

**PWRUP_N leaves its pin on cuts turned on their side.** A pin is 3200
wide and the default cut 8800, so a stack centred on it reaches 4800
west -- into the core's own M4 riser 5200 away, and met3.2 wants 3000.
`options="1cuts,2vcuts"` fits the same two cuts inside the pin. Moving
the transition east instead worked for this cell and cost the pair
above it its riser lane, which is why the narrow cut is the answer and
not the detour.

## What the conversion broke above it, and why

The pair `LELO_TEMP_CCMP` is assembled by LELO_TEMP's `ccmp` subcell,
never built alone -- `make mag CELL=LELO_TEMP_CCMP` silently replaces
it with an unrouted copy. Build `LELOTEMP_CCMP` first, then
`LELO_TEMP`; nothing in between.

Two things in the framework only ever worked for cells whose geometry
starts at their origin, and this cell's VSS ring hangs 24000 below it:

* **`Instance.setAngle` folded MX by `y1 + y2`** where MY folds by
  `x2`. The same number for an origin-based cell; for this one the
  mirrored copy landed 24000 low, ate the 20000 seam gap the placer
  had left and overlapped the lower comparator by 4000 -- VDD, VSS and
  CMPO_B shorted.
* **the fold is applied to the children too**, and a maglib cell's
  children were normalised at load (`libshift`). So the fold about the
  raw box is off by the cell's own `y1` for them: the upper
  comparator's pins read 24000 low, and the two seam nets landed short
  of pins that were painted somewhere else. `_foldForChildren()` now
  says which frame it is folding in.

And one thing in this design's own measurement: `_emptyColumn` found
the pair's crossing column by asking the comparator for its rects.
Made of cells, the comparator does not have them -- the wall it
measures, the cap bank's tall M4/M5, belongs to a subcell. It asks
`flatMetal()` now, and takes the RIGHTMOST tall column rather than the
leftmost, because through the view the core's own risers are visible
too and the leftmost of those named a 6500 band in the middle of the
core.

## Then the framework

`hierarchy()` can now run unconditionally and the `routes`-presence
rule can go: a declared piece is a cell, always, and `routes` only
describes the assembly. Nothing in this design depends on the flat
path any more.
