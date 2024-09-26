import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as scop

load = np.genfromtxt("depthresults.csv", delimiter=",")

binnumber = len(load[:][0])
bins = np.linspace(start= 0 + 1/(binnumber*2), stop=1 - 1/(binnumber*2), num=binnumber)

means = np.zeros(len(load[:][0]))
sigmas = np.zeros(len(load[:][0]))
for n in range(len(load[:][0])):
    means[n] = np.mean(load[:,n])
    sigmas[n] = np.std(load[:,n]) / np.sqrt(len(load[:,n]))


def fitfunc(x,a,b):
    return a * x + b

fitparameters, fitcovariance = scop.curve_fit(fitfunc, bins, means, sigma = sigmas, absolute_sigma=True)


plt.figure(1, figsize=[6,4], dpi=200)
plt.errorbar(bins, means, xerr = 1/binnumber / np.sqrt(12), yerr=sigmas, alpha=0.8, color="r", linestyle="dashed", capsize=5, fmt='.')
plt.fill_between(bins, means-sigmas, means+sigmas, color="r", alpha=0.1)
plt.plot(bins,fitfunc(bins, *fitparameters),color='k', label="Best linear fit")
plt.plot(bins,fitfunc(bins, fitparameters[0] + np.sqrt(fitcovariance[0,0]), fitparameters[1] + np.sqrt(fitcovariance[1,1]) ),color='k', linestyle="dashed", label="Fit uncertainty")
plt.plot(bins,fitfunc(bins, fitparameters[0] - np.sqrt(fitcovariance[0,0]), fitparameters[1] - np.sqrt(fitcovariance[1,1]) ),color='k', linestyle="dashed")
plt.minorticks_on()
plt.grid(True, which='both')
plt.grid(linestyle='dashed', linewidth=0.25, which="minor")
plt.xlabel("Depth (0.1mm)")
plt.ylabel("D/95MeVmb")
plt.legend(loc="upper right")
plt.title("Displacement damage in silicon")
plt.savefig("Depth.pdf", format = "pdf")

#plt.show()
