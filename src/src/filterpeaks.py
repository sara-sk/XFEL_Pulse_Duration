###############################################################
# Class for specifying further constraint on recording of peaks
###############################################################
import sys
from src.parameters import Parameters as p

class Filter_peaks:

    # Set edge data to zero
    def __init__(self,data):
        for i in range(len(data)):
            if data[i] < 100 or data[i] > 2550:
                data[i] = 0
        self.data = data[data != 0]

    def filtered_peaks(self):
        return self.data
