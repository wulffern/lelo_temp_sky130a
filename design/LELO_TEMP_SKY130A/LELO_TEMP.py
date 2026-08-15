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
from cicpy.core.path import pin, track, landing, PITCH, SPACE

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

        #- THE SEAM IS A GAP, NOT AN ABUTMENT. beforePlace opens 2 um
        #- between the halves for capm.2a, and their VSS straps land at
        #- y 502000..511000 and 531000..540000 -- 20 um apart, joined
        #- by nothing. The wrapper published a pin between them and
        #- every level above assumed the pin meant metal: measured,
        #- VSS inside this cell is two components, and it was the last
        #- split in the whole tile's VSS. One vertical at the straps'
        #- own centre closes it; everything that crosses the seam does
        #- so well away from mid-width.
        paths = [
            dict(net="VSS", layer="M1",
                 start=("x2_ccmp", "VSS"), stop=("x3_ccmp", "VSS"),
                 steps=[("movey", pin("x3_ccmp", "VSS", "y")),
                        ("end",)]),
        ]

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
            #- THE LOWER ONE IS THE MIRRORED ONE, so that the two cap
            #- banks -- which live at LELOTEMP_CCMPR's bottom -- meet
            #- at the seam. They are the matched pair's matched
            #- element and they belong beside each other; mirroring
            #- the upper half instead put them at the tile's extreme
            #- top and bottom, 100 um apart.
            lower = lay.getInstanceFromInstanceName("x2_ccmp")
            upper = lay.getInstanceFromInstanceName("x3_ccmp")
            if lower is None or upper is None:
                log.error("ccmp: both comparators are needed to route")
                return None
            #- setAngle leaves the instance position in the mirrored
            #- frame, so pin it back where it was
            x, y = int(lower.x1), int(lower.y1)
            lower.setAngle("MX")
            lower.moveTo(x, y)
            lower.updateBoundingRect()
            self.updateBoundingRect()
            self._crossSeam(lay, lower, upper)
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

            #- VC: THE SEAM GAP, AND NOTHING ELSE. Both halves put VC
            #- on the edge that meets at the seam, so the two pads are
            #- at the same x facing each other -- but `stack(ygap=2um)`
            #- holds the halves 2 um apart for capm.2a, so they do not
            #- touch. Without this jumper VC extracted as the local
            #- node `x3_ccmp/VC`. On M2, which is what the pads are,
            #- and one step: the gap is the whole story.
            lo, hi = pins("VC")
            if lo is not None and hi is not None:
                p = lay.path("VC", "M2", start=[lo], stop=[hi],
                             options=narrow)
                p.start()
                p.movey(p.landing("y"))
                p.end()

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

            #- VDD ONLY, AND THAT IS THE MIRROR'S DOING. The caps and
            #- the VSS ring share LELOTEMP_CCMPR's bottom edge, so
            #- bringing the banks together at the seam brought the two
            #- VSS rings with them -- they abut there and need nothing
            #- drawn. It is VDD that is now split, one ring at the
            #- pair's top and one at its bottom, and without this the
            #- upper comparator's supply is not connected to the pair
            #- at all: it extracted as the local node
            #- `x3_ccmp/VDD_1V8`, and at the top it floated into VSS
            #- and took the whole VDD network with it.
            #-
            #- The run crosses both VSS rings at the seam, which is
            #- safe because it crosses them on M2 with no via -- the
            #- rails are M1.
            for net, x in (("VDD_1V8", int(a.x1) + 186000),):
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
                #- THE INSTANCE, NOT ITS CORNER. `rects()` used to take
                #- (dx, dy) and this passed inst.x1, inst.y1; it takes
                #- the INSTANCE CHAIN now, and composes each instance's
                #- own transform -- which is the only form that carries
                #- a mirror. Left as two ints it raised "'int' object is
                #- not reversible", the whole ladder below never ran,
                #- and the strip came out unrouted: 7 nets the maze
                #- router then failed on and 7 open nets at the top,
                #- none of which looked like a crash.
                for r in sub.blockCell().rects((inst,)):
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
    #- their ports.
    #-
    #- WHICH ROUTING RUNS. `_PHASES` picks the supply and bias phases;
    #- the crossing nets are `paths` below and are gated by
    #- `paths_only`. Both exist to bisect a short: take routing away
    #- until it goes, then put it back one at a time with DRC and LVS
    #- between each. None means all of them -- an empty tuple means
    #- NONE, which is a phase that runs and lays not one wire.
    _PHASES = ("supplies", "ibp", "antenna")
    #- WHAT IS PROVEN CLEAN. Walked one net at a time, rebuilding and
    #- running checkroutes and DRC between each:
    #-
    #-   ()                       0 shorts, 8 opens, DRC OK
    #-   RST_A                    0 shorts, 8 opens, DRC OK
    #-   + PWRUP_N_1V8            0 shorts, 8 opens, DRC OK
    #-   + VC                     0 shorts, 7 opens, DRC OK   <- here
    #-   + PWRUP_B_1V8            0 shorts, 7 opens, DRC 4
    #-
    #- PWRUP_B_1V8 is the one left out: it costs four met2.2 (Metal2
    #- spacing < 0.14 um). It is declared and gated off rather than
    #- deleted, so putting it back is one name in this tuple.
    #-
    #- The 7 opens are not this table's. CMPO_A, CMPO_B, RST_B and VSS
    #- have no story yet. RST_A's is a failure INSIDE LELO_TEMP_DIG --
    #- its own maze route reports "no path for RST_A ... closest
    #- approach 38000 away" and leaves a stub at (1475900, 153500);
    #- the top-level path lands correctly. PWRUP_N_1V8's second leg
    #- reaches the strip but the strip's side is not closed either.
    paths_only = ("RST_A", "PWRUP_N_1V8", "VC", "CMPO_A", "CMPO_B", "VSS", "RST_B", "PWRUP_B_1V8")

    #- THE CROSSING NETS, DECLARED. Each is the same shape: out of a
    #- pin, into a corridor, along it, and down into the pin at the
    #- other end. What differs is WHICH corridor, and none of them is
    #- a number here:
    #-
    #-   * between the blocks, the floorplan's own gaps -- `lband`,
    #-     `dband`, `eband` and the bands above the short blocks,
    #-     registered in afterPlace from the placement that just made
    #-     them.
    #-   * ACROSS a block, whatever that block leaves free, asked of
    #-     its block view.
    #-
    #- So a resize moves every one of these and no line here changes.
    paths = [
        #- VC: the bias block's own M3 pin runs to its east edge, and
        #- the pair's is an M2 pin just above its base.
        #-
        #- JUST ABOVE THE PIN, not on its row and not below it. Along
        #- the pin's row 522000, entering at the pair's west edge, it
        #- drives through LELOTEMP_CCMPR's VSS -- an M5 pad over
        #- 497000..526000 with a cut_M1M5_2x2 under it whose M4
        #- enclosure is 516400..526000. Up at the pin's own column
        #- instead it crosses LELOTEMP_CCMPR_CAPS' M4 bar, which spans
        #- the pair almost end to end at 470500..479500. Both END at
        #- 526000, which is the pin's top, so the lane above the pin
        #- clears them and the drop in is one lane long.
        #-
        #- LBAND HAS NO CLEAN LANE for the riser and track 6 is the
        #- least bad: `_ibp` takes `2 + i*2`, so 6 is assigned twice,
        #- and moving west only trades IBP_1U<2>'s leg for IBP<3>'s
        #- and IBP<2>'s risers. On M5 the whole band is PWRUP_N's --
        #- its riser is 981900..984900 over the full height. Closing
        #- it needs a lane budget for this band, not another track
        #- number.
        #- NO CLIMB AT ALL. The start pin is M3 and the stop pin M2,
        #- so the whole story fits between them and `end()` makes the
        #- one transition there is. Going up to M4 -- which is what
        #- this did -- was a choice, and it chose the one layer in
        #- this band that is spoken for: `_ibp` takes lband `2 + i*2`,
        #- and IBP_1U<2>'s leg east into its pin blankets
        #- 1001400..1028900 at 498000..501000, which a riser from
        #- 333000 to the pair's pin at 522000 has to cross. M5 is no
        #- better -- PWRUP_N's riser owns 981900..984900 over the full
        #- height. Measured on M3, over this riser's own span: lband
        #- the only clear slot is 974400..984600 -- `xbias/LPI` ends
        #- at the block edge on its west and IBP_1U<3> starts at
        #- 984600 -- and lband's own grid steps 6250, so track 0 lands
        #- 1250 off LPI and track 1 lands 300 into IBP<3>'s via pad.
        #- One SPACE east of track 0 is the lane, and it is derived:
        #- the band's edge is where the neighbour's metal stops, and a
        #- space is what the technology asks between them.
        dict(net="VC", at="e",
             start=("xbias", "VC"), stop=("xccmp", "VC"),
             steps=[("movex", track("lband", 0) + SPACE),
                    ("movey", pin("xccmp", "VC", "y") + 2 * PITCH),
                    ("movex", pin("xccmp", "VC", "x")),
                    ("movey", pin("xccmp", "VC", "y")),
                    ("end",)]),

        #- PWRUP_N, twice: the pair and the strip are on opposite
        #- sides of it. Both legs leave the same M5 pin on the same
        #- lane -- one goes down and one goes up, and a lane is busy
        #- only where its net is.
        #-
        #- AND IT STOPS ON THE PAIR'S OWN BAR: the pin's row east of
        #- it is that comparator's PWRUP_N on M5, this same net, so
        #- the leg lands on metal the net already owns.
        #- AND IT COMES DOWN. This story used to stop after the last
        #- movex, on the claim that the pin's row east of it was the
        #- pair's own PWRUP_N on M5 and landing there was landing on
        #- the net. Measured against the pair as built today: nothing
        #- of this net is on M5 at that row, the leg flew over its own
        #- M3 pin two layers up, and the net stood in two components.
        #- `end()` is the drop the claim used to stand in for.
        dict(net="PWRUP_N_1V8", layer="M5",
             start=("xbias", "PWRUP_N_1V8"), stop=("xccmp", "PWRUP_N_1V8"),
             steps=[("movex", track("lband", 1)),
                    ("movey", landing("y")),
                    ("movex", landing("x")),
                    ("end",)]),

        #- and up to the strip. IT STAYS ON M4 TO THE PIN, rising only
        #- in end(): coming up to M5 for the last leg put this net's
        #- landing pad 0.28 um from the strip's own port pad where
        #- met4.2 wants 0.30 -- both pads ITS OWN, bridged by a wire
        #- narrower than either, so the overhangs missed by 0.02 and
        #- DRC counted four. One layer lower there is no pad at all
        #- until the end.
        #-
        #- LANE 10 IS THE ONLY ONE THAT WORKS, and the DRC count alone
        #- would have picked a broken one -- measured:
        #-   9  -> 2 DRC, PWRUP_N merged into VDD_1V8 (the supply tie
        #-         stands at 8)
        #-   10 -> 4 DRC, nothing merged            <- this
        #-   11 -> 2 DRC, PWRUP_N merged with RST_A
        #-   12 -> 0 DRC, PWRUP_N merged with RST_A
        #- Read LVS before believing a DRC improvement.
        dict(net="PWRUP_N_1V8", layer="M5",
             start=("xbias", "PWRUP_N_1V8"), stop=("xdig", "PWRUP_N_1V8"),
             steps=[("movex", track("lband", 1)),
                    ("movey", track("cband", 20)),
                    ("movex", track("dband", 10)),
                    ("down", "M4"),
                    ("movey", landing("y")),
                    ("movex", landing("x")),
                    ("end",)]),

        #- RST_A is published on the pair's top edge, which is where
        #- the band is: north out of the pin on its own layer, up, and
        #- east. It rises OUTSIDE the block -- the pin shares its row
        #- with the upper comparator's VSS ring, and a via stack in
        #- that row ties the net to it.
        dict(net="RST_A",
             start=("xccmp", "RST_A"), stop=("xdig", "RST_A"),
             steps=[("movey", track("cband", 0)),
                    ("up", "M3"),
                    ("movey", track("cband", 8)),
                    ("movex", track("dband", 2)),
                    ("up", "M4"),
                    ("movey", landing("y")),
                    ("up", "M5"),
                    ("movex", landing("x")),
                    ("end",)]),

        #- CMPO_A AND CMPO_B: the pair's outputs to the strip, and the
        #- antenna diode on each one.
        #-
        #- THE LANE IS ALREADY CHOSEN. afterPlace stands each diode at
        #- the foot of a dband track -- CMPO_B on 4, CMPO_A on 6 --
        #- precisely so the net that has to reach it descends that same
        #- lane and the riser out of the diode never leaves it. Naming
        #- the track here and there is the statement that they are one
        #- lane; the diodes were placed for these two stories before
        #- the stories existed.
        #-
        #- OUT OF THE FLOOR, NOT ACROSS THE PAIR. Both pins are on the
        #- pair's BOTTOM edge (y 15000..19000) and the strip is 33 um
        #- east, so the leg has to cross the pair's whole width. Over
        #- it means through the cap banks and every net the pair
        #- publishes; under it is `fband`, where the only metal is
        #- VDD_1V8's two M1 ring bars. So: south out of the pin, up to
        #- M4 where those bars cannot be touched, east along the floor,
        #- and north up the net's own lane.
        #-
        #- M4 for the crossing and the riser, M5 only at the end: the
        #- strip publishes these two on M5, and `end()` makes that one
        #- transition where it lands.
        dict(net="CMPO_A", at="s",
             start=("xccmp", "CMPO_A"), stop=("xdig", "CMPO_A"),
             steps=[("up", "M4"),
                    ("movey", track("fband", 0)),
                    ("movex", track("dband", 6)),
                    ("movey", landing("y")),
                    ("up", "M5"),
                    ("movex", landing("x")),
                    ("end",)]),
        #- and the diode up to the same lane. A second story on one
        #- net, sharing the lane end to end: two shapes of one net that
        #- overlap are not a short, and this is the one that makes the
        #- diode part of the net rather than a third component.
        dict(net="CMPO_A",
             start=("xant_cmpo_a", "CMPO_A"), stop=("xdig", "CMPO_A"),
             steps=[("up", "M4"),
                    ("movex", track("dband", 6)),
                    ("movey", landing("y")),
                    ("up", "M5"),
                    ("movex", landing("x")),
                    ("end",)]),

        #- CMPO_B LEAVES BY THE TOP, not the floor. The pair is
        #- mirrored MX, so the two halves publish these on opposite
        #- edges: CMPO_A at y 15000 and CMPO_B at 1053000. Same story,
        #- the other way up -- north out of the pin into `cband`, which
        #- is what RST_A already uses, then down its own lane. Its
        #- diode still stands at the foot of that lane, 100 um below.
        #- AND IT CROSSES cband ON M5, not on M4 or M3.
        #-
        #- Both of the cheap layers are already spoken for by RST_A,
        #- which leaves the pair by this same band: its M3 rises at its
        #- own pin's column through cband 0..8 and then runs east on M3
        #- to dband 2, where it turns UP ONTO M4 and descends -- so a
        #- leg crossing this band eastward meets RST_A's M3 vertical on
        #- M3 and its M4 riser on M4, whichever track it picks.
        #- Measured on M4 at cband 4: CMPO_B and RST_A in one component
        #- of 289 rects.
        #-
        #- M5 crosses over both. The only other M5 in this band is
        #- PWRUP_N's second leg at track 20, and RST_A's own M5 exists
        #- only at its landing row beside the strip -- 13 um east of
        #- where this turns down.
        dict(net="CMPO_B", at="n",
             start=("xccmp", "CMPO_B"), stop=("xdig", "CMPO_B"),
             steps=[("up", "M5"),
                    ("movey", track("cband", 4)),
                    ("movex", track("dband", 4)),
                    ("down", "M4"),
                    ("movey", landing("y")),
                    ("up", "M5"),
                    ("movex", landing("x")),
                    ("end",)]),
        dict(net="CMPO_B",
             start=("xant_cmpo_b", "CMPO_B"), stop=("xdig", "CMPO_B"),
             steps=[("up", "M4"),
                    ("movex", track("dband", 4)),
                    ("movey", landing("y")),
                    ("up", "M5"),
                    ("movex", landing("x")),
                    ("end",)]),

        #- RST_B: the pair's other reset, published on the same bottom
        #- edge as CMPO_A and leaving the same way -- south out of the
        #- pin, east along the floor, north up its own dband lane.
        #-
        #- DECLARED AND GATED OFF: this one does not close yet. It is
        #- left here rather than deleted so that turning it on is one
        #- name in `paths_only`, the same as PWRUP_B_1V8.
        #-
        #- THE FLOOR HAS ROOM FOR ONE LANE, and CMPO_A has it. Track 1
        #- sits at y 24000 and diode B's guard starts at 25000, so
        #- anything crossing x 1394900..1407900 up there takes met3.2
        #- (measured: 4). Track 0 is CMPO_A's, and one SPACE above it
        #- is not a lane -- an M4 leg is 3000 wide, so track 0 + SPACE
        #- abuts CMPO_A's own metal and track 0 + PITCH is track 1
        #- again.
        #-
        #- SO IT WAS TRIED ON ANOTHER LAYER, three times, and the fault
        #- did not move -- every one merged RST_B, RST_A and VDD_1V8
        #- into a single component of ~8000 rects:
        #-
        #-     M5 floor leg   shorts=1  DRC 6
        #-     M3 floor leg   shorts=1  DRC 8
        #-     M4 floor leg   is CMPO_A's lane; shorts by construction
        #-
        #- THE EAST END WAS THE WRONG SUSPECT. It looked like one,
        #- because `dig` records exactly this hazard for exactly this
        #- net. It is the FLOOR LEG, and VSS above says why: the pair's
        #- bottom nine microns are a VDD_1V8 guard (the lower half is
        #- mirrored MX, so its VDD strap is the floor), and `fband`
        #- track 0 resolves to y 18000, inside it. Every attempt put
        #- this leg in the VDD strap -- which is why all three merged
        #- RST_B, RST_A and VDD_1V8 rather than failing differently,
        #- and why the layer never mattered.
        #-
        #- Fix `fband` first -- the 6 um slot between the ring's top and
        #- the blocks' floor, measured off named_rects["rail_b_VSS"] in
        #- beforeRoute -- and try this again before touching the east
        #- end at all.
        #- VSS: ON M1, AND IT TURNS. The one net in this cell for which
        #- the preferred-direction convention is the wrong rule.
        #-
        #- M1 is what the supply IS in this library -- the rings are M1,
        #- every block's guard is M1, and three of the five VSS pins are
        #- M1 bars. A leg that runs horizontally on it is not crossing a
        #- plane it has to share; it is lying on the same metal the net
        #- already owns everywhere, and every guard it passes is another
        #- pin of itself. Nothing above M1 needs to be spent, which is
        #- the whole reason this is worth doing on the busiest cell in
        #- the design.
        #-
        #- The gap is real and it is a floorplan fact: the bottom ring
        #- runs y 0..9000 and xbias publishes VSS at 15000..24000, so
        #- the two never touch -- 6 um of nothing between a supply ring
        #- and the block it rings.
        #-
        #- DECLARED AND GATED OFF, one measurement short of working.
        #-
        #- THE PAIR'S FLOOR IS VDD, NOT VSS. That is the fact the whole
        #- bottom of this cell turns on, and it was assumed the other
        #- way round for a long time. LELOTEMP_CCMPR straps VSS at the
        #- bottom and VDD at the top; the pair mirrors the LOWER half
        #- MX, so that half's VDD strap is now the FLOOR. Asked
        #- directly (`blockers` VSS over 1024400..1374400 by
        #- 15000..30000):
        #-
        #-     VDD_1V8  at 16000  span 1024400..1374400
        #-     VDD_1V8  at 20000  span 1024400..1374400
        #-     VDD_1V8  at 24000  span 1024400..1374400
        #-
        #- Nine microns of VDD guard, the pair's full width. An M1 leg
        #- crossing under the pair lands on it: measured, VSS, VDD_1V8,
        #- CMPO_A and PWRUP_N in one component of 10451 rects.
        #-
        #- AND IT EXPLAINS RST_B, whose three failures were blamed on
        #- the east end. They were not. `fband` as registered runs
        #- layout.y1..cc.y1 but its track 0 resolves to y 18000 --
        #- INSIDE that guard -- so every RST_B attempt put its floor leg
        #- in the VDD strap and merged RST_B, RST_A and VDD_1V8. CMPO_A
        #- survives the same track only because it crosses on M4 and the
        #- guard is M1.
        #-
        #- SO THE M1 IDEA IS RIGHT AND THE LANE IS WRONG. M1 is what the
        #- supply IS here and a turning M1 leg costs no plane at all;
        #- what it may not do is run at 15000..24000. The lane is the
        #- 6 um slot between the bottom ring's top (9000) and the
        #- blocks' floor (15000), and that is not a number to spell:
        #- register `fband` off `named_rects["rail_b_VSS"]` in
        #- beforeRoute, where the ring exists, exactly as LELOTEMP_CCMPR
        #- registers its own "base" band. Then track 0 is the slot, and
        #- both this and RST_B have a floor to cross on.
        #-
        #- Three legs, west to east, each landing on the next pin:
        #- bias to diode B, diode B to diode A, and diode A up to the
        #- strip.
        #- VSS HAS NO ENTRIES HERE, and that is a finding, not an
        #- omission. The supplies phase already draws a ring leg to
        #- every VSS pin the flight lines showed apart: ring to xbias
        #- (M1 x 488100), ring to each antenna diode (M1 x 1399900 and
        #- 1411900), and ring to the strip's M4 pin (x 1478800, y
        #- 3000..179000 -- proof, incidentally, that the strip's VSS
        #- column is ridable on M4). Three declared ring legs were
        #- written here and changed the component count by exactly
        #- nothing; a fourth leg to the strip crossed VDD's own
        #- full-height M4 riser in dband (x 1423900..1426900, y
        #- 19500..1091600 -- checkroutes' own chain) and shorted.
        #- The two components that remained, found by flooding the
        #- built .cic with the ring metal included:
        #-
        #-   * the supply phase's own riser to the strip is M4 from
        #-     y 3000 -- OVER the M1 ring, with no via at the ring
        #-     end. It floats. The first entry below is the same
        #-     riser said as a story, whose `up` puts the via ON the
        #-     ring; the two then merge along the column.
        #-   * the pair's SEAM pin -- both halves' VSS straps meet at
        #-     y 517000..526000 and publish one M1 bar that nothing
        #-     touches. The second entry walks it west into lband
        #-     (which is empty on M1; every story there rides M3 and
        #-     above) and down to the ring on the supply's own layer.
        dict(net="VSS", layer="M1", at="w",
             start=("xccmp", "VSS"), stop="ring_b_VSS",
             steps=[("movex", track("lband", 0) + SPACE),
                    ("movey", landing("y")),
                    ("end",)]),
        dict(net="RST_B", at="s", options="1cuts,2vcuts",
             start=("xccmp", "RST_B"), stop=("xdig", "RST_B"),
             steps=[("up", "M3"),
                    ("movey", track("fband", 0) - PITCH),
                    ("movex", pin("xdig", "RST_B", "x") + 2 * PITCH),
                    ("up", "M4"),
                    ("movey", landing("y")),
                    ("movex", landing("x")),
                    ("end",)]),
    ]

    #- PWRUP_B is a SEARCH, not a story, and cannot become one. dband's
    #- lanes are spoken for (four nets and a supply tie) and the sliver
    #- before the strip's pins is where every other net's last leg
    #- goes, so this one is handed a layer budget and left to find its
    #- own way OVER the strip.
    #-
    #- leg 1, bias -> pair: M2/M3/M5 and NOT M4. The pair's east edge
    #- is the cap bank, and a leg on M4 there is met3 under a MiM,
    #- which capm.11 keeps 1.34 um clear of. With M4 in the stack this
    #- is LVS clean and 9 DRC -- eight capm.11 and met3.2/met3.3d, all
    #- at 136..138 um, which is that edge. Without it, none.
    #- leg 2, pair -> strip: M3/M4. Both ports are low and on M3, and
    #- there is no MiM between them.
    #- PWRUP_B WAS THE ONE MAZE LEFT, and converting it is what
    #- finished the cell. The search genuinely earned its keep here --
    #- it discovered that the pair's INTERIOR is crossable (nothing in
    #- the lane plan knew that) -- but its output could not be kept:
    #- the descent x was a bare coordinate, its landing at the bias
    #- pin wanted an M3M5 cut that does not exist (nothing was drawn,
    #- the net stayed split, and the log said links=1/1), and its
    #- drawn staircase left 3 met2.2 slivers at the pair's pin. The
    #- topology it found, told as two stories: every x is a pin, a
    #- measured channel, or a lane offset, and the via stack at the
    #- bias pin goes through M4 -- which the maze's layer budget
    #- forbade globally because of capm.11 at the PAIR's east edge, a
    #- rule about a place this stack is nowhere near.
    mazes = []
    paths = paths + [
        dict(net="PWRUP_B_1V8",
             start=("xbias", "PWRUP_B_1V8"), stop=("xccmp", "PWRUP_B_1V8"),
             steps=[("down", "M4"),
                    ("down", "M3"),
                    #- two lanes INTO the measured column, so the via
                    #- pads at its two corners stand clear of the metal
                    #- that bounds it -- the column's edge is where the
                    #- neighbour's metal begins
                    ("movex", track("pband", 0) + 2 * PITCH),
                    ("down", "M2"),
                    ("movey", landing("y")),
                    ("up", "M3"),
                    ("movex", landing("x")),
                    ("end",)]),
        dict(net="PWRUP_B_1V8", at="e", options="1cuts,2vcuts",
             start=("xccmp", "PWRUP_B_1V8"), stop=("xdig", "PWRUP_B_1V8"),
             steps=[#- one SPACE past the track: the 1x2 pad is wider
                    #- than the wire and its west edge stood 1.1 um
                    #- from the pin where met2.2 wants 1.4
                    ("movex", track("dband", 0) + SPACE),
                    ("up", "M4"),
                    ("movey", landing("y")),
                    ("down", "M3"),
                    ("movex", landing("x")),
                    ("end",)]),
    ]

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
        #- AND THE FLOOR. `cband` is the band ABOVE the pair and it is
        #- what RST_A and PWRUP_N leave by; the nets published on the
        #- pair's BOTTOM edge -- CMPO_A, CMPO_B, RST_B -- had no
        #- corridor named at all, which is most of why they had no
        #- story. The strip below the blocks is the same kind of fact
        #- about the same floorplan.
        #-
        #- Measured before registering it (`blockers`, CMPO_A over
        #- 1120000..1450000 by 0..16000): the only pin spans in it are
        #- VDD_1V8's own ring bars at y 12000 and 16000, which are M1.
        #- A leg that crosses on M3 or above clears them, and nothing
        #- else is down there.
        layout.addRoutingChannel("fband", int(layout.y1), int(cc.y1))
        #- and the lane in front of the strip's own pins, measured off
        #- the westmost of them. Lost in a rewrite once, and the story
        #- that aimed at it did not fail -- the anchor resolved to
        #- None, the move was skipped, and PWRUP_B descended in
        #- `lband` and crossed the tile at its landing row. It is
        #- registered HERE with the other three now, because a channel
        #- is a fact about the placement and the paths that use it are
        #- a declaration that cannot register anything.
        west = [c.get() for c in getattr(dg, "children", []) or []
                if getattr(c, "isPort", lambda: False)()]
        west = [r for r in west if r is not None]
        if west:
            layout.addRoutingChannel("eband", int(dg.x1),
                                     min(int(r.x1) for r in west),
                                     horizontal=False)

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
        #- the `paths` table sends the descents down (4 and 6), which is what
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
        #- into one component holding thirty-odd nets. What the
        #- `paths` table encodes is exactly what the search lacks -- a
        #- lane budget and a layer reservation per band.
        #- ONE PHASE AT A TIME, same reason as `paths_only`: a short
        #- is found by taking routing AWAY until it goes.
        for name in self._PHASES:
            getattr(self, "_" + name)(layout)
        #- PWRUP_B's corridor THROUGH the pair, measured off the pair
        #- itself. The maze found this topology -- across at the bias
        #- pin's row, down through the pair's interior, across again at
        #- the pair's own pin row -- and could not be allowed to keep
        #- it: its descent x was a coordinate, and its bias-pin landing
        #- needed an M5-M3 cut this library does not have (drawVia drew
        #- nothing, silently, and the net stayed split while the maze
        #- reported links=1/1). The descent column is a MEASUREMENT:
        #- the pair's free M2 columns over exactly the span the leg
        #- runs, asked of its block view, registered here because a
        #- channel is a fact about the placement.
        cc = layout.getInstanceFromInstanceName("xccmp")
        ccell = (getattr(cc, "layoutcell", None)
                 or getattr(cc, "_cell_obj", None)) if cc is not None else None
        if ccell is not None and hasattr(ccell, "freeColumns"):
            a = self.declaredPort(layout, "xccmp", "PWRUP_B_1V8")
            b = self.declaredPort(layout, "xbias", "PWRUP_B_1V8")
            if a is not None and b is not None:
                span = (int(a.y2) - int(cc.y1), int(b.y1) - int(cc.y1))
                cols = ccell.freeColumns("M2", span=span,
                                         net="PWRUP_B_1V8")
                if cols:
                    #- the widest column, so the wire and its two via
                    #- pads all fit inside what was measured
                    x1, x2 = max(cols, key=lambda c: c[1] - c[0])
                    layout.addRoutingChannel(
                        "pband", int(cc.x1) + int(x1),
                        int(cc.x1) + int(x2), horizontal=False)
                else:
                    layout.log.error(
                        "pband: the pair has no free M2 column over "
                        "PWRUP_B's span; the leg will not draw")
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

        #- and the comparators' VDD climbs the 4 um gap between the
        #- pair and the strip.
        #-
        #- IT LEAVES THE BAR ON M2, IT DOES NOT SLIDE ALONG IT.
        #- Sliding east on M1 to reach the column is the one thing
        #- this file already warns against twice, and it did it here:
        #- the run crossed the row east of the pair's top ring and
        #- tied the WHOLE VDD network into VSS -- both comparators,
        #- both tapcells' AVDD, all thirteen JNWTR_PCHDL bulks and the
        #- bias block. Nothing in checkroutes named it (the bridges it
        #- printed were all VSS to VSS) and no DRC rule catches a
        #- short. netgen did: `Net: VSS` came back with
        #- LELOTEMP_CCMPR/VDD_1V8 in it.
        #-
        #- So the story starts on a SLICE of the bar at its own east
        #- end, rises to M3 there, and travels in the air.
        bar = self._port(ccmp, "VDD_1V8", top)
        if bar is not None:
            from cicpy.core.rect import Rect as _RS
            seed = _RS(bar.layer, int(bar.x2) - 9000, int(bar.y1), 3000,
                       int(bar.y2) - int(bar.y1))
            seed.setNet("VDD_1V8")
            p = layout.path("VDD_1V8", "M1", start=[seed], stop=[rt])
            p.start()
            p.up()                       #- M2
            p.up()                       #- M3, and east in the air
            #- TRACK 8, NOT 1: the pair's east edge is its cap bank,
            #- and a MiM claims 1.34 um from unrelated M4 (capm.11) --
            #- including metal outside its own cell. The riser stood
            #- 0.75 um off it on the first track and 1.22 on the
            #- second, where the wire cleared but the via pad, half
            #- again as wide, did not.
            p.movex(p.track("dband", 8))
            p.up()                       #- M4, up the gap
            p.movey(p.landing("y"))
            p.down()
            p.down()
            p.down()                     #- M1, onto the ring

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
