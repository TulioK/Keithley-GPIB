## Imports
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
import os
cwd = os.getcwd()

## Getting a list of the folders with runs in them
folders =  glob("../runs/*/", recursive = True)
print(folders)

dataPaths = []
for n in folders: # Making a list of paths to all the data, so that it it easy to pick out which one to load
    dataPaths.append(n + "/data.csv")

def loadIV(number):
    result = np.genfromtxt(dataPaths[number], delimiter = ",",skip_header=1)
    bias = result[:,0]
    totalCurrent = result[:,1]
    padCurrent = result[:,2]
    return bias, totalCurrent, padCurrent

def loadCV(number):
    result = np.genfromtxt(dataPaths[number], delimiter=",", skip_header=1)
    voltage = result[:,0]
    capacitance = result[:,1]
    conductivity = result[:,2]
    bias = result[:,3]
    padCurrent = result[:,4]
    return bias, capacitance, padCurrent, voltage, conductivity


####################################################

bias, totalCurrent, padCurrent = loadIV(2)

plt.figure(1)
plt.plot(bias,totalCurrent, 'r', label="Total Current")
plt.plot(bias,padCurrent, 'b', label="Pad Current")
plt.title("IV curves")
plt.xlabel("Bias voltage (V)")
plt.ylabel("Current (nA)")
plt.legend()
#plt.show()
plt.close()

plt.figure(2)
B, C, I, V, R = loadCV(0)
plt.plot(B,C, label="10kHz")
B, C, I, V, R = loadCV(4)
plt.plot(B,C, label="7.5kHz")
B, C, I, V, R = loadCV(1)
plt.plot(B,C, label="5kHz")
B, C, I, V, R = loadCV(9)
plt.plot(B,C, label="2kHz")
plt.title("CV curve")
plt.xlabel("Bias voltage (V)")
plt.ylabel("Capacitance (F)")
plt.legend()
plt.show()
plt.close()

