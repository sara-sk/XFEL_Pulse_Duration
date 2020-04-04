import numpy as np
import sys
import plotly
from src.parameters import Parameters as p
import plotly.graph_objects as go
import  matplotlib.pyplot as plt 

##############
# Class for analysing effectiveness of model. Change True condition to False to print analysis on the interface screen
##############


class Model_Analysis:
    def __init__(self, inputs):

        if True:
            pass
        else:
            nofoverlaps = inputs[0]
            diffs = inputs[1]
            time = inputs[4]
            r2old = inputs[2]
            r2new = inputs[3]
            overlap_times = inputs[5]
            r2s = inputs[6]
            nofspectra = inputs[7]
            avg_overlap_time = np.average(overlap_times)
            a = 0

            # output time taken
            print("time taken in minutes", time)

            # count number of spectra still not fitted by the overlap procedure
            for i in range(len(diffs)):
                if diffs[i]*100 > p.threshold:
                    a = a + 1
            
            print("Number of peaks still not under threshold:", a)
            if nofoverlaps > 0:
                print("percentage:", a*100/nofoverlaps)
            print("Average overlap time:", avg_overlap_time, "seconds")
            print("Average new r2 value:", np.average(r2s))
            print("Average old r2 value:", np.average(r2old))
        
