import numpy as np
import sys
from src.parameters import Parameters as p
import matplotlib.pyplot as plt
from lmfit.models import GaussianModel
class Overlap_Fit:
    def __init__(self, overlaps, photE):
        # Works only for one overlap

        self.diff = overlaps[0]
        self.g1 = overlaps[1]
        self.g2 = overlaps[2]
        self.lpfn = overlaps[3]
        sig1 = overlaps[4]
        self.sig1 = np.sqrt(sig1)
        sig2 = overlaps[5]
        self.sig2 = np.sqrt(sig2)
        self.slicepos = int(overlaps[6])
        self.ampl = overlaps[7]
        self.center = overlaps[8]
        counter = 0
        while True:

            if self.diff > 0:
                incr = 0.99
            else:
                incr = 1.01
            

            self.sig1 = self.sig1*incr
            self.sig2 = self.sig2*incr
            self.ampl[0] = self.ampl[0]*incr
            self.ampl[1] = self.ampl[1] * incr
            gnew = []
            for i in range(len(photE)):
                G1 = (self.ampl[0] / (self.sig1 * np.sqrt(2*np.pi))) * np.exp(-(i-self.center[0])**2/(2 * self.sig1 **2))
                G2 = (self.ampl[1] / (self.sig2 * np.sqrt(2*np.pi))) * np.exp(-(i-self.center[1])**2/(2 * self.sig2 **2))
                add = G1 + G2
                gnew.append(add)
            newmin = int(np.where(min(gnew[int(self.center[0]):int(self.center[1])]) == gnew)[0])
            print(newmin)

            if counter == 0:
                old_diff = abs(gnew[newmin] - self.lpfn[self.slicepos]) + 1
                counter = counter + 1
            else: 
                old_diff = diff
            diff = abs(gnew[newmin] - self.lpfn[self.slicepos])
            if diff > old_diff:
                break
            #print(counter)

            plt.plot(photE,gnew, label="new one")
            plt.plot(photE, np.add(self.g1,self.g2))
            plt.plot(photE,self.lpfn)
            plt.plot(photE[self.slicepos], self.lpfn[self.slicepos], 'ro')
            plt.plot(photE[newmin],gnew[newmin],'go')
            plt.legend()
            plt.show()
        return None
