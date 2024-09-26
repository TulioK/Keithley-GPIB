import numpy as np
import matplotlib.pyplot as plt

load = np.genfromtxt("results.csv", delimiter=",")

energies = load[:,0]
particles = load[:,1]
sizes = load[:,2]
datas = load[:,3:]

means = np.zeros(len(energies))
sigmas = np.zeros(len(energies))
for n in range(len(energies)):
    means[n] = np.mean(datas[n])                                / sizes[n] * 0.490966 * 1000 / 0.0233 # Conversion from Nie-dep to D
    sigmas[n] = np.std(datas[n]) / np.sqrt(len(energies))       / sizes[n] * 0.490966 * 1000 / 0.0233 # Conversion from Nie-dep to D


Lload = np.genfromtxt("Lindhardresults.csv", delimiter=",")

Lenergies = Lload[:,0]
Lparticles = Lload[:,1]
Lsizes = Lload[:,2]
Ldatas = Lload[:,3:]

Lmeans = np.zeros(len(Lenergies))
Lsigmas = np.zeros(len(Lenergies))
for n in range(len(Lenergies)):
    Lmeans[n] = np.mean(Ldatas[n])                                / Lsizes[n] * 0.490966 * 1000 / 0.0233 # Conversion from Nie-dep to D
    Lsigmas[n] = np.std(Ldatas[n]) / np.sqrt(len(Lenergies))       / Lsizes[n] * 0.490966 * 1000 / 0.0233 # Conversion from Nie-dep to D


plt.figure(1, figsize=[6,4], dpi=200)
plt.errorbar(sizes, means, yerr=sigmas, alpha=0.8, color="r", linestyle="dashed", capsize=5, fmt='.', label="My method")
plt.fill_between(sizes, means-sigmas, means+sigmas, color="r", alpha=0.1)
plt.errorbar(Lsizes, Lmeans, yerr=Lsigmas, alpha=0.8, color="b", linestyle="dashed", capsize=5, fmt='.', label="Lindhard")
plt.fill_between(Lsizes, Lmeans-Lsigmas, Lmeans+Lsigmas, color="b", alpha=0.1)
plt.minorticks_on()
plt.grid(True, which='both')
plt.grid(linestyle='dashed', linewidth=0.25, which="minor")
plt.xlabel("Size (0.1mm)")
plt.ylabel("D/95MeVmb")
plt.legend(loc="upper right")
plt.title("Displacement damage pr size")
plt.savefig("Sizecheck.pdf", format = "pdf")
#plt.show()