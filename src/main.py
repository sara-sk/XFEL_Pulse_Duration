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

class Main:
    def __init__(self, intense, photE):
        
        #start = time.time()
        #print("Optimising lowpass cutoff for fast fit")
        cutoff = Fast_Backloop(intense).cutoff()
        spectra_for_slow_fit = []

        for i in range(len(intense[:,1])):
            fn = Fast_Fit(intense[i,:],p.deg,cutoff,photE)
            if fn.U() == 1:             
                spectra_for_slow_fit = np.append(spectra_for_slow_fit, i) 
                                        
            if i == 0:
                lpfns = fn.lpfn
                gaussians = fn.gauss()
                self.number_of_peaks = fn.nofpeaks()
                self.avgsigma = fn.avg_sigmas()
            else:
                lpfns = np.vstack((lpfns, fn.lpfn))
                gaussians = np.vstack((gaussians, fn.gauss()))
                self.number_of_peaks = np.vstack((self.number_of_peaks, fn.nofpeaks()))
                self.avgsigma = np.vstack((self.avgsigma, fn.avg_sigmas()))
            '''
            lpfns.append([fn.lpfn])
            gaussians.append([fn.gauss()])
            number_of_peaks.append( [(number_of_peaks, fn.nofpeaks())] )
            avgsigma.append( [(avgsigma, fn.avg_sigmas())] )
            '''

        intermediate = time.time()
        print("Time taken for fast fit:", (intermediate - start)/60, "minutes")
        print("Number of spectra to be analysed by slow fit: ", len(spectra_for_slow_fit))
        print("Beginning slow fit")

        for k in spectra_for_slow_fit:
            k = int(k)
            fn = Slow_Fit(intense[k,:], photE)
            lpfns[k] = fn.lpfn
            gaussians[k] = fn.gauss()
            self.number_of_peaks[k] = fn.nofpeaks()
            self.avgsigma[k] = fn.avg_sigmas()
        print("Data replaced")
        end = time.time()
        #lpfns, gaussians, number_of_peaks, avgsigma = np.array(lpfns), np.array(gaussians), np.array(number_of_peaks), np.array(avgsigma)
        print("Time taken for slow fit:", (end - intermediate)/60, "minutes")
        print("Time taken overall:", (end - start)/60, "minutes")

    def number_of_peaks(self):
        return self.number_of_peaks
    def avgsigma(self):
        return self.avgsigma
