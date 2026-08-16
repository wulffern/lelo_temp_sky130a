#!/usr/bin/env python3
"""Result figures for the README.

One figure per run-set (typical, etc, mc), each a grid of
temperature-error panels: rows are the views (Sch on top, Lay below),
columns are the calibrations (one-point left, two-point right). Every
corner is a thin black line. The industrial spec is the dashed red
pair of lines, the commercial spec (0..70C) the dotted box, and the
worst corner-to-corner error is printed in each panel.

Also updates each run's .yaml with the derived measurements
(errors, freq span, FOM) exactly as tran.py did, so `cicsim summary`
reads the same numbers the figures show.
"""
import os
import re
import sys

import matplotlib.pyplot as plt
import numpy as np
import yaml
from matplotlib.patches import Rectangle

sys.path.append("../../py/")
import LELO_TEMP

CLOCK_PERIODS = 4
TMIN, TMAX = -40, 125

SPEC = {
    "1p": {"ind": 15, "com": 10},
    "2p": {"ind": 10, "com": 5},
}

lt = LELO_TEMP.LELO_TEMP()

with open("replace.yaml") as fi:
    _replace = yaml.safe_load(fi)
TEMPS = np.array([int(i) for i in re.split(r"\s+", _replace["temperatures"])])


def process(name):
    """Read one corner's measurements, return temps/freq/errors in C.

    Writes the derived values back into <name>.yaml, mirroring what
    tran.py stored, so the summary tables agree with the figures.
    """
    yamlfile = name + ".yaml"
    with open(yamlfile) as fi:
        obj = yaml.safe_load(fi)

    freq = []
    for t in TEMPS:
        dt = (float(obj[f"t2_{t}"]) - float(obj[f"t1_{t}"])) / CLOCK_PERIODS
        freq.append(1 / dt)
    freq = np.array(freq)
    xk = TEMPS + lt.T0

    cname = (name.replace("tran", "calibrate")
                 .replace("Vh", "Vt").replace("Vl", "Vt")) + ".yaml"
    if not os.path.exists(cname):
        raise SystemExit(f"ERROR: no calibration values at {cname}")
    with open(cname) as fi:
        calib = yaml.safe_load(fi)

    temp = lt.KelvinFromFreq(freq, compensate=True)
    err1 = (temp + calib["one_offset"]) - xk
    err2 = (temp * calib["two_gain"] + calib["two_offset"]) - xk

    com = (TEMPS >= 0) & (TEMPS <= 70)
    for key, err in (("1p", err1), ("2p", err2)):
        obj[f"ind_{key}_max"] = float(err.max())
        obj[f"ind_{key}_min"] = float(err.min())
        obj[f"com_{key}_max"] = float(err[com].max())
        obj[f"com_{key}_min"] = float(err[com].min())
    obj["freq_min"] = float(freq.min())
    obj["freq_max"] = float(freq.max())
    obj["temperature"] = [float(lt.celcius(x)) for x in xk]
    obj["freq"] = [float(f) for f in freq]
    obj["error_two_pp"] = float(np.abs(err2[com].max() - err2[com].min()))
    obj["FOM"] = float((-obj["idd_25"] * (1 / 32768) / (100e-3)
                        - obj["iddq_25"]) * obj["error_two_pp"])
    with open(yamlfile, "w") as fo:
        yaml.dump(obj, fo)

    return {"temp": TEMPS.astype(float), "freq": freq,
            "1p": err1, "2p": err2}


def runs_of(runfile):
    with open(runfile) as fi:
        return [process(l.strip()) for l in fi if l.strip()]


def error_panel(ax, runs, cal):
    ind, com = SPEC[cal]["ind"], SPEC[cal]["com"]
    for r in runs:
        ax.plot(r["temp"], r[cal], color="black", lw=0.9,
                marker="o", ms=2.5, alpha=0.8)
    ax.axhline(+ind, color="crimson", ls="--", lw=1)
    ax.axhline(-ind, color="crimson", ls="--", lw=1)
    ax.add_patch(Rectangle((0, -com), 70, 2 * com, fill=False,
                           edgecolor="0.35", ls=":", lw=1))
    wmax = max(r[cal].max() for r in runs)
    wmin = min(r[cal].min() for r in runs)
    ax.text(0.02, 0.97, f"worst {wmax:+.1f} / {wmin:+.1f} C",
            transform=ax.transAxes, va="top", fontsize=9)
    lim = max(ind, wmax, -wmin) + 3
    ax.set_ylim(-lim, lim)
    ax.set_xlim(TMIN - 5, TMAX + 5)
    ax.grid(True, alpha=0.3)


def error_figure(runset):
    views = [v for v in ("Sch", "Lay")
             if os.path.exists(f"tran_{v}_{runset}.run")]
    if not views:
        print(f"INFO: no runs for {runset}, skipped")
        return
    fig, axes = plt.subplots(len(views), 2, figsize=(10, 3.2 * len(views)),
                             sharex=True, squeeze=False)
    for i, view in enumerate(views):
        runs = runs_of(f"tran_{view}_{runset}.run")
        for j, cal in enumerate(("1p", "2p")):
            ax = axes[i][j]
            error_panel(ax, runs, cal)
            n = len(runs)
            noun = "samples" if runset == "mc" else "corners"
            title = {"1p": "One point calibration",
                     "2p": "Two point calibration"}[cal]
            ax.set_title(f"{title}, {view}"
                         + (f" ({n} {noun})" if n > 1 else ""), fontsize=10)
        axes[i][0].set_ylabel("Temperature error [C]")
    for ax in axes[-1]:
        ax.set_xlabel("Temperature [C]")
    fig.tight_layout()
    fig.savefig(f"tran_err_{runset}.png", dpi=110)
    plt.close(fig)
    print(f"INFO: wrote tran_err_{runset}.png")


def transfer_figure():
    fig, ax = plt.subplots(figsize=(10, 3.6))
    styles = {"Sch": "-", "Lay": "--"}
    for view in ("Sch", "Lay"):
        runfile = f"tran_{view}_typical.run"
        if not os.path.exists(runfile):
            continue
        for r in runs_of(runfile):
            ax.plot(r["temp"], r["freq"] / 1e6, styles[view], color="black",
                    lw=1, marker="o", ms=3, label=view)
    ax.set_xlabel("Temperature [C]")
    ax.set_ylabel("Frequency [MHz]")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig("tran_transfer.png", dpi=110)
    plt.close(fig)
    print("INFO: wrote tran_transfer.png")


if __name__ == "__main__":
    transfer_figure()
    for runset in ("typical", "etc", "mc"):
        error_figure(runset)
