import sys
import numpy as np 
from numpy import random
import matplotlib.pyplot as plt
from scipy import signal
import scipy as sp
from scipy.signal import butter
import random

from src.parameters import Parameters as k


# Trialling lowpass function for random spectra to find optimal cutoff
# Indexed neutrally (i.e. not by energy)

# This is a simple backloop, which takes into account only height difference of dataset maxima. It assumes a low cutoff, and increases this until fit seems appropriate.
# Should the cutoff found give rise to overfitting, send through slow fit for which backloop also takes into account overfitting.

class Fast_Backloop:
    def __init__(self, intense):
        cutoffs = []
        # finding appropriate cutoff for 4 spectra within dataset
        for i in range(4):

            p = random.randrange(0, len(intense[:,1]), 1) # finding random spectrum to use
            
            
            self.lowpassdata = intense[p,:]
            lpcutoff = 0.001                         # starting at low cutoff (a sure underfit)
            n = 0

            while True:
                # fitting lowpass function with given cutoff
                b, a = signal.butter(k.deg, lpcutoff, 'low')
                self.lpfn = signal.filtfilt(b, a, self.lowpassdata)
                
                # Visual module for checking
                """plt.plot(self.lpfn, label='lowpass')
                plt.plot(self.lowpassdata, label='raw data')
                plt.legend()
                plt.show()"""

                # condition for good fitting based on vertical distance between maxima of raw and lowpass dataset
                # if not fitted within backloop_condition, increment until good fit
                self.height_difference = abs(max(self.lowpassdata) - max(self.lpfn))
                if self.height_difference > k.backloop_condition * max(self.lowpassdata)/100:
                    lpcutoff = lpcutoff + 0.005                                                     # arbitrarily chosen increment - high enough for efficiency
                else:
                    break

            cutoffs = np.append(cutoffs, lpcutoff)
        
        # Finding average of cutoffs to 4 decimal points
        self.avg_cutoff = "%.4f" % np.average(cutoffs)
        print("Average cutoff for dataset:", self.avg_cutoff)
        return None
    # cutoff fed to fastfit function
    def cutoff(self):
        return self.avg_cutoff
