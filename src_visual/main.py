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
from src_visual.parameters import Parameters as p

from src_visual.slowfit import Slow_Fit
from src_visual.fastfit import Fast_Fit
from src_visual.fastbackloop import Fast_Backloop

# Higher-level class which fits the function and calculates for each spectrum in the dataset
# the average sigma of its peaks and the number of peaks in the spectrum.

class Main:
    def __init__(self, intense, photE):
        
        start = time.time() # start timer

        for i in range(1):

            # Data taken through slow fit. Returns lowpassfunctions, individual Gaussians, number of peaks and
            # average sigma
            fn = Slow_Fit(intense,photE)

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

        end = time.time() # end timer

        print("Time taken for model to compute:", (end - start)/60, "minutes")

    # return number of peaks and average sigma. Average is root mean squared.
    def number_of_peaks(self):
        return self.number_of_peaks
    def avgsigma(self):
        return self.avgsigma
