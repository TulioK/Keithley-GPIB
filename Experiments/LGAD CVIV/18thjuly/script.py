## Imports
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
import os
cwd = os.getcwd()

'''
## Getting a list of the folders with runs in them
folders =  glob("9thJulyData/PPS_TILGAD_6 152 4 C1-V3-1TRB/*", recursive = True)

dataPaths = []
for n in folders: # Making a list of paths to all the data, so that it it easy to pick out which one to load
    dataPaths.append(n)
'''


def plotIV(path):
    ## Just check real quick that it's actually an IV measurement
    with open(path) as f:
        first_line = f.readline().strip('\n')
    if not first_line.startswith("IV"):
        print("Mega error! This is not an IV file!")
        return #stops the function
    ## Logic for reading the data files and some parameters from it automatically
    templogic = False
    temp = ""
    skip = 0
    pix = ""
    n = 0
    with open(path) as fh:
        for line in fh:
            if line.startswith("pixel") or line.startswith("Pixel"):
                pix = line
            if line.startswith("BEGIN"):
                skip = n+1
            if templogic:
                temp = line
                templogic = False
            if line.startswith(":temp"):
                templogic = True
            n += 1
    result = np.genfromtxt(path, delimiter="\t", skip_header=skip, skip_footer=1) ## Actually loading the data
    bias = result[:, 0]
    totalCurrent = result[:, 1]
    padCurrent = result[:, 2]

    ## Logic so I can plot many lines in one plot
    fig = plt.gcf()
    if not fig.axes: ##This checks if the figure is empty, and if so it will make a subplot
        axis1 = fig.add_subplot()
        axis2 = axis1.twinx()
        axis1.minorticks_on()
        axis1.grid(True, which='both')
        axis1.grid(linestyle='dashed', linewidth=0.25, which="minor")
        axis1.set_xlabel("Bias voltage (V)")
        axis1.set_ylabel("Pad current (A)")
        axis2.set_ylabel("Total current (A)")

    ax1 = fig.axes[0]
    ax2 = fig.axes[1]

    ## Actually plotting
    ax1.plot(-bias, -padCurrent, label=pix + ", T=" + temp)
    ax1.legend(loc = "upper left")
    ax2.plot(-bias, -totalCurrent, '--', label=pix + ", T=" + temp, alpha=0.2)
    ax2.legend(loc = "upper right")



def plotCV(path):
    ## Just check real quick that it's actually an IV measurement
    with open(path) as f:
        first_line = f.readline().strip('\n')
    if not first_line.startswith("CV"):
        print("Mega error! This is not a CV file!")
        return #stops the function
    ## Logic for reading the data files and some parameters from it automatically
    templogic = False
    temp = ""
    skip = 0
    pix = ""
    n = 0
    with open(path) as fh:
        for line in fh:
            if line.startswith("pixel") or line.startswith("Pixel"):
                pix = line
            if line.startswith("BEGIN"):
                skip = n+1
            if templogic:
                temp = line
                templogic = False
            if line.startswith(":temp"):
                templogic = True
            n += 1
    result = np.genfromtxt(path, delimiter="\t", skip_header=skip, skip_footer=1) ## Actually loading the data
    bias = result[:, 0]
    capacitance = result[:, 1]
    totalCurrent = result[:, 4]

    ## Logic so I can plot many lines in one plot
    fig = plt.gcf()
    if not fig.axes: ##This checks if the figure is empty, and if so it will make a subplot
        axis1 = fig.add_subplot()
        axis2 = axis1.twinx()
        axis1.minorticks_on()
        axis1.grid(True, which='both')
        axis1.grid(linestyle='dashed', linewidth=0.25, which="minor")
        axis1.set_xlabel("Bias voltage (V)")
        axis1.set_ylabel("1/C^2 (F⁻2)")
        axis2.set_ylabel("Total current (A)")

    ax1 = fig.axes[0]
    ax2 = fig.axes[1]

    ## Actually plotting
    ax1.plot(-bias, 1/(capacitance**2), label=pix + ", T=" + temp)
    ax1.legend(loc = "upper left")
    ax2.plot(-bias, -totalCurrent, '--', label=pix + ", T=" + temp, alpha=0.2)
    ax2.legend(loc = "upper right")

    ## For just quickly making a heatmap of the capacitance values of various pixels by hand.
    ## Give me more caffeine and I will program a function that extracts this automatically and plots it automatically in a heatmap.
    print(pix, "C =", capacitance[-1])


####################################################
size = (10,10)


