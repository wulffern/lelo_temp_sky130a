"""Routing for the switch stack, on its own.

This file exists to make a point as much as to route a column: the five
ladder nets are a small local problem and were only ever a hard one
because they were being solved at the top, against the whole cell.

    net1..net5 are INTERNAL to this stack. Nothing above it can see
    them, nothing above it can collide with them, and nothing above it
    has to reserve a track for them.

It was also dead for two sessions, and the reason is worth keeping:
cicpy ran stack pycells from `write_stack_cells` in **afterPaint**, so
the routes below were created after `route()` had already drawn
everything. They were never drawn, and the log said "routed by its own
pycell" regardless. cicpy now calls stack pycells between afterPlace
and beforeRoute -- see `run_stack_pycells` -- and the hook takes
`(layout, entry)`.

Measured against the built-in stack router on the same placement: both
give 0 DRC, 0 shorts and a correctly extracted series chain, and this
one does it on the pin layer in 30 fewer shapes because it needs no
vias. `route_stack_level` will not touch a stack whose pycell has
spoken.

WHAT IT DOES NOT DO IS DRAW. An earlier version called
MazeRouter.connect() and emitted rects and cut instances itself, and it
looked exactly like what it was -- a hand stitched wire down the middle
of the column, one segment at a time, ignoring the alignment and cut
placement route.py applies to everything else in the cell.

The chain is a series ladder: each link joins the drain of one device to
the source of the device below it, one row apart. So every link is a
LEFT route on the pin layer -- "-|--" -- which puts the trunk left of
the pins and left aligns the cuts on them, and that is the shape the
sources want.
"""
import logging

log = logging.getLogger("LELOTEMP_OTAR_P_SW")

#- The pin layer. A link inside a column has both its pins on it
#- already, so this costs no via and no landing pad. Taken from the
#- technology rather than named, so this is not a route for one PDK.
#- via TrackMap, not Rules.get: Rules.get("ROUTE", "pinlayer") returns
#- the value once per layer in the technology, so it comes back as
#- "M1M1M1..." and the route silently asks for a layer that does not
#- exist. TrackMap already resolves it to one name.
def _pin_layer(layout):
    from cicpy.core.trackmap import TrackMap
    return TrackMap(layout).pin_layer


def route(layout, entry):
    """Route what is internal to this stack, through route.py.

    `layout` is the parent the stack was cut from and `entry` its plan.
    The parent is needed because the node graph lives there: the stack
    holds the instances but not the netlist.
    """
    import re
    from cicpy.core.subcell import stack_groups

    internal = list(entry["internal"])
    if not internal:
        return

    layer = _pin_layer(layout)
    if layer is None:
        log.warning("no ROUTE.pinlayer in the technology; not routing")
        return

    grp = stack_groups(layout).get(entry["stack"])
    if grp is None:
        log.warning(f"no group for stack {entry['stack']}; not routing")
        return

    #- LEFT, so the trunk sits left of the column and the cuts land left
    #- aligned on the source pins. route.py picks the trunk from the
    #- net's own rects, and for a one row link that is a short trunk
    #- beside the two pins rather than a spine down the column.
    for net in internal:
        grp.addConnectivityRoute(layer, f"^{re.escape(net)}$", "-|--")
    log.info(f"internal nets: {len(internal)} routed on {layer} (-|--)")

    #- VCP is every gate in the column: the tabs share the right lane
    #- (306800..310000) and there is no foreign tab in it, so one M2
    #- rail with a cut per tab takes the whole net. xbs8's drain is
    #- the diode variant's internal tie, so the rail covers it too.
    #- The ladder bottom's source is VDD and the guard-connection
    #- strap is banned here: measured, its li path merges the whole
    #- cell into one net. A metal hop from the S strap to xbs6's own
    #- VDD edge pin, cuts filling both accesses, stays out of the li.
    #- The ladder bottom's source is VDD: an L on the layer above the
    #- pins, from the source strap to xbs6's own VDD edge pin.
    layout.addConnectivityRoute("M2", "^VDD_1V8$", "-|--", "",
                                1, "", r"^xbs6$")

    i = layout.getInstanceFromInstanceName("xbs6")
    #- rightmost narrow rect: duplicate subports put a false tab 6000
    #- left, and a rail there ties the ladder nets together.
    cands = [r for r in i.findRectanglesByNode("^VCP$", None)
             if r.x2 - r.x1 <= 4000]
    tab = max(cands, key=lambda r: r.x1)
    layout.addConnectivityRoute("M1", "^VCP$", "||", f"trunkx={int(tab.x1) + 1600}",
                                1, "", r"^xbs\d+$")
