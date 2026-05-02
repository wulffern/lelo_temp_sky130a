#!/usr/bin/env python3

data = {
    "afterPaint": [
        {"resetOrigins": [[1]]},
    ]
}


def beforePlace(layout):
    layout.noPowerRoute = True
    layout.place_xspace = [0]
    layout.place_yspace = [0]
    layout.place_groupbreak = [1]


def afterPlace(layout):
    branch_gap = 3 * layout.um
    cap_gap = 2 * layout.um

    cmp_group = layout.makeCellGroup("cmp")
    cmp_stack = cmp_group.addStack("cmp_stack", layout.getSortedInstancesByInstanceName("x1_cmp"))
    cmp_inst = layout.getInstanceFromInstanceName("x1_cmp")
    if cmp_inst is not None:
        cmp_inst.setAngle("MY")

    caps = layout.makeCellGroup("caps")
    cap_stack = caps.addStack("cap_stack", layout.getSortedInstancesByInstanceName("xd1"))
    cap_stack.stack(ygap=cap_gap)

    nmos = layout.makeCellGroup("nmos")
    nmos_stack = nmos.addStack("nmos_stack", layout.getSortedInstancesByInstanceName("xg"))
    nmos_stack.addTaps()

    nmos.abutRight(cmp_group, space=branch_gap)
    caps.abutRight(nmos, space=branch_gap)

    cmp_group.updateBoundingRect()
    caps.updateBoundingRect()
    nmos.updateBoundingRect()
    nmos.routeDummyDevices()

    layout._route_scopes = {
        "cmp": cmp_group,
        "cmp_stack": cmp_stack,
        "caps": caps,
        "cap_stack": cap_stack,
        "nmos": nmos,
        "nmos_stack": nmos_stack,
    }


def beforeRoute(layout):
    layout.addRouteRing("M1", "VDD_1V8", "t", widthmult=3, spacemult=2)
    layout.addRouteRing("M1", "VSS", "b", widthmult=3, spacemult=5)
    layout.addPowerConnection("VDD_1V8", "", "top")
    layout.addPowerConnection("VSS", "", "bottom")

    caps = layout._route_scopes["caps"]
    nmos = layout._route_scopes["nmos"]
    nmos_stack = layout._route_scopes["nmos_stack"]

    caps.addConnectivityRoute("M5", "^IBP_1U<0>$", "||")
    #layout.addConnectivityRoute("M4", "^IBP_1U<0>$","-|--","track2,onTopLeft,noendcut", 2,"cmp","")
    layout.addOrthogonalConnectivityRoute("M2", "M4", "^IBP_1U", "onTopLeft,noendcut,track0", 1, "x1_cmp", "")
    layout.addOrthogonalConnectivityRoute("M2", "M3", "^PWRUP_N_1V8$", "onTopLeft,track0,left", 1, "", "^(x1_cmp|xg4)$", accessLayer="M2")


def afterPorts(layout):
    layout.addPortOnEdge("M2","RST","bottom","--|-", "offset_track-4,track4")
    pass
    #caps = layout._route_scopes["caps"]
    #cmp_group = layout._route_scopes["cmp"]
    #nmos = layout._route_scopes["nmos"]

    #exported_ports = [
    #    ("CMPO", cmp_group.representativeAccessRects("CMPO", "M4"), "M4"),
    #    ("VC", cmp_group.representativeAccessRects("VC", "M2"), "M2"),
    #    ("PWRUP_B_1V8", cmp_group.representativeAccessRects("PWRUP_B_1V8", "M3"), "M3"),
    #    ("PWRUP_N_1V8", cmp_group.representativeAccessRects("PWRUP_N_1V8", "M3"), "M3"),
    #    ("IBP_1U<1>", cmp_group.representativeAccessRects("IBP_1U<1>", "M3"), "M3"),
    #    ("RST", nmos.representativeAccessRects("RST", "M2", anymetal=True), "M2"),
    #]
    #for node, rects, layer in exported_ports:
    #    if rects:
    #        layout.addPortFromRect(node, rects[0], routeLayer=layer)

    #cap_ring = layout.addRouteRingOnRect("M5", "ibp_cap_pickup", caps.getCopy(), "l", widthmult=1, spacemult=2)

    #cap_rects = caps.representativeAccessRects("IBP_1U<0>", "M5")
    #branch_rects = layout.collectPhysicalRects("IBP_1U<0>", "M3")
    #if cap_ring is not None and cap_rects and branch_rects:
    #    layout.addOrthogonalRouteFromRects("IBP_1U<0>", "M4", "M5", [branch_rects[0], cap_ring.get("left")], "onTopTop,track2,branchtrack0,nolabel", cuts=1)
    #    caps_x1 = caps.getCopy().x1
    #    m5_all = layout.collectPhysicalRects("IBP_1U<0>", "M5")
    #    m5_in_gap = [r for r in m5_all if r.centerX() < caps_x1]
    #    if m5_in_gap:
    #        rightmost = max(m5_in_gap, key=lambda r: r.centerX())
    #        layout.addRouteFromRects("IBP_1U<0>", "M5", [rightmost], cap_rects, "-", "nolabel")
    #    layout.addPortFromRect("IBP_1U<0>", cap_ring.get("left"), routeLayer="M5")
