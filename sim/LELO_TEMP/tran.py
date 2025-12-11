#!/usr/bin/env python3
import pandas as pd
import yaml
import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as const
import re


def calcTemperatureFromFreq(freq,compensate=False):
    C = 53e-15*10
    R = 7.535e3*(8+4)
    N = 64
    ell = 2.8
    #- temperature coefficient from resistor
    res_n25 = 1/10.6e-6
    res_125 = 1/10e-6
    res_d_dtemp = (res_125 - res_n25)/(125-25)

    gain1 = 0.57
    offset1 = -40
    gain2 = 0.765
    offset2 = -35


    #- boltzman/unit charge
    k_q = const.k/const.e
    #- Calculate the diode voltage
    vd = k_q*(273.15 + 25)*(ell - 3*np.log(273.15 + 25)) + 1.12
    #- Estimate first temperature
    temperature = (freq*R*C/np.log(N)/k_q - 273.15)*gain1 + offset1

    if(compensate):
      #- Calculate the temperature dependent resistor from the temperature
      R_tcomp = (R + (res_d_dtemp)*(temperature - 25))
      #R_tcomp = R

      vdt = k_q*(273.15 + temperature)*(ell - 3*np.log(273.15 + temperature)) + 1.12

      temperature = (freq*R_tcomp*C/np.log(N)/k_q - 273.15)*vdt*gain2 + offset2

    return temperature


def main(name,show=False):
  yamlfile = name + ".yaml"
  with open(yamlfile) as fi:
    obj = yaml.safe_load(fi)


  with open("replace.yaml") as fi:
    replace = yaml.safe_load(fi)

  x = np.array([int(i) for i in re.split(r"\s+",replace["temperatures"])])

  y = list()
  for t in x:
    freq = float(1/(float(obj[f"t2_{t}"]) - float(obj[f"t1_{t}"])))
    y.append(freq)

  yi = np.array(y)
  fig,ax = plt.subplots(2,1,figsize=(12,6),sharex=True)


  y_no_res = calcTemperatureFromFreq(yi)
  y = calcTemperatureFromFreq(yi,compensate=True)

  error = y - x

  coefficients = np.polyfit(x, y, 1) # '1' indicates a first-degree polynomial (linear)
  slope = coefficients[0]
  intercept = coefficients[1]

  ycorr = (y - intercept)/slope

  inl = ycorr - x

  for i in range(0,len(x)):
      if(x[i] == -40):
          obj["freq_N40"] = float(yi[i])
          obj["temp_N40"] = float(y[i])
      elif(x[i] == 25):
          obj["freq_25"] = float(yi[i])
          obj["temp_25"] = float(y[i])
      elif(x[i] == 125):
          obj["freq_125"] = float(yi[i])
          obj["temp_125"] = float(y[i])



  #obj["temperature"] = [float(x) for x in x]
  #obj["estimate"] = [float(i) for i in y]
  #obj["freq"] = [float(i) for i in yi]
  obj["error"] = float(abs(error).max())
  obj["gainerror"] = float(slope)
  obj["offset"] = float(intercept)
  obj["inl"] = float(inl.max())


  with open(yamlfile,"w") as fo:
    yaml.dump(obj,fo)

  ax[0].plot(x,y,label="Simulation",marker="o")
  ax[0].plot(x,y_no_res,label="Simulation no resistor compensation",marker="^")
  ax[0].plot(x,x,label="Ideal curve",marker="x")
  ax[1].plot(x,y - x,label="Error",marker="o")
  ax[1].plot(x,y_no_res - x,label="Error, no resistor compensation",marker="^")
  ax[1].set_xlabel("Temperature [C]")
  ax[0].set_ylabel("Temperature estimate [C]")
  ax[1].set_ylabel("Temperature error [C]")
  ax[0].grid()
  ax[1].grid()
  ax[0].legend()
  ax[1].legend()
  ax[1].set_ylim(-5,5)
  plt.tight_layout()
  if(show):
    plt.show()
  else:
    plt.savefig(f"{name}.png")

if __name__ == "__main__":
  main("output_tran/tran_SchGtKttTtVt",show=True)
