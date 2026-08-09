
import logging

log = logging.getLogger("LELOTEMP_OTAR_P_SW")


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

    layout.addConnectivityRoute("M1", "^VDD_1V8$", "-|--", "offsetlowend",
                                1, "", r"^xbs6$")
    layout.addConnectivityRoute("M1", "^VCP$", "||", "",1, "", r"^xbs\d+$")
