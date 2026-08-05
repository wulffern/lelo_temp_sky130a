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

    xbl = layout.getSortedInstancesByGroupName("xbl")
    xnd = layout.getSortedInstancesByGroupName("xnd")

    pmos = layout.makeCellGroup("pmos")
    p_in_a = pmos.addStack("p_in_a", _pick(xbl, [r"xbl0<[01]>", r"xbl1<[01]>", r"xbl4"]), preserveOrder=True)
    p_in_b = pmos.addStack("p_in_b", _pick(xbl, [r"xbl0<[23]>", r"xbl1<[23]>", r"xbl5"]), preserveOrder=True)
    p_bias = pmos.addStackByGroup("xba", name="p_bias")
    p_sw = pmos.addStackByGroup("xbs", name="p_sw")

    nmos = layout.makeCellGroup("nmos")
    n_load_a = nmos.addStack("n_load_a", _pick(xnd, [r"xnd1<[0-3]>", r"xnd3"]), preserveOrder=True)
    n_load_b = nmos.addStack("n_load_b", _pick(xnd, [r"xnd2<[0-3]>", r"xnd4"]), preserveOrder=True)
    n_mirr = nmos.addStackByGroup("xnc", name="n_mirr")
    n_sw = nmos.addStackByGroup("xns", name="n_sw")

    res = layout.makeCellGroup("res")
    r_deg = res.addStackByGroup("xd", name="r_deg")

    #- pack every column. The split stacks inherit interleaved first pass
    #- positions from their source groups, so without this each column has
    #- holes where the other half's devices used to sit
    for s in (p_in_a, p_in_b, p_bias, p_sw, n_load_a, n_load_b, n_mirr, n_sw, r_deg):
        s.stack()

    #- mirror the right half of each matched pair, the seam then carries
    #- mirror symmetric edge geometry and the halves can abut
    p_in_b.mirror()
    n_load_b.mirror()

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
    n_sw.addTaps()

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
    n_sw.abutRight(n_mirr, space=branch_gap)

    pmos.updateBoundingRect()
    nmos.updateBoundingRect()
    res.updateBoundingRect()

    #- pmos row above nmos row, and the resistor in the notch above the
    #- short powerdown stack, under the pmos row
    pmos.abutTop(nmos, space=branch_gap)
    #- the resistor is shorter than the nmos row, so it rides along at the
    #- end of the row. The branch gap keeps the poly resistor clear of the
    #- 0.48 um poly.9 spacing to the tap diffusion next to it
    r_deg.abutRight(n_sw, space=branch_gap)

    pmos.updateBoundingRect()
    nmos.updateBoundingRect()
    res.updateBoundingRect()
    nmos.routeDummyDevices()
    pmos.routeDummyDevices()

    layout._route_scopes = {
        "pmos": pmos,
        "nmos": nmos,
        "p_in_a": p_in_a,
        "p_in_b": p_in_b,
        "p_bias": p_bias,
        "p_sw": p_sw,
        "n_load_a": n_load_a,
        "n_load_b": n_load_b,
        "n_mirr": n_mirr,
        "n_sw": n_sw,
    }
