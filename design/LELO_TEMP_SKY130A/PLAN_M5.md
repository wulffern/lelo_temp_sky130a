
# Plan: nothing INSIDE the tile on M5

*2026-08-16. Written against `feat/cmpr-lvt-comparator` at the commit
where `make checkall` first came back green on all five cells. Every
number below is measured off that build, not remembered.*

## The goal, restated by a measurement

"Remove M5" cannot mean the tile stops touching magic met4:
`tt_block_1x1_pg.def` places every TinyTapeout pin as `+ LAYER met4`,
so the tile's own interface pads (OSC_TEMP_1V8, PWRUP_1V8, and the
supplies) are met4 by contract. cicpy M5 *is* magic met4.

So the goal is: **M5 exists only as the tile-edge port pads the DEF
demands, each fed from below by an M4 story. No wire, riser, crossing
or block port uses M5 anywhere inside.**

Why it is worth doing: M5 is the tile's interface layer. Every
internal M5 wire is metal the INTEGRATOR has to route around when the
tile is placed; a tile that is empty on met4 inside can be crossed
freely above.

## What uses M5 today (the full census)

Measured from the built `.cic` (`grep M5` counts 73 mentions in
`LELO_TEMP.py` alone; the geometry inventory is smaller):

**Stories drawing M5 at the top (8 nets):**

| net | why it is on M5 |
|---|---|
| `PWRUP_N_1V8` | lband riser + cband crossing: lband's M4 is owned by the four IBP legs, cband's M3+M4 by RST_A |
| `CMPO_B` | cband crossing: RST_A owns the M3 row and the M4 turn it would need |
| `IBP_1U<0..3>` | four lband risers (the `_ibp` phase) |
| `CMPO_A`, `RST_A`, `RST_B` | only the final `up` onto the strip's M5 ports — forced by the ports, not chosen |

**Ports published on M5 (13):**

* `xdig`: 7 — `_promote`/`_portRise` lift chosen ports to M5 pads
  ("M5 IS THE ONE LAYER THESE CELLS DO NOT USE" — true inside the
  strip, and the reason its neighbours all pay an M5 landing).
* `xbias`: 6 — `IBP_1U<0..3>`, `PWRUP_N_1V8`, `PWRUP_B_1V8` edge pads.

**Inside the strip:** the ladder's `_m5Lane`/`_crossLayer` machinery
sends an input stub over the rails on M5 when its lane allows
(`return "M5" if (m5ok and pin.x1 < 25000) else "M3"`).

**Not involved:** `VC`, `VSS`, `VBP2`-class column nets, `PWRUP_B`
(already M2/M3/M4), all four subcell interiors below the strip.

## The dependency that orders everything

The landings (`CMPO_A/B`, `RST_A/B` ending `up M5`) are *consequences*
of dig's ports. The bias-side risers are *consequences* of bias's
ports plus lband congestion. So ports move first, stories follow —
the same bottom-up rule as the wires conversion. And every phase ends
with the same gate: `checkroutes` shorts=0 opens=0, `make drc`,
`kdrc`, `lvs` unique, one net at a time via `paths_only`.

## Phase 0 — measure the headroom (no edits)

For each corridor the stories will need on M4, ask before moving
anything:

    blockers <net> over the exact span      # per corridor
    tracks --layer M4 --band <lo:hi> --free <span>

Corridors to measure: cband (full width), lband (full height), the
strip's three `exit` columns, sband, and the east margin (proven free
during RST_B). Record the free lanes in the plan file. **Expected
finding:** cband has no free M4 track crossing RST_A's descent —
that is what phase 3 re-plans.

## Phase 1 — dig's ports M5 → M4 (the biggest single win)

* `_promote`: publish the lifted pads on M4 (cicpy met3) instead of
  M5. The pads sit above cells that own only M1 and their M4 supply
  columns — cicpy-M4 is free at every promoted pad site *except where
  a crossing story already runs*; phase 0's map says where.
