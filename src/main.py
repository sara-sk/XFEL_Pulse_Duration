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

from src.overlap import Overlap_Fit
from src.slowfit import Slow_Fit
from src.fastfit import Fast_Fit
from src.fastbackloop import Fast_Backloop

# Higher-level class which fits the function and calculates for each spectrum in the dataset
# the average sigma of its peaks and the number of peaks in the spectrum.

class Main:
    def __init__(self, intense, photE):
        
        start = time.time() # start timer
        a = 0

        for i in range(len(intense[:,1])):

            # Data taken through slow fit. Returns lowpassfunctions, individual Gaussians, number of peaks and
            # average sigma
            fn = Slow_Fit(intense[i,:],photE)
            #print(fn.U)
            #print(fn.U())
            if fn.U() > 0:
                Overlap_Fit(fn.Arr(),photE)
                a = a + 1

            # Initiate datasets for all data we want to extract from the slow fit
            if i == 0:
                lpfns = fn.lpfn
                gaussians = fn.gauss()
                self.number_of_peaks = fn.nofpeaks()
                self.avgsigma = fn.avg_sigmas()

            # Vertically stack data for all spectra. 'gaussians' may have different shapes for each spectrum,
            # hence the need to vertically stack.
            else:
                lpfns = np.vstack((lpfns, fn.lpfn))
                gaussians = np.vstack((gaussians, fn.gauss()))
                self.number_of_peaks = np.vstack((self.number_of_peaks, fn.nofpeaks()))
                self.avgsigma = np.vstack((self.avgsigma, fn.avg_sigmas()))
            #print("number of significantly overlapping spectra", len(overlaps))

            #Overlap_Fit(overlaps)


        end = time.time() # end timer

        # print("Time taken for fit:", (end - start)/60, "minutes")

    # return number of peaks and average sigma. Average is root mean squared.
        print("Overlaps:",a)
        #Overlap_Fit(overlaps,photE)
    def number_of_peaks(self):
        return self.number_of_peaks
    def avgsigma(self):
        return self.avgsigma
