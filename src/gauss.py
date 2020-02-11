# Class takes individual slices and approximates Gaussians to them
# Returns individual Gaussians and total added Gaussian
import sys
import numpy as np 
import matplotlib.pyplot as plt
import scipy as sp
from lmfit.models import GaussianModel

from src_visual.parameters import Parameters as p

class Gauss:
    def __init__(self, data, n):
        self.data = data
        self.sigmas = []
        self.n = n
        self.gaussResults = []
        
        
        if self.n == 1:
            peak = self.data
            mod = GaussianModel()
            pars = mod.guess(peak, x = p.x)
            out = mod.fit(peak, pars, x= p.x)
            gaussResult = out.best_fit
            self.gaussResults.append(gaussResult)
            self.sigmas.append(out.params['sigma'].value)
        
        if False:
            pass
        
        
        else:
            for i in range(len(self.data)):
                peak = self.data[i,:]
                mod = GaussianModel()
                pars = mod.guess(peak, x = p.x)
                out = mod.fit(peak, pars, x = p.x)
                gaussResult = out.best_fit

                # stacking Gaussians
                #if i == 0:
                self.gaussResults.append(gaussResult)
                #else:
                #    self.gaussResults = np.vstack((self.gaussResults,gaussResult))

                self.sigmas.append(out.params['sigma'].value)
                
        self.gaussResults = np.array(self.gaussResults)
        
    def IndivGaussians(self):
        return self.gaussResults
        
    def sigmas(self):
        return self.sigmas
        
    def Added_Gaussian(self):
        #if self.n == 1:
        #    GaussAdd = self.gaussResults
            
        #else:
        GaussAdd = []
        for o in range(len(self.gaussResults[0])):
            GaussAdd = np.append(GaussAdd, 0)
            for t in range(len(self.gaussResults[:,0])):
                GaussAdd[o] = GaussAdd[o] + self.gaussResults[t,o]
                    
        return GaussAdd
