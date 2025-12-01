#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("tb.csv")

fig,ax = plt.subplots(2,1,figsize=(12,6),sharex=True)

aoffset = -130
boffset = 0
gain = 1.2

y = (df["count"]+aoffset)*gain + boffset
x = df["temperature"]
coefficients = np.polyfit(x, y, 1) # '1' indicates a first-degree polynomial (linear)
slope = coefficients[0]
intercept = coefficients[1]

ax[0].plot(x,y,label="Simulation")
ax[0].plot(x,x,label="Ideal curve")
ax[1].plot(x,y - x,label="error")
ax[1].set_xlabel("Temperature [C]")
ax[0].set_ylabel("Temperature estimate [C]")
ax[1].set_ylabel("Temperature error [C]")
ax[0].grid()
ax[1].grid()
plt.tight_layout()
plt.savefig("verilog.png")

#plt.show()
