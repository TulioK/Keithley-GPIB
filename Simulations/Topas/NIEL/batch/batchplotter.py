import numpy as np
import matplotlib.pyplot as plt


# Simulated data
data = np.genfromtxt("batchresults.csv", delimiter="," )
energies = data[:,0]
particles = data[:,1]
total = data[:,2]
primary = data[:,3]
secondary = data[:,4]
more = data[:,5]


# Data from other sources:
huhtinen = np.genfromtxt("/home/anton/Desktop/gitrepos/CERN/Simulations/Topas/NIEL/huhtinen.csv", delimiter="\t")
summers = np.genfromtxt("/home/anton/Desktop/gitrepos/CERN/Simulations/Topas/NIEL/summers.csv", delimiter="\t")

plt.figure(0, figsize=(8,6), dpi=200)
plt.minorticks_on()
plt.grid(True, which='both')
plt.grid(linestyle='dashed', linewidth=0.25, which="minor")
plt.plot(energies, total, label="Total coulomb damage", color="k", marker='.', linewidth=1, alpha=0.3)
plt.plot(energies, primary, label="Primary coulomb damage", color="g", marker='.', linewidth=1, alpha=0.3)
plt.plot(energies, secondary, label="Secondary coulomb damage", color="r", marker='.', linewidth=1, alpha=0.3)
plt.plot(energies, more, label="Higher order coulomb damage", color="b", marker='.', linewidth=1, alpha=0.3)
plt.plot(huhtinen[:,0], huhtinen[:,1], label="M. Huhtinen and P.A. Aarnio; NIM A 335 (1993) 580 and priv. comm.", linewidth=2, color="m", linestyle="solid")
plt.plot(summers[:,0], summers[:,1], label="G.P. Summers et al., IEEE NS 40 (1993) 1372", linewidth=2, color="c", linestyle="solid")
plt.xlim([min(energies), max(energies)])
plt.ylim([0.05, 20])
plt.xscale("log")
plt.yscale("log")
plt.xlabel("Proton energy (MeV)")
plt.ylabel("NIEL damage /1MeV neq")
plt.title("NIEL damage in silicon from protons")
plt.legend()
plt.savefig("NielCurve.pdf", format="pdf")

plt.show()
