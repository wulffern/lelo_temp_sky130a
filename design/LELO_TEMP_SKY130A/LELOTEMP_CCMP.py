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
        mimcap is "unrelated metal3" to capm.11, and the plate's own
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

    #- rings and connections are hand-rolled below: the recipe's
    #- supply loop hardcodes strap geometry this cell does not want
    supplies = []

    def beforeRoute(self, layout):
        layout.addRouteRing("M1", "VDD_1V8", "t", widthmult=3,
                            spacemult=2)
        layout.addRouteRing("M1", "VSS", "b", widthmult=3, spacemult=5)
        layout.addPowerConnection("VDD_1V8", "", "top")
        layout.addPowerConnection("VSS", "", "bottom")
        #- PWRUP_N_1V8 by hand: an M4 bar at the cmp pin's own row
        #- (the core is routed up through M4; only M5 crosses it touching nothing, so M4 crosses it touching
        #- nothing), a cut at the pin, and a drop outside the core
        #- down to xg4's gate tab. The orthogonal route's via column
        #- at the gate reached into the core's tail drains (measured:
        #- three proxy ports on the extracted comparator).
        from cicpy.core.rect import Rect as _Rect
        from cicpy.core.cut import Cut as _Cut
        from cicpy.core.rules import Rules as _Rules
        i_cmp = layout.getInstanceFromInstanceName("x1_cmp")
        pw = i_cmp.instancePorts["PWRUP_N_1V8"].get()
        xg4 = layout.getInstanceFromInstanceName("xg4")
        gpin = xg4.instancePorts["PWRUP_N_1V8"].get()
        if None not in (pw, gpin):
            w4 = _Rules.getInstance().get("M5", "width")
            yb2 = int(pw.centerY())
            #- from the LEFT EDGE: the parent reaches PWRUP_N here,
            #- and the interior pin is unreachable from outside
            bar2 = _Rect("M5", 0, int(yb2 - w4),
                         int(gpin.x2), int(w4 * 2))
            bar2.setNet("PWRUP_N_1V8")
            layout.add(bar2)
            ct = (_Cut.getInstance(pw.layer, "M5", 1, 1)
                  or _Cut.getInstance("M5", pw.layer, 1, 1))
            if ct is not None:
                ct.moveCenter(int(pw.centerX()), yb2)
                layout.add(ct)
            v = _Rect(gpin.layer, int(gpin.x1), int(gpin.y2),
                      int(gpin.x2 - gpin.x1),
                      int(yb2 + w4 - gpin.y2))
            v.setNet("PWRUP_N_1V8")
            layout.add(v)
            ct2 = (_Cut.getInstance(gpin.layer, "M5", 1, 1)
                   or _Cut.getInstance("M5", gpin.layer, 1, 1))
            if ct2 is not None:
                ct2.moveCenter(int(gpin.centerX()), yb2)
                layout.add(ct2)
            #- the stacks' mid-level M4 pads alone are under the
            #- metal3 minimum area; one 0.5 um patch per stack
            for cx in (int(pw.centerX()), int(gpin.centerX())):
                pad = _Rect("M4", cx - 2500, yb2 - 2500, 5000, 5000)
                pad.setNet("PWRUP_N_1V8")
                layout.add(pad)
        #- IBP_1U<0> rides one M4 bar in the band between the VSS
        #- ring and the cells' bases, tapped from the cmp's input pin,
        #- the nmos drain trunk and the caps' A-plate rail. The old
        #- orthogonal route anchored a bar at the cmp's TOP for a pin
        #- on its BOTTOM edge, and its vertical sliced the whole core
        #- (measured: every diff pin on one net).
        xg1 = layout.getInstanceFromInstanceName("xg1")
        vin = i_cmp.instancePorts["IBP_1U<0>"].get()
        dpin = xg1.instancePorts["IBP_1U<0>"].get()
        abar = getattr(layout, "_caps_ibp_rail", None)
        rbv = layout.named_rects.get("rail_b_VSS")
        if None not in (vin, dpin, abar, rbv):
            w4 = _Rules.getInstance().get("M4", "width")
            #- hug the ring: at mid-band the bar sat 0.9 um
            #- under the first cap's mimcap (capm.11 wants 1.34)
            yb = int(rbv.y2) + 2 * _Rules.getInstance().get("M4", "width")
            c0 = layout.getInstanceFromInstanceName("xd1<0>")
            x_app = int(c0.x1) - 10000
            bar = _Rect("M4", int(vin.centerX() - w4),
                        int(yb - w4 // 2),
                        int(x_app + 2 * w4 - (vin.centerX() - w4)),
                        int(w4 * 2))
            bar.setNet("IBP_1U<0>")
            layout.add(bar)
            #- taps: a vertical on each pin's own layer down to the
            #- bar, a stack where the layers differ
            for pr in (vin, dpin):
                v = _Rect(pr.layer, int(pr.x1), int(yb - w4 // 2),
                          int(pr.x2 - pr.x1),
                          int(pr.y1 - yb + w4 // 2 + 100))
                v.setNet("IBP_1U<0>")
                layout.add(v)
                ct = (_Cut.getInstance(pr.layer, "M4", 1, 1)
                      or _Cut.getInstance("M4", pr.layer, 1, 1))
                if ct is not None:
                    ct.moveCenter(int(pr.centerX()), int(yb))
                    layout.add(ct)
            #- approach the column from the LEFT, never from below:
            #- any metal3 under the mimcap's halo is "unrelated" to
            #- capm.11 (measured three ways). A stub 1 um left of the
            #- cells climbs to the pin bar's own height and enters ON
            #- the pin bar, whose geometry the cap cell already owns.
            v = _Rect("M4", x_app, int(yb - w4 // 2), int(2 * w4),
                      int(c0.y1) + 3000 - int(yb - w4 // 2))
            v.setNet("IBP_1U<0>")
            layout.add(v)
            h = _Rect("M4", x_app, int(c0.y1),
                      int(abar.x2 - x_app), 3000)
            h.setNet("IBP_1U<0>")
            layout.add(h)
        #- the caps' VSS plate rail down onto the bottom ring: extend
        #- the bar into the ring band and stack through to its M1
        bar = getattr(layout, "_caps_vss_rail", None)
        rb = layout.named_rects.get("rail_b_VSS")
        if bar is not None and rb is not None:
            from cicpy.core.rect import Rect
            from cicpy.core.cut import Cut
            ext = Rect("M5", int(bar.x1), int(rb.y1),
                       int(bar.x2 - bar.x1), int(bar.y1 - rb.y1))
            ext.setNet("VSS")
            layout.add(ext)
            ct = (Cut.getInstance("M1", "M5", 2, 1)
                  or Cut.getInstance("M1", "M5", 1, 1))
            if ct is not None:
                ct.moveCenter(int((bar.x1 + bar.x2) // 2),
                              int(rb.centerY()))
                layout.add(ct)
        super().beforeRoute(layout)

        #- PWRUP_B to the BOTTOM edge: the pin sits at the core's
        #- right edge, so a stub on its own layer steps into the
        #- core-to-nmos gap and drops straight down -- no crossing of
        #- the PWRUP_N M5 bar that shares the pin row
        pb = i_cmp.instancePorts["PWRUP_B_1V8"].get()
        if pb is not None:
            w3 = _Rules.getInstance().get(pb.layer, "width")
            xg = int(pb.x2) + 12000
            hst = _Rect(pb.layer, int(pb.x1), int(pb.centerY() - w3),
                        xg - int(pb.x1) + 2 * w3, int(2 * w3))
            hst.setNet("PWRUP_B_1V8")
            layout.add(hst)
            vpb = _Rect(pb.layer, xg, 0, int(2 * w3),
                        int(pb.centerY() + w3))
            vpb.setNet("PWRUP_B_1V8")
            layout.add(vpb)

    def afterPorts(self, layout):
        layout.addPortOnEdge("M2", "RST", "bottom", "--|-",
                             "offset_track-4,track4")
