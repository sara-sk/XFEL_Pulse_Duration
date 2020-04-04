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
from src.parameters import Parameters as p
from src.modelanalysis import Model_Analysis
from src.overlap import Overlap_Fit
from src.slowfit import Slow_Fit

# Higher-level class which fits the function and calculates for each spectrum in the dataset
# the average sigma of its peaks and the number of peaks in the spectrum.

class Main:
    def __init__(self, intense, photE):
        
        start = time.time() # start timer
        a = 0
        diffs = []
        r2old = []
        r2new = []
        overlap_times = []
        b = 0
        for i in range(len(intense[:,1])):
            # Data taken through slow fit. Returns lowpassfunctions, individual Gaussians, number of peaks and average sigma
            fn = Slow_Fit(intense[i,:],photE)
            
            # detect cases of no peaks
            if fn.getnumber == 0:
                b = b + 1

            else:
                # record spectra with overlaps (fn.U > 0)
                if fn.U() > 0:
                    t1 = time.time()
                    function = Overlap_Fit(fn.Arr(), photE, fn.nofpeaks())
                    t2 = time.time()
                    overlap_times.append(t2-t1)
                    a = a + 1
                    replacement = function.Get_New_Sigma()
                    diffs.append(function.diff)
                    r2old.append(function.r2old)
                    r2new.append(function.r2new)
                else:
                    r2new.append(fn.r2)
                    r2old.append(fn.r2)

                # Initiate datasets for all data we want to extract from the slow fit. Case of overlaps, replace sigmas
                if i == 0:
                    lpfns = fn.lpfn
                    gaussians = fn.gauss()
                    self.number_of_peaks = fn.nofpeaks()
                    self.avgsigma = fn.avg_sigmas()
                    if fn.U() > 0:
                        self.avgsigma = replacement

                # Vertically stack data for all spectra. 'gaussians' may have different shapes for each spectrum,
                # hence the need to vertically stack.
                else:
                    lpfns = np.vstack((lpfns, fn.lpfn))
                    gaussians = np.vstack((gaussians, fn.gauss()))
                    self.number_of_peaks = np.vstack((self.number_of_peaks, fn.nofpeaks()))
                    
                    # account for overlapping spectra
                    if fn.U() > 0:
                        self.avgsigma = np.vstack((self.avgsigma, replacement))
                    else:
                        self.avgsigma = np.vstack((self.avgsigma, fn.avg_sigmas()))

        end = time.time() # end timer
        t = (end-start)/60
        inputs = np.array([a, diffs, r2old, r2new, t, overlap_times, r2new, i])

        # class for analysing effectiveness of model
        Model_Analysis(inputs)

        # return number of peaks and average sigma. Average is root mean squared.

        #print("Overlaps:",a, "out of", i, "spectra")
        #print("Number of spectra without a clear peak", b)
    def number_of_peaks(self):
        return self.number_of_peaks
    def avgsigma(self):
        return self.avgsigma
