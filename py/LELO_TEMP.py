#!/usr/bin/env python3

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
        self.cmp_delay = 1.5e-9

        #- Simulation of 1 V across the resistor
        self.T_points = np.array([self.T0 -25, self.T0 + 27, self.T0 + 75])
        self.R_points = np.array([
            1 / 9.77e-6,
            1 / 9.68e-6,
            1 / 9.44e-6
        ])

        #- Boltzmann's constatnt over the unit charge
        self.k_q = const.k/const.e

        #- Parasitic capacitance
        self.C_cmp = 19e-15

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
