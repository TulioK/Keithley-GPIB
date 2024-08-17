## Imports
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
import os
cwd = os.getcwd()

## Getting a list of the folders with runs in them
folders =  glob("9thJulyData/PPS_TILGAD_6 152 4 C1-V3-1TRB/*", recursive = True)
print(folders)

dataPaths = []
for n in folders: # Making a list of paths to all the data, so that it it easy to pick out which one to load
    dataPaths.append(n)



def loadIV(path):
    result = np.genfromtxt(path, delimiter = "\t",skip_header=67, skip_footer=1)
    bias = result[:,0]
    totalCurrent = result[:,1]
    padCurrent = result[:,2]
    return bias, totalCurrent, padCurrent


def loadCV(path):
    result = np.genfromtxt(path, delimiter="\t", skip_header=72, skip_footer=1)
    voltage = result[:,0]
    capacitance = result[:,1]
    conductivity = result[:,2]
    bias = result[:,3]
    padCurrent = result[:,4]
    return bias, capacitance, padCurrent, voltage, conductivity

print(dataPaths)
####################################################


## CV's at different temps
plt.figure(1)
b, c, t, v, g = loadCV("9thJulyData/PPS_TILGAD_6 152 4 C1-V3-1TRB/PPS_TILGAD_6 152 4 C1-V3-1TRB_2024-07-09_14.cv")
plt.plot(-b,1.0 / c**2, label = "-20C")
b, c, t, v, g = loadCV("9thJulyData/PPS_TILGAD_6 152 4 C1-V3-1TRB/PPS_TILGAD_6 152 4 C1-V3-1TRB_2024-07-09_11.cv")
plt.plot(-b,1.0 / c**2, label = "20C")
b, c, t, v, g = loadCV("9thJulyData/PPS_TILGAD_6 152 4 C1-V3-1TRB/PPS_TILGAD_6 152 4 C1-V3-1TRB_2024-07-09_10.cv")
plt.plot(-b,1.0 / c**2, label = "0C")
b, c, t, v, g = loadCV("9thJulyData/PPS_TILGAD_6 152 4 C1-V3-1TRB/PPS_TILGAD_6 152 4 C1-V3-1TRB_2024-07-09_8.cv")
plt.plot(-b[:-1],1.0 / c[:-1]**2, label = "-10C")

plt.minorticks_on()
plt.grid(True, which='both')
plt.grid(linestyle='dashed', linewidth=0.25, which="minor")
plt.title("CV curves @ 10kHz")
plt.xlabel("Bias voltage (V)")
plt.ylabel("1/C² (F⁻²)")
plt.legend()
#plt.show()
#plt.close()
plt.savefig("cvtemps.png")



## IVs at different temps
plt.figure(2)
b, t, p = loadIV("9thJulyData/PPS_TILGAD_6 152 4 C1-V3-1TRB/PPS_TILGAD_6 152 4 C1-V3-1TRB_2024-07-09_10.iv")
plt.plot(-b,-p, label = "-20C")
b, t, p = loadIV("9thJulyData/PPS_TILGAD_6 152 4 C1-V3-1TRB/PPS_TILGAD_6 152 4 C1-V3-1TRB_2024-07-09_8.iv")
plt.plot(-b,-p, label = "20C")
b, t, p = loadIV("9thJulyData/PPS_TILGAD_6 152 4 C1-V3-1TRB/PPS_TILGAD_6 152 4 C1-V3-1TRB_2024-07-09_7.iv")
plt.plot(-b,-p, label = "0C")
b, t, p = loadIV("9thJulyData/PPS_TILGAD_6 152 4 C1-V3-1TRB/PPS_TILGAD_6 152 4 C1-V3-1TRB_2024-07-09_6.iv")
plt.plot(-b,-p, label = "-10C")

plt.minorticks_on()
plt.grid(True, which='both')
plt.grid(linestyle='dashed', linewidth=0.25, which="minor")
plt.title("IV curves, pad current")
plt.xlabel("Bias voltage (V)")
plt.ylabel("Pad current (A)")
plt.legend()
#plt.show()
#plt.close()
plt.savefig("ivpadtemps.png")


## Zoomed in on the weird bump around the gain layer depletion
plt.figure(3)
b, t, p = loadIV("9thJulyData/PPS_TILGAD_6 152 4 C1-V3-1TRB/PPS_TILGAD_6 152 4 C1-V3-1TRB_2024-07-09_10.iv")
plt.plot(-b,-p, label = "-20C")
b, t, p = loadIV("9thJulyData/PPS_TILGAD_6 152 4 C1-V3-1TRB/PPS_TILGAD_6 152 4 C1-V3-1TRB_2024-07-09_8.iv")
plt.plot(-b,-p, label = "20C")
b, t, p = loadIV("9thJulyData/PPS_TILGAD_6 152 4 C1-V3-1TRB/PPS_TILGAD_6 152 4 C1-V3-1TRB_2024-07-09_7.iv")
plt.plot(-b,-p, label = "0C")
b, t, p = loadIV("9thJulyData/PPS_TILGAD_6 152 4 C1-V3-1TRB/PPS_TILGAD_6 152 4 C1-V3-1TRB_2024-07-09_6.iv")
plt.plot(-b,-p, label = "-10C")


