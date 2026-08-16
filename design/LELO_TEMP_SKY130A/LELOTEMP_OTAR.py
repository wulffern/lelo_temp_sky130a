"""LELOTEMP_OTAR: the declarative sidecar, and the WHOLE truth.

One class, one cell. Subcells are nested classes subclassing the
real placement groups (a Stack IS a StackGroup), so a hook's `self`
is the group that was actually built; the floorplan rows, supplies
and the assembled top's routes are declarations on the cell class
itself. cicpy executes it (cicpy/sidecar.py compiles the class,
cicpy/core/sidecarcell.py runs the recipe -- which this class
inherits, so any recipe hook can be overridden with super()).

Order matters twice here, and both were measured:
* every N stack puts its xns gate device at the BOTTOM, so the
  subcell's tab-lane rail spans the rows above it and the parent's
  powerdown via stack still lands on the tab;
* p_bias runs (xba1, xba8, xba2, xba6, xba7, xba3): xba8's gate
  tab lies below every PWRUP_1V8 tab, and VO's (xba8,xba2) and
  VBP's (xba6,xba7) drains both stay adjacent. orderByTerminalNet
  interleaved the gate tabs down the one lane, where no pair of
  rails can coexist.

Hooks run in the parent, between its afterPlace and beforeRoute,
with `entry` this subcell's plan:
    entry["instances"]  the instance names in this subcell
    entry["ports"]      its boundary nets
    entry["internal"]   nets wholly inside it
    entry["type"]       stack | diffpair | mirror, from the class
beforeRoute returns True to claim the subcell as ROUTED (the
built-in stack router leaves it alone), None to let the built-in
router handle whatever it will take. `self.addConnectivityRoute` is
group-scoped; `self.layout.addConnectivityRoute` is parent-scoped.
"""
import logging

from cicpy.core.path import (PITCH, SPACE, left_of_pins, pin,
                             right_of_pins, tab_lane, track)
from cicpy.sidecar import SidecarCell, Stack, Mirror

log = logging.getLogger("LELOTEMP_OTAR")


