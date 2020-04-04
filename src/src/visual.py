from __future__ import print_function
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets
import sys
import h5py
import numpy as np 
from src.parameters import Parameters as p
from src.peaksandsigmas import Peaks_and_Sigmas
from src.main import Main
from src.avgspectrum import Avg_Spectrum
from src.alldata import All_Data
from src.peaksandsigmasprinting import Peaks_and_Sigmas_Printing
def File(Input_file):
    # reading h5 file
    f = h5py.File(Input_file)
    photE = f.get("x-axis")
    intense = f.get("y-axis")
    spectrum = range(0,len(intense[1,:]-1)) # for parameter redefinition
    p.x = np.asarray(spectrum)
    '''
    fn = Main(intense,photE)
    
    def analysis(Input1):
        number_of_peaks = fn.number_of_peaks
        avgsigma = fn.avgsigma
        characters = []
        indices = []
        for i in range(len(Input1)):
            if Input1[i] == ',':
                pass
            elif Input1[i] == ' ':
                pass
            else:
                integer = int(Input1[i])
                characters = np.append(characters, integer)
        characters = characters.astype(int)
        return Peaks_and_Sigmas_Printing(number_of_peaks, avgsigma, photE, intense, characters)
    '''

    # button for plotting average spectrum
    button = widgets.Button(description="Plot avg spectrum")
    output = widgets.Output()
    display(button, output)

    def on_button_clicked(b):
        with output:
            return Avg_Spectrum(intense, photE)

    button.on_click(on_button_clicked)

    # button for analysing data
    button2 = widgets.Button(description = "Full data table")
    output2 = widgets.Output()
    display(button2, output2)
    def on_button_clicked2(b):
        with output2:
            return All_Data(intense, photE, Input_file)
    button2.on_click(on_button_clicked2)
    
    #print("For analysis on specific spectra types, input spike numbers separated by a comma. Maximum number of peaks is", max(fn.number_of_peaks))
    #interact(analysis, Input1 = '1')
