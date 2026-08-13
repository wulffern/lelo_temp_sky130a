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
        order = ['xtap_dig_0', 'x6', 'x2', 'x7', 'x3', 'x4', 'x1',
                 'x5']

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
                lay.updatePort(net, pad, routeLayer="M2")

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
                pad = _R("M2", int(pin.centerX()) - wides["M3"] // 2,
                         y - pads["M3"] // 2, wides["M3"], pads["M3"])
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
        #- DROP EVERY BLOCK 0.13 um, to buy the top band its
        #- clearance. The lanes over the bias block need 0.40 under
        #- the first one (met4.5a/b, "attached to large metal4"), and
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
        self._supplies(layout)
        self._ibp(layout)
        super().beforeRoute(layout)


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
            p.movex(p.track("dband", 3))
            p.up()
            p.up()
            p.up()
            p.movey(p.landing("y"))
            p.down()
            p.down()
            p.down()

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
        b.movey(b.track("cband", 30))
        b.down("M4")

        #- and from here each net is alone: two turn down in the gap
        #- west of the pair, two carry on over it
        for i, net in enumerate(nets):
            p = b.member(net)
            p.movex(p.track("lband", 2 + i * 2) if i < 2
                    else p.landing("x"))
            p.movey(p.landing("y"))
            p.down(stops[i].layer)
            p.movex(p.landing("x"))
            p.end()
