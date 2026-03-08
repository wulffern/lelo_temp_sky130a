#!/usr/bin/env python3
import pandas as pd
from io import StringIO
#- From 
resistor_model = """
Index   v(vtemp)        i(v1)
0	-4.00000e+01	-1.07821e-05	
1	-3.50000e+01	-1.07906e-05	
2	-3.00000e+01	-1.07820e-05	
3	-2.50000e+01	-1.07722e-05	
4	-2.00000e+01	-1.07612e-05	
5	-1.50000e+01	-1.07490e-05	
6	-1.00000e+01	-1.07357e-05	
7	-5.00000e+00	-1.07213e-05	
8	0.000000e+00	-1.07056e-05	
9	5.000000e+00	-1.06889e-05	
10	1.000000e+01	-1.06710e-05	
11	1.500000e+01	-1.06521e-05	
12	2.000000e+01	-1.06320e-05	
13	2.500000e+01	-1.06109e-05	
14	3.000000e+01	-1.05886e-05	
15	3.500000e+01	-1.05653e-05	
16	4.000000e+01	-1.05410e-05	
17	4.500000e+01	-1.05157e-05	
18	5.000000e+01	-1.04893e-05	
19	5.500000e+01	-1.04620e-05	
20	6.000000e+01	-1.04336e-05	
21	6.500000e+01	-1.04043e-05	
22	7.000000e+01	-1.03741e-05	
23	7.500000e+01	-1.03429e-05	
24	8.000000e+01	-1.03108e-05	
25	8.500000e+01	-1.02778e-05	
26	9.000000e+01	-1.02440e-05	
27	9.500000e+01	-1.02093e-05	
28	1.000000e+02	-1.01738e-05	
29	1.050000e+02	-1.01375e-05	
30	1.100000e+02	-1.01003e-05	
31	1.150000e+02	-1.00624e-05	
32	1.200000e+02	-1.00238e-05	
33	1.250000e+02	-9.98438e-06
"""

import scipy.constants as const
import numpy as np

class LELO_TEMP():

    def __init__(self):


        #- Bipolar size difference and current difference
        self.N = 8*8

        #- 0 degrees celcius
        self.T0 = 273.15

        #- Center of the -40C to 125C curve
        self.Tcenter = 42.5

        #- Model comparator delay
        self.cmp_delay = 0e-9

        #- Simulation with 0.1 V across the resistor
        df = pd.read_csv(StringIO(resistor_model), sep=r"\s+")

        #- Simulation of 1 V across the resistor
        self.T_points = df["v(vtemp)"] + self.T0
        self.R_points = -1/df["i(v1)"]
        #self.T_points = np.array([self.T0-25, self.T0 + 27 , self.T0 + 75])
        #self.R_points = np.array([
       #    1 / 10.77e-6,
       #     1 / 10.6e-6,
       #     1 / 10.34e-6
        #])

        #- Boltzmann's constatnt over the unit charge
        self.k_q = const.k/const.e

        #- Parasitic capacitance
        self.C_cmp = 22e-15

        #- Capacitance of the
        self.C = 53.8e-15*5 + self.C_cmp

        #- Diode voltage current factor (<https://analogicus.com/aic2026/diodes>)
        self.ell = 2.35

        #- Bandgap silicon
        self.VG = 1.12

        #- Placeholder for compensation function
        self.compensate = None

        #- Compensation function generator
        self.makeLookupFunction()

        pass

    def makeLookupFunction(self):
        """Calculate a compensation function
        """
        #- Temperature in kelvin
        x = np.array(range(-40,125)) + self.T0

        #- Estimate frequency of oscillator
        freq = self.Freq(x)

        #- Estimated T_kelvin without know T_kelvin
        #  which disables the higher order effects of the resistor
        #  and diode
        y = self.KelvinFromFreq(freq)

        #- Compute a function to map from estimate T_kelvin
        #  to actual T_kelvin
        coeffs = np.polyfit(y, x, deg=2)
        self.compensate = np.poly1d(coeffs)


    def celcius(self,kelvin):
        return kelvin - self.T0

    def R(self,T_kelvin=None):
        """ Compute the T_kelvin dependent resistance
        """
        res = np.interp(300, self.T_points, self.R_points)
        if(T_kelvin is not None):
           res =np.interp(T_kelvin, self.T_points, self.R_points)
        return res



    def KelvinFromFreq(self,freq,T_kelvin=None,compensate=False):

        #- dt = 1/f/2
        dt = 1/freq/2 - self.cmp_delay

        #- I = C dV/dt
        I = self.C*self.Vc(T_kelvin)/dt

        #- DeltaV = I*R
        deltaV = I*self.R(T_kelvin)

        #- T = deltaV/(k/q)/ln(N)
        T = deltaV/self.k_q/np.log(self.N)

        if(compensate):
            T = self.compensate(T)

        return T

    def DeltaV(self,T_kelvin=None):
        deltaV =self.k_q*(T_kelvin)*np.log(self.N)
        return  deltaV

    def Current(self,T_kelvin=None):
        return self.DeltaV(T_kelvin)/self.R(T_kelvin)

    def dt(self,T_kelvin=None):
        return self.C*self.Vc(T_kelvin)/self.Current(T_kelvin) + self.cmp_delay

    def Vc(self,T_kelvin=None):
        #- Compute the default diode voltage at center T_kelvin
        vc = self.k_q*(self.T0+self.Tcenter)*(self.ell - 3*np.log(self.T0+self.Tcenter)) + self.VG
        if(T_kelvin is not None):
            #- If we know the T_kelvin, we can compute the actual T_kelvin
            vc =  self.k_q*(T_kelvin)*(self.ell - 3*np.log(T_kelvin)) + self.VG
            pass
        return vc

    def Freq(self,T_kelvin=None):
        return  1/(2*self.dt(T_kelvin))
