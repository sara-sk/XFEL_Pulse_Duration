

class Parameters:
    pass

Parameters.heightcut = 10 # percentage height of max a peak must be
Parameters.prominence = 10 # percentage prominence required for peak
Parameters.nn_distance = 5
Parameters.alpha = 1.5
Parameters.beta = 1.5
Parameters.x = None

# Lowpass/backloop conditions
Parameters.deg = int(5) # lowpass function degree. Chosen by inspection.
Parameters.threshold = 10 # percentage overlap threshold for spectra to be sent through slow fit
Parameters.backloop_condition_slow = 5
Parameters.backloop_condition = 8 # percentage height difference between max of raw and max of lp function (maybe determine in terms of noise)
