
import numpy as np
import matplotlib.pyplot as plt
import re

# Function that takes the energy of a recoil atom and returns the Lindhard Partition function at that energy
# Here it is assumed that the recoil atom is the same nucleus as the bulk material (so A = A1, Z = Z1). This is actually untrue at higher energies since inelastic collisions dominate there.
def LindhardPartition(E, A1=28.0, Z1=14.0, A2=28, Z2=14): #1 for projectile, 2 for medium
    if Z1==0: # This gives a value of 0 for neutrons. This works under the assumption that neutrons just exit straight through the material. Which is likely, but does not happen exactly 100% of the time
        return 0
    #if A==1: # Same, but also ignoring protons (for various reasons)
        #return 0

    # Just as a side note, it really irritates me that these coefficients are so precisely stated, yet come with no uncertainty.
    e = E / (30.73547 * Z1 * Z2 * pow((pow(Z1,2/3) + pow(Z2, 2/3)),1/2) * (A1 + A2) / A2)
    g = e + 0.40244 * pow(e, 3/4) + 3.4008 * pow(e, 1/6)
    #g = 0.74422 * e + 1.6812 * pow(e, 3/4) + 0.90565 * pow(e, 1/6) # A different parametrisation from Akkerman et al 2006
    k = 0.079524 * pow(Z1, 2/3) * pow(Z2, 1/2) * pow(A1 + A2, 3/2) / (pow(pow(Z1, 2/3) + pow(Z2, 2/3), 3/4) * pow(A1, 3/2) * pow(A2, 1/2))
    Q = 1 / (1 + k * g)
    return Q


#header = open("bigruns/Knock.header", 'r')
header = open("Knock.header", 'r')
histories = float(re.findall(r'\d+',header.readlines()[2])[0]) # Using regexp to extract the number of geant4 histories from the header file
header.close()

#pkadatas = np.genfromtxt("/home/anton/Desktop/gitrepos/bigruns/Knock.phsp", dtype='unicode')
pkadatas = np.genfromtxt("Knock.phsp", dtype='unicode')
#pkadatas = np.genfromtxt("bigruns/Knock.phsp", dtype='unicode')

pkaenergies = pkadatas[:,0].astype(float)
pkaprocesses = pkadatas[:,1]
pkaparticles = pkadatas[:,2]
pkaevents = pkadatas[:,3]
pkaZs = pkadatas[:,5].astype(int)
pkaAs = pkadatas[:,6].astype(int)

elastics = pkaenergies[pkaprocesses == "hadElastic"]
elasticZs = pkaZs[pkaprocesses == "hadElastic"]
elasticAs = pkaAs[pkaprocesses == "hadElastic"]
inelastics = pkaenergies[pkaprocesses == "protonInelastic"]
inelasticZs = pkaZs[pkaprocesses == "protonInelastic"]
inelasticAs = pkaAs[pkaprocesses == "protonInelastic"]

# Reading in data for coulombscattering, since that requires a separate simulation
coulombdatas = np.genfromtxt("/home/anton/Desktop/gitrepos/bigruns/CoulombKnock.phsp", dtype='unicode')
coulombenergies = coulombdatas[:,0].astype(float)
coulombprocesses = coulombdatas[:,1]
coulombZs = coulombdatas[:,5].astype(int)
coulombAs = coulombdatas[:,6].astype(int)
# Filtering for only coulomb scattering
coulombZs = coulombZs[coulombprocesses == "CoulombScat"]
coulombAs = coulombAs[coulombprocesses == "CoulombScat"]
coulombs = coulombenergies[coulombprocesses == "CoulombScat"]
# Filtering out those events with energy less than 21eV since those won't displace the Si atoms
coulombZs = coulombZs[coulombs > 21e-6]
coulombAs = coulombAs[coulombs > 21e-6]
coulombs = coulombs[coulombs > 21e-6]


coulombheader = open("/home/anton/Desktop/gitrepos/bigruns/CoulombKnock.header", 'r')
coulombhistories = float(re.findall(r'\d+',coulombheader.readlines()[2])[0]) # Using regexp to extract the number of geant4 histories from the header file
coulombheader.close()

# Cross section is = reactions / (incident particles * length of material) * atomic mass of material / density of material
# m_si / rho_si = 2.002 * 10^-23 cm^3

