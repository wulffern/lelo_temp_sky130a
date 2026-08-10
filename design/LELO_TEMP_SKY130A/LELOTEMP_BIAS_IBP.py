"""LELOTEMP_BIAS_IBP: the declarative sidecar.

The bias block: a ladder of pmos current sources (gate LPI) beside a
ladder of pmos cascodes (gate VCP), a 6-segment poly resistor chain,
the bipolar core, the regulating OTA (LELOTEMP_OTAR, a finished
cell), startup, a decap column and the MiM caps.

The two pmos ladders declare the SAME order so every source-cascode
link (VBD1, VBD2, IBD<3:0>) crosses between adjacent columns:

    p_src (bottom to top): xca3<0..3>  xca2   xca1<0..7>
    p_cas (bottom to top): xca2<0..3>  xca4   xca5<0..7>
    nets:                  IBD<0..3>   VBD2   VBD1

IBD drains sit at the BOTTOM of both columns, nearest the mid
channel their nets cross through.

The caps are MiM (M3 bottom plate A, M4 top plate B) -- no
diffusion, columns routed by their own hooks on M3/M4.
"""
import logging

from cicpy.sidecar import SidecarCell, Stack
from cicpy.core.sidecarcell import HierLayoutCell

log = logging.getLogger("LELOTEMP_BIAS_IBP")


class BiasHier(HierLayoutCell):
    """The assembled top, plus the seam nets the channels cannot say.

    The source-cascode links (VBD1, VBD2, IBD<3:0>) pair pins at
    MATCHED heights across the abutted src/cas seam -- the two
    ladders declare the same order for exactly this. Routed as plain
    horizontals on M4 (magic metal3): each net is one hop at its own
    row, so nothing shares an x, where mid-channel drops stacked all
    six verticals on one column x and shorted (measured).
    """

    def route(self):
        #- L-shapes, not straights: a D pin and an S pin sit at
        #- different heights WITHIN the cell (0.8 um here), and a
        #- straight wire at the start pin's y puts the far cut just
        #- off the far pin, onto whatever li lies between the rows
        #- (measured: five nets merged through exactly that)
        for net in ("IBD<0>", "IBD<1>", "IBD<2>", "IBD<3>", "VBD1"):
            self.addConnectivityRoute("M4", f"^{net}$", "-|--", "",
                                      1, "", "")
        #- cutalignright: the default cut pad grazed the cell's own
        #- mcon at the far pin (met1.2/mcon.2 slivers, measured)
        self.addConnectivityRoute("M4", "^VBD2$", "-|--",
                                  "cutalignright", 1, "", "")
        #- VD1 enters p_cas by a seam hop from p_su, NOT by a channel
        #- drop: the drop's vertical would run the drain window and
        #- clip the IBP pin stacks (its discovered drop is skipped)
        self.addConnectivityRoute("M4", "^VD1$", "-|--",
                                  "cutalignright", 1, "",
                                  r"^(xp_cas|xp_su)$")
        super().route()


def _rail(stack, net, layer, widthmult=3, inset=5000):
    """A plain bar down the column, joining every member's plate.

    The same mechanism as the dummy straps: geometry owned by the
    stack. Computed from the INSTANCE boxes -- the port rects a
    stack carries are captured at netlist read and go stale when the
    floorplan moves the column (measured: a pin-derived bar landed a
    full millimetre above the caps). For the MiM columns the plates
    span the cell, so a vertical bar over the column IS the
    connection -- no cuts, no router. ``inset`` keeps the bar ends
    on the end members' plates.
    """
    from cicpy.core.rect import Rect
    from cicpy.core.rules import Rules
    insts = stack.instances
    if len(insts) < 2:
        log.warning(f"_rail {stack.name}/{net}: only {len(insts)} members")
        return None
    w = Rules.getInstance().get(layer, "width") * widthmult
    x = (min(int(i.x1) for i in insts) + max(int(i.x2) for i in insts)) / 2
    y1 = min(int(i.y1) for i in insts) + inset
    y2 = max(int(i.y2) for i in insts) - inset
    bar = Rect(layer, int(x - w / 2), int(y1), int(w), int(y2 - y1))
    bar.setNet(net)
    stack.layout.add(bar)
    stack.layout.detachPlacementChild(bar, keepParent=stack)
    stack.add(bar)
    stack.dummy_routes.append(bar)
    log.info(f"_rail {stack.name}/{net}: {layer} bar "
             f"{bar.x1},{bar.y1}..{bar.x2},{bar.y2}")
    return bar