class LELOTEMP_OTAR(SidecarCell):

    place = {"groupbreak": 6, "channel": 6}

    class p_in_a(Stack):
        match = r'^(xbl4|xbl1<\d+>|xstack_p_in_a_(top|bot)|xfill_p_in_a_\d+)$'
        group = "pmos"
        channel = "in_a"
        order = ['xbl4', r'xbl1<\d+>']
        #- FOUR RAILS, each on the lane its own pins define. Was a
        #- router-generated `wires` block and a wires_key; the anchors
        #- are the same anchors, recomputed every build instead of
        #- fingerprinted.
        paths = [
            dict(net="VDD_1V8", layer="M1",
                 steps=[("trunk", tab_lane())]),
            dict(net="VD1", layer="M1",
                 steps=[("trunk", right_of_pins())]),
            dict(net="VIN", layer="M1",
                 steps=[("trunk", tab_lane())]),
            dict(net="VS", layer="M1",
                 steps=[("trunk", left_of_pins())]),
        ]

    class p_in_b(Stack):
        match = r'^(xbl5|xbl2<\d+>|xstack_p_in_b_(top|bot)|xfill_p_in_b_\d+)$'
        group = "pmos"
        channel = "in_b"
        order = ['xbl5', r'xbl2<\d+>']
        #- p_in_a's four, mirrored. VDD_1V8 is the one that differs:
        #- the search could not join its two pins inside this column
        #- and said so, and the reason it does not matter is the same
        #- one as everywhere else -- the supply reaches every source
        #- through the guard, on M1, and a rail in the column is a
        #- second path to a node that already has one.
        blocked = [
            ('VDD_1V8', "no path inside the column (the search's own "
                        "words: from (159200,446000) to (159200,486000), "
                        "closest approach 40000 away) -- and none is "
                        "wanted: the guard carries it"),
        ]
        paths = [
            dict(net="VD2", layer="M1",
                 steps=[("trunk", right_of_pins())]),
            dict(net="VIP", layer="M1",
                 steps=[("trunk", tab_lane())]),
            dict(net="VS", layer="M1",
                 steps=[("trunk", left_of_pins())]),
        ]

    class p_bias(Stack):
        """Route VBP and PWRUP_1V8, which the stack router declines.

        VO it routes itself once the rows are adjacent.

        Depends on the row order this class sets for its stack
        (xba1, xba2, xba8, xba6, xba7, xba3 bottom to top): VO's two
        drains are then adjacent, VBP's two drains are adjacent, and
        the gate-tab lane interleaving that made VBP and PWRUP_1V8
        mutually unroutable is gone -- VBP's tab span (xba8 to xba6)
        holds no PWRUP_1V8 tab, so VBP takes the lane on M2 and
        PWRUP_1V8 crosses it on M3, its via stacks' M2 pads all
        clear of VBP's wire.

        Drain rails sit in the bar window right of the VDD source
        straps (straps end 230000; 233200 keeps the 1700 gap; the
        shorter bars run to 236400). The tab lane is 239600..242800.
        """
        match = r'^(xba\d+|xstack_p_bias_(top|bot)|xfill_p_bias_\d+)$'
        group = "pmos"
        channel = "bias"
        order = ['xba1', 'xba8', 'xba2', 'xba6', 'xba7', 'xba3']
        #- VDD_1V8 the guard carries, as everywhere. PWRUP_1V8 and VBP
        #- the search could not SHAPE -- "not a shape route.py can
        #- draw", 47 and 15 nodes over three layers -- which is the
        #- fault a path exists to fix: a polyline needs no canned shape.
        #- They are still routed by the hook below rather than declared
        #- here, because each is several scoped rails and not one story.
        blocked = [
            ('VDD_1V8', 'the guard carries it; the search wanted a rail '
                        'from (278200,350000) to (239200,366000) and '
                        'the node is already tied'),
            ('PWRUP_1V8', 'routed by this class\'s beforeRoute, scoped '
                          'to xba2/xba3/xba7 -- the search returned 47 '
                          'nodes over three layers and no shape'),
            ('VBP', 'routed by this class\'s beforeRoute in two scoped '
                    'rails -- the search returned 15 nodes over three '
                    'layers and no shape'),
        ]

        #- VO: xba8 and xba2's drains, adjacent rows once `order` puts
        #- them there, one M1 rail on their right edge.
        paths = [
            dict(net="VO", layer="M1",
                 steps=[("trunk", right_of_pins())]),
        ]

        def beforeRoute(self, entry):
            conn = self.layout.addConnectivityRoute
            conn("M1", "^VBP$", "||", "trunkright,nostartcut,noendcut",
                 2, "", r"^(xba6|xba7)$")
            #- xba8's gate joins its drain pair on M4: the vertical
            #- rides the tab lane below the PWRUP_1V8 rail's span,
            #- and the far cut lands under the wire on xba7's bar,
            #- out in the window.
            conn("M4", "^VBP$", "-|--", "", 2, "", r"^(xba8|xba7)$")
            #- ONE cut, said twice and meant: a 2x1 pad does not
            #- fit beside the guard ring here
            conn("M2", "^PWRUP_1V8$", "||", "trunktab,1cuts",
                 1, "", r"^(xba2|xba3|xba7)$")
            return None

    class p_sw(Stack):
        match = r'^(xbs\d+|xstack_p_sw_(top|bot)|xfill_p_sw_\d+)$'
        group = "pmos"
        channel = "sw"
        order = ['xbs6', 'xbs1', 'xbs2', 'xbs4', 'xbs7', 'xbs8']
        #- Both are the hook's below, which claims the whole stack
        #- (`return True`). VCP is a LADDER -- 11 nodes on M1 and no
        #- canned shape -- and the hook draws it as one scoped rail per
        #- internal net rather than as one wire.
        blocked = [
            ('VDD_1V8', 'the guard carries it; the search wanted a rail '
                        'from (319200,406000) to (319200,446000), 40000 '
                        'short'),
            ('VCP', "routed by this class's beforeRoute -- the search "
                    "returned 11 nodes on M1 and no shape"),
        ]

        def beforeRoute(self, entry):
            """Route this stack's internal nets through route.py.

            Group-scoped: self IS the built stack, so the trunk is
            picked from the net's own rects inside the column.
            Returns True -- the ladder is this hook's, and the
            built-in router must not lay a second set of wires.
            """
            import re
            internal = list(entry["internal"])
            if not internal:
                return None

            from cicpy.core.trackmap import TrackMap
            layer = TrackMap(self.layout).pin_layer
            if layer is None:
                log.warning("no ROUTE.pinlayer in the technology; "
                            "not routing")
                return None

            #- LEFT, so the trunk sits left of the column and the
            #- cuts land left aligned on the source pins. For a one
            #- row link that is a short trunk beside the two pins
            #- rather than a spine down the column.
            for net in internal:
                self.addConnectivityRoute(layer, f"^{re.escape(net)}$",
                                          "-|--")
            log.info(f"internal nets: {len(internal)} routed on "
                     f"{layer} (-|--)")

            self.layout.addConnectivityRoute(
                "M1", "^VDD_1V8$", "-|--", "offsetlowend",
                2, "", r"^xbs6$")
            self.layout.addConnectivityRoute(
                "M1", "^VCP$", "||", "", 2, "", r"^xbs\d+$")
            return True

    class n_load_a(Stack):
        """VD1 mixes two pin shapes the stack router declines: the
        wide D bars (the diodes' bars plus xns1's shorter one) and
        the right-lane gate tabs (the diodes' G tie and xnd3's
        gate). No single vertical lands on all of them, so two do,
        and both are stated from the pins themselves -- no
        coordinates:

        - `trunkright` on the bar scope: the common overlap's right
          edge, so the rail lies on every bar including xns1's short
          one. Same layer as the pins, no cuts.
        - `trunktab` on the tab scope: centred on the rightmost
          narrow rect, which is the gate-tab lane.

        The two rails meet through the diodes' own bar-to-tab metal.
        """
        match = r'^(xnd1<\d+>|xnd3|xns1|xstack_n_load_a_(top|bot)|xfill_n_load_a_\d+)$'
        group = "nmos"
        order = ['xns1', r'xnd1<\d+>', 'xnd3']
        #- VSS BLOCKED, which is what its three sibling columns already
        #- said and what this one should have said all along. Its pins
        #- here are the SOURCE and BULK of every device -- read them:
        #- xns1, xnd1<0..3> and xnd3, S and B, and nothing else -- so
        #- the node is the supply and addPowerGuardConnection has
        #- already tied it, on M1, beside every source.
        #-
        #- It was ('VSS', 'M2', '-|--', 'trunktab'): the search asked
        #- to route every net, so it routed this one too, and the shape
        #- it found was the smallest dogleg that joined two of the pins.
        #- MEASURED while converting, by writing it as the rail it looks
        #- like (M2 trunk on the tab lane plus taps): PWRUP_N_1V8, VBP,
        #- VD1 and VSS merged into one component of 1953 rects, VBP
        #- opened, 17 DRC. A full-height rail on the gate-tab lane
        #- touches every gate tab it passes, which is the whole reason
        #- CMPR's PWRUP_N_1V8 flies on M4. The lesson is not about the
        #- layer: this net wanted no wire at all.
        blocked = [
            ('VSS', 'the guard carries it -- every pin on this net in '
                    'this column is a source or a bulk'),
        ]


    class n_load_b(Stack):
        """VD2 is n_load_a's VD1, one cell right -- see that class
        for the shape argument. Both rails are stated from the pins
        themselves, no coordinates: `trunkright` is the bar
        overlap's right edge (so the rail lies on xns2's shorter bar
        too), `trunktab` centres on the rightmost narrow rect, the
        gate-tab lane.
        """
        match = r'^(xnd2<\d+>|xnd4|xns2|xstack_n_load_b_(top|bot)|xfill_n_load_b_\d+)$'
        group = "nmos"
        order = ['xns2', r'xnd2<\d+>', 'xnd4']
        #- VSS as in n_load_a: sources and bulks, carried by the guard.
        blocked = [
            ('VSS', 'the guard carries it -- every pin on this net in '
                    'this column is a source or a bulk'),
        ]


    class n_mirr(Mirror):
        match = r'^(xnc0|xnc1<\d+>|xns4|xstack_n_mirr_(top|bot)|xfill_n_mirr_\d+)$'
        group = "nmos"
        order = ['xns4', 'xnc0', r'xnc1<\d+>']

        def beforeRoute(self, entry):
            """Route the mirror. A Mirror declines the built-in stack
            router (routeInternal), so what it needs is stated here;
            the nets are plain verticals once the pins are read:

            - VCP: the three xnc1 drains, adjacent rows, one M1 rail
              in the bar window right of the VSS straps (straps end
              217200; 220400 keeps the 1700 gap; bars run to
              223600).
            - VD3: the diode xnc0 and the gates of all three xnc1 --
              their tabs share the right lane (226800..230000), M2
              so the rail can cross xns4's PWRUP_N tab. Plus xnc0's
              bar to xns4's drain bar, adjacent rows, M1 in the same
              bar window (y-disjoint from the VCP rail at the same
              x).

            PWRUP_N and the ports are the tabs themselves.
            """
            conn = self.layout.addConnectivityRoute
            conn("M1", "^VCP$", "||", "trunkright,nostartcut,noendcut",
                 2, "", r"^xnc1<\d+>$")
            #- onTopR: keep the TAB cut of the diode, not its bar
            #- cut, so the rail's bottom stays above xns4's PWRUP_N
            #- tab -- the parent lands its powerdown via stack there.
            conn("M1", "^VD3$", "||", "trunktab,onTopR",
                 2, "", r"^(xnc0|xnc1<\d+>)$")
            conn("M1", "^VD3$", "||", "trunkright,nostartcut,noendcut",
                 2, "", r"^(xnc0|xns4)$")
            return None

    class r_deg(Stack):
        match = r'^(xd2<\d+>|xstack_r_deg_(top|bot)|xfill_r_deg_\d+)$'
        group = "res"
        channel = "res"
        fill = False
        order = [r'xd2<\d+>']
        blocked = [
            ('VSS', 'the guard carries it; the search wanted a rail '
                    'from (719200,34000) to (719200,74000), 40000 short'),
        ]
        #- R1<0>: the ladder tap, one M1 rail on the tab lane.
        paths = [
            dict(net="R1<0>", layer="M1",
                 steps=[("trunk", tab_lane())]),
        ]

    rows = [
        [n_load_a, n_load_b, n_mirr, r_deg],
        [p_in_a, p_in_b, p_bias, p_sw],
    ]

    #- pin_strap: this cell is an ASSEMBLY, so its ring reaches the
    #- subcells through their PUBLISHED supply rects, and that is
    #- addPowerConnection -- which is opt-in now, because on a library
    #- whose pins overhang their abutment box it drags the pin's layer
    #- across everything between. These children's do not overhang,
    #- and without this the ring is connected to nothing: measured,
    #- LVS went from "Circuits match uniquely" to "Top level cell
    #- failed pin matching".
    supplies = [
        {"net": "VDD_1V8", "ring": "t", "guard_exclude": "^xbs6$",
         "strap": "top", "pin_strap": True},
        {"net": "VSS", "ring": "b", "strap": "bottom",
         "strap_exclude": "^xd2<[1-9]", "pin_strap": True},
    ]

    #- The top, from the same declarations: rows reused, one track
    #- per net -- a channel track IS one legal lane now, so
    #- consecutive indices are consecutive lanes and nothing has to
    #- be counted in twos. Drops split by layer where pins share a
    #- column (the bias column: VDS M2, VO M4; VBP lands cutless on
    #- the subcell's own M4 pad), align left/center/right as the fine
    #- dial. Drops are discovered: every subcell exposing the net
    #- gets one, on the route's default layer M2, centered, two
    #- cuts. Entries below only override.
    channel = 8
    #- HOW THE PIECES ARE JOINED. What makes this cell MADE OF
    #- SUBCELLS -- cicpy splitting the netlist, building a cell per
    #- subcell and assembling them -- is the subcell classes above;
    #- `routes` only lays the nets that cross between them. Built
    #- flat this cell does not pass LVS.
    routes = [
        {"net": "VDS", "track": 0, "drops": [[r_deg, "M2", "left"]]},
        {"net": "VD1", "track": 1, "drops": [[p_in_a, "M2", "right"]]},
        {"net": "VO", "track": 2, "drops": [[p_bias, "M4", "left"]]},
        {"net": "VCP", "track": 5, "drops": [[n_mirr, "M2", "left"],
                                             [p_bias, "M2", "right"]]},
        {"net": "VD3", "track": 4, "drops": [[n_mirr, "M2", "right"],
                                             [p_in_a, "M2", "left"],
                                             [p_in_b, "M2", "left"]]},
        {"net": "VD2", "track": 5, "align": "right"},
        {"net": "VBP", "track": 6, "drops": [[n_load_a, "M2", "left"],
                                              [p_bias, "M4", "center",
                                               "nopin"]]},
        {"net": "VS", "track": 7, "layer": "M4",
         "drops": [[r_deg, "M4", "left"]]},
        {"net": "PWRUP_N_1V8", "track": 8, "layer": "M4",
         "align": "left", "drops": [[p_bias, "M2", "right"]]},
    ]

    def afterPorts(self, layout):
        """Put the inputs on the BOTTOM edge.

        VIN and VIP are the p_in gate tabs, and a subcell's tabs sit
        mid-cell: published as they fall, they leave the parent's
        pins ~10 um up inside a cell 13.7 um tall, so anything
        reaching them drives a trunk deep past the internals (that is
        where LELOTEMP_BIAS_IBP's met1.2 sites came from). On the
        edge they are reachable from outside without entering.

        cicpy M2 is magic metal1 -- the layer the row above is
        already crossed on, so the drop is a straight vertical.
        """
        for net in ("VIN", "VIP"):
            layout.addPortOnEdge("M2", net, "bottom", "||", "offset_track+1")
