---
layout: page
title: Layout Flow
---

# Layout Flow

The layout in this repository is schematic driven: the schematic is
drawn in `xschem`, the layout is written by `cicpy`, and `magic`,
`klayout` and `netgen` check it.

The flow itself is documented with the tool that implements it, so it
is written once and stays current:

**→ [Layout with cicpy, a field guide](https://analogicus.com/cicpy/agent_layout.html)**

That guide covers the sidecar (`design/<LIB>/<CELL>.py` *is* the
cell), the routing loop — search → emit an anchored story → import it
into the sidecar → DRC/KDRC/LVS/ANT → next net — and the rule that
holds all of it together: **a design file never carries a
coordinate**; every wire is anchored to a pin, a channel track or a
band that is recomputed from the placement on every build.

The reference cells for the guide live in this repository:
`design/LELO_TEMP_SKY130A/LELOTEMP_CMPR.py` (a fully declared cell)
and `design/LELO_TEMP_SKY130A/LELO_TEMP.py` (a top of stories).

Build and verify from `work/`:

```bash
make mag  CELL=<CELL>
make drc  CELL=<CELL>
make gds kdrc CELL=<CELL>
make cdl lvs  CELL=<CELL>
make ant  CELL=<CELL>
```
