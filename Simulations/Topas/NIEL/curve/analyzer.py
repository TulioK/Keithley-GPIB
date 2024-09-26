import numpy as np
import matplotlib.pyplot as plt

nielload = np.genfromtxt("nielresults.csv", delimiter=",")

nielenergies = nielload[:,0]
nielparticles = nielload[:,1]
nieldatas = nielload[:,2:]

nielmeans = np.zeros(len(nielenergies))
nielsigmas = np.zeros(len(nielenergies))
for n in range(len(nielenergies)):
    nielmeans[n] = np.mean(nieldatas[n])                                / 0.490966 * 1000 / 0.0233 # Conversion from Nie-dep to D
    nielsigmas[n] = np.std(nieldatas[n]) / np.sqrt(len(nielenergies))       / 0.490966 * 1000 / 0.0233 # Conversion from Nie-dep to D

lindhardload = np.genfromtxt("lindhardresults.csv", delimiter=",")

lindhardenergies = lindhardload[:,0]
lindhardparticles = lindhardload[:,1]
lindharddatas = lindhardload[:,2:]

lindhardmeans = np.zeros(len(lindhardenergies))
lindhardsigmas = np.zeros(len(lindhardenergies))
for n in range(len(lindhardenergies)):
    lindhardmeans[n] = np.mean(lindharddatas[n])                                / 0.490966 * 1000 / 0.0233 # Conversion from Nie-dep to D
    lindhardsigmas[n] = np.std(lindharddatas[n]) / np.sqrt(len(lindhardenergies))       / 0.490966 * 1000 / 0.0233 # Conversion from Nie-dep to D


plt.figure(1, figsize=[6,4], dpi=200)
plt.errorbar(nielenergies, nielmeans, yerr=nielsigmas, alpha=0.8, color="r", linestyle="dashed", capsize=5, fmt='.', label="My method")
plt.fill_between(nielenergies, nielmeans-nielsigmas, nielmeans+nielsigmas, color="r", alpha=0.1)
plt.errorbar(lindhardenergies, lindhardmeans, yerr=lindhardsigmas, alpha=0.8, color="b", linestyle="dashed", capsize=5, fmt='.', label="Lindhard")
plt.fill_between(lindhardenergies, lindhardmeans-lindhardsigmas, lindhardmeans+lindhardsigmas, color="b", alpha=0.1)
plt.minorticks_on()
plt.grid(True, which='both')
plt.grid(linestyle='dashed', linewidth=0.25, which="minor")
plt.xlabel("Proton energy (MeV)")
plt.ylabel("D/95MeVmb")
plt.xscale("log")
plt.yscale("log")
plt.legend(loc="upper right")
plt.title("Displacement damage in silicon")
plt.savefig("NielCurve.pdf", format = "pdf")
#plt.show()
