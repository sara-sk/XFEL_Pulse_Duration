import sys
import numpy as np 
import matplotlib.pyplot as plt
from scipy import signal
import scipy as sp

from src.parameters import Parameters as p

# Peakfinding class builds on Scipy Peakfinder
# Conditions defined in Parameter class
# Returns dataset with x- and y- coordinates of peaks

class Peakfinder:
    def __init__(self, data, photE):
        self.data = data
        self.peaks = sp.signal.find_peaks(self.data, height = p.heightcut*max(self.data)/100, prominence = p.prominence*max(self.data)/100, distance = p.nn_distance*len(photE)/100)
        self.peaks = self.peaks[0]
        
        self.xpeaks = np.asarray(self.peaks)
        self.ypeaks = np.asarray(self.data[self.xpeaks])
        self.allpeaks = np.array([self.xpeaks,self.ypeaks])
        
    def peaks(self):
    # returns dataset with neutral index x and intensity y
        return self.allpeaks
