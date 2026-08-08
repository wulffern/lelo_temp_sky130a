"""Routing for the switch stack, on its own.

This file exists to make a point as much as to route a column: the five
ladder nets are a small local problem and were only ever a hard one
because they were being solved at the top, against the whole cell.

    net1..net5 are INTERNAL to this stack. Nothing above it can see
    them, nothing above it can collide with them, and nothing above it
    has to reserve a track for them.

Whole-cell routing could place three of the five before the last two
were stranded by the geometry the first three had drawn. Scoped to this
stack the search has the room that whole-cell routing had already spent.
"""
import logging

log = logging.getLogger("LELOTEMP_OTAR_P_SW")

#- Room to leave around the stack when the track map is cut. Big enough
#- that a route may step outside the devices to get around one, small
#- enough that it cannot wander into the next column.
MARGIN = 8000


def _pins(layout, net, wanted, layer=None):
    """Pin rects of `net` belonging to instances in this stack."""
    g = layout.nodeGraph.get(net)
    if g is None:
        return []
    out = []
    for port in getattr(g, "ports", []):
        inst = getattr(port, "parent", None)
        name = getattr(inst, "instanceName", "") if inst else ""
        if name not in wanted:
            continue
        rect = port.get(layer) if (layer and hasattr(port, "get")) else (
            port.get() if hasattr(port, "get") else None)
        if rect is not None:
            out.append(rect)
    return out


def route(cell, layout, entry):
    """Route what is internal to this stack.

    `cell` is the stack cell, `layout` the parent it was cut from, and
    `entry` its plan. The parent is needed because the node graph lives
    there: this cell holds the instances but not the netlist.
    """
    from cicpy.core.trackmap import TrackMap
    from cicpy.core.mazerouter import MazeRouter, Blocked

    wanted = set(entry["instances"])
    internal = list(entry["internal"])
    if not internal:
        return

    #- the extent of this stack, and nothing else. This is the whole
    #- reason the ladder is routable here and was not at the top.
    rects = [r for net in (internal + list(entry["ports"]))
             for r in _pins(layout, net, wanted)]
    if not rects:
        log.warning("no pins found for this stack; not routing")
        return
    extent = (min(r.x1 for r in rects) - MARGIN,
              min(r.y1 for r in rects) - MARGIN,
              max(r.x2 for r in rects) + MARGIN,
              max(r.y2 for r in rects) + MARGIN)

    done = blocked = 0
    for net in internal:
        pins = _pins(layout, net, wanted)
        if len(pins) < 2:
            continue
        #- rebuilt per net: what was just drawn is an obstacle now
        tm = TrackMap(layout, block_pins=True, extent=extent).build()
        r = MazeRouter(tm, net)
        try:
            for a, b in zip(pins, pins[1:]):
                r.connect(cell, a, b)
                tm = TrackMap(layout, block_pins=True, extent=extent).build()
                r = MazeRouter(tm, net)
            done += 1
        except Blocked as e:
            blocked += 1
            log.warning(f"{net}: {e}")
    log.info(f"internal nets: {done} routed, {blocked} blocked")
