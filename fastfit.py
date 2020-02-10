import sys
import h5py
import glob
import numpy as np 
from numpy import random
import matplotlib.pyplot as plt
from scipy import signal
import scipy as sp
from scipy.signal import butter
from scipy.optimize import curve_fit
from lmfit.models import GaussianModel
import time
import random
from src.peakfinder import Peakfinder
from src.filterpeaks import Filter_peaks
from src.gauss import Gauss
from src.slices import Slice
from src.parameters import Parameters as p

class Fast_Fit:
    def __init__(self, lowpassdata, deg, cutoff, photE):
        self.cutoff = float(cutoff)
        # lowpass function itself
        self.lowpassdata = lowpassdata
        b, a = signal.butter(deg, self.cutoff, 'low')
        self.spec = signal.filtfilt(b, a, self.lowpassdata)
        
        # shift spectrum
        self.lpfn = self.spec - min(self.spec)
        
        # calculate noise
        self.noise = np.array([self.lowpassdata-self.spec]).T
        
        """
        # visual module
        print("plotting lowpass data vs raw data, noise etc")
        plt.plot(photE,self.lowpassdata,label="raw data")
        plt.plot(photE,self.lpfn,label="shifted spectrum")
        plt.plot(photE,self.spec,label="lowpass")
        plt.plot(photE,self.noise,label="noise")
        plt.legend()
        plt.show()
        """
        
        # Extracting peaks ([x-axis, y-axis]) - indexed to neutral
        self.peaks = Peakfinder(self.lpfn, photE).peaks
        
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
        
        """
        # Visual module: comparing Gaussian to lowpass function - including individual gaussians
        plt.plot(self.Gaussian, label = "Added Gaussian")
        plt.plot(self.lpfn, label = "Shifted lowpass")
        for i in range(self.IndivGauss.shape[0]):
            plt.plot(self.IndivGauss[i],'--', markersize = '0.1', label = "indiv gaussian")
        plt.legend()
        plt.show()
        #"""
        
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
