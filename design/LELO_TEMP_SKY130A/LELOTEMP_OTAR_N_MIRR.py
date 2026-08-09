"""LELOTEMP_OTAR_N_MIRR: this subcell's own layout hooks.

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
    """Route the mirror. Declared type=mirror, so the built-in stack
    router declines the whole cell; the nets it needs are plain
    verticals once the pins are read:

    - VCP: the three xnc1 drains, adjacent rows, one M1 rail in the
      bar window right of the VSS straps (straps end 217200; 220400
      keeps the 1700 gap; bars run to 223600).
    - VD3: the diode xnc0 and the gates of all three xnc1 -- their
      tabs share the right lane (226800..230000), M2 so the rail can
      cross xns4's PWRUP_N tab. Plus xnc0's bar to xns4's drain bar,
      adjacent rows, M1 in the same bar window (y-disjoint from the
      VCP rail at the same x).

    PWRUP_N and the ports are the tabs themselves. Return None so the
    built-in still handles anything else it will take.
    """
    conn = layout.addConnectivityRoute
    conn("M1", "^VCP$", "||", f"trunkx={_bar_x(layout, 'xnc1<0>', 'VCP')},nostartcut,noendcut",
         1, "", r"^xnc1<\d+>$")
    #- onTopR: keep the TAB cut of the diode, not its bar cut, so
    #- the rail's bottom stays above xns4's PWRUP_N tab -- the parent
    #- lands its powerdown via stack there.
    conn("M1", "^VD3$", "||", f"trunkx={_tab_x(layout, 'xnc1<0>', 'VD3')},onTopR",
         1, "", r"^(xnc0|xnc1<\d+>)$")
    conn("M1", "^VD3$", "||", f"trunkx={_bar_x(layout, 'xns4', 'VD3')},nostartcut,noendcut",
         1, "", r"^(xnc0|xns4)$")
    return None
