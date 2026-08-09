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

    #- Pins that face each other across the channel: plain verticals,
    #- each pinned to its column's channel so the wire sits on the
    #- narrow bottom pin, not the wide top pin's center.
    conn("M2", "^VD1$", "||", "vchannel=in_a,vtrack=19", 1, "", "^(xn_load_a|xp_in_a)$")
    #- VD2 sits right of its pin center: VD3's 8800-wide via pads at
    #- the in_b pin center reach within 100 of a centered wire.
    conn("M2", "^VD2$", "||", "vchannel=in_b,vtrack=19", 1, "", "^(xn_load_b|xp_in_b)$")
    #- noendcut: the mirr end lands on the pad of VCP's own M4 access
    #- stack below. Its own cut there interleaved two cut arrays 1500
    #- apart on one pin, which mcon spacing does not allow.
    conn("M2", "^VCP$", "||", "vchannel=bias,vtrack=12,noendcut", 1, "", "^(xn_mirr|xp_bias)$")

    #- Channel crossings, one M3 band each, 3 tracks (12000) apart so
    #- an 8800 via pad on one band clears the next band's bar. The
    #- bias column's three wide pins share one centerX, so their
    #- verticals split by layer: VDS keeps M2 (lowest pin), VO takes
    #- M4. VBP and VS take M4 and the two highest bands so their
    #- verticals clear PWRUP_N's and each other's at shared columns.
    ortho("M2", "M3", "^VDS$", "hchannel=mid,htrack=0,vchannel=res,vtrack=13", 1, "", "")
    ortho("M4", "M3", "^VO$", "hchannel=mid,htrack=6,left", 1, "", "")
    #- VCP's switch leg rides M4 with its band below VO's, so neither
    #- crosses the other's pads on M4 at the shared bias column.
    ortho("M4", "M3", "^VCP$", "hchannel=mid,htrack=3,vchannel=sw,vtrack=24", 1, "", "^(xn_mirr|xp_sw)$")
    ortho("M2", "M3", "^VD3$", "hchannel=mid,htrack=9,vchannel=bias,vtrack=19", 1, "", "")
    ortho("M4", "M3", "^VBP$", "hchannel=mid,htrack=12,vchannel=sw,vtrack=0", 1, "", "")
    ortho("M4", "M3", "^VS$", "hchannel=mid,htrack=15,vchannel=res,vtrack=13", 1, "", "")

    #- The powerdown rail: every N-row pin sits directly below another
    #- net's pin in the same column, so it cannot cross the channel at
    #- a pin. The N-row route branches at its own pin levels to a
    #- trunk right of the mirr pin; the bias leg drops on an M3 bar
    #- inside the N row (horizontaltrack13 off the mirr pin) to a
    #- trunk on the SAME bias-channel track, so the two trunks merge.
    ortho("M2", "M3", "^PWRUP_N_1V8$", "vchannel=bias,vtrack=22",
          1, "", "^(xn_load_a|xn_load_b|xn_mirr)$")
    ortho("M2", "M3", "^PWRUP_N_1V8$", "horizontaltrack13,vchannel=bias,vtrack=22",
          1, "", "^(xp_bias|xn_mirr)$")

    #- No drawn supply routes: the guard rings of overlap-tiled
    #- neighbours share 4800 of edge, so VSS is one ring across the N
    #- row and VDD one across the P row already. The port graph cannot
    #- see subcell internals and will report both nets open; LVS,
    #- which extracts the real geometry, is the check that counts.