materiallength = 0.01 # Length of the material in cm

def crossection(number, histories):
    return number / (histories * materiallength) * 2.002e-23 * 1e24

# Length inputs in units of cm. 1 cm^2 = 10^24barn
crosselastic = crossection(len(elastics),histories)
crossinelastic = crossection(len(inelastics),histories)
crosscoulomb = crossection(len(coulombs),coulombhistories)


# Labels for plotting
elasticlabel = "σ_elastic = " + np.format_float_positional(crosselastic, precision=3) + "b"
inelasticlabel = "σ_inelastic = " + np.format_float_positional(crossinelastic, precision=3) + "b"
coulomblabel = "σ_coulomb = " + np.format_float_positional(crosscoulomb, precision=3) + "b"


logspæs = np.logspace(start=np.log10(1e-6), stop=np.log10(200), num=200)
(elasticcounts, bins) = np.histogram(elastics, bins=logspæs)
elasticfreqs = elasticcounts/histories
(inelasticcounts, bins) = np.histogram(inelastics, bins=logspæs)
inelasticfreqs = inelasticcounts/histories
(coulombcounts, bins) = np.histogram(coulombs, bins=logspæs)
coulombfreqs = coulombcounts/coulombhistories

plt.figure(1)
plt.minorticks_on()
#plt.grid(True, which='both')
#plt.grid(linestyle='dashed', linewidth=0.25, which="minor")
plt.title("Created particles")
plt.xlabel("Energy of interaction (MeV)")
plt.ylabel("Frequency of events in bin")
plt.xscale('log')
plt.xlim([1e-3, 2e2])
plt.ylim([0,2*max(inelasticfreqs)])
#plt.yscale('log')
plt.stairs(elasticfreqs, bins, label=elasticlabel,  color='b')
plt.stairs(inelasticfreqs, bins, label=inelasticlabel,  color='k')
plt.stairs(coulombfreqs, bins, label=coulomblabel,  color='r')
plt.legend()



linspæs = np.logspace(start=-3, stop=1, num=200) #logspace starts at 10^start and stops at 10^stop
plt.figure(2)
plt.minorticks_on()
plt.title("Lindhard partition function")
plt.grid(True, which='both')
plt.grid(linestyle='dashed', linewidth=0.25, which="minor")
plt.xlabel("Energy of recoil atom (MeV)")
plt.ylabel("Lindhard partition function in Si28")
plt.xscale('log')
plt.plot(logspæs, LindhardPartition(linspæs, A1=1, Z1=1), label="Proton")
plt.plot(logspæs, LindhardPartition(linspæs, A1=28, Z1=14), label="Silicon")
plt.legend()

damageelastics = np.zeros(len(elastics))
damageinelastics = np.zeros(len(inelastics))
damagecoulombs = np.zeros(len(coulombs))
# The
for n in range(len(elastics)):
    damageelastics[n] = LindhardPartition(elastics[n], A1=elasticAs[n], Z1=elasticZs[n]) * elastics[n] * crossection(1,histories) # In units of MeV barn
for n in range(len(inelastics)):
    damageinelastics[n] = LindhardPartition(inelastics[n], A1=inelasticAs[n], Z1=inelasticZs[n]) * inelastics[n] * crossection(1,histories)
for n in range(len(coulombs)):
    damagecoulombs[n] = LindhardPartition(coulombs[n], A1=coulombAs[n], Z1=coulombZs[n]) * coulombs[n] * crossection(1,coulombhistories)

damageelastic = sum(damageelastics)
print(damageelastic)
damageinelastic = sum(damageinelastics)
print(damageinelastic)
damagecoulomb = sum(damagecoulombs)
print(damagecoulomb)
print("Displacement damage function for 200MeV protons is: ", np.format_float_positional(damageelastic + damageinelastic, precision=3), "MeV barn")
print("Scaled to 1MeV neq: ", np.format_float_positional((damageelastic + damageinelastic + damagecoulomb) * 0.095, precision=3))

plt.figure(3)
plt.minorticks_on()
plt.grid(True, which='both')
plt.grid(linestyle='dashed', linewidth=0.25, which="minor")
plt.xlabel("Energy of recoil atom (MeV)")
plt.ylabel("Lindhard partition function")

plt.show()





#plt.show()
