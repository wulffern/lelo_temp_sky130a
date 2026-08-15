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

As a SidecarCell each column is a CELL. Its internal nets are routed
by the stack-level maze router, which is space-aware and writes its
conclusions back as `wires`; only the nets that cross between columns
are declared here, as one bar each on its own track of a channel that
belongs to no column. That is the difference: a bar in a channel
cannot land on a pin, because the channel is where there are none.

The placement above is unchanged and was verified flat -- the column
order, every stack order, and the port plan are the same decisions,
now stated as `order` and `rows` instead of as an afterPlace.
"""
import logging

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
        order = ['xn_mirr_load0', 'xg4', 'xg1', 'xn_mirr_load1',
                 'xn_mirr_load2', 'xn_mirr_load3', 'xn_mirr_load4',
                 'xn_mirr_load5']

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
    supplies = [{"net": "VDD_1V8", "ring": "t", "strap": "top",
                 "pin_strap": True},
                {"net": "VSS", "ring": "b", "strap": "bottom",
                 "pin_strap": True}]

    #- Every net with pins in more than one column, one bar each on its
    #- own track of "band" -- the empty strip above the columns, which
    #- afterPlace registers. Drops are DISCOVERED: a subcell that
    #- publishes the net gets one.
    #-
    #- Tracks are two apart, not one. A lane is width+space, 0.6 um,
    #- but a via PAD is 0.88, so neighbouring bars whose drops land
    #- near each other overlap even though the wires do not -- measured
    #- on the flat version, VO1's bar inside VBN1's gate pad.
    #- cuts: 1 on every drop. A two-cut pad is 0.88 um wide and the
    #- drop lanes inside a column are 0.6 apart, so a centred 2x1 pad
    #- overhangs into BOTH neighbours -- measured, VO1's pad
    #- M2 (125800,257300)-(134600,260700) lying across VBN1's drop at
    #- 123300..126300 and PWRUP_N_1V8's at 132900..135900, which merged
    #- all seven crossing nets. The bars were never the problem; they
    #- sit 1.2 um apart on their own tracks and always did.
    routes = [
        {"net": "VBN1", "channel": "band", "track": 0, "cuts": 1},
        {"net": "VO1", "channel": "band", "track": 2, "cuts": 1},
        {"net": "VIP", "channel": "band", "track": 4, "cuts": 1},
        {"net": "VO", "channel": "band", "track": 6, "cuts": 1},
        {"net": "VS", "channel": "band", "track": 8, "cuts": 1},
        {"net": "VBP2", "channel": "band", "track": 10, "cuts": 1},
        {"net": "PWRUP_N_1V8", "channel": "band", "track": 12, "cuts": 1},
    ]

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
