#!/usr/bin/env python3
"""Make the RC extraction (work/lpe/*_lper.spi) simulatable.

Two magic/ext2spice artifacts stop ngspice from parsing it:
 - ~19 DUPLICATE device names ("device already exists, bail out"):
   renamed in place, second occurrence onward gets a uN suffix;
 - diode area/perim come out in pm^2/pm (the same issue the lpe
   netlist target fixes in tech's sim.make): scaled to m^2/m, with
   the >1 guard making it idempotent.

Both edits are idempotent, so running this twice is safe.
"""
import re
import sys


def main(path):
    lines = open(path).readlines()
    seen = {}
    fixed = 0
    for i, l in enumerate(lines):
        if l[:1] in "RrCcXx" and l.split():
            name = l.split()[0]
            if name in seen:
                seen[name] += 1
                lines[i] = l.replace(name, f"{name}u{seen[name]}", 1)
                fixed += 1
            else:
                seen[name] = 0
        if "sky130_fd_pr__diode" in lines[i]:
            def area(m):
                v = float(m.group(1))
                return f"area={v*1e-24:.6g}" if v > 1 else m.group(0)

            def perim(m):
                v = float(m.group(1))
                return f"perim={v*1e-12:.6g}" if v > 1 else m.group(0)
            lines[i] = re.sub(r"\barea=([0-9.eE+]+)", area, lines[i])
            lines[i] = re.sub(r"\bperim=([0-9.eE+]+)", perim, lines[i])
    open(path, "w").writelines(lines)
    print(f"fix_lper: {path}: renamed {fixed} duplicate device names")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else
         "../../work/lpe/LELO_TEMP_lper.spi")
