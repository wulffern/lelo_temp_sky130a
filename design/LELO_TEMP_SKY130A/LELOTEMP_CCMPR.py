"""LELOTEMP_CCMPR: the comparator and its five caps.

Simpler than LELOTEMP_CCMP, which is otherwise the model: CCMP holds
the comparator, a two-device nmos pull (xg1 on RST, xg4 on PWRUP_N)
and the caps, and here the pull has moved INSIDE the comparator. So
this cell is the cap bank and LELOTEMP_CMPR, and nothing else.

The port list is CCMP's, exactly -- checked against the netlists:

    IBP_1U<1> IBP_1U<0> VDD_1V8 PWRUP_N_1V8 PWRUP_B_1V8 CMPO VC RST VSS

LELO_TEMP.sch is already swapped to this cell, and the top's seam
stories anchor on PWRUP_N_1V8 and PWRUP_B_1V8 where the core publishes
them, mid-row. Those two are not promoted to edges here for the same
reason CCMP does not promote them: the pair is assembled by
LELO_TEMP's `ccmp` subcell and all five seam nets lose their second end
if they move.

=====================================================================
THE CAPS GO BELOW, AND IN A ROW
=====================================================================

CCMP puts them beside the comparator, in a column. Beside costs WIDTH,
which is what this block has none of -- the tile gives it 41 um and the
comparator is already 34.96. Below costs HEIGHT, of which the tile has
28 um spare (LELO_TEMP.mag: xccmp 20200..28396 in a 21892 tile).

And in a ROW rather than a column, because the direction is now free:
five 2.70 um caps stacked cost 19 um of height, laid side by side they
cost 2.70. The row is 5 x 2.70 plus four 2 um gaps = 21.5 um, well
inside the comparator's own 34.96.

capm.11 is the rule to respect here: a MiM claims 1.34 um from
unrelated M4 and counts anything under its halo, so a bar running the
full width below the caps picks up the whole bank. Nothing is drawn
under them; the cap rail leaves from the plate and the supply ring is
kept clear of the halo.
"""
import logging

from cicpy.sidecar import SidecarCell, Stack

log = logging.getLogger("LELOTEMP_CCMPR")


