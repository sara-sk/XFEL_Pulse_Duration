import sys
import numpy as np 
import matplotlib.pyplot as plt
import scipy as sp

from src.parameters import Parameters as p

class Slice:
    def __init__(self, data, peaks, nofpeaks):
        assert nofpeaks > 0
        
        self.peaks = peaks
        self.data = data
        self.xpeaks = peaks 
        self.minima = []
        self.nofpeaks = nofpeaks
        self.Slices = []
        for j in range(self.nofpeaks-1):
            # Compute x-indices of all minima by which we slice
            peak1 = self.xpeaks[j]
            peak2 = self.xpeaks[j+1]
            Min_y = min(data[peak1:peak2])
            Min_x = np.asarray(np.where(self.data == Min_y))
            self.minima = np.append(self.minima, Min_x)      
    
        # To make following loop easier, include zeroth and last index of spectrum
        zero = np.insert(self.minima, 0, 0)
        self.minima_indices = np.append(zero, len(self.data))
        
        # Actually slicing, filling zeros where out of slice bounds
        for k in range(self.nofpeaks):
            if k == 0:
                index0 = self.minima_indices[k]
                index1 = self.xpeaks[k]/2
                index2 = self.minima_indices[k+1]
                single_slice = self.data[int(index1):int(index2)]
                for n in range(int(index0),int(index1)):
                    single_slice = np.insert(single_slice, 0, 0)
                for n in range(int(index2), len(self.data)):
                    single_slice = np.append(single_slice, 0)
                self.Slices.append(single_slice)
                
            elif k == len(self.peaks)-1:
                index1 = self.minima_indices[k]
                index2 = self.xpeaks[k] + (len(self.data)-self.xpeaks[k])/2
                index0 = self.minima_indices[k+1]
                single_slice = self.data[int(index1):int(index2)]  
                for n in range(0,int(index1)):
                    single_slice = np.insert(single_slice, 0, 0)   
                for n in range(int(index2), int(index0)):
                    single_slice = np.append(single_slice, 0)  
                #self.Slices = np.vstack((self.Slices,single_slice))
                self.Slices.append(single_slice)
                
            else:
                single_slice = self.data[int(self.minima_indices[k]):int(self.minima_indices[k+1])]
                for n in range(0,int(self.minima_indices[k])):
                    single_slice = np.insert(single_slice, 0, 0)
                for n in range(int(self.minima_indices[k+1]), len(self.data)):
                    single_slice = np.append(single_slice, 0)
                #self.Slices = np.vstack((self.Slices,single_slice))
                self.Slices.append(single_slice)
            """
            # Visual module
            print("plotting single slices")
            plt.plot(single_slice)
            plt.show()
            """
                
        self.Slices = np.array(self.Slices)
        
    def SlicingPoints(self):
        return self.minima
    def slices(self):
        return self.Slices