class LELOTEMP_BIAS_IBP(SidecarCell):

    place = {"groupbreak": 3, "channel": 6}

    #- row 0 -----------------------------------------------------

    class bip(Stack):
        """The bipolar core, a finished cell of its own."""
        match = r'^xe1$'
        group = "bip"
        fill = False
        order = ['xe1']

    class r_lad(Stack):
        """VR1 -> R1<4:0> -> VD2, bottom to top follows the chain."""
        match = r'^(xd3<\d+>|xstack_r_lad_(top|bot))$'
        group = "res"
        channel = "res"
        fill = False
        order = [r'xd3<\d+>']

    class n_g(Stack):
        """xg1: nmos diode VR1 -> VD2."""
        match = r'^(xg1|xstack_n_g_(top|bot)|xfill_n_g_\d+)$'
        group = "nmos"
        xspace = 2
        order = ['xg1']

    #- row 1 -----------------------------------------------------

    class ota(Stack):
        """LELOTEMP_OTAR, placed as the finished cell it is."""
        match = r'^xad6$'
        group = "ota"
        fill = False
        order = ['xad6']

    class p_src(Stack):
        """Current sources: drains VBD1 x8, VBD2, IBD<3:0>; the one
        rail is VBD1 over the xca1 drains, the gate rail is LPI on
        the tab lane."""
        match = r'^(xca1<\d+>|xca2|xca3<\d+>|xstack_p_src_(top|bot)|xfill_p_src_\d+)$'
        group = "pmos"
        channel = "src"
        order = ['xca2', r'xca3<\d+>', r'xca1<\d+>']

        def beforeRoute(self, entry):
            conn = self.layout.addConnectivityRoute
            conn("M1", "^VBD1$", "||", "trunkright,nostartcut,noendcut",
                 1, "", r"^xca1<\d+>$")
            conn("M2", "^LPI$", "||", "trunktab",
                 1, "", r"^(xca1<\d+>|xca2|xca3<\d+>)$")
            return None

    class p_cas(Stack):
        """Cascodes: sources VBD1 x8, VBD2, IBD<3:0>; drains VD1 x8,
        VR1, IBP_1U<3:0>; common gate VCP on the tab lane."""
        match = r'^(xca2<\d+>|xca4|xca5<\d+>|xstack_p_cas_(top|bot)|xfill_p_cas_\d+)$'
        group = "pmos"
        channel = "cas"
        order = ['xca4', r'xca2<\d+>', r'xca5<\d+>']

        def beforeRoute(self, entry):
            conn = self.layout.addConnectivityRoute
            conn("M1", "^VD1$", "||", "trunkright,nostartcut,noendcut",
                 1, "", r"^xca5<\d+>$")
            conn("M1", "^VBD1$", "||", "trunkleft,nostartcut,noendcut",
                 1, "", r"^xca5<\d+>$")
            conn("M2", "^VCP$", "||", "trunktab",
                 1, "", r"^(xca2<\d+>|xca4|xca5<\d+>)$")
            return None

    class p_su(Stack):
        """Startup: xsu1 diode from VDD, xsu2 diode VD1 -> VSU."""
        match = r'^(xsu\d+|xstack_p_su_(top|bot)|xfill_p_su_\d+)$'
        group = "pmos"
        channel = "su"
        order = ['xsu1', 'xsu2']

        def beforeRoute(self, entry):
            #- VSU: xsu1's tied bar to xsu2's source, adjacent rows;
            #- the L-shape lands the cut on each pin's own overlap
            from cicpy.core.trackmap import TrackMap
            layer = TrackMap(self.layout).pin_layer
            if layer is None:
                return None
            self.addConnectivityRoute(layer, "^VSU$", "-|--")
            return None

    class p_cc(Stack):
        """Decap column: every terminal on VDD_1V8, one strap."""
        match = r'^(xcc<\d+>|xstack_p_cc_(top|bot)|xfill_p_cc_\d+)$'
        group = "pmos"
        channel = "cc"
        order = [r'xcc<\d+>']

        def beforeRoute(self, entry):
            #- the decaps are netlist-real supply devices: exactly
            #- the dummy treatment, straps + a finger into the taps
            self.routeSupplyDevices(self.instances)
            return True

    class cap_lpi_a(Stack):
        match = r'^xd1<[0-4]>$'
        group = "cap"
        fill = False
        order = [r'xd1<[0-4]>']

        def beforeRoute(self, entry):
            #- cicpy layers sit one above the magic names: M4 is
            #- magic metal3, the MiM bottom plate; M5 is metal4, the
            #- top plate. A bar per plate down the column.
            _rail(self, "LPI", "M4")
            _rail(self, "VDD_1V8", "M5")
            return True

    class cap_lpi_b(Stack):
        match = r'^xd1<[5-9]>$'
        group = "cap"
        fill = False
        order = [r'xd1<[5-9]>']

        def beforeRoute(self, entry):
            #- cicpy layers sit one above the magic names: M4 is
            #- magic metal3, the MiM bottom plate; M5 is metal4, the
            #- top plate. A bar per plate down the column.
            _rail(self, "LPI", "M4")
            _rail(self, "VDD_1V8", "M5")
            return True

    class cap_vcp(Stack):
        match = r'^xd2<\d+>$'
        group = "cap"
        fill = False
        order = [r'xd2<\d+>']

        def beforeRoute(self, entry):
            #- cicpy layers sit one above the magic names: M4 is
            #- magic metal3, the MiM bottom plate; M5 is metal4, the
            #- top plate. A bar per plate down the column.
            _rail(self, "VCP", "M4")
            _rail(self, "VDD_1V8", "M5")
            return True

    #- the OTA stands at the RIGHT end of its row: its VSS port is a
    #- full-width bar that addPowerConnection stretches straight down
    #- to the bottom ring, and that corridor must hold nothing --
    #- over row 0 it shorted the nmos diode's li tabs (measured)
    rows = [
        [bip, n_g, r_lad],
        [p_src, p_cas, p_su, p_cc, cap_lpi_a, cap_lpi_b, cap_vcp, ota],
    ]

    supplies = [
        {"net": "VDD_1V8", "ring": "t", "strap": "top",
         "guard_exclude": r"^(xe1|xg1|xd3<\d+>|xd1<\d+>|xd2<\d+>|xad6)$"},
        {"net": "VSS", "ring": "b", "strap": "bottom",
         "strap_exclude": r"^(xd3<[1-9]|xad6|xd1|xd2|xe1)",
         "guard_exclude": r"^(xca|xsu|xcc|xd1<\d+>|xd2<\d+>|xad6|xfill_p)"},
    ]

    #- the assembled top: BiasHier (hier_cell) does the placement and
    #- adds the src/cas seam nets; the mid channel carries the nets
    #- that genuinely cross rows, one track each. Where two nets'
    #- pins share a column x, the drops split by align and layer
    #- (bip: VD1 center pnp vs VD2 ring; r_lad: chain ends).
    #- The IBP_1U outputs leave their column on four VERTICAL
    #- channel routes -- M5 bars on su-channel tracks, horizontal M4
    #- drops, so four nets from one column never share an x.
    hier_cell = BiasHier
    channel = 12
    routes = [
        {"net": "VD2", "track": 0, "drops": [[bip, "M2", "right"],
                                             [r_lad, "M2", "left"]]},
        {"net": "VR1", "track": 2, "drops": [[r_lad, "M4", "right"]]},
        {"net": "VD1", "track": 4, "drops": [[bip, "M4", "left"],
                                             {"inst": p_cas, "skip": True}]},
        {"net": "VCP", "track": 6},
        {"net": "LPI", "track": 8},
        {"net": "IBP_1U<0>", "channel": "su", "track": 6,
         "bar_layer": "M5", "layer": "M4", "align": "top"},
        {"net": "IBP_1U<1>", "channel": "su", "track": 10,
         "bar_layer": "M5", "layer": "M4", "align": "top"},
        {"net": "IBP_1U<2>", "channel": "su", "track": 14,
         "bar_layer": "M5", "layer": "M4", "align": "top"},
        {"net": "IBP_1U<3>", "channel": "su", "track": 18,
         "bar_layer": "M5", "layer": "M4", "align": "top"},
    ]
