#!/usr/bin/env python3
import pandas as pd
import yaml
import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as const
import re
import os
import sys

sys.path.append("../../design/LELO_TEMP_SKY130A/")

import LELO_TEMP

def main(name,corner=None,show=False,ax=None,redColor="red",blueColor="blue"):

  print(f"INFO: Opening {name}")

  yamlfile = name + ".yaml"
  with open(yamlfile) as fi:
    obj = yaml.safe_load(fi)

  with open("replace.yaml") as fi:
    replace = yaml.safe_load(fi)



  x = np.array([int(i) for i in re.split(r"\s+",replace["temperatures"])])

  y = list()
  for t in x:
    dt = (float(obj[f"t2_{t}"]) - float(obj[f"t1_{t}"]))/3
    y.append(float(1/dt))

    lt = LELO_TEMP.LELO_TEMP()
  xk = x + lt.T0
  freq = np.array(y)

  if(ax is None):
    fig,ax = plt.subplots(2,2,figsize=(16,9),sharex=True,sharey=True)

  #- Find calibration values
  cname = name.replace("tran","calibrate").replace("Vh","Vt").replace("Vl","Vt") + ".yaml"

  if(os.path.exists(cname)):
    with open(cname) as fi:
      calib = yaml.safe_load(fi)


    #- Calculate one point calibration
    temp1 = lt.KelvinFromFreq(freq)
    temp_one =  temp1 +  calib["one_offset"]

    #- Calculate two point calibration
    temp2 = lt.KelvinFromFreq(freq)
    temp_two = temp2*calib["two_gain"] + calib["two_offset"]

    pass
  else:
    raise Exception(f"Can't find calibration values for {cname}")

  error_one = temp_one - xk
  error_two = temp_two - xk

  istart = 0
  istop  = 0
  for i in range(0,len(x)):
    if(x[i] <= 0):
      istart = i
    if(x[i] <= 70):
      istop = i


  def addError(name,error):
    obj[f"ind_{name}_max"] = float(error.max())
    obj[f"ind_{name}_min"] = float(error.min())
    obj[f"com_{name}_max"] = float(error[istart:istop+1].max())
    obj[f"com_{name}_min"] = float(error[istart:istop+1].min())
  addError("1p",error_one)
  addError("2p",error_two)


  obj["freq_min"] = float(freq.min())
  obj["freq_max"] = float(freq.min())

  with open(yamlfile,"w") as fo:
    yaml.dump(obj,fo)

  xp = xk
  yp1 = temp_one
  yp2 = temp_two

  shortname = name.split("/")[-1]

  #- Use blue color map for yp1 and red color map for yp2 
  ax[0][0].plot(lt.celcius(xp),lt.celcius(yp1),marker="o",color=blueColor,label=shortname)
  ax[0][1].plot(lt.celcius(xp),lt.celcius(yp2),marker="o",color=redColor,label=shortname)
  ax[0][0].plot(lt.celcius(xp),lt.celcius(xp),color="black",marker="x",linestyle="dotted",alpha=0.5)
  ax[0][1].plot(lt.celcius(xp),lt.celcius(xp),color="black",marker="x",linestyle="dotted",alpha=0.5)
  ax[1][0].plot(lt.celcius(xp),lt.celcius(yp1) - lt.celcius(xp),marker="o",color=blueColor,label=shortname)
  ax[1][1].plot(lt.celcius(xp),lt.celcius(yp2) - lt.celcius(xp),marker="o",color=redColor,label=shortname)
  ax[1][0].set_xlabel("Temperature [C]")
  ax[0][0].set_ylabel("Temperature estimate [C]")
  ax[1][0].set_ylabel("Temperature error [C]")
  ax[1][1].set_xlabel("Temperature [C]")
  ax[0][0].set_title("One Point Calibration")
  ax[0][1].set_title("Two Point Calibration")
  #ax[3].set_ylabel("Temperature error [C]")
  ax[0][0].grid(True)
  ax[0][1].grid(True)  
  ax[1][0].grid(True)  
  ax[1][1].grid(True)
  ax[1][0].set_ylim(-15,15)
  ax[1][1].set_ylim(-15,15)
 # ax[2].grid(True)
  #ax[3].grid(True)
  #- Use font size small for the legend with multiple columns
  ax[0][0].legend(fontsize=8, ncol=3, loc='upper left', bbox_to_anchor=(0, 1))
  ax[0][1].legend(fontsize=8, ncol=3, loc='upper left', bbox_to_anchor=(0, 1))
  plt.tight_layout()
  if(ax is None):
    if(show):
      plt.show()
    else:
      plt.savefig(f"{name}.png")

if __name__ == "__main__":

  if(len(sys.argv) > 1):
    fig,ax = plt.subplots(2,2,figsize=(16,9),sharex=True)

    # Read all lines from all files first to determine total count
    all_lines = []
    for f in sys.argv[1:]:
      with open(f) as fi:
        all_lines.extend([l.strip() for l in fi if l.strip()])
    
    # Create colormaps for blue and red
    blue_cmap = plt.cm.jet
    red_cmap = plt.cm.jet
    n_lines = len(all_lines)
    
    # Process each line with colors from the colormaps
    for i, line in enumerate(all_lines):
      # Map index to colormap (use range 0.4 to 0.9 to avoid too light colors)
      blue_color = blue_cmap(0.4 + 0.5 * i / max(1, n_lines - 1))
      red_color = red_cmap(0.4 + 0.5 * i / max(1, n_lines - 1))
      main(line, show=False, ax=ax, blueColor=blue_color, redColor=red_color)
    
    #plt.show()
    plt.savefig(f.replace(".run",".png"))
  else:
    main("output_tran/tran_SchGtKttTtVt",show=True)
