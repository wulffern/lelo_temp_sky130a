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

  load   D: VSS | VIP VIP | VBN1 VBN1 | VO1 | VO VO
         G: VSS | PWRUP_N | RST | PWRUP_N | VBN1 VBN1 | PWRUP_N | VO1
         D is contiguous, G's PWRUP_N is not, and it cannot be: the
         three PWRUP_N gates sit on three different drain nets and
         each of those three has a second pin elsewhere in the column.
         Chose D. PWRUP_N crosses to bias anyway and gets a trunk lane
         of its own, never a rail on the gate pins.
         load0 is the netlist's own VSS dummy and sits at row 0,
         below every pin span, where a supply bar blocks nothing.
         WHICH END each drain net takes is the port plan, and it is
         not free: VIP and VO are the two nets that leave this cell on
         opposite edges, so they take the two ends of the column. VIP
         at rows 1-2 is one row above the bottom edge, which is where
         LELOTEMP_CCMPR's cap bank hangs off it -- CCMP's model puts
         five MiM caps on exactly this node, and phase 3 puts them
         BELOW the comparator. VO at rows 6-7 is under the top edge.
         Their two port risers then leave in OPPOSITE directions from
         the two ends of the drain lane and cannot meet.
         MEASURED, with VIP at the top instead: VIP's bottom-edge
         riser ran M2 y 0..340400 and VO's top-edge riser M2 y
         97000..398000 in the SAME lane (M2 t42..t46, x 117000..129000
         -- the drain lane), and checkroutes merged eight nets. Nothing
         about the routing was wrong; the column was upside down.

  diff   D: VDD x4 | VBN1 | VO1        G: VDD x4 | VIN | VIP
         the four xp_diff3 dummies are all-VDD devices, so they go to
         the bottom for the same reason load0 does, and the live pair
         lands at rows 4-5, level with load's VBN1 (rows 3-4) and VO1
         (row 5). VIP is the one crossing net that travels -- load
         rows 1-2 to diff row 5 -- which is the price of the bottom
         edge, and it is paid in the seam, on a trunk of its own.

  tail   D: VBP2 VBP2 | VO | VS VS VS   G: PWRUP_1V8 | VBP2 x5
         both contiguous. tail1<0> is the gate-odd device and goes to
         the bottom. VS at rows 3-5 faces p_diff's sources at rows
         4-5. VO's tail pin is at row 2 and its load pins at rows 6-7,
         so its branches cross p_diff ABOVE the top tap, where that
         column is empty -- which is why VO's trunk stands in ctail
         and not in the seam.

The branch gap stays 2 um. It is a gap between an nmos row and a pmos
row, where 2 um is the smallest clean value in the spacing table, and
nothing routes ALONG it -- the crossing nets cross it in row channels
and only need it to be legal, not wide. Widening it spends the width
budget on nothing; the routing budget is in y, where the tile has
28 um free.

=====================================================================
WHERE THE ROUTING STANDS -- READ BEFORE TOUCHING _route_signals
=====================================================================

WHAT THIS CELL IS TODAY: placement, two supply rings and the guard
connections. 0 DRC errors, 34.48 x 39.80 um. `_route_signals()` and
`_port_edges()` below are written, are NOT called, and do not verify.
They are kept because the analysis in them cost the measurements
listed here, not because they are ready.

FIXED AND KEPT (these are real, and they verify):

  1. The column order and every stack order, from the netlist. See
     above. This is the part that was actually wrong with the old
     cell.
  2. THE SUPPLIES. The old cell said addPowerConnection, which copies
     the PIN rect and stretches it to the ring on the pin's own layer.
     On REY_ATR, whose pins overhang, that dragged M1 from an upper
     device's source down across the drain and gate of everything
     below it. On the BARE PLACEMENT, with no signal route anywhere,
     checkroutes found two components of 31 rects:
         VBN1,VBP2,VDD_1V8,VIN,VIP,VO,VO1,VS
         IBP_1U,VBN1,VBP2,VIP,VO,VO1,VSS
     -- every signal in the cell shorted to a supply before routing
     began. addPowerGuardConnection + addPowerStrap(terminals=("B",))
     is the REY_ATR answer and it is what is called now.

