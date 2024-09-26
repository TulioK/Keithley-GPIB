import random
import numpy as np
import matplotlib.pyplot as plt
from iminuit import Minuit
import scipy.stats as stats

import scipy
from matplotlib.pyplot import imshow
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm, ticker


#data = np.genfromtxt("resolution_CERNSept2024_Run_7_TOA250to500.csv", skip_header=1, delimiter=",")
data = np.genfromtxt("resolution_CERNSept2024_Run_7_TOA250to500.csv", skip_header=1, delimiter=",")
values = data[:,-2]
weights = data[:,-1]

pixelmeans = np.zeros([16,16])
pixelsigmas = np.zeros([16,16])
for x in range(16):
    rowfilter = data[:, -4] == x
    rowed = data[rowfilter]
    #print(rowed)
    for y in range(16):
        colfilter = rowed[:, -3] == y
        coled = rowed[colfilter]
        resolutions = coled[:,-2]
        resolutionerrors = coled[:,-1] # These are the variances, I am pretty sure

        if len(resolutions) > 0: # Only use those pixels for which there are data
            pixelmeans[x,y] = np.sum(resolutions / np.pow(resolutionerrors,2)) / np.sum(1 / np.pow(resolutionerrors,2))
            pixelsigmas[x,y] = np.sqrt(1 / np.sum(1 / np.pow(resolutionerrors,2)))


# Make a list that doesn't have the zero pixels in it
notzero = pixelmeans > 0
means = pixelmeans[notzero]
sigmas = pixelsigmas[notzero]


# Plot it out
fig, ax = plt.subplots( figsize=[8,6], dpi=200)
im = ax.imshow(pixelmeans)
for i in range(16):
    for j in range(16):
        text = ax.text(j, i, str(np.format_float_positional(pixelmeans[i, j], precision=3, fractional = False)) + "\n ±" + str(np.format_float_positional(pixelsigmas[i, j], precision=2, fractional = False)), ha="center", va="center", color="w", fontsize=5)
#plt.show()
plt.title("Pixel time resolutions (ps)")
fig.colorbar(im, ax=ax)
plt.savefig("Map.pdf", format="pdf")
plt.close()

# Calculate the mean and spread of the whole board
mean = np.sum(means / np.pow(sigmas,2)) / np.sum(1 / np.pow(sigmas,2))
sigma = np.sqrt(1 / np.sum(1 / np.pow(sigmas,2)))

print("Naively: ", str(mean) + " ± " + str(sigma) + ". Alternatively, std is: " + str(np.std(means)))

#####################################################################################################

# Bootstrapping the pdf of the data from the uncertainties on the data

boots = 1000000

bootsample = np.zeros(boots)
for n in range(boots):
    index = random.randint(0, len(means)-1)
    bootsample[n] = np.random.normal(loc = means[index], scale = sigmas[index]) # Could probably be made faster if it sampled a lot of points at once, but then the logic becomes harder for me to write :[
    #bootsample[n] = np.random.normal(loc = means[index], scale = sigmas[index], size = 100)

plt.hist(bootsample, bins = 200)
#plt.hist(means)
#plt.show()
plt.close()

print("Bootsrapped std = ", np.std(bootsample))


## Now for maximum likelihood fitting!


#####################################################################################################
def neggausslogl(mean, deviation): # The data "means" is hardcoded into the function. Usually this is not a proble, since data rarely changes after the experiment :p
    #return -np.sum(0.5 * np.log10(1 / np.pow(deviation, 2)) - np.pow(means - mean, 2) / (2 * np.pow(deviation, 2)))
    return -np.sum(- 0.5 * np.log(np.pow(deviation, 2)) - np.pow(means - mean, 2) / (2 * np.pow(deviation, 2)))

print("Maximum likelihood on the data, not taking uncertainties into account")
minu = Minuit(neggausslogl, mean=10, deviation= 1)
minu.errordef = 0.5 #Because of log-likelihood
minu.limits = [(None, None), (0, None)]

minu.migrad()
minu.hesse() # Finite difference (assume parabolic) covariance matrix
minu.minos() # Profile likelihood method
#print(minu) # Printing all out
print(repr(minu.values[:])) # Accessing the fitted parameters
#print(repr(minu.covariance)) # Accessing the covariance matrix from Hesse
print(repr(minu.merrors[0].lower), repr(minu.merrors[0].upper), repr(minu.merrors[1].lower), repr(minu.merrors[1].upper)) # Accessing the assymmetrical errors from MINOS. Haven't found a better way yet :/


def bootlog(mean, deviation): # The data "means" is hardcoded into the function. Usually this is not a proble, since data rarely changes after the experiment :p
    return -np.sum(- 0.5 * np.log(np.pow(deviation, 2)) - np.pow(bootsample - mean, 2) / (2 * np.pow(deviation, 2)))


print("Maximum likelihood on the bootstrapped data")
minu = Minuit(bootlog, mean=10, deviation= 1)
minu.errordef = 0.5 #Because of log-likelihood
minu.limits = [(None, None), (0, None)]

minu.migrad()
minu.hesse() # Finite difference (assume parabolic) covariance matrix
minu.minos() # Profile likelihood method
#print(minu) # Printing all out
print(repr(minu.values[:])) # Accessing the fitted parameters
#print(repr(minu.covariance)) # Accessing the covariance matrix from Hesse
print(repr(minu.merrors[0].lower), repr(minu.merrors[0].upper), repr(minu.merrors[1].lower), repr(minu.merrors[1].upper)) # Accessing the assymmetrical errors from MINOS. Haven't found a better way yet :/



plt.figure(7)
plt.hist(bootsample, bins=200, density=True, label="Bootstrapped samples")
linspes = np.linspace(30, 50, 100)
plt.plot(linspes,  1 / (minu.values[1] * np.sqrt(2 * np.pi)) * np.exp(-0.5 * np.pow((linspes - minu.values[0])/minu.values[1] ,2)), label="ML fit")
plt.plot(linspes, 1 / (1.178 * np.sqrt(2 * np.pi)) * np.exp(-0.5 * np.pow((linspes - 40.387)/1.178, 2)), label="Weighted mean")
plt.legend()
plt.savefig("BootstrapFit.pdf", format="pdf")



plt.figure(8)
fig, ax = minu.draw_mnprofile("deviation")
plt.show()
plt.close()

# Iminuit testing:
'''
#####################################################################################################
# This shows all the uncertainty regions
fig, ax = minu.draw_mnmatrix()
#plt.show()
plt.close()

# Only a certain contour (pick out specific parameters)
# get individual contours to plot them yourself (the "experimental" option (instead of "interpolated") needs scipy)
pts = minu.mncontour("mean", "deviation", cl=0.68, size=20, experimental=True)
x, y = np.transpose(pts)
plt.plot(x, y, "o-")
#plt.show()
plt.close()

# Draw one of the parameters
fig, ax = minu.draw_mnprofile("deviation")
#plt.show()
plt.close()
#####################################################################################################
'''
