import sys
import numpy as np
from src_visual.parameters import Parameters as p

# Class for returning average sigma and number of spectra with given number of peaks, for data analysis
# Both average and number of spectra are indexed by number of spikes in spectra
# i.e. single-peak spectra counted into index 1, double peak to index 2 etc.

class Peaks_and_Sigmas:
    def __init__(self, number_of_peaks, avgsigma, photE, intense, array):
        self.corr = (max(photE)-min(photE))/len(intense)
        self.number_of_peaks = number_of_peaks
        self.avgsigma = avgsigma
        self.photE = photE
        self.intense = intense
        self.array = array # Array to be entered with the peak numbers of interest

        avg_sigmas = []
        counts = []
        for i in range(int(self.number_of_peaks)+1):
            avg_sigmas = np.append(avg_sigmas, 0)
            counts = np.append(counts, 0)
        
        for i in range(1):
            index = int(self.number_of_peaks)
            counts[index] = counts[index] + 1
            avg_sigmas = avg_sigmas + self.avgsigma*self.corr

        for i in range(len(avg_sigmas)):
            if counts[i] == 0:
                avg_sigmas[i] = 0
            else:
                avg_sigmas[i] = avg_sigmas[i]/counts[i]
        
        self.out_data = [0, 0, 0]
        for i in range(len(self.array)):
            index = self.array[i]
            index = int(index)
            peaks = counts[index - 1] 
            table = np.array([index, counts[index], avg_sigmas[index]])
            self.out_data = np.vstack((self.out_data, table))
        
        self.spectra = np.sum(self.out_data[:,1])
        weighted_avg = []
        for i in range(len(self.out_data)):
            weight = self.out_data[i,1]/self.spectra
            ave = weight * self.out_data[i,2]
            weighted_avg = np.append(weighted_avg, ave)
        
        self.overall_average = np.sum(weighted_avg)
        
      #  print("Average sigma for all input spectra:", overall_average)
      #  print("Number of spectra:", spectra)
        
    # Stacks arrays to return one dataset with all data
    def Returns(self):
        return self.out_data
    def Spectra(self):
        return self.spectra
    def Overall_Average(self):
        return self.overall_average
