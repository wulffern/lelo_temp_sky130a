"""LELOTEMP_OTAR_N_LOAD_A: this subcell's own layout hooks.

Generated once by `cicpy sch2subcells`, then yours: edit and commit.

Both hooks run in the parent, between its afterPlace and beforeRoute,
with `layout` the parent LayoutCell and `entry` this subcell's plan:
    entry["instances"]  the instance names in this subcell
    entry["ports"]      its boundary nets
    entry["internal"]   nets wholly inside it
    entry["type"]       stack | diffpair | mirror, from LELOTEMP.yaml
"""


def _rects(layout, inst, net):
    i = layout.getInstanceFromInstanceName(inst)
    return i.findRectanglesByNode(f"^{net}$", None) if i else []


def _bar_x(layout, inst, net):
    """Trunk x for a drain rail: RIGHT-ALIGNED on the bar, the
    library's lane convention (sources left, drains right). The
    source straps end 6400 left of the bar end, so even flush the
    wire clears them by 3400. Read from the LIVE pin rect: the
    pycell runs before resetOrigins, so published coordinates are
    the wrong frame here."""
    r = max(_rects(layout, inst, net), key=lambda r: r.x2 - r.x1)
    return int(r.x2) - 1500


def _tab_x(layout, inst, net):
    """Trunk x centered on the 3200 gate-tab lane. The RIGHTMOST
    narrow rect: an instance can carry duplicate subports and the
    narrowest pick landed a rail 6000 left, on the neighbouring
    bars (measured in p_sw: VCP tied every ladder net to VDD)."""
    rs = [r for r in _rects(layout, inst, net) if r.x2 - r.x1 <= 4000]
    r = max(rs or _rects(layout, inst, net), key=lambda r: r.x1)
    return int(r.x1) + 1600


def beforePlace(layout, entry):
    """Adjust this subcell's placement before anything routes."""


def beforeRoute(layout, entry):
    """Route VD1, which the stack router declines.

    VD1's pins mix two shapes: the wide D bars (the diodes' bar runs
    41200..70000, xns1's D stops at 63600) and the right-lane tabs
    (66800..70000; the diodes' G tie and xnd3's gate). No single
    vertical lands on all of them, so two do:

    - M1 in the bar window, right of the VSS source straps (they end
      at 57200; 60400 leaves the 1700 gap DRC wants): joins the three
      diode bars and xns1's D. Same layer as the pins, no cuts.
    - M1 up the tab lane (68400): joins the diode tabs and xnd3's
      gate tab. It crosses xns1's PWRUP_N tab as a wire, which is
      why it cannot be M1.

    The two rails meet through the diodes' own bar-to-tab metal.
    Return None: the built-in router still does the rest.
    """
    conn = layout.addConnectivityRoute
    conn("M1", "^VD1$", "||", f"trunkx={_bar_x(layout, 'xns1', 'VD1')},nostartcut,noendcut",
         1, "", r"^(xnd1<\d+>|xns1)$")
    conn("M1", "^VD1$", "||", f"trunkx={_tab_x(layout, 'xnd3', 'VD1')}",
         1, "", r"^(xnd1<\d+>|xnd3)$")
    return None