plt.xlim(20,30)
plt.ylim(-0.5E-10, 0.5E-10)
plt.minorticks_on()
plt.grid(True, which='both')
plt.grid(linestyle='dashed', linewidth=0.25, which="minor")
plt.title("IV curves, pad current, gain depletion")
plt.xlabel("Bias voltage (V)")
plt.ylabel("Pad current (A)")
plt.legend()
#plt.show()
#plt.close()
plt.savefig("ivpadtempszoom.png")


## CV curves for all pixels at room temp
plt.figure(4)
b, c, t, v, g = loadCV("9thJulyData/PPS_TILGAD_6 152 4 C1-V3-1TRB/PPS_TILGAD_6 152 4 C1-V3-1TRB_2024-07-09_3.cv")
plt.plot(-b,1.0 / c**2, label = "Pixel 0,0")
b, c, t, v, g = loadCV("9thJulyData/PPS_TILGAD_6 152 4 C1-V3-1TRB/PPS_TILGAD_6 152 4 C1-V3-1TRB_2024-07-09_4.cv")
plt.plot(-b,1.0 / c**2, label = "Pixel 0,1")
b, c, t, v, g = loadCV("9thJulyData/PPS_TILGAD_6 152 4 C1-V3-1TRB/PPS_TILGAD_6 152 4 C1-V3-1TRB_2024-07-09_5.cv")
plt.plot(-b,1.0 / c**2, label = "Pixel 1,1")
b, c, t, v, g = loadCV("9thJulyData/PPS_TILGAD_6 152 4 C1-V3-1TRB/PPS_TILGAD_6 152 4 C1-V3-1TRB_2024-07-09_6.cv")
plt.plot(-b[:-1],1.0 / c[:-1]**2, label = "Pixel 1,0")

plt.minorticks_on()
plt.grid(True, which='both')
plt.grid(linestyle='dashed', linewidth=0.25, which="minor")
plt.title("CV curves @ 10kHz")
plt.xlabel("Bias voltage (V)")
plt.ylabel("1/C² (F⁻²)")
plt.legend()
#plt.show()
#plt.close()
plt.savefig("cvpixels.png")


## IVs of the pixels
plt.figure(5)
b, t, p = loadIV("9thJulyData/PPS_TILGAD_6 152 4 C1-V3-1TRB/PPS_TILGAD_6 152 4 C1-V3-1TRB_2024-07-09_3.iv")
plt.plot(-b,-p, label = "Pixel 0,0")
b, t, p = loadIV("9thJulyData/PPS_TILGAD_6 152 4 C1-V3-1TRB/PPS_TILGAD_6 152 4 C1-V3-1TRB_2024-07-09_4.iv")
plt.plot(-b,-p, label = "Pixel 0,1")
b, t, p = loadIV("9thJulyData/PPS_TILGAD_6 152 4 C1-V3-1TRB/PPS_TILGAD_6 152 4 C1-V3-1TRB_2024-07-09_5.iv")
plt.plot(-b,-p, label = "Pixel 1,1")
b, t, p = loadIV("9thJulyData/PPS_TILGAD_6 152 4 C1-V3-1TRB/PPS_TILGAD_6 152 4 C1-V3-1TRB_2024-07-09_6.iv")
plt.plot(-b,-p, label = "Pixel 1,0")

plt.minorticks_on()
plt.grid(True, which='both')
plt.grid(linestyle='dashed', linewidth=0.25, which="minor")
plt.title("IV curves, pad current")
plt.xlabel("Bias voltage (V)")
plt.ylabel("Pad current (A)")
plt.legend()
#plt.show()
#plt.close()
plt.savefig("ivpadspixels.png")


## IVs of the pixels
plt.figure(6)
b, t, p = loadIV("9thJulyData/PPS_TILGAD_6 152 4 C1-V3-1TRB/PPS_TILGAD_6 152 4 C1-V3-1TRB_2024-07-09_3.iv")
plt.plot(-b,-t, label = "Pixel 0,0")
b, t, p = loadIV("9thJulyData/PPS_TILGAD_6 152 4 C1-V3-1TRB/PPS_TILGAD_6 152 4 C1-V3-1TRB_2024-07-09_4.iv")
plt.plot(-b,-t, label = "Pixel 0,1")
b, t, p = loadIV("9thJulyData/PPS_TILGAD_6 152 4 C1-V3-1TRB/PPS_TILGAD_6 152 4 C1-V3-1TRB_2024-07-09_5.iv")
plt.plot(-b,-t, label = "Pixel 1,1")
b, t, p = loadIV("9thJulyData/PPS_TILGAD_6 152 4 C1-V3-1TRB/PPS_TILGAD_6 152 4 C1-V3-1TRB_2024-07-09_6.iv")
plt.plot(-b,-t, label = "Pixel 1,0")

plt.minorticks_on()
plt.grid(True, which='both')
plt.grid(linestyle='dashed', linewidth=0.25, which="minor")
plt.title("IV curves, total current")
plt.xlabel("Bias voltage (V)")
plt.ylabel("Pad current (A)")
plt.legend()
#plt.show()
#plt.close()
plt.savefig("ivtotalspixels.png")


#plt.show()