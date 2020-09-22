#plots time series
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy
import scipy.signal as signal
from scipy.signal import find_peaks
from scipy import stats
import math

import scalebar

def calciumplot(data, numplots, length, step):
    max=data.max() #finds max of each row and creates a series of all maximums
    maximum=max.max() #finds maximum in that series
    flength=float(length)
    fstep=float(step)
    time=np.arange(start=0, stop=flength, step=fstep)
    fig,ax=plt.subplots(nrows=int(numplots), sharex=True, sharey=True)
    colors=plt.rcParams["axes.prop_cycle"]()
    for i in range(0,int(numplots)):
        c=next(colors)["color"]
        ax[i].set_xticks(range(0,200,30))
        ax[i].set_xlim([0,180])
        ax[i].set_yticks(range(0,math.ceil(maximum)))
        ax[i].set_ylim([-0.5,math.ceil(maximum)])
        ax[i].plot(time, data.iloc[:,i], color=c)
        c=next(colors)["color"]
        #ax[i].plot(time, filterdata.iloc[:,i+1], color=c)
        #ax[i].plot(peaks[str(column[i+1])][0],peaks[str(column[i+1])][1], "x") #put an x at location of peak
        scalebar.add_scalebar(ax[i])
    plt.show()
    return fig, ax
