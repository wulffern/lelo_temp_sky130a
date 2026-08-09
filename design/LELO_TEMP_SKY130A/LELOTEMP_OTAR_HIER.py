"""LELOTEMP_OTAR_HIER: the OTA as eight placed subcells.

The layout hierarchy exists to make routing easy; the schematic stays
flat at the OTA level for readability, and netgen flattens the
difference at LVS. Placement is two rows and a channel; routing is
the channel's business, and every route below aims at a registered
channel rather than a coordinate.

The subcells (REY_ATR assemblies) own nothing above M1, so M2/M3/M4
over the cells is free space -- what collides is never a cell
interior but the routes' own verticals. The ledger that matters:
a net's vertical at a pin lands at the PIN's x, so two nets whose
pins share a column must differ in layer, or in the y-span their
verticals occupy. That is what decides M2 vs M4 below, and which
nets get a straight vertical instead of a channel crossing.
"""


def beforePlace(layout):
    layout.noPowerRoute = True
    layout.place_xspace = [0]
    layout.place_yspace = [0]
    layout.place_groupbreak = [4]


def afterPlace(layout):
    #- 8 um, not 6: the M3 via pads are 8800 tall against a 4000 track
    #- pitch, so usable bands sit 12000 apart. Six crossing nets need
    #- six bands plus the pads' own reach -- 80000 holds them, 60000
    #- did not (measured: every adjacent-band pair shorted through a
    #- pad).
    channel = 8 * layout.um
    rows = [
        ("xn_load_a", "xn_load_b", "xn_mirr", "xr_deg"),
        ("xp_in_a", "xp_in_b", "xp_bias", "xp_sw"),
    ]
    #- Within a row, the cells keep their PUBLISHED relative offsets:
    #- these cells overlap-tile (the drawn guard rings share 4800 of
    #- edge, the pitch is 80000 against an 84800 bounding box), and
    #- the published coordinates are the arrangement DRC has already
    #- accepted. Abutting bounding boxes pulled the rings 4800 apart
    #- and left 51 sliver errors down every seam. Only the rows move.
    y = 0
    row_tops = []
    for row in rows:
        anchor_x, tallest = None, 0
        for nm in row:
            inst = layout.getInstanceFromInstanceName(nm)
            if inst is None:
                continue
            sub = inst.layoutcell
            if anchor_x is None:
                anchor_x = int(sub.x1)
            inst.moveTo(int(sub.x1) - anchor_x, y)
            #- A published subcell keeps the parent's absolute
            #- coordinates; the instance ports already land at
            #- position + relative, but the painted reference is
            #- position + published. xcell = -origin cancels it,
            #- the same way the hier flow places identity.
            inst.xcell = -int(sub.x1)
            inst.ycell = -int(sub.y1)
            tallest = max(tallest, int(inst.height()))
        row_tops.append(y + tallest)
        y += tallest + channel
    layout.updateBoundingRect()

    #- The gap the two rows just opened, and the columns, by name.
    layout.addRoutingChannel("mid", row_tops[0],
                             int(layout.getInstanceFromInstanceName("xp_in_a").y1))
    for short, nm in (("in_a", "xp_in_a"), ("in_b", "xp_in_b"),
                      ("bias", "xp_bias"), ("sw", "xp_sw"),
                      ("res", "xr_deg")):
        inst = layout.getInstanceFromInstanceName(nm)
        if inst is not None:
            layout.addRoutingChannel(short, int(inst.x1), int(inst.x2),
                                     horizontal=False)


def beforeRoute(layout):
    conn = layout.addConnectivityRoute
    ortho = layout.addOrthogonalConnectivityRoute

    #- Every nmos<->pmos net rides a ChannelRoute: one full-width
    #- bar per net on its own mid-channel track, pins dropped onto it
    #- with addRouteConnection, the bar trimmed back to its outermost
    #- drop afterwards. Tracks two apart (8000): the drops' 1x1 via
    #- pads clear the neighbouring bars. Where pins share a column
    #- the drops split by layer (the bias column: VDS M2, VO M4) or
    #- by align (left/center/right on the pin).
    chan = [
        #  net            trk  n-side drops           p-side drops
        ("VDS",           0, [("xr_deg",  "M2", "left")], [("xp_bias", "M2", "center")]),
        ("VD1",           2, [("xn_load_a","M2", "center")], [("xp_in_a", "M2", "right")]),
        ("VO",            4, [("xn_load_b","M2", "center")], [("xp_bias", "M4", "left")]),
        ("VCP",           6, [("xn_mirr", "M2", "left")],    [("xp_bias", "M2", "right"),
                                                             ("xp_sw",   "M2", "center")]),
        ("VD3",           8, [("xn_mirr", "M2", "right")],   [("xp_in_a", "M2", "left"),
                                                             ("xp_in_b", "M2", "left")]),
        ("VD2",          10, [("xn_load_b","M2", "right")],  [("xp_in_b", "M2", "right")]),
        ("VBP",          12, [("xn_load_a","M2", "left")],   [("xp_bias", "M4", "center")]),
        ("VS",           14, [("xr_deg",  "M4", "left")],  [("xp_in_a", "M4", "center"),
                                                             ("xp_in_b", "M4", "center")]),
        ("PWRUP_N_1V8",  16, [("xn_load_a","M4", "left"),
                              ("xn_load_b","M4", "left"),
                              ("xn_mirr", "M4", "left")],    [("xp_bias", "M4", "right")]),
    ]
    for net, trk, ndrops, pdrops in chan:
        layout.addChannelRoute("M3", net, "mid", trk)
        for inst, lay, al in ndrops + pdrops:
            layout.addRouteConnection(net, f"^{inst}$", "t", lay, align=al)
        layout.trimChannelRoute(net)

    #- Supplies as the flat design does them: a VDD ring on top, a
    #- VSS ring on the bottom, each subcell reached by stretching its
    #- supply port straight to the ring. The ports sit on the BULK
    #- geometry at the row boundary (sch2subcells places them there),
    #- so the stretch runs through pure guard column and the pin
    #- layer over the stacks stays free.
    layout.addRouteRing("M1", "VDD_1V8", "t", widthmult=3, spacemult=2)
    layout.addRouteRing("M1", "VSS", "b", widthmult=3, spacemult=2)
    layout.addPowerConnection("VDD_1V8", "", "top")
    layout.addPowerConnection("VSS", "", "bottom")