STILL OPEN, with the last measurement:

     checkroutes  1 short: PWRUP_N_1V8,VBP2,VIP,VO,VO1,VS
     magic        Ports "PWRUP_N_1V8" and "VO" are electrically
                  shorted / and "VIP"
     netgen       18 devices vs 18, 13 nets vs 13, "Top level cell
                  failed pin matching" -- the layout publishes 6 of
                  the 9 ports; VIP, VO and PWRUP_N_1V8 are the three
                  that are merged
     make drc     50 errors (was 63 on the old cell)

WHAT IS ALREADY RULED OUT, so nobody pays for it twice:

  - It is not the trunk lanes. vchannel/vtrack is honoured; M2 track
    maps show the three seam trunks at 167800, 173800 and 179800 as
    asked.
  - It is not the bars either, on their own. Naming ONLY the trunk
    left each bar where its own pins put it, and a bar leaving lane 0
    rightwards runs through the trunks in lanes 1 and 2 (16 measured
    VBN1 x VO1 pairs). Both axes are named now and VBN1 and IBP_1U
    came clean.
  - A via pad is 0.88 um tall and a lane is 0.6, so a row shared by
    two nets does not have six free lanes. VO1 at r5,t4 landed inside
    VBN1's gate pad on xn_mirr_load3, the device that carries both.
  - It is not fixable by putting everything on M2: that build came
    out 13 devices against 18 and 11 nets against 13, far worse.
  - The three M4 flyers are each in a SEPARATE metal3 component (I
    clustered the .mag), so the remaining merge is through M3/M2/M1
    or a via column, NOT on M4.

WHAT I WOULD DO NEXT, in this order:

  1. Ask `blockers` for VIP, VO and PWRUP_N_1V8 over the load column
     -- the merge is a via COLUMN, which is exactly what that tool
     was written for and which no same-layer check can see.
  2. Suspect _port_edges first. PWRUP_N_1V8's left port is drawn
     "-|--" on M4 and lays a horizontal M4 bar the whole width of
     n_mirr_bias at y 61000..64000; VIP's and VO's port risers stand
     in the load drain lane 0.02 um from their own rails, which is a
     met4 spacing error as well. Two of the three merged nets are
     port routes and the third crosses them.
  3. If that does not close it, stop hand-placing lanes and convert
     this cell to a SidecarCell with one Stack per column, the way
     LELOTEMP_OTAR and LELOTEMP_BIAS_IBP are written. The stack-level
     maze router is space-aware and writes its conclusions back as
     `wires`; the flat connectivity router is not, and every failure
     above is a shape it drew without being able to see what was
     already there.
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
    "n_mirr_load": ["xn_mirr_load0", "xg4", "xg1",
                    "xn_mirr_load1", "xn_mirr_load2", "xn_mirr_load3",
                    "xn_mirr_load4", "xn_mirr_load5"],
    "p_diff": ["xp_diff3<0>", "xp_diff3<1>", "xp_diff3<2>",
               "xp_diff3<3>", "xp_diff1", "xp_diff2"],
    "p_mirr_tail": ["xp_mirr_tail1<0>", "xp_mirr_tail1",
                    "xp_mirr_tail3<0>", "xp_mirr_tail3<1>",
                    "xp_mirr_tail3<2>", "xp_mirr_tail2"],
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

    #- ============ the channels, and why they are the numbers =========
    #- A route may not carry a coordinate. Every number below comes off
    #- the placement that just ran, so the cell survives a resize and
    #- another technology; beforeRoute names these and never a y or an
    #- x. addRoutingChannel's own track pitch is width+space, one legal
    #- lane, so consecutive indices are consecutive wires -- there is
    #- no "keep every track even" rule to hand-compensate for.
    #-
    #- One VERTICAL channel per column plus the seam, because a trunk
    #- is what two nets collide on: the router lays one vertical trunk
    #- per net and a horizontal branch per pin, so nets are separated
    #- by giving each trunk its own lane, not by hoping their pins
    #- differ.
    layout.addRoutingChannel("cbias", n_mirr_bias.x1, n_mirr_bias.x2,
                             horizontal=False)
    layout.addRoutingChannel("cload", n_mirr_load.x1, n_mirr_load.x2,
                             horizontal=False)
    layout.addRoutingChannel("seam", n_mirr_load.x2, p_diff.x1,
                             horizontal=False)
    layout.addRoutingChannel("cdiff", p_diff.x1, p_diff.x2,
                             horizontal=False)
    layout.addRoutingChannel("ctail", p_mirr_tail.x1, p_mirr_tail.x2,
                             horizontal=False)

    #- and one HORIZONTAL channel over the nmos top tap row, which is
    #- 2.4 um of cell that carries M1 only. It is the full width of the
    #- cell and above every pmos pin, which is what VBP2 wants: its two
    #- pin clusters are at the BOTTOM of p_mirr_tail and the TOP of
    #- n_mirr_bias, so any bar between them crosses somebody.
    #- and one HORIZONTAL channel per device ROW, taken from the tall
    #- column's own instances so the names mean the same thing on both
    #- sides of the cell. A row is 4 um and a lane is 0.6, so each of
    #- these holds six bars; the route table below spends at most two
    #- of them, which is what "one net per row channel" buys.
    for i, inst in enumerate(n_mirr_load.instances):
        layout.addRoutingChannel(f"r{i}", inst.y1, inst.y2)

    #- plus the nmos top tap row, 2.4 um of full-width cell that
    #- carries M1 only. VBP2 lives there: its pins are at the top of
    #- n_mirr_bias and the bottom of p_mirr_tail, so every bar between
    #- them crosses somebody, and the only band that crosses nobody is
    #- above every pin in the cell.
    toptap = max(n_mirr_load.tap_instances, key=lambda i: i.y1)
    layout.addRoutingChannel("top", toptap.y1, toptap.y2)

    layout._route_scopes = {
        "nmos": nmos,
        "pmos": pmos,
        "n_mirr_bias": n_mirr_bias,
        "n_mirr_load": n_mirr_load,
        "p_mirr_tail": p_mirr_tail,
        "p_diff": p_diff,
    }


