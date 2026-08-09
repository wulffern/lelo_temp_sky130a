"""LELOTEMP_OTAR_N_LOAD_A: this subcell's own layout hooks.

VD1 mixes two pin shapes the stack router declines: the wide D bars
(the diodes' bars plus xns1's shorter one) and the right-lane gate
tabs (the diodes' G tie and xnd3's gate). No single vertical lands on
all of them, so two do, and both are stated from the pins themselves
-- no coordinates:

- `trunkright` on the bar scope: the common overlap's right edge, so
  the rail lies on every bar including xns1's short one. Same layer
  as the pins, no cuts.
- `trunktab` on the tab scope: centred on the rightmost narrow rect,
  which is the gate-tab lane.

The two rails meet through the diodes' own bar-to-tab metal.
"""


def beforePlace(layout, entry):
    """Adjust this subcell's placement before anything routes."""


def beforeRoute(layout, entry):
    conn = layout.addConnectivityRoute
    conn("M1", "^VD1$", "||", "trunkright,nostartcut,noendcut",
         1, "", r"^(xnd1<\d+>|xns1)$")
    conn("M1", "^VD1$", "||", "trunktab",
         1, "", r"^(xnd1<\d+>|xnd3)$")
    return None
