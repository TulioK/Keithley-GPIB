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
b, t, p = loadIV("10thJulyData/PPS_TILGAD_4 152 2 C2-V3-1TRB/PPS_TILGAD_4 152 2 C2-V3-1TRb_2024-07-10_1.iv")
plt.plot(-b,-p, label = "Pixel 0,0")
b, t, p = loadIV("10thJulyData/PPS_TILGAD_4 152 2 C2-V3-1TRB/PPS_TILGAD_4 152 2 C2-V3-1TRb_2024-07-10_2.iv")
plt.plot(-b,-p, label = "Pixel 0,1")
b, t, p = loadIV("10thJulyData/PPS_TILGAD_4 152 2 C2-V3-1TRB/PPS_TILGAD_4 152 2 C2-V3-1TRb_2024-07-10_3.iv")
plt.plot(-b,-p, label = "Pixel 1,1")
b, t, p = loadIV("10thJulyData/PPS_TILGAD_4 152 2 C2-V3-1TRB/PPS_TILGAD_4 152 2 C2-V3-1TRb_2024-07-10_4.iv")
plt.plot(-b,-p, label = "Pixel 1,0")

plt.minorticks_on()
plt.grid(True, which='both')
plt.grid(linestyle='dashed', linewidth=0.25, which="minor")
plt.title("IV curves")
plt.xlabel("Bias voltage (V)")
plt.ylabel("Pad current (A)")
plt.legend()
#plt.show()
#plt.close()
plt.savefig("2x2IV.png")



## CV curves for all pixels at room temp
plt.figure(2)
b, c, t, v, g = loadCV("10thJulyData/PPS_TILGAD_4 152 2 C2-V3-1TRB/PPS_TILGAD_4 152 2 C2-V3-1TRb_2024-07-10_1.cv")
plt.plot(-b,1.0 / c**2, label = "Pixel 0,0")
b, c, t, v, g = loadCV("10thJulyData/PPS_TILGAD_4 152 2 C2-V3-1TRB/PPS_TILGAD_4 152 2 C2-V3-1TRb_2024-07-10_2.cv")
plt.plot(-b,1.0 / c**2, label = "Pixel 0,1")
b, c, t, v, g = loadCV("10thJulyData/PPS_TILGAD_4 152 2 C2-V3-1TRB/PPS_TILGAD_4 152 2 C2-V3-1TRb_2024-07-10_3.cv")
plt.plot(-b,1.0 / c**2, label = "Pixel 1,1")
b, c, t, v, g = loadCV("10thJulyData/PPS_TILGAD_4 152 2 C2-V3-1TRB/PPS_TILGAD_4 152 2 C2-V3-1TRb_2024-07-10_4.cv")
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
plt.savefig("2x2CV.png")


plt.figure(3)
b, t, p = loadIV("10thJulyData/PPS_TILGAD_4 152 2 C2-V3-1TRB/PPS_TILGAD_4 152 2 C2-V3-1TRb_2024-07-10_5.iv")
plt.plot(-b,-p, label = "T = 20C")
b, t, p = loadIV("10thJulyData/PPS_TILGAD_4 152 2 C2-V3-1TRB/PPS_TILGAD_4 152 2 C2-V3-1TRb_2024-07-10_6.iv")
plt.plot(-b,-p, label = "T = -20C")
b, t, p = loadIV("10thJulyData/PPS_TILGAD_4 152 2 C2-V3-1TRB/PPS_TILGAD_4 152 2 C2-V3-1TRb_2024-07-10_7.iv")
plt.plot(-b,-p, label = "T = -20C")
b, t, p = loadIV("10thJulyData/PPS_TILGAD_4 152 2 C2-V3-1TRB/PPS_TILGAD_4 152 2 C2-V3-1TRb_2024-07-10_8.iv")
plt.plot(-b,-p, label = "T = -10C")
b, t, p = loadIV("10thJulyData/PPS_TILGAD_4 152 2 C2-V3-1TRB/PPS_TILGAD_4 152 2 C2-V3-1TRb_2024-07-10_9.iv")
plt.plot(-b,-p, label = "T = 0C")
b, t, p = loadIV("10thJulyData/PPS_TILGAD_4 152 2 C2-V3-1TRB/PPS_TILGAD_4 152 2 C2-V3-1TRb_2024-07-10_10.iv")
plt.plot(-b,-p, label = "T = 20C")

#plt.xlim(0,150)
plt.ylim(-1E-12,3E-11)
plt.minorticks_on()
plt.grid(True, which='both')
plt.grid(linestyle='dashed', linewidth=0.25, which="minor")
plt.title("IV curves")
plt.xlabel("Bias voltage (V)")
plt.ylabel("Pad current (A)")
plt.legend()
#plt.show()
#plt.close()
plt.savefig("2x2IVtemps.png")