## TILGAD AIDA 3 IV curves
plt.figure(0,figsize=size)
plotIV("18thJulyData/PPS_TILGAD_AIDA_03/PPS_TILGAD_AIDA_03_2024-07-18_1.iv")
plotIV("18thJulyData/PPS_TILGAD_AIDA_03/PPS_TILGAD_AIDA_03_2024-07-18_2.iv")
plotIV("18thJulyData/PPS_TILGAD_AIDA_03/PPS_TILGAD_AIDA_03_2024-07-18_3.iv")
plotIV("18thJulyData/PPS_TILGAD_AIDA_03/PPS_TILGAD_AIDA_03_2024-07-18_4.iv")
plotIV("18thJulyData/PPS_TILGAD_AIDA_03/PPS_TILGAD_AIDA_03_2024-07-18_5.iv")

plt.title("AIDA3 weird IV measurements")
#plt.show()
#plt.close()
plt.savefig("AIDA3IVweird.png")


plt.figure(1,figsize=size)
plotIV("18thJulyData/PPS_TILGAD_AIDA_03/PPS_TILGAD_AIDA_03_2024-07-18_6.iv")
plotIV("18thJulyData/PPS_TILGAD_AIDA_03/PPS_TILGAD_AIDA_03_2024-07-18_7.iv")
plotIV("18thJulyData/PPS_TILGAD_AIDA_03/PPS_TILGAD_AIDA_03_2024-07-18_8.iv")
plotIV("18thJulyData/PPS_TILGAD_AIDA_03/PPS_TILGAD_AIDA_03_2024-07-18_9.iv")
plotIV("18thJulyData/PPS_TILGAD_AIDA_03/PPS_TILGAD_AIDA_03_2024-07-18_10.iv")
plotIV("18thJulyData/PPS_TILGAD_AIDA_03/PPS_TILGAD_AIDA_03_2024-07-18_11.iv")
plotIV("18thJulyData/PPS_TILGAD_AIDA_03/PPS_TILGAD_AIDA_03_2024-07-18_12.iv")
plotIV("18thJulyData/PPS_TILGAD_AIDA_03/PPS_TILGAD_AIDA_03_2024-07-18_13.iv")

plt.title("AIDA3 IV curves")
#plt.show()
#plt.close()
plt.savefig("AIDA3IV.png")



print("Aida 3")
## TILGAD AIDA 3 CV curves
plt.figure(2,figsize=size)
plotCV("18thJulyData/PPS_TILGAD_AIDA_03/PPS_TILGAD_AIDA_03_2024-07-18_1.cv")
plotCV("18thJulyData/PPS_TILGAD_AIDA_03/PPS_TILGAD_AIDA_03_2024-07-18_2.cv")
plotCV("18thJulyData/PPS_TILGAD_AIDA_03/PPS_TILGAD_AIDA_03_2024-07-18_3.cv")
plotCV("18thJulyData/PPS_TILGAD_AIDA_03/PPS_TILGAD_AIDA_03_2024-07-18_4.cv")
plotCV("18thJulyData/PPS_TILGAD_AIDA_03/PPS_TILGAD_AIDA_03_2024-07-18_5.cv")
plotCV("18thJulyData/PPS_TILGAD_AIDA_03/PPS_TILGAD_AIDA_03_2024-07-18_6.cv")
plotCV("18thJulyData/PPS_TILGAD_AIDA_03/PPS_TILGAD_AIDA_03_2024-07-18_7.cv")
plotCV("18thJulyData/PPS_TILGAD_AIDA_03/PPS_TILGAD_AIDA_03_2024-07-18_8.cv")

plt.title("AIDA3 CV curves")
#plt.show()
#plt.close()
plt.savefig("AIDA3CV.png")


## TILGAD AIDA 6 IV curves
plt.figure(3,figsize=size)
plotIV("18thJulyData/PPS_TILGAD_AIDA_06/PPS_TILGAD_AIDA_06_2024-07-08_1.iv")

#plotIV("18thJulyData/PPS_TILGAD_AIDA_06/PPS_TILGAD_AIDA_06_2024-07-18_1.iv")
#plotIV("18thJulyData/PPS_TILGAD_AIDA_06/PPS_TILGAD_AIDA_06_2024-07-18_2.iv")
plotIV("18thJulyData/PPS_TILGAD_AIDA_06/PPS_TILGAD_AIDA_06_2024-07-18_3.iv")
plotIV("18thJulyData/PPS_TILGAD_AIDA_06/PPS_TILGAD_AIDA_06_2024-07-18_4.iv")
plotIV("18thJulyData/PPS_TILGAD_AIDA_06/PPS_TILGAD_AIDA_06_2024-07-18_5.iv")
plotIV("18thJulyData/PPS_TILGAD_AIDA_06/PPS_TILGAD_AIDA_06_2024-07-18_6.iv")
plotIV("18thJulyData/PPS_TILGAD_AIDA_06/PPS_TILGAD_AIDA_06_2024-07-18_7.iv")
plotIV("18thJulyData/PPS_TILGAD_AIDA_06/PPS_TILGAD_AIDA_06_2024-07-18_8.iv")
plotIV("18thJulyData/PPS_TILGAD_AIDA_06/PPS_TILGAD_AIDA_06_2024-07-18_9.iv")
plotIV("18thJulyData/PPS_TILGAD_AIDA_06/PPS_TILGAD_AIDA_06_2024-07-18_10.iv")

