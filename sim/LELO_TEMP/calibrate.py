#!/usr/bin/env python3
import pandas as pd
import yaml
import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as const
import re

import sys

sys.path.append("../../design/LELO_TEMP_SKY130A/")

import LELO_TEMP


def main(name,corner=None,show=False,ax=None):

  print(f"INFO: Opening {name}")

  yamlfile = name + ".yaml"
  with open(yamlfile) as fi:
    obj = yaml.safe_load(fi)

  with open("replace.yaml") as fi:
    replace = yaml.safe_load(fi)

  lt = LELO_TEMP.LELO_TEMP()

  x = [25,85]

  y = list()
  for t in x:
    dt = (float(obj[f"t2_{t}"]) - float(obj[f"t1_{t}"]))/3
    freq = float(1/dt)
    y.append(freq)

  xk = np.array(x) + lt.T0
  freq = np.array(y)


  #- One point calibration
  temp1 = lt.KelvinFromFreq(freq,np.array([25,25]))
  one_b1 = (lt.T0 + 25) - temp1[0]
  temp_onepoint = temp1 + one_b1

  #- Two point calibration
  temp2 = lt.KelvinFromFreq(freq)
  gain = 60/(temp2[1] - temp2[0])
  temp3 = temp2*gain
  offset = (lt.T0 + 25) - temp3[0]
  temp_twopoint = temp2*gain + offset


  obj["one_offset"] = float(one_b1)
  obj["two_offset"] = float(offset)
  obj["two_gain"] = float(gain)


  with open(yamlfile,"w") as fo:
    yaml.dump(obj,fo)

if __name__ == "__main__":

  if(len(sys.argv) > 1):
    fig,ax = plt.subplots(2,1,figsize=(12,6),sharex=True)
    ax[0].set_title("")
    for f in sys.argv[1:]:
      with open(f) as fi:
        for l in fi:
          main(l.strip(),show=False,ax=ax)
    plt.show()
  else:
    main("output_calibrate/calibrate_SchGtKttTtVt",show=True)
