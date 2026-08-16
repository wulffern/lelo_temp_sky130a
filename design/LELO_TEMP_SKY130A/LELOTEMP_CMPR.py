"""LELOTEMP_CMPR: the REY_ATR comparator, with the reset switches in.

Same topology as LELOTEMP_CMP, three things different:

  - every device is a REY_ATR cell, so every column is 8.000 x 4.000
    whatever its contact count (expand_row pads the rest with empty
    columns, which is what makes the taps one shape);
  - the input pair is REYATR_LVT_PCH_8C5F0, because a standard pfet
    needs |Vsg| = 0.983 V at 2 uA at -40 C and VC peaks at 0.845 V
    there -- VS would have to sit above the supply;
  - xg1 (RST) and xg4 (powerdown) pull VIP down from inside this
    cell, so CCMPR is only the cap bank and this.

FOUR COLUMNS, NOT FIVE. A REY_ATR column is 8 um against JNW_ATR's
2.56, and the tile gives the ccmp block 41 um of width and 28 um of
unused height (LELO_TEMP.mag: xccmp 20200..28396 in a 21892 tile).
Five columns is 40 um plus the branch gap and does not fit, so the
switch pair goes INTO a stack as a fillGroup -- spending the height
that is free instead of the width that is not.

  five columns                       40.64 x 36.20   too wide
  xg abutted on top of n_mirr_load   38.08 x 45.80   two extra taps
  xg as n_mirr_load's fillGroup      38.08 x 41.00


=====================================================================
WHY THE COLUMNS SIT IN THIS ORDER
=====================================================================

Read from `netlist_info work/xsch/LELOTEMP_CMPR.spice LELOTEMP_CMPR`.
Only five nets have pins in more than one column; everything else is
column local and needs no lane at all:

    net     from            to              what it is
    ------- --------------- --------------- --------------------------
    VBN1    load1,2,3       diff1           the mirrored branch
    VO1     load3,5         diff2           the other branch
    VO      load4,5         tail2           the output
    VBP2    bias2<0..3>     tail1,1<0>,3<*> the pmos bias
    VIP     xg1, xg4        diff2           the input + its two pulls

The column order is what decides how far each of those has to travel,
and it is the only thing that decides it -- a route cannot make a
20 um span short. Weighting each net by the number of columns it
spans, with the nmos group necessarily left of the pmos group:

    load+xg | bias || diff | tail   = 11    <- what this cell had
    bias | load+xg || diff | tail   =  8    <- what it has now
    load+xg | bias || tail | diff   = 12
    bias | load+xg || tail | diff   =  9

VIP is the measurable one. It used to run 10.54 -> 25.05 um, nearly
the whole cell, because xg rode in the FAR column from p_diff; with
load+xg next to the seam its two ends are in adjacent columns. bias
loses nothing by going to the outside: its own net IBP_1U is column
local and its port is on that same left edge, and its one crossing
net VBP2 has a top ring rather than a lane.

The switches stay a fillGroup of n_mirr_load (not of n_mirr_bias):
they belong to the column that touches p_diff, and that is load's
job here because load owns VBN1 and VO1, the other two nets that
cross the seam. xg is ONE group and not two because the group name
is the leading letters of the instance name -- xg_rst and xg_pdn
would have been two groups of one.

=====================================================================
WHY THE STACKS SIT IN THIS ORDER
=====================================================================

`stackorder` reports every column but p_mirr_tail and p_diff
interleaved on D. A drain rail down a column crosses every pin it
passes, so an interleaved column cannot have one -- and that is
placement's business, not routing's. Each `order` below groups the
column on D, because D carries the signal; where D and G disagree the
gate net loses and is given a row channel instead.

  bias   D: IBP_1U IBP_1U | VBP2 x4        G: PWRUP_N | IBP_1U x5
         both contiguous. bias3 is the one device whose gate is not
         IBP_1U, so it goes to the BOTTOM and the tab lane spans the
         rows above it.

  load   D: VSS | VIP VIP | VBN1 VBN1 | VO1 | VO VO
         G: VSS | PWRUP_N | RST | PWRUP_N | VBN1 VBN1 | PWRUP_N | VO1
         D is contiguous, G's PWRUP_N is not, and it cannot be: the
         three PWRUP_N gates sit on three different drain nets and
         each of those three has a second pin elsewhere in the column.
         Chose D. PWRUP_N crosses to bias anyway and gets a trunk lane
         of its own, never a rail on the gate pins.
         load0 is the netlist's own VSS dummy and sits at row 0,
         below every pin span, where a supply bar blocks nothing.
         WHICH END each drain net takes is the port plan, and it is
         not free: VIP and VO are the two nets that leave this cell on
         opposite edges, so they take the two ends of the column. VIP
         at rows 1-2 is one row above the bottom edge, which is where
         LELOTEMP_CCMPR's cap bank hangs off it -- CCMP's model puts
         five MiM caps on exactly this node, and phase 3 puts them
         BELOW the comparator. VO at rows 6-7 is under the top edge.
         Their two port risers then leave in OPPOSITE directions from
         the two ends of the drain lane and cannot meet.
         MEASURED, with VIP at the top instead: VIP's bottom-edge
         riser ran M2 y 0..340400 and VO's top-edge riser M2 y
         97000..398000 in the SAME lane (M2 t42..t46, x 117000..129000
         -- the drain lane), and checkroutes merged eight nets. Nothing
         about the routing was wrong; the column was upside down.

  diff   D: VDD x4 | VBN1 | VO1        G: VDD x4 | VIN | VIP
         the four xp_diff3 dummies are all-VDD devices, so they go to
         the bottom for the same reason load0 does, and the live pair
         lands at rows 4-5, level with load's VBN1 (rows 3-4) and VO1
         (row 5). VIP is the one crossing net that travels -- load
         rows 1-2 to diff row 5 -- which is the price of the bottom
         edge, and it is paid in the seam, on a trunk of its own.

  tail   D: VBP2 VBP2 | VO | VS VS VS   G: PWRUP_1V8 | VBP2 x5
         both contiguous. tail1<0> is the gate-odd device and goes to
         the bottom. VS at rows 3-5 faces p_diff's sources at rows
         4-5. VO's tail pin is at row 2 and its load pins at rows 6-7,
         so its branches cross p_diff ABOVE the top tap, where that
         column is empty -- which is why VO's trunk stands in ctail
         and not in the seam.

The branch gap stays 2 um. It is a gap between an nmos row and a pmos
row, where 2 um is the smallest clean value in the spacing table, and
nothing routes ALONG it -- the crossing nets cross it in row channels
and only need it to be legal, not wide. Widening it spends the width
budget on nothing; the routing budget is in y, where the tile has
28 um free.

=====================================================================
WHY THIS IS A SidecarCell
=====================================================================

It was a classic pycell and the flat connectivity router could not
finish it. Four columns, seven crossing nets and only M2/M3/M4 free
is past what hand-placed lanes can hold: the router draws a shape
without being able to see what is already there, so every fix moved
the collision rather than removing it. Measured, in order: 6 nets
merged, then 5, then 2, then 1, over about twenty builds -- and not
one of the shorts was two wires crossing on a layer. They were via
COLUMNS and rails sitting on foreign pins, which no track map shows.

As a SidecarCell each column is a CELL, and every wire in this file --
inside a column and between them -- is DECLARED. Nothing searches.

That is the change this file most recently carried. A column's own
nets used to be `wires`: the stack-level maze router searched them,
resolved its conclusion to a layer, a shape and an option string, and
wrote a paste-ready block for a person to put back into the class,
guarded by `wires_key`, a fingerprint of the column's placement. The
guard is the problem. Change the placement and the key stops matching;
the block is dropped, the net is searched afresh, and NOTHING SAYS the
design no longer describes the layout. Measured here while converting:
n_mirr_load's key had not matched for some time. Its wires replayed
anyway -- a mismatch condemns only the wires holding a coordinate, and
none of those did -- so the guard warned once and changed nothing. It
was inert in the good case and silent in the bad one.

A `paths` entry names pins and lanes instead. Every anchor in it is
recomputed from the pins on every build, so there is no key, nothing
to go stale, and a placement change MOVES the wire rather than
invalidating it. Demonstrated, not assumed: widening the nmos-pmos
seam by 1 um (`xspace` 2 -> 3) moves p_diff from x 3696 to 3896 and
every route follows, still shorts=0 opens=0, DRC and LVS clean, with
no line of this file touched but the 2.

The placement above is unchanged and was verified flat -- the column
order, every stack order, and the port plan are the same decisions,
now stated as `order` and `rows` instead of as an afterPlace.

THE FOUR SUBCELLS ARE DONE: each is 0 DRC, 0 shorts, 0 opens and
"Circuits match uniquely".

The last short was the GUARD JOG, not the routing. addPowerGuardConnection
centres its jog on the source pin, and REYATR_*_2C1F2's poly contact
column reaches that row -- L=0.22 makes its poly bars 2.2 um where every
other cell's are 9.4 -- so the jog tied xn_mirr_load5's GATE, which is
VO1, to VSS. That is why VO1 was the one port of seven that would not
publish, and why no anchor or layer change ever moved it: the geometry
is inside the placed cell.

The fix lives in cicpy, not here. A cell that needs the offset asks for
it by its name, so every design that instantiates a 1F2 gets it without
having to know. Two earlier explanations for this same bridge were
wrong -- PWRUP_N_1V8's M2 rail, then a supposed defect in the library --
and the second was an accusation made off a single grep that missed
`POB` being the same physical layer as `PO`. Check every alias of a
layer before making a geometry claim about a library.

STATE: clean, on all four checks.

    checkroutes   shorts=0 opens=0 components=47 shapes=3158
    magic drc     0
    klayout drc   OK
    lvs           Circuits match uniquely

The band is gone. Seven crossing nets used to ride one ChannelRoute
each on a "band" above the columns, and the bars were never the
problem -- own tracks, 1.2 um apart -- the DROPS were. Every net whose
pins sit on one terminal of a column publishes its port at the same x,
so VIP (rows 1-2) and VO (rows 6-7) both dropped in n_mirr_load's
drain lane and VIP's drop had to pass VO's rows to reach the band:

    VIP  M2 (120100,139000)-(123100,410000)
    VO   M2 (120100,299000)-(123100,422000)

the same lane, overlapping over 11 um, which no cut size reaches. The
crossing nets are stories now (see CROSSINGS below): each leaves its
own pin, rides its own column and crosses on a row that is named as an
anchor, so no two of them share a lane by construction rather than by
luck.

WHERE THE DRC USED TO BE, kept because the arithmetic is the method:
build with the top's routes empty and subtract.

    LELOTEMP_CMPR_N_MIRR_BIAS      0
    LELOTEMP_CMPR_P_DIFF           0
    LELOTEMP_CMPR_P_MIRR_TAIL      0
    LELOTEMP_CMPR_N_MIRR_LOAD     12   met1.2, mcon.2
    the top, routes = []          12   so the tiling, the rings and
                                       the guard connections add NONE
    the top, routes as declared   31   the band added 19

Both numbers are 0 today. n_mirr_load's own 12 were two rails on one
terminal 0.12 um apart -- the search had given VIP and VO the same
anchor -- and they are on opposite sides of the pin now.
"""
import logging
import re

