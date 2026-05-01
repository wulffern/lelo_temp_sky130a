data = {
    "afterPaint": [
        {"resetOrigins": [[1]]},
    ]
}

def beforePlace(layout):
    layout.noPowerRoute = True
    layout.place_xspace = [0]
    layout.place_yspace = [0]
    layout.place_groupbreak = [5]


def beforeRoute(layout):
    # VBP2: top-only M3 rail + M4 vertical stubs from each pin up to the rail.
    # Using location="t" avoids vertical M3 edges that would short VS's M3 branches.
    layout.addRouteRing("M3", "VBP2", "t", widthmult=2, spacemult=2)
    layout.addRouteRing("M1", "VDD_1V8", "t", widthmult=3, spacemult=2)
    layout.addRouteRing("M1", "VSS", "b", widthmult=3, spacemult=2)
    layout.addPowerConnection("VDD_1V8", "", "top")
    layout.addPowerConnection("VSS", "", "bottom")
    n_mirr_bias = layout._route_scopes["n_mirr_bias"]
    n_mirr_load = layout._route_scopes["n_mirr_load"]
    nmos = layout._route_scopes["nmos"]
    pmos = layout._route_scopes["pmos"]
    # Stack-local and group-local routes first.
    n_mirr_bias.addOrthogonalConnectivityRoute("M2", "M3", "^IBP_1U$", "track0", 1, accessLayer="M2")
    nmos.addOrthogonalConnectivityRoute("M4", "M3", "^PWRUP_N_1V8$", "onTopLeft,track6", 1, accessLayer="M2")
    pmos.addOrthogonalConnectivityRoute("M4", "M3", "^VS$", "track0", 1, accessLayer="M1")
    # Cross-group routes last.

    layout.addRouteConnection("^VBP2$", "", "M4", "top", "")
    layout.addOrthogonalConnectivityRoute("M4", "M3", "^VO1$", "onTopLeft,track6", 1, "", "", accessLayer="M1")
    layout.addOrthogonalConnectivityRoute("M4", "M3", "^VO$", "onTopLeft,track8", 1, "", "", accessLayer="M1")
    layout.addOrthogonalConnectivityRoute("M4", "M3", "^VBN1$", "onTopLeft,track4", 1, "", "", accessLayer="M1")

def afterPorts(layout):
    layout.addPortOnEdge("M4","VO","top","||", "")
    layout.addPortOnEdge("M3","IBP_1U","left","|-", "track0")
    layout.addPortOnEdge("M3","PWRUP_N_1V8","left","|-", "track6")
    layout.addPortOnEdge("M2","VIN","bottom","||", "")
    layout.addPortOnEdge("M3","PWRUP_1V8","right","-|", "offset_track0")
    layout.addPortOnEdge("M2","VIP","bottom","--|-", "offset_track-4,track4")

def afterPlace(layout):
    branch_gap = 2 * layout.um
    nmos = layout.makeCellGroup("nmos")
    n_mirr_load = nmos.addStack("n_mirr_load",layout.getSortedInstancesByInstanceName("xn_mirr_load"))
    n_mirr_bias = nmos.addStack("n_mirr_bias",layout.getSortedInstancesByInstanceName("xn_mirr_bias"))

    pmos = layout.makeCellGroup("pmos")
    p_mirr_tail = pmos.addStack("p_mirr_load",layout.getSortedInstancesByInstanceName("xp_mirr_tail"))
    p_diff = pmos.addStack("p_diff",layout.getSortedInstancesByInstanceName("xp_diff"))


    pmos.abutRight(nmos, space=branch_gap)

    n_mirr_load.addTaps()
    n_mirr_bias.addTaps()

    p_mirr_tail.addTaps()
    p_diff.addTaps()

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