* `_m5Lane`/`_crossLayer`: cap the ladder's stub layer at M4; the
  "over the rails" case becomes M4-with-jogs or a re-booked row.
* Every landing story (`CMPO_A/B`, `RST_A/B`, `PWRUP_N` leg 2) drops
  its final `("up","M5")` — the diffs are one line each, and `end()`
  does the rest.
* **Trap already known:** an M2–M5 cut carries a 10.8 µm M4 pad; the
  M2–M4 cut's pad is smaller. Re-measure the two pad-squeeze sites
  (RST_A/RST_B rows, 800 units apart; the PWRUP_N pad at the strip)
  — they get *easier* on M4, but verify, don't assume.

## Phase 2 — bias's six ports off M5

Find the producer (the `LELO_TEMP_BIAS` build lifts edge pads; the
same `_EDGE_PORTS`-style code that CCMPR uses). Publish on M3, which
is what the pair already does — its lifted pads are M3 and every
story lands on them without ceremony.

* `PWRUP_B_1V8` needs nothing else: its story already descends
  M5→M4→M3 *at the pin*; with an M3 pad the two `down` steps vanish.
* `PWRUP_N_1V8` and `IBP_1U<0..3>` depend on phase 3.

## Phase 3 — the lband/cband re-plan (the real work)

The only phase with design freedom, and the reason M5 got used at all.

**lband** (50 µm ≈ 8 lanes): the four IBP legs cross it horizontally
on M4 at four rows, so any full-height M4 riser crosses all four.
Options, cheapest first:
1. IBP legs one layer down (M3) for the crossing leg only — lband's
   M3 is empty above y 524000 (VC ends there). Then M4 risers are
   free for PWRUP_N + the four IBP verticals themselves.
2. Keep IBP on M4 and weave PWRUP_N: M4 riser with an M3 jog at each
   of the four rows. Four jogs, eight vias — legal but ugly, and
   every added IBP tap breaks it.
3. Move the IBP risers into the pair's interior (`pband` proved 54 µm
   of free M2 there) — radical, but empties lband entirely.

Option 1 is the recommendation: one layer digit per leg, anchors
unchanged.

**cband**: RST_A's M3 run (cband 0→8) plus its M4 descent at dband 2
block both cheap layers for CMPO_B. Options:
1. RST_A turns onto M4 at its *own* pin column (drop the M3 run east
   to dband 2), freeing the whole M3 row set — then CMPO_B crosses on
   M3 and nothing needs M5.
2. CMPO_B descends *west* of RST_A's column and crosses under cband in
   the pair's interior (pband again).

Option 1 first — it is one story edit and it un-blocks the band for
any future net.

## Phase 4 — the tile-edge pads

`OSC_TEMP_1V8`, `PWRUP_1V8` (+ supplies) keep an M5 pad exactly at the
DEF's pin position, fed by an M4 story from below. This is the *only*
M5 left, and it is the DEF's, not ours.

## Tooling that makes this cheaper

The path emitter (`routeplan.path_suggestion`, on `feat/net-rules`)
turns any searched route into a paste-ready anchored `paths` entry.
After each port migration, a throwaway `mazes` entry with
`layers=("M2","M3","M4")` is a cheap scout: the search finds a legal
M5-free shape against the *current* metal, and the suggestion lands in
`.routes.py` ready to paste and gate. That is how each re-planned
story should be drafted before it is reasoned about.

## Order and cost estimate

    0. headroom map            half a session, no risk
    1. dig ports -> M4         one session; 5 stories lose one step
    2. bias ports -> M3        short, once phase 3's plan exists
    3. lband/cband re-plan     the real design work, one session
    4. tile-edge pads          short, closes the goal

Do not start phase 1 until phase 0's cband/lband numbers are written
down: the whole plan turns on whether option 1 of each re-plan holds,
and that is a measurement, not an opinion.
