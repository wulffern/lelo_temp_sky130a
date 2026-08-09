"""LELOTEMP_OTAR: the OTA on REY_ATR transistors.

Placement here. The subcells and their types are declared in
LELOTEMP_OTAR.yaml; each subcell's own hooks live in
LELOTEMP_OTAR_<SUBCELL>.py. The measurement history that used to fill
this file lives in cicpy/plans/ and the git log.
"""
import re

data = {
    "afterPaint": [
        {"resetOrigins": [[1]]},
    ]
}


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
    channel = 6 * layout.um

    xbl = layout.getSortedInstancesByGroupName("xbl")
    xnd = layout.getSortedInstancesByGroupName("xnd")

    pmos = layout.makeCellGroup("pmos")
    p_in_a = pmos.addStack("p_in_a", _pick(xbl, [r"xbl4"]) + _pick(xbl, [r"xbl1<\d+>"]), preserveOrder=True)
    p_in_b = pmos.addStack("p_in_b", _pick(xbl, [r"xbl5"]) + _pick(xbl, [r"xbl2<\d+>"]), preserveOrder=True)
    p_bias = pmos.addStackByGroup("xba", name="p_bias")
    xbs = layout.getSortedInstancesByGroupName("xbs")
    chain = []
    for nm in ("xbs6", "xbs1", "xbs2", "xbs4", "xbs7", "xbs8"):
        chain += _pick(xbs, [nm])
    p_sw = pmos.addStack("p_sw", chain, preserveOrder=True)

    xns = layout.getSortedInstancesByGroupName("xns")
    xnc = layout.getSortedInstancesByGroupName("xnc")

    nmos = layout.makeCellGroup("nmos")
    n_load_a = nmos.addStack("n_load_a", _pick(xnd, [r"xnd1<\d+>", r"xnd3"]) + _pick(xns, [r"xns1"]), preserveOrder=True)
    n_load_b = nmos.addStack("n_load_b", _pick(xnd, [r"xnd2<\d+>", r"xnd4"]) + _pick(xns, [r"xns2"]), preserveOrder=True)
    n_mirr = nmos.addStack("n_mirr", xnc + _pick(xns, [r"xns4"]), preserveOrder=True)

    res = layout.makeCellGroup("res")
    r_deg = res.addStackByGroup("xd", name="r_deg")

    for s in (p_in_a, p_in_b, p_bias, p_sw, n_load_a, n_load_b, n_mirr):
        s.stack()
    r_deg.stack()
    r_deg.addTaps()

    for st in (p_bias, n_load_a, n_load_b, n_mirr):
        st.orderByTerminalNet("D")


    pmos.fillDummyTransistors()
    nmos.fillDummyTransistors()

    p_in_a.addTaps()
    p_in_b.addTaps()
    p_bias.addTaps()
    p_sw.addTaps()
    n_load_a.addTaps()
    n_load_b.addTaps()
    n_mirr.addTaps()

    p_in_b.abutRight(p_in_a)
    p_bias.abutRight(p_in_b)
    p_sw.abutRight(p_bias)

    n_load_b.abutRight(n_load_a)
    n_mirr.abutRight(n_load_b)

    pmos.updateBoundingRect()
    nmos.updateBoundingRect()
    res.updateBoundingRect()

    pmos.abutTop(nmos, space=channel)

    r_deg.abutRight(nmos)
    r_deg.translate(0, nmos.y1 - r_deg.y1)

    pmos.updateBoundingRect()
    nmos.updateBoundingRect()
    res.updateBoundingRect()
    nmos.routeDummyDevices()
    pmos.routeDummyDevices()

    layout.addRoutingChannel("mid", nmos.y2, pmos.y1)
    for nm, st in (("in_a", p_in_a), ("in_b", p_in_b),
                   ("bias", p_bias), ("sw", p_sw)):
        layout.addRoutingChannel(nm, st.x1, st.x2, horizontal=False)
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
    layout.addRouteRing("M1", "VDD_1V8", "t", widthmult=3, spacemult=2)
    layout.addRouteRing("M1", "VSS", "b", widthmult=3, spacemult=2)
    layout.addPowerGuardConnection("VDD_1V8", excludeInstances="^xbs6$")
    layout.addPowerGuardConnection("VSS")
    layout.addPowerStrap("VDD_1V8", "", "top", terminals=("B",))
    layout.addPowerStrap("VSS", "", "bottom", terminals=("B",),
                         excludeInstances=r"^xd2<[1-9]")

    _route_stacks(layout)


#- every subcell. What a router cannot take it declines -- by TYPE
#- (n_mirr is a mirror in LELOTEMP_OTAR.yaml and no mirror router
#- exists yet) or by measurement -- and a decline is an open, never a
#- short.
STACK_ROUTING = None
STACK_BOUNDARY = True


def _route_stacks(layout):
    from cicpy.core.mazerouter import route_stack_level
    routed, blocked = route_stack_level(layout, log=layout.log,
                                        only=STACK_ROUTING,
                                        boundary=STACK_BOUNDARY)
    layout.log.info(f"stack level: {len(routed)} routed, "
                    f"{len(blocked)} blocked")


def afterPaint(layout):
    """Publish each stack as its own cell.

    Every stack gets a .mag and a generated subckt of its own, so it can
    be LVS'd ALONE -- which is the gate the hierarchy needs before the
    group and top levels are routed on top of it. A stack that fails
    stops the run where the evidence is nine instances rather than 1969
    rects.

    The parent is NOT restructured. It keeps its instances; the stacks
    are published alongside. Making the parent reference them instead of
    containing them is a separate change and should wait until these
    pass LVS -- the difference between "generate and check" and
    "generate, check, and rely on".

    In afterPaint rather than afterRoute so the stacks are published
    with the routing that was just drawn into them.
    """
    from cicpy.core.mazerouter import write_stack_cells
    write_stack_cells(layout, log=layout.log)

