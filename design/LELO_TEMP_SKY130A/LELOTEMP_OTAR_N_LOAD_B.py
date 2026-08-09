"""LELOTEMP_OTAR_N_LOAD_B: this subcell's own layout hooks.

VD2 is n_load_a's VD1, one cell right -- see that file for the shape
argument. Both rails are stated from the pins themselves, no
coordinates: `trunkright` is the bar overlap's right edge (so the
rail lies on xns2's shorter bar too), `trunktab` centres on the
rightmost narrow rect, the gate-tab lane.
"""


def beforePlace(layout, entry):
    """Adjust this subcell's placement before anything routes."""


def beforeRoute(layout, entry):
    conn = layout.addConnectivityRoute
    conn("M1", "^VD2$", "||", "trunkright,nostartcut,noendcut",
         1, "", r"^(xnd2<\d+>|xns2)$")
    conn("M1", "^VD2$", "||", "trunktab",
         1, "", r"^(xnd2<\d+>|xnd4)$")
    return None
