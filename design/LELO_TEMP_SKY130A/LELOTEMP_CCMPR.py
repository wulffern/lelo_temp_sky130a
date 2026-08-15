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
            self.layout._caps_ibp_rail = self.plateRail(
                "IBP_1U<0>", "M4", inset=20000)
            self.layout._caps_vss_rail = self.plateRail(
                "VSS", "M5", inset=20000)
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
        #- the band between the ground ring and the cells' base, which
        #- is where anything reaching the cap bank turns. Registered
        #- here rather than in afterPlace because the ring bounds it.
        rb = (layout.named_rects.get("rail_b_VSS")
              or layout.named_rects.get("ring_b_VSS"))
        if rb is not None:
            layout.addRoutingChannel("base", int(rb.y2), 0)
        super().beforeRoute(layout)

    #- NO ROUTES YET. The placement is verified on its own first, the
    #- way LELOTEMP_CMPR's was: the crossing nets go in one at a time,
    #- shortest first, each written as a path and checked for shorts
    #- before the next.
    routes = []
