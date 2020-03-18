import sys
import numpy as np 
import matplotlib.pyplot as plt
import scipy as sp
from scipy.signal import butter
from scipy.optimize import curve_fit
from scipy import signal
from src.peakfinder import Peakfinder
from src.slices import Slice
from src.gauss import Gauss
from src.maxmin import MaxMin
from src.filterpeaks import Filter_peaks

from src.parameters import Parameters as p

# Class for fitting lowpass function and approximating Gaussians to raw data.
# Originally named slow fit because of the adaptive cutoff parameter for each spectrum.

class Slow_Fit:
    def __init__(self, lowpassdata,photE):
        self.lowpassdata = lowpassdata
        
        # Fitting lowpass function, adjusting for both r2 value between points and for smoothness
        # Starting with ultra-low cutoff.
        lpcutoff = 0.0001

        while True:
            # fitting lowpass function
            b, a = signal.butter(p.deg, lpcutoff, 'low')
            self.spec = signal.filtfilt(b, a, self.lowpassdata)
                                  
            # Visual module for checking
            #plt.plot(photE,self.spec, label='Lowpass function')
            #plt.plot(photE,self.lowpassdata, label='Raw data')
            #plt.title("Typical XFEL energy spectru")
            #plt.xlabel("Energy (eV)")
            #plt.ylabel("Intensity (arbitrary)")
            #plt.legend()
            #plt.show()
            

            # condition for good fitting based on vertical distance between maxima of raw and lowpass dataset
            # if not fitted within backloop_condition, increment until good fit
            self.height_difference = abs(max(self.lowpassdata) - max(self.spec))

            # r2 value
            # parameters alpha and beta are tunable in parameter class
            r2 = (p.alpha * np.sum((self.lowpassdata - self.spec)**2) 
                      - p.beta * np.sum((self.lowpassdata[:-1] - self.lowpassdata[1:])**2))
            # rd value
            rd = np.sqrt(r2 / len(photE))

            # backloop condition defined in parameter class
            if rd > p.backloop_condition_slow * max(self.lowpassdata)/100:
                lpcutoff = lpcutoff + 0.001            # increment arbitrarily chosen
            else:
                break
                 
        
        # shift spectrum
        self.lpfn = self.spec - min(self.spec)
        
        #for i in range(100):
            #self.lpfn[i] = 0.1 *  self.lpfn[100]

        # calculate noise
        self.noise = np.array([self.lowpassdata-self.spec]).T
        '''
        plt.plot(photE, self.lpfn, label = 'Smoothened data (shifted)')
        plt.plot(photE, self.lowpassdata, label = 'Raw data')
        plt.plot(photE, self.noise, label = 'Noise')
        plt.xlabel('Energy (eV)')
        plt.ylabel('Intensity (arbitrary)')
        plt.legend()
        plt.show()
        '''
        # Extracting peaks ([x-axis, y-axis]) - indexed to neutral.
        self.peaks = Peakfinder(self.lpfn,photE).peaks
        
        # Apply further constraints to peaks
        self.filteredpeaks = Filter_peaks(self.peaks).filtered_peaks()
                
        # Number of peaks, after filtering.
        self.n = len(self.filteredpeaks)
        
        fn = Slice(self.lpfn,self.filteredpeaks, self.n)
        
        # Slice into individual peak functions, sprectrum == 0 outside individual slice
        self.slices = fn.slices()
        
        # Approximate each slice with Gaussian functions
        self.fn1 = Gauss(self.slices, self.n)
        self.Gaussian = self.fn1.Added_Gaussian()       # Return added Gaussian
        self.IndivGauss = self.fn1.IndivGaussians()     # Return individual Gaussians
        
        slicepos = fn.SlicingPoints()                   # Used to find minima
        
        if True:

            self.fn2 = MaxMin(self.IndivGauss,self.n, slicepos, self.lpfn, photE)
            ''' 
            plt.plot(photE, self.Gaussian, label="Summed Gaussian")
        
            for i in range(self.IndivGauss.shape[0]):
                plt.plot(photE, self.IndivGauss[i],'--',markersize = 0.1, label="Single gaussian")
            plt.plot(photE, self.lpfn, label = "Shifted smoothened spectrum")
            plt.plot(photE, self.lowpassdata)
            #plt.plot(photE, lowpassdata, label = "Raw data")
        
        
            plt.plot(self.fn2.GetMax_x(),self.fn2.GetMax_y(), 'go')
            if self.n != 1:
                plt.plot(self.fn2.GetMin_x(),self.fn2.GetMin_y(), 'ro')
            plt.xlabel('Energy (eV)')
            plt.ylabel('Intensity')
            plt.legend()
            plt.show()
            '''
        # Checking for significant overlap, definded by p.threshold
        minima = slicepos
        self.u = 0
        sig = self.fn1.sigmas
        ampl = self.fn1.ampl()
        center = self.fn1.center()
        a = 0
        if True:

            for i in range(len(minima)):
                index = int(minima[i])
                diff = self.Gaussian[index]-self.lpfn[index]
                if (abs(diff)*100/max(self.lpfn)) > p.threshold and self.u == 0:
                    a = 1
                else:
                    pass
            if a > 0:
                for i in range(len(minima)):

                    G1 = self.IndivGauss[i]
                    G2 = self.IndivGauss[i+1]
                    sig1 = sig[i]
                    sig2 = sig[i + 1]
                    ampl1 = ampl[i]
                    ampl2 = ampl[i + 1]
                    center1 = center[i]
                    center2 = center[i + 1]
                    #slicepos = minima
                    if self.u == 0:
                        self.arr = np.array([diff, G1, G2, self.lpfn, sig1, sig2, minima[i], ampl1, ampl2, center1, center2, self.n])
                    else:
                        array = np.array([diff, G1, G2, self.lpfn, sig1, sig2, minima[i], ampl1, ampl2, center1, center2, self.n])
                        self.arr = np.vstack((self.arr, array))

                    self.u = self.u + 1
                #self.ind = np.append(self.ind, i+1)
        
        # getting sigmas squared, taking the root mean
        #sig = self.fn1.sigmas
        self.sig = np.array(np.sqrt((np.average(sig))))
        self.r2 = float(np.sum((self.lpfn - self.Gaussian)**2))
    def U(self):
        return self.u
    def Arr(self):
        return self.arr
    def r2(self):
        return self.r2
   # def Ind(self):
        #return self.ind
    def lpfn(self):
        return self.lpfn
    def gauss(self):
        return self.Gaussian
    def indiv(self):
        return self.IndivGauss
    def nofpeaks(self):
        return self.n
    def avg_sigmas(self):
        return self.sig
