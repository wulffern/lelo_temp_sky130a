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


def main(name,show=False,ax=None):

  print(f"INFO: Opening {name}")

  yamlfile = name + ".yaml"
  with open(yamlfile) as fi:
    obj = yaml.safe_load(fi)


  with open("replace.yaml") as fi:
    replace = yaml.safe_load(fi)

  lt = LELO_TEMP.LELO_TEMP()

  x = np.array([int(i) for i in re.split(r"\s+",replace["temperatures"])])

  y = list()
  for t in x:
    dt = (float(obj[f"t2_{t}"]) - float(obj[f"t1_{t}"]))/3
    freq = float(1/dt)
    y.append(freq)

  xk = x + lt.T0
  yi = np.array(y)

  if(ax is None):
    fig,ax = plt.subplots(2,1,figsize=(12,6),sharex=True)

  index25 = None
  index85 = None
  for i in range(0,len(x)):
      if(x[i] == -40):
        obj["freq_N40"] = float(yi[i])
        obj["temp_N40"] = float(y[i])
      elif(x[i] == 25):
        obj["freq_25"] = float(yi[i])
        obj["temp_25"] = float(y[i])
        index25 = i
      elif(x[i] == 85):
        index85 = i
        obj["freq_85"] = float(yi[i])
        obj["temp_85"] = float(y[i])
      elif(x[i] == 125):
        obj["freq_125"] = float(yi[i])
        obj["temp_125"] = float(y[i])


  y1,y1nc = lt.onePointCalibration(yi,index25)
  y2,y2nc = lt.twoPointCalibration(yi,index25,index85)

  error_one = y1 -xk
  error_two = y2-xk

  istart = 0
  istop  = 0
  for i in range(0,len(x)):
    if(x[i] <= 0):
      istart = i
    if(x[i] <= 70):
      istop = i

    if(x[i] == -40):
      obj["temp_N40"] = float(y2[i] - lt.T0)
    elif(x[i] == 25):
      obj["temp_25"] = float(y2[i] - lt.T0)
      index25 = i
    elif(x[i] == 85):
      obj["temp_85"] = float(y2[i] - lt.T0)
    elif(x[i] == 125):
      obj["temp_125"] = float(y2[i] - lt.T0)


  obj["temperature"] = [float(x) for x in x]
  obj["freq"] = [float(i) for i in yi]

  def addError(name,error):
    obj[f"ind_{name}_max"] = float(error.max())
    obj[f"ind_{name}_min"] = float(error.min())
    obj[f"com_{name}_max"] = float(error[istart:istop+1].max())
    obj[f"com_{name}_min"] = float(error[istart:istop+1].min())
  addError("1p",error_one)
  addError("2p",error_two)



  with open(yamlfile,"w") as fo:
    yaml.dump(obj,fo)

  def celcius(kelvin):
    return kelvin - lt.T0

  xp = xk
  yp1 = y1
  yp2 = y2

  ax[0].plot(celcius(xp),celcius(yp1),marker="o",color="blue")
  ax[0].plot(celcius(xp),celcius(yp2),marker="o",color="red")

  ax[0].plot(celcius(xp),celcius(xp),color="black",marker="x",linestyle="dotted",alpha=0.5)
  ax[1].plot(celcius(xp),celcius(yp1) - celcius(xp),marker="o",color="blue")
  ax[1].plot(celcius(xp),celcius(yp2) - celcius(xp),marker="o",color="red")
  ax[1].set_xlabel("Temperature [C]")
  ax[0].set_ylabel("Temperature estimate [C]")
  ax[1].set_ylabel("Temperature error [C]")
  ax[0].grid()
  ax[1].grid()
  plt.tight_layout()
  if(show):
    plt.show()
  else:
    plt.savefig(f"{name}.png")

if __name__ == "__main__":

  if(len(sys.argv) > 1):
    fig,ax = plt.subplots(2,1,figsize=(12,6),sharex=True)
    for f in sys.argv[1:]:
      with open(f) as fi:
        for l in fi:
          main(l.strip(),show=False,ax=ax)
    plt.show()
  else:
    main("output_tran/tran_SchGtKttTtVt",show=True)
