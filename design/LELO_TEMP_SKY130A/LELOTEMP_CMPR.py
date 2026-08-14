"""LELOTEMP_CMPR: the REY_ATR comparator, with the reset switches in.

Same topology as LELOTEMP_CMP, three things different:

  - every device is a REY_ATR cell, so every column is 8.000 x 4.000
    whatever its contact count (expand_row pads the rest with empty
    columns, which is what makes the taps one shape);
  - the input pair is REYATR_LVT_PCH_8C5F0, because a standard pfet
    needs |Vsg| = 0.983 V at 2 uA at -40 C and VC peaks at 0.845 V
    there -- VS would have to sit above the supply;
  - xg1 (RST) and xg4 (powerdown) pull VIP down from inside this
    cell, so CCMPR is only the cap bank and this.

FOUR COLUMNS, NOT FIVE. A REY_ATR column is 8 um against JNW_ATR's
2.56, and the tile gives the ccmp block 41 um of width and 28 um of
unused height (LELO_TEMP.mag: xccmp 20200..28396 in a 21892 tile).
Five columns is 40 um plus the branch gap and does not fit, so the
switch pair goes INTO a stack as a fillGroup -- spending the height
that is free instead of the width that is not.

  five columns                       40.64 x 36.20   too wide
  xg abutted on top of n_mirr_load   38.08 x 45.80   two extra taps
  xg as n_mirr_load's fillGroup      38.08 x 41.00


=====================================================================
WHY THE COLUMNS SIT IN THIS ORDER
=====================================================================

Read from `netlist_info work/xsch/LELOTEMP_CMPR.spice LELOTEMP_CMPR`.
Only five nets have pins in more than one column; everything else is
column local and needs no lane at all:

    net     from            to              what it is
    ------- --------------- --------------- --------------------------
    VBN1    load1,2,3       diff1           the mirrored branch
    VO1     load3,5         diff2           the other branch
    VO      load4,5         tail2           the output
    VBP2    bias2<0..3>     tail1,1<0>,3<*> the pmos bias
    VIP     xg1, xg4        diff2           the input + its two pulls

The column order is what decides how far each of those has to travel,
and it is the only thing that decides it -- a route cannot make a
20 um span short. Weighting each net by the number of columns it
spans, with the nmos group necessarily left of the pmos group:

    load+xg | bias || diff | tail   = 11    <- what this cell had
    bias | load+xg || diff | tail   =  8    <- what it has now
    load+xg | bias || tail | diff   = 12
    bias | load+xg || tail | diff   =  9

VIP is the measurable one. It used to run 10.54 -> 25.05 um, nearly
the whole cell, because xg rode in the FAR column from p_diff; with
load+xg next to the seam its two ends are in adjacent columns. bias
loses nothing by going to the outside: its own net IBP_1U is column
local and its port is on that same left edge, and its one crossing
net VBP2 has a top ring rather than a lane.

The switches stay a fillGroup of n_mirr_load (not of n_mirr_bias):
they belong to the column that touches p_diff, and that is load's
job here because load owns VBN1 and VO1, the other two nets that
cross the seam. xg is ONE group and not two because the group name
is the leading letters of the instance name -- xg_rst and xg_pdn
would have been two groups of one.

=====================================================================
WHY THE STACKS SIT IN THIS ORDER
=====================================================================

`stackorder` reports every column but p_mirr_tail and p_diff
interleaved on D. A drain rail down a column crosses every pin it
passes, so an interleaved column cannot have one -- and that is
placement's business, not routing's. Each `order` below groups the
column on D, because D carries the signal; where D and G disagree the
gate net loses and is given a row channel instead.

  bias   D: IBP_1U IBP_1U | VBP2 x4        G: PWRUP_N | IBP_1U x5
         both contiguous. bias3 is the one device whose gate is not
         IBP_1U, so it goes to the BOTTOM and the tab lane spans the
         rows above it.

  load   D: VSS | VO VO | VO1 | VBN1 VBN1 | VIP VIP
         G: VSS | PWRUP_N | VO1 | VBN1 VBN1 | PWRUP_N PWRUP_N | RST
         D is contiguous, G's PWRUP_N is not, and it cannot be: the
         three PWRUP_N gates sit on three different drain nets and
         each of those three has a second pin elsewhere in the column.
         Chose D. PWRUP_N crosses to bias anyway and is a row-channel
         net, never a rail.
         VO lands at rows 1-2 deliberately -- it is the one net that
         has to cross OVER p_diff to reach p_mirr_tail, and rows 1-2
         of p_diff are dummies, so it crosses quiet rows.
         VIP lands at rows 6-7 against p_diff's row 5 gate, one row.
         load0 is the netlist's own VSS dummy and sits at row 0,
         below every pin span, where a supply bar blocks nothing.

  diff   D: VDD x4 | VBN1 | VO1        G: VDD x4 | VIN | VIP
         the four xp_diff3 dummies are all-VDD devices, so they go to
         the bottom for the same reason load0 does, and the live pair
         ends up beside load's VBN1/VO1/VIP rows.

  tail   D: VBP2 VBP2 | VO | VS VS VS   G: PWRUP_1V8 | VBP2 x5
         both contiguous. tail1<0> is the gate-odd device and goes to
         the bottom. VO lands at row 2, level with load's rows 1-2.

The branch gap stays 2 um. It is a gap between an nmos row and a pmos
row, where 2 um is the smallest clean value in the spacing table, and
nothing routes ALONG it -- the crossing nets cross it in row channels
and only need it to be legal, not wide. Widening it spends the width
budget on nothing; the routing budget is in y, where the tile has
28 um free.
"""

