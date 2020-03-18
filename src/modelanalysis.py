import numpy as np
import sys
import plotly
from src.parameters import Parameters as p
import plotly.graph_objects as go
import  matplotlib.pyplot as plt 
class Model_Analysis:
    def __init__(self, inputs):
        nofoverlaps = inputs[0]
        diffs = inputs[1]
        time = inputs[4]
        r2old = inputs[2]
        r2new = inputs[3]
        overlap_times = inputs[5]
        r2s = inputs[6]
        avg_overlap_time = np.average(overlap_times)
        print(type(r2old), r2old)
        a = 0
        print("time taken in minutes", time)
        for i in range(len(diffs)):
            if diffs[i]*100 > p.threshold:
                a = a + 1
        #print(diffs)
        #print(p.threshold)
        print("Number of peaks still not under threshold:", a)
        print("percentage:", a*100/nofoverlaps)
        print("Average overlap time:", avg_overlap_time, "seconds")
        print("Average r2 value:", np.average(r2s))
