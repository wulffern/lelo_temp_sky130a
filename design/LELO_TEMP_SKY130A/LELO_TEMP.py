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
        match = r'^x[1-7]$'
        group = "dig"
        fill = False
        xspace = 4
        order = ['x7', 'x3', 'x4', 'x1', 'x5', 'x2', 'x6']

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
        #- the move leaves every group's stored extent where base
        #- place scattered it, and the ring wraps THAT box: refresh
        for grp in layout.cellgroups:
            grp.updateBoundingRect()
        layout.updateBoundingRect()

    def beforeRoute(self, layout):
        layout.addRouteRing("M1", "VDD_1V8", "t", widthmult=3,
                            spacemult=2)
        layout.addRouteRing("M1", "VSS", "b", widthmult=3, spacemult=2)
        layout.addPowerConnection("VDD_1V8", "", "top")
        layout.addPowerConnection("VSS", "", "bottom")
        super().beforeRoute(layout)