class LELOTEMP_CCMPR(SidecarCell):

    place = {"groupbreak": 1, "channel": 6}

    class caps(Stack):
        """Five JNWTR_CAPX1 on IBP_1U<0>, side by side.

        `Stack` stacks in y and there is no horizontal form, so the
        row is laid here -- off the instances' own widths, so it holds
        for another cap cell and another technology.
        """
        match = r'^xd1<\d+>$'
        group = "caps"
        fill = False
        order = [r'xd1<\d+>']

        def beforePlace(self, entry):
            gap = 2 * self.layout.um
            insts = list(self.instances)
            if not insts:
                return
            x, y = int(insts[0].x1), int(insts[0].y1)
            for inst in insts:
                inst.moveTo(x, y)
                x = int(inst.x2) + gap
            self.updateBoundingRect()

        def beforeRoute(self, entry):
            #- cicpy layers sit one above the magic names: the JNWTR
            #- cap's A plate (magic m3) is M4, its B plate (magic m4)
            #- is M5. The old CCMP pycell railed IBP on M5 and shorted
            #- the pads into the VSS plates.
            #- direction="h": these five sit in a ROW, so the bar runs
            #- across them. The default vertical bar joined the middle
            #- cap to nothing and left the net in four components.
            self.layout._caps_ibp_rail = self.plateRail(
                "IBP_1U<0>", "M4", inset=20000, direction="h")
            self.layout._caps_vss_rail = self.plateRail(
                "VSS", "M5", inset=20000, direction="h")
            return True

    class cmp(Stack):
        """The finished comparator, straight up.

        NOT mirrored: setAngle("MY") on a placed instance leaves the
        instance PORT rects in a half-mirrored frame and every route
        aimed through them lands beside its pin (measured on CCMP).
        """
        match = r'^x1_cmp$'
        group = "cmp"
        fill = False
        order = ['x1_cmp']

    #- caps first: rows are bottom to top
    rows = [[caps], [cmp]]

    supplies = [{"net": "VDD_1V8", "strap": "top"},
                {"net": "VSS", "strap": "bottom"}]

    def beforeRoute(self, layout):
        """The rings, then the recipe.

        The supplies above carry no `ring`, so the assembly recipe
        straps to one but does not make one -- CCMP does the same and
        for the same reason: this cell wants its own ring geometry,
        wider on the ground side, and the recipe's is not it.
        """
        layout.addRouteRing("M1", "VDD_1V8", "t", widthmult=3,
                            spacemult=2)
        layout.addRouteRing("M1", "VSS", "b", widthmult=3, spacemult=5)
        #- and the connection to them. The `supplies` list above
        #- carries no `ring`, so the assembly recipe straps to a ring
        #- it does not make and does nothing at all here -- the rings
        #- are made by hand just above, so the connection is too.
        #- addPowerConnection is the right call for an assembly: what
        #- it stretches are the children's PUBLISHED supply rects,
        #- which are their guard columns and rings at the edges, not
        #- pins in the middle of a device row.
        layout.addPowerConnection("VDD_1V8", "", "top")
        layout.addPowerConnection("VSS", "", "bottom")
        #- the band between the ground ring and the cells' base, which
        #- is where anything reaching the cap bank turns. Registered
        #- here rather than in afterPlace because the ring bounds it.
        rb = (layout.named_rects.get("rail_b_VSS")
              or layout.named_rects.get("ring_b_VSS"))
        if rb is not None:
            layout.addRoutingChannel("base", int(rb.y2), 0)
        super().beforeRoute(layout)
        self._crossings(layout)

    @staticmethod
    def _port(inst, net):
        rs = [c.get() for c in getattr(inst, "children", []) or []
              if getattr(c, "name", "") == net and hasattr(c, "get")]
        rs = [r for r in rs if r is not None]
        return rs[0] if rs else None

    def _crossings(self, layout):
        """The nets that cross between the cap bank and the core.

        One at a time, shortest first, each checked for shorts before
        the next -- the way LELOTEMP_CMPR's seven were done.
        """
        caps = layout.getInstanceFromInstanceName("xcaps")
        cmp_i = layout.getInstanceFromInstanceName("xcmp")
        if None in (caps, cmp_i):
            log.error("CCMPR: the cap bank and the core are both needed")
            return

        #- IBP_1U<0>: the plate rail to the comparator's own input.
        #- ON M4, and up the DRAIN LANE. The comparator publishes this
        #- pin 13.7 um inside its own footprint, at the load column's
        #- row 2 -- but the net's own M4 vertical already runs down
        #- that column to y 139000 (cell frame), so arriving on M4 at
        #- the same x merges with it instead of crossing anything. The
        #- rows below are load0's VSS bar and the net's own two switch
        #- drains, and the subcell's only other M4 is PWRUP_N_1V8's
        #- rail over on the gate-tab lane.
        ci = self._port(caps, "IBP_1U<0>")
        ni = self._port(cmp_i, "IBP_1U<0>")
        if ci is not None and ni is not None:
            #- THE SAME CUT SHAPE THE CORE USED. LELOTEMP_CMPR lands
            #- this pin with cut_M1M4_1x2 -- one cut wide, two tall,
            #- because it is a gate tab -- and the default here is
            #- cut_M1M4_2x1, two wide and one tall. The two overlap
            #- PARTIALLY at the same pin, which is exactly what magic
            #- means by "this layer can't abut or partially overlap
            #- between subcells": not a spacing rule, a hierarchy one.
            p = layout.path("IBP_1U<0>", "M4", start=[ci], stop=[ni],
                            options="1cuts,2vcuts")
            p.start()
            p.movex(p.landing("x"))
            p.movey(p.landing("y"))
            p.end()

    #- ROUTES SO FAR. The placement is verified on its own first, the
    #- way LELOTEMP_CMPR's was: the crossing nets go in one at a time,
    #- shortest first, each written as a path and checked for shorts
    #- before the next.
    routes = []
