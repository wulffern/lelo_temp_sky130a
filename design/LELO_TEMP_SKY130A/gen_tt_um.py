#!/usr/bin/env python3
"""tt_um_lelo_temp_wulffern.mag, generated -- never drawn by hand.

The TinyTapeout wrapper for LELO_TEMP. Everything here is derived:

* THE PORT ROW COMES FROM THE DEF. tt_block_1x1_pg.def is the
  authority on where every pin sits (PLACED x, LAYER met4); the
  tt_block_1x1_pg.mag template beside it is MIRRORED against it --
  ena leftmost where the DEF has it rightmost -- and gr01..gr04 each
  hand-corrected their copy. Generating from the DEF removes the
  copy step that flipped it.

* THE TILE IS THE CORE, ALMOST. LELO_TEMP was designed to the TT
  tile (154.52 x 110.95 um in 161 x 111.52) and carries its own
  digital strip, so the wrapper adds only: two power rails with a
  via stack each, two signal routes, an antenna diode on the input,
  and the uio_oe tie-low bus through res_generic_m4 bodies (the
  resistor keeps uio_oe and VGND separate nets for LVS, exactly as
  the gr0x tiles do).

* THE ROUTES RUN WHERE THE CORE IS EMPTY BY MEASUREMENT: the top
  band above y 109.3 um (nothing but the M1 ring since the cband
  retune), the east margin (x > 154.52), the strip's west sliver
  and the slot between its supply columns.

Units are magic internal at magscale 1 2 = 5 nm; um * 200.
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
DEF = os.path.join(HERE, "tt_block_1x1_pg.def")
OUT = os.path.join(HERE, "tt_um_lelo_temp_wulffern.mag")

U = 200          # units per um
TOP = 22304      # tile top, 111.52 um
PADW = 60        # port pad 0.3 um wide
PADY0, PADY1 = 22104, TOP

layers = {k: [] for k in
          ("locali", "viali", "metal1", "via1", "metal2", "via2",
           "metal3", "via3", "metal4", "rmetal4")}
uses, labels = [], []


def rect(layer, x1, y1, x2, y2):
    layers[layer].append((int(x1), int(y1), int(x2), int(y2)))


def stack(x, y, top_l, bot_l, pad=50):
    """A via stack centred on (x, y), from top_l down to bot_l.

    Generous 0.5 um pads and single centred cuts: every sky130
    enclosure rule is <= 0.09 um, so nothing here is marginal.
    """
    #- magic CONTACT PAINT includes the enclosure: the drawn via rect
    #- must be cut + 2*enc (via.1a 0.26, via2.1a 0.28, via3.1 0.32 um)
    #- -- drawn at the cut size alone, magic reported all four as
    #- underwidth. 0.35 um paint with 0.55 um metal pads clears every
    #- width and enclosure rule at once.
    order = ["locali", "metal1", "metal2", "metal3", "metal4"]
    cuts = {("metal1", "locali"): "viali", ("metal2", "metal1"): "via1",
            ("metal3", "metal2"): "via2", ("metal4", "metal3"): "via3"}
    hi, lo = order.index(top_l), order.index(bot_l)
    pad = max(pad, 55)
    for i in range(lo, hi + 1):
        rect(order[i], x - pad, y - pad, x + pad, y + pad)
    for i in range(lo, hi):
        rect(cuts[(order[i + 1], order[i])], x - 35, y - 35, x + 35, y + 35)


#- ------------------------------------------------------------------
#- the 43 signal ports, from the DEF
#- ------------------------------------------------------------------
pins = []
for m in re.finditer(r"-\s+(\S+)\s+\+ NET \S+ \+ DIRECTION (\w+).*?"
                     r"PLACED \( (\d+) (\d+) \)", open(DEF).read(), re.S):
    name, direction, x_nm = m.group(1), m.group(2).lower(), int(m.group(3))
    pins.append((name, direction, x_nm // 5))
assert len(pins) == 43, f"DEF gave {len(pins)} pins"
#- PORT NUMBERS IN THE SCHEMATIC'S ORDER, not the DEF's. Magic writes
#- the extracted .subckt ports by port number, and netgen resolves a
#- symmetric orbit -- the eight identical tie resistors, or the two
#- fanout-1 supply/output pins -- POSITIONALLY within the orbit, not
#- by name. With DEF-ordered numbers every orbit came out permuted
#- and the top failed pin matching; gr01's apparently random numbers
#- are its schematic's order, and that is why it passes.
SCH_ORDER = ([f"uio_oe[{i}]" for i in range(7, -1, -1)]
             + ["VDPWR", "VGND"]
             + [f"ui_in[{i}]" for i in range(7, -1, -1)]
             + [f"uio_in[{i}]" for i in range(7, -1, -1)]
             + ["ena", "rst_n", "clk"]
             + [f"uo_out[{i}]" for i in range(7, -1, -1)]
             + [f"uio_out[{i}]" for i in range(7, -1, -1)])
NUM = {nm: i for i, nm in enumerate(SCH_ORDER)}
for name, direction, xc in pins:
    rect("metal4", xc - PADW // 2, PADY0, xc + PADW // 2, PADY1)
    labels.append(f"flabel metal4 s {xc - PADW // 2} {PADY0} "
                  f"{xc + PADW // 2} {PADY1} 0 FreeSans 480 90 0 0 {name}\n"
                  f"port {NUM[name]} nsew signal {direction}")
n = 45

#- power rails, full height at the west edge -- gr01's proven geometry
rect("metal4", 0, 0, 400, TOP)
rect("metal4", 480, 0, 880, TOP)
labels.append(f"flabel metal4 0 0 400 {TOP} 1 FreeSans 800 0 0 0 VDPWR\n"
              f"port {NUM['VDPWR']} nsew power bidirectional")
labels.append(f"flabel metal4 480 0 880 {TOP} 1 FreeSans 800 0 0 0 VGND\n"
              f"port {NUM['VGND']} nsew ground bidirectional")

#- ------------------------------------------------------------------
#- the core, at the origin: the rails overlay only its M1 ring
#- ------------------------------------------------------------------
uses.append(("LELO_TEMP", "LELO_TEMP_0", "", 1, 0, 0, 0, 1, 0,
             0, 0, 30904, 22200))

#- power: each rail lands on its ring as a WIDE stack -- metal pads
#- over the whole rail-to-ring overlap with contact PAINT, which
#- magic fractures into every cut the rules admit. A single-cut
#- stack here was ~20 ohm in series (mcon 9.3 + via1 4.5 + via2 3.4
#- + via3 3.4) feeding the whole tile; paint the size of the overlap
#- is dozens of cuts per level. The met1 pad lands on the ring's own
#- met1 strap, whose full-length viali paint carries into the locali
#- ring -- so the stack stops at met1 and the worst resistor in the
#- chain (a lone mcon) is not in it at all.
def power_pad(x1, y1, x2, y2):
    for lay in ("metal1", "metal2", "metal3", "metal4"):
        rect(lay, x1, y1, x2, y2)
    for cut in ("via1", "via2", "via3"):
        rect(cut, x1 + 20, y1 + 20, x2 - 20, y2 - 20)

#- ON THE RING ROWS -- not the blocks' own supply bars. The first
#- version landed at the bars (y 107.4 / 1.95 um), which the old
#- single stacks reached because they drilled to locali; a stack
#- that stops at met1 must stand where the met1 STRAP is, and that
#- is the ring rows themselves (measured: on the bars, VGND came
#- out split, with the core's VSS on the substrate node).
power_pad(30, 21727, 370, 21877)     # VDPWR rail onto the VDD ring row
power_pad(510, 15, 850, 165)         # VGND rail onto the VSS ring row

#- ------------------------------------------------------------------
#- ui_in[0] -> PWRUP_1V8, all metal4
#- ------------------------------------------------------------------
XC = {name: xc for name, _d, xc in pins}
ui = XC["ui_in[0]"]
rect("metal4", ui - 30, 21984, ui + 30, PADY0)          # drop
rect("metal4", ui - 30, 21984, 32030, 22044)            # top row
#- AND UNDER EVERYTHING TO THE PAD, from below. Two drops at the
#- pad column were measured and both shorted: at 145.0 the met4
#- landing bars of RST_A, CMPO_A and CMPO_B (they span to 146.21);
#- at 147.0 the strip's own met4 crossing stubs (x7/Y, x4/B) and
#- RST_B's landing bar. Every lane ABOVE the pad crosses somebody.
#- Below it is the tile floor: y 0.55..0.85 um runs under the ring
#- (M1), under RST_B's floor (met2), under CMPO_A's (met3), and
#- RST_B's margin riser starts at y 1.2 -- 0.35 clear. The pad is
#- then entered through its own bottom edge, the one side nothing
#- else uses.
rect("metal4", 31970, 110, 32030, 22044)                # east margin lane
rect("metal4", 29184, 110, 32030, 170)                  # floor row, y 0.7 um
rect("metal4", 29184, 110, 29244, 690)                  # up into PWRUP's bottom

#- the antenna diode, tapped off ui's OWN margin lane. It sat at
#- x 158.5 -- which the lane swap made the uo met3 lane -- and the
#- tap's met3 pad landed on that instead: the diode extracted onto
#- uo_out[0], found only when the wrapper check was stripped to 17
#- lines. 159.75 overlaps the ui met4 lane and clears the uo lane by
#- 0.8 um and the tile edge by 0.4.
uses.append(("sky130_fd_pr__diode_pw2nd_05v5_lc", "ant_pwrup", "",
             1, 0, 31950, 0, 1, 6000, -183, -183, 183, 183))
stack(31950, 6000, "metal4", "metal1")

#- ------------------------------------------------------------------
#- OSC_TEMP_1V8 -> uo_out[0]: metal3 rows so nothing crosses ui's
#- metal4, metal4 only at the two pads
#- ------------------------------------------------------------------
uo = XC["uo_out[0]"]
rect("metal4", uo - 30, 21964, uo + 30, PADY0)          # drop
rect("metal4", uo - 55, 21969, uo + 55, 22059)          # via enclosure
rect("via3", uo - 35, 21979, uo + 35, 22049)
rect("metal3", uo - 55, 21964, uo + 55, 22064)
rect("metal3", uo - 50, 21984, 31730, 22044)            # top row
rect("metal3", 31670, 4150, 31730, 22044)               # margin lane (west of ui's)
#- THE LAST HOP IS MET4, because the slot into the OSC pad is not
#- crossable on met3: a second VDD riser runs met3 at x 150.58..150.88
#- down to y 17.9 (measured: it put VDD_1V8 on the uo net). On met4
#- the same row is empty -- the strip's supply columns and every
#- riser there are met3 -- and the pad itself is met4, so the stub
#- lands on it with no via at all. The lanes swap sides so the met4
#- stub never crosses ui's met4 margin lane.
rect("metal3", 31615, 4150, 31785, 4320)                # via pad
rect("via3", 31665, 4200, 31735, 4270)
rect("metal4", 31615, 4150, 31785, 4320)
rect("metal4", 29770, 4190, 31785, 4250)                # met4 stub onto the pad

#- ------------------------------------------------------------------
#- uio_oe[7:0] -> VGND, tied low through a res_generic_m4 each
#- ------------------------------------------------------------------
bus_e = 0
for i in range(8):
    xc = XC[f"uio_oe[{i}]"]
    bus_e = max(bus_e, xc + 30)
    #- gr01's exact construction: the body sits DIRECTLY under the
    #- port pad, so its contacts are the pad (north) and the wire
    #- (south) and it extracts as exactly W=0.3 L=0.3. With metal on
    #- both sides of a floating body the extractor measured 0.32 x
    #- 0.28 -- and one of the eight 0.31 x 0.29 -- and netgen, unable
    #- to resolve eight identical-by-design resistors whose properties
    #- all differed, never reached its match-by-pin-name fallback.
    rect("rmetal4", xc - 30, 22044, xc + 30, PADY0)     # body under the pad
    rect("metal4", xc - 30, 21924, xc + 30, 22044)      # wire side
rect("metal4", 480, 21924, bus_e, 21984)                # the bus, into VGND

#- ------------------------------------------------------------------
#- write
#- ------------------------------------------------------------------
with open(OUT, "w") as f:
    f.write("magic\ntech sky130A\nmagscale 1 2\ntimestamp 1\n")
    for lay in ("locali", "viali", "metal1", "via1", "metal2", "via2",
                "metal3", "via3", "metal4", "rmetal4"):
        if not layers[lay]:
            continue
        f.write(f"<< {lay} >>\n")
        for x1, y1, x2, y2 in layers[lay]:
            f.write(f"rect {x1} {y1} {x2} {y2}\n")
    for cell, inst, path, *t in uses:
        a, b, c, d, e, g, bx1, by1, bx2, by2 = t
        f.write(f"use {cell}  {inst}"
                + (f" {path}" if path else "") + "\n")
        f.write(f"transform {a} {b} {c} {d} {e} {g}\n")
        f.write(f"box {bx1} {by1} {bx2} {by2}\n")
    f.write("<< labels >>\n")
    for l in labels:
        f.write(l + "\n")
    f.write("<< properties >>\n")
    f.write(f"string FIXED_BBOX 0 0 32200 {TOP}\n")
    f.write("<< end >>\n")
print(f"wrote {OUT}: {sum(len(v) for v in layers.values())} rects, "
      f"{len(uses)} uses, {n} ports")
