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

class Slow_Fit:
    def __init__(self, lowpassdata,photE):
        self.lowpassdata = lowpassdata
        
        # fitting lowpass, including backloop for better cutoff.
        lpcutoff = 0.0001
        while True:
            # fitting lowpass function with given cutoff
            b, a = signal.butter(p.deg, lpcutoff, 'low')
            self.spec = signal.filtfilt(b, a, self.lowpassdata)
                                  
            # Visual module for chpecking
            plt.plot(self.lpfn, label='lowpass')
            plt.plot(self.lowpassdata, label='raw data')
            plt.legend()
            plt.show()

            # condition for good fitting based on vertical distance between maxima of raw and lowpass dataset
            # if not fitted within backloop_condition, increment until good fit
            self.height_difference = abs(max(self.lowpassdata) - max(self.spec))
            #r2 value
            r2 = (p.alpha * np.sum((self.lowpassdata - self.spec)**2) 
                      - p.beta * np.sum((self.lowpassdata[:-1] - self.lowpassdata[1:])**2))
            #if self.height_difference > backloop_condition_slow * max(self.lowpassdata)/100:
            #    lpcutoff = lpcutoff + 0.001
            rd = np.sqrt(r2 / len(photE))
            
            if rd > p.backloop_condition_slow * max(self.lowpassdata)/100:
                lpcutoff = lpcutoff + 0.001
            else:
                break
                
        
        
        # shift spectrum
        self.lpfn = self.spec - min(self.spec)
        
        # calculate noise
        self.noise = np.array([self.lowpassdata-self.spec]).T
        
        # Extracting peaks ([x-axis, y-axis]) - indexed to neutral
        self.peaks = Peakfinder(self.lpfn,photE).peaks
        
        #print(self.peaks)
        
        # Apply further constraints to peaks
        self.filteredpeaks = Filter_peaks(self.peaks).filtered_peaks()
                
        # number of peaks, after filtering.
        self.n = len(self.filteredpeaks)
        
        fn = Slice(self.lpfn,self.filteredpeaks, self.n)
        
        # Slice into individual peak functions, outside peak spectrum = 0. 
        self.slices = fn.slices()
        
        # Approximate slices with Gaussians
        
        self.fn1 = Gauss(self.slices, self.n)
        self.Gaussian = self.fn1.Added_Gaussian()  
        self.IndivGauss = self.fn1.IndivGaussians()
        
        slicepos = fn.SlicingPoints()
        
        self.fn2 = MaxMin(self.IndivGauss,self.n, slicepos, self.lpfn, photE)
        
        plt.plot(photE, self.Gaussian, label="Gaussian approximation")
        
        for i in range(self.IndivGauss.shape[0]):
            plt.plot(photE, self.IndivGauss[i],'--',markersize = 0.1, label="indiv gaussian")
        plt.plot(photE, self.lpfn, label = "shifted lowpass function")
        plt.plot(photE, lowpassdata, label = "original function")
        
        
        plt.plot(self.fn2.GetMax_x(),self.fn2.GetMax_y(), 'go')
        if self.n != 1:
            plt.plot(self.fn2.GetMin_x(),self.fn2.GetMin_y(), 'ro')
        plt.legend()
        plt.show()
        
        minima = fn.SlicingPoints()
        self.u = 0
        for i in range(len(minima)):
            index = int(minima[i])
            if (abs(self.Gaussian[index]-self.lpfn[index])*100/max(self.lpfn)) > p.threshold and self.u == 0:
                self.u = self.u + 1
        
        sig = self.fn1.sigmas
        self.sig = np.array((np.average(sig)))
        
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
