# Can put further constraints in this class
import sys
import h5py
import glob
import numpy as np 
from numpy import random
import matplotlib.pyplot as plt
from scipy import signal
import scipy as sp
from scipy.signal import butter
from scipy.optimize import curve_fit
from lmfit.models import GaussianModel
import time
import random

from src.parameters import Parameters as p

class Filter_peaks:
    def __init__(self,data):
        self.data = data
        return None
    def filtered_peaks(self):
        return self.data
