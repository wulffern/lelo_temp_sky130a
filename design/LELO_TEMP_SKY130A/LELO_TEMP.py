#!/usr/bin/env python3

import scipy.constants as const
import numpy as np

class LELO_TEMP():

    def __init__(self):


        self.N = 8*8
        self.T0 = 273.15

        #- fudge factor to get the second order compensation working
        self.fudge = 3.125
        self.cmp_delay = 1e-9
        self.cmp_delay = 0
        #- Simulation of 1 V across the resistor
        self.R_n25 = 1/10.77e-6
        #self.R0 = 7.535e3*(8+4)
        self.R0 = 1/10.611e-6
        self.R_75 = 1/10.34e-6
        self.R_d_dtemp = (self.R_75 - self.R_n25)/100*self.fudge

        self.k_q = const.k/const.e
        self.onePointGain = 1.63
        #- Modify capacitor to get gain correct
        #self.C = 53.8e-15*10
        self.C = 53.8e-15*5
        self.ell = 2.35

        #- Bandgap silicon
        self.VG = 1.12
        pass

    def R(self,temperature=None):
        res = self.R0
        if(temperature is not None):
            res =  (self.R0 - (self.R_d_dtemp*(temperature-25)))
            pass

        return res

    def KelvinFromFreq(self,freq,temperature=None):

        #- f = 2/RC*DeltaV/Vc
        deltaV_Vc = freq/2*self.R(temperature)*self.C
        deltaV = deltaV_Vc  #/self.Vc(temperature)

        #- deltaV = kT/q*ln(64)
        T = deltaV/self.k_q/np.log(self.N)
        return T

    def DeltaV(self,temperature):
        return  self.k_q*(self.T0+temperature)*np.log(self.N)

    def Current(self,temperature):
        return self.DeltaV(temperature)/self.R(temperature)

    def Vc(self,temperature):
        vc = self.k_q*(self.T0 + 42)*(self.ell - 3*np.log(self.T0 + 42)) + self.VG
        if(temperature is not None):
            #- Does not look like this works to compensate the temperature sensor. Don't know why
            #vc =  self.k_q*(self.T0 + temperature)*(self.ell - 3*np.log(self.T0 + temperature)) + self.VG
            pass
        #print(vc)
        return vc

    def Freq(self,temperature):
        return  self.Current(temperature)/(self.C*self.Vc(temperature))


    def onePointCalibrationTemp(self,temperature,index25C):
        return temperature + self.T0 + 25 - temperature[index25C]

    def twoPointCalibrationTemp(self,temperature,index25C,index85C):
        gain = (temperature[index85C] - temperature[index25C])/60
        tcal = temperature/gain

        offset = self.T0 + 25 - tcal[index25C]
        return tcal + offset

    def onePointCalibration(self,freq,index25C):

        T = self.KelvinFromFreq(freq,temperature=None)
        Tcal = self.onePointCalibrationTemp(T,index25C)
        caltemp = list()
        for (f,t) in zip(freq,Tcal-self.T0):
            caltemp.append(self.KelvinFromFreq(f,temperature=t))

        caltemp = np.array(caltemp)*self.onePointGain
        return (self.onePointCalibrationTemp(caltemp,index25C),Tcal)

    def twoPointCalibration(self,freq,index25C,index85C):

        #- First iteration
        T = self.KelvinFromFreq(freq)
        Tcal = self.twoPointCalibrationTemp(T,index25C,index85C)

        #- Calculate the corrected temperature function
        caltemp = list()
        for (f,t) in zip(freq,Tcal-self.T0):
            caltemp.append(self.KelvinFromFreq(f,temperature=t))
        caltemp = np.array(caltemp)

        return (self.twoPointCalibrationTemp(caltemp,index25C,index85C),Tcal)
