import sys
import numpy as np 
import matplotlib.pyplot as plt

from src.parameters import Parameters as p

# Class for extracting local minima and maxima of lowpass functions based on found peaks
# Use only for visual demonstration

class MaxMin:
    def __init__(self, data, nofpeaks, slicepos, lpfn, photE):
        self.n = nofpeaks
        self.data = data
        self.slicepos = slicepos
        self.lpfn = lpfn
        
        if False:
            pass

        else:
            # Find local minima from slicing positions
            self.ymin = []
            self.xmin = []
            for j in range(len(slicepos)):
                ind2 = int(self.slicepos[j])
                ymin = self.lpfn[ind2]
                self.ymin = np.append(self.ymin, ymin)
                xmin = photE[self.slicepos[j]]
                self.xmin = np.append(self.xmin, xmin)
            
            # Find local maxima between local minima (in Gaussian), matching to lowpass function
            self.ymax = []
            self.xmax = []
            '''
            plt.plot(self.lpfn)
            plt.show()
            '''

            # Define indices differently for edge peaks
            for i in range(self.n):
                if i == 0:
                    i2 = int(len(self.lpfn)) if self.n == 1 else int(self.slicepos[i])
                    i1 = int(0)
                    #print('Finding first minmax within {},{}'.format(i1, i2))
                    ymax = max(self.lpfn[i1:i2])
                    xmax = np.where(self.lpfn == ymax)
                    ind1 = int(xmax[0])
                    if ind1 == 0:
                        i1 = int(0.3 * i2)
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
