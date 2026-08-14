"""LELOTEMP_CCMP: the declarative sidecar.

A wrapper around the finished comparator: the LELOTEMP_CMP core
(mirrored, so its IBP pins face the branch), a two-device nmos
column (xg1 the reset switch, xg4 the powerdown pull), and five
JNWTR MiM caps on IBP_1U<0>.

Converted from the classic pycell of the same name; the escape
hatches carry what the declarations cannot say: the mirror and the
cap pitch in subcell beforePlace hooks, the power connections and
the two crossing routes in the cell's own beforeRoute (super() runs
the recipe's supply loop and the stack-level router).
"""
import logging

from cicpy.sidecar import SidecarCell, Stack

log = logging.getLogger("LELOTEMP_CCMP")


class LELOTEMP_CCMP(SidecarCell):

    place = {"groupbreak": 1, "channel": 6}

    class cmp(Stack):
        """The finished comparator, mirrored: its IBP pins then face
        the nmos column and the caps."""
        match = r'^x1_cmp$'
        group = "cmp"
        fill = False
        order = ['x1_cmp']

        #- NOT mirrored: setAngle("MY") on a placed instance leaves
        #- the instance PORT rects in a half-mirrored frame (measured:
        #- y at the pre-place origin, VC 480 off in x) and every route
        #- aimed through them lands beside its pin. Until the mirror
        #- transforms the ports correctly, the straight orientation is
        #- the one whose pins are where the model says.

    class n_g(Stack):
        """xg1 (RST pull of IBP_1U<0>) under xg4 (powerdown pull)."""
        match = r'^(xg\d+|xstack_n_g_(top|bot)|xfill_n_g_\d+)$'
        group = "nmos"
        xspace = 3
        order = ['xg1', 'xg4']

    class caps(Stack):
        """Five MiM caps on IBP_1U<0> at the 2 um pitch gap the cap
        cell's own spacing rules want. The A rail STARTS OVER the
        first mimcap (inset 2 um): a rail stub standing beside a
        mimcap is unrelated M4 to capm.11, and the plate's own
        continuity carries the net down to the pin bar."""
        match = r'^xd1<\d+>$'
        group = "caps"
        fill = False
        xspace = 3
        order = [r'xd1<\d+>']

        def beforePlace(self, entry):
            self.stack(ygap=2 * self.layout.um)

        def beforeRoute(self, entry):
            #- cicpy layers sit one above the magic names: the JNWTR
            #- cap's A plate (magic m3) is M4, its B plate (magic m4)
            #- is M5 -- the old pycell railed IBP on M5 and shorted
            #- the pads into the VSS plates (measured)
            self.layout._caps_ibp_rail = self.plateRail(
                "IBP_1U<0>", "M4", inset=20000)
            #- the VSS rail is finished off in the cell's beforeRoute,
            #- where the ring it must reach exists
            self.layout._caps_vss_rail = self.plateRail(
                "VSS", "M5", inset=20000)
            return True

    rows = [
        [cmp, n_g, caps],
    ]

    #- STRAPS FOR THE SUBCELLS, RINGS BY HAND HERE. An entry without
    #- `ring` does nothing at this level -- the assembly recipe only
    #- reads `ring` -- and everything at the subcell level, where the
    #- flat recipe guards and straps each stack. Which is exactly the
    #- split this cell wants: it does not want the recipe's ring
    #- geometry, and its pieces do want their own rails. As groups
    #- they got them from the parent's addPowerConnection reaching
    #- every published supply rect; as cells they have to be strapped
    #- where they are.
    supplies = [{"net": "VDD_1V8", "strap": "top"},
                {"net": "VSS", "strap": "bottom"}]

    #- EVERY DECLARED PIECE IS A CELL. The stacks above are written as
    #- classes like any other subcell, so they are built as cells with
    #- their own lifecycle and assembled here.
    #-
    #- IBP_1U<0> is what the three of them share -- the comparator's
    #- input, the reset pull's drain and the cap bank's plate -- and
    #- all three publish it within 30 um of the cell's base, so one
    #- bar in the band between the ring and the cells reaches every
    #- one. The drops are discovered: a subcell exposing the net gets
    #- one.
    #- THE BAR STOPS SHORT OF THE CAPS. A MiM claims 1.34 um from
    #- unrelated M4 (capm.11) and counts anything under its halo,
    #- so a bar running the cell's full width in the band below picks
    #- up the whole cap bank. The bank's drop is skipped here and told
    #- as a story instead -- west of the caps, then up and in on the
    #- pin bar the cap cell already owns.
    routes = [
        {"net": "IBP_1U<0>", "bar_layer": "M4", "channel": "base",
         "track": 0, "drops": [{"inst": "caps", "skip": True}]},
    ]

    def beforeRoute(self, layout):
        """Three subcells, and the nets that cross between them.

        WHAT THIS USED TO BE: 150 lines of Rect and Cut reaching into
        `x1_cmp`, `xg1`, `xg4` and `xd1<0>` by instance name and
        computing every coordinate off their pins. None of it could
        survive the hierarchy, because none of those instances belong
        to this cell any more -- they belong to the three cells it
        places.
        """
        layout.addRouteRing("M1", "VDD_1V8", "t", widthmult=3,
                            spacemult=2)
        layout.addRouteRing("M1", "VSS", "b", widthmult=3, spacemult=5)
        layout.addPowerConnection("VDD_1V8", "", "top")
        layout.addPowerConnection("VSS", "", "bottom")
        #- the band the channel route rides: between the ring just
        #- laid and the cells' base. Registered here rather than in
        #- afterPlace because the ring is what bounds it.
        rb = (layout.named_rects.get("rail_b_VSS")
              or layout.named_rects.get("ring_b_VSS"))
        if rb is not None:
            layout.addRoutingChannel("base", int(rb.y2), 0)
        #- and the gap between the pull and the cap bank, which is
        #- where anything reaching the caps has to turn
        n_g = layout.getInstanceFromInstanceName("xn_g")
        caps = layout.getInstanceFromInstanceName("xcaps")
        if None not in (n_g, caps):
            layout.addRoutingChannel("capgap", int(n_g.x2),
                                     int(caps.x1), horizontal=False)
        super().beforeRoute(layout)
        self._crossings(layout)

    @staticmethod
    def _port(inst, net):
        rs = [c.get() for c in getattr(inst, "children", []) or []
              if getattr(c, "isPort", lambda: False)()
              and getattr(c, "name", "") == net]
        rs = [r for r in rs if r is not None]
        return rs[0] if rs else None

    def _crossings(self, layout):
        """The nets a channel bar cannot carry.

        PWRUP_N crosses the comparator, not the band under it: its pin
        is at the core's own row and the pull's gate is 13 um lower.
        The core is routed through M4, so M5 is the one layer that
        crosses it touching nothing -- which the hand-drawn version
        found too, the hard way.

        The cap bank's VSS is its plate rail on M5 and the ring is M1
        in the band below, so that one is a drop.
        """
        cmp_i = layout.getInstanceFromInstanceName("xcmp")
        n_g = layout.getInstanceFromInstanceName("xn_g")
        caps = layout.getInstanceFromInstanceName("xcaps")
        rb = (layout.named_rects.get("rail_b_VSS")
              or layout.named_rects.get("ring_b_VSS"))
        if None in (cmp_i, n_g, caps, rb):
            log.error("CCMP: three subcells and a ring are needed")
            return

        a = self._port(cmp_i, "PWRUP_N_1V8")
        b = self._port(n_g, "PWRUP_N_1V8")
        if a is not None and b is not None:
            #- A PIN IS 3200 WIDE AND THE DEFAULT CUT IS 8800, so a
            #- stack centred on this pin reaches 4800 west, and the
            #- core's own M4 riser is 5200 away: met3.2 wants 3000 and
            #- got 2000. Turned on its side the same two cuts fit
            #- INSIDE the pin (the seam stories above this cell found
            #- the same thing), which leaves the pin's whole
            #- neighbourhood free -- for this net's clearance and for
            #- the pair's riser, which needs a lane beside the pin.
            p = layout.path("PWRUP_N_1V8", a.layer, start=[a], stop=[b],
                            options="1cuts,2vcuts")
            p.start()
            p.up("M5")
            p.movex(p.landing("x"))
            p.movey(p.landing("y"))
            p.down("M2")
            p.movex(p.landing("x"))
            p.end()

        #- the cap bank, from the LEFT and never from below
        ci = self._port(caps, "IBP_1U<0>")
        ni = self._port(n_g, "IBP_1U<0>")
        if ci is not None and ni is not None:
            p = layout.path("IBP_1U<0>", "M4", start=[ci], stop=[ni])
            p.start()
            p.movex(p.track("capgap", 2))
            p.movey(p.track("base", 0))
            p.end()

        #- NO STORY FOR THE CAP BANK'S VSS. Its plate rail is a
        #- published supply rect, and addPowerConnection above already
        #- stretches every one of those to the ring -- a second stack
        #- at the same x put four via layers 2400 from the first
        #- (via.2, via2.2, via3.2 and nine mcon.2).

    def afterPorts(self, layout):
        layout.addPortOnEdge("M2", "RST", "bottom", "--|-",
                             "offset_track-4,track4")
        #- PWRUP_N AND PWRUP_B STAY WHERE THEY ARE, in the middle
        #- of the core's own row. Promoting them to edges looked
        #- right when this cell was built alone -- but it is never
        #- built alone: the pair above it is assembled by LELO_TEMP's
        #- `ccmp` subcell, whose five seam stories anchor on these two
        #- pins where the core publishes them. Moved to the edges,
        #- all three seam nets lost their second end (measured).
