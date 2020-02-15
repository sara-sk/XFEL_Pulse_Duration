import plotly
import plotly.graph_objects as go
import numpy as np
import sys
from src.main import Main
from src.peaksandsigmas import Peaks_and_Sigmas

# Class outputs table of the following data for all spectra in one dataset:
# - Name of the dataset
# - Number of spectra with given number of spikes
# - Average (rms)  spike widths for all single peak spectra
# - ___________________________________ double peak spectra
# - Overall rms spike width (weighted)

class All_Data:
    def __init__(self, intense, photE, dataset):

        # extract data from Main class
        fn = Main(intense,photE)
        number_of_peaks = fn.number_of_peaks
        avgsigma = fn.avgsigma
        characters = []
        number_of_spectra = []

        # Array for t2
        for i in range(int(max(number_of_peaks))):
            characters = np.append(characters, i)

        # Filling in array t2
        for i in range(1,int(max(number_of_peaks) + 1)):
            spectra = Peaks_and_Sigmas(number_of_peaks, avgsigma, photE, intense, np.array([i])).Spectra()
            number_of_spectra = np.append(number_of_spectra, spectra)
        ee = []
        for i in range(len(number_of_spectra)):
            e = (number_of_spectra[i] * (i + 1))
            ee = np.append(ee, e)
        avg_spike_number = np.sum(ee)/np.sum(number_of_spectra)
        number_of_spectra = np.array2string(number_of_spectra, separator=',',suppress_small=True)
        
        # Values for table
        t1 = dataset

        t2 = number_of_spectra # array with number of spectra with certain number of spikes
        t3 = Peaks_and_Sigmas(number_of_peaks, avgsigma, photE, intense, 
                np.array([1])).Overall_Average()                        # rms 1-spike width
        t4 = Peaks_and_Sigmas(number_of_peaks, avgsigma, photE, intense, 
                np.array([2])).Overall_Average()                        # rms 2-spike width
        t5 = Peaks_and_Sigmas(number_of_peaks, avgsigma, photE, intense, 
                characters).Overall_Average()                           # rms all spike widths
        t6 = avg_spike_number


        fig = go.Figure(data=[go.Table(header=dict(values=['Index', 'Value']), cells=dict(values=
            [['Dataset', '# of 1,2,.. spikes', 'single spike widths', '2-spike widths', 'overall spike widths','Average number of spikes in single spectrum'],
                [t1, t2, t3, t4, t5, t6]]))])
        fig.show()    
