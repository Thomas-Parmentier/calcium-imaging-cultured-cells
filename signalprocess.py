#Takes a pandas data frame opened from .csv file, computes dF/F0 and smooths time series with exponential moving average
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy
import scipy.signal as signal
from scipy.signal import find_peaks
from scipy import stats

def dataframe(data, length, step, stim):
    flength=float(length)
    fstep=float(step)
    # remove background and calculate dF/Fzero
    bkg=data.iloc[:,1]
    measures=data.iloc[:,2:]
    mean_bkg=bkg.mean()
    measures_corrected=measures-mean_bkg
    if stim=="No":
        fzero=measures_corrected.min() #baseline fluorescence calculated as minimum
    else:
        fzero=measures_corrected.iloc[:50,:].mean(axis=0) #baseline fluorescence calculated over first 25 seconds
    final=(measures_corrected-fzero)/fzero

    #set column time as index
    time=np.arange(start=0, stop=flength, step=fstep)
    final.insert(0,"Time (s)",time)
    final2=final.set_index("Time (s)")

    #change name rows to Neuron1, Neuron2...
    column=list()
    for i in range (1,len(final2.columns)+1):
        column.append("Neuron"+ str(i))
    final3=final2.set_axis(column, axis=1)

    return final3
