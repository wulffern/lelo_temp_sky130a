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

The caps are MiM. cicpy's layer names sit one above magic's: the
bottom plate (pin A) is cicpy M4 = magic metal3, the top plate (pin B)
is cicpy M5 = magic metal4. No diffusion -- each column is a plain bar
per plate, drawn by the stack's own hook with `plateRail`.
"""
import logging

from cicpy.sidecar import SidecarCell, Stack

log = logging.getLogger("LELOTEMP_BIAS_IBP")


#- The `wires` blocks below are ROUTER-GENERATED, pasted from the
#- build's .routes.py. Each 4-tuple is ordinary addConnectivityRoute
#- arguments and can be edited like any other route; a ("net",
#- "blocked", reason) triple records a search that proved unroutable,
#- so replay reproduces the outcome instead of retrying it. The
#- options are resolved against a placement, so `wires_key`
#- fingerprints the stack's instances -- on a mismatch the whole block
#- is ignored, loudly, and the router searches afresh and prints a new
#- one. A stack whose beforeRoute returns True is claimed ENTIRELY and
#- never consults its wires, so those stacks carry none.


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
        wires = [
            ('VSS', 'blocked', "no path for VSS from (1040900, 1098000, 'M1') to (1040900, 1138000, 'M1'); closest approach (1040900, 1098000, 'M1') (40000 away)"),
            ('R1<0>', 'M1', '||', 'trunktab'),
            ('R1<1>', 'M1', '||', 'trunktab'),
            ('R1<2>', 'M1', '||', 'trunktab'),
            ('R1<3>', 'M1', '||', 'trunktab'),
            ('R1<4>', 'M1', '||', 'trunktab'),
        ]
        wires_key = "6dad32574c7a"

    class n_g(Stack):
        """xg1: nmos diode VR1 -> VD2."""
        match = r'^(xg1|xstack_n_g_(top|bot)|xfill_n_g_\d+)$'
        group = "nmos"
        xspace = 2
        order = ['xg1']
        wires = [
            ('VR1', 'blocked', "VR1: trunk 1005900 lies outside the pins' common overlap 1017700..1020900"),
        ]
        wires_key = "a123dc0963bc"

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
        wires = [
            ('VDD_1V8', 'M2', '-|--', 'trunktab'),
            ('LPI', 'M1', '||', 'trunktab'),
            ('VBD1', 'blocked', "path for VBD1 is not a shape route.py can draw (13 nodes, layers ['M1', 'M2'])"),
        ]
        wires_key = "a295e31e2fcc"

        def beforeRoute(self, entry):
            conn = self.layout.addConnectivityRoute
            conn("M1", "^VBD1$", "||", "trunkright,nostartcut,noendcut",
                 2, "", r"^xca1<\d+>$")
            conn("M2", "^LPI$", "||", "trunktab",
                 2, "", r"^(xca1<\d+>|xca2|xca3<\d+>)$")
            return None

    class p_cas(Stack):
        """Cascodes: sources VBD1 x8, VBD2, IBD<3:0>; drains VD1 x8,
        VR1, IBP_1U<3:0>; common gate VCP on the tab lane."""
        match = r'^(xca2<\d+>|xca4|xca5<\d+>|xstack_p_cas_(top|bot)|xfill_p_cas_\d+)$'
        group = "pmos"
        channel = "cas"
        order = ['xca4', r'xca2<\d+>', r'xca5<\d+>']
        wires = [
            ('VDD_1V8', 'blocked', "no path for VDD_1V8 from (479200, 1470000, 'M1') to (479200, 1510000, 'M1'); closest approach (479200, 1470000, 'M1') (40000 away)"),
            ('VBD1', 'M1', '||', 'trunkleft'),
            ('VCP', 'M1', '||', 'trunktab'),
            ('VD1', 'blocked', "path for VD1 is not a shape route.py can draw (15 nodes, layers ['M1', 'M2'])"),
        ]
        wires_key = "caa71805a52e"

        def beforeRoute(self, entry):
            conn = self.layout.addConnectivityRoute
            conn("M1", "^VD1$", "||", "trunkright,nostartcut,noendcut",
                 2, "", r"^xca5<\d+>$")
            conn("M1", "^VBD1$", "||", "trunkleft,nostartcut,noendcut",
                 2, "", r"^xca5<\d+>$")
            conn("M2", "^VCP$", "||", "trunktab",
                 2, "", r"^(xca2<\d+>|xca4|xca5<\d+>)$")
            return None

    class p_su(Stack):
        """Startup: xsu1 diode from VDD, xsu2 diode VD1 -> VSU."""
        match = r'^(xsu\d+|xstack_p_su_(top|bot)|xfill_p_su_\d+)$'
        group = "pmos"
        channel = "su"
        order = ['xsu1', 'xsu2']
        wires = [
            ('VDD_1V8', 'blocked', "no path for VDD_1V8 from (595200, 1854000, 'M1') to (559200, 1870000, 'M1'); closest approach (559200, 1870000, 'M3') (0 away)"),
            ('VD1', 'blocked', "VD1: trunk 604200 lies outside the pins' common overlap 612800..616000"),
            ('VSU', 'blocked', 'VSU: pins share only -9600 of column, a straight vertical cannot land'),
        ]
        wires_key = "095b78be0d58"

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
            self.plateRail("LPI", "M4")
            self.plateRail("VDD_1V8", "M5")
            return True

    class cap_lpi_b(Stack):
        match = r'^xd1<[5-9]>$'
        group = "cap"
        fill = False
        order = [r'xd1<[5-9]>']

        def beforeRoute(self, entry):
            self.plateRail("LPI", "M4")
            self.plateRail("VDD_1V8", "M5")
            return True

    class cap_vcp(Stack):
        match = r'^xd2<\d+>$'
        group = "cap"
        fill = False
        order = [r'xd2<\d+>']

        def beforeRoute(self, entry):
            self.plateRail("VCP", "M4")
            self.plateRail("VDD_1V8", "M5")
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

    #- the assembled top: the rows above are the floorplan and
    #- route() below adds the src/cas seam nets; the mid channel
    #- carries the nets that genuinely cross rows, one track each.
    #- Where two nets' pins share a column x, the drops split by
    #- align and layer (bip: VD1 center pnp vs VD2 ring; r_lad: chain
    #- ends). The IBP_1U outputs leave their column on four VERTICAL
    #- channel routes -- M5 bars on su-channel tracks, horizontal M4
    #- drops, so four nets from one column never share an x.
    #- Declaring `routes` is what tells cicpy this cell is MADE OF
    #- SUBCELLS: it splits the netlist, builds a cell per part and
    #- assembles them.
    #- headroom the TT 1x1 tile (111.52 um tall) cannot afford
    channel = 6
    routes = [
        {"net": "VD2", "track": 0, "drops": [[bip, "M2", "right"],
                                             [r_lad, "M2", "left"]]},
        {"net": "VR1", "track": 1, "drops": [[r_lad, "M4", "right"]]},
        #- trim "l": VD1 carries net VC in the parent, and its bar's
        #- untrimmed right end IS the parent's pin, at the cell edge
        {"net": "VD1", "track": 2, "trim": "l",
         "drops": [[bip, "M4", "left"],
                   {"inst": p_cas, "skip": True}]},
        {"net": "VCP", "track": 3},
        {"net": "LPI", "track": 4, "trim": "l"},
        {"net": "IBP_1U<0>", "channel": "su", "track": 3,
         "bar_layer": "M5", "layer": "M4", "align": "top",
         "trim": "b"},
        {"net": "IBP_1U<1>", "channel": "su", "track": 5,
         "bar_layer": "M5", "layer": "M4", "align": "top",
         "trim": "b"},
        {"net": "IBP_1U<2>", "channel": "su", "track": 7,
         "bar_layer": "M5", "layer": "M4", "align": "top",
         "trim": "b"},
        {"net": "IBP_1U<3>", "channel": "su", "track": 9,
         "bar_layer": "M5", "layer": "M4", "align": "top",
         "trim": "b"},
    ]

    #def beforeRoute(self):
        #- L-shapes, not straights: a D pin and an S pin sit at
        #- different heights WITHIN the cell (0.8 um here), and a
        #- straight wire at the start pin's y puts the far cut just
        #- off the far pin, onto whatever li lies between the rows
        #- (measured: five nets merged through exactly that)
     #   for net in ("IBD<0>", "IBD<1>", "IBD<2>", "IBD<3>", "VBD1"):
      #      self.addConnectivityRoute("M4", f"^{net}$", "-|--", "",
       #                               1, "", "")
        #- LEFT-aligned, which is the default: the pin is 22.4 um of
        #- li and the cut lands at its left end, 6.5 um clear of VR1's
        #- trunk. cutalignright puts it at the RIGHT end, on top of
        #- VR1. It used to be here because the landing rect was
        #- recentred whatever the alignment said, so the option was
        #- picked for a side effect it no longer has.
       # self.addConnectivityRoute("M4", "^VBD2$", "-|--",
        #                          "", 1, "", "")
        #- VD1 enters p_cas by a seam hop from p_su, NOT by a channel
        #- drop: the drop's vertical would run the drain window and
        #- clip the IBP pin stacks (its discovered drop is skipped)
        #self.addConnectivityRoute("M4", "^VD1$", "-|--",
        #                          "cutaligncenter,endStopLayerM2", 2, "",
        #                          r"^(xp_cas|xp_su)$")


    def route(self):
        """The assembled top, plus the seam nets the channels cannot say.

        The source-cascode links (VBD1, VBD2, IBD<3:0>) pair pins at
        MATCHED heights across the abutted src/cas seam -- the two
        ladders declare the same order for exactly this. Routed as
        plain horizontals on M4 (magic metal3): each net is one hop at
        its own row, so nothing shares an x, where mid-channel drops
        stacked all six verticals on one column x and shorted
        (measured).

        These run BEFORE super(), which is the only ordering there is
        now: the subcells are built by hierarchy() long before this,
        and what these nets read is the assembly's own access rects.
        """
        #- L-shapes, not straights: a D pin and an S pin sit at
        #- different heights WITHIN the cell (0.8 um here), and a
        #- straight wire at the start pin's y puts the far cut just
        #- off the far pin, onto whatever li lies between the rows
        #- (measured: five nets merged through exactly that)
        for net in ("IBD<0>", "IBD<1>", "IBD<2>", "IBD<3>", "VBD1"):
            self.addConnectivityRoute("M4", f"^{net}$", "-|--", "",
                                      2, "", "")
        #- LEFT-aligned, which is the default: the pin is 22.4 um of
        #- li and the cut lands at its left end, 6.5 um clear of VR1's
        #- trunk. cutalignright puts it at the RIGHT end, on top of
        #- VR1. It used to be here because the landing rect was
        #- recentred whatever the alignment said, so the option was
        #- picked for a side effect it no longer has.
        self.addConnectivityRoute("M4", "^VBD2$", "-|--",
                                  "", 2, "", "")
        #- VD1 enters p_cas by a seam hop from p_su, NOT by a channel
        #- drop: the drop's vertical would run the drain window and
        #- clip the IBP pin stacks (its discovered drop is skipped)
        self.addConnectivityRoute("M4", "^VD1$", "-|--",
                                  "cutaligncenter,endStopLayerM2", 2, "",
                                  r"^(xp_cas|xp_su)$")
        #- the powerdown pins live deep in the OTA; the parent needs
        #- them at an edge. M5 risers from each pin straight up to the
        #- top -- nothing above the OTA carries M5. Every number in
        #- this (the cut, the intermediate pads, how far in from the
        #- bar's end to attach) comes from the technology; it used to
        #- be twenty lines of Rect and Cut with 2400, 5000 and a 1x1
        #- via typed into them.
        for net in ("PWRUP_1V8", "PWRUP_N_1V8"):
            self.promoteInstancePort(net, r"^xota$", "top", "M5",
                                     startLayer="M2")
        super().route()
