"""LELO_TEMP: the top-level sidecar, aimed at a TinyTapeout 1x1 tile.

The temperature sensor as a relaxation oscillator: the bias block
charges/discharges through two comparators whose outputs cross-couple
in a NOR latch; a buffer drives OSC_TEMP_1V8 out. The tile budget is
161 x 111.52 um (tt_block_1x1_pg.def) -- the bias block was reworked
to 96 x 106.5 to clear the height.

Floorplan (afterPlace finishes what rows cannot say -- rows are
horizontal bands, and this is an L: one tall block beside two
stacked ones):

    bias (96 x 106.5) | ccmp_b (41 x 37)  | dig strip
                      | ccmp_a (41 x 37)  |
"""
import logging

from cicpy.sidecar import SidecarCell, Stack

log = logging.getLogger("LELO_TEMP")


class LELO_TEMP(SidecarCell):

    place = {"groupbreak": 2, "channel": 6}

    class bias(Stack):
        """LELOTEMP_BIAS_IBP, the finished cell."""
        match = r'^x1_ibp$'
        group = "bias"
        fill = False
        order = ['x1_ibp']

        def beforeRoute(self, entry):
            """LPI, the loop: the block's LPO pad back to its LPI bar.

            Both ends are inside this subcell -- the top used to draw
            it by hand, so it went when the top's routing went, and LVS
            read 10 nets against 11.

            A SEARCH IS THE WRONG TOOL FOR IT. `-|--` takes the direct
            line, straight west through the M5 supply columns and the
            cap array, and merges five nets (11 DRC, the layout down to
            5 nets); a channel trunk resolves to `trunkx891000`, mid
            block, and leaves the net open. The corridor a person would
            use is the last few microns at the RIGHT EDGE, which is
            empty and which the LPI bar already reaches -- so the story
            says that, and nothing has to discover it.
            """
            lay = self.layout
            inst = lay.getInstanceFromInstanceName("x1_ibp")
            if inst is None:
                return None
            #- both pins carry the net name, so tell them apart by
            #- position: the pad is the high one, the bar the low
            rs = [c.get() for c in inst.children
                  if getattr(c, "isPort", lambda: False)()
                  and getattr(c, "name", "") == "LPI"]
            rs = [r for r in rs if r is not None]
            if len(rs) < 2:
                log.error("LPI: expected two pins on the block")
                return None
            lpo = max(rs, key=lambda r: r.y1)
            lpi = min(rs, key=lambda r: r.y1)
            pp = lay.path("LPI", lpo.layer, start=[lpo], stop=[lpi])
            pp.start()
            pp.up()
            pp.up()
            pp.movex(pp.track("bias", 155))
            pp.movey(pp.landing("y"))
            pp.down()
            pp.down()
            pp.end()
            #- TRUE CLAIMS THE NET. Returning None leaves the built-in
            #- router free to route LPI as well, and it draws a bare M2
            #- vertical from pin to pin -- x 712300..715300, straight
            #- up 35 um through the block's own device metal, which is
            #- what pulled xota/VR1 into this net and made LVS read one
            #- net fewer in the layout than in the schematic. The story
            #- above is the route; there is nothing left to find.
            return True

    class ccmp(Stack):
        """BOTH comparators, as one subcell. They were two stacks the
        top had to abut by hand; as one they stack themselves, get
        their own cell, and present ports the top can reach instead of
        interior pins it had to hop into."""
        match = r'^x[23]_ccmp$'
        group = "ccmp"
        fill = False
        xspace = 5
        order = ['x2_ccmp', 'x3_ccmp']

        def beforePlace(self, entry):
            """SPACE FOR THE CAPS AT THE SEAM.

            Mirrored, the pair meets cap array to cap array -- and a
            MiM cap wants 0.84 um to another (capm.2a), where abutted
            they sat 0.44 apart. The gap is stated in microns from the
            rule, not guessed: the caps are the tallest thing at the
            seam and they set it.
            """
            self.stack(ygap=2 * self.layout.um)

        def beforeRoute(self, entry):
            """MIRROR THE UPPER ONE about x, so the pair is symmetric
            about the seam they share.

            A matched pair placed as two identical copies repeats the
            same edge at the seam; mirrored, the two halves meet edge
            to mirrored-edge, which is what lets a matched pair sit
            together at all. The same argument as CellGroup.mirror()
            makes for a column about its vertical axis -- this is the
            horizontal one, because these two are stacked.
            """
            lay = self.layout
            up = lay.getInstanceFromInstanceName("x3_ccmp")
            if up is not None:
                #- setAngle leaves the instance position in the
                #- mirrored frame, so pin it back where it was
                x, y = int(up.x1), int(up.y1)
                up.setAngle("MX")
                up.moveTo(x, y)
                up.updateBoundingRect()
                self.updateBoundingRect()
            down = lay.getInstanceFromInstanceName("x2_ccmp")
            if up is None or down is None:
                log.error("ccmp: both comparators are needed to route")
                return None
            self._crossSeam(lay, down, up)
            #- TRUE CLAIMS THE PAIR. Left to the built-in router this
            #- cell came out with two straps that no rule catches and
            #- LVS does: an M1 riser up the right edge tying VDD to
            #- VDD straight THROUGH both VSS rails, and a full height
            #- M2 bar at x 205000 crossing VO, VS and VBP2 inside both
            #- comparators. The three signals it did not draw at all
            #- (`no path`, 520000 away) are the ones below.
            return True

        #- ------------------------------------------------------------
        #- The seam, told as five stories
        #-
        #- MIRRORED, THE PAIR IS ITS OWN COORDINATE SYSTEM: every
        #- shared net has its two pins at the same x and at mirrored y,
        #- so each story is written once with a pin anchor and its
        #- opposite, and stays symmetric through any resize.
        #-
        #- What the mirror does NOT give is a way across. A comparator
        #- is solid M1/M2/M3 from edge to edge except for two gaps, and
        #- `tracks` is what found them:
        #-
        #-   * the empty column between the last device stack and the
        #-     cap bank -- 26 free M2 lanes, the full height of both
        #-     blocks. VC, PWRUP_B, VDD and VSS ride it.
        #-   * one free M4 lane just east of the PWRUP_N pin, also full
        #-     height, which saves that net the trip east.
        #-
        #- and the jog rows are pin anchors offset by whole lanes,
        #- because the free M3 rows sit one lane off each pin.
        #- ------------------------------------------------------------

        @staticmethod
        def _emptyColumn(inst):
            """The comparator's own empty column, measured off it.

            A wrapper sees a placed block as the rects it PUBLISHES,
            not as the cells inside it, so "the widest gap between the
            rects" is not a question worth asking -- asked over all of
            them it answers 147000, the middle of the comparator, and
            four risers went there and shorted eleven nets.

            Two features of the published set do say it, and they are
            the two things that bound the column:

              * the cap bank's supply column, tall M4/M5 the full
                height of the block, is its right wall (378300);
              * the rightmost M2 west of that wall is where the
                block's own routing stops (311400).

            `tracks`, which reads the .cic and does see the devices,
            independently calls that band 26 free M2 lanes over the
            full height of both comparators.
            """
            sub = (getattr(inst, "layoutcell", None)
                   or getattr(inst, "_cell_obj", None))
            if sub is None:
                return None
            tall = (int(inst.y2) - int(inst.y1)) // 4
            wall, stop = None, None
            rects = []
            for c in getattr(sub, "children", []) or []:
                r = c.get() if hasattr(c, "get") else c
                if r is not None and getattr(r, "layer", ""):
                    rects.append(r)
            for r in rects:
                if r.layer in ("M4", "M5") and int(r.y2 - r.y1) > tall:
                    wall = int(r.x1) if wall is None else min(wall,
                                                              int(r.x1))
            if wall is None:
                return None
            for r in rects:
                if r.layer == "M2" and int(r.x2) <= wall:
                    stop = int(r.x2) if stop is None else max(stop,
                                                              int(r.x2))
            if stop is None or stop >= wall:
                return None
            return (int(inst.x1) + stop, int(inst.x1) + wall)

        @staticmethod
        def _port(inst, net):
            """The instance's published pin for `net`, as placed."""
            rs = [c.get() for c in getattr(inst, "children", []) or []
                  if getattr(c, "isPort", lambda: False)()
                  and getattr(c, "name", "") == net]
            rs = [r for r in rs if r is not None]
            return rs[0] if rs else None

        def _crossSeam(self, lay, a, b):
            col = self._emptyColumn(a)
            if col is None:
                log.error("ccmp: no empty column to cross the seam in")
                return
            lay.addRoutingChannel("cross", col[0], col[1], horizontal=False)

            def pins(net):
                return self._port(a, net), self._port(b, net)

            #- A PIN IS 3200 WIDE AND THE DEFAULT CUT IS 8800. Every
            #- signal here leaves its pin through a via, and a 2x1 pad
            #- centred on the pin overhangs it by 2800 on each side --
            #- measured, PWRUP_B's start pad reached 2800 west and
            #- landed on the comparator's own PWRUP_1V8. Turned on its
            #- side the same two cuts fit inside the pin.
            narrow = "1cuts,2vcuts"

            #- VC: an M2 pin at the bottom edge. Up to M3, DOWN one
            #- lane to the free row under the pin (the rows at the
            #- pin's own y are full), east into the column, and the
            #- mirror of all that at the top.
            lo, hi = pins("VC")
            if lo is not None and hi is not None:
                p = lay.path("VC", "M2", start=[lo], stop=[hi],
                             options=narrow)
                p.start()
                #- DOWN FIRST, THEN UP. Taking M3 at the pin and
                #- riding it down to the row put a 3 um M3 leg beside
                #- the pin and two met2.2 errors with it; on M2 the
                #- same leg is the pin's own lane continued.
                p.movey(p.pin("x2_ccmp", "VC", "y") - p.PITCH)
                p.up()                                    #- M3, east
                p.movex(p.track("cross", 1))
                p.down()                                  #- M2, up the
                p.movey(p.pin("x3_ccmp", "VC", "y") + p.PITCH)
                p.up()                                    #- column
                p.movex(p.landing("x"))
                p.down()                                  #- M2 again
                p.end()

            #- PWRUP_B: an M3 pin with the tap row under it, so its
            #- free row is one lane ABOVE. The step up is on M2, which
            #- is free right there and nowhere else nearby.
            lo, hi = pins("PWRUP_B_1V8")
            if lo is not None and hi is not None:
                p = lay.path("PWRUP_B_1V8", "M3", start=[lo],
                             stop=[hi], options=narrow)
                p.start()
                p.down()                                  #- M2
                p.movey(p.pin("x2_ccmp", "PWRUP_B_1V8", "y") + p.PITCH)
                p.up()                                    #- M3, east
                p.movex(p.track("cross", 3))
                p.down()                                  #- M2, up the
                p.movey(p.pin("x3_ccmp", "PWRUP_B_1V8", "y") - p.PITCH)
                p.up()                                    #- column
                p.movex(p.landing("x"))
                p.end()

            #- PWRUP_N: its own M4 lane, two stubs east of the pin. The
            #- trip to the empty column would cross the whole cell
            #- twice for a net that has a free lane 5 um away.
            lo, hi = pins("PWRUP_N_1V8")
            if lo is not None and hi is not None:
                p = lay.path("PWRUP_N_1V8", "M3", start=[lo],
                             stop=[hi], options=narrow)
                p.start()
                #- TWO lanes east, not one: at one the M4 riser sits
                #- 0.2 um from the comparator's own M4 and met3.2
                #- wants 0.3.
                p.movex(p.pin("x2_ccmp", "PWRUP_N_1V8", "x")
                        + 2 * p.PITCH)
                p.up()                           #- M4, free top to
                p.movey(p.landing("y"))          #- bottom at this x
                p.down()
                p.end()

            #- VDD and VSS: RISE IN THE COLUMN, DO NOT TRAVEL TO IT.
            #- The rails are full width, so sliding along one on M1 to
            #- reach the column looks free -- and is not: the tap and
            #- guard geometry above a rail carries the same supply at
            #- other x, and one such slide tied VDD to VSS through
            #- (13800,394000)-(238600,427000). The rail is already
            #- under the column, so the story starts THERE: a slice of
            #- the rail at the lane, and nothing horizontal is drawn
            #- at all.
            from cicpy.core.rect import Rect as _R

            def _on_rail(bar, x, net):
                r = _R(bar.layer, int(x) - 1500, int(bar.y1), 3000,
                       int(bar.y2) - int(bar.y1))
                r.setNet(net)
                return r

            for net, lane in (("VDD_1V8", 5), ("VSS", 7)):
                lo, hi = pins(net)
                if lo is None or hi is None:
                    log.error(f"ccmp: {net} is not on both comparators")
                    continue
                x = lay.channelTrackCoord("cross", lane)
                if x is None:
                    continue
                p = lay.path(net, "M1", start=[_on_rail(lo, x, net)],
                             stop=[_on_rail(hi, x, net)])
                p.start()
                p.up()                           #- M2, over everything
                p.movey(p.landing("y"))          #- the rails carry
                p.down()
                p.end()

    class dig(Stack):
        """The oscillator's logic: OR gate, the cross-coupled NOR
        pair, the two buffers, the powerdown inverter chain."""
        match = r'^(x[1-7]|xtap_dig_0)$'
        group = "dig"
        fill = False
        xspace = 4
        order = ['xtap_dig_0', 'x7', 'x3', 'x4', 'x1', 'x5', 'x2',
                 'x6']

        #- The tapcell is in the schematic now (the CV logic family
        #- carries no taps of its own, and netgen counts the two
        #- tie-off devices), so the stack places it like any other
        #- instance -- first, at the strip's base. It used to be an
        #- addPhysicalInstance here, which became a duplicate the
        #- moment the schematic gained one.

        def beforeRoute(self, entry):
            """The strip's own nets, each on its own lane.

            Left to itself the router put RST_A, RST_B and net2 in one
            column on M2 and shorted all three -- the same failure as
            the top level had, and the same cause: no lane budget. A
            channel over the strip's own width gives each net a lane,
            and the lanes are two tracks apart because an M2-M3 pad is
            wider than one.
            """
            lay = self.layout
            lay.addRoutingChannel("strip", int(self.x1), int(self.x2),
                                  horizontal=False)
            for _i, _n in enumerate(("net1", "net2", "RST_A", "RST_B")):
                self.addConnectivityRoute(
                    "M2", "^" + _n + "$", "||",
                    f"vchannel=strip,vtrack={2 + _i * 7}", 2)
            return None

        #- NO `return True` HERE ANY MORE. That claimed the subcell as
        #- already routed, which was true when the top hand-routed
        #- every net into it; with the top's routing gone it meant
        #- nothing wired the strip at all -- LVS counted 25 nets in
        #- the layout against 18 in the schematic, seven of them
        #- split. The built-in router takes it now.

    rows = [
        [bias, ccmp, dig],
    ]

    supplies = []

    #- the presence of `routes` is what makes this cell MADE OF
    #- SUBCELLS: hierarchy() splits the netlist, builds a cell per
    #- subcell, and the top instantiates them and routes between
    #- their ports. Empty means the top declares no channel routes
    #- of its own yet.
    routes = []

    def afterPlace(self, layout):
        super().afterPlace(layout)
        from cicpy.core.subcell import subcell_groups
        g = subcell_groups(layout)
        #- the two comparators stack themselves now: one subcell
        #- the tap hangs 16000 below the logic strip, which drags the
        #- whole dig group below the other blocks' bases -- and the
        #- bottom VSS ring, drawn on the FULL bbox, then lays its 9 um
        #- li bar straight across the tap and the OR gate, shorting
        #- AVDD to AVSS (measured: the short vanished as soon as the
        #- tap cleared the ring band). Lift the group so its base --
        #- tap included -- sits at the comparators' base.
        #- the tap hangs 16000 below the logic strip, and the group
        #- bbox does not count it: the bottom VSS ring wraps the true
        #- extent and lays its 9 um li bar straight across the tap and
        #- the OR gate, shorting AVDD to AVSS (measured: the short
        #- vanished the moment the tap cleared the ring band). Lift
        #- the strip, tap included, so the tap's base sits where the
        #- other blocks' bases do.
        dg = g.get("dig")
        tap = layout.getInstanceFromInstanceName("xtap_dig_0")
        if dg is not None and ca is not None and tap is not None:
            dy = int(ca.y1) - int(tap.y1)
            if dy:
                moved = set()
                for i in list(dg.instances) + [tap]:
                    if id(i) in moved:
                        continue
                    moved.add(id(i))
                    i.translate(0, dy)
                dg.updateBoundingRect()
        #- DROP EVERY BLOCK 0.13 um, to buy the S band its clearance.
        #- The four M5 lanes over the bias block need 0.40 under the
        #- first one (met4.5a/b, "attached to large metal4"), 0.30 x 4
        #- of wire, 0.40 x 3 of gap and 0.09 for the via cap above
        #- S(4) -- 2.89 um. Between the block's top and the 111.52 um
        #- tile ceiling there was 2.76. Everything else in the strip is
        #- already at its minimum, so the room has to come from below.
        #-
        #- It is there: the rings are laid on the INSTANCES' own bbox
        #- (see beforeRoute), so they come down with the blocks, and
        #- the band under them absorbs the move. Measured -- the cell
        #- goes 111.500 -> 111.370 on this alone, and 87 DRC -> 82.
        #- With S at +4000 it lands on 111.520 exactly and 75.
        for _n in ("x1_ibp", "x2_ccmp", "x3_ccmp", "xtap_dig_0",
                   "x1", "x2", "x3", "x4", "x5", "x6", "x7"):
            _i = layout.getInstanceFromInstanceName(_n)
            if _i is not None:
                _i.translate(0, -1300)
        #- the move leaves every group's stored extent where base
        #- place scattered it, and the ring wraps THAT box: refresh
        for grp in layout.cellgroups:
            grp.updateBoundingRect()
        layout.updateBoundingRect()

        #- THE BANDS, NAMED. Every corridor this floorplan opens gets
        #- registered here, so a route can aim at "lband track 1"
        #- instead of a lambda over a literal pitch. The lambdas below
        #- are what these replace; a track index survives a resize and
        #- another technology, and 960000 + 1000 + (i-1)*6000 does not.
        _bi = layout.getInstanceFromInstanceName("x1_ibp")
        _ca = layout.getInstanceFromInstanceName("x2_ccmp")
        _cb = layout.getInstanceFromInstanceName("x3_ccmp")
        _d0 = layout.getInstanceFromInstanceName("x7")
        if None not in (_bi, _ca, _cb, _d0):
            layout.addRoutingChannel("lband", int(_bi.x2), int(_ca.x1),
                                     horizontal=False)
            layout.addRoutingChannel("dband", int(_ca.x2), int(_d0.x1),
                                     horizontal=False)
            layout.addRoutingChannel("bband", 0, int(_ca.y1))
            layout.addRoutingChannel("myband", int(_ca.y2), int(_cb.y1))
            layout.addRoutingChannel("sband", int(_bi.y2),
                                     int(_bi.y2) + 28000)

    def beforeRoute(self, layout):
        #- rings on an EXPLICIT rect: addRouteRing wraps the layout
        #- bbox, which does not count the physical-only tapcell, so
        #- the bottom ring landed 2 um INSIDE the content and its 9 um
        #- li bar shorted the logic strip's AVDD to AVSS (measured).
        #- The rect here spans every instance, tap included.
        from cicpy.core.rect import Rect as _RR
        #- MADE OF SUBCELLS: the devices live inside them now, so the
        #- ring wraps the three block instances. The old list named
        #- every device and came back empty the moment the hierarchy
        #- appeared -- min() on nothing, which is a loud failure and
        #- the right one.
        names = ["xbias", "xccmp", "xdig",
                 "x1_ibp", "x2_ccmp", "x3_ccmp", "xtap_dig_0",
                 "x1", "x2", "x3", "x4", "x5", "x6", "x7"]
        boxes = [layout.getInstanceFromInstanceName(n) for n in names]
        boxes = [i for i in boxes if i is not None]
        if not boxes:
            log.error("no blocks to wrap a ring around")
            return
        x1 = min(int(i.x1) for i in boxes)
        y1 = min(int(i.y1) for i in boxes)
        x2 = max(int(i.x2) for i in boxes)
        y2 = max(int(i.y2) for i in boxes)
        full = _RR("M1", x1, y1, x2 - x1, y2 - y1)
        layout.addRouteRingOnRect("M1", "VDD_1V8", full, "t",
                                  widthmult=3, spacemult=2)
        layout.addRouteRingOnRect("M1", "VSS", full, "b",
                                  widthmult=3, spacemult=2)
        #- ring attachments happen in beforePaint: the rings re-lay
        #- as routes grow the bbox, and a cut placed at the ring's
        #- beforeRoute position lands 8000 off the painted bar
        #- (measured)
        import os as _os
        if _os.environ.get("AUTOROUTE"):
            #- AUTOROUTE=1 hands every top net to the maze router
            #- instead of the lane plan below -- one
            #- addConnectivityRoute per net and nothing else.
            #-
            #- IT LOSES, and the first measurement said otherwise
            #- because it counted the wrong thing. Short COMPONENTS
            #- flatter a build that merges everything: one component
            #- can hold thirty nets.  Count the NETS caught in a short:
            #-
            #-                        shorts  nets shorted  worst
            #-   lane plan (778 ln)     13         24        8 nets
            #-   router, all on M5       6         29       24 nets
            #-   router, M3/M4/M5        4         32       29 nets
            #-   router, M4/M5 only      5         37       33 nets
            #-
            #- Every variant collapses into one giant component, and
            #- the bridges say why: the top level has no idea which
            #- layers the BLOCKS own. Routed on M3 it runs into
            #- LELOTEMP_CMP's own VBP2; confined to M4/M5 it has two
            #- layers for twenty nets and they cross each other.
            #-
            #- Which is exactly what the 778 lines encode -- a lane
            #- budget and a layer reservation per band. Converting this
            #- cell is not deleting them; it is saying the same thing
            #- declaratively, as channels and tracks, so the search has
            #- the constraints the hand plan carries in its head.
            import re as _re
            #- keep the hand-drawn PORT pins: they are the cell's
            #- interface, not signal routing, and dropping them fails
            #- LVS on pin matching for reasons that say nothing about
            #- the router
            _rt = _os.environ.get("RT")
            _os.environ["RT"] = "misc"
            try:
                self._signal_routes(layout)
            finally:
                if _rt is None:
                    _os.environ.pop("RT", None)
                else:
                    _os.environ["RT"] = _rt
            #- ONE LAYER PER NET IS NOT A TEST OF THE ROUTER. Giving
            #- every net "M5" put twenty of them on one plane, where
            #- they crossed freely and merged into a single 24-net
            #- component of 2293 rects -- which says nothing about
            #- routing and everything about the question asked.
            #- Spread them instead, and let the search do the rest.
            _skip = {"VDD_1V8", "VSS"}
            _layers = ["M4", "M5"]
            _nets = [n for n in (getattr(layout, "nodeGraphList", []) or [])
                     if n not in _skip]
            for _i, _net in enumerate(sorted(_nets)):
                layout.addConnectivityRoute(
                    _layers[_i % len(_layers)],
                    "^" + _re.escape(_net) + "$", "-|--", "", 2, "", "")
        #- NO TOP ROUTING. This cell is made of subcells now: the
        #- blocks are cells with ports, and the top's job is to route
        #- between those ports -- declaratively, in `routes` -- not to
        #- reach into their interiors with hand geometry.
        #-
        #- The 778 lines that used to live here are in git; they named
        #- devices (x1_ibp, x2_ccmp, x7) that this level no longer has,
        #- so they could not survive the hierarchy even if they were
        #- wanted.
        super().beforeRoute(layout)


    def beforePaint(self, layout):
        #- the block supply ties reached into device instances that a
        #- hierarchical build no longer has at this level; the rings
        #- are laid in beforeRoute and the blocks present their own
        #- supply ports for the top to tie to.
        return
        #- NO addPowerConnection here: it stretches EVERY published
        #- supply rect to the ring -- including the blocks' mid-cell
        #- tap bars -- and each stretched copy slices through the core
        #- it came from (measured: every pin of both comparators and
        #- the bias merged into one VSS blob with zero signal routes).
        #- Each block instead ties its own EDGE bar to the ring.
        from cicpy.core.rect import Rect as _R
        from cicpy.core.cut import Cut as _C

        def _edge_bar(inst, net, top):
            #- the block's own ring bar on the facing edge: of the
            #- published M1 rects on the net, the extreme one
            rs = [c.get() for c in inst.children
                  if getattr(c, "isPort", lambda: False)()
                  and getattr(c, "name", "") == net]
            rs = [r for r in rs if r is not None and r.layer == "M1"]
            if not rs:
                return None
            return (max(rs, key=lambda r: int(r.y2)) if top
                    else min(rs, key=lambda r: int(r.y1)))

        rb = layout.named_rects.get("ring_b_VSS")
        rt = layout.named_rects.get("ring_t_VDD_1V8")
        rt_cy = int(rt.centerY()) if rt is not None else None
        bias = layout.getInstanceFromInstanceName("x1_ibp")
        ca = layout.getInstanceFromInstanceName("x2_ccmp")
        cb = layout.getInstanceFromInstanceName("x3_ccmp")

        def _tie(net, bar, rail, top):
            if bar is None or rail is None:
                log.error(f"missing tie pieces for {net}")
                return
            y1 = int(bar.y1) if top else int(rail.y1)
            y2 = int(rail.y2) if top else int(bar.y2)
            t = _R("M1", int(bar.x1), y1, int(bar.x2 - bar.x1), y2 - y1)
            t.setNet(net)
            layout.add(t)

        import os as _os
        _nt = _os.environ.get("NT", "")
        #- straight down/up where the corridor is the block's own gap
        if "b" not in _nt:
            _tie("VSS", _edge_bar(bias, "VSS", False), rb, False)
            _tie("VDD_1V8", _edge_bar(bias, "VDD_1V8", True), rt, True)
        if "c" not in _nt:
            _tie("VSS", _edge_bar(ca, "VSS", False), rb, False)
            _tie("VDD_1V8", _edge_bar(cb, "VDD_1V8", True), rt, True)

        #- the dig strip: supply is the JNWTR M4 columns; VSS column
        #- drops onto the bottom ring, VDD column ties east to the
        #- ring's right leg (the top ring is 90 um up)
        dig_lo = layout.getInstanceFromInstanceName("x7")
        dig_hi = layout.getInstanceFromInstanceName("x6")

        def _m4col(inst, net):
            rs = [c.get() for c in inst.children
                  if getattr(c, "isPort", lambda: False)()
                  and getattr(c, "name", "") == net]
            rs = [r for r in rs if r is not None and r.layer == "M4"]
            return rs[0] if rs else None

        rleg_v = layout.named_rects.get("ring_r_VSS")
        rleg_d = layout.named_rects.get("ring_r_VDD_1V8")
        gcol = _m4col(dig_lo, "VSS")
        if gcol is not None and rb is not None and "d" not in _nt:
            t = _R("M4", int(gcol.x1), int(rb.y1),
                   int(gcol.x2 - gcol.x1), int(gcol.y1) + 100 - int(rb.y1))
            t.setNet("VSS")
            layout.add(t)
            ct = (_C.getInstance("M1", "M4", 2, 1)
                  or _C.getInstance("M1", "M4", 1, 1))
            if ct is not None:
                ct.moveCenter(int(gcol.centerX()), int(rb.centerY()))
                layout.add(ct)
        vcol = _m4col(dig_hi, "VDD_1V8")
        if vcol is not None and rt is not None and "e" not in _nt:
            t = _R("M4", int(vcol.x1), int(vcol.y2) - 1000,
                   int(vcol.x2 - vcol.x1),
                   rt_cy + 2000 - int(vcol.y2) + 1000)
            t.setNet("VDD_1V8")
            layout.add(t)
            ct = (_C.getInstance("M1", "M4", 2, 1)
                  or _C.getInstance("M1", "M4", 1, 1))
            if ct is not None:
                ct.moveCenter(int(vcol.centerX()), rt_cy)
                layout.add(ct)
        #- ca's VDD and cb's VSS cannot stretch through each other
        #- (the stacked-comparator corridor), and the rings have no
        #- legs: each rides an M4 riser through the ccmp-dig gap.
        #- x lanes 1421000 (up, clears the CMPO_A stack at D1 which
        #- starts above y 390000 only) and 1456000 (down, east of the
        #- B-lane ends at D6).
        def _stack14(net, cx, cy):
            ct = (_C.getInstance("M1", "M4", 1, 1)
                  or _C.getInstance("M4", "M1", 1, 1))
            if ct is None:
                log.error("no M1-M4 cut")
                return
            ct.moveCenter(int(cx), int(cy))
            layout.add(ct)

        #- The ccmp supplies rise/fall in the ccmp-dig corridor, which
        #- the signal replan emptied of verticals: every logic-bound
        #- net now turns down its own M2 column OVER the strip, so the
        #- corridor carries horizontals only. both take M4 lanes: every
        #- signal crosses this corridor on an M5 horizontal, so an M5
        #- riser here collects the lot (measured: VDD picked up
        #- CMPO_A, CMPO_B, RST_A and PWRUP_B). The two M1 stubs that
        #- feed the lanes cross each other's lane at their own rows,
        #- where the other net has only M4.
        _xv, _xg = int(ca.x2) + 16000, int(ca.x2) + 28000

        def _stack1n(net, top_layer, cx, cy):
            ct = (_C.getInstance("M1", top_layer, 1, 1)
                  or _C.getInstance(top_layer, "M1", 1, 1))
            if ct is None:
                log.error(f"no M1-{top_layer} cut")
                return
            ct.moveCenter(int(cx), int(cy))
            layout.add(ct)

        def _corridor_tie(net, bar, rail, xr, vlayer):
            if bar is None or rail is None:
                log.error(f"missing tie pieces for {net}")
                return
            y0 = int(bar.y1) + 1000
            #- the stub leaves the block's own ring bar on M1
            t = _R("M1", int(bar.x2) - 3000, y0,
                   xr + 4000 - int(bar.x2) + 3000, 6000)
            t.setNet(net)
            layout.add(t)
            _stack1n(net, vlayer, xr + 2000, y0 + 3000)
            ry = int(rail.centerY())
            import os as _o2
            _cap = _o2.environ.get("LANECAP")
            if _cap:
                y0 = min(y0, int(_cap))
            v = _R(vlayer, xr, min(ry, y0), 4000, abs(ry - y0) + 6000)
            v.setNet(net)
            layout.add(v)
            _stack1n(net, vlayer, xr + 2000, ry)

        if "f" not in _nt:
            _corridor_tie("VDD_1V8", _edge_bar(ca, "VDD_1V8", True),
                          rt, _xv, "M4")
        if "g" not in _nt:
            _corridor_tie("VSS", _edge_bar(cb, "VSS", False), rb,
                          _xg, "M4")

