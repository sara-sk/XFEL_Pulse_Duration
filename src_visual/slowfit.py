import sys
import numpy as np 
import matplotlib.pyplot as plt
import scipy as sp
from scipy.signal import butter
from scipy.optimize import curve_fit
from scipy import signal
from src_visual.peakfinder import Peakfinder
from src_visual.slices import Slice
from src_visual.gauss import Gauss
from src_visual.maxmin import MaxMin
from src_visual.filterpeaks import Filter_peaks

from src_visual.parameters import Parameters as p

# Class for fitting lowpass function and approximating Gaussians to raw data.
# Originally named slow fit because of the adaptive cutoff parameter for each spectrum.

class Slow_Fit:
    def __init__(self, lowpassdata,photE):
        self.lowpassdata = lowpassdata
        
        # Fitting lowpass function, adjusting for both r2 value between points and for smoothness
        # Starting with ultra-low cutoff.
        lpcutoff = 0.0001

        while True:
            # fitting lowpass function
            b, a = signal.butter(p.deg, lpcutoff, 'low')
            self.spec = signal.filtfilt(b, a, self.lowpassdata)
                                  
            # Visual module for checking
            #plt.plot(self.spec, label='lowpass')
            plt.plot(self.lowpassdata, label='raw data')
            plt.plot(self.spec, label='lowpass data')
            plt.legend()
            plt.show()

            # condition for good fitting based on vertical distance between maxima of raw and lowpass dataset
            # if not fitted within backloop_condition, increment until good fit
            self.height_difference = abs(max(self.lowpassdata) - max(self.spec))

            # r2 value
            # parameters alpha and beta are tunable in parameter class
            r2 = (p.alpha * np.sum((self.lowpassdata - self.spec)**2) 
                      - p.beta * np.sum((self.lowpassdata[:-1] - self.lowpassdata[1:])**2))
            # rd value
            rd = np.sqrt(r2 / len(photE))

            # backloop condition defined in parameter class
            if rd > p.backloop_condition_slow * max(self.lowpassdata)/100:
                lpcutoff = lpcutoff + 0.001            # increment arbitrarily chosen
            else:
                break
                
        
        
        # shift spectrum
        self.lpfn = self.spec - min(self.spec)
        
        # calculate noise
        self.noise = np.array([self.lowpassdata-self.spec]).T
        
        # Extracting peaks ([x-axis, y-axis]) - indexed to neutral.
        self.peaks = Peakfinder(self.lpfn,photE).peaks
        
        # Apply further constraints to peaks
        self.filteredpeaks = Filter_peaks(self.peaks).filtered_peaks()
                
        # Number of peaks, after filtering.
        self.n = len(self.filteredpeaks)
        
        fn = Slice(self.lpfn,self.filteredpeaks, self.n)
        
        # Slice into individual peak functions, sprectrum == 0 outside individual slice
        self.slices = fn.slices()
        
        # Approximate each slice with Gaussian functions
        self.fn1 = Gauss(self.slices, self.n)
        self.Gaussian = self.fn1.Added_Gaussian()       # Return added Gaussian
        self.IndivGauss = self.fn1.IndivGaussians()     # Return individual Gaussians
        
        slicepos = fn.SlicingPoints()                   # Used to find minima
        
        self.fn2 = MaxMin(self.IndivGauss,self.n, slicepos, self.lpfn, photE)
        
        plt.plot(photE, self.Gaussian, label="Gaussian approximation")
        
        for i in range(self.IndivGauss.shape[0]):
            plt.plot(photE, self.IndivGauss[i],'--',markersize = 0.1, label="indiv gaussian")
        plt.plot(photE, self.lpfn, label = "Shifted lowpass function")
        plt.plot(photE, lowpassdata, label = "Raw data")
        
        
        plt.plot(self.fn2.GetMax_x(),self.fn2.GetMax_y(), 'go')
        if self.n != 1:
            plt.plot(self.fn2.GetMin_x(),self.fn2.GetMin_y(), 'ro')
        plt.legend()
        plt.show()
        
        # Checking for significant overlap, definded by p.threshold
        minima = slicepos
        self.u = 0
        for i in range(len(minima)):
            index = int(minima[i])
            if (abs(self.Gaussian[index]-self.lpfn[index])*100/max(self.lpfn)) > p.threshold and self.u == 0:
                self.u = self.u + 1
        
        # getting sigmas squared, taking the root mean
        sig = self.fn1.sigmas
        self.sig = np.array(np.sqrt((np.average(sig))))
        
    def U(self):
        return self.u
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
