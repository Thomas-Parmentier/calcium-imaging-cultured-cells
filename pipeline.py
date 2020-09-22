#goes through the whole pipeline of calcium imaging
from signalprocess import dataframe
import findpeaks
import plot
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy

fh=input("Enter file name: ")
file=fh+".csv"
data=pd.read_csv(file) #open csv file

length=input('length of recording in seconds: ')
step=input('Image interval in seconds: ')
stimulation=input('stimulation applied Yes or No?: ')


normdata=dataframe(data, length, step, stimulation)
print(normdata)
h=input("Enter height threshold peaks: ")
p=input("Enter prominence threshold peaks: ")

acell, nonacell, listacell, numpeaks=findpeaks.findpeaks(normdata, float(h), float(p), length)

numplots=input("How many plots would you like?: ")
fig, ax= plot.calciumplot(normdata, numplots, length, step)

out=input('Enter processed file name: ')
savename=out+"-processed.csv"
normdata.to_csv(savename, index=True) #exports final datasheet into csv file without the extra first column
print("done")
