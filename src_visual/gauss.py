import sys
import numpy as np 
import matplotlib.pyplot as plt
import scipy as sp
from lmfit.models import GaussianModel

from src_visual.parameters import Parameters as p

# Class for approximating Gaussian functions to individual slices

class Gauss:
    def __init__(self, data, n):
        self.data = data        # stacked individual slices
        self.sigmas = []
        self.n = n              # number of peaks
        self.gaussResults = []
        
        if False:
            pass
        
        else:
            print("Approximating Gaussians to individual peaks")
            # Model from lmfit package
            for i in range(len(self.data)):
                peak = self.data[i,:]
                mod = GaussianModel()
                pars = mod.guess(peak, x = p.x)
                out = mod.fit(peak, pars, x = p.x)
                gaussResult = out.best_fit

                # stacking Gaussians for each slice
                self.gaussResults.append(gaussResult)

                # sigma squared value
                self.sigmas.append(out.params['sigma'].value **2 )
                
        self.gaussResults = np.array(self.gaussResults)
        
    def IndivGaussians(self):
        return self.gaussResults
        
    def sigmas(self):
        return self.sigmas
        
    def Added_Gaussian(self):
        GaussAdd = []
        for o in range(len(self.gaussResults[0])):
            GaussAdd = np.append(GaussAdd, 0)
            for t in range(len(self.gaussResults[:,0])):
                GaussAdd[o] = GaussAdd[o] + self.gaussResults[t,o]
                    
        return GaussAdd
