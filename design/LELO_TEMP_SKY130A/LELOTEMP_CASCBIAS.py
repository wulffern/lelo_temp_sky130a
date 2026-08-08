"""cicpy layout hooks for LELOTEMP_CASCBIAS.

Uncomment the hooks you need. Each hook receives the LayoutCell object
as ``layout``.
"""

from cicpy.core.rect import Rect


def _m2_terminal_rects(layout, net, instance_name, terminals=("D", "G")):
    graph = getattr(layout, "nodeGraph", None)
    if graph is None or net not in graph:
        return []
    wanted = set(terminals)
    rects = []
    for port in getattr(graph[net], "ports", []):
        inst = getattr(port, "parent", None)
        if inst is None or getattr(inst, "instanceName", "") != instance_name:
            continue
        if getattr(port, "childName", "") not in wanted:
            continue
        rect = port.get("M2") if hasattr(port, "get") else None
        if rect is None:
            continue
        rects.append(rect)
    return rects


def _add_m2_diode_stitch(layout, net, instance_name):
    rects = _m2_terminal_rects(layout, net, instance_name)
    if len(rects) < 2:
        return

    width = int(0.3 * layout.um)
    track_x = int(max(r.x2 for r in rects) + 0.4 * layout.um)
    y1 = int(min(r.centerY() for r in rects) - width / 2)
    y2 = int(max(r.centerY() for r in rects) + width / 2)

    vr = Rect("M2", track_x, y1, width, y2 - y1)
    vr.net = net
    layout.add(vr)

    for rect in rects:
        y = int(rect.centerY() - width / 2)
        x1 = int(min(rect.centerX(), track_x))
        x2 = int(max(rect.centerX(), track_x + width))
        hr = Rect("M2", x1, y, x2 - x1, width)
        hr.net = net
        layout.add(hr)


def beforePlace(layout):
    layout.noPowerRoute = True
    layout.place_xspace = [0]
    layout.place_yspace = [0]
    layout.place_groupbreak = [6]


def afterPlace(layout):
    nmos = layout.makeCellGroup("nmos")
    n_vbnt = nmos.transistorStack("xn_vbnt", routeDiodes=False)
    n_vcn = nmos.transistorStack("xn_vcn", routeDiodes=False)
    n_cap = nmos.transistorStack("xn_cap", routeDiodes=False)

    pmos = layout.makeCellGroup("pmos")
    p_mirr = pmos.currentMirrorStack("xp_mirr", routeDiodes=False)
    p_src = pmos.transistorStack("xp_src", routeDiodes=False).abutLeft(p_mirr)
    p_vcp = pmos.transistorStack("xp_vcp", routeDiodes=False).abutLeft(p_src)
    pmos.abutRight(nmos, space=2*layout.um)

    for group in [nmos, pmos]:
        group.updateBoundingRect()
        group.routeDummyDevices()

    layout.nmos = nmos
    layout.pmos = pmos



def beforeRoute(layout):
    #return
    layout.addRouteRing("M3", "PWRUP_N_1V8", "b", widthmult=1, spacemult=3)
    layout.addRouteRing("M3", "PWRUP_1V8", "t", widthmult=1, spacemult=3)
    #layout.addRouteRing("M3", "VCP", "b", widthmult=1, spacemult=3)
    #ayout.addRouteRing("M3", "VCN", "b", widthmult=1, spacemult=3)
    #layout.addRouteRing("M3", "VBNT", "b", widthmult=1, spacemult=3)


    layout.addRouteRing("M1", "VDD_1V8", "t", widthmult=3, spacemult=2)
    layout.addRouteRing("M1", "VSS", "b", widthmult=3, spacemult=2)

    #layout.addRouteConnection("VCP", "", "M4", "bottom", "", excludeInstances="^xfill_")
    #layout.addRouteConnection("VCN", "", "M4", "bottom", "", excludeInstances="^xfill_")
    #layout.addRouteConnection("VBNT", "", "M4", "bottom", "", excludeInstances="^xfill_")
    layout.addRouteConnection("PWRUP_1V8", "", "M2", "top", "", excludeInstances="^xfill_")
    layout.addRouteConnection("PWRUP_N_1V8", "", "M4", "bottom", "", excludeInstances="^xfill_")



    layout.addPowerConnection("VDD_1V8", "", "top", "^xfill_")
    layout.addPowerConnection("VSS", "", "bottom", "^xfill_")

    _add_m2_diode_stitch(layout, "VBNT", "xn_vbnt7")
    _add_m2_diode_stitch(layout, "VBP4", "xp_mirr4")
    _add_m2_diode_stitch(layout, "VCP", "xp_vcp1<0>")
    layout.addConnectivityRoute("M2","^VC_NSR","-|--","",2,"","")
    layout.addConnectivityRoute("M2","^VC_SER","-|--","",2,"","")
    #layout.addConnectivityRoute("M3","^VCP","-|--","",2,"","")
    # Bias trunks: one named RouteGroup per net, trunk + auto-spurs on
    # M3. The regex anchor in RouteGroup matches both bare and bus
    # forms, and U_TOP/U_BOTTOM auto-spans cross-domain anchors so a
    # single trunk reaches NMOS and PMOS pickups.
    #layout.addRouteGroup("VBP4").trunk("M3", side="top")
    #layout.addRouteGroup("VBNT").trunk("M3", side="bottom")
    pass


# def afterRoute(layout):
#     pass


# def beforePaint(layout):
#     pass


# def afterPaint(layout):
#     pass


# def beforePorts(layout):
#     pass


# def afterPorts(layout):
#     pass
