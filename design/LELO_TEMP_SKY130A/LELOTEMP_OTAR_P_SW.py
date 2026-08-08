"""Routing for the switch stack, on its own.

This file exists to make a point as much as to route a column: the five
ladder nets are a small local problem and were only ever a hard one
because they were being solved at the top, against the whole cell.

    net1..net5 are INTERNAL to this stack. Nothing above it can see
    them, nothing above it can collide with them, and nothing above it
    has to reserve a track for them.

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


def route(cell, layout, entry):
    """Route what is internal to this stack, through route.py.

    `cell` is the stack cell, `layout` the parent it was cut from, and
    `entry` its plan. The parent is needed because the node graph lives
    there: this cell holds the instances but not the netlist.
    """
    import re
    from cicpy.core.mazerouter import stack_groups

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
