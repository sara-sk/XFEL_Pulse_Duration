import sys
import numpy as np 
import matplotlib.pyplot as plt
import scipy as sp
from scipy.signal import butter
from scipy.optimize import curve_fit
from scipy import signal
from src.peakfinder import Peakfinder
from src.slices import Slice
from src.gauss import Gauss
from src.maxmin import MaxMin
from src.filterpeaks import Filter_peaks

from src.parameters import Parameters as p

# Class for fitting lowpass function and approximating Gaussians to raw data.
# Originally named slow fit because of the adaptive cutoff parameter for each spectrum.

class Slow_Fit:
    def __init__(self, lowpassdata,photE, fact):
        self.lowpassdata = lowpassdata
        
        # Fitting lowpass function, adjusting for both r2 value between points and for smoothness
        # Starting with ultra-low cutoff.
        lpcutoff = 0.0001
        rd = 1000000000000000000000000000000
        while True:
            # fitting lowpass function
            b, a = signal.butter(p.deg, lpcutoff, 'low')
            self.spec = signal.filtfilt(b, a, self.lowpassdata)

            # condition for good fitting based on vertical distance between maxima of raw and lowpass dataset
            # if not fitted within backloop_condition, increment until good fit
            self.height_difference = abs(max(self.lowpassdata) - max(self.spec))

            # r2 value
            # parameters alpha and beta are tunable in parameter class
            r2 = (p.alpha * np.sum((self.lowpassdata - self.spec)**2) 
                      + p.beta * np.sum((self.spec[:-1] - self.spec[1:])**2))
            # rd value
            old_rd = rd
            rd = np.sqrt(r2 / len(photE))
            
            if rd > old_rd:
                break
            else:
                lpcutoff = lpcutoff + 0.001
        
        # shift spectrum
        self.lpfn = self.spec - min(self.spec)
        self.shiftraw = self.lowpassdata - min(self.spec)
        
        # calculate noise
        self.noise = np.array([self.lowpassdata-self.spec]).T
        
        # Extracting peaks ([x-axis, y-axis]) - indexed to neutral.
        self.peaks = Peakfinder(self.lpfn,photE).peaks
         
        # Apply further constraints to peaks
        self.filteredpeaks = Filter_peaks(self.peaks).filtered_peaks()
                
        # Number of peaks, after filtering.
        self.n = len(self.filteredpeaks)
        
        # labelling spectra in case of no spike detected, as to skip further analysis
        if self.n == 0:
            self.getnumber = 0

        else:

            fn = Slice(self.lpfn,self.filteredpeaks, self.n)
        
            # Slice into individual peak functions, sprectrum == 0 outside individual slice
            self.slices = fn.slices()
        
            # Approximate each slice with Gaussian functions
            self.fn1 = Gauss(self.slices, self.n)
            self.Gaussian = self.fn1.Added_Gaussian()       # Return added Gaussian
            self.IndivGauss = self.fn1.IndivGaussians()     # Return individual Gaussians

            slicepos = fn.SlicingPoints()                   # Used to find minima 
            if True:
                self.fn2 = MaxMin(self.IndivGauss,self.n, slicepos, self.lpfn, photE)
                
            # Checking for significant overlap, definded by p.threshold
            minima = slicepos
            self.u = 0
            sig = self.fn1.sigmas
            ampl = self.fn1.ampl()
            center = self.fn1.center()
            a = 0
            if True:
                for i in range(len(minima)):
                    index = int(minima[i])
                    diff = self.Gaussian[index]-self.lpfn[index]
                    if (abs(diff)*100/max(self.lpfn)) > p.threshold and self.u == 0:
                        a = 1
                    else:
                        pass
                if a > 0:
                    for i in range(len(minima)):

                        G1 = self.IndivGauss[i]
                        G2 = self.IndivGauss[i+1]
                        sig1 = sig[i]
                        sig2 = sig[i + 1]
                        ampl1 = ampl[i]
                        ampl2 = ampl[i + 1]
                        center1 = center[i]
                        center2 = center[i + 1]

                        if self.u == 0:
                            self.arr = np.array([diff, G1, G2, self.lpfn, sig1, sig2, minima[i], ampl1, ampl2, center1, center2, self.n])
                        else:
                            array = np.array([diff, G1, G2, self.lpfn, sig1, sig2, minima[i], ampl1, ampl2, center1, center2, self.n])
                            self.arr = np.vstack((self.arr, array))

                        self.u = self.u + 1

            sum_ampl = np.sum(ampl)
            
            sig = sig/fact
            #print(sig)
            for i in range(len(sig)):
                sig[i] = sig[i]*ampl[i] / sum_ampl

            #print(sig)

            average = np.sum(sig)
            #print(average)
            # getting sigmas squared, taking the root mean

            self.sig = np.array(2.355*average)
            self.r2 = float(np.sum((self.lpfn - self.Gaussian)**2))

            self.getnumber = 1

    def getnumber(self):
        return self.getnumber
    def U(self):
        return self.u
    def Arr(self):
        return self.arr
    def r2(self):
        return self.r2
    def lpfn(self):
        return self.lpfn
    def gauss(self):
        return self.Gaussian
    def indiv(self):
        return self.IndivGauss
    def nofpeaks(self):
        return self.n
    def avg_sigmas(self):
        return self.sig
