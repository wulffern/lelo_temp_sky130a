def beforePlace(layout):
    layout.noPowerRoute = True
    layout.place_xspace = [0]
    layout.place_yspace = [0]
    layout.place_groupbreak = [5]


def afterPlace(layout):
    device_type_gap = 2 * layout.um

    pmos = layout.makeCellGroup("pmos")
    p_ladder_mid = pmos.addStackByGroup("xp_ladder_mid", name="p_ladder_mid")
    p_ladder_top = pmos.addStackByGroup("xp_ladder_top", name="p_ladder_top")
    p_ladder_out = pmos.addStackByGroup("xp_ladder_out", name="p_ladder_out")
    p_ctrl = pmos.addStackByGroup("xp_ctrl", name="p_ctrl", fillGroup="xfill_xp_ctrl")

    nmos = layout.makeCellGroup("nmos")
    n_vp = nmos.addStackByGroup("xn_vp", name="n_vp", fillGroup="xfill_xn_vp")
    n_vbn = nmos.addStackByGroup("xn_vbn", name="n_vbn")

    p_ladder_mid.stack()
    p_ladder_top.stack()
    p_ladder_out.stack()
    p_ctrl.stack()
    n_vp.stack()
    n_vbn.stack()

    for stack in [p_ladder_mid, p_ladder_top, p_ladder_out, p_ctrl, n_vp, n_vbn]:
        stack.addTaps()

    p_ladder_out.abutRight(p_ctrl, space=0)
    p_ladder_top.abutRight(p_ladder_out, space=0)
    p_ladder_mid.abutRight(p_ladder_top, space=0)

    n_vbn.abutRight(n_vp, space=0)
    nmos.abutLeft(pmos, space=device_type_gap)

    for group in [pmos, nmos]:
        group.updateBoundingRect()
        group.routeDummyDevices()

    layout._route_scopes = {
        "pmos": pmos,
        "p_ladder_top": p_ladder_top,
        "p_ladder_mid": p_ladder_mid,
        "p_ladder_out": p_ladder_out,
        "p_ctrl": p_ctrl,
        "nmos": nmos,
        "n_vp": n_vp,
        "n_vbn": n_vbn,
    }


def beforeRoute(layout):

    layout.addRouteRing("M3", "VSTART1", "b", widthmult=1, spacemult=2)
    layout.addRouteRing("M3", "VSTART3", "b", widthmult=1, spacemult=2)
    layout.addRouteRing("M2", "VCP", "l", widthmult=1, spacemult=3)
    layout.addRouteRing("M3", "VO", "t", widthmult=1, spacemult=2)
    layout.addRouteRing("M1", "VDD_1V8", "t", widthmult=3, spacemult=2)
    layout.addRouteRing("M1", "VSS", "b", widthmult=3, spacemult=2)
    layout.addRouteConnection("VSTART1", "xp", "M2", "bottom", "", excludeInstances="^xfill_")
    layout.addRouteConnection("VCP", "xn_vp3", "M3", "left", "", excludeInstances="^xfill_")
    layout.addRouteConnection("VSTART3", "xp|xn_vp1", "M4", "bottom", "", excludeInstances="^xfill_")
    layout.addRouteConnection("VO", "", "M4", "top", "", excludeInstances="^xfill_")
    layout.addPowerConnection("VDD_1V8", "", "top", "^xfill_")
    layout.addPowerConnection("VSS", "", "bottom", "^xfill_")

    layout.addConnectivityRoute("M3","^SER","-|--","",2,"^xfill_","")
    layout.addConnectivityRoute("M3","^MID","-|--","",2,"^xfill_","")
    layout.addConnectivityRoute("M3","^TOP","-|--","",2,"^xfill_","")

    layout.addOrthogonalConnectivityRoute(
        "M2",
        "M3",
        "^VBN$",
        "onTopLeft,verticaltrack6",
        1,
        r"^(xn_vbn2)",
        "",
        accessLayer="M2",
    )
    layout.addConnectivityRoute("M2","^VBN","||","",2,"^xfill_","^(xn_vbn1|xn_vbn2)")




    layout.addOrthogonalConnectivityRoute(
        "M2",
        "M3",
        "^VP2$",
        "left,onTopRight,verticaltrack0,nolabel",
        1,
        "^xfill_",
        "^(xn_vp4|xn_vp2)$",
        accessLayer="M2",
    )
    layout.addOrthogonalConnectivityRoute(
        "M2",
        "M3",
        "^VP1$",
        "left,onTopLeft,verticaltrack1,nolabel",
        1,
        "^xfill_",
        "^(xn_vp3|xn_vp1)$",
        accessLayer="M2",
    )
    layout.addOrthogonalConnectivityRoute(
        "M2",
        "M3",
        "^VSTART2$",
        "right,onTopLeft,verticaltrack8,nolabel",
        1,
        "^xfill_",
        "^(xn|xp)",
        accessLayer="M2",
    )
    layout.addOrthogonalConnectivityRoute(
        "M2",
        "M3",
        "^VSTART3$",
        "left,onTopLeft,verticaltrack2,nolabel",
        1,
        "^xfill_",
        "^(xn_vbn6|xn_vp1|xn_vp2)$",
        accessLayer="M2",
    )
    layout.addOrthogonalConnectivityRoute(
        "M2",
        "M3",
        "^PWRUP_N_1V8$",
        "left,onTopLeft,verticaltrack0,nolabel",
        1,
        "^xfill_",
        "^(xn_vbn3|xn_vbn4|xp_ctrl4)$",
        accessLayer="M2",
    )
    layout.addOrthogonalConnectivityRoute(
        "M2",
        "M3",
        "^VSTART1$",
        "right,onTopLeft,verticaltrack2,nolabel",
        1,
        "^xfill_",
        "^(xn)",
        accessLayer="M2",
    )
    layout.addOrthogonalConnectivityRoute(
        "M2",
        "M3",
        "^VSTART1$",
        "right,onTopLeft,verticaltrack4,nolabel",
        1,
        "^xfill_",
        "^(xn_vbn2<0>|xp_ctrl)",
        accessLayer="M2",
    )


def afterPorts(layout):
    pass

