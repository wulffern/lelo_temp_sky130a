#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

sys.path.append("../../py/")


import LELO_TEMP

lt = LELO_TEMP.LELO_TEMP()

df = pd.read_csv("tb.csv")

freq = df["count"]*32768

offset = -6
x = df["temperature"]
y = lt.KelvinFromFreq(freq,compensate=True) - lt.T0 + offset

fig,ax = plt.subplots(3,1,figsize=(12,10),sharex=True)

ax[0].plot(x,y,label="Simulation")
ax[0].plot(x,x,label="Ideal curve")
ax[1].plot(x,y - x,label="error")
ax[2].plot(x,freq/1e6,label="Frequency")
ax[2].set_xlabel("Temperature [C]")
ax[0].set_ylabel("Temperature estimate [C]")
ax[1].set_ylabel("Temperature error [C]")
ax[2].set_ylabel("Frequency [MHz]")
ax[0].grid()
ax[2].grid()
ax[0].legend()
ax[1].grid()
ax[1].legend()
plt.tight_layout()
plt.savefig("verilog.png")

plt.show()
