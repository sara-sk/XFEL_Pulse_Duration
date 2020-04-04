import numpy as np
import sys
import matplotlib.pyplot as plt
from src.parameters import Parameters as p

# Plots the average spectrum of entire dataset
class Avg_Spectrum:
    def __init__(self, data, photE):
        self.summed = []
        spectrum = range(0,len(data[1,:]-1))
        for i in spectrum:
            self.summed = np.append(self.summed,np.average(data[:,i]))
        plt.plot(photE, self.summed, label = "Average spectrum")
        plt.legend()
