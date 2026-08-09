"""LELOTEMP_OTAR_N_LOAD_B: this subcell's own layout hooks.

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
    """Route VD2 -- n_load_a's VD1, shifted one cell right (+80000).

    See LELOTEMP_OTAR_N_LOAD_A.py for the shape argument: an M1 rail
    in the bar window right of the VSS straps (140400), an M2 rail up
    the tab lane (148400) past xns2's PWRUP_N tab to xnd4's gate tab.
    """
    conn = layout.addConnectivityRoute
    conn("M1", "^VD2$", "||", f"trunkx={_bar_x(layout, 'xns2', 'VD2')},nostartcut,noendcut",
         1, "", r"^(xnd2<\d+>|xns2)$")
    conn("M1", "^VD2$", "||", f"trunkx={_tab_x(layout, 'xnd4', 'VD2')}",
         1, "", r"^(xnd2<\d+>|xnd4)$")
    return None
