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

class MaxMin:
    def __init__(self, data, nofpeaks, slicepos, lpfn, photE):
        self.n = nofpeaks
        self.data = data
        self.slicepos = slicepos
        self.lpfn = lpfn
        
        #if self.n == 1:
        #    self.ymax = max(self.data)
        #    self.xmax = np.where(self.data == self.ymax)
        if False:
            pass
        else:
            self.ymin = []
            self.xmin = []
            for j in range(len(slicepos)):
                ind2 = int(self.slicepos[j])
                ymin = self.lpfn[ind2]
                self.ymin = np.append(self.ymin, ymin)

                xmin = photE[self.slicepos[j]]
                self.xmin = np.append(self.xmin, xmin)
                
            self.ymax = []
            self.xmax = []
            for i in range(self.n):
                if i == 0:
                    i1 = int(0)
                    i2 = int(len(self.lpfn)) if self.n == 1 else int(self.slicepos[i])
                    print('Finding first minmax within {},{}'.format(i1, i2))
                    ymax = max(self.lpfn[i1:i2])
                    xmax = np.where(self.lpfn == ymax)

                    ind1 = int(xmax[0])
                    xmax = photE[ind1]
                    self.ymax = np.append(self.ymax, ymax)
                    self.xmax = np.append(self.xmax, xmax)
                    
                elif i == self.n - 1:
                    i1 = int(self.slicepos[i-1])
                    i2 = int(len(self.lpfn))
                    ymax = max(self.lpfn[i1:i2])
                    xmax = np.where(self.lpfn == ymax)

                    ind1 = int(xmax[0])
                    xmax = photE[ind1]
                    self.ymax = np.append(self.ymax, ymax)
                    self.xmax = np.append(self.xmax, xmax)
                    
                else:
                    i1 = int(self.slicepos[i-1])
                    i2 = int(self.slicepos[i])

                    ymax = max(lpfn[i1:i2])
                    xmax = np.where(lpfn == ymax)

                    ind1 = int(xmax[0])
                    xmax = photE[ind1]
                    self.ymax = np.append(self.ymax, ymax)
                    self.xmax = np.append(self.xmax, xmax)

    def GetMax_x(self):
        return self.xmax
    def GetMax_y(self):
        return self.ymax
    def GetMin_x(self):
        return self.xmin
    def GetMin_y(self):
        return self.ymin            