def beforeRoute(layout):
    #- Every signal route here is NEW. None of LELOTEMP_CMP's options
    #- were carried over: CMP's track4/track6/track8 were tuned for
    #- JNW_ATR's 2.56 um columns and a bare `track` is an offset from
    #- the net's OWN pins, so on REY_ATR's 8 um columns six nets
    #- (IBP_1U, PWRUP_N_1V8, VBN1, VBP2, VIP, VO1) computed nearly the
    #- same anchor and landed on M3 track t24 together -- 143 met3.2
    #- boxes in one 0.9 um band at x 9.7..10.6. Not one bare `track`
    #- appears below; every net names a channel.
    layout.addRouteRing("M1", "VDD_1V8", "t", widthmult=3, spacemult=2)
    layout.addRouteRing("M1", "VSS", "b", widthmult=3, spacemult=2)

    #- THE SUPPLIES GO TO THE GUARD, not up a strap the width of a pin.
    #- LELOTEMP_CMP could say addPowerConnection because JNW_ATR is a
    #- 2.56 um cell whose pins do not overhang; REY_ATR's do.
    #- addPowerConnection copies the PIN rectangle and stretches it to
    #- the ring on the pin's own layer, so an upper device's source
    #- drags M1 down across the drain and gate of everything below it.
    #- Measured on the bare placement, with not one signal route in the
    #- cell: checkroutes reported two components of 31 rects each,
    #-   VBN1,VBP2,VDD_1V8,VIN,VIP,VO,VO1,VS   and
    #-   IBP_1U,VBN1,VBP2,VIP,VO,VO1,VSS
    #- i.e. every signal in the cell shorted to a supply before any
    #- routing existed. Chasing that in the router would have been
    #- chasing the wrong file.
    #-
    #- REY_ATR rings each device in its own tap, so the real connection
    #- is a jog from each source to the guard column beside it, and the
    #- tap cells already tie the guard up, down and across. That is
    #- addPowerGuardConnection. addPowerStrap then carries only the
    #- BULK terminal out to the ring, one routing width wide rather
    #- than one pin wide, with the via down on the pin.
    for net, side in (("VDD_1V8", "top"), ("VSS", "bottom")):
        layout.addPowerGuardConnection(net)
        layout.addPowerStrap(net, "", side, terminals=("B",))

    #- VBP2 first, and differently from everything else. Its pins are
    #- at the TOP of n_mirr_bias (rows 2-5) and the BOTTOM of
    #- p_mirr_tail (rows 0-1 on D, 1-5 on G), at opposite ends of the
    #- cell in both axes, so no trunk-and-branch shape reaches both
    #- without crossing a row that belongs to somebody else. It gets a
    #- full width bar in the "top" channel instead -- the nmos tap row,
    #- which carries M1 only -- and M4 drops from every pin. M4 is the
    #- point: the drop from p_mirr_tail's row 0/1 drains passes rows
    #- 2-5 of that same column, which are VO's and VS's drains, and
    #- those are on M2. Two layers, no crossing.
    #- ---------------------------------------------------------------
    #- STOPS HERE. Everything below is _route_signals(), which is
    #- WRITTEN AND NOT CALLED. See "WHERE THE ROUTING STANDS" in the
    #- docstring: the signal routing does not verify yet, and a cell
    #- that half-routes is worse than one that does not, because the
    #- next reader cannot tell which half to trust. The placement, the
    #- rings and the guard connections above DO verify -- 0 DRC -- and
    #- that is what this cell is.
    return


def _route_signals(layout):
    """The signal routing. NOT CALLED -- see the docstring."""
    #- MEASURED, and the reason this is not one route: the pair
    #-     addChannelRoute("M3", "VBP2", "top", track=1)
    #-     addRouteConnection("^VBP2$", "", "M4", "top", "")
    #- put a drop on EVERY VBP2 access rect -- fourteen routes, each
    #- "||,onTopB,fillvcut" -- and fillvcut stacks cuts through the
    #- whole access. connectivity reported one component of 4136 rects
    #- holding all twelve nets INCLUDING VDD_1V8 and VSS, attributed to
    #- that call. The supplies must reach the guard/tap rows, not be
    #- crossed by a via stack on the way to a bar.
    #-
    #- So VBP2 is TWO trunks, one per group, and a bridge between them.
    conn0 = layout.addOrthogonalConnectivityRoute
    conn0("M2", "M3", "^VBP2$", "vchannel=cbias,vtrack=4,hchannel=top,htrack=1",
          2, "", r"^xn_mirr_bias2")
    conn0("M2", "M3", "^VBP2$", "vchannel=ctail,vtrack=6,hchannel=top,htrack=1",
          2, "", r"^xp_mirr_tail")

    #- The rest: one vertical trunk and one horizontal branch per pin,
    #- with the trunk lane stated per net. Read the lane table as a
    #- floorplan of the routing, because that is what it is.
    #-
    #-   net           trunk lane      what it joins
    #-   ------------- --------------- -------------------------------
    #-   IBP_1U        cbias  10       bias-local, rows 0-5
    #-   PWRUP_N_1V8   cload   1       bias row 0 -> load rows 1,5,6
    #-   VO1           seam    0       load rows 2,3 -> diff row 5
    #-   VBN1          seam    1       load rows 3,4,5 -> diff row 4
    #-   VIP           seam    2       load rows 6,7 -> diff row 5
    #-   VO            ctail   2       load rows 6,7 -> tail row 2
    #-   VS            ctail   9       diff rows 4,5 -> tail rows 3-5
    #-
    #- The seam is 2 um and holds exactly three lanes, which is what
    #- decides who gets one: VBN1, VO1 and VIP are the three nets whose
    #- two ends are in n_mirr_load and p_diff, the two columns the seam
    #- separates. VO is not one of them -- it reaches past p_diff to
    #- p_mirr_tail, and it does so at rows 6-7 where p_diff is empty
    #- above its top tap, so its trunk stands in ctail beside the pin
    #- it has to reach. PWRUP_N_1V8 never reaches p_diff at all.
    #-
    #- PWRUP_N_1V8 is the one net that gets a lane of its own INSIDE a
    #- column rather than a rail on the pins. Its three load gates are
    #- at rows 1, 5 and 6 with VO1's and VBN1's gates at rows 2, 3, 4
    #- between them, and that interleaving cannot be ordered away: the
    #- three PWRUP_N gates sit on three different drain nets and each
    #- of those has a second pin elsewhere in the column, so drain
    #- contiguity and gate contiguity are mutually exclusive here. The
    #- column is ordered on D and PWRUP_N_1V8 flies past on a trunk
    #- that is not the gate lane, touching down only at rows 1, 5, 6.
    #- WHICH VERTICAL LAYER, and why it is not all M2. A trunk lane
    #- separates two nets that both stand in the channel; it does not
    #- separate a net's rail from another net's PIN, and a rail is not
    #- optional -- a net with several pins on one terminal of one
    #- column gets a vertical down that terminal's lane whatever the
    #- trunk says. Three such rails cross a foreign pin here, and all
    #- three were measured on M2 (tracks --layer M2):
    #-
    #-   PWRUP_N_1V8[98600..307400] x VBN1[218600..267400]  @135000
    #-        load's gate lane: PWRUP_N's gates are rows 1,3,6 and
    #-        VBN1's are rows 4,5, between them
    #-   VS[201300..244700]         x VBN1[217300..220700]  @222000
    #-        p_diff: the LVT cell's source and drain lanes are 0.6 um
    #-        apart, so VS's source rail and VBN1's drain stub meet
    #-   VBP2[54600..267400]        x VO[137300..140700]    @304000
    #-        p_mirr_tail: VBP2 has a pin on every row 0-5, so its rail
    #-        spans the column and VO's row-2 drain is inside it
    #-
    #- None of the three is fixable by moving a trunk, because the
    #- rail is on the pins. They go up a layer instead. M4 is free --
    #- REY_ATR cells hold M1 and nothing above it, so M2, M3 and M4 are
    #- empty over the whole cell -- and the three flyers land in
    #- disjoint x: PWRUP_N_1V8 is nmos-only, VS is pmos-only, and VO's
    #- nmos pins are on the drain lane, 3 um from PWRUP_N's gate lane.
    #- BOTH AXES, ALWAYS. Naming only the trunk was not enough and the
    #- measurement says why: with VO1, VBN1 and VIP on seam lanes 0, 1
    #- and 2, each net's bar still landed where its own pins put it,
    #- and a bar reaching RIGHT out of lane 0 runs straight through the
    #- trunks in lanes 1 and 2. checkroutes found the pattern 16 times
    #- for VBN1 x VO1 alone -- e.g. VBN1's M3 trunk pad
    #- (167800,254600)-(171200,263400) with VO1's M3 bar
    #- (140900,261500)-(173800,264500) laid across it. A shared channel
    #- separates trunks from each other; it does not separate a trunk
    #- from a BAR that has to cross the channel to reach the far side.
    #-
    #- So every net names an hchannel as well, and the two indices
    #- together make each crossing a single point of one M2-over-M3.
    #-
    #-   net           bar            trunk         vert
    #-   ------------- -------------- ------------- ----
    #-   IBP_1U        r1  t2         cbias 10      M2
    #-   VIP           r5  t0         seam  2       M4
    #-   VBN1          r4  t1         seam  1       M2
    #-   VO1           r5  t4         seam  0       M2
    #-   VO            r6  t2         ctail 2       M4
    #-   VS            r4  t5         ctail 9       M4
    #-   PWRUP_N_1V8   r3  t2         cload 1       M4
    #-   VBP2          top t1         cbias 4 /     M2
    #-                                ctail 6
    #-
    #- r5 carries two bars and r4 two, at indices four lanes apart --
    #- 2.4 um, four times the met3 pitch. They are pairs whose x spans
    #- overlap (VIP/VO1 and VBN1/VS), which is exactly when the index
    #- has to be said rather than left to the pins.
    conn = layout.addOrthogonalConnectivityRoute
    conn("M2", "M3", "^IBP_1U$", "vchannel=cbias,vtrack=10,hchannel=r1,htrack=2", 2, "", "")
    conn("M2", "M3", "^VBN1$", "vchannel=seam,vtrack=1,hchannel=r4,htrack=1", 2, "", "")
    #- VO1's bar is in r6 and not in r5 with its own drain, because r5
    #- is xn_mirr_load3 and that device carries BOTH VO1 (drain) and
    #- VBN1 (gate). The gate via pad is 0.88 um tall and swallows lanes
    #- 3 and 4 of the row: at r5,t4 VO1's pad (137500,261600)-(140900,
    #- 270400) sat inside VBN1's (137500,258600)-(140900,267400). A
    #- via pad is taller than a lane, so a row shared by two nets is
    #- not six free lanes, it is however many the pads leave.
    conn("M2", "M3", "^VO1$", "vchannel=seam,vtrack=0,hchannel=r6,htrack=0", 2, "", "")
    conn("M4", "M3", "^VIP$", "vchannel=seam,vtrack=2,hchannel=r5,htrack=0", 2, "", "")
    conn("M4", "M3", "^PWRUP_N_1V8$", "vchannel=cload,vtrack=1,hchannel=r3,htrack=2", 2, "", "")
    conn("M4", "M3", "^VO$", "vchannel=ctail,vtrack=2,hchannel=r6,htrack=4", 2, "", "")
    conn("M4", "M3", "^VS$", "vchannel=ctail,vtrack=9,hchannel=r4,htrack=5", 2, "", "")


def _port_edges(layout):
    """The edge ports. NOT CALLED -- they need _route_signals()."""
    #- Port edges follow the column order, which changed: IBP_1U and
    #- PWRUP_N_1V8 are on the left because n_mirr_bias is now the left
    #- column and both have a pin in it; PWRUP_1V8 stays on the right
    #- with p_mirr_tail.
    #-
    #- VIP down and VO up is the pair the stack order was built for --
    #- each is one row from its edge and they leave in opposite
    #- directions, so the drain lane carries both risers without them
    #- ever meeting.
    #- A PORT LEAVES ON THE LAYER ITS NET IS ROUTED ON. addPortOnEdge
    #- draws a bare run from the port rect to the edge on the layer it
    #- is given, and it adds no via to whatever the net is actually
    #- built from: VIP, VO and PWRUP_N_1V8 all have M4 trunks, and
    #- asking for M2 gave each of them a riser lying beside its own net
    #- and touching nothing --
    #-     VIP  M2 (121300,2000)-(124300,139000)   over M4 at 124900
    #-     VO   M2 (121300,299000)-(124300,396000) over M4 at 124900
    #- and netgen said so exactly: 18 devices and 13 nets on both
    #- sides, "Top level cell failed pin matching", with VIP, VO and
    #- PWRUP_N_1V8 the three the layout had no pin for.
    layout.addPortOnEdge("M4", "VIP", "bottom", "||", "")
    layout.addPortOnEdge("M4", "VO", "top", "||", "")
    layout.addPortOnEdge("M3", "IBP_1U", "left", "|-", "track0")
    layout.addPortOnEdge("M4", "PWRUP_N_1V8", "left", "-|--", "track2")
    layout.addPortOnEdge("M2", "VIN", "bottom", "||", "")
    layout.addPortOnEdge("M3", "PWRUP_1V8", "right", "-|", "offset_track0")
    #- RST gets NO edge. Its one pin is xg1's gate at row 2 of
    #- n_mirr_load, in the middle of the cell in both axes: the left
    #- edge means crossing n_mirr_bias on M3 at a row IBP_1U's own
    #- branch already owns, and the bottom means running down the gate
    #- lane past xg4's PWRUP_N gate and load0's. A port does not have
    #- to be on an edge -- LELO_TEMP already anchors its seam stories
    #- on PWRUP_N_1V8 and PWRUP_B_1V8 where the core publishes them,
    #- mid-row -- so RST is published where it is and LELOTEMP_CCMPR
    #- reaches it.
