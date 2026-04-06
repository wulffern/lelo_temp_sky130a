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
    branch_gap = 2 * layout.um
    cap_gap = 1 * layout.um

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
    layout.addRouteRing("M1", "VSS", "b", widthmult=3, spacemult=2)
    layout.addPowerConnection("VDD_1V8", "", "top")
    layout.addPowerConnection("VSS", "", "bottom")

    caps = layout._route_scopes["caps"]
    cmp_group = layout._route_scopes["cmp"]
    nmos = layout._route_scopes["nmos"]

    caps.addConnectivityRoute("M5", "^IBP_1U<0>$", "||")
    nmos.addConnectivityRoute("M2", "^IBP_1U<0>$", "||")
    layout.addOrthogonalConnectivityRoute("M2", "M3", "^IBP_1U<0>$", "track0", 1, "", "^(x1_cmp|xg1)$", accessLayer="M2")
    layout.addOrthogonalConnectivityRoute("M2", "M3", "^PWRUP_N_1V8$", "onTopLeft,track0,left", 1, "", "^(x1_cmp|xg4)$")
