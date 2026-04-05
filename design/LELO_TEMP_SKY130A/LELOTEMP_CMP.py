#!/usr/bin/env python3


data = {
    "afterPaint": [
        {"resetOrigins": [[1]]},
    ]
}


def _inst(layout, name):
    inst = layout.getInstanceFromInstanceName(name)
    if inst is None:
        raise ValueError(f"Missing instance {name}")
    return inst


def beforePlace(layout):
    layout.noPowerRoute = True
    layout.place_xspace = [0]
    layout.place_yspace = [0]
    layout.place_groupbreak = [5]


def afterPlace(layout):
    branch_gap = 2 * layout.um

    nmos = layout.makeCellGroup("nmos")
    n_bias_ref = nmos.addStack("n_bias_ref", [_inst(layout, "xaa_bias_ref<0>"), _inst(layout, "xaa_bias_ref<1>")]).sort()
    n_bias_mirror = nmos.addStack("n_bias_mirror", [_inst(layout, f"xab_bias_mirror<{i}>") for i in range(4)]).sort()
    n_left = nmos.addStack("n_left", [_inst(layout, "xac_left<0>"), _inst(layout, "xac_left<1>")]).sort()
    n_right = nmos.addStack("n_right", [_inst(layout, "xad_right<0>"), _inst(layout, "xad_right<1>")]).sort()
    n_out = nmos.addStack("n_out", [_inst(layout, "xae_out<0>")]).sort()

    pmos = layout.makeCellGroup("pmos")
    p_bias_ref = pmos.addStack("p_bias_ref", [_inst(layout, "xba_bias_ref<0>"), _inst(layout, "xba_bias_ref<1>")]).sort()
    p_bias_mirror = pmos.addStack("p_bias_mirror", [_inst(layout, f"xbb_bias_mirror<{i}>") for i in range(3)]).sort()
    p_left = pmos.addStack("p_left", [_inst(layout, "xbc_left<0>")]).sort()
    p_right = pmos.addStack("p_right", [_inst(layout, "xbd_right<0>")]).sort()
    p_out = pmos.addStack("p_out", [_inst(layout, "xbe_out<0>")]).sort()

    nmos.fillDummyTransistors()
    n_bias_ref.addTaps()
    n_bias_mirror.addTaps()
    n_left.addTaps()
    n_right.addTaps()
    n_out.addTaps()

    pmos.fillDummyTransistors()
    p_bias_ref.addTaps()
    p_bias_mirror.addTaps()
    p_left.addTaps()
    p_right.addTaps()
    p_out.addTaps()

    pmos.abutTop(nmos, space=branch_gap)
