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

    #- INERT ON THIS CELL, kept only so a reader does not add it back
    #- expecting an effect. Both knobs are read by _placeStacks, which
    #- returns at once for a cell that holds no stacks, and this cell
    #- holds subcells. The gap between the assembled rows is `channel`
    #- on the class (below), not this one.
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
            #- THROUGH THE BLOCK VIEW, not the block's own children.
            #- The comparator is made of cells now, and the wall this
            #- measures -- the cap bank's tall M4/M5 -- belongs to one
            #- of them. Asked of the children alone the question came
            #- back empty and the seam went unrouted, which is the
            #- same blindness the view was built to end.
            rects = [r for r in sub.flatMetal()
                     if getattr(r, "layer", "")]
            #- THE RIGHTMOST tall column, not the leftmost. Through
            #- the published rects alone the cap bank was the only
            #- one and either answer was it; through the view there
            #- are the comparator's own risers too, and the leftmost
            #- of those (44300) named a 6500 band in the middle of
            #- the core. The bank is the block's right wall, so the
            #- rightmost is the one that means it.
            for r in rects:
                if r.layer in ("M4", "M5") and int(r.y2 - r.y1) > tall:
                    wall = int(r.x1) if wall is None else max(wall,
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

        #- THE COLUMNS THE PAIR CROSSES IN, measured off the block's
        #- own M2 track map (cicpy tracks ... --layer M2). Two pins
        #- are left in the middle of the row by LELOTEMP_CCMPR and
        #- each has a column free the full height of the block within
        #- a few microns of it, so neither has to travel:
        #-
        #-   PWRUP_N pin @57600  -> the band 60000..99000
        #-   PWRUP_B pin @317600 -> the band 312000..350000
        #-
        #- (net, the column, the lane the M3 hop takes off the pin)
        SEAM = (("PWRUP_N_1V8", 66000, 0),
                ("PWRUP_B_1V8", 330000, 0))

        def _crossSeam(self, lay, a, b):
            #- A STEP TAKES SOMETHING NAMED IN THE DESIGN, NEVER A
            #- COORDINATE -- so each column is registered as a channel
            #- and the story asks for its track.
            for net, colx, _ in self.SEAM:
                lay.addRoutingChannel(net, int(a.x1) + colx,
                                      int(a.x1) + colx + 12000,
                                      horizontal=False)

            def pins(net):
                return self._port(a, net), self._port(b, net)

            #- A PIN IS 3200 WIDE AND THE DEFAULT CUT IS 8800. Every
            #- signal here leaves its pin through a via, and a 2x1 pad
            #- centred on the pin overhangs it by 2800 on each side --
            #- measured, PWRUP_B's start pad reached 2800 west and
            #- landed on the comparator's own PWRUP_1V8. Turned on its
            #- side the same two cuts fit inside the pin.
            narrow = "1cuts,2vcuts"

            #- VC, RST AND CMPO ARE NOT HERE ANY MORE, AND THAT IS THE
            #- POINT. LELOTEMP_CCMPR now puts them on its own edges,
            #- and the mirror sorts them out for free: VC leaves at the
            #- block's TOP, so the two halves' VC pads meet AT the seam
            #- and abut with nothing drawn; RST and CMPO leave at the
            #- BOTTOM, which the mirror turns into the pair's outer
            #- faces, which is exactly where RST_A/RST_B and
            #- CMPO_A/CMPO_B want them. Three stories deleted, not
            #- rewritten.
            #-
            #- What is left is the pair that CANNOT move: PWRUP_N and
            #- PWRUP_B are published mid-row because LELO_TEMP.sch and
            #- the CCMP port list say so.
            for net, colx, lane in self.SEAM:
                lo, hi = pins(net)
                if lo is None or hi is None:
                    log.error(f"ccmp: {net} is not on both comparators")
                    continue
                #- START ON M3, WHICH IS WHERE THE PIN IS. The path's
                #- layer argument does not win over the start rect's
                #- own layer, so `path(net, "M1", ...)` on a pin
                #- LELOTEMP_CCMPR lifted to M3 climbed to M4 and M5
                #- instead of M2 and M3 -- a 72 um M4 riser straight
                #- through the cap bank, and three nets in one
                #- component. Nothing said so; the riser was just on
                #- the wrong layer.
                p = lay.path(net, "M3", start=[lo], stop=[hi],
                             options=narrow)
                p.start()
                p.movex(p.track(net, lane))         #- M3, to the col
                p.down()                            #- M2, up it past
                p.movey(p.landing("y"))             #- the seam
                p.up()                              #- M3, back in
                p.movex(p.landing("x"))
                p.end()
                if net == "PWRUP_B_1V8":
                    self._pwrupb_col = lay.channelTrackCoord(net, lane)

            #- AND PWRUP_B LEAVES THE PAIR HERE, on a pad at the east
            #- edge. Its pin is in the middle of a comparator row and
            #- the row east of it is the other comparator's PWRUP_N bar
            #- on M5, so nothing the level above sends down can land on
            #- the pin -- this was the one pin of the pair it could not
            #- reach. A port in the middle of a block cannot be left
            #- without crossing the block, so it is carried to the edge
            #- here and published in afterPorts.
            from cicpy.core.rect import Rect as _Rect
            lo, _hi = pins("PWRUP_B_1V8")
            col = getattr(self, "_pwrupb_col", None)
            if lo is not None and col is not None:
                #- the row: one lane above the pin, which is where the
                #- crossing story already proved the block is clear.
                pad = _Rect("M3", int(lay.x2) - 4000,
                            int(lo.y1) + 6000, 4000, 3400)
                pad.setNet("PWRUP_B_1V8")
                lay.add(pad)
                p = lay.path("PWRUP_B_1V8", "M2", start=[
                    _Rect("M2", col - 1700, int(lo.y1), 3400, 4000)],
                    stop=[pad], options=narrow)
                p.start()
                p.up()                              #- M3, east
                p.movey(p.landing("y"))
                p.movex(p.landing("x"))
                p.end()
                self._pwrupb_pad = pad

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

            for net, x in ():
                lo, hi = pins(net)
                if lo is None or hi is None:
                    log.error(f"ccmp: {net} is not on both comparators")
                    continue
                p = lay.path(net, "M1", start=[_on_rail(lo, x, net)],
                             stop=[_on_rail(hi, x, net)])
                p.start()
                p.up()                           #- M2, over everything
                p.movey(p.landing("y"))          #- the rails carry
                p.down()
                p.end()


        def afterPorts(self, entry):
            """PWRUP_B, published on the pad its own story drew.

            The pad is MADE and routed to in the routing phase; this
            only names it. A path added in afterPorts never routes --
            the phase is over -- and a port computed from a story's
            endsAt came out as a port rect with nothing under it
            (measured: the pair's port matched nothing at all).
            """
            pad = getattr(self, "_pwrupb_pad", None)
            if pad is None:
                log.error("ccmp: PWRUP_B has no pad to publish")
                return
            self.layout.updatePort("PWRUP_B_1V8", pad,
                                   routeLayer=pad.layer)

        @staticmethod
        def _netRects(layout, net, layer):
            """What this cell holds on `net` -- rects, or anything on
            it when `layer` is None (a cut is an instance, not a
            rect, so a rect search never sees the metal it brings)."""
            out = []

            def walk(o):
                for ch in getattr(o, "children", []) or []:
                    if getattr(ch, "net", "") == net and \
                            (layer is None
                             or getattr(ch, "layer", "") == layer):
                        out.append(ch)
                    elif getattr(ch, "children", None):
                        walk(ch)
            walk(layout)
            return out

    class dig(Stack):
        """The oscillator's logic: OR gate, the cross-coupled NOR
        pair, the two buffers, the powerdown inverter chain."""
        match = r'^(x[1-7]|xtap_dig_\d+)$'
        group = "dig"
        fill = False
        #- SEVEN MICRONS OFF THE PAIR, not four. The pair's east edge
        #- IS the cap bank, and a MiM claims 1.34 um from any
        #- unrelated M4 (capm.11) -- so at four the whole corridor
        #- the two blocks was inside the halo, and every lane a net
        #- came down cost capm.11 (150 boxes), met3.3d and met4.5b.
        #- At seven the corridor's first two lanes are the halo's and
        #- the rest are free; the tile is 159 um, inside its 161.
        xspace = 7
        #- ORDER IS THE ROUTING BUDGET. The powerdown chain used to
        #- sit at the TOP of the strip while the OR gate it drives sat
        #- at the base, so PWRUP_N spanned six cells and 150 um -- and
        #- it was the net stuck on the lane between the two M4 supply
        #- bars, where an input pin has no legal row at all. Put the
        #- chain at the base, beside the gate it feeds, and it becomes
        #- three adjacent cells.
        #-
        #- Total net span, in cells: 12 before, 8 after. Four of the
        #- five nets are now adjacent-cell hops.
        #- A TAP ROW ABOVE x2, for room rather than for taps. The
        #- strip is fully abutted -- the varying pitches are cell
        #- HEIGHTS, ORX1 is 40000 tall, and there is no empty band
        #- anywhere in it. A tapcell makes one: it carries no signal
        #- pin, so no row is booked in it and no via pad sits in it,
        #- and the lanes cross it as bare wire. That is the one place
        #- a leg can cross a lane it does not own -- which is what
        #- PWRUP_B needs to reach the west sliver, and where every
        #- earlier attempt met PWRUP_N's pad at t0.
        order = ['xtap_dig_0', 'x6', 'x2', 'xtap_dig_1', 'x7', 'x3',
                 'x4', 'x1', 'x5']

        #- NETS THAT ESCAPE WEST, ON M4. The strip's west sliver
        #- (exit0, block x 0..31500) is free on M4 for the full
        #- height, and it is the one column a neighbour can reach
        #- without crossing the block: dband has no lane left and
        #- there is no column over the strip on M5. What kept this
        #- from working before was the LAYER -- the walk ends
        #- `up("M5")`, and RST_B's own rungs cross the sliver on M5 at
        #- two heights, so the pad landed on RST_B (measured, one
        #- merged net). One layer down passes under all of them.
        left_exit = ("PWRUP_B_1V8",)

        #- The tapcell is in the schematic now (the CV logic family
        #- carries no taps of its own, and netgen counts the two
        #- tie-off devices), so the stack places it like any other
        #- instance -- first, at the strip's base. It used to be an
        #- addPhysicalInstance here, which became a duplicate the
        #- moment the schematic gained one.

        def beforeRoute(self, entry):
            """The strip's own nets, each on its own lane, told out.

            THE STRIP IS A LADDER and its rungs are stated, not
            searched. Every JNWTR cell puts its pins on M1 in two
            columns -- inputs at 18000, outputs at 36000 -- and
            carries nothing above them but its two M4 supply columns,
            so M2 and M3 are free the strip's whole height. That is
            the whole geometry: a lane per net on M2 east of the
            pins, an M3 stub in to each pin, and one via at each end.

            What it replaces asked `addConnectivityRoute` for a
            vchannel track per net and got `vtrack=16` and `23` out of
            a channel with 16 tracks: RST_A and RST_B were railed
            OUTSIDE the cell, which is why LVS found each of them
            split between its gate side and its drain side, and two
            more gates landed on VSS.

            The lanes are two tracks apart because an M2-M3 pad is
            wider than one lane.
            """
            lay = self.layout
            lay.addRoutingChannel("strip", int(self.x1), int(self.x2),
                                  horizontal=False)
            #- AND THE COLUMNS THE CELLS LEAVE FREE ON M4. Every JNWTR
            #- cell carries a full height M4 supply bar in each of its
            #- two supply columns, and the strip's OUTPUT pins sit
            #- under one of them -- so a port published there can be
            #- met on M2 and by nothing above M3, which is every
            #- neighbour this strip has. Asked of the block view, the
            #- free columns come back measured; a port that cannot
            #- rise where it is rises in the nearest one.
            self._exits = []
            for i, (a, b) in enumerate(lay.freeColumns("M4")):
                nm = f"exit{i}"
                lay.addRoutingChannel(nm, a, b, horizontal=False)
                self._exits.append(nm)
            #- AND THE BANDS BETWEEN THE CELLS. The order leaves real
            #- gaps -- x7 ends at 64000 and x3 starts at 88000 -- and
            #- a gap has no cell in it, so no pin, no booked row and
            #- no via pad: the lanes cross it as bare wire. That is
            #- the one place a leg can cross a lane it does not own.
            #- Measured with M1, which every cell is full of and a
            #- gap has none of.
            self._gaps = []
            for nme in [n for n in self.order if n.startswith("xtap")]:
                inst = lay.getInstanceFromInstanceName(nme)
                if inst is None:
                    continue
                nm = "band_" + nme
                lay.addRoutingChannel(nm, int(inst.y1), int(inst.y2))
                self._gaps.append((nm, int(inst.y1), int(inst.y2)))
            log.info(f"dig: tap bands {self._gaps}")
            #- net, lane, and the hops that make it whole.
            #-
            #- THE SUPPLY COLUMNS ARE NOT FREE ABOVE M1. Every JNWTR
            #- cell carries a full height M4 bar in each of them --
            #- 31500..40300 and 58500..67300 -- with an M1-M4 cut
            #- stack at every rail, so a lane whose M2-M3 pad reaches
            #- into one is tied to that supply. Measured: net2 on a
            #- lane at 57000 came back as part of VDD_1V8. The lanes
            #- below are the ones a 8800 wide pad clears.
            #-
            #- A THREE PIN NET IS NOT THREE HOPS. Two vias on one pin
            #- land concentric but not identical, which magic reports
            #- as "this layer can't abut or partially overlap between
            #- subcells" -- 36 boxes of it. The far pins take the lane
            #- end to end and the middle pin meets the lane where it
            #- passes, which is one via each.
            #- A LANE IS 12000 FROM THE NEXT, not 6000: the via pad
            #- that drops a stub onto a lane is 8800 wide, and at
            #- 6000 spacing it lands on the neighbouring lane's wire
            #- (measured, RST_A's lane and RST_B's pad). What that
            #- leaves, once both M4 supply columns are excluded, is
            #- four lanes -- t0 west of the pins, t7 between the
            #- columns, t13 and t15 east of them. Not t1: the 9600
            #- wide pad that drops a stub on it reaches 13800 and the
            #- input pins start at 13500.
            #-
            #- Four lanes for five nets, so net1 and net2 SHARE one:
            #- one runs y 50..66k and the other 95..118k, and a lane
            #- is only busy where its net is.
            #-
            #- PWRUP_N TAKES THE MIDDLE LANE because it is the one
            #- that can. A lane between the two M4 columns cannot be
            #- reached from M5 (below), so its net's inputs cross on
            #- M3 and are held to the band above each rail -- and
            #- PWRUP_N is the net whose three pins sit in the roomiest
            #- cells. RST_B there left x4 with no row assignment at
            #- all, three stubs into one 24 um cell.
            plan = (("PWRUP_N_1V8", 0, ("x6", "x7"), "x2"),
                    ("RST_A", 0, ("x3", "x4"), None),
                    ("net1", 13, ("x7", "x3"), None),
                    ("net2", 13, ("x1", "x4"), None),
                    ("RST_B", 15, ("x3", "x5"), "x4"))
            #- rows step in SPACE, not in whole lanes: the pins sit
            #- on a 4000 grid and the rows have to interleave with
            #- them, which a 6000 step cannot do -- three pins in one
            #- cell had no assignment at all.
            from cicpy.core.rules import Rules as _Ru
            step = int(_Ru.getInstance().get("M3", "space"))
            #- rows are a PAD APART, not a lane: what has to fit
            #- between two of them is the M2-M3 cut that drops a stub
            #- onto its lane, and a lane's worth (6000) leaves three
            #- stubs of one cell with no assignment at all, because
            #- the pins sit on a 4000 grid and the steps on a 3000
            #- one -- no two rows off different pins ever coincide.
            #- HALF OF EACH PAD, plus half a space. The deck asks
            #- 0.14 um between two M2 shapes; the design's own default
            #- 0.3 um is a preference, and at a full space three stubs
            #- of one 24 um cell have no assignment at all -- the pins
            #- are on a 4000 grid, the steps on a 3000 one, and
            #- nothing lines up. Half of it is 0.15 um, still over
            #- the rule, and it verifies.
            from cicpy.core.cut import Cut as _Cut

            def _cut(a, b):
                return (_Cut.getInstance(a, b, 2, 1)
                        or _Cut.getInstance(b, a, 2, 1))

            def _pad(a, b):
                ct = _cut(a, b)
                return int(ct.height()) if ct is not None else 2 * step

            #- the leg now ends in a cut from li, so the pad that sits
            #- on the row is the M1-to-crossing-layer one, 8800 or
            #- 9600 wide -- three times the leg. Checking the leg
            #- alone left the pads to the GDS.
            def _wide(a, b):
                ct = _cut(a, b)
                return int(ct.width()) if ct is not None else 3000

            pads = {"M3": _pad("M1", "M3"), "M5": _pad("M1", "M5"),
                    "pin": _pad("M1", "M2")}
            wides = {"M3": _wide("M1", "M3"), "M5": _wide("M1", "M5")}
            #- and the space between two rows is the one their
            #- HIGHEST SHARED LAYER asks for. Two M5 pads are thick
            #- metal to each other -- met4.2 wants 0.3 um where
            #- met1.2 wants 0.14 -- but an M5 pad beside an M3 pad
            #- only ever meets it on M2 and M3. Charging every pair
            #- the M5 figure cost x3 its assignment by 100 units.
            #- EVERY PAD HAS AN li PIECE now that the leg starts on
            #- li, so no two rows may come closer than li.3 asks --
            #- 0.17 um, more than the 0.14 the thin metals want, and
            #- the 200 that was missing showed up as 50 li.3 boxes.
            li = 1800
            gaps = {"M3": li, "M5": int(_Ru.getInstance().get(
                "M5", "space")), "pin": li}

            #- li has a rule of its own -- li.3 asks 0.17 um, more
            #- than the 0.14 the metals do -- and the leg and the
            #- pads that sit on it are li, so anything measured
            #- against a PIN is measured with that.
            def _gap(l1, l2):
                if "pin" in (l1, l2):
                    return gaps["pin"]
                return gaps[l1] if l1 == l2 else max(li, min(gaps[l1],
                                                             gaps[l2]))
            pitch = lay._lanePitch("M2")
            m5 = {}
            wanted = []
            self._lanes = {n: l for n, l, _h, _m in plan}
            for net, _lane, (src, dst), mid in plan:
                x = lay.channelTrackCoord("strip", _lane)
                ok = x is not None and self._m5Lane(lay, x)
                for inst in (src, dst) + ((mid,) if mid else ()):
                    r = self._pin(lay, inst, net)
                    if r is None:
                        continue
                    m5[(net, inst)] = self._crossLayer(r, ok)
                    wanted.append(((net, inst), r, m5[(net, inst)],
                                   int(x) if x is not None else 0))
            for net in ("CMPO_A", "CMPO_B", "OSC_TEMP_1V8", "PWRUP_1V8",
                        "PWRUP_B_1V8", "PWRUP_N_1V8", "RST_A", "RST_B"):
                inst, pin = self._anyPin(lay, net)
                if pin is not None and (net, inst) not in \
                        {(k[0], k[1]) for k, _r, _l, _x in wanted}:
                    wanted.append(((net, "^" + inst), pin, "M3",
                                   int(pin.centerX())))
            rows = self._bookRows(step, pads, wides, _gap, wanted)

            def row(net, inst):
                return rows.get((net, inst), (1, 0))

            for net, lane, (src, dst), mid in plan:
                a, b = self._pin(lay, src, net), self._pin(lay, dst, net)
                if a is None or b is None:
                    log.error(f"dig: {net} is not on {src} and {dst}")
                    continue
                p = lay.path(net, "M1", start=[a], stop=[b])
                p.start()
                #- STEP OFF THE PIN ROW BEFORE TURNING. A cell puts
                #- its input at 18000 and its output at 36000 only a
                #- row or two apart in y, so two nets' stubs leaving
                #- at their own pin rows ran 600 apart across the VSS
                #- column -- ten met1.2 and met2.2 pairs, no short.
                #- Inputs step down and outputs step up, which puts
                #- two lanes between the families wherever they cross.
                ka, _ = row(net, src)
                kb, _ = row(net, dst)
                #- THE LEG TO THE ROW IS li. It used to via up to M2
                #- at the pin and up again at the row, one step away
                #- -- two cuts whose pads overlapped, on a leg 3000
                #- long. The pin is li, the column is li, and li is
                #- the ONE layer these cells publish: the row search
                #- can check the leg against the real geometry, which
                #- it cannot do on M2 or M3.
                p.movey(p.pin(src, net, "y") + ka * p.SPACE)
                p.up(m5[(net, src)])              #- east, over or
                p.movex(p.track("strip", lane))   #- under the rails
                #- RIDE THE LANE FIRST, ALWAYS. On a row of its own
                #- the turn is obvious; on the pin's own row (k=0) it
                #- is easy to leave out, and then the vertical
                #- happens at the far pin's x instead -- measured,
                #- 155 um of M2 down the output column, five nets in
                #- one component.
                p.down("M2")             #- the lane
                p.movey(p.landing("y") + kb * p.SPACE)
                p.up(m5[(net, dst)])              #- in to the other
                p.movex(p.landing("x"))           #- pin
                #- and down to li in one cut, so end() draws the last
                #- leg on the pin's own layer
                p.down("M1")
                p.end()
                if mid is None:
                    continue
                m = self._pin(lay, mid, net)
                if m is None:
                    log.error(f"dig: {net} is not on {mid}")
                    continue
                #- the middle pin meets the lane, not the other pins
                x = lay.channelTrackCoord("strip", lane)
                if x is None:
                    continue
                km, y = row(net, mid)
                from cicpy.core.rect import Rect as _R
                meet = _R("M2", int(x) - pitch // 2, y - pitch // 2,
                          pitch, pitch)
                meet.setNet(net)
                p = lay.path(net, "M1", start=[m], stop=[meet])
                p.start()
                p.movey(p.pin(mid, net, "y") + km * p.SPACE)
                p.up(m5[(net, mid)])
                p.movex(p.track("strip", lane))
                p.end()
            self._promote(lay, step, pads, wides, _gap, rows)
            #- TRUE CLAIMS THE STRIP. Everything else it holds is a
            #- port on one pin -- CMPO_A, CMPO_B, OSC_TEMP_1V8,
            #- PWRUP_1V8, PWRUP_B_1V8 -- and the supplies are the M4
            #- columns, which the cells abut into each other.
            return True

        @staticmethod
        def _step(pin):
            """Which way a stub prefers to leave its pin: inputs down,
            outputs up. The two pin columns are 13500..22500 and
            31500..40500."""
            return -1 if int(pin.x1) < 25000 else 1

        #- EVERY STUB CROSSES ON M3, under the M4 supply bars and
        #- between the rails.
        #-
        #- M5 looks better -- it is free the strip's whole height and
        #- an input pin, at 13500..22500, is clear of both M4 columns
        #- and could climb to it. What kills it is the via at the
        #- other end: an M2-M5 cut carries an M4 pad 10800 wide with
        #- its enclosure, so a lane anywhere in the 18 um between the
        #- two M4 columns lands that pad ON one of them. Measured --
        #- RST_B on the middle lane came back shorted to VSS. There
        #- is no track in that band where it fits, so the layer that
        #- can use the band is the one that never reaches M4.
        def _m4columns(self, lay):
            """The M4 supply bars, off the cells' own ports."""
            cols = []
            for inst in self.instances:
                ports = getattr(inst, "instancePorts", {}) or {}
                for net in ("VDD_1V8", "VSS"):
                    port = ports.get(net)
                    r = port.get() if port is not None else None
                    if r is not None and r.layer == "M4":
                        cols.append((int(r.x1), int(r.x2)))
            return cols

        def _m5Lane(self, lay, x):
            """Can a stub drop onto the lane at `x` from M5?

            Only if the M4 pad the cut carries clears both supply
            bars. That is the whole reason the middle lane is M3
            only.
            """
            from cicpy.core.cut import Cut as _Cut
            from cicpy.core.rules import Rules as _Ru
            ct = (_Cut.getInstance("M2", "M5", 2, 1)
                  or _Cut.getInstance("M5", "M2", 2, 1))
            if ct is None:
                return False
            half = int(ct.width()) // 2 + int(_Ru.getInstance().get(
                "M4", "space"))
            return all(x + half < c1 or x - half > c2
                       for c1, c2 in self._m4columns(lay))

        def _crossLayer(self, pin, m5ok):
            """An input crosses above everything on M5 when its lane
            can take the drop; an output cannot -- its pin IS the VSS
            column, so it can never pass M4 there -- and crosses on
            M3, under the bars and between the rails."""
            return "M5" if (m5ok and int(pin.x1) < 25000) else "M3"

        def _bookRows(self, step, pads, wides, gapfor, pins):
            """A stub row for every pin at once, as step counts.

            SOLVED FOR THE WHOLE STRIP, NOT HANDED OUT AS ASKED. Four
            things decide whether a row is legal, and each one cost a
            build to find:

            * an M3 row must clear the cell's own rail -- every JNWTR
              cell carries an M1-M4 cut stack 2500..4200 above its
              bottom edge. An M5 row is above all of that.
            * the leg that reaches the row runs up the pin column, so
              the row may not sit on the far side of another pin in
              that column, nor close enough for its pad to touch one.
            * two rows keep half of each pad plus the space their
              highest shared layer asks for. The pads are not one
              size: the cut that reaches M5 is 4800 tall where the
              one that reaches M3 is 3400.
            * and rows in ADJACENT CELLS see each other -- solved a
              cell at a time, RST_A's row at the top of x3 and
              RST_B's at the bottom of x4 came out 4000 apart with
              two M5 pads on them.

            First-come-first-served fails on the first two cells: it
            takes the middle row and leaves the last pin nothing. So
            every pin is collected first and the whole strip is
            solved by search, shortest legs preferred.
            """
            cells = [(int(i.y1), int(i.y2)) for i in self.instances]
            #- WHAT THE LEG HAS TO MISS, from the cells themselves.
            #- A JNWTR cell publishes its li -- and only its li, which
            #- is why this check exists for M1 and for nothing else.
            #- A NET'S OWN PINS ARE NOT OBSTACLES TO IT; every other
            #- net's are. Excluding all of them at once let RST_B's
            #- leg sit 1000 under the pin it shares a column with,
            #- which is 50 li.3 boxes and no short.
            own = {}
            for (n, _i), r, _l, _x in pins:
                own.setdefault(n, set()).add(
                    (int(r.x1), int(r.y1), int(r.x2), int(r.y2)))
            #- WHAT IS IN THE WAY, FROM THE CELLS THEMSELVES. Not
            #- their children -- a JNWTR cell's children are its pins
            #- and its two M4 bars, and the M2 and M3 of its M1-M4
            #- stacks are in the cells it uses. `blockCell()` is that
            #- view: metal and cuts, at every depth, in the cell's own
            #- frame.
            #-
            #- It replaces two things this used to guess. The li leg
            #- was checked against published M1 alone, which was all
            #- there was; and a stub's row had to clear its cell's
            #- rail by 7800, a number measured off DRC boxes rather
            #- than read off the rail.
            blocked = {}
            for inst in self.instances:
                sub = (getattr(inst, "layoutcell", None)
                       or getattr(inst, "_cell_obj", None))
                if sub is None or not hasattr(sub, "blockCell"):
                    continue
                for r in sub.blockCell().rects(int(inst.x1),
                                               int(inst.y1)):
                    blocked.setdefault(r.layer, []).append(
                        (int(r.x1), int(r.y1), int(r.x2), int(r.y2)))
            m1 = blocked.get("M1", [])
            #- A NET OWNS WHAT TOUCHES ITS PINS. The li that reaches a
            #- pin is drawn inside the cell, at a depth where it is
            #- just another rect -- (36000,50500,43500,53500) is the
            #- OR gate's output conductor, overlapping the pin and
            #- three microns longer. Compared box for box it reads as
            #- somebody else's metal, and every candidate row for
            #- every output pin was rejected against the pin's own
            #- wire. Flood the ownership out from each pin instead,
            #- which is what the router's own attribution does.
            for net, boxes in own.items():
                grown, wave = set(boxes), list(boxes)
                while wave:
                    a = wave.pop()
                    for o in m1:
                        if o in grown:
                            continue
                        if o[0] < a[2] and a[0] < o[2] \
                                and o[1] < a[3] and a[1] < o[3]:
                            grown.add(o)
                            wave.append(o)
                own[net] = grown

            def hits(layer, box, space, mine=()):
                x1, y1, x2, y2 = box
                return any(o not in mine
                           and o[0] < x2 + space and x1 - space < o[2]
                           and o[1] < y2 + space and y1 - space < o[3]
                           for o in blocked.get(layer, []))

            def leg_clear(net, r, y, half, wide, space, layer, lane):
                """The whole stub, against everything below.

                Three shapes, and each one used to be a separate
                guess: the li leg from the pin up to its row, the pad
                that ends it -- which spans every layer from li to the
                crossing one -- and the crossing run itself, from the
                pin's column out to its lane. That last one is the
                check that replaces the rail band: it asks the rail
                whether it is in the way instead of assuming where it
                is.
                """
                mine = own.get(net, set())
                cx = int(r.centerX())
                leg = (cx - 1500, min(int(r.y1), y),
                       cx + 1500, max(int(r.y2), y))
                if hits("M1", leg, space, mine):
                    return False
                pad = (cx - wide // 2, y - half, cx + wide // 2, y + half)
                stack = ["M1", "M2", "M3"]
                if layer == "M5":
                    stack += ["M4", "M5"]
                for l in stack:
                    if hits(l, pad, space, mine):
                        return False
                run = (min(cx, lane), y - 1500, max(cx, lane), y + 1500)
                return not hits(layer, run, space)

            cand = []
            for key, r, layer, lane in pins:
                y0 = int(r.centerY())
                #- `band`, not `own`: `own` is the pins each net may
                #- land on, which is what leg_clear needs to know to
                #- tell its own metal from everyone else's.
                band = next(((a, b) for a, b in cells if a <= y0 <= b),
                            None)
                if band is None:
                    log.error(f"dig: a pin at {y0} is in no cell")
                    continue
                #- the row stays inside the pin's own cell, because
                #- the leg that reaches it runs up the pin column
                #- where every other net's pins are. How far it must
                #- keep off the cell's rail is no longer a number
                #- here: leg_clear asks the rail.
                lo, hi = band[0] + 1100, band[1] - 1100
                half = pads[layer] // 2
                #- the other pins of this column, in this cell
                others = [int(o.centerY()) for k2, o, _l, _x in pins
                          if k2 != key and band[0] <= int(o.centerY())
                          <= band[1] and abs(int(o.x1) - int(r.x1)) < 9000]
                s0 = self._step(r)
                #- NEVER ONE STEP OFF THE PIN. The pad that ends the
                #- leg is as wide as the pin and the leg is a third of
                #- that, so at one step the pad's li stops 700 short
                #- of the pin and leaves a 0.33 um notch either side of
                #- the leg -- li.3 wants 0.17. Two steps and the gap
                #- is 2900, clear.
                #- k=0 IS THE BEST ROW: the cut lands on the pin, one
                #- cut and no leg at all, and the pad is the pin's own
                #- width. It is tried first, and it is the only row a
                #- 16 um cell has room for.
                cs = []
                for k in [0] + list(range(2, 12)):
                    for sign in (s0, -s0):
                        y = y0 + sign * k * step
                        if not lo <= y <= hi:
                            continue
                        if any(min(y0, y) < o < max(y0, y)
                               for o in others):
                            continue
                        if any(abs(y - o) < half + pads["pin"] // 2
                               + gapfor(layer, "pin") for o in others):
                            continue
                        #- AND ASK THE CELLS. Everything above is what
                        #- the pins say; this is what the geometry
                        #- says, at every depth -- the leg, the pad
                        #- and the run across the supply columns.
                        if not leg_clear(key[0], r, y, half,
                                         wides[layer],
                                         gapfor(layer, "pin"),
                                         layer, lane):
                            continue
                        cs.append((sign * k, y))
                        if k == 0:
                            break
                #- the row's x EXTENT, not its pin: what it occupies
                #- is the run from the pin out to its lane
                cx = int(r.centerX())
                cand.append((key, half, layer, y0,
                             (min(cx, lane) - wides[layer] // 2,
                              max(cx, lane) + wides[layer] // 2), cs))

            #- the pin with the fewest ways to go decides first
            cand.sort(key=lambda c: len(c[5]))
            taken, chosen = [], {}

            def place(i, ease):
                if i == len(cand):
                    return True
                key, half, layer, y0, span, cs = cand[i]
                for k, y in cs:
                    #- TWO ROWS SEE EACH OTHER WHERE THEY OVERLAP IN X,
                    #- and a row reaches from its pin all the way to
                    #- its lane. Compared at the PIN alone, an output
                    #- row and an input row read as different columns
                    #- -- and then RST_A's run west to its lane passed
                    #- 100 under net2's pad on the way (met2.2).
                    if any(span[0] < tsp[1] and tsp[0] < span[1]
                           and abs(y - t) < ease * (half + th
                                                    + gapfor(layer, tl))
                           for t, th, tl, tsp in taken):
                        continue
                    taken.append((y, half, layer, span))
                    chosen[key] = (k, y)
                    if place(i + 1, ease):
                        return True
                    taken.pop()
                    del chosen[key]
                return False

            #- GIVE GROUND IN ORDER, rather than all at once. The
            #- strip does not always have an assignment at full
            #- spacing -- x3 and x4 between them are 12 um of band for
            #- six stubs -- and the fallback used to be "first
            #- candidate each", which throws away the constraint
            #- entirely. Easing the separation a step at a time keeps
            #- the best assignment that does exist, and says by how
            #- much it had to give.
            for ease in (1.0, 0.9):
                taken.clear()
                chosen.clear()
                if place(0, ease):
                    if ease < 1.0:
                        log.warning(f"dig: rows fit at {ease:.0%} of "
                                    f"the spacing, not at full")
                    break
            else:
                log.error("dig: no row assignment for the strip; "
                          + repr([(k, l, x, [c[1] for c in cs])
                                  for k, _h, l, _y, x, cs in cand]))
                #- A PIN WITH NO LEGAL ROW FALLS BACK TO ITS OWN.
                #- k=0 is one cut on the pin and no leg at all, which
                #- is the least a stub can be; the old fallback took
                #- k=1 and put the pad three microns up, on whatever
                #- was there.
                for key, _half, _layer, _y, _x, cs in cand:
                    if not cs:
                        log.warning(f"dig: {key[0]} has no legal row on "
                                    f"{key[1]}; on its own pin instead")
                    chosen.setdefault(key, cs[0] if cs else (0, 0))
            return chosen

        def afterPorts(self, entry):
            """Publish the pads the promotion drew."""
            lay = self.layout
            for net, pad in (getattr(self, "_pads", None) or {}).items():
                lay.updatePort(net, pad, routeLayer=pad.layer)

        def _exitLane(self, lay, net, x):
            """Where this port may rise to M5, and whether it travels.

            M5 IS THE ONE LAYER THESE CELLS DO NOT USE, so a port on it
            can be met from anywhere above. What stops a port rising
            where it stands is the cells' own supply bars -- full
            height M4, one per supply column -- and the strip's OUTPUT
            pins sit inside one, so a stack from above lands on VSS.

            Three answers, in the order that costs least:

              * the pin's own column is free: rise on the spot, no leg.
              * the net has a LANE in the strip: it already has metal
                in a free column, so rise there. Still no leg -- the
                lane is the route it was going to take anyway.
              * neither: the nearest free column, and a leg to it.
                Measured, that leg is the expensive one -- on M2 it
                crosses the strip's lanes, on M3 the supply column's
                own via stacks -- so it is what the two nets that have
                no lane pay, and nothing else.

            Returns (x, travels) -- WHERE THE METAL ALREADY IS, so
            the rise is a cut and nothing else. Answering with a lane
            index instead put the pad at the lane and the cut at the
            pin, and the port came back on a piece of metal joined to
            nothing (measured: RST_B, one net split).
            """
            if net in getattr(self, "left_exit", ()):
                #- straight to the sliver, whatever else it stands in
                cols = [(lay.routingChannel(nm), nm)
                        for nm in getattr(self, "_exits", [])]
                cols = [(int(c[0]), int(c[1]), nm)
                        for c, nm in cols if c is not None]
                if cols:
                    #- THE WESTMOST TRACK, not the middle of the
                    #- sliver. exit0 is 0..31500 but the strip's lane
                    #- t0 runs down it at ~13200, and a pad centred in
                    #- the column lands on it -- measured, PWRUP_B
                    #- merged with PWRUP_N, which is what t0 carries.
                    #- Hard against the west edge there is nothing.
                    #- HALF A PAD IN FROM THE EDGE. The westmost
                    #- track hangs the pad at x=-3200, outside the
                    #- block; the middle of the sliver lands on lane
                    #- t0 at 13200. Half a pad in puts it at 0..8800,
                    #- inside the block and 4400 clear of the lane.
                    from cicpy.core.cut import Cut as _C
                    _c = (_C.getInstance("M1", "M5", 2, 1)
                          or _C.getInstance("M5", "M1", 2, 1))
                    w = int(_c.width()) if _c is not None else 8800
                    lo, hi, nm = min(cols)
                    idx = lay.channelTrackNear(nm, lo + w // 2)
                    c = int(lay.channelTrackCoord(nm, idx))
                    #- the grid has no track that far in, so clamp:
                    #- a pad half outside the block is not a port.
                    return max(c, int(lo) + w // 2), True
            for nm in getattr(self, "_exits", []):
                ch = lay.routingChannel(nm)
                if ch and int(ch[0]) <= x <= int(ch[1]):
                    return x, False
            lane = getattr(self, "_lanes", {}).get(net)
            if lane is not None:
                #- the net's own lane, at this port's row: its stub
                #- runs from the pin to the lane on exactly that row,
                #- so there is M2 there to rise from
                return int(lay.channelTrackCoord("strip", lane)), False
            #- TO A COLUMN NOBODY ELSE IS USING, and one track each.
            #- The nearest free column to an output pin is the one the
            #- input pins and lane t0 are in, and a leg reaching it
            #- crosses whatever t0 carries -- measured, OSC_TEMP walked
            #- west across PWRUP_N and took VSS with it. And two nets
            #- that walk to the same track short to each other. So:
            #- columns with no lane in them first, nearest first; and
            #- within one, out from the middle, first free -- the
            #- middle because the column's walls ARE the supply bars,
            #- and a cut against one left its M4 pad 300 from met3.2's
            #- 3000.
            taken = [int(lay.channelTrackCoord("strip", l))
                     for l in set(getattr(self, "_lanes", {}).values())]
            used = getattr(self, "_walked", None)
            if used is None:
                used = self._walked = set()
            cols = []
            for nm in getattr(self, "_exits", []):
                ch = lay.routingChannel(nm)
                if ch is None:
                    continue
                lo, hi = int(ch[0]), int(ch[1])
                busy = any(lo <= t <= hi for t in taken)
                cols.append((1 if busy else 0,
                             min(abs(lo - x), abs(hi - x)), nm, lo, hi))
            pitch = lay._lanePitch(None) or 1
            for _b, _d, nm, lo, hi in sorted(cols):
                n = max(1, int((hi - lo) // pitch))
                mid = lay.channelTrackNear(nm, (lo + hi) // 2)
                for idx in sorted(range(n), key=lambda i: abs(i - mid)):
                    if (nm, idx) in used:
                        continue
                    used.add((nm, idx))
                    return int(lay.channelTrackCoord(nm, idx)), True
            log.error(f"dig: no free track to walk {net} out on")
            return None

        def _promote(self, lay, step, pads, wides, gapfor, rows):
            """Every signal port up to M2, before anyone above sees it.

            A JNWTR cell puts its pins on li and the strip published
            them as it found them, so all eight of this cell's signals
            arrived at the top on the ONE layer the design reserves
            for power. The level above then has to meet li -- eight
            times, across a tile.

            So each port is carried up here instead, on a row booked
            like any other stub and with the same three checks against
            the cells' own geometry. What leaves this cell is an
            ordinary M2 pad on the vertical layer, which is what the
            strip's neighbours can route to.
            """
            from cicpy.core.rect import Rect as _R
            self._pads = {}
            for net in ("CMPO_A", "CMPO_B", "OSC_TEMP_1V8", "PWRUP_1V8",
                        "PWRUP_B_1V8", "PWRUP_N_1V8", "RST_A", "RST_B"):
                inst, pin = self._anyPin(lay, net)
                if pin is None:
                    log.error(f"dig: no pin to promote for {net}")
                    continue
                #- A NET THE STRIP ALREADY ROUTES HAS A PAD ALREADY.
                #- Its stub left the pin through a cut that spans M1
                #- to M3 or M5, so there is M2 on that row and the
                #- port is simply that. Drilling a second via six
                #- microns away instead put two mcon arrays 1700
                #- apart where mcon.2 wants 1900 -- 18 boxes, for
                #- geometry that was already there.
                routed = rows.get((net, inst))
                if routed is not None:
                    k, y = routed
                else:
                    k, y = rows.get((net, "^" + inst),
                                    (0, int(pin.centerY())))
                    p = lay.path(net, "M1", start=[pin], stop=[pin])
                    p.start()
                    if k:
                        p.movey(p.pin(inst, net, "y") + k * p.SPACE)
                    p.up("M2")
                #- AND ON UP TO M5, where the strip's neighbours can
                #- meet it. An M2 pad is what a JNWTR cell gives and
                #- what nothing above M3 can land on when the pin sits
                #- under a supply bar.
                seed = _R("M2", int(pin.centerX()) - wides["M3"] // 2,
                          y - pads["M3"] // 2, wides["M3"], pads["M3"])
                seed.setNet(net)
                where = self._exitLane(lay, net, int(pin.centerX()))
                if where is None:
                    self._pads[net] = seed
                    continue
                px, travels = where
                #- CROSS IN THE TAP BAND, not at the pin's row. The
                #- leg west has to pass lane t0, which is PWRUP_N's,
                #- and at this net's own row PWRUP_N's via pad is
                #- 4000 away with pads 9600 tall -- they overlap and
                #- the two nets merge. The tap row above has no
                #- signal pin in it, so nothing is booked there and
                #- the lanes cross it as bare wire.
                ty, band = y, None
                if net in self.left_exit and self._gaps:
                    band, ba, bb = min(
                        self._gaps,
                        key=lambda g: abs((g[1] + g[2]) // 2 - y))
                    ty = (ba + bb) // 2
                seed = _R("M2", px - wides["M3"] // 2,
                          ty - pads["M3"] // 2, wides["M3"], pads["M3"])
                seed.setNet(net)
                #- A NET WITH NEITHER A FREE PIN NOR A LANE has to
                #- walk to a free column, and the walk is on M3: M2 is
                #- what the strip's lanes are and a leg across them on
                #- their own layer shorts every one it passes. On M3
                #- what it crosses is the supply column, whose stacks
                #- are at the rails -- not at a booked signal row.
                if travels:
                    #- ON ITS SIDE: the column between the two supply
                    #- bars is 13700 wide and a default cut's pad is
                    #- 8800, so two walkers in it overlapped each
                    #- other and came within 300 of a bar (met3.2
                    #- wants 3000). Turned, the same cuts are 3200.
                    #- FROM THE M2 PAD, not from the pin: starting on
                    #- the pin makes the first cut an li one, and the
                    #- turned cut is below mcon's own minimum width
                    #- (22 mcon.1 boxes). The M2 is already there --
                    #- the stub that promoted the pin drew it.
                    home = _R("M2", int(pin.centerX()) - wides["M3"] // 2,
                              y - pads["M3"] // 2, wides["M3"],
                              pads["M3"])
                    home.setNet(net)
                    q = lay.path(net, "M2", start=[home], stop=[seed],
                                 options="1cuts,2vcuts")
                    q.start()
                    q.up("M3")
                    if band is not None:
                        #- TWO WALLS, CROSSED IN DIFFERENT PLACES. The
                        #- supply column is crossed at the PIN'S row,
                        #- where its via stacks are only at the rails;
                        #- inside a tapcell the whole cell is supply
                        #- and a leg across it at any row lands on VSS
                        #- (measured -- x2's output pair joined VSS).
                        #- The LANE is crossed in the tap band, where
                        #- nothing is booked. So: west at this row to
                        #- the strip between the lane and the column,
                        #- up into the band, then on west.
                        t0 = int(lay.channelTrackCoord("strip", 0))
                        ch0 = lay.routingChannel(self._exits[0])
                        stop = int(ch0[1]) if ch0 else t0
                        q.movex(q.track(self._exits[0],
                                        lay.channelTrackNear(
                                            self._exits[0],
                                            (t0 + stop) // 2)))
                        q.movey(q.track(band, lay.channelTrackNear(
                            band, ty)))
                    q.movex(q.landing("x"))
                    #- AND IT STOPS ON M3. The walk is already there
                    #- -- M3 is what carries it west under RST_B's M5
                    #- rungs -- so rising again only puts the pad one
                    #- layer up, against the supply columns, where the
                    #- search can reach the port's x and y exactly (0
                    #- away, on M3) and then not via up to it.
                    if net not in self.left_exit:
                        q.up("M5")
                else:
                    #- and NOT turned for a port that rises where it
                    #- stands: on its own pin or its own lane there is
                    #- room for the default cut, and the narrow one
                    #- cost 32 DRC of its own.
                    q = lay.path(net, "M2", start=[seed], stop=[seed])
                    q.start()
                    q.up("M5")
                pad = _R("M3" if net in self.left_exit else "M5",
                         px - wides["M3"] // 2,
                         ty - pads["M3"] // 2, wides["M3"], pads["M3"])
                pad.setNet(net)
                #- SAID IN afterPorts, NOT HERE. addAllPorts runs
                #- after routing and takes the first rect it finds on
                #- the net, so a port set now is overwritten before
                #- the cell is published -- measured, six of these
                #- eight went back to li.
                self._pads[net] = pad

        @staticmethod
        def _anyPin(lay, net):
            """The first instance carrying `net`, and its pin."""
            for inst in lay.instances if hasattr(lay, "instances") else []:
                pass
            for name in ("x1", "x2", "x3", "x4", "x5", "x6", "x7"):
                inst = lay.getInstanceFromInstanceName(name)
                if inst is None:
                    continue
                port = (getattr(inst, "instancePorts", {}) or {}).get(net)
                if port is not None:
                    return name, port.get()
            return None, None

        @staticmethod
        def _pin(lay, instname, net):
            """One instance's pin on `net`, as placed."""
            inst = lay.getInstanceFromInstanceName(instname)
            if inst is None:
                return None
            port = (getattr(inst, "instancePorts", {}) or {}).get(net)
            return port.get() if port is not None else None

    #- THE STRIP SITS ON THE PAIR, not beside it. Side by side, the
    #- only corridor between them is the 4 um gap at the pair's east
    #- edge -- and that edge is the cap bank, whose MiM claims 1.34 um
    #- from any unrelated M4. Every lane in that gap was inside
    #- the halo: 150 capm.11 boxes, and met3.3d and met4.5b with them.
    #- Above the pair there is 26 um of empty tile, the strip is 18
    #- tall, and the nets it shares with the pair (CMPO_A/B, RST_A/B)
    #- stop being a journey at all. The tile gets narrower too: 142 um
    #- against 156, inside a 161 um budget either way.
    rows = [
        [bias, ccmp, dig],
    ]

    supplies = []

    #- the subcell classes above are what make this cell MADE OF
    #- SUBCELLS: hierarchy() splits the netlist, builds a cell per
    #- subcell, and the top instantiates them and routes between
    #- their ports. `routes` only declares the channel routes that
    #- join them, and this top has none -- _signals() lays its
    #- crossing nets instead, as a hand lane plan.
    #- WHICH ROUTING RUNS. Both of these exist to bisect a short:
    #- take routing away until it goes, then put it back one at a
    #- time with DRC and LVS between each.
    _PHASES = ("supplies","ibp","antenna")
    #- see _signals: None draws every story in the phase
    _ONLY = ()

    routes = []

    def afterPlace(self, layout):
        super().afterPlace(layout)
        #- DROP EVERY BLOCK 0.13 um, to buy the top band its
        #- clearance. The lanes over the bias block need 0.40 under
        #- the first one (met4.5a/b, "large metal4" = cicpy M5), and
        #- between the block's top and the 111.52 um tile ceiling
        #- there was 2.76 where 2.89 was wanted. Everything else is
        #- already at its minimum, so the room comes from below --
        #- the rings are laid on the INSTANCES' own bbox (see
        #- beforeRoute), so they come down with the blocks.
        for _n in ("xbias", "xccmp", "xdig"):
            _i = layout.getInstanceFromInstanceName(_n)
            if _i is not None:
                _i.translate(0, -1300)
        #- the move leaves every group's stored extent where base
        #- place scattered it, and the ring wraps THAT box: refresh
        for grp in layout.cellgroups:
            grp.updateBoundingRect()
        layout.updateBoundingRect()

        #- THE BANDS, NAMED. Every corridor this floorplan opens is
        #- registered here, so a route can aim at "dband track 1"
        #- instead of at a coordinate -- a track index survives a
        #- resize and another technology, and 1419800 + 6000 does not.
        #-
        #- They used to be keyed on x1_ibp, x2_ccmp and x7, which are
        #- inside the three blocks now and not instances of this cell
        #- at all. The whole registration was guarded by `if None not
        #- in (...)` and so registered NOTHING, quietly, from the day
        #- the subcells appeared.
        bi = layout.getInstanceFromInstanceName("xbias")
        cc = layout.getInstanceFromInstanceName("xccmp")
        dg = layout.getInstanceFromInstanceName("xdig")
        if None in (bi, cc, dg):
            log.error("top: the three blocks are not all placed")
            return
        #- the two vertical gaps the floorplan opens, and the free
        #- band above each of the short blocks
        layout.addRoutingChannel("lband", int(bi.x2), int(cc.x1),
                                 horizontal=False)
        layout.addRoutingChannel("dband", int(cc.x2), int(dg.x1),
                                 horizontal=False)
        layout.addRoutingChannel("cband", int(cc.y2), int(bi.y2))
        layout.addRoutingChannel("sband", int(dg.y2), int(bi.y2))

        #- THE ANTENNA DIODES STAND IN THE FLOOR OF `dband`, which is
        #- the one part of this tile that is empty at every layer.
        #- They are in the SCHEMATIC -- a diode extracts as a DEVICE
        #- and LVS counts devices -- and the schematic says nothing
        #- about where a device goes, so `place` has no row for them
        #- and drops them above the floorplan. Left there they are not
        #- merely misplaced: the tile has a 111.52 um ceiling, the
        #- bbox grew to 117.39, and the rings and both supply ports
        #- followed the bbox up with it.
        #-
        #- ONE DIODE PER LANE, EACH UNDER ITS OWN. The two violations
        #- are CMPO_A's and CMPO_B's M4, and each of those nets holds
        #- a full-height lane of this channel -- so a diode standing
        #- at the foot of the lane reaches the offending metal on a
        #- riser that never leaves it. The tracks are the ones
        #- `_signals` sends the descents down (4 and 6), which is what
        #- makes the riser straight; naming the track twice is the
        #- statement that they are the same lane.
        #-
        #- AND THEY STACK, they do not stand side by side. The drawn
        #- guard rings are 1.83 um across against a 1.2 um lane pitch,
        #- so two at one height would overlap outright. The lower one
        #- sits in the clear box below every descent (measured with
        #- `blockers`: x 1425000..1489000 by y 16000..53000 holds
        #- nothing on any layer), the upper one above it -- and the
        #- lane a diode stands under is free at that height precisely
        #- because its own descent stops higher up: CMPO_B's M4
        #- begins at 82200 and CMPO_A's at 170200.
        #- (track, height above the blocks' own floor)
        for name, track, y in (("xant_cmpo_b", 4, 10000),
                               ("xant_cmpo_a", 6, 40000)):
            ant = layout.getInstanceFromInstanceName(name)
            if ant is None:
                log.error(f"top: the antenna diode {name} is not placed")
                continue
            #- OFF THE FLOOR AND OFF EACH OTHER, both by p-select.
            #- The cell's guard ring overhangs its abutment box by
            #- 0.265 um on every side and its psubdiff generates
            #- psdm, which owes 0.38 to anybody else's -- psdm.1, the
            #- same rule that rode inside the bandgap unseen. 25000
            #- clears the blocks' floor by a micron; the 30000
            #- between the two clears their rings by 0.765.
            ant.translate(int(layout.channelTrackCoord("dband", track)
                              - ant.centerX()),
                          int(int(cc.y1) + y - int(ant.y1)))
        for grp in layout.cellgroups:
            grp.updateBoundingRect()
        layout.updateBoundingRect()

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
        #- THE TOP'S SIGNAL NETS ARE A HAND LANE PLAN, not a search.
        #- Handing every one of them to the maze router instead was
        #- measured and lost: the top level does not know which layers
        #- the BLOCKS own, so on M3 it ran into LELOTEMP_CMP's own
        #- VBP2, and confined to M4/M5 it had two layers for twenty
        #- nets that then crossed each other. Every variant collapsed
        #- into one component holding thirty-odd nets. What _signals()
        #- encodes is exactly what the search lacks -- a lane budget
        #- and a layer reservation per band.
        #- ONE PHASE AT A TIME, same reason as `_ONLY` below: a short
        #- is found by taking routing AWAY until it goes.
        for name in self._PHASES:
            getattr(self, "_" + name)(layout)
        super().beforeRoute(layout)

    def afterPorts(self, layout):
        """SAY WHICH RECT IS THE SUPPLY PIN. Do not let it be found.

        `afterPorts` on the recipe places supply ports on the bulk
        column -- but only for a cell built as a PIECE, and this one
        is the top, so it returns early and the two supplies keep
        whatever `addAllPorts` picked, which is the FIRST rect on the
        net. That is iteration order, and it held only by luck.

        The luck ran out when the antenna diodes arrived. Each one
        ties its guard ring to VSS, and one of those rings became the
        rect published as this tile's ground pin: a 1.47 x 0.17 um
        patch of li at (145.1, 5.4) um, in the middle of the floor
        between two blocks, in place of the 96 um bar along the
        bottom. Nothing in the flow complains -- DRC, LVS and the
        antenna check all pass, because all three are about this
        cell's inside, and a port is a promise to whatever instantiates
        it. The harness that lands on that pin is not in this repo.

        So the tile names them: the bias block's own two bars, which
        are what the rings run to and where the committed layout had
        them.
        """
        super().afterPorts(layout)
        bias = layout.getInstanceFromInstanceName("xbias")
        if bias is None:
            log.error("top: no bias block to take the supply pins from")
            return
        for net, pick in (("VDD_1V8", lambda rs: max(rs, key=lambda r: int(r.y1))),
                          ("VSS", lambda rs: min(rs, key=lambda r: int(r.y1)))):
            r = self._port(bias, net, pick)
            if r is None:
                log.error(f"top: the bias block has no {net} bar to publish")
                continue
            layout.updatePort(net, r)

    #- ------------------------------------------------------------
    #- The blocks meet the rings
    #- ------------------------------------------------------------

    @staticmethod
    def _port(inst, net, pick=None):
        """A placed block's published pin for `net`."""
        rs = [c.get() for c in getattr(inst, "children", []) or []
              if getattr(c, "isPort", lambda: False)()
              and getattr(c, "name", "") == net]
        rs = [r for r in rs if r is not None]
        if not rs:
            return None
        return pick(rs) if pick else rs[0]

    def _supplies(self, layout):
        """Five ties, and every one of them in empty space.

        WHAT DOES NOT NEED ONE is most of it. The comparators' VSS bar
        and the bias block's two bars sit on the rings' own rows, and
        the strip's supplies are already M4 columns pointing at them.
        What is left is: both bias bars up to their rings, which
        `addRouteRingOnRect` lays 6600 clear of the block rather than
        against it; the strip's two columns, which stop 87 um short;
        and the comparators' VDD, which is a bar mid cell.

        A RING IS A ROW, NOT A PLACE. None of these stories `end()`:
        `end()` lands on the stop rect and a ring spans the tile, so
        the last leg would run to the middle of the cell. A ring is
        met wherever the riser reaches its row -- `movey` to it and
        drop a via -- which is also why none of them need to name a
        coordinate.

        NOT `addPowerConnection`. It stretches EVERY published supply
        rect to the ring, the blocks' mid-cell tap bars included, and
        each stretched copy slices through the core it came from.
        Measured: every pin of both comparators and the bias merged
        into one VSS blob, with no signal routes drawn at all.
        """
        rt = layout.named_rects.get("ring_t_VDD_1V8")
        rb = layout.named_rects.get("ring_b_VSS")
        bias = layout.getInstanceFromInstanceName("xbias")
        ccmp = layout.getInstanceFromInstanceName("xccmp")
        dig = layout.getInstanceFromInstanceName("xdig")
        if None in (rt, rb, bias, ccmp, dig):
            log.error("top: no rings or blocks to tie")
            return
        top = lambda rs: max(rs, key=lambda r: int(r.y1))
        bot = lambda rs: min(rs, key=lambda r: int(r.y1))

        #- the bias block's own bars, straight up and straight down to
        #- the rows above and below them
        for net, ring, pick in (("VDD_1V8", rt, top), ("VSS", rb, bot)):
            bar = self._port(bias, net, pick)
            if bar is None:
                log.error(f"top: the bias block has no {net} bar")
                continue
            p = layout.path(net, "M1", start=[bar], stop=[ring])
            p.start()
            p.movey(p.landing("y"))

        #- the strip's two columns are already M4 and already
        #- vertical: they only have to keep going, and nothing is
        #- above the strip for 87 um
        for net, ring in (("VDD_1V8", rt), ("VSS", rb)):
            col = self._port(dig, net)
            if col is None:
                log.error(f"top: the strip has no {net} column")
                continue
            p = layout.path(net, "M4", start=[col], stop=[ring])
            p.start()
            p.movey(p.landing("y"))
            #- ONE CUT TO THE RING'S OWN LAYER. A bare `down()` is one
            #- step, and one step from M4 is M3 -- 87 um of riser
            #- ending a layer short of what it came for.
            p.down("M1")

        #- and the comparators' VDD slides east along the bar it is
        #- already on -- same net, same layer -- to climb the 4 um gap
        #- between the pair and the strip, which holds nothing else
        bar = self._port(ccmp, "VDD_1V8", top)
        if bar is not None:
            p = layout.path("VDD_1V8", "M1", start=[bar], stop=[rt])
            p.start()
            #- TRACK 3, NOT 1: the pair's east edge is its cap bank,
            #- and a MiM claims 1.34 um from unrelated M4 (capm.11) --
            #- including metal outside its own cell. The riser stood
            #- 0.75 um off it on the first track and 1.22 on the
            #- second, where the wire cleared but the via pad, half
            #- again as wide, did not.
            p.movex(p.track("dband", 8))
            p.up()
            p.up()
            p.up()
            p.movey(p.landing("y"))
            p.down()
            p.down()
            p.down()

    def _signals(self, layout):
        """The nets that leave one block for another, told out.

        Every one of them is the same shape: out of a pin, into a
        corridor, along it, and down into the pin at the other end.
        What differs is WHICH corridor, and none of them is a number
        here:

          * between the blocks, the floorplan's own gaps -- `lband`,
            `dband` and the empty bands above the short blocks. Those
            are registered in afterPlace, from the placement that just
            made them.
          * ACROSS a block, whatever that block leaves free.
            `addBlockChannel` asks it, through its block view, for the
            corridors on a layer that are clear over the stretch this
            route needs, and takes the one nearest the pin it is
            leaving. A block made of cells answers for the metal its
            children own, which is the only reason the question can be
            asked at all.
          * INTO the logic strip, the sliver west of its own pins --
            measured off the pins, not spelled.

        So a resize moves every one of these and no line here changes.
        """
        bias = layout.getInstanceFromInstanceName("xbias")
        ccmp = layout.getInstanceFromInstanceName("xccmp")
        dig = layout.getInstanceFromInstanceName("xdig")
        if None in (bias, ccmp, dig):
            log.error("top: the three blocks are needed to route")
            return
        P = self._port

        #- the lane in front of the strip's own pins, measured off the
        #- westmost of them. Lost in a rewrite once, and the story
        #- that aimed at it did not fail -- the anchor resolved to
        #- None, the move was skipped, and PWRUP_B descended in
        #- `lband` and crossed the tile at its landing row.
        west = [c.get() for c in getattr(dig, "children", []) or []
                if getattr(c, "isPort", lambda: False)()]
        west = [r for r in west if r is not None]
        if west:
            layout.addRoutingChannel("eband", int(dig.x1),
                                     min(int(r.x1) for r in west),
                                     horizontal=False)

        #- ONE STORY AT A TIME. `_ONLY` names the nets whose stories
        #- are drawn; None draws them all. A short is found by taking
        #- routes AWAY until it goes, and then put back one at a time
        #- with DRC and LVS between each -- `path` is the one choke
        #- point every story goes through, so the gate lives here.
        only = self._ONLY

        def path(net, a, b, layer=None, at=None):
            if only is not None and net not in only:
                return None
            if a is None or b is None:
                log.error(f"top: {net} is not on both blocks")
                return None
            #- A PIN IS 3200 WIDE AND THE DEFAULT CUT 8800, so every
            #- turn pad here would be wider than the lane it turns in
            #- -- six nets into three corridors leaves no lane to
            #- waste, and the pins these land on are the strip's own
            #- 3200 ones. Turned on its side the same cuts fit.
            p = layout.path(net, layer or a.layer, start=[a], stop=[b],
                            options="1cuts,2vcuts")
            p.start(at=at)
            return p

        def over(name, pin, layer="M5"):
            """The corridor across the pair this pin can rise in.

            From the pin's own row to the pair's top, on the layer the
            riser will use, nearest the pin -- which is exactly the
            question, and the block answers it.
            """
            return layout.addBlockChannel(name, ccmp, layer,
                                          span=(int(pin.y2),
                                                int(ccmp.y2)),
                                          near=int(pin.centerX()))

        def lane(name, pin, step):
            """`step` lanes east of the pin, inside that corridor.

            A corridor measured off a block is as wide as the block
            leaves it, so its track 0 is an edge and says nothing
            about where this route is. The pin does: the lane beside
            it, and the count from there.
            """
            #- CLAMPED TO THE CORRIDOR. A corridor measured off a
            #- block is as wide as the block leaves it, and a count of
            #- lanes from the pin can walk out the far side -- asked
            #- for track 19 of a 12-track channel, the route went
            #- wherever channelTrackCoord extrapolated to.
            ch = layout.routingChannel(name)
            i = layout.channelTrackNear(name, int(pin.centerX())) + step
            if ch is None:
                return i
            pitch = layout._lanePitch(None) or 1
            n = max(1, int((int(ch[1]) - int(ch[0])) // pitch))
            return max(0, min(i, n - 1))

        #- ORDER IS THE WHOLE PLAN, because on one layer a crossing is
        #- a short:
        #-
        #-   * a leg east in `cband` passes over every riser west of
        #-     where it turns, so the risers over the pair go WEST to
        #-     EAST with DECREASING band tracks -- an eastern riser
        #-     stops below the western legs that cross it.
        #-   * a descent in `dband` cuts every band track below the
        #-     one it leaves, so the lanes go WEST to EAST with
        #-     INCREASING band tracks.
        #-   * the descents are on M4 and the band legs on M5, so a
        #-     descent never meets the rows it cuts.
        #-   * and the last leg, in to the strip, goes back UP to M5:
        #-     every JNWTR cell carries a full height M4 supply bar in
        #-     each of its supply columns, so a leg reaching across
        #-     one on M4 lands on that supply (measured, RST_B tied to
        #-     VSS). M5 is the layer those cells do not use, which is
        #-     why the strip publishes its ports there.
        #-   * DBAND'S FIRST TWO LANES BELONG TO THE CAP BANK. The
        #-     pair's east edge is the bank, and a MiM claims 1.34 um
        #-     from unrelated M4, so the descents start at track 2.
        #-
        #- THE ORDER, WEST TO EAST BY RISER, WITH FALLING TRACKS.
        #- It was the other way round and the connectivity check named
        #- every consequence: RST_A's riser at 1280700 and RST_B's at
        #- 1310100 both climbed through CMPO_A's leg at 862500 and
        #- CMPO_B's at 838500, because they were assigned the HIGHER
        #- tracks. The riser furthest east must stop lowest.
        #-
        #-   net       riser at    cband   down
        #-   CMPO_A    ~1067000      16    dband 6
        #-   CMPO_B    ~1079000      12    dband 4
        #-   RST_A      1280700        8    dband 2
        #-   RST_B      1310100        4    dband 0
        #-   PWRUP_N   -- (lband)     20    dband 10
        #-   PWRUP_B   -- (lband)     24    eband 0
        #-
        #- THE LOWER PIN TAKES THE FARTHER RISER. Both comparator
        #- outputs walk WEST from a pin column outside their corridor
        #- to reach it, and each walk is at its own pin's row -- so
        #- the walk of the one whose pin is higher would cross the
        #- other's riser. CMPO_A's pin is at 338700 and CMPO_B's at
        #- 456700, so CMPO_A goes further west and CMPO_B's walk
        #- passes below where CMPO_A's riser begins.
        #-
        #- AND DBAND'S LANES 7..9 BELONG TO A SUPPLY TIE: the VDD tie
        #- to the strip stands at 1466000..1475600, and the
        #- connectivity check caught a descent in it twice.

        #- VC: the bias block's own M3 pin runs to its east edge, and
        #- the pair's is an M2 pin just above its base. The leg east
        #- over the pair's foot is on M4 -- on M5 it would cut the
        #- riser RST_B takes out of the pin below it.
        p = path("VC", P(bias, "VC"), P(ccmp, "VC"), at="e")
        if p:
            p.movex(p.track("lband", 6))
            p.up("M4")
            p.movey(p.pin("xccmp", "VC", "y"))
            p.movex(p.pin("xccmp", "VC", "x"))
            p.end()

        #- PWRUP_N, twice: the pair and the strip are on opposite
        #- sides of it. Both legs leave the same M5 pin on the same
        #- lane -- one goes down and one goes up, and a lane is busy
        #- only where its net is.
        pn = P(bias, "PWRUP_N_1V8")
        p = path("PWRUP_N_1V8", pn, P(ccmp, "PWRUP_N_1V8"), "M5")
        if p:
            p.movex(p.track("lband", 1))
            p.movey(p.landing("y"))
            #- AND STOP ON THE PAIR'S OWN BAR: the pin's row east of
            #- it is that comparator's PWRUP_N on M5, this same net,
            #- so the leg lands on metal the net already owns.
            p.movex(p.landing("x"))

        #- PWRUP_B DOES NOT REACH THE PAIR YET, and the tile has
        #- six merges besides. Every way down to the pair's port
        #- tried so far makes it worse, and the reason is that this
        #- level is out of room rather than that any one story is
        #- wrong: `lband` fits four lanes at the 12000 a via pad
        #- wants and five nets ask for one; the band above the pair
        #- carries five M5 legs, the bundle's four M4 rows sit over
        #- those, and the pair's own column is walled by its seam
        #- ring below and the cap bank east. Measured, in layout nets
        #- against the schematic's 24: 18 with no leg at all, 16 on
        #- M5 down the column, 16 crossing above the bundle, 13 on M4
        #- at the pin's row.
        p = path("PWRUP_N_1V8", pn, P(dig, "PWRUP_N_1V8"), "M5")
        if p:
            p.movex(p.track("lband", 1))
            p.movey(p.track("cband", 20))
            p.movex(p.track("dband", 10))
            p.down("M4")
            p.movey(p.landing("y"))
            #- AND IT STAYS ON M4 TO THE PIN, rising only in end().
            #- Coming up to M5 for the last leg put this net's landing
            #- pad 0.28 um from the strip's own port pad where met4.2
            #- wants 0.30 -- both pads ITS OWN, bridged by a wire
            #- narrower than either, so the overhangs missed by 0.02
            #- and DRC counted four. One layer lower there is no pad
            #- at all until the end.
            #-
            #- LANE 10 IS THE ONLY ONE THAT WORKS, and the DRC count
            #- alone would have picked a broken one -- measured:
            #-   9  -> 2 DRC, PWRUP_N merged into VDD_1V8 (the supply
            #-         tie stands at 8)
            #-   10 -> 4 DRC, nothing merged            <- this
            #-   11 -> 2 DRC, PWRUP_N merged with RST_A
            #-   12 -> 0 DRC, PWRUP_N merged with RST_A
            #- Read LVS before believing a DRC improvement.
            p.movex(p.landing("x"))
            p.end()

        #- PWRUP_B: OVER the strip, not in front of it. dband's lanes
        #- are spoken for (four nets and a supply tie), and the sliver
        #- before the strip's pins is where every other net's last leg
        #- runs -- a descent there met RST_A's landing cut. The strip
        #- itself leaves a corridor east of its pins, and that is
        #- measured, not chosen. Its crossing of `lband` is on M4:
        #- PWRUP_N rises there on M5, and the bundle's M4 rows are
        #- higher than this one.
        #- A CORRIDOR IS PER NET, and asked FOR that net. The strip
        #- routes its own rungs on M5, RST_B's clear across the block
        #- at two heights -- so asked net-blind there is no free M5
        #- column over the strip at all, and the one `digfree` both
        #- these nets shared registered nothing. Every step that
        #- named it then resolved to a bogus x, which is how RST_B's
        #- descent came down on RST_A: one merged net, and the only
        #- thing between this cell and LVS (23 nets against 24).
        #- Asked for its own net, each gets the true answer.
        def blockfree(tag, blk, net, pin, span=None):
            nm = f"{tag}free_{net.lower()}"
            return layout.addBlockChannel(
                nm, blk, "M5",
                span=span or (int(blk.y1), int(blk.y2)),
                near=int(pin.centerX()) if pin is not None
                else int(blk.x2), net=net) and nm

        def digfree(net, pin):
            return blockfree("dig", dig, net, pin)

        #- AND IT STILL DOES NOT REACH THE STRIP. Measured this round,
        #- against the schematic's 24 nets:
        #-
        #-   no leg at all                        26  (split in 3)
        #-   down dband lane 8                    21  (the VDD tie
        #-                                            stands there,
        #-                                            1466000..1475600)
        #-   down dband lane 12                   21  (track(dband,12)
        #-                                            resolves to
        #-                                            1494800, OUTSIDE
        #-                                            the channel and
        #-                                            inside the strip)
        #-
        #- dband has no lane left: 0 and 1 are the cap bank's MiM
        #- halo, 2/4/6 are RST_A and the two outputs, 8 is the supply
        #- tie, 10 is PWRUP_N, and 12 is past the far edge. And there
        #- is no column over the strip either -- the strip's own RST_B
        #- rungs cross it full width on M5 at two heights, which is
        #- what `digfree` reports and why it is guarded rather than
        #- ignored. The fix is in the STRIP: move those rungs off M5.
        #- Until then this net is left open, honestly, rather than
        #- drawn somewhere that shorts.
        pb = P(bias, "PWRUP_B_1V8")
        #- THE SEARCH TAKES THIS ONE NET, in two legs, each on the
        #- stack that leg needs. It runs at DRAW time, so every story
        #- above is metal it can see -- which is what a hand lane plan
        #- was standing in for, and why twenty of them were needed.
        #-
        #- THE STACKS ARE NOT THE SAME, and neither is the default.
        #- Left to the technology's own chain the search runs verticals
        #- on li, the supply layer, and its own via check then calls
        #- the descent blocked.
        #-
        #-   leg 1, bias -> pair: M2/M3/M5. It needs M5 because that
        #-     is where the bias block publishes, and it must NOT have
        #-     M4: the leg passes the cap bank's west edge, and M4 is
        #-     met3, which capm.11 keeps 1.34 um clear of a MiM. With
        #-     M4 in the stack this is LVS clean and 9 DRC -- eight
        #-     capm.11 and met3.2/met3.3d, all of them at 136..138 um,
        #-     which is that edge. Without it, none.
        #-   leg 2, pair -> strip: M3/M4. Both ports are low and on
        #-     M3, and there is no MiM between them.
        layout.addMazeRoute("^PWRUP_B_1V8$", layers=["M2", "M3", "M5"],
                            rects=[pb, P(ccmp, "PWRUP_B_1V8")])
        layout.addMazeRoute("^PWRUP_B_1V8$", layers=["M3", "M4"],
                            rects=[P(ccmp, "PWRUP_B_1V8"),
                                   P(dig, "PWRUP_B_1V8")])
        #- RST_A is published on the pair's top edge, which is where
        #- the band is: north out of the pin on its own layer, up, and
        #- east. It rises OUTSIDE the block -- the pin shares its row
        #- with the upper comparator's VSS ring, and a via stack in
        #- that row ties the net to it.
        p = path("RST_A", P(ccmp, "RST_A"), P(dig, "RST_A"))
        if p:
            p.movey(p.track("cband", 0))
            p.up("M5")
            p.movey(p.track("cband", 8))
            p.movex(p.track("dband", 2))
            p.down("M4")
            p.movey(p.landing("y"))
            p.up("M5")
            p.movex(p.landing("x"))
            p.end()

        #- and the three whose pins are inside the pair, each rising
        #- in the corridor the pair leaves clear beside it
        #- and the two comparator outputs, whose risers are the
        #- westmost and so take the highest tracks. Their corridors
        #- are the same span, so the lanes are counted from the pin
        #- and kept two apart -- at the same index they came out at
        #- the same x and shorted to each other.
        #- RST_B lands furthest east of all of them (block-x 86800),
        #- so a leg from dband to its pad crosses every other net's
        #- landing on the way -- it caught RST_A's cut. It comes down
        #- over the strip instead, in the same measured corridor
        #- PWRUP_B uses, two lanes along.
        for net, band, down, step in (("RST_B", 4, 3, 2),
                                      ("CMPO_A", 16, 6, -4),
                                      ("CMPO_B", 12, 4, -2)):
            pin = P(ccmp, net)
            name = net.lower() + "_up"
            p = path(net, pin, P(dig, net))
            if not p or not over(name, pin):
                continue
            #- RST_B comes down over the strip, in the column its own
            #- port already sits in; the other two use dband.
            ch = digfree(net, P(dig, net)) if net == "RST_B" else "dband"
            if not ch:
                log.error(f"top: {net} has no corridor over the strip")
                continue
            p.up("M5")
            p.movex(p.track(name, lane(name, pin, step)))
            p.movey(p.track("cband", band))
            p.movex(p.track(ch, down))
            p.down("M4")
            p.movey(p.landing("y"))
            p.up("M5")
            p.movex(p.landing("x"))
            p.end()

    def _antenna(self, layout):
        """The two diodes, and the legs that make them count.

        The check is `make ant`: metal3 collects charge during its own
        etch and discharges through whatever gate it reaches. Two
        gates here are over the limit of 400 -- MP0 of `x1`, the
        output buffer, at 450.6, and MP0 of `x7`'s NOR at 488.2.

        THE NETS ARE CMPO_A AND CMPO_B, and finding that out was the
        whole of the work. Nothing in the antenna report names a net:
        it gives a gate box and one rect of the offender, and both
        gates extract under the same device name, `MP0`. The rects
        place themselves -- (1456400,170200) and (1444400,82200) in
        this cell's units -- exactly on the two lanes `tracks` calls
        CMPO_A's and CMPO_B's, at the very bottom of each. The
        netlist agrees from the other side: `x1 CMPO_A ...` and
        `x7 CMPO_B PWRUP_N_1V8 ...`, and MP0 is the pmos on the A
        input of both cells. A diode was hung on PWRUP_N first, on
        the strength of the report alone, and the two ratios came
        back to the third decimal unchanged -- which is what a diode
        on the wrong net looks like.

        WHY THIS IS ROUTED BY HAND rather than by `addAntennaDiode`.
        That command places a PHYSICAL-only instance and routes to
        it, which is right when the netlist does not know about the
        diode. These are in the schematic, because a diode extracts
        as a DEVICE and LVS counts devices: place one physically as
        well and the layout has two where the schematic has one. So
        the schematic carries them, `place` puts them down as
        ordinary instances, and what is left is exactly the routing
        half of that command -- these stories.

        THE A LEG MUST END ON M4 OR BELOW, and that is the whole
        constraint. It is metal3's etch that does the damage, so a
        diode reached over M5 would be connected in the netlist and
        useless in the fab -- the protection has to exist at the step
        the charge is collected. Straight up in the diode's own
        column to M4, then north until it meets the descent already
        in that lane: same net, so the overlap is the connection.

        AND THE LEG STOPS ON THE LANE, without `end()`. The stop rect
        is the strip's pin and `end()` would drive the leg all the
        way east to it, laying a second copy of a leg the net already
        has -- more metal3 on the very nets whose metal3 is the
        problem.
        """
        dig = layout.getInstanceFromInstanceName("xdig")
        rb = layout.named_rects.get("ring_b_VSS")
        if None in (dig, rb):
            log.error("top: nothing to hang the antenna diodes on")
            return

        for name, net, track in (("xant_cmpo_b", "CMPO_B", 4),
                                 ("xant_cmpo_a", "CMPO_A", 6)):
            ant = layout.getInstanceFromInstanceName(name)
            if ant is None:
                log.error(f"top: no antenna diode {name}")
                continue
            #- an instance's ports are named for the NETS they carry,
            #- not for the pins of the cell: these are A and AVSS
            a = self._port(ant, net)
            gnd = self._port(ant, "VSS")
            pin = self._port(dig, net)
            if None in (a, gnd, pin):
                log.error(f"top: {name} published no ports")
                continue

            #- A: M2 AND NOT M1. The diode already carries its own li
            #- to met1 contact over the anode, so met1 is the metal
            #- the pin has been brought up to; starting a stack from
            #- the li below it lands a second via on the cell's own,
            #- concentric and a few tens of nm off, which magic
            #- reports as "this layer can't abut or partially overlap
            #- between subcells".
            p = layout.path(net, "M2", start=[a], stop=[pin],
                            options="1cuts,2vcuts")
            p.start()
            p.up("M4")
            p.movex(p.track("dband", track))
            p.movey(p.pin("xdig", net, "y"))

            #- AVSS is the substrate tie, and it is li all the way:
            #- the ring below is li too, so this is one leg and no
            #- via. A RING IS A ROW -- `movey` onto it, never `end()`.
            p = layout.path("VSS", "M1", start=[gnd], stop=[rb])
            p.start()
            p.movey(p.landing("y"))

    def _ibp(self, layout):
        """The four bias currents, as one bundle and four endings.

        THE ORDER OF THE MEMBERS IS THE ORDER THEY LEAVE IN. Each
        takes the row one lane above the last and turns down at its
        own column, so the bundle only works if the member that turns
        FIRST is on the LOWEST row -- otherwise its descent crosses
        the rows still travelling east. <3> and <2> drop into the gap
        west of the comparators to reach their pins at the bottom of
        the pair, <1> and <0> carry on to the pins at the top, and
        that is the order they are listed in.

        They cross the bias block on M4, not on the M5 they leave: the
        four pins ARE M5 verticals 60 um tall, so a horizontal on M5
        would short the lot. One layer down they pass under all four.
        """
        bias = layout.getInstanceFromInstanceName("xbias")
        ccmp = layout.getInstanceFromInstanceName("xccmp")
        if None in (bias, ccmp):
            return
        nets = ["IBP_1U<3>", "IBP_1U<2>", "IBP_1U<1>", "IBP_1U<0>"]
        starts = [self._port(bias, n) for n in nets]
        stops = [self._port(ccmp, n) for n in nets]
        if None in starts or None in stops:
            log.error("top: the bias currents are not on both blocks")
            return

        #- TWO LANES APART, not one: they turn off M5 at their own
        #- rows, and the pad of that turn is three times the wire --
        #- at one lane the four pads left 2400 between them where
        #- met4.2 wants 3000.
        b = layout.bus(nets, "M5", starts=starts, stops=stops, lanes=2)
        b.start()
        #- up its own pin to its own row, then off M5 before turning
        #- ON A ROW THE BIAS BLOCK LEAVES FREE, because the bundle
        #- crosses it: asked of the block rather than counted off the
        #- band. Its own track 2 -- 15 um above the pair, which looked
        #- like open tile -- runs through the block's M4 and tied all
        #- four members to VSS.
        band = "cband"
        if layout.addBlockChannel("ibpband", bias, "M4",
                                  span=(int(bias.x1), int(bias.x2)),
                                  near=int(bias.y2), horizontal=True):
            band = "ibpband"
        b.movey(b.track(band, 1))
        b.down("M4")

        #- and from here each net is alone: two turn down in the gap
        #- west of the pair, two carry on over it
        for i, net in enumerate(nets):
            p = b.member(net)
            #- THREE TURN IN LBAND NOW, not two. IBP_1U<1>'s pin has
            #- moved to the pair's WEST edge, so carrying on over the
            #- pair to reach it means descending ON the block -- and
            #- the mirrored half puts its cap bank exactly there: the
            #- riser at x 1024900 landed on JNWTR_CAPX1's M4 plate.
            #- ALL FOUR TURN IN LBAND NOW. IBP_1U<1>'s pin has moved
            #- to the pair's WEST edge and IBP_1U<0>'s cap-plate pin
            #- was always at x1=0, so carrying on OVER the pair to
            #- reach either means descending ON the block -- and the
            #- mirrored half puts its cap bank and its VSS ring
            #- exactly there. Measured: <1>'s riser at x 1024900
            #- landed on JNWTR_CAPX1's M4 plate, and <0>'s
            #- cut_M1M5_2x2 at (1046600,1017400) on the ring's VIA4.
            p.movex(p.track("lband", 2 + i * 2))
            #- AND DOWN TO M2 FOR THE ONE THAT LANDS ON M3. capm.11
            #- keeps a MiM 1.34 um from UNRELATED metal3 -- cicpy M4 --
            #- and the mirrored half puts its cap bank at the pair's
            #- top, exactly where IBP_1U<1>'s west-edge pad is. On M4
            #- the descent broke it at (1026400,1001300); on M2 the
            #- rule does not apply. IBP_1U<0> stays on M4 because the
            #- MiM plate IS its pin -- related metal, not unrelated.
            if net == "IBP_1U<1>":
                p.down("M2")
                p.movey(p.landing("y"))
                p.up("M3")
                p.movex(p.landing("x"))
            else:
                p.movey(p.landing("y"))
            p.down(stops[i].layer)
            p.movex(p.landing("x"))
            p.end()
