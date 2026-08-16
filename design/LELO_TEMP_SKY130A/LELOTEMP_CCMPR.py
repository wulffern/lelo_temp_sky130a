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

    #- the gap between the cap row and the core. `place: channel` is
    #- the FLAT recipe's knob and does nothing here -- placeHier reads
    #- this one, and its default 8 um is what left the two so far
    #- apart. capm.11 is the floor: a MiM claims 1.34 um from
    #- unrelated M4, so the gap cannot close past that.
    channel = 2

    supplies = [{"net": "VDD_1V8", "strap": "top"},
                {"net": "VSS", "strap": "bottom"}]

    #- (net, layer, x of the descent lane relative to the core, edge)
    _EDGE_PORTS = [
        #- WHICH EDGE IS DECIDED BY THE MIRROR ABOVE, NOT BY THE PIN.
        #- LELO_TEMP stacks two of these and mirrors the LOWER one MX,
        #- so that the two CAP BANKS meet at the seam -- they are the
        #- matched pair's matched element and they belong beside each
        #- other. The caps live at this cell's BOTTOM, so it is the
        #- two BOTTOM edges that meet at the seam and the two TOP
        #- edges that become the pair's outer faces.
        #-
        #- Which inverts the rule from the first arrangement: a net
        #- that is SHARED between the halves wants the BOTTOM edge --
        #- its two pads come out adjacent at the seam -- and a net
        #- that is PER-HALF (RST_A/RST_B, CMPO_A/CMPO_B upstairs)
        #- wants the TOP, where the level above can still see it.
        ("RST", "M2", 170000, "top"),
        #- VC is the shared one: to the seam, which is now the bottom.
        ("VC", "M2", 264000, "bottom"),
        #- CMPO is per-half, so it goes to the TOP -- which is also
        #- where its pin already is, so the 43 um lane the previous
        #- arrangement cost it is gone.
        #- WEST of the pin, not east: the pin is VO's, and VO's own M3
        #- crossing leaves it eastward at the same y, so an eastward
        #- hop runs met2.2 against it whatever lane it is aimed at.
        #- West of x 118400 the row is clear.
        ("CMPO", "M2", 100000, "top"),
        #- IBP_1U<1> is per-half too and its pin is already 38 um from
        #- the WEST edge, which is the side the bias block is on. Left
        #- mid-row the top reached it with an 87 um M4 bar that ran
        #- into the block and landed on JNWTR_CAPX1's plate. `xlane`
        #- is a row offset in PITCHes for a west/east port, not an x.
        ("IBP_1U<1>", "M3", 4, "west"),
    ]

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

        #- RST: A PORT ON THE EDGE, AND A PATH TO IT.
        #-
        #- Raising the port in place was tried and abandoned: a stack
        #- driven onto the subcell's own pin rect lands a second mcon
        #- beside the one already there, and publishing a pad computed
        #- from the story's endsAt left RST and VSS out of the
        #- extracted port list entirely. An edge port is simpler and it
        #- is also what CCMP did -- its RST sat at y 0..4000, on the
        #- bottom edge, which is where the level above comes for it.
        #-
        #- The port rect is MADE here and the path is drawn to it, both
        #- in the routing phase; afterPorts only publishes it. A path
        #- created in afterPorts never routes -- the phase is over.
        from cicpy.core.rect import Rect as _Rect
        self._edge_ports = {}
        #- EACH SEAM PORT: a pad MADE at an edge, and a path to it.
        #- (net, edge layer, x of the descent, which edge)
        #-
        #- THE DESCENT LANE IS THE DESIGN. Straight down from a pin is
        #- usually the comparator's gate-tab lane, and PWRUP_N_1V8's
        #- own via stack lives there -- M2 (137300,199000)-(140700,
        #- 207800) took RST's first attempt. The 2 um seam between the
        #- nmos and pmos halves carries nothing, and east of the cap
        #- row (which ends at x 215000) is clear to the bottom.
        for net, lay_, xlane, edge in self._EDGE_PORTS:
            r = self._port(cmp_i, net)
            if r is None:
                log.error(f"{net}: the core does not publish it")
                continue
            if edge in ("bottom", "top"):
                x = int(cmp_i.x1) + xlane
                y = (int(layout.y1) if edge == "bottom"
                     else int(layout.y2) - 4000)
                pad = _Rect(lay_, x, y, 3200, 4000)
            else:
                #- WEST AND EAST: the pad is at the pin's own row and
                #- the story is one horizontal hop. `xlane` is the
                #- row offset in whole PITCHes here, not an x.
                y = int(r.y1) + xlane * 6000
                x = (int(layout.x1) if edge == "west"
                     else int(layout.x2) - 4000)
                pad = _Rect(lay_, x, y, 4000, 3400)
            pad.setNet(net)
            layout.add(pad)
            p = layout.path(net, "M1", start=[r], stop=[pad],
                            options="1cuts,2vcuts")
            p.start()
            p.up()                      #- M2
            p.up()                      #- M3
            if edge in ("bottom", "top"):
                p.movex(p.landing("x"))     #- across to the lane
                p.down()                    #- M2, and down it
                p.movey(p.landing("y"))
            else:
                p.movey(p.landing("y"))     #- M3 is horizontal, so
                p.movex(p.landing("x"))     #- the hop IS the story
            p.end()
            self._edge_ports[net] = pad

        #- PWRUP_N_1V8 AND PWRUP_B_1V8: LIFTED IN PLACE, NOT MOVED.
        #-
        #- These two stay mid-row -- LELO_TEMP's seam stories anchor on
        #- them where the core publishes them -- but they cannot stay
        #- on M1. The pin is 3200 x 4000 and every M1M2 cut is bigger
        #- than that in one direction: 1cuts,2vcuts overhangs 4400 in
        #- y, the default 2cuts,1vcuts overhangs 5200 in x, and either
        #- way the parent's own via pad lands on the neighbouring
        #- device (measured: PWRUP_N's pad at (1081900,891600) touched
        #- REYATR_NCH_2C5F0's M1, and PWRUP_B's the pmos next door --
        #- two LVS shorts at the top and nothing wrong down here).
        #-
        #- So the cut is made HERE, where the cell knows its own row,
        #- and the port is published on the M3 above it. The parent
        #- then arrives on metal with room around it and draws no cut
        #- at the pin at all. This is what LELOTEMP_CCMP did too -- its
        #- seam stories start `lay.path(..., "M3", ...)`.
        #-
        #- IBP_1U<1> HAS THE SAME SYMPTOM AND IS NOT THE SAME BUG, so
        #- it is NOT lifted here. The top reaches it with a
        #- cut_M1M4_2x1 that landed on REYATR_NCH_2C5F0's M1 at
        #- (1066000,898100) -- but that pin is a 16000-wide bar, wide
        #- enough for any cut, and the pad sits 2900 BELOW it and
        #- overlaps by 300. That is the top aiming low, not the pin
        #- being too small, and lifting it here just moved the fault
        #- (2 met2.2 in this cell, top unchanged).
        self._lifted = {}
        for net in ("PWRUP_N_1V8", "PWRUP_B_1V8"):
            r = self._port(cmp_i, net)
            if r is None:
                log.error(f"{net}: the core does not publish it")
                continue
            #- THE PAD IS THE PIN, LIFTED -- not a fixed 8000 stub.
            #- IBP_1U<1>'s pin is a 16000-wide bar and a stub beside
            #- it ran met2.2 against the block's own M3 (4 errors);
            #- over it, the pad is inside geometry that is already
            #- legal. The 8000 floor is for the 3200-wide gate tabs,
            #- which need a via to fit.
            w = max(8000, int(r.x2) - int(r.x1))
            pad = _Rect("M3", int(r.x1) - (w - (int(r.x2) - int(r.x1))) // 2,
                        int(r.y1), w, 4000)
            pad.setNet(net)
            p = layout.path(net, "M1", start=[r], stop=[pad],
                            options="1cuts,2vcuts")
            p.start()
            p.up()                      #- M2
            p.up()                      #- M3, and stop: the pad is at
            p.end()                     #- the pin's own x and y
            layout.add(pad)
            self._lifted[net] = pad

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
            #- NO END CUT AT ALL, which is the rest of that argument.
            #-
            #- Matching the core's cut SHAPE (cut_M1M4_1x2, one wide and
            #- two tall, because it is a gate tab) stopped magic
            #- complaining -- "this layer can't abut or partially
            #- overlap between subcells" is a hierarchy rule and the
            #- tiles resolved once the shapes agreed. It did not stop
            #- KLAYOUT, which reads the flattened GDS: the parent's
            #- stack and the child's still sat 0.02 x 0.04 um apart, and
            #- two 0.2 um squares that far off union into a notched
            #- polygon where a via must be square. Two via2.1a, in this
            #- cell and again at the top, and NOT fixable by moving:
            #- measured, the two stacks' viali and via1 already coincide
            #- exactly, so any shift that aligns via2 breaks those.
            #-
            #- The parent does not need a stack here. LELOTEMP_CMPR
            #- already brings this net M1 -> M4 at this pin; arriving on
            #- M4 IS the connection, and a second stack on top of the
            #- first was only ever the default doing its job. Same
            #- reasoning as VBP landing cutless on the subcell's own M4
            #- pad in LELOTEMP_OTAR.
            p = layout.path("IBP_1U<0>", "M4", start=[ci], stop=[ni],
                            options="1cuts,2vcuts,noendcut")
            p.start()
            p.movex(p.landing("x"))
            p.movey(p.landing("y"))
            p.end()

    def afterPorts(self, layout):
        """Publish the edge ports _crossings drew."""
        super().afterPorts(layout)
        #- AND NARROW THE CAP PLATE'S PORT TO ITS WEST END. The plate
        #- publishes 54 um of M4 and the parent aims at the MIDDLE of
        #- what it is given, so the top ran east INTO the block to
        #- reach it -- a 20 um riser at x 1023900 and a bar to
        #- x 1052900, both within capm.11's 1.34 um of the mirrored
        #- half's own cap bank. A port is an invitation; a wide one
        #- invites the parent inside.
        from cicpy.core.rect import Rect as _R2
        ip = self._port(layout.getInstanceFromInstanceName("xcaps"),
                        "IBP_1U<0>")
        if ip is not None:
            end = _R2(ip.layer, int(ip.x1), int(ip.y1), 6000,
                      int(ip.y2) - int(ip.y1))
            end.setNet("IBP_1U<0>")
            layout.updatePort("IBP_1U<0>", end, routeLayer=ip.layer)
        for net, pad in (getattr(self, "_edge_ports", {}) or {}).items():
            layout.updatePort(net, pad, routeLayer=pad.layer)
        for net, pad in (getattr(self, "_lifted", {}) or {}).items():
            layout.updatePort(net, pad, routeLayer=pad.layer)

    #- ROUTES SO FAR. The placement is verified on its own first, the
    #- way LELOTEMP_CMPR's was: the crossing nets go in one at a time,
    #- shortest first, each written as a path and checked for shorts
    #- before the next.
    routes = []
