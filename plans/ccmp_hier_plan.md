# LELOTEMP_CCMP: the last flat cell

Three of this design's four sidecars declare `routes` and build their
declared pieces as cells. `LELOTEMP_CCMP` does not, so its three --
`cmp`, `n_g`, `caps` -- stay groups inside one cell. The pieces are
written as classes either way, so the difference is not in the design
but in what the framework does with it, and the framework's rule
(`routes` present ⇒ made of subcells) is the wrong axis: `routes`
should say how a parent connects its children, not whether they exist.

## What was tried, 2026-08-13

Adding `routes = []` is the whole switch, and the split works:

```
LELOTEMP_CCMP: building LELOTEMP_CCMP_CMP   (1 instances, 8 ports)
LELOTEMP_CCMP: building LELOTEMP_CCMP_N_G   (2 instances, 4 ports)
LELOTEMP_CCMP: building LELOTEMP_CCMP_CAPS  (5 instances, 2 ports)
```

with clean ports on each:

| cell | ports |
|:-----|:------|
| `_CMP` | CMPO M2, IBP_1U<0> M2, IBP_1U<1> M3, PWRUP_B M3, PWRUP_N M3, VC M2, VDD M1, VSS M1 |
| `_N_G` | IBP_1U<0> M2, PWRUP_N M2, RST M2, VSS M1 |
| `_CAPS` | IBP_1U<0> M4, VSS M5 |

The parent's 150 lines of `Rect`/`Cut` reaching into `x1_cmp`, `xg1`,
`xg4` and `xd1<0>` cannot survive that -- none of those instances
belong to this cell any more -- and they do not need to. What crosses
is three nets, and two of them came out shorter said between ports:

* **`IBP_1U<0>`** -- the comparator's input, the reset pull's drain and
  the cap bank's plate, all published within 30 um of the cell's base.
  One `routes` entry: a bar on a channel registered between the ring
  and the cells, drops discovered. **Worked.**
* **`PWRUP_N_1V8`** -- the core's pin at its own row, the pull's gate
  13 um lower. Up to M5 (the one layer that crosses the core touching
  nothing), east, down to M2. **Drew.**
* **the cap bank's `VSS`** -- its plate rail on M5 down to the M1 ring.
  **Drew.**

## Where it stopped

LVS 10 nets against 9. `LELOTEMP_CCMP_N_G`'s two NMOS **sources** are
not on its own VSS rail:

```
Net: VSS                          | Net: VSS
  ...                             |   JNWATR_NCH_2C5F0/S = 2      <- missing
Net: LELOTEMP_CCMP_N_G:xn_g/xg4/S | (no matching net)
```

As a GROUP they were tied by the parent's `addPowerConnection("VSS",
"", "bottom")`, which stretches every published supply rect to the
ring and so reached the devices' own source rails. As a CELL the
subcell has to rail them itself, and the stack does carry
`JNWATR_NCH_2CTAPBOT`/`TAPTOP`. Tried and did not do it:

* `addConnectivityRoute("M1", "^VSS$", "||", "trunkleft"/"trunkright")`
  -- joins one source, not both;
* `addPowerConnection("VSS", "", "bottom")` inside the subcell --
  no change, and it put the count back to 11.

Next thing to try: give the subcell a `supplies` entry rather than a
route, so the recipe straps it at the taps the way every other subcell
in this design is strapped -- `LELOTEMP_OTAR_P_BIAS` and friends all
get their rails that way, and this cell declares `supplies = []` at the
top precisely because the PARENT did not want the recipe's straps. The
subcell is not the parent and does.

## Then the framework

Once this cell converts, `hierarchy()` can run unconditionally and the
`routes`-presence rule goes away: a declared piece is a cell, always,
and `routes` only describes the assembly. Nothing else in the design
depends on the flat path.
