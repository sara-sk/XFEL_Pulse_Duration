import numpy as np
import sys
from src.parameters import Parameters as p
import matplotlib.pyplot as plt
from lmfit.models import GaussianModel

######################
# Class treats overlapping spikes
######################


class Overlap_Fit:
    def __init__(self, overlaps, photE, n):
        self.n = int(n)

        # Distinguish case of 1 or multiple overlaps
        if self.n == 2:
            self.diff = overlaps[0]
            self.g1 = overlaps[1]
            self.g2 = overlaps[2]
            self.lpfn = overlaps[3]
            sig1 = overlaps[4]
            self.sig1 = np.sqrt(sig1)
            sig2 = overlaps[5]
            self.sig2 = np.sqrt(sig2)
            self.slicepos = int(overlaps[6])
            self.ampl1 = overlaps[7]
            self.ampl2 = overlaps[8]
            self.center1 = overlaps[9]
            self.center2 = overlaps[10]
            counter = 0

            while True:
                # Distinguish case of overlap or "under-lap" (i.e. summed Gaussian is less than lpfn)
                if self.diff > 0:
                    incr = 0.99
                else:
                    incr = 1.01

                # adjust sigmas and amplitudes of both spikes
                self.sig1 = self.sig1*incr
                self.sig2 = self.sig2*incr
                self.ampl1 = self.ampl1*incr
                self.ampl2 = self.ampl2 * incr
                gnew = []

                # generate Gaussian distributions with new sigma and amplitude
                for i in range(len(photE)):
                    G1 = (self.ampl1 / (self.sig1 * np.sqrt(2*np.pi))) * np.exp(-(i-self.center1)**2/(2 * self.sig1 **2))
                    G2 = (self.ampl2 / (self.sig2 * np.sqrt(2*np.pi))) * np.exp(-(i-self.center2)**2/(2 * self.sig2 **2))
                    add = G1 + G2
                    gnew.append(add)
                newmin = np.where(min(gnew[int(self.center1):int(self.center2)]) == gnew)[0]
                newmin = int(newmin)

                # save old and new Gaussians
                if counter == 0:
                    old_diff = abs(gnew[newmin] - self.lpfn[self.slicepos]) + 1
                    old_r2 = np.sum((self.lpfn - gnew))
                    gold = gnew
                    counter = counter + 1
                else: 
                    old_diff = diff
                    counter = counter + 1
                diff = abs(gnew[newmin] - self.lpfn[self.slicepos])
                r2 = np.sum((self.lpfn - gnew))

                # break if difference has reached a minimum OR if loop has been done more than 10 times and r2 value is significantly changed
                if diff > old_diff:
                    break
                if counter > 10:
                    if r2 > old_r2*1.2:
                        break 
            
            # save values
            self.sigmas = np.array(self.sig1, self.sig2)
            self.diff = old_diff/max(self.lpfn)
            self.r2old = np.sum((self.lpfn - gold)**2)
            self.r2new = np.sum((self.lpfn - gnew)**2)

        # case: multiple overlaps
        else:
            self.lpfn = overlaps[0,3]
            differences = []
            gaussians = []
            sigmas = []
            amplitudes = []
            centers = []
            slicepos = []

            # generate datasets
            for i in range(len(overlaps)):
                differences.append(overlaps[i,0])
                if i == 0:
                    gaussians.append(overlaps[i,1])
                else:
                    gaussians = np.vstack((gaussians, overlaps[i,1]))

                centers.append(overlaps[i,9])
                sigmas.append(np.sqrt(overlaps[i,4]))
                amplitudes.append(overlaps[i,7])
                slicepos.append(overlaps[i,6])

                if i == len(overlaps)-1:
                    gaussians = np.vstack((gaussians, overlaps[i,2]))
                    amplitudes.append(overlaps[i,8])
                    sigmas.append(np.sqrt(overlaps[i,5]))
                    centers.append(overlaps[i,10])

            # compute average difference between overlaps etc. to be able to factor in eventually
            avgdiff = abs(np.average(differences))
            oldsig = np.asarray(sigmas)
            sigmas = np.asarray(sigmas)
            amplitudes = np.asarray(amplitudes)
            centers = np.asarray(centers)
            
            differs = []
            for i in range(len(overlaps)):
                differs.append(abs(differences[i]))
            diffsum = np.sum(differs)

            added_old_gauss = gaussians[0]
            for i in range(1,len(gaussians)):
                added_old_gauss = np.add(added_old_gauss, gaussians[i])
            
            counter = 0

            # iteratively re-fit
            while True:
                diffs = []
                Min = []
                adj = 2

                # incremental factors depend on relative sizes of differences and whether previous spike has been widened or narrowed.
                # adjust sigmas and amplitudes according to computed factors
                for i in range(len(overlaps)+1):
                    if i == 0:
                        if differences[i] > 0:
                            incr = 0.99
                        else:
                            incr = 1.01
                        sigmas[i] = sigmas[i] * incr
                        amplitudes[i] = amplitudes[i] * incr

                    elif i == len(overlaps):
                        if differences[i-1] > 0:
                            incr = 0.99
                        else:
                            incr = 1.01
                        sigmas[i] = sigmas[i] * incr
                        amplitudes[i] = amplitudes[i] * incr

                    else:
                        d1 = differences[i-1]
                        d2 = differences[i]
                        if d1 > 0 and d2 > 0:
                            incr = 0.99
                        elif d2 < 0 and d2 < 0:
                            incr = 1.01
                        else:
                            d = d1 + d2
                            dabs = abs(d2) + abs(d1)
                            if d > 0:
                                incr = 1. - 0.01*d/dabs
                            else:
                                incr = 1. + 0.01*d/dabs
                        sigmas[i] = sigmas[i]*incr
                        amplitudes[i] = amplitudes[i] * incr
                
                # generate new Gaussian distributions
                for i in range(self.n):
                    gnew = []
                    for j in range(len(photE)):
                        g = (amplitudes[i] / (sigmas[i] * np.sqrt(2*np.pi))) * np.exp(-(j-centers[i])**2/(2 * sigmas[i] **2))
                        gnew.append(g)
                    if i == 0:
                        self.gold = gnew
                    else:
                        self.gold = np.add(self.gold, gnew)

                # compute new differences
                for i in range(self.n - 1):
                    Minim = np.where(min(self.gold[int(centers[i]):int(centers[i + 1])]) == self.gold)[0]
                    Minim = int(Minim)
                    Min.append(Minim)
                    diff = abs(self.gold[Minim] - self.lpfn[int(slicepos[i])])
                    diffs.append(diff)
                if counter == 0:
                    old_avgdiff = np.average(diffs) + 1
                    old_r2 = np.sum((self.lpfn - self.gold))
                    counter = counter + 1
                else:
                    old_avgdiff = avgdiff
                    counter = counter + 1
                avgdiff = np.average(diffs)
                r2 = np.sum((self.lpfn - self.gold))

                # break if adequately re-fit or loop has been performed too many times
                if avgdiff > old_avgdiff:
                    break
                if counter > 10:
                    if r2>old_r2*1.2:
                        break
            
            # save data
            self.sigmas = sigmas
            self.diff = avgdiff/max(self.lpfn)
            self.r2old = np.sum((self.lpfn - added_old_gauss)**2)
            self.r2new = np.sum((self.lpfn - self.gold)**2)

        return None

    def Get_Overlap_Fit(self):
        return self.gold
    def Get_New_Sigma(self):
        return np.sqrt(np.average(np.square(self.sigmas)))
    def diff(self):
        return self.diff
    def r2old(self):
        return self.r2old
    def r2new(self):
        return self.r2new
