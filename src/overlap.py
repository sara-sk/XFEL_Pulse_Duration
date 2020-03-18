import numpy as np
import sys
from src.parameters import Parameters as p
import matplotlib.pyplot as plt
from lmfit.models import GaussianModel
class Overlap_Fit:
    def __init__(self, overlaps, photE, n):
        # Works only for one overlap
        self.n = int(n)
        if self.n == 2:
            #print("1")
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

            #print(self.n)
            counter = 0
            while True:
                if self.diff > 0:
                    incr = 0.99
                else:
                    incr = 1.01
            

                self.sig1 = self.sig1*incr
                self.sig2 = self.sig2*incr
                self.ampl1 = self.ampl1*incr
                self.ampl2 = self.ampl2 * incr
                gnew = []
                for i in range(len(photE)):
                    G1 = (self.ampl1 / (self.sig1 * np.sqrt(2*np.pi))) * np.exp(-(i-self.center1)**2/(2 * self.sig1 **2))
                    G2 = (self.ampl2 / (self.sig2 * np.sqrt(2*np.pi))) * np.exp(-(i-self.center2)**2/(2 * self.sig2 **2))
                    add = G1 + G2
                    gnew.append(add)
                newmin = np.where(min(gnew[int(self.center1):int(self.center2)]) == gnew)[0]
                '''print(type(newmin))
                print(newmin)
                plt.plot(gnew)
                plt.show()
                '''
                newmin = int(newmin)
            #print(newmin)

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
                #print(diff)
                if diff > old_diff:
                    break
                if counter > 10:
                    if r2 > old_r2*1.2:
                        break 
            #print(r2)
            #print(counter)
            '''
            print("New Overlapping Spectrum")
            print("Number of peaks:",self.n)
            print("Old sigmas:", np.sqrt(sig1), np.sqrt(sig2))
            print("New sigmas:", self.sig1, self.sig2)
            
            plt.plot(photE,gnew, label="Adjusted added Gaussian")
            plt.plot(photE, np.add(self.g1,self.g2), ':',label = "Original Gaussian")
            plt.plot(photE,self.lpfn, label = "Lowpass function")
            #plt.plot(photE[self.slicepos], self.lpfn[self.slicepos], 'ro')
            #plt.plot(photE[newmin],gnew[newmin],'go')
            plt.legend()
            plt.show()
            '''
            self.sigmas = np.array(self.sig1, self.sig2)

            self.diff = old_diff/max(self.lpfn)
            #self.r2old = np.sum((self.lpfn - added_old_gauss)**2)
            self.r2old = np.sum((self.lpfn - gold)**2)
            self.r2new = np.sum((self.lpfn - gnew)**2)

        else:
            #print("2")
            self.lpfn = overlaps[0,3]
            #self.slicepos = overlaps[0,6]

            differences = []
            gaussians = []
            sigmas = []
            amplitudes = []
            centers = []
            slicepos = []

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

            avgdiff = abs(np.average(differences))
            oldsig = np.asarray(sigmas)
            sigmas = np.asarray(sigmas)
            amplitudes = np.asarray(amplitudes)
            centers = np.asarray(centers)
            
            differs = []
            for i in range(len(overlaps)):
                differs.append(abs(differences[i]))
            diffsum = np.sum(differs)

            #oldsig = sigmas
            #print(oldsig)
            added_old_gauss = gaussians[0]
            for i in range(1,len(gaussians)):
                added_old_gauss = np.add(added_old_gauss, gaussians[i])
            #print(amplitudes)
            ''' 
            for i in range(len(overlaps)-1):
                weighted_diff1 = differences[i] / avgdiff
                weighted_diff2 = differences[i] + differences[i + 1] / (avgdiff * 2)
                weighted_diff3 = differences[i + 1] / avgdiff

                if weighted_diff1 > 0:
                    incr1 = 0.99 * abs(weighted_diff1)
                else:
                    incr1 = 1.01 * abs(weighted_diff1)

                if weighted_diff2 > 0:
                    incr2 = 0.99 * abs(weighted_diff2)
                else:self
                    incr2 = 0.99 * abs(weighted_diff2)

                if weighted_diff3 > 0:
                    incr3 = 0.99 * abs(weighted_diff3)
                else:
                    incr3 = 1.01 * abs(weighted_diff3)

                if i == 0:
                    sigmas[i] = sigmas[i] * incr1
                    amplitudes[i] = amplitudes[i] * incr1

                if i == len(overlaps)-1:
                    sigmas[i + 2] = sigmas[i + 2] * incr3
                    amplitudes[i+2] = amplitudes[i+2] * incr3

                sigmas[i + 1] = sigmas[i + 1] * incr2
                amplitudes[i + 1] = amplitudes[i + 1] * incr2
            '''
            counter = 0
            #diffs = []
            while True:
                diffs = []
                Min = []
                for i in range(len(overlaps)-1):
                    #factor = abs(differences[i]/diffsum)
                    if differences[i] > 0:
                        incr = 0.99 #* factor
                    else:
                        incr = 1.01 #* factor
                    sigmas[i] = sigmas[i] * incr #* factor
                    amplitudes[i] = amplitudes[i] * incr #* factor
                    sigmas[i+1] = sigmas[i+1] * incr #* factor
                    amplitudes[i + 1] = amplitudes[i + 1] *incr #* factor
                    '''
                    if i == len(overlaps) - 1:
                        sigmas[i + 1] = sigmas[i + 1] * incr 
                        amplitudes[i + 1] = amplitudes[i + 1] * incr
                    '''
                for i in range(self.n):
                    #print(amplitudes[i],sigmas[i])
                    gnew = []
                    for j in range(len(photE)):
                        #g = (amplitudes[i] / (sigmas[i] * np.sqrt(2*np.pi))) * np.exp(-(j-centers[i])**2/(2 * sigmas[i]**2))
                        g = (amplitudes[i] / (sigmas[i] * np.sqrt(2*np.pi))) * np.exp(-(j-centers[i])**2/(2 * sigmas[i] **2))
                        gnew.append(g)
                    #plt.plot(photE, gnew)
                    if i == 0:
                        self.gold = gnew
                    else:
                        self.gold = np.add(self.gold, gnew)
                for i in range(self.n - 1):
                    #print(slicepos)
                    Minim = np.where(min(self.gold[int(centers[i]):int(centers[i + 1])]) == self.gold)[0]
                    Minim = int(Minim)

                    Min.append(Minim)
                    diff = abs(self.gold[Minim] - self.lpfn[int(slicepos[i])])
                    diffs.append(diff)
                if counter == 0:
                    old_avgdiff = np.average(diffs) + 1
                    counter = counter + 1
                else:
                    old_avgdiff = avgdiff
                avgdiff = np.average(diffs)
                #print(avgdiff)
                if avgdiff > old_avgdiff:
                    break
            '''
            print("New Overlapping Spectrum")
            print("Number of peaks:", self.n)
            print("Old sigmas:", oldsig)
            print("New sigmas:", sigmas)
            
            plt.plot(photE, self.gold, label = "Adjusted Gaussian")
            plt.plot(photE, self.lpfn, label = "Lowpass function")
            plt.plot(photE, added_old_gauss, ':', label = "Old Gaussian")
            plt.legend()
                #for i in range(len(slicepos)):
                    #plt.plot(photE[int(slicepos[i])], self.lpfn[int(slicepos[i])], 'ro')
                    #plt.plot(photE[Min[i]],self.gold[Min[i]],'go')
            plt.show()
            '''
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
