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

    class ccmp_a(Stack):
        """The comparator on IBP_1U<3:2> (CMPO_A, reset RST_B)."""
        match = r'^x2_ccmp$'
        group = "ccmp"
        fill = False
        xspace = 5
        order = ['x2_ccmp']

    class ccmp_b(Stack):
        """The comparator on IBP_1U<1:0> (CMPO_B, reset RST_A).
        Placed above ccmp_a by afterPlace."""
        match = r'^x3_ccmp$'
        group = "ccmp"
        fill = False
        order = ['x3_ccmp']

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
            #- every net is hand-routed at the top; the built-in
            #- series router has nothing to say about logic cells
            return True

    rows = [
        [bias, ccmp_a, dig],
    ]

    supplies = []

    def afterPlace(self, layout):
        super().afterPlace(layout)
        from cicpy.core.subcell import subcell_groups
        g = subcell_groups(layout)
        ca, cb = g.get("ccmp_a"), g.get("ccmp_b")
        if ca is not None and cb is not None:
            #- the L: ccmp_b above ccmp_a, lefts aligned
            cb.abutTop(ca, space=4 * layout.um)
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

    def beforeRoute(self, layout):
        #- rings on an EXPLICIT rect: addRouteRing wraps the layout
        #- bbox, which does not count the physical-only tapcell, so
        #- the bottom ring landed 2 um INSIDE the content and its 9 um
        #- li bar shorted the logic strip's AVDD to AVSS (measured).
        #- The rect here spans every instance, tap included.
        from cicpy.core.rect import Rect as _RR
        names = ["x1_ibp", "x2_ccmp", "x3_ccmp", "xtap_dig_0",
                 "x1", "x2", "x3", "x4", "x5", "x6", "x7"]
        boxes = [layout.getInstanceFromInstanceName(n) for n in names]
        boxes = [i for i in boxes if i is not None]
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
            #- instead of the lane plan below, with no guidance at all
            #- -- one addConnectivityRoute per net and nothing else.
            #-
            #- It wins, on every number that can be measured:
            #-
            #-                   lane plan (778 lines)   router
            #-   DRC                   72                  66
            #-   shorts                13                   6
            #-   opens                 13                   8
            #-   time                   -                 3.3 s
            #-
            #- Neither passes LVS -- the hand build says "Netlists do
            #- not match", the router's "failed pin matching", and
            #- matchports --apply does not move it. But the router is
            #- closer on both counts it can be judged by, from a
            #- standing start, and that is the argument for converting
            #- this cell rather than repairing it.
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
            _skip = {"VDD_1V8", "VSS"}
            for _net in list(getattr(layout, "nodeGraphList", []) or []):
                if _net in _skip:
                    continue
                layout.addConnectivityRoute(
                    "M5", "^" + _re.escape(_net) + "$", "-|--", "", 2,
                    "", "")
        else:
            self._signal_routes(layout)
        super().beforeRoute(layout)


    def beforePaint(self, layout):
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

    def _dbg_dig(self, layout):
        for nm in ("x6", "x7"):
            i = layout.getInstanceFromInstanceName(nm)
            for net, pt in sorted(i.instancePorts.items()):
                r = pt.get()
                if r is not None:
                    log.warning(f"DBG {nm}.{net} {r.layer} ({int(r.x1)},{int(r.y1)})..({int(r.x2)},{int(r.y2)})")

    def _signal_routes(self, layout):
        self._dbg_dig(layout)
        """Every top net, hand-placed on the lane plan.

        Corridors (all coordinates from the placed pins; the lanes
        are formulas off the block edges): the 5 um bias-ccmp GAP
        carries eight vertical lanes L1..L8; the strip ABOVE the
        content four horizontal M5 lanes S1..S4 (M4 risers cross
        them); B lanes run under the comparators, My lanes between
        them, D lanes down the ccmp-dig gap, and every logic pin is
        reached by an M2 stub at its own row -- the JNWTR cells
        carry no metal1/metal2, so M2 crosses them freely.
        """
        from cicpy.core.rect import Rect
        from cicpy.core.cut import Cut

        #- Every hand route is recorded here, and _report_collisions
        #- below walks the list for two nets sharing a layer and a
        #- spot. Bisecting builds against the extract to find one
        #- crossing took the best part of a day; this finds them all
        #- in the build that made them.
        drawn = []

        def wire(net, layer, x1, y1, x2, y2):
            r = Rect(layer, int(min(x1, x2)), int(min(y1, y2)),
                     int(abs(x2 - x1)), int(abs(y2 - y1)))
            r.setNet(net)
            layout.add(r)
            drawn.append((net, layer, int(min(x1, x2)), int(min(y1, y2)),
                          int(max(x1, x2)), int(max(y1, y2))))
            return r

        def stk(net, la, lb, x, y):
            ct = (Cut.getInstance(la, lb, 1, 1)
                  or Cut.getInstance(lb, la, 1, 1))
            if ct is None:
                log.error(f"no cut {la}-{lb} for {net}")
                return
            ct.moveCenter(int(x), int(y))
            layout.add(ct)
            #- A stack's pad on a layer it only passes through is the
            #- cut's own, 0.44 x 0.44 um = 0.19 um^2, under the 0.24
            #- that met3.6/met4.4a want. Patch the pass-through metal
            #- layers to 0.5 um square.
            names = ["M1", "M2", "M3", "M4", "M5"]
            try:
                _lo, _hi = sorted((names.index(la), names.index(lb)))
            except ValueError:
                _lo = _hi = -1
            for _k in range(_lo + 1, _hi):
                if names[_k] not in ("M4", "M5"):
                    continue
                #- 0.3 x 0.85 um, not a 0.5 um square: the square is
                #- wider than the 3 um lanes and ate the spacing to
                #- the neighbouring lane on both sides
                pt = Rect(names[_k], int(x) - 1500, int(y) - 4250,
                          3000, 8500)
                pt.setNet(net)
                layout.add(pt)
            names = ["M1", "M2", "M3", "M4", "M5"]
            try:
                lo, hi = sorted((names.index(la), names.index(lb)))
            except ValueError:
                return
            hw = int(ct.width()) // 2 or 1600
            hh = int(ct.height()) // 2 or 1600
            for k in range(lo, hi + 1):
                drawn.append((net, names[k], int(x) - hw, int(y) - hh,
                              int(x) + hw, int(y) + hh))

        def P(inst, net):
            i = layout.getInstanceFromInstanceName(inst)
            pt = i.instancePorts.get(net) if i is not None else None
            r = pt.get() if pt is not None else None
            if r is None:
                log.error(f"no pin {inst}.{net}")
            return r

        def pad(net, r, x=None):
            #- an M2 landing on an li pin: pad plus mcon
            cx = int(x if x is not None else r.centerX())
            cy = int(r.centerY())
            wire(net, "M2", cx - 1700, cy - 1700, cx + 1700, cy + 1700)
            stk(net, "M1", "M2", cx, cy)

        import os
        RT = os.environ.get("RT", "all")
        on = lambda k: RT == "all" or k in RT
        w = 3000
        bias = layout.getInstanceFromInstanceName("x1_ibp")
        GAP = int(bias.x2)                       # 960000
        #- L: 1 um off the bias edge, not 2.5 -- L(8) sat 2.5 um from
        #- the comparator's own M5 edge bar, and met4.2 wants 3.
        L = lambda i: GAP + 1000 + (i - 1) * 6000
        #- S: the IBP bars leave the bias on M5 and turn east over its
        #- top. The lanes must clear the bars' own tops (they cross
        #- every bar on the way) and stay under the top ring -- and
        #- under the TinyTapeout ceiling, which the old rows at
        #- bias.y2+1900 and up overshot by 2 um. 7.5 um pitch: the
        #- M4-M5 cut pads are 4.8 um, wider than the 3 um lane, so a
        #- 6 um pitch leaves 1.2 um between pads.
        #- clear of the block's OWN M5, which reaches 1.5 um higher
        #- than the IBP pins do -- the wide source bars in the middle
        #- of the block. Basing the rows on the pin tops ran S(1) and
        #- S(2) straight through them (measured: IBP<3:2> on VDD).
        #- ABOVE the block, not in its top strip: the strip carries
        #- the block's own straps and the two lowest lanes shorted
        #- IBP<3:2> onto VDD there (measured). 0.7 um pitch -- these
        #- are long runs, and met4.5a/b ask 0.4 um of a long M4/M5
        #- shape, not the 0.3 um of met4.2. So 0.3 of wire + 0.4 of
        #- gap, and the FIRST lane needs that same 0.4 to the block
        #- below it: at +1900 it sat 0.19 away and fired 24 times, once
        #- per column, because the block's 7.2 um M5 columns repeat at
        #- 8 um. +4000 is the rule, not a tuning.
        #-
        #- NOTE ON UNITS: these are cicpy units, 10000 to the micron.
        #- The numbers here are right and the older comments in this
        #- method are not -- they read "7 um" for 7000, which is 0.7.
        S = lambda j: int(bias.y2) + 4000 + (j - 1) * 7000
        #- The B and MY bands carry lanes on THREE layers, and only
        #- same-layer lanes need the 3 um metal pitch: M3 and M4 lanes
        #- share row 1 with the M5 lanes stacked above them at 6 um.
        #- At the old 4.5 um pitch every neighbour pair was 1.5 um
        #- apart and met3.2/met4.2 fired right down the band.
        B = lambda j: 1500 + (j - 1) * 6000
        ca = layout.getInstanceFromInstanceName("x2_ccmp")
        cb = layout.getInstanceFromInstanceName("x3_ccmp")
        MY = lambda j: int(ca.y2) + 1500 + (j - 1) * 6000
        D = lambda i: int(ca.x2) + 3200 + (i - 1) * 6000

        import os
        RT = os.environ.get("RT", "all")
        on = lambda k: RT == "all" or k in RT.split(",")

        #- ---------------------------------------------------------------
        #- Reaching the logic strip.
        #-
        #- The ccmp-dig corridor is 40 um wide and eight nets wanted a
        #- vertical in it: six 6 um lanes, and every attempt to wedge
        #- the extra two in landed on a neighbour. But the corridor is
        #- the wrong place for them. The JNWTR logic cells carry li,
        #- poly and their two M4 supply columns and NOTHING else, so
        #- M2, M3 and M5 are free the whole height of the strip -- the
        #- fan-out verticals belong OVER the cells, not beside them.
        #-
        #- So each net crosses the corridor once, on M5, at its own y,
        #- and turns down an M2 column of its own over the strip; a
        #- short M3 stub reaches each pin from there. The corridor
        #- keeps only horizontals, which cannot collide with the
        #- supply ties (M4/M5 verticals) or with each other.
        dig0 = layout.getInstanceFromInstanceName("x7")
        DIG_X1 = int(dig0.x1)
        #- The strip's own occupancy, in cell-local units off DIG_X1.
        #- The li pins do not block M2 -- only these do:
        #-   31500..40300   AVSS column: an M1-M4 cut stack in every
        #-                  cell, so an M2 column here ties every Y
        #-                  pin to AVSS (measured)
        #-   58500..67300   AVDD column, same stack
        #-   16300..19700   the M2 pad this file lands on each A pin
        #-   34300..37700   the same on each Y pin
        #- Columns run at a 6 um pitch: the M2-M3 cut pad is 4.4 um,
        #- wider than the 3 um column, and a tighter pitch leaves the
        #- pads 1.1 um apart where met1.2 wants 1.4.
        COL = {
            "CMPO_A":      DIG_X1 + 1000,
            "CMPO_B":      DIG_X1 + 7000,
            "RST_B":       DIG_X1 + 23500,
            "RST_A":       DIG_X1 + 42000,
            "PWRUP_N_1V8": DIG_X1 + 48000,
            "PWRUP_B_1V8": DIG_X1 + 54000,
            "net1":        DIG_X1 + 68000,
            "net2":        DIG_X1 + 74000,
        }

        def link_logic(net, pins, ylane=None, x_from=None):
            """The net's own M2 column over the strip, with an M3 stub
            to every pin. With ylane/x_from it first crosses the
            corridor on M5 at that row and drops into the column."""
            col = COL[net]
            rows = [int(P(i, n).centerY()) for i, n in pins]
            if ylane is not None:
                wire(net, "M5", x_from, ylane, col + w, ylane + w)
                stk(net, "M5", "M2", col + 1500, ylane + 1500)
                rows.append(ylane + 1500)
            wire(net, "M2", col, min(rows) - 1500, col + w,
                 max(rows) + 1500)
            for inst, pinname in pins:
                r = P(inst, pinname)
                ry = int(r.centerY())
                #- M3 across: an M2 stub would cross the other nets'
                #- columns on its own layer. At MINIMUM width: the
                #- cells' pin rows are 4 um apart, and 3 um stubs on
                #- neighbouring rows leave 1 um where met2.2 wants
                #- 1.4. The cut pads are wider than that, but two
                #- neighbouring rows belong to different nets on
                #- different columns, so their pads never meet.
                stk(net, "M2", "M3", col + 1500, ry)
                wire(net, "M3", col, ry - 700,
                     int(r.centerX()) + 1700, ry + 700)
                stk(net, "M3", "M2", int(r.centerX()), ry)
                pad(net, r)

        def to_logic(net, x_from, ylane, pins):
            link_logic(net, pins, ylane=ylane, x_from=x_from)

        if on("lpi"):
            #- LPI: the loop -- the OTA output back to the bias input.
            #- Both pins share the net, so the port dict keeps one; take
            #- both rects off the instance's children.
            lpis = [c.get() for c in bias.children
                    if getattr(c, "isPort", lambda: False)()
                    and getattr(c, "name", "") == "LPI"]
            lpo = max(lpis, key=lambda r: r.y1)      # the OTA output pad
            lpi = min(lpis, key=lambda r: r.y1)      # the bar's right end
            y = int(lpo.centerY())
            stk("LPI", "M3", "M5", int(lpo.x2) - 3000, y)
            wire("LPI", "M5", int(lpo.x2) - 4500, y - 1500, L(1) + w, y + 1500)
            wire("LPI", "M5", L(1), int(lpi.centerY()) - 1500, L(1) + w, y + 1500)
            wire("LPI", "M3", int(lpi.x2), int(lpi.y1), L(1) + w, int(lpi.y2))
            stk("LPI", "M3", "M5", L(1) + 1500, int(lpi.centerY()))

        if on("vc"):
            #- VC: the bias VD1 bar to both comparators' VC pins
            vcb = P("x1_ibp", "VC")
            yv = int(vcb.centerY())
            wire("VC", "M3", int(vcb.x2), yv - 1500, L(2) + w, yv + 1500)
            wire("VC", "M3", L(2), B(1), L(2) + w, yv + 1500)
            for tgt, ylane in ((P("x2_ccmp", "VC"), B(1)),
                               (P("x3_ccmp", "VC"), MY(1))):
                #- the pin sits at the comparator CORE's bottom edge: the
                #- riser must be the pin's own M2 -- the core is full of
                #- everything below M5 (measured: an M3 riser merged the
                #- mirror tails)
                wire("VC", "M3", L(2), ylane, int(tgt.x2), ylane + w)
                stk("VC", "M3", "M2", int(tgt.centerX()), ylane + 1500)
                wire("VC", "M2", int(tgt.x1), ylane,
                     int(tgt.x2), int(tgt.y2))
            wire("VC", "M3", L(2), MY(1), L(2) + w, yv)

        if on("ibp"):
            #- IBP_1U<0..3>: the bias's M5 su-channel bars over the top
            #- strip and down the gap. Risers M4 so they cross the M5
            #- strip lanes; each turns to M5 only in its own lane.
            ibp = []
            for k in range(4):
                ibp.append(P("x1_ibp", f"IBP_1U<{k}>"))
            #- RIGHT to LEFT: each bar climbs to its lane on its OWN
            #- M5, which is the only layer that crosses the block's
            #- top strip cleanly -- an M4 riser met the block's own
            #- straps there (measured: IBP<3:2> on VDD). A riser can
            #- only stay on M5 if no LOWER lane passes over it, and
            #- the lanes run east, so the rightmost bar takes the
            #- lowest lane.
            keys = ["IBP_1U<3>", "IBP_1U<2>", "IBP_1U<1>", "IBP_1U<0>"]
            tgts = [P("x2_ccmp", "IBP_1U<3>"), P("x2_ccmp", "IBP_1U<2>"),
                    P("x3_ccmp", "IBP_1U<1>"), P("x3_ccmp", "IBP_1U<0>")]
            bars = [ibp[3], ibp[2], ibp[1], ibp[0]]
            hows = ["M3stub", "B2", "M3stub", "MY2"]
            _ib = os.environ.get("IB", "0123")
            for _k, (net, bar, sj, li_, tgt, how) in enumerate(zip(
                    keys, bars, (1, 2, 3, 4), (3, 4, 5, 6), tgts, hows)):
                if str(_k) not in _ib:
                    continue
                bx = int(bar.centerX())
                wire(net, "M5", bx - 1500, int(bar.y2) - 3000,
                     bx + 1500, S(sj) + w)
                wire(net, "M5", bx - 1500, S(sj), L(li_) + w, S(sj) + w)
                stk(net, "M5", "M4", L(li_) + 1500, S(sj) + 1500)
                if how == "B2":
                    wire(net, "M4", L(li_), B(2), L(li_) + w, S(sj) + w)
                    wire(net, "M4", L(li_), B(2), int(tgt.x2), B(2) + w)
                    stk(net, "M4", "M2", int(tgt.centerX()), B(2) + 1500)
                    wire(net, "M2", int(tgt.x1), B(2),
                         int(tgt.x2), int(tgt.y2))
                elif how == "MY2":
                    wire(net, "M4", L(li_), MY(2), L(li_) + w, S(sj) + w)
                    wire(net, "M4", L(li_), MY(2), int(tgt.x2), MY(2) + w)
                    stk(net, "M4", "M2", int(tgt.centerX()), MY(2) + 1500)
                    wire(net, "M2", int(tgt.x1), MY(2),
                         int(tgt.x2), int(tgt.y2))
                else:  # M3stub: the pin is M3 at the ccmp's left edge
                    ty = int(tgt.centerY())
                    wire(net, "M4", L(li_), ty - 1500,
                         L(li_) + w, S(sj) + w)
                    stk(net, "M4", "M3", L(li_) + 1500, ty)
                    wire(net, "M3", L(li_), int(tgt.y1),
                         int(tgt.x2), int(tgt.y2))

        if on("pwrn"):
            #- PWRUP_N: off the bias's M5 riser sideways at its own
            #- attach row, down L7 to both comparators' edge bars, and
            #- on to the logic under everything
            pn = P("x1_ibp", "PWRUP_N_1V8")
            pnx = int(pn.centerX())
            #- on the riser, above both risers' bases (the bases sit at
            #- the OTA pins; constants here were once bias-frame and
            #- missed by the placement offset -- derive from the pin)
            #- low on the riser: the PWRUP_B riser two tracks east
            #- hangs down to 856000, and an attach row above that
            #- crossed it on M5 (measured: PWRUP_N merged with the
            #- whole PWRUP_B/OTA chain)
            yn = int(pn.y1) - 300000
            wire("PWRUP_N_1V8", "M5", pnx - 1500, yn - 1500,
                 L(7) + w, yn + 1500)
            #- the crossing row: above ccmp_b, where the corridor
            #- carries nothing. The B band under ccmp_a is 24 um tall
            #- and holds four lanes at the 6 um metal pitch, which VC,
            #- IBP, RST_B and PWRUP_B already fill.
            ytn = int(cb.y2) + 8500
            #- the L7 riser has to cover EVERY attach row: the bias
            #- stub, both comparator bars and the crossing row. When
            #- the crossing moved above the pair it stopped reaching
            #- down to the bars and ccmp_b's PWRUP_N went open.
            _bys = [int(P(cc, "PWRUP_N_1V8").centerY())
                    for cc in ("x2_ccmp", "x3_ccmp")]
            wire("PWRUP_N_1V8", "M5", L(7), min(_bys + [yn]) - 1500,
                 L(7) + w, max(_bys + [ytn + w, yn + 1500]))
            for cc in ("x2_ccmp", "x3_ccmp"):
                #- the stub crosses the PWRUP_B L8 vertical: hop it on
                #- M4, with the vias on the L7 vertical and on the
                #- ccmp's own edge bar
                bar = P(cc, "PWRUP_N_1V8")
                by = int(bar.centerY())
                stk("PWRUP_N_1V8", "M5", "M4", L(7) + 1500, by)
                wire("PWRUP_N_1V8", "M4", L(7), by - 1500,
                     1014500, by + 1500)
                stk("PWRUP_N_1V8", "M4", "M5", 1013000, by)
            #- PWRUP_N is the only net that starts WEST of L(8), and
            #- L(8) is PWRUP_B's M5 riser spanning the whole height:
            #- crossing it on M5 shorted the two (measured). Hop over
            #- on M4, then carry on east.
            wire("PWRUP_N_1V8", "M5", L(7), ytn, L(7) + 4500, ytn + w)
            stk("PWRUP_N_1V8", "M5", "M4", L(7) + 3000, ytn + 1500)
            wire("PWRUP_N_1V8", "M4", L(7) + 3000, ytn,
                 L(8) + 7500, ytn + w)
            stk("PWRUP_N_1V8", "M4", "M5", L(8) + 6000, ytn + 1500)
            to_logic("PWRUP_N_1V8", L(8) + 4500, ytn,
                     [("x2", "PWRUP_N_1V8"), ("x7", "PWRUP_N_1V8"),
                      ("x6", "PWRUP_N_1V8")])

        if on("pwrb"):
            #- PWRUP_B: off the bias riser at the pad row, down L8, under
            #- the comparators to their bottom drops, and to x2's output
            pb = P("x1_ibp", "PWRUP_B_1V8")
            pbx = int(pb.centerX())
            yb = int(pb.y1) - 124000
            wire("PWRUP_B_1V8", "M5", pbx - 1500, yb - 1500,
                 L(8) + w, yb + 1500)
            wire("PWRUP_B_1V8", "M5", L(8), B(4), L(8) + w, yb + 1500)
            #- B(5)/MY(4): a riser must sit on the HIGHEST lane of its
            #- band, or it climbs through the ones above it
            for cc, yl in (("x2_ccmp", B(4)), ("x3_ccmp", MY(5))):
                drop = P(cc, "PWRUP_B_1V8")
                #- the ccmp's own drop column stands 12000 east of the
                #- interior pin and STOPS at the top of the cell's own
                #- bottom ring (local y 24000), so the riser must reach
                #- INTO it. The column at local x 378000 looks like a
                #- drop but is the caps' VSS M1-M5 stack: landing there
                #- shorted PWRUP_B into VSS (measured).
                ci = layout.getInstanceFromInstanceName(cc)
                dx = int(drop.x2) + 12000
                #- climb into the cell on M5 and only THEN drop to the
                #- drop's own layer: an M3 riser through the cell's
                #- bottom ring band merged PWRUP_B into VSS (measured,
                #- both comparators). The cut sits above the cell's
                #- IBP band bar (local y 19500) and inside the drop,
                #- which spans local y 24000..126000.
                ylo = int(ci.y1) + 30000
                wire("PWRUP_B_1V8", "M5", L(8), yl, dx + 6000, yl + w)
                #- the riser climbs past the lanes ABOVE this one --
                #- PWRUP_N under ccmp_a, CMPO_A between the pair -- so
                #- it crosses them on M4 and turns M5 only in the gap
                #- below the cell, where M4 would hit the block's own
                #- IBP band bar (local y 13500..19500)
                ymid = int(ci.y1) - 1000
                stk("PWRUP_B_1V8", "M5", "M4", dx + 3000, yl + 1500)
                wire("PWRUP_B_1V8", "M4", dx, yl, dx + 6000, ymid + w)
                stk("PWRUP_B_1V8", "M4", "M5", dx + 3000, ymid + 1500)
                wire("PWRUP_B_1V8", "M5", dx, ymid, dx + 6000,
                     ylo + 4000)
                stk("PWRUP_B_1V8", "M5", "M3", dx + 3000, ylo)
                wire("PWRUP_B_1V8", "M3", dx, ylo - 4000,
                     dx + 6000, ylo + 4000)
            #- cross at MY(4), the lane its ccmp_b drop already uses:
            #- RST_B owns B(3), and two nets on one M5 lane is a short
            to_logic("PWRUP_B_1V8", L(8), MY(5),
                     [("x2", "PWRUP_B_1V8")])

        if on("cmpoa"):
            #- CMPO_A: comparator A's output up into the My window and
            #- east on M5 to its own column over the logic strip
            cma = P("x2_ccmp", "CMPO_A")
            cx = int(cma.centerX())
            wire("CMPO_A", "M2", cx - 1500, int(cma.y1), cx + 1500,
                 MY(4) + w)
            stk("CMPO_A", "M2", "M5", cx, MY(4) + 1500)
            to_logic("CMPO_A", cx - 1500, MY(4), [("x1", "CMPO_A")])

        if on("cmpob"):
            #- CMPO_B: comparator B's output over its own top, then east
            cmb = P("x3_ccmp", "CMPO_B")
            cx = int(cmb.centerX())
            ytop = int(cb.y2) + 2500
            wire("CMPO_B", "M2", cx - 1500, int(cmb.y1), cx + 1500,
                 ytop + w)
            stk("CMPO_B", "M2", "M5", cx, ytop + 1500)
            to_logic("CMPO_B", cx - 1500, ytop, [("x7", "CMPO_B")])

        if on("rstb"):
            #- RST_B: comparator A's reset, out of its bottom pin into
            #- the B band and east to the NORs and the buffer
            rstb = P("x2_ccmp", "RST_B")
            rx = int(rstb.centerX())
            wire("RST_B", "M2", rx - 1500, B(3), rx + 1500, int(rstb.y2))
            stk("RST_B", "M2", "M5", rx, B(3) + 1500)
            to_logic("RST_B", rx - 1500, B(3),
                     [("x3", "RST_B"), ("x4", "RST_B"), ("x5", "RST_B")])

        if on("rsta"):
            #- RST_A: comparator B's reset, down into the My window
            rsta = P("x3_ccmp", "RST_A")
            rx = int(rsta.centerX())
            wire("RST_A", "M2", rx - 1500, MY(3), rx + 1500,
                 int(rsta.y2))
            stk("RST_A", "M2", "M5", rx, MY(3) + 1500)
            to_logic("RST_A", rx - 1500, MY(3),
                     [("x3", "RST_A"), ("x4", "RST_A")])

        if on("nets"):
            #- net1, net2: the logic's own links. They ran an M2
            #- vertical in the pin's own column before, and the Y pin
            #- column IS the cells' AVSS column -- every cell puts an
            #- M1-M4 cut stack there, so the wire collected AVSS and
            #- everything else that landed on a Y pin (measured).
            link_logic("net1", [("x7", "net1"), ("x3", "net1")])
            link_logic("net2", [("x1", "net2"), ("x4", "net2")])

        def _report_collisions():
            bad = 0
            for i in range(len(drawn)):
                n1, l1, ax1, ay1, ax2, ay2 = drawn[i]
                for j in range(i + 1, len(drawn)):
                    n2, l2, bx1, by1, bx2, by2 = drawn[j]
                    if n1 == n2 or l1 != l2:
                        continue
                    if ax1 < bx2 and bx1 < ax2 and ay1 < by2 and by1 < ay2:
                        log.error(
                            f"ROUTE SHORT {n1} x {n2} on {l1} at "
                            f"({max(ax1, bx1)},{max(ay1, by1)}).."
                            f"({min(ax2, bx2)},{min(ay2, by2)})")
                        bad += 1
            if bad:
                log.error(f"{bad} route collisions")

        if on("misc"):
            #- the block's own pins: PWRUP_1V8 up to the top edge on M4,
            #- OSC_TEMP_1V8 east to the strip edge on M2
            pw1 = P("x6", "PWRUP_1V8")
            pad("PWRUP_1V8", pw1)
            stk("PWRUP_1V8", "M2", "M4", int(pw1.centerX()),
                int(pw1.centerY()))
            ptop = S(4) + 3900
            wire("PWRUP_1V8", "M4", int(pw1.centerX()) - 1500,
                 int(pw1.y1), int(pw1.centerX()) + 1500, ptop)
            pin1 = Rect("M4", int(pw1.centerX()) - 1500, ptop - 4000,
                        3000, 4000)
            pin1.setNet("PWRUP_1V8")
            layout.updatePort("PWRUP_1V8", pin1)
            #- OSC leaves on M3: an M2 run east crosses every net's
            #- M2 column over the strip (measured: it landed on
            #- PWRUP_B)
            osc = P("x5", "OSC_TEMP_1V8")
            pad("OSC_TEMP_1V8", osc)
            ocx, ocy = int(osc.centerX()), int(osc.centerY())
            stk("OSC_TEMP_1V8", "M2", "M3", ocx, ocy)
            dig_x2 = int(layout.getInstanceFromInstanceName("x5").x2)
            wire("OSC_TEMP_1V8", "M3", ocx - 1500, ocy - 1500,
                 dig_x2 + 3000, ocy + 1500)
            pin2 = Rect("M3", dig_x2, ocy - 1500, 3000, 3000)
            pin2.setNet("OSC_TEMP_1V8")
            layout.updatePort("OSC_TEMP_1V8", pin2)

        _report_collisions()