fig = plt.gcf()
ax1 = fig.axes[0]
ax1.set_xlim(10,75)
ax1.set_ylim(0,1E-8)
ax2 = fig.axes[1]
ax2.set_ylim(2E-5,5E-5)

plt.title("AIDA6 IV curves")
#plt.show()
#plt.close()
plt.savefig("AIDA6IV.png")

print("AIDA 6")
## TILGAD AIDA 6 CV curves
plt.figure(4,figsize=(5,5))
plotCV("18thJulyData/PPS_TILGAD_AIDA_06/PPS_TILGAD_AIDA_06_2024-07-18_1.cv")
plotCV("18thJulyData/PPS_TILGAD_AIDA_06/PPS_TILGAD_AIDA_06_2024-07-18_2.cv")
plotCV("18thJulyData/PPS_TILGAD_AIDA_06/PPS_TILGAD_AIDA_06_2024-07-18_3.cv")
plotCV("18thJulyData/PPS_TILGAD_AIDA_06/PPS_TILGAD_AIDA_06_2024-07-18_4.cv")
plotCV("18thJulyData/PPS_TILGAD_AIDA_06/PPS_TILGAD_AIDA_06_2024-07-18_5.cv")
plotCV("18thJulyData/PPS_TILGAD_AIDA_06/PPS_TILGAD_AIDA_06_2024-07-18_6.cv")
#plotCV("18thJulyData/PPS_TILGAD_AIDA_06/PPS_TILGAD_AIDA_06_2024-07-18_7.cv")
plotCV("18thJulyData/PPS_TILGAD_AIDA_06/PPS_TILGAD_AIDA_06_2024-07-18_8.cv")

fig = plt.gcf()
ax1 = fig.axes[0]
ax1.set_ylim(3E22,4.5E22)


plt.title("AIDA6 CV curves")
#plt.show()
#plt.close()
plt.savefig("AIDA6CV.png")



## Plotting heatmap of capacitances at 40V for AIDA 3
aida3 = np.empty((5,5))
aida3[:] = np.nan
aida3[4-2,2] = 5.081837e-12
aida3[4-1,1] = 5.049437e-12
aida3[4-3,3] = 5.018637e-12
aida3[4-4,4] = 4.774937e-12
aida3[4-0,4] = 4.904837e-12
aida3[4-1,3] = 5.123737e-12
aida3[4-3,1] = 5.034937e-12
aida3[4-4,0] = 4.779137e-12
plt.figure(5,figsize=size)
plt.imshow(aida3, cmap='viridis')
cbar = plt.colorbar()
cbar.set_label("Capacitance (F)")
fig = plt.gcf()
ax1 = fig.axes[0]
ax1.set_xticks(np.arange(5), labels=[0,1,2,3,4])
ax1.set_yticks(np.arange(5), labels=[4,3,2,1,0])
ax1.set_xlabel("First index")
ax1.set_ylabel("Second index")
plt.title("AIDA 3 Capacitances")
plt.savefig("AIDA3map.png")



## Plotting heatmap of capacitances at 40V for AIDA 6
aida6 = np.empty((5,5))
aida6[:] = np.nan
aida6[4-2,2] = 5.057037e-12
aida6[4-3,3] = 5.065137e-12
aida6[4-1,1] = 5.084137e-12
aida6[4-0,0] = 4.868837e-12
aida6[4-0,4] = 4.944537e-12
aida6[4-1,3] = 5.125437e-12
#aida6[4-3,1] = 9.666237e-12
aida6[4-4,0] = 4.820937e-12

plt.figure(6,figsize=size)
plt.imshow(aida6, cmap='viridis')
cbar = plt.colorbar()
cbar.set_label("Capacitance (F)")
fig = plt.gcf()
ax1 = fig.axes[0]
ax1.set_xticks(np.arange(5), labels=[0,1,2,3,4])
ax1.set_yticks(np.arange(5), labels=[4,3,2,1,0])
ax1.set_xlabel("First index")
ax1.set_ylabel("Second index")
plt.title("AIDA 6 Capacitances")
plt.savefig("AIDA6map.png")






#plt.show()