from cicpy.core.path import (PITCH, SPACE, left_of_pins, pin,
                             right_of_pins, tab_lane, track)
from cicpy.sidecar import SidecarCell, Stack

log = logging.getLogger("LELOTEMP_CMPR")


class LELOTEMP_CMPR(SidecarCell):

    place = {"groupbreak": 5, "channel": 6}

    class n_mirr_bias(Stack):
        """D: IBP_1U IBP_1U | VBP2 x4     G: PWRUP_N | IBP_1U x5

        bias3 is the one device whose gate is not IBP_1U, so it goes
        to the BOTTOM and the tab lane spans the rows above it.
        """
        match = r'^(xn_mirr_bias\d+(<\d+>)?|xstack_n_mirr_bias_(top|bot)|xfill_n_mirr_bias_\d+)$'
        group = "nmos"
        channel = "cbias"
        order = ['xn_mirr_bias3', 'xn_mirr_bias1', r'xn_mirr_bias2<\d+>']

        #- VSS BLOCKED. The search drew it as an M2 rail at
        #- trunkx=-800, outside the cell -- an unnecessary second path
        #- to a node addPowerGuardConnection has already tied to the
        #- guard column beside every source, on M1, with the tap cells
        #- carrying it up, down and across.
        #-
        #- `blocked` and not a wires triple: this half of a wires block
        #- never held geometry, so it needs no fingerprint to guard and
        #- nothing in it can go stale.
        blocked = [
            ('VSS', 'the supply reaches the guard on M1; a stack does '
                    'not need an M2 rail for it, and the search only '
                    'drew one because it was asked to route every net'),
        ]

        #- VBP2: the four bias2 drains, one M1 rail on their right edge.
        #-
        #- WAS ('VBP2', 'M1', '||', 'trunkright') plus a wires_key. The
        #- rail is the same rail; what is gone is the fingerprint. The
        #- pins are COLLECTED rather than named, so `order` can be
        #- rewritten and bias2 can grow a fifth device without touching
        #- this line -- where the key would have stopped matching and
        #- the block would have been discarded in silence.
        paths = [
            dict(net="VBP2", layer="M1",
                 steps=[("trunk", right_of_pins())]),
        ]

    class n_mirr_load(Stack):
        """D: VSS | VIP VIP | VBN1 VBN1 | VO1 | VO VO

        The switches ride here as part of the column, not as a stack
        of their own: two stacks abutted vertically each bring their
        own TAPBOT and TAPTOP and the pair went over the tile.

        VIP takes rows 1-2 and VO rows 6-7 because they are the two
        nets that leave on opposite edges -- VIP down to CCMPR's cap
        bank, VO up -- so their port risers leave the shared drain
        lane in opposite directions. With VIP at the top instead, the
        two risers ran M2 y 0..340400 and y 97000..398000 in the same
        lane and eight nets merged.
        """
        match = r'^(xn_mirr_load\d+|xg\d+|xstack_n_mirr_load_(top|bot)|xfill_n_mirr_load_\d+)$'
        group = "nmos"
        channel = "cload"
        #- xn_mirr_load5 BEFORE xn_mirr_load4, so VO1's two pins are
        #- on ADJACENT rows. VO1 is the awkward net here: its pins are
        #- on different terminals -- load3's drain (a wide M1 bar) and
        #- load5's gate (a narrow tab 0.9 um to the right of it) -- and
        #- with load4 between them any vertical joining the two had to
        #- cross a whole row of VO's drain bar and PWRUP_N_1V8's tab
        #- rail on the way. Swapping load4 and load5 costs nothing:
        #- both carry VO on the drain, so the column's drain order is
        #- untouched.
        order = ['xn_mirr_load0', 'xg4', 'xg1', 'xn_mirr_load1',
                 'xn_mirr_load2', 'xn_mirr_load3', 'xn_mirr_load5',
                 'xn_mirr_load4']

        #- VSS BLOCKED, not routed. The search drew it as a rail at
        #- trunkx=-800 -- a coordinate outside the cell -- and it landed
        #- on the bottom tap row's own M1 at y=4.5, which was 6 of the
        #- 12 errors this column used to carry. The supply does not need
        #- it: addPowerGuardConnection ties every source to the guard
        #- column beside it and the tap cells carry it.
        blocked = [
            ('VSS', 'supplies go to the guard, not to a rail in the '
                    'stack'),
        ]

        #- WHAT THE wires BLOCK USED TO SAY, and what replaced it. The
        #- old block was router output, hand-edited twice: the search
        #- had given VIP and VO the SAME anchor, two rails on one
        #- terminal 0.12 um apart, which was 12 met1.2/mcon.2 errors and
        #- the only dirty subcell in the cell.
        #-
        #- MEASURED WHILE CONVERTING: its `wires_key` (68e8d342a26b) had
        #- not matched the placement (f01a10fc0963) for some time, and
        #- every wire in it replayed anyway -- a mismatch condemns only
        #- the wires that carry a coordinate, and none of these did. So
        #- the guard fired, warned once in a 200-line log, and changed
        #- nothing. That is the good case. The bad one is a block that
        #- DOES carry a coordinate: it is dropped, the net is searched
        #- afresh, and nothing says the design no longer describes the
        #- layout. A path has no key, because it has nothing to guard:
        #- every anchor in it is recomputed from the pins each run.
        #-
        #- VIP and VO: rows 1-2's and rows 6-7's drains, one M1 rail
        #- each on their right edge. trunkright is the RIGHT EDGE of
        #- each net's own pins -- x 46600..49600 -- and that is the only
        #- M1-safe vertical window in this library: the drain bar spans
        #- 33600..49600 and the source bar 27200..43200, so a rail
        #- anywhere in 33600..43200 crosses both, and only 43200..49600
        #- is drain-only. Both nets take it and they do not meet,
        #- because a trunk spans its OWN pins and their y spans are
        #- disjoint.
        paths = [
            dict(net="VIP", layer="M1",
                 steps=[("trunk", right_of_pins())]),
            dict(net="VO", layer="M1",
                 steps=[("trunk", right_of_pins())]),

            #- PWRUP_N_1V8: a FLYOVER, and the two steps say so.
            #-
            #- Its three gates sit on non-adjacent rows, so its rail
            #- spans the whole column on the gate-tab lane -- and in
            #- the full-hierarchy view that lane is the busiest in the
            #- cell: every REYATR cell puts its own M1 gate tab at
            #- x 52800..56000. On M2 the rail ran right above that
            #- column and every other net that has to land on a tab
            #- shorted to it. On M4 it flies over and `taps` brings it
            #- down at its own three pins and nowhere else.
            #-
            #- M4 and not M3, still: M3 is the layer the PARENT crosses
            #- on, and four of the seven crossing nets pass through
            #- this column. Lowest is a rule about the cell, not about
            #- the design.
            dict(net="PWRUP_N_1V8", layer="M4",
                 steps=[("trunk", tab_lane()), ("taps",)]),

            #- VO1: the one net in this column with NO common lane.
            #- Its two pins are on different terminals of adjacent
            #- rows -- xn_mirr_load3's drain, a 1.6 um M1 bar, and
            #- xn_mirr_load5's gate, a 0.32 um tab 0.9 um to its right
            #- -- so trunkright and trunkleft are both undefined and
            #- the search fell back to a raw coordinate. It was carried
            #- as a channel (`vchannel=vo1lane,vtrack=6`) with the
            #- channel itself registered by hand in beforeRoute off
            #- load3's drain rect, which is thirteen lines of hook to
            #- say "a lane near that pin".
            #-
            #- As a story there is no lane to name at all. The two pins
            #- ARE the specification: leave the drain by its east edge,
            #- which is the side the tab is on, hop to M2, and cross to
            #- the tab's own column. Nothing here is a coordinate and
            #- nothing depends on the row order.
            dict(net="VO1", at="e",
                 start=("xn_mirr_load3", "VO1"),
                 stop=("xn_mirr_load5", "VO1"),
                 steps=[("up",),
                        ("movex", pin("xn_mirr_load5", "VO1", "x")),
                        ("end",)]),
        ]

        def beforeRoute(self, entry):
            """Strap the netlist's OWN supply devices.

            routeSupplyDevices defaults to the layout-generated
            xfill_* and this schematic carries its fills explicitly,
            so they are named like any other instance and the default
            misses them -- their D/G/S is left floating against the
            guard. Measured: VDD_1V8 split into 2 components here and
            VSS into 8 in n_mirr_load, and these were the only two of
            the four columns that failed LVS.

            Done here and not in cicpy's default on purpose: adding
            these instances to the default took LELOTEMP_CMP from 0
            opens to 2, so it is not a safe change to a shared
            library. The call already accepts the instances; nothing
            was passing them.
            """
            self.routeSupplyDevices(instances=[
                i for i in self.instances
                if re.fullmatch(r"xn_mirr_load0", getattr(i, "instanceName", "") or "")])
            #- WHAT IS NO LONGER HERE: thirteen lines that walked the
            #- instances to find xn_mirr_load3's VO1 rect and registered
            #- a routing channel across it, so that VO1's wire had a
            #- lane to name. VO1's path names the two pins instead, so
            #- there is no lane to register and no hook to hold it.
            return None


    class p_diff(Stack):
        """D: VDD x4 | VBN1 | VO1        G: VDD x4 | VIN | VIP

        The four xp_diff3 dummies are all-VDD devices and go to the
        bottom, so the live pair lands at rows 4-5, level with
        n_mirr_load's VBN1 and VO1.
        """
        match = r'^(xp_diff\d+(<\d+>)?|xstack_p_diff_(top|bot)|xfill_p_diff_\d+)$'
        group = "pmos"
        channel = "cdiff"
        #- 2 um on its LEFT: this is the nmos-to-pmos seam, and 2 um is
        #- the smallest clean value in the spacing table.
        xspace = 2
        order = [r'xp_diff3<\d+>', 'xp_diff1', 'xp_diff2']

        #- VS: the pair's two sources, one M1 rail on their LEFT edge --
        #- the side facing p_mirr_tail's own VS rail across the seam.
        #-
        #- This is the net that was never in the file. It searched on
        #- every build and its conclusion was written to
        #- LELOTEMP_CMPR.routes.py for someone to paste back; declared,
        #- the search does not run and there is nothing to paste.
        paths = [
            dict(net="VS", layer="M1",
                 steps=[("trunk", left_of_pins())]),
        ]

        def beforeRoute(self, entry):
            """Strap the netlist's OWN supply devices.

            routeSupplyDevices defaults to the layout-generated
            xfill_* and this schematic carries its fills explicitly,
            so they are named like any other instance and the default
            misses them -- their D/G/S is left floating against the
            guard. Measured: VDD_1V8 split into 2 components here and
            VSS into 8 in n_mirr_load, and these were the only two of
            the four columns that failed LVS.

            Done here and not in cicpy's default on purpose: adding
            these instances to the default took LELOTEMP_CMP from 0
            opens to 2, so it is not a safe change to a shared
            library. The call already accepts the instances; nothing
            was passing them.
            """
            self.routeSupplyDevices(instances=[
                i for i in self.instances
                if re.fullmatch(r"xp_diff3<\d+>", getattr(i, "instanceName", "") or "")])
            return None


    class p_mirr_tail(Stack):
        """D: VBP2 VBP2 | VS VS VS | VO   G: PWRUP_1V8 | VBP2 x5

        tail1<0> is the gate-odd device (PWRUP_1V8) and goes to the
        bottom. tail2 is at the TOP so VO's tail pin is level with its
        n_mirr_load pins at rows 6-7, and its bar crosses p_diff above
        that column's top tap, where p_diff is empty.
        """
        match = r'^(xp_mirr_tail\d+(<\d+>)?|xstack_p_mirr_tail_(top|bot)|xfill_p_mirr_tail_\d+)$'
        group = "pmos"
        channel = "ctail"
        order = ['xp_mirr_tail1<0>', 'xp_mirr_tail1', r'xp_mirr_tail3<\d+>',
                 'xp_mirr_tail2']

        #- VDD_1V8 BLOCKED, same reason as VSS in n_mirr_bias.
        blocked = [
            ('VDD_1V8', 'the supply reaches the guard on M1; a stack '
                        'does not need an M2 rail for it, and the '
                        'search only drew one because it was asked to '
                        'route every net'),
        ]

        #- VS: the three tail3 sources, one M1 rail on their right edge,
        #- facing p_diff's sources across the seam.
        paths = [
            dict(net="VS", layer="M1",
                 steps=[("trunk", right_of_pins())]),
        ]

    #- ONE row: the four columns side by side, in the order the
    #- netlist asked for (see WHY THE COLUMNS SIT IN THIS ORDER).
    rows = [[n_mirr_bias, n_mirr_load, p_diff, p_mirr_tail]]

    #- pin_strap: the top is an ASSEMBLY, so its ring reaches the four
    #- columns through their PUBLISHED supply rects, and that is
    #- addPowerConnection, which is opt-in because it stretches each
    #- rect to the ring on that rect's own layer. Here the published
    #- rects are the columns' own guard rings, already at the cell's
    #- top and bottom edges, so the stretch is a via and not a wire
    #- across the block -- which is exactly the case the opt-in is for.
    #- NOT STRAPPED, though the ring is locali at ~12.8 ohm/sq and a
    #- 38 um side is ~42 squares. Strapping was measured (met1 over
    #- each ring, stitched full length): this cell verifies clean, and
    #- the PARENT breaks -- LELOTEMP_CCMPR's VC descends through this
    #- cell's bottom edge on M2, and the strap is a full-length M2 bar
    #- across that edge. A via stack's intermediate metal is
    #- continuous, so an M3 strap blocks the same crossings through
    #- its M2 enclosure. A subcell's ring can only be strapped by
    #- something that can see every crossing its parent makes -- see
    #- the supply-impedance notes on the top cell.
    supplies = [{"net": "VDD_1V8", "ring": "t", "strap": "top",
                 "pin_strap": True},
                {"net": "VSS", "ring": "b", "strap": "bottom",
                 "pin_strap": True}]

    #- NO TOP ROUTES YET. Deliberately empty: the four subcells verify
    #- on their own and the tiling, the rings and the guard connections
    #- add nothing, so this is the clean baseline every route is
    #- measured against. They go back one at a time, shortest first,
    #- written as PATHS -- one route, then check for shorts.
    #-
    #- What was here before: seven ChannelRoute bars on a "band" above
    #- the columns. The bars were never the problem -- own tracks,
    #- 1.2 um apart -- the DROPS were: every net whose pins sit on one
    #- terminal of a column publishes at the same x, so two nets drop
    #- in one lane and a 0.88 um via pad on a 0.6 um lane overhangs
    #- both neighbours. Cut size did not reach it, because the overlap
    #- is two nets sharing a lane end to end.
    routes = []

    #- ------------------------------------------------------------
    #- THE CROSSING NETS, ONE AT A TIME, SHORTEST FIRST.
    #-
    #- Every one has exactly two pins, one per subcell, so each is a
    #- single story rather than a bar with drops. Spans, measured off
    #- the placement:
    #-
    #-     PWRUP_N_1V8   12.72 um   bias  -> load
    #-     VBN1          12.96      load  -> diff
    #-     VO1           15.44      load  -> diff
    #-     VS            18.00      diff  -> tail
    #-     VIP           26.00      load  -> diff
    #-     VO            28.00      load  -> tail
    #-     VBP2          32.64      bias  -> tail
    #-
    #- Added in that order, one build and one short check each.
    #- (net, from, to, cut options). THE CUT SHAPE FOLLOWS THE PIN and
    #- cannot be one setting for the cell: a gate TAB is 0.32 um across
    #- and takes one cut wide and two tall, a drain BAR is 2.24 um and
    #- takes the opposite. Measured both ways round -- two cuts side by
    #- side on PWRUP_N_1V8's tab reached 2.2 um past it (li.3, li.c2),
    #- and two cuts tall on VBN1's bar overhung it in y for four more.
    #- "" lets cicpy fit the largest cut that fits, which is right
    #- whenever the pin is not the odd shape.
    #- (net, from, to, cuts, vertical layer, crossing layer, leg order)
    #-
    #- Each crossing net has exactly two pins, one per subcell, so each
    #- is one story: up out of the pin, along the column to the target
    #- row, across, down onto the other pin.
    #-
    #- THE TWO LAYERS ARE THE WHOLE DESIGN. A vertical leg rides the
    #- source column and a horizontal leg crosses the cell, and each
    #- has to be on a layer that is free where it runs:
    #-   M2 vertical   fine unless the column's shared terminal lane
    #-                 already carries another net's landings
    #-   M3 crossing   fine unless a subcell owns M3 down that column,
    #-                 or another net has landed at that y
    #-   M4/M5         empty in this cell, for the net that cannot use
    #-                 the cheap pair
    #-
    #- The cut shape follows the PIN and cannot be one setting: a gate
    #- tab is 0.32 um across and takes one cut wide and two tall, a
    #- drain bar is 2.24 um and takes the opposite. "" lets cicpy fit
    #- the largest that fits, which is right for every ordinary pin.
    #- (net, from, to, cuts, vertical layer, crossing layer,
    #-  which subcell's row to cross on, offset in PITCHes)
    #-
    #- Each crossing net has two pins, one per subcell, so each is one
    #- story: up out of the pin, along the source column to the
    #- crossing row, across, back to the target row, down onto the
    #- other pin.
    #-
    #- THE CROSSING ROW IS THE LEVER, not the layer. Everything a
    #- crossing leg can hit is a via STACK, and a stack is one pin
    #- wide -- so a row that clears it is usually a pitch or two away,
    #- and going up a layer to dodge it spends a whole plane on a 0.6
    #- um problem. The row is named as an anchor (whose pin, plus n
    #- lanes) so it stays a statement about the design.
    #-
    #- The cut shape follows the PIN: a gate tab is 0.32 um across and
    #- takes one cut wide and two tall, a drain bar is 2.24 um and
    #- takes the opposite. "" lets cicpy fit the largest that fits.
    CROSSINGS = [
        ("PWRUP_N_1V8", "xn_mirr_bias", "xn_mirr_load", "1cuts,2vcuts",
         "M2", "M3", "xn_mirr_load", 0),
        ("VBN1", "xn_mirr_load", "xp_diff", "", "M2", "M3", "xp_diff", 0),
        ("VO1", "xn_mirr_load", "xp_diff", "", "M2", "M3", "xp_diff", 0),
        ("VS", "xp_diff", "xp_mirr_tail", "", "M2", "M3", "xp_mirr_tail", 0),
        #- VIP crosses ONE LANE ABOVE p_diff's pin row: on the row
        #- itself its M3 leg (261500..264500) sat 0.1 um from VO1's
        #- (257500..260500), which met2.2 wants 0.14 apart. Its
        #- vertical stays on M4 -- on M2 it would ride n_mirr_load's
        #- drain lane through VBN1's and VO1's landings.
        ("VIP", "xn_mirr_load", "xp_diff", "1cuts,2vcuts",
         "M4", "M3", "xp_diff", 1),
        #- VO crosses ONE LANE ABOVE its own source row. That row is
        #- n_mirr_load's top, and n_mirr_load's PWRUP_N_1V8 rail lands
        #- on the gate there through an M1-M4 via stack -- so VO's M3
        #- leg sat 0.1 um from the stack's M3 pad. One lane up is above
        #- the rail's top (343000) and clear. It crosses at the SOURCE
        #- row rather than the target because both pmos columns have
        #- already ended by then (303000), so it passes over empty
        #- cell instead of through p_diff.
        ("VO", "xn_mirr_load", "xp_mirr_tail", "", "M2", "M3",
         "xn_mirr_load", 3),
        #- VBP2 crosses ONE LANE BELOW p_mirr_tail's pin row. On the
        #- row itself its leg ran through PWRUP_N_1V8's via stack in
        #- n_mirr_bias (M3 (57500,98600)-(60900,107400)); a lane down
        #- is under the stack and clear of everything else, and costs
        #- one jog instead of a whole plane.
        ("VBP2", "xn_mirr_bias", "xp_mirr_tail", "", "M2", "M3",
         "xp_mirr_tail", -1),
    ]

    _UPS = {"M2": 1, "M3": 2, "M4": 3, "M5": 4}

    @staticmethod
    def _pin(layout, instname, net):
        """A subcell's published port rect, in the parent's frame."""
        for inst in layout.iterInstances():
            if getattr(inst, "instanceName", "") != instname:
                continue
            for ch in getattr(inst, "children", []):
                if getattr(ch, "name", "") == net and hasattr(ch, "get"):
                    r = ch.get()
                    if r is not None:
                        return r
        log.warning(f"{net}: no published pin on {instname}")
        return None

    def beforeRoute(self, layout):
        super().beforeRoute(layout)
        for (net, a_inst, b_inst, cuts, vlayer, xlayer,
             row_inst, detour) in self.CROSSINGS:
            a = self._pin(layout, a_inst, net)
            b = self._pin(layout, b_inst, net)
            if a is None or b is None:
                continue
            v, x = self._UPS[vlayer], self._UPS[xlayer]
            q = layout.path(net, "M1", start=[a], stop=[b], options=cuts)
            q.start()
            for _ in range(v):
                q.up()
            row = q.pin(row_inst, net, "y")
            if detour:
                row = row + detour * q.PITCH
            q.movey(row)
            #- to the crossing layer, which may be BELOW the vertical
            #- one: VIP climbs on M4 to clear a shared drain lane and
            #- then crosses on M3. `range(x - v)` silently did nothing
            #- when that difference was negative, so VIP crossed on M4
            #- and ran the length of n_mirr_load's own M4 rail.
            step = q.up if x > v else q.down
            back = q.down if x > v else q.up
            for _ in range(abs(x - v)):
                step()
            q.movex(q.landing("x"))
            for _ in range(abs(x - v)):
                back()
            q.movey(q.landing("y"))
            for _ in range(v):
                q.down()
            q.end()

    def afterPlace(self, layout):
        """Register "band", the strip the crossing nets route in.

        The recipe registers a channel between two ROWS, and this
        floorplan has one row, so there is no "mid" to aim at. The
        space is there anyway and it is the reason the columns are
        laid out this way: the tile gives this block 28 um of height it
        does not use, so the bars go ABOVE the columns rather than
        between the pins.

        Measured off the placement, never written as a coordinate.
        """
        super().afterPlace(layout)
        tops = [i for i in layout.iterInstances()]
        if not tops:
            return
        y = max(int(i.y2) for i in tops)
        layout.addRoutingChannel("band", y, y + 14 * 6000)
