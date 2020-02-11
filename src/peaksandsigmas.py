import sys
import numpy as np
from src_visual.parameters import Parameters as p


# Peak number takes form as an index, and two arrays are returned: one with number of spectra with given index,
# one with average sigma. Indices are the same for the two array.
# Index '0' is added for useability: index 1 refers to spectra with 1 peak, 2 to 2 etc.
class Peaks_and_Sigmas:
    def __init__(self, number_of_peaks, avgsigma, photE, intense, array):
        self.corr = (max(photE)-min(photE))/len(intense[1,:])
        self.number_of_peaks = number_of_peaks
        self.avgsigma = avgsigma
        self.photE = photE
        self.intense = intense
        self.array = array # Array to be entered with the peak numbers of interest

        avg_sigmas = []
        counts = []
        for i in range(int(max(self.number_of_peaks))+1):
            avg_sigmas = np.append(avg_sigmas, 0)
            counts = np.append(counts, 0)
        
        for i in range(len(self.number_of_peaks)):
            index = int(self.number_of_peaks[i])
            counts[index] = counts[index] + 1
            avg_sigmas[index] = avg_sigmas[index] + self.avgsigma[index]*self.corr

        for i in range(len(avg_sigmas)):
            if counts[i] == 0:
                avg_sigmas[i] = 0
            else:
                avg_sigmas[i] = avg_sigmas[i]/counts[i]
        
        self.out_data = [0, 0, 0]
        for i in range(len(self.array)):
            index = self.array[i]
            peaks = counts[index - 1] 
            table = np.array([index, counts[index], avg_sigmas[index]])
            self.out_data = np.vstack((self.out_data, table))
        
        spectra = np.sum(self.out_data[:,1])
        weighted_avg = []
        for i in range(len(self.out_data)):
            weight = self.out_data[i,1]/spectra
            ave = weight * self.out_data[i,2]
            weighted_avg = np.append(weighted_avg, ave)
        
        overall_average = np.sum(weighted_avg)
        
        print("Average sigma for all input spectra:", overall_average)
        print("Number of spectra:", spectra)
        
    # Stacks arrays to return one dataset with all data
    def Returns(self):
        return self.out_data
