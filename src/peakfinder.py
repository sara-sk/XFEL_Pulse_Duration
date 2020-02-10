# helps fast_fit return peaks
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

class Peakfinder:
    def __init__(self, data, photE):
        self.data = data
        self.peaks = sp.signal.find_peaks(self.data, height = p.heightcut, prominence = p.prominence*max(self.data)/100, distance = p.nn_distance*len(photE)/100)
        self.peaks = self.peaks[0]
        
        self.xpeaks = np.asarray(self.peaks)
        self.ypeaks = np.asarray(self.data[self.xpeaks])
        self.allpeaks = np.array([self.xpeaks,self.ypeaks])
        
        
    def peaks(self):
    # returns dataset with neutral index x and intensity y  
        """
        # Visual module
        print("Plotting peaks found. Neutrally indexed.")
        plt.plot(self.data, label="data fed to peak finder")
        plt.plot(self.xpeaks,self.ypeaks,label="peaks",'go')
        plt.legend()
        plt.show()
        """
        return self.allpeaks
