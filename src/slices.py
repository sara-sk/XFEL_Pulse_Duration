import sys
import numpy as np 
import matplotlib.pyplot as plt
import scipy as sp

from src.parameters import Parameters as p

# Class slices lowpass function by local minima, prepares slices to be approximated by Gaussians

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
    
        # Add beginning and end of spectrum to minima by which we slice
        zero = np.insert(self.minima, 0, 0)
        self.minima_indices = np.append(zero, len(self.data))
        
        # Actually slicing, filling zeros where out of slice bounds

        if self.nofpeaks == 1:
            # In case of a single peak, we want to be careful with where we slice
            index0 = self.minima_indices[0]
            index4 = self.minima_indices[1]

            # Module for cutting single peaks at twice FWHM
            '''
            # calculating fwhm to define indices of actual peak
            halfMax = max(self.data)/2
            max_x = np.where(self.data == max(self.data))
            max_x = int(max_x[0])
            data1 = data[0:int(max_x)]
            data2 = data[int(max_x):len(self.data)-1]

            a = abs(np.subtract(data1, halfMax))
            indy1  = min(a)
            indx1 = np.where(indy1 == a)[0]

            b = abs(np.subtract(data2, halfMax))

            indy2 = min(b)
            ind2 = np.where(indy2 == b)[0]
            indx2 = max_x + ind2

            #print(indx1,indx2)

            halfwidth = indx2 - indx1

           # print(halfwidth)
            index1 = max_x - halfwidth
            index2 = max_x + halfwidth

            #print(index1)

            '''

            # Module for cutting single peaks at halfway between peak max and beginning/end of spectrum
            
            max_x = np.where(self.data == max(self.data))[0]
            print(max_x)
            max_x = int(max_x)
            index1 = max_x/2
            index2 = max_x + (index4 - max_x)/2
    

            single_slice = self.data[int(index1):int(index2)]

            for n in range(int(index0),int(index1)):
                single_slice = np.insert(single_slice, 0, 0)
            for n in range(int(index2),int(index4)):
                single_slice = np.append(single_slice, 0)
            self.Slices.append(single_slice)

        # For multiple peak spectra
        # Edge peaks cut at half distance between peak max and spectrum ultimata
        # Appending zeros elsewhere
        else:
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
