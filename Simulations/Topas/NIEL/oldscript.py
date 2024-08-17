
import numpy as np
import matplotlib.pyplot as plt

# Function that takes the energy of a recoil atom and returns the Lindhard Partition function at that energy
# Here it is assumed that the recoil atom is the same nucleus as the bulk material (so A = A1, Z = Z1). This is actually untrue at higher energies since inelastic collisions dominate there.
def LindhardPartition(E, A=28.0, Z=14.0):
    A1 = A
    Z1 = Z
    # Just as a side note, it really irritates me that these coefficients are so precisely stated, yet come with no uncertainty.
    e = E / (30.73547 * Z * Z1 * pow((pow(Z,2/3) + pow(Z1, 2/3)),1/2) * (A + A1) / A1)
    g = e + 0.40244 * pow(e, 3/4) + 3.4008 * pow(e, 1/6)
    #g = 0.74422 * e + 1.6812 * pow(e, 3/4) + 0.90565 * pow(e, 1/6) # A different parametrisation from Akkerman et al 2006
    k = 0.079524 * pow(Z, 2/3) * pow(Z1, 1/2) * pow(A + A1, 3/2) / (pow(pow(Z, 2/3) + pow(Z1, 2/3), 3/4) * pow(A, 3/2) * pow(A1, 1/2))
    Q = 1 / (1 + k * g)
    return Q

total = np.genfromtxt("Total.csv", delimiter=",", skip_header=6)
primary = np.genfromtxt("Primary.csv", delimiter=",", skip_header=6)
secondary = np.genfromtxt("Secondary.csv", delimiter=",", skip_header=6)


plt.figure(1)
plt.minorticks_on()
plt.grid(True, which='both')
plt.grid(linestyle='dashed', linewidth=0.25, which="minor")
plt.xlabel("Energy of interaction (MeV)")
plt.ylabel("Number of events in bin")
plt.xscale('log')
plt.yscale('log')
linspæs = np.logspace(start=-3, stop=1, num=len(total[1:-1])) #logspace starts at 10^start and stops at 10^stop
plt.plot(linspæs, total[1:-1], 'k', alpha=0.5, label="Elastic + Inelastic")
plt.plot(linspæs, primary[1:-1], 'b', alpha=0.5, label="Primary")
plt.plot(linspæs, secondary[1:-1], 'r', alpha=0.5, label="Secondary")
plt.legend()




plt.figure(2)
plt.minorticks_on()
plt.grid(True, which='both')
plt.grid(linestyle='dashed', linewidth=0.25, which="minor")
plt.xlabel("Energy of recoil atom (MeV)")
plt.ylabel("Lindhard partition function")
plt.xscale('log')
plt.plot(linspæs, LindhardPartition(linspæs))







plt.show()
