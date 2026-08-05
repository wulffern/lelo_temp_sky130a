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
    p_in_a = pmos.addStack("p_in_a", _pick(xbl, [r"xbl4"]) + _pick(xbl, [r"xbl1<[0-3]>"]), preserveOrder=True)
    p_in_b = pmos.addStack("p_in_b", _pick(xbl, [r"xbl5"]) + _pick(xbl, [r"xbl0<[0-3]>"]), preserveOrder=True)
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
    n_load_a = nmos.addStack("n_load_a", _pick(xnd, [r"xnd1<[0-3]>", r"xnd3"]) + _pick(xns, [r"xns1"]), preserveOrder=True)
    n_load_b = nmos.addStack("n_load_b", _pick(xnd, [r"xnd2<[0-3]>", r"xnd4"]) + _pick(xns, [r"xns2"]), preserveOrder=True)
    n_mirr = nmos.addStack("n_mirr", xnc + _pick(xns, [r"xns4"]), preserveOrder=True)

    res = layout.makeCellGroup("res")
    r_deg = res.addStackByGroup("xd", name="r_deg")

    #- pack every column. The split stacks inherit interleaved first pass
    #- positions from their source groups, so without this each column has
    #- holes where the other half's devices used to sit
    for s in (p_in_a, p_in_b, p_bias, p_sw, n_load_a, n_load_b, n_mirr, r_deg):
        s.stack()

    #- mirror the left half of each matched pair. The cells carry S left of
    #- center and D right, so mirroring the left half puts source against
    #- source at the seam: mirror symmetric edges that may abut, and no
    #- different-net drain drops facing each other across the seam
    p_in_a.mirror()
    n_load_a.mirror()

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
    n_mirr.abutRight(n_load_b, space=branch_gap)

    pmos.updateBoundingRect()
    nmos.updateBoundingRect()
    res.updateBoundingRect()

    #- pmos row above nmos row, and the resistor in the notch above the
    #- short powerdown stack, under the pmos row
    pmos.abutTop(nmos, space=channel)
    #- both resistor terminals belong to the pmos row, so the resistor
    #- wants to sit at the right end of that row rather than here. It stays
    #- in the nmos row for now: moved against p_sw it widens the cell by
    #- its own width plus two gaps and buys nothing until VS and net1 can
    #- actually be routed. The branch gap keeps the poly resistor clear of
    #- the 0.48 um poly.9 spacing to the tap diffusion next to it
    r_deg.abutRight(n_mirr, space=branch_gap)

    pmos.updateBoundingRect()
    nmos.updateBoundingRect()
    res.updateBoundingRect()
    nmos.routeDummyDevices()
    pmos.routeDummyDevices()

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
    #- power on M1 rails, VDD along the pmos row top, VSS along the nmos
    #- row bottom, same pattern as LELOTEMP_CMP
    layout.addRouteRing("M1", "VDD_1V8", "t", widthmult=3, spacemult=2)
    layout.addRouteRing("M1", "VSS", "b", widthmult=3, spacemult=2)
    layout.addPowerConnection("VDD_1V8", "", "top")
    layout.addPowerConnection("VSS", "", "bottom")

    s = layout._route_scopes

    #- Wiring follows LELOTEMP_CMP: one addOrthogonalConnectivityRoute per
    #- net, scoped to the smallest group that holds the whole net so the
    #- horizontal bar spans as little x as possible. routeMirror and
    #- routeDiodeConnected are not used here, they place every rail of a
    #- column at the x of its pins and columns carrying several nets on
    #- one terminal then short.

    #- ladder junctions, each between two neighbouring cells of one column
    s["p_sw"].addOrthogonalConnectivityRoute("M2", "M3", "^net[23456]$", "onTopLeft", 1)

    #- the two differential branches. Each drain net owns one x lane, the
    #- pmos input half sits directly above the nmos load half it drives,
    #- so the net is a vertical rail with one bar per row
    layout.addOrthogonalConnectivityRoute("M2", "M3", "^VD1$", "onTopLeft,track4", 1, "", "")
    layout.addOrthogonalConnectivityRoute("M2", "M3", "^VD2$", "onTopLeft,track6", 1, "", "")
    #- the common mode sense branch, its loads sit under the two input
    #- devices xbl4 and xbl5 that feed it
    #- VD3 is NOT routed. It is the one net with pins in both rows and in
    #- three columns, and the router can only reach across by dropping a
    #- vertical through a column, where it lands on the M2 access pads
    #- another net already put on that column's pins. It needs primitives
    #- that keep the metal layers free, see REY_ATR_SKY130A.
    #layout.addOrthogonalConnectivityRoute("M2", "M3", "^VD3$", "onTopLeft,track8", 1, "", "")
