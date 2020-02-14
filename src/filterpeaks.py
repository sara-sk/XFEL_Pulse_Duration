# Class for specifying further constraint on recording of peaks
import sys

from src.parameters import Parameters as p

class Filter_peaks:
    def __init__(self,data):
        self.data = data
        return None
    def filtered_peaks(self):
        return self.data
