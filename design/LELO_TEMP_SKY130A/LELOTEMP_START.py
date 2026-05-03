def beforePlace(layout):
    layout.noPowerRoute = True
    layout.place_xspace = [0]
    layout.place_yspace = [0]
    layout.place_groupbreak = [5]


def afterPlace(layout):
    device_type_gap = 2 * layout.um

    pmos = layout.makeCellGroup("pmos")
    p_ladder_mid = pmos.addStack("p_ladder_mid", layout.getSortedInstancesByInstanceName("xp_b1"))
    p_ladder_top = pmos.addStack("p_ladder_top", layout.getSortedInstancesByInstanceName("xp_c2"))
    p_ladder_out = pmos.addStack("p_ladder_out", layout.getSortedInstancesByInstanceName("xp_f1"))
    p_ctrl = pmos.addStack("p_ctrl", _instances(layout, ["xp_d5", "xp_d4", "xp_d1", "xp_d2"]))

    nmos = layout.makeCellGroup("nmos")
    n_vp = nmos.addStack("n_vp", _instances(layout, ["xn_a9", "xn_a10"]))
    n_vbn = nmos.addStack(
        "n_vbn",
        _instances(
            layout,
            [
                "xn_a1",
                "xn_a2<0>",
                "xn_a2<1>",
                "xn_a2<2>",
                "xn_a2<3>",
                "xn_a3",
                "xn_a4",
                "xn_a5",
                "xn_a6",
                "xn_a7",
                "xn_a8",
            ],
        ),
    )

    p_ladder_mid.stack()
    p_ladder_top.stack()
    p_ladder_out.stack()
    p_ctrl.stack()
    n_vp.stack()
    n_vbn.stack()

    pmos.fillDummyTransistors()
    nmos.fillDummyTransistors()

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
    layout.addRouteRing("M1", "VDD_1V8", "t", widthmult=3, spacemult=2)
    layout.addRouteRing("M1", "VSS", "b", widthmult=3, spacemult=2)
    layout.addPowerConnection("VDD_1V8", "", "top")
    layout.addPowerConnection("VSS", "", "bottom")

    layout.addConnectivityRoute("M3","^SER","-|--","",2,"","")
    layout.addConnectivityRoute("M3","^MID","-|--","",2,"","")
    layout.addConnectivityRoute("M3","^TOP","-|--","",2,"","")

    layout.addOrthogonalConnectivityRoute(
        "M2",
        "M3",
        "^VCP$",
        "right,onTopRight,verticaltrack0,nolabel",
        1,
        "",
        "^xn_a9$",
        accessLayer="M2",
    )
    layout.addOrthogonalConnectivityRoute(
        "M2",
        "M3",
        "^VO$",
        "right,onTopRight,verticaltrack0,nolabel",
        1,
        "",
        "^xn_a10$",
        accessLayer="M2",
    )
    layout.addOrthogonalConnectivityRoute(
        "M2",
        "M3",
        "^VP2$",
        "right,onTopRight,verticaltrack2,nolabel",
        1,
        "",
        "^(xn_a10|xn_a8)$",
        accessLayer="M2",
    )
    layout.addOrthogonalConnectivityRoute(
        "M2",
        "M3",
        "^VP1$",
        "right,onTopRight,verticaltrack4,nolabel",
        1,
        "",
        "^(xn_a9|xn_a7)$",
        accessLayer="M2",
    )
    layout.addOrthogonalConnectivityRoute(
        "M2",
        "M3",
        "^VSTART2$",
        "left,onTopLeft,verticaltrack0,nolabel",
        1,
        "",
        "^(xn_a5|xn_a6)$",
        accessLayer="M2",
    )
    layout.addOrthogonalConnectivityRoute(
        "M2",
        "M3",
        "^VSTART3$",
        "left,onTopLeft,verticaltrack2,nolabel",
        1,
        "",
        "^(xn_a6|xn_a7|xn_a8)$",
        accessLayer="M2",
    )
    layout.addOrthogonalConnectivityRoute(
        "M2",
        "M3",
        "^PWRUP_N_1V8$",
        "left,onTopLeft,verticaltrack0,nolabel",
        1,
        "",
        "^(xn_a3|xn_a4|xp_d5)$",
        accessLayer="M2",
    )
    layout.addOrthogonalConnectivityRoute(
        "M2",
        "M3",
        "^VSTART1$",
        "center,onTopTop,verticaltrack0,nolabel",
        1,
        "",
        "^(xn_a2<0>|xn_a2<1>|xn_a2<2>|xn_a2<3>|xn_a4|xn_a5)$",
        accessLayer="M2",
    )


def afterPorts(layout):
    pass


def _instances(layout, names):
    instances = []
    for name in names:
        inst = layout.getInstanceFromInstanceName(name)
        if inst is None:
            raise ValueError(f"Missing instance {name}")
        instances.append(inst)
    return instances
