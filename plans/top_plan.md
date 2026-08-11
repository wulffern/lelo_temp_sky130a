# LELO_TEMP top level, what is left

The whole sensor is placed and routed into a TinyTapeout 1x1 tile.
This is the state and the remaining work.

## State, 2026-08-11

- **placement**: 156.18 x 111.50 um of content in the 161.00 x 111.52
  um tile. Bias left, the two comparators stacked in the middle
  column, the oscillator logic in a strip on the right with its
  tapcell at the base.
- **routing**: 0 collisions from the build-time report, every
  block-to-block net connecting.
- **LVS**: 30/30 devices; one line left, and it is not routing (below).
- **DRC**: 93 (from 238 when the routing first closed).

Blocks below it are finished: `LELOTEMP_BIAS_IBP` and `LELOTEMP_CCMP`
both LVS "Circuits match uniquely", CCMP DRC clean, BIAS 8 slivers.

## The one LVS line

```
Net: x1_ibp/LPO                | Net: LPI
  BIAS_IBP/xota/VR1 = 1        |            (no matching net)
```

Magic's hierarchical extraction promotes the OTA's `VR1` label to a
twelfth port on the bias block, and the top schematic has nothing to
tie it to. It appears with **zero top-level paint present**, so it is a
`LELOTEMP_BIAS_IBP` sidecar question, not a routing one: either stop
the OTA exposing `VR1` at the block boundary, or expose it as a real
port and carry it in the schematic.

Standalone, `LELOTEMP_BIAS_IBP` extracts 11 ports and matches. Only the
deeper walk the top does promotes the twelfth.

## The 93 DRC

No single change clears a block of them any more.

| Count | Rule | Where |
|------:|:-----|:------|
| 141 | met4.2  | 50 gap/top, 39 bias, 34 ccmp, 18 strip |
| 77  | met3.2  | 60 gap/top, 17 strip |
| 48  | met2.2  | strip |
| 40  | met1.2  | 30 strip, 10 bias |
| 15  | met4.5b | bias, ccmp |
| 12  | mcon.2  | bias |
| 10  | li abut/overlap between subcells | bias (pre-existing, the OTA pad) |
| 9   | met4.5a | bias |
| 4   | via2.2 / via3.2 | bias, ccmp |

(box counts; magic's own total is 93 rule instances)

The gap/top and strip entries are this file's own lanes and want
individual attention — mostly 3 um spacing where a long neighbour
makes it large metal and 4 um is required. The bias and ccmp entries
are inside finished blocks and were there before integration.

## Optional: make the logic strip a block

The top places seven logic cells and a tapcell directly, so every one
of their li pins is reached individually from the top. A `DIG` block
would collapse that to a handful of edge pins, contain the tapcell, and
verify on its own.

It would not have solved the routing — the strip-column scheme did that
— and it needs a new xschem subcircuit. Cleanup, not a prerequisite.

## Loop

```bash
cd work
RT=all make mag CELL=LELO_TEMP        # ROUTE SHORT lines name any collision
make gds cdl lvs CELL=LELO_TEMP
make drc CELL=LELO_TEMP
```

`RT=<sections>` builds a subset of the signal routes (`lpi`, `vc`,
`ibp`, `pwrn`, `pwrb`, `cmpoa`, `cmpob`, `rstb`, `rsta`, `nets`,
`misc`) and `NT=<letters>` drops individual supply ties, so any subset
can be bisected in one build. Read the LVS `Final result:` line only —
"match uniquely with port errors" is a failure that greps as success.

## Traps this cost

Written up in [LAYOUT_FLOW.md](../LAYOUT_FLOW.md) under "Integrating
Blocks At The Top". The short version: `addPowerConnection` slices
through the block it came from, `addRouteRing` does not see
physical-only instances, ring attachments belong in `beforePaint`, the
standard-cell strip is free above M1 but its Y-pin column is the AVSS
via stack, and a riser must own the highest lane in its band.