plt.figure(4)
b, c, t, v, g = loadCV("10thJulyData/PPS_TILGAD_4 152 2 C2-V3-1TRB/PPS_TILGAD_4 152 2 C2-V3-1TRb_2024-07-10_5.cv")
plt.plot(-b,1.0 / c**2, label = "T = -20C")
b, c, t, v, g = loadCV("10thJulyData/PPS_TILGAD_4 152 2 C2-V3-1TRB/PPS_TILGAD_4 152 2 C2-V3-1TRb_2024-07-10_6.cv")
plt.plot(-b,1.0 / c**2, label = "T = 0C")
b, c, t, v, g = loadCV("10thJulyData/PPS_TILGAD_4 152 2 C2-V3-1TRB/PPS_TILGAD_4 152 2 C2-V3-1TRb_2024-07-10_7.cv")
plt.plot(-b[:-1],1.0 / c[:-1]**2, label = "T = 20C")

plt.ylim(2.5E22,3.5E22)
plt.minorticks_on()
plt.grid(True, which='both')
plt.grid(linestyle='dashed', linewidth=0.25, which="minor")
plt.title("CV curves @ 10kHz")
plt.xlabel("Bias voltage (V)")
plt.ylabel("1/C² (F⁻²)")
plt.legend()
#plt.show()
#plt.close()
plt.savefig("2x2CVtemps.png")




plt.figure(5)
b, c, t, v, g = loadCV("10thJulyData/PPS_TILGAD_AIDA_04/PPS_TILGAD_AIDA_04_2024-07-10_1.cv")
plt.plot(-b,1.0 / c**2, label = "Pixel 0,0")

plt.minorticks_on()
plt.grid(True, which='both')
plt.grid(linestyle='dashed', linewidth=0.25, which="minor")
plt.title("CV curves @ 10kHz")
plt.xlabel("Bias voltage (V)")
plt.ylabel("1/C² (F⁻²)")
plt.legend()
#plt.show()
#plt.close()
plt.savefig("5x5CV.png")



plt.figure(6)
b, t, p = loadIV("10thJulyData/PPS_TILGAD_AIDA_04/PPS_TILGAD_AIDA_04_2024-07-10_1.iv")
plt.plot(-b,-p, label = "Pixel 0,0")

plt.minorticks_on()
plt.grid(True, which='both')
plt.grid(linestyle='dashed', linewidth=0.25, which="minor")
plt.title("IV curves")
plt.xlabel("Bias voltage (V)")
plt.ylabel("Pad current (A)")
plt.legend()
#plt.show()
#plt.close()
plt.savefig("5x5IV.png")

plt.figure(7)
b, t, p = loadIV("10thJulyData/PPS_TILGAD_AIDA_04/PPS_TILGAD_AIDA_04_2024-07-10_2.iv")
plt.plot(-b,-p, label = "Pixel 0,0")

plt.ylim(0,0.5E-8)
plt.minorticks_on()
plt.grid(True, which='both')
plt.grid(linestyle='dashed', linewidth=0.25, which="minor")
plt.title("IV curves")
plt.xlabel("Bias voltage (V)")
plt.ylabel("Pad current (A)")
plt.legend()
#plt.show()
#plt.close()
plt.savefig("2,2IV.png")


plt.figure(8)
b, c, t, v, g = loadCV("10thJulyData/PPS_TILGAD_AIDA_04/PPS_TILGAD_AIDA_04_2024-07-10_4.cv")
plt.plot(-b,1.0 / c**2, label = "Pixel 0,0")

plt.minorticks_on()
plt.grid(True, which='both')
plt.grid(linestyle='dashed', linewidth=0.25, which="minor")
plt.title("CV curves @ 10kHz")
plt.xlabel("Bias voltage (V)")
plt.ylabel("1/C² (F⁻²)")
plt.legend()
#plt.show()
#plt.close()
plt.savefig("4,0CV.png")

plt.figure(9)
b, t, p = loadIV("10thJulyData/PPS_TILGAD_AIDA_04/PPS_TILGAD_AIDA_04_2024-07-10_11.iv")
plt.plot(-b[:-1],-p[:-1], label = "Pixel 0,0")

plt.ylim(0,0.5E-8)
plt.minorticks_on()
plt.grid(True, which='both')
plt.grid(linestyle='dashed', linewidth=0.25, which="minor")
plt.title("IV curves")
plt.xlabel("Bias voltage (V)")
plt.ylabel("Pad current (A)")
plt.legend()
#plt.show()
#plt.close()
plt.savefig("4,0IV.png")












#plt.show()