data = {
    "afterPaint": [
        {"resetOrigins": [[1]]},
    ]
}


#- bottom-to-top, one list per column. Named instances first, anything
#- the netlist grows later falls through to the end rather than
#- raising -- a new device should not break the build, only the order.
ORDER = {
    "n_mirr_bias": ["xn_mirr_bias3", "xn_mirr_bias1",
                    "xn_mirr_bias2<0>", "xn_mirr_bias2<1>",
                    "xn_mirr_bias2<2>", "xn_mirr_bias2<3>"],
    "n_mirr_load": ["xn_mirr_load0", "xn_mirr_load4", "xn_mirr_load5",
                    "xn_mirr_load3", "xn_mirr_load2", "xn_mirr_load1",
                    "xg4", "xg1"],
    "p_diff": ["xp_diff3<0>", "xp_diff3<1>", "xp_diff3<2>",
               "xp_diff3<3>", "xp_diff1", "xp_diff2"],
    "p_mirr_tail": ["xp_mirr_tail1<0>", "xp_mirr_tail1", "xp_mirr_tail2",
                    "xp_mirr_tail3<0>", "xp_mirr_tail3<1>",
                    "xp_mirr_tail3<2>"],
}


def _order(stack):
    """Put a stack's devices in ORDER[stack.name] and repack it.

    orderByTerminalNet() would do the grouping, but it groups on ONE
    terminal and takes the net order from first appearance; the lists
    above also say which end each net sits at, which is what makes VO
    cross p_diff's dummy rows and not its live pair.
    """
    names = ORDER[stack.name]
    by = {i.instanceName: i for i in stack.instances}
    ordered = [by[n] for n in names if n in by]
    rest = [i for i in stack.instances if i.instanceName not in set(names)]
    if rest:
        stack.log.warning(
            f"_order: {stack.name} has devices not in ORDER: "
            + ", ".join(i.instanceName for i in rest))
    stack.instances = ordered + rest
    stack.preserve_order = True
    stack.stack()
    return stack


def beforePlace(layout):
    layout.noPowerRoute = True
    layout.place_xspace = [0]
    layout.place_yspace = [0]
    layout.place_groupbreak = [5]


def afterPlace(layout):
    branch_gap = 2 * layout.um

    nmos = layout.makeCellGroup("nmos")
    n_mirr_bias = nmos.addStackByGroup("xn_mirr_bias", name="n_mirr_bias")
    #- REQUIRED after merging two groups into one column: the first
    #- pass dropped xg at x=0 and n_mirr_load at x=160000, and a stack
    #- keeps the positions it was given until it is packed. _order()
    #- does the packing.
    n_mirr_load = nmos.addStackByGroup("xn_mirr_load", name="n_mirr_load",
                                       fillGroup="xg")

    pmos = layout.makeCellGroup("pmos")
    p_diff = pmos.addStackByGroup("xp_diff", name="p_diff")
    p_mirr_tail = pmos.addStackByGroup("xp_mirr_tail", name="p_mirr_tail")

    for s in (n_mirr_bias, n_mirr_load, p_diff, p_mirr_tail):
        _order(s)

    #- column order, left to right, is stated here and nowhere else:
    #- bias | load+xg || diff | tail. The stacks keep whatever x the
    #- first pass gave them until they are abutted.
    n_mirr_load.abutRight(n_mirr_bias)
    p_mirr_tail.abutRight(p_diff)

    #- NO fillDummyTransistors HERE, deliberately. bias is 6 devices
    #- against load's 8 and the corner above it stays empty. This
    #- netlist names its OWN dummies -- xn_mirr_load0 and xp_diff3<*>
    #- are schematic devices with every terminal on a supply -- so a
    #- layout-generated xfill_* has no counterpart to match against.
    #- Measured: the two fills a height match produced took the layout
    #- to 36 devices against the schematic's 26 and LVS reported a
    #- device mismatch. If those rows are ever wanted for matching,
    #- they have to be added to LELOTEMP_CMPR.sch first.
    for s in (n_mirr_bias, n_mirr_load, p_diff, p_mirr_tail):
        s.addTaps()

    nmos.updateBoundingRect()
    pmos.abutRight(nmos, space=branch_gap)

    pmos.updateBoundingRect()
    nmos.updateBoundingRect()
    nmos.routeDummyDevices()
    pmos.routeDummyDevices()

    layout._route_scopes = {
        "nmos": nmos,
        "pmos": pmos,
        "n_mirr_bias": n_mirr_bias,
        "n_mirr_load": n_mirr_load,
        "p_mirr_tail": p_mirr_tail,
        "p_diff": p_diff,
    }


def beforeRoute(layout):
    #- PHASE 1: supply rings only. Every signal route was deleted
    #- rather than carried over from LELOTEMP_CMP -- CMP's track
    #- numbers were tuned for JNW_ATR's 2.56 um columns and a track is
    #- an offset from the net's OWN pins, so on 8 um columns six nets
    #- landed on M3 track t24 together (143 met3.2 boxes in one band).
    layout.addRouteRing("M1", "VDD_1V8", "t", widthmult=3, spacemult=2)
    layout.addRouteRing("M1", "VSS", "b", widthmult=3, spacemult=2)
    layout.addPowerConnection("VDD_1V8", "", "top")
    layout.addPowerConnection("VSS", "", "bottom")
