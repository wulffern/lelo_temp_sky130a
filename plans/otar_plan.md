# LELOTEMP_OTAR, what is left

`LELOTEMP_OTAR` is `LELOTEMP_OTA` on the REY_ATR_SKY130A transistors. Same
netlist: same instances, same nets, same connectivity, same device sizes.
It exists because the OTA could not be finished on the JNWATR cells —
`VD3` has pins in both rows and three columns, and on those cells the only
way across a column landed on another net's access pads.

## State, 2026-08-05

- placement: 0 shorts, 0 DRC
- power: rings on M1, sources tied to their own guard, one strap per
  column off the body pin out to the ring
- routed: the five ladder nets, each on its own track, alternating sides
- **0 shorts, 13 opens, 4 met3.2 errors** between M3 bars

Open: `VD1 VD2 VD3 VBP VO VCP VS net1 PWRUP_1V8 PWRUP_N_1V8 VIN VIP`, plus
VDD at `xbs6` (see below).

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
