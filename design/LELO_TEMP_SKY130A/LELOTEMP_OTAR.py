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
    layout.addPowerStrap("VSS", "", "bottom", terminals=("B",))

    s = layout._route_scopes

    #- Signals on M4 vertical, M3 horizontal: M1 is the pins' layer and M2
    #- carries the power straps, so M3 and M4 are the free ones.
    #-
    #- The ladder is five separate nets sharing one column, so one regex
    #- for all of them puts every trunk in the same place. Each gets its
    #- own track, and they alternate sides so no net's horizontal bar has
    #- to cross another's trunk to reach its own.
    for i, net in enumerate(("net2", "net3", "net4", "net5", "net6")):
        side = "onTopLeft" if i % 2 == 0 else "left"
        s["p_sw"].addOrthogonalConnectivityRoute("M4", "M3", f"^{net}$", f"{side},track{i//2}", 1)

    #- The two input gates. Every pin of each is inside its own column,
    #- so each is a single vertical run and neither leaves its stack
    s["p_in_a"].addConnectivityRoute("M4", "^VIN$", "||", "", 1)
    s["p_in_b"].addConnectivityRoute("M4", "^VIP$", "||", "", 1)

    #- VS is the tail node: the source of every input device in both
    #- columns, plus the top of the degeneration resistor in the nmos
    #- row. Run it across the pmos row first and see what it costs
    s["p_in_a"].addConnectivityRoute("M4", "^VS$", "||", "", 1)
    s["p_in_b"].addConnectivityRoute("M4", "^VS$", "||", "", 1)
    #- and the bar that ties the two columns together and reaches the
    #- resistor below. It crosses the channel, so it takes a track of
    #- its own
    layout.addOrthogonalConnectivityRoute("M4", "M3", "^VS$", "track0", 1, "", "")

    #- The two drain nets. Each stays in one column pair: VD1 runs the a
    #- lane from the input devices down to its diode loads, VD2 the b
    #- lane. Own track each so their channel bars clear
    layout.addOrthogonalConnectivityRoute("M4", "M3", "^VD1$", "track1,left", 1, "", "")
    layout.addOrthogonalConnectivityRoute("M4", "M3", "^VD2$", "track3", 1, "", "")

    #- net1 is two pins, the resistor bottom and the powerdown pull in
    #- the bias column above it
    layout.addOrthogonalConnectivityRoute("M4", "M3", "^net1$", "track5", 1, "", "")

    #- PWRUP_1V8 is three gates, all in the bias column: one vertical, no
    #- channel crossing
    s["p_bias"].addConnectivityRoute("M4", "^PWRUP_1V8$", "||", "", 1)

    #- VCP spans the ladder column, the bias column and the mirror column,
    #- so it goes around rather than through: a rail down the right hand
    #- edge, which is the side both its pmos groups end on, and each pin
    #- reaches it from its own row. The fill devices are held out, they
    #- carry the net too and would each ask for their own run
    #- a ring is routing, not content: without this the cell's bounding
    #- box grows to contain it and every later route measures from the
    #- wrong edge
    layout.ignoreBoundaryRouting = True
    layout.addRouteRing("M2", "VCP", "r", widthmult=1, spacemult=4)
    layout.addRouteConnection("VCP", "xnc", "M2", "right", "", excludeInstances="^xfill_")


