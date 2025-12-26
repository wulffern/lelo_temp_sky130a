#!/usr/bin/env python3

#!/usr/bin/env python3
import pandas as pd
import yaml
import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as const
import re
import os
import sys



def getEll():
    return 2.34

def getR(temperature):
    R = 7.535e3*(8+4)
    T0 = 273.15

    #- temperature coefficient from resistor
    res_n25 = 1/10.6e-6
    res_125 = 1/10e-6
    res_d_dtemp = (res_125 - res_n25)/(125-25)

    R_tcomp = (R + (res_d_dtemp)*(temperature - 25))
    return R_tcomp

def getC():
    return 53e-15*5

def calcTKelvinFromFreq(freq,temperature=25):
    #- f = 2/RC*DeltaV/Vc
    deltaV_Vc = freq/2*getR(temperature)*getC()
    deltaV = deltaV_Vc*calcVc(temperature)
    #- deltaV = kT/q*ln(64)
    T = deltaV*k_q
    return deltaV


def calcDeltaV(temperature):
    T0 = 273.15
    N = 8*8
    k_q = const.k/const.e
    delta_v = k_q*(T0+temperature)*np.log(N)
    return delta_v

def calcCurrent(temperature,compensate=False):

    #- boltzman/unit charge
    k_q = const.k/const.e

    id = calcDeltaV(temperature)/getR(temperature)

    return id

def calcVc(temperature):
    #- Calculate the diode voltage, see https://analogicus.com/aic2026/2024/10/25/Diodes.html#forward-voltage-temperature-dependence

    T0 = 273.15
    k_q = const.k/const.e
    vc = k_q*(T0 + temperature)*(getEll() - 3*np.log(T0 + temperature)) + 1.12
    return vc

def calcFreq(temperature,compensate=False):

    id = calcCurrent(temperature,compensate=compensate)

    freq = id/(getC()*calcVc(temperature))

    return freq



def main(name,show=False):
    sys.path.append("./design/LELO_TEMP_SKY130A/")
    #- Get the model for calculating the temperature from the frequency
    import LELO_TEMP as lt

    x = np.arange(-40,125,5)

    fname = "sim/LELO_TEMP/output_tran/tran_SchGtKttTtVt.yaml"
    havesim = False
    if(os.path.exists(fname)):
        havesim = True
        with open(fname) as fi:
            obj  = yaml.safe_load(fi)

        temp = obj["temperature"]
        freqsim = obj["freq"]


    fig,ax = plt.subplots(3,1,figsize=(12,6),sharex=True)
    #ax = [ax]
    freq = calcFreq(x)

    ax[0].plot(x,freq,label="Frequency")
    y1 = lt.KelvinFromFreq(freq)
    ax[1].plot(x,y1,label="Calc raw")
    ax[1].plot(x,x,label="Ideal")
    ax[2].plot(x,y1-x,label="Error, no comp")
    if(havesim):
        ax[0].plot(temp,freqsim,label="Simulated Frequency")

    for a in ax:
        a.grid()
        a.legend()

    plt.tight_layout()
    if(show):
        plt.show()
    else:
        plt.savefig(f"{name}.png")

if __name__ == "__main__":
    main("output_tran/tran_SchGtKttTtVt",show=True)
