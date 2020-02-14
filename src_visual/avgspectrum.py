import numpy as np
import sys
import matplotlib.pyplot as plt
from src_visual.parameters import Parameters as p
# Plots the average spectrum of entire dataset
class Avg_Spectrum:
    def __init__(self, data, photE):
        summed = []
        spectrum = range(0,len(data-1))
        for i in spectrum:
            summed = np.append(summed,np.average(data[0][i]))
        plt.plot(photE, summed, label = "Average spectrum")
        plt.legend()
