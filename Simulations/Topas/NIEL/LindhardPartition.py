



import numpy as np
import matplotlib.pyplot as plt



def LindhardPartition(E, A1=28.0, Z1=14.0, A2=28, Z2=14): #1 for projectile, 2 for medium
    if Z1==0: # This gives a value of 0 for neutrons. This works under the assumption that neutrons just exit straight through the material. Which is likely, but does not happen exactly 100% of the time
        return 0
    #if A1==1: # Same, but also ignoring protons (for various reasons)
        #return 0
    #if A1==0:
        #return 0

    # Just as a side note, it really irritates me that these coefficients are so precisely stated, yet come with no uncertainty.
    e = 1000000 * E / (30.73547 * Z2 * Z1 * pow((pow(Z2,2/3) + pow(Z1, 2/3)),1/2) * (A2 + A1) / A1)  # The energy E should be in eV
    #g = e + 0.40244 * pow(e, 3/4) + 3.4008 * pow(e, 1/6)
    g = 0.74422 * e + 1.6812 * pow(e, 3/4) + 0.90565 * pow(e, 1/6) # A different parametrisation from Akkerman et al 2006
    k = 0.079524 * pow(Z1, 2/3) * pow(Z2, 1/2) * pow(A2 + A1, 3/2) / (pow(pow(Z1, 2/3) + pow(Z2, 2/3), 3/4) * pow(A1, 3/2) * pow(A2, 1/2))
    Q = 1 / (1 + k * g)
    return Q


logspæs = np.logspace(start=-6, stop=3, num=50)


plt.figure(1)
plt.minorticks_on()
plt.title("Lindhard partition function")
plt.grid(True, which='both')
plt.grid(linestyle='dashed', linewidth=0.25, which="minor")
plt.xlabel("Energy of recoil atom (MeV)")
plt.ylabel("Lindhard partition function in Si28")
plt.xscale('log')
plt.plot(logspæs, LindhardPartition(logspæs, A1=1, Z1=1), label="Proton")
plt.plot(logspæs, LindhardPartition(logspæs, A1=2, Z1=1), label="Deuteron")
plt.plot(logspæs, LindhardPartition(logspæs, A1=4, Z1=2), label="Alpha")
plt.plot(logspæs, LindhardPartition(logspæs, A1=28, Z1=14), label="Silicon")
plt.legend()

plt.show()

print(LindhardPartition(100/1000000))