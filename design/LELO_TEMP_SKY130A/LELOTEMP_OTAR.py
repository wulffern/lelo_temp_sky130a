import re

data = {
    "afterPaint": [
        {"resetOrigins": [[1]]},
    ]
}

#- Placement only. Routing waits until the placement is DRC clean, but the
#- arrangement is chosen with the routing in mind: the input halves sit
#- next to the nmos loads they drive, the powerdown devices at the outer
#- edge where the PWRUP wiring will arrive, and the degeneration resistor
#- in the notch next to the bias stack it feeds.
#-
#- The two ten device groups are folded into pairs of five device columns
#- so the rows come out even and the cell approaches a square:
#-   xbl  input pair and CM sense   -> two interleaved halves, one from
#-        each bus so both columns carry both inputs
#-   xnd  matched loads             -> VD1 side and VD2 side columns,
#-        each diode with its own mirror output
#- Groups hold one device width each, see the netlist.


def _pick(insts, patterns):
    out = []
    for i in insts:
        name = getattr(i, "instanceName", "")
        if any(re.fullmatch(p, name) for p in patterns):
            out.append(i)
    return out


def beforePlace(layout):
    layout.noPowerRoute = True
    layout.place_xspace = [0]
    layout.place_yspace = [0]
    layout.place_groupbreak = [6]


def afterPlace(layout):
    branch_gap = 2 * layout.um
    #- the gap between the two rows is the routing channel, and it is the
    #- only place a net may cross the cell. Seven nets have pins in both
    #- rows, so the channel is opened to six micron: each of them gets its
    #- own horizontal band and the bands have to clear each other
    channel = 6 * layout.um

    xbl = layout.getSortedInstancesByGroupName("xbl")
    xnd = layout.getSortedInstancesByGroupName("xnd")

    pmos = layout.makeCellGroup("pmos")
    #- one input side per column: VD1 stays in the a lane, VD2 in the b
    #- lane, so each drain net runs one vertical corridor to its loads
    #- the common mode sense device of each half goes to the bottom of its
    #- column, next to the routing channel. Its drain VD3 is the one net
    #- that has to cross the whole cell, and a net can only cross in the
    #- channel: a vertical drop through a column lands on the M2 access
    #- pads another net's route already put on the pins in that column
    #- bus widths come from the schematic, so match any index rather
    #- than a range. The input pair has been 4 and is now 6 a side, and
    #- a hard coded <[0-3]> silently dropped the devices past it into no
    #- stack at all -- they still place, just nowhere anyone asked
    p_in_a = pmos.addStack("p_in_a", _pick(xbl, [r"xbl4"]) + _pick(xbl, [r"xbl1<\d+>"]), preserveOrder=True)
    p_in_b = pmos.addStack("p_in_b", _pick(xbl, [r"xbl5"]) + _pick(xbl, [r"xbl2<\d+>"]), preserveOrder=True)
    p_bias = pmos.addStackByGroup("xba", name="p_bias")
    #- the ladder is a series chain, stacked in chain order so every link
    #- is between neighbours and no junction has to travel the column.
    #- The chain runs VDD end at the top, VCP end at the bottom: the only
    #- ladder device with a VDD source pin is xbs6, and addPowerConnection
    #- straps such a pin straight up to the ring. From the bottom of the
    #- column that strap crossed the source pin of every other ladder
    #- device and shorted net2..net6 to VDD. At the top it is one cell long
    xbs = layout.getSortedInstancesByGroupName("xbs")
    chain = []
    for nm in ("xbs8", "xbs7", "xbs4", "xbs2", "xbs1", "xbs6"):
        chain += _pick(xbs, [nm])
    p_sw = pmos.addStack("p_sw", chain, preserveOrder=True)

    xns = layout.getSortedInstancesByGroupName("xns")
    xnc = layout.getSortedInstancesByGroupName("xnc")

    nmos = layout.makeCellGroup("nmos")
    #- each powerdown pull lives in the column of the net it pulls, so no
    #- net has to cross the row to reach its switch
    n_load_a = nmos.addStack("n_load_a", _pick(xnd, [r"xnd1<\d+>", r"xnd3"]) + _pick(xns, [r"xns1"]), preserveOrder=True)
    n_load_b = nmos.addStack("n_load_b", _pick(xnd, [r"xnd2<\d+>", r"xnd4"]) + _pick(xns, [r"xns2"]), preserveOrder=True)
    n_mirr = nmos.addStack("n_mirr", xnc + _pick(xns, [r"xns4"]), preserveOrder=True)

    res = layout.makeCellGroup("res")
    r_deg = res.addStackByGroup("xd", name="r_deg")

    #- pack every column. The split stacks inherit interleaved first pass
    #- positions from their source groups, so without this each column has
    #- holes where the other half's devices used to sit
    for s in (p_in_a, p_in_b, p_bias, p_sw, n_load_a, n_load_b, n_mirr):
        s.stack()
    #- Flush. No ygap, and that is the RPPO2 frame paying off.
    #-
    #- RPPO4 needed one: its ring came from addGuard, which insets its
    #- M1 0.08 from the box, so two stacked cells left their rings 0.16
    #- apart -- under the 0.17 li.3 minimum, twice per seam -- and the
    #- fix was to overlap them by exactly one wall (ygap=-144*50) so
    #- the two rings coincided. REYATR_RPPO2 is built from the device's
    #- own bulk section instead, so its ring reaches the box edge and
    #- overhangs it the way a device column's does. Two of them abut
    #- and merge with no help: measured on REYATR_RESABUTR, 0 DRC and
    #- 0 shorts stacked flush, and B comes out one component.
    r_deg.stack()
    #- Cap the resistor column ONCE, the way a transistor stack is
    #- capped. The rows carry only their side walls, so the taps belong
    #- to the column, not to every row -- six framed tiles paid 4.800 of
    #- tap six times over and put 55% of the stack's height into tap.
    #- addTaps resolves RES_36CTAPBOT/TOP from the row's name.
    r_deg.addTaps()

    #- Order the columns for the rails, before anything measures them.
    #- A rail down a column crosses every pin it passes, so a net whose
    #- pins are interleaved with another's cannot have one, and that is
    #- placement's to fix: n_load_a came out VD1 VD1 VD1 VD1 VBP VD1,
    #- and moving one device to the end of the column is the difference
    #- between a rail and a trip up to M2 and back for five pins.
    #-
    #- p_sw is not in the list and must not be. It is the series ladder,
    #- where the order is what makes each link a neighbour of the next,
    #- and every device in it carries a different net on its drain
    #- anyway, so there is no rail to win.
    for st in (p_bias, n_load_a, n_load_b, n_mirr):
        st.orderByTerminalNet("D")

    #- No mirroring. LELOTEMP_OTA mirrors the left half of each matched
    #- pair, and the reason it can is a JNWATR property: those cells carry
    #- S left of centre and D right, so a mirrored half meets its partner
    #- source against source. REYATR lays its pins out differently, S at
    #- x 324..1404 and D at 468..1548, overlapping in x with G out at the
    #- right edge and B on the left, so mirroring maps D onto where S was
    #- and every device in the column shorts its own drain to the source
    #- rail. Measured: 11 placement shorts with the two mirror calls, 0
    #- without. Matched-pair symmetry has to come from somewhere else here.

    #- fill the short columns with dummies of their own device so every
    #- column in a row reaches the height of the tallest, and the taps
    #- land above the dummies
    pmos.fillDummyTransistors()
    nmos.fillDummyTransistors()

    p_in_a.addTaps()
    p_in_b.addTaps()
    p_bias.addTaps()
    p_sw.addTaps()
    n_load_a.addTaps()
    n_load_b.addTaps()
    n_mirr.addTaps()

    #- rows of four columns each. The pmos stacks abut so the wells merge,
    #- any small gap leaves two wells inside the nwell spacing minimum
    p_in_b.abutRight(p_in_a)
    p_bias.abutRight(p_in_b)
    p_sw.abutRight(p_bias)

    #- every nmos boundary gets the full branch gap. Abutted edges violate
    #- the 0.17 um licon spacing between neighbouring diffusion contacts,
    #- and intermediate gaps of 0.3 to 1.5 um trip other tap and diffusion
    #- rules, 2 um is the smallest spacing found clean
    n_load_b.abutRight(n_load_a)
    n_mirr.abutRight(n_load_b)

    pmos.updateBoundingRect()
    nmos.updateBoundingRect()
    res.updateBoundingRect()

    #- pmos row above nmos row
    pmos.abutTop(nmos, space=channel)

    #- The resistor gets a column of its own, right of both rows.
    #-
    #- It used to sit in the notch beside the mirror stack, which worked
    #- while it was one cell. The schematic now asks for three RPPO4 in
    #- series and the stack is 48 um tall against an nmos row of 24.8, so
    #- the top one climbed out of the row and landed inside the bias
    #- column: measured, x 217600 spanning y up to 495000 against a pmos
    #- row starting at 323000. Every rpm.3, rpm.6 and rpm.7 in the cell
    #- came from that one overlap, and DRC went from clean to 111.
    #-
    #- The notch beside the mirror is 10.5 um wide and 30.8 tall, so it
    #- cannot take this column at any orientation: 11.2 will not fit in
    #- 10.5, and three stacked will not fit in 30.8. Right of everything
    #- costs width, and that is the honest price of tripling the
    #- resistor rather than something placement can arrange away
    #- Flush against the transistors, no branch_gap. The old resistor
    #- needed one: its ring came from addGuard, which insets its M1 from
    #- the box, so it could only ever stand NEXT to a device column. The
    #- horizontal row is built from the device's own bulk section and
    #- overhangs its box by 0.480 a side, exactly as a device column
    #- does, so the two rings interpenetrate and merge -- the resistor
    #- column abuts the pmos the same way two device columns abut.
    #- against the NMOS, not the pmos. The column is translated to the
    #- nmos row, so the pmos is not what it has a seam with -- abutting
    #- the pmos left its ring 7.040 from the nearest nmos guard, a gap
    #- dressed up as an abutment. Right of the nmos row the two rings
    #- are at the same y and merge.
    r_deg.abutRight(nmos)
    r_deg.translate(0, nmos.y1 - r_deg.y1)

    pmos.updateBoundingRect()
    nmos.updateBoundingRect()
    res.updateBoundingRect()
    nmos.routeDummyDevices()
    pmos.routeDummyDevices()

    #- The gap between the rows is the only place a net may cross, and
    #- the placement is what decides where it is. Name it here, in the
    #- units this technology produced, so routes can aim at it by track
    #- index instead of carrying coordinates that a resize would break
    layout.addRoutingChannel("mid", nmos.y2, pmos.y1)
    #- and the columns, as vertical channels, so a trunk can be given a
    #- track inside one without naming a coordinate
    for nm, st in (("in_a", p_in_a), ("in_b", p_in_b),
                   ("bias", p_bias), ("sw", p_sw)):
        layout.addRoutingChannel(nm, st.x1, st.x2, horizontal=False)
    #- the resistor column too. The links between stacked resistors are
    #- two nets in one column, so track<n> cannot separate them -- it
    #- counts from each net's own pins and both land on the same lane.
    #- A named channel is absolute and can.
    layout.addRoutingChannel("res", r_deg.x1, r_deg.x2, horizontal=False)

    layout._route_scopes = {
        "res": res,
        "pmos": pmos,
        "nmos": nmos,
        "p_in_a": p_in_a,
        "p_in_b": p_in_b,
        "p_bias": p_bias,
        "p_sw": p_sw,
        "n_load_a": n_load_a,
        "n_load_b": n_load_b,
        "n_mirr": n_mirr,
    }


def beforeRoute(layout):
    #- Power never travels. Every REYATR device is ringed by its own tap,
    #- and a device whose source is the supply has that source sitting a
    #- micron from the guard column beside it on the same layer, so the
    #- supply reaches it at its own row. The guard is already continuous
    #- through the stack and tied side to side by the tap cells; one strap
    #- per column off the body pin carries it out to the ring, running up
    #- inside the guard where it crosses nothing. Rings go on M1, which is
    #- where these pins are, and M2 upward is left entirely to signals.
    #-
    #- This replaces a strap per source pin. That version worked but had to
    #- be nursed: REYATR's S and D pins overlap in x, so a rail leaving a
    #- source ran over its own device's drain, and net2 shorted to VDD
    #- under every routing option until the VDD strap was pushed to the far
    #- edge of the pin. A supply that does not travel cannot do that.
    layout.addRouteRing("M1", "VDD_1V8", "t", widthmult=3, spacemult=2)
    layout.addRouteRing("M1", "VSS", "b", widthmult=3, spacemult=2)
    #- xbs6 is held out. It is the one VDD source in the ladder column, and
    #- its jog to the guard crosses VCP: measured, 1 short with it in and 0
    #- without. The rule "nearest guard" is not safe on its own, the jog has
    #- to be told which pins it may not cross. Leaves VDD open at xbs6.
    layout.addPowerGuardConnection("VDD_1V8", excludeInstances="^xbs6$")
    layout.addPowerGuardConnection("VSS")
    layout.addPowerStrap("VDD_1V8", "", "top", terminals=("B",))
    #- Only the bottom resistor is strapped to the ring. RPPO4 puts B as
    #- a full width strip along the bottom of its guard and P and N near
    #- the top, so a strap from an upper resistor's B down to the rail
    #- runs the length of the column straight across the terminals of
    #- every resistor below it -- and since a strap on the pin's own
    #- layer takes the port's full width, it covers both pads. Measured:
    #- R1<0>, R1<1> and VS all shorted to VSS. The rings touch each
    #- other, so one strap at the bottom carries the whole column
    layout.addPowerStrap("VSS", "", "bottom", terminals=("B",),
                         excludeInstances=r"^xd2<[1-9]")

    s = layout._route_scopes

    #- ---------------------------------------------------------------
    #- Signal routing: torn up, and being rebuilt from the bottom layer
    #- upward. What went before was every net on M3/M4 from the start,
    #- which put the crossing nets and the column local ones in the same
    #- two layers and left the cell at one short and six opens with a
    #- guess costing a regeneration each.
    #-
    #- The order now is the order of reach:
    #-   inside one device   -> the cell does it. REYATR carries a diode
    #-                          connected twin tied with one column of
    #-                          M1, and cicpy substitutes it when the
    #-                          netlist puts one net on D and G
    #-   inside one column   -> M1 rails, edge picked per terminal
    #-   between columns     -> M2
    #-   across the cell     -> M3 horizontal, M4 vertical, aimed at a
    #-                          named channel
    #-
    #- Nothing below this line yet beyond the column rails. Each net
    #- goes back one at a time, checked before the next.
    #- ---------------------------------------------------------------

    #- Column rails on M1, one terminal at a time, each on its own edge
    #- of the pin. REYATR's source rail covers pattern columns 10..16 and
    #- its drain run 12..18, so they share five columns: a rail taking
    #- the full pin width for both would short them. The drain takes the
    #- right edge, the gate the left, and each is one routing width, so
    #- the part of the pin the other needs is left alone.
    for name in ("p_in_a", "p_in_b", "p_bias", "p_sw",
                 "n_load_a", "n_load_b", "n_mirr"):
        s[name].routeMirror("M1", terminals=("D",), align="right")

    #- and the gates, on the other edge. The gate tab sits at the far
    #- right of the pattern, past the drain run, so the two rails are two
    #- pattern columns apart and clear each other. Where a diode cell
    #- tied D to G they are the same net anyway.
    #-
    #- The columns were ordered for the drain, so several are now
    #- interleaved on the gate and decline; that is the trade the order
    #- buys and the refusals name it. Two do not care: the ladder's gates
    #- are all VCP and the mirror's are all VD3, so those close here and
    #- need nothing above M1 at all.
    for name in ("p_in_a", "p_in_b", "p_bias", "p_sw",
                 "n_load_a", "n_load_b", "n_mirr"):
        s[name].routeMirror("M1", terminals=("G",), align="left")

    #- M2, for what is inside one column but could not be a rail. The
    #- ladder links are two pins each, the drain of one device and the
    #- source of the device stacked on it, and the chain order put those
    #- next to each other -- so each is a stub, not a run.
    #- The ladder is left for last, on purpose. Each of net2..net6 is
    #- the drain of one device and the source of the device stacked on
    #- it, so the two pins are a few microns apart -- and unreachable
    #- directly, because the source rail of the device in between sits
    #- across the only columns they share. The link has to go out to a
    #- spine and back, five times, in one column.
    #-
    #- Measured, giving each net its own lane of the column's channel:
    #-   vtrack i    5 spines land clear, the M3 via pads at their ends
    #-               overlap corner to corner        2 shorts, DRC 4
    #-   vtrack 3i   1 short, DRC 8
    #-   vtrack 4i   1 short, DRC 10
    #- Spreading the lanes moves the collision without removing it: the
    #- pads are 8800 across and the bars grow as the spine moves away,
    #- so each step trades a pad clash for a bar clash. This wants the
    #- pad footprint accounted for, not another guess at a track number.

    #- three gates in the bias column, one vertical, no crossing
    s["p_bias"].addConnectivityRoute("M2", "^PWRUP_1V8$", "||", "", 1)

    #- R1<0> and R1<1>, the links between the stacked resistors, are
    #- NOT the easy pair they look like. Both pins of a link sit near
    #- the TOP of their own guard -- RPPO4 puts P and N there and B as
    #- a full width strip at the bottom -- so the link from the P of
    #- one tile to the N of the tile above it has to travel the whole
    #- height of the upper tile and passes that tile's own P on the
    #- way. A plain vertical in the column therefore lands on it:
    #- measured, one component holding R1<0>, R1<1> and VDS.
    #-
    #- Two things were ruled out on the way and should not be retried:
    #-   one regex for both      `^R1<\d+>$` puts both nets on one lane.
    #-                           track<n> counts from each net's OWN
    #-                           pins, so two nets in a column compute
    #-                           the same lane and neither can tell.
    #-   a named lane each       vchannel=res,vtrack=2 and 6 resolve
    #-                           correctly (trunkx 712300 pre-reset,
    #-                           329900 after resetOrigins) and still
    #-                           short: the lane is not the problem,
    #-                           the intervening pin is.
    #- This is the same shape as the ladder below -- a link whose two
    #- pins are separated by a pin of the net in between -- and it
    #- wants the same answer, so it waits for it.
