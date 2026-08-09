"""LELOTEMP_OTAR_P_BIAS: this subcell's own layout hooks.

Generated once by `cicpy sch2subcells`, then yours: edit and commit.

Both hooks run in the parent, between its afterPlace and beforeRoute,
with `layout` the parent LayoutCell and `entry` this subcell's plan:
    entry["instances"]  the instance names in this subcell
    entry["ports"]      its boundary nets
    entry["internal"]   nets wholly inside it
    entry["type"]       stack | diffpair | mirror, from LELOTEMP.yaml
"""


def beforePlace(layout, entry):
    """Adjust this subcell's placement before anything routes."""


def beforeRoute(layout, entry):
    """Route VBP and PWRUP_1V8, which the stack router declines.

    VO it routes itself once the rows are adjacent.

    Depends on the row order the parent pycell sets for this stack
    (xba1, xba2, xba8, xba6, xba7, xba3 bottom to top): VO's two
    drains are then adjacent, VBP's two drains are adjacent, and the
    gate-tab lane interleaving that made VBP and PWRUP_1V8 mutually
    unroutable is gone -- VBP's tab span (xba8 to xba6) holds no
    PWRUP_1V8 tab, so VBP takes the lane on M2 and PWRUP_1V8 crosses
    it on M3, its via stacks' M2 pads all clear of VBP's wire.

    Drain rails sit in the bar window right of the VDD source straps
    (straps end 230000; 233200 keeps the 1700 gap; the shorter bars
    run to 236400). The tab lane is 239600..242800.
    """
    conn = layout.addConnectivityRoute
    conn("M1", "^VBP$", "||", "trunkright,nostartcut,noendcut",
         1, "", r"^(xba6|xba7)$")
    #- xba8's gate joins its drain pair on M4: the vertical rides the
    #- tab lane below the PWRUP_1V8 rail's span, and the far cut
    #- lands under the wire on xba7's bar, out in the window.
    conn("M4", "^VBP$", "-|--", "", 1, "", r"^(xba8|xba7)$")
    conn("M2", "^PWRUP_1V8$", "||", "trunktab,1cuts",
         1, "", r"^(xba2|xba3|xba7)$")
    return None
