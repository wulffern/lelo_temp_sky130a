"""LELOTEMP_OTAR_HIER: the OTA as eight placed subcells.

The layout hierarchy exists to make routing easy; the schematic stays
flat at the OTA level for readability, and netgen flattens the
difference at LVS. Placement is the whole file: two rows and a
channel.
"""

def beforePlace(layout):
    layout.noPowerRoute = True
    layout.place_xspace = [0]
    layout.place_yspace = [0]
    layout.place_groupbreak = [4]


def afterPlace(layout):
    channel = 6 * layout.um
    rows = [
        ("xn_load_a", "xn_load_b", "xn_mirr", "xr_deg"),
        ("xp_in_a", "xp_in_b", "xp_bias", "xp_sw"),
    ]
    y = 0
    for row in rows:
        x, tallest = 0, 0
        for nm in row:
            inst = layout.getInstanceFromInstanceName(nm)
            if inst is None:
                continue
            inst.moveTo(x, y)
            x += int(inst.width())
            tallest = max(tallest, int(inst.height()))
        y += tallest + channel
    layout.updateBoundingRect()
