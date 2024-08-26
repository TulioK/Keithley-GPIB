
import numpy as np
import matplotlib.pyplot as plt
import re
import os

# Function that takes the energy of a recoil atom and returns the Lindhard Partition function at that energy
# Here it is assumed that the recoil atom is the same nucleus as the bulk material (so A = A1, Z = Z1). This is actually untrue at higher energies since inelastic collisions dominate there.
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


#header = open("bigruns/Knock.header", 'r')
#header = open("Knock.header", 'r')
header = open("/home/anton/Desktop/gitrepos/CERN/Simulations/Topas/NIEL/batch/Knock.header", 'r')
histories = float(re.findall(r'\d+',header.readlines()[2])[0]) # Using regexp to extract the number of geant4 histories from the header file
header.close()

#pkadatas = np.genfromtxt("/home/anton/Desktop/gitrepos/bigruns/Knock.phsp", dtype='unicode')
#pkadatas = np.genfromtxt("Knock.phsp", dtype='unicode')
#pkadatas = np.genfromtxt("bigruns/Knock.phsp", dtype='unicode')
pkadatas = np.genfromtxt("/home/anton/Desktop/gitrepos/CERN/Simulations/Topas/NIEL/batch/Knock.phsp", dtype='unicode')

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
inelasticparticles = pkaparticles[pkaprocesses == "protonInelastic"]
inelasticZs = pkaZs[pkaprocesses == "protonInelastic"]
inelasticAs = pkaAs[pkaprocesses == "protonInelastic"]




inprotons = inelastics[inelasticparticles == "proton"]
inneutrons = inelastics[inelasticparticles == "neutron"]
indeuterons = inelastics[inelasticparticles == "deuteron"]
inalphas = inelastics[inelasticparticles == "alpha"]
ingammas = inelastics[inelasticparticles == "gamma"]
ines = inelastics[inelasticparticles == "e-"]


# Reading in data for coulombscattering, since that requires a separate simulation
#coulombdatas = np.genfromtxt("/home/anton/Desktop/gitrepos/bigruns/CoulombKnock.phsp", dtype='unicode')
#coulombdatas = np.genfromtxt("CoulombKnock.phsp", dtype='unicode')
coulombdatas = np.genfromtxt("/home/anton/Desktop/gitrepos/CERN/Simulations/Topas/NIEL/batch/CoulombKnock.phsp", dtype='unicode')
coulombenergies = coulombdatas[:,0].astype(float)
coulombprocesses = coulombdatas[:,1]
coulombZs = coulombdatas[:,5].astype(int)
coulombAs = coulombdatas[:,6].astype(int)
coulombgenerations = coulombdatas[:,7].astype(int)
# Filtering for only coulomb scattering
coulombZs = coulombZs[coulombprocesses == "CoulombScat"]
coulombAs = coulombAs[coulombprocesses == "CoulombScat"]
coulombs = coulombenergies[coulombprocesses == "CoulombScat"]
coulombgenerations = coulombgenerations[coulombprocesses == "CoulombScat"]
# Filtering out those events with energy less than 21eV since those won't displace the Si atoms
coulombZs = coulombZs[coulombs > 21e-6]
coulombAs = coulombAs[coulombs > 21e-6]
coulombgenerations = coulombgenerations[coulombs > 21e-6]
coulombs = coulombs[coulombs > 21e-6]
primarycoulombs = coulombs[coulombgenerations == 0]
secondarycoulombs = coulombs[coulombgenerations == 1]
morecoulombs = coulombs[coulombgenerations > 1]

#coulombheader = open("/home/anton/Desktop/gitrepos/bigruns/CoulombKnock.header", 'r')
#coulombheader = open("CoulombKnock.header", 'r')
coulombheader = open("/home/anton/Desktop/gitrepos/CERN/Simulations/Topas/NIEL/batch/CoulombKnock.header", 'r')
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
crossprotons = crossection(len(inprotons),histories)
crossneutrons = crossection(len(inneutrons),histories)
crossdeuterons = crossection(len(indeuterons),histories)
crossalphas = crossection(len(inalphas),histories)
crossgammas = crossection(len(ingammas),histories)
crosses = crossection(len(ines),histories)
crosscoulomb = crossection(len(coulombs),coulombhistories)
crossprimarycoulomb = crossection(len(primarycoulombs),coulombhistories)
crosssecondarycoulomb = crossection(len(secondarycoulombs),coulombhistories)
crossmorecoulomb = crossection(len(morecoulombs),coulombhistories)

# Labels for plotting
elasticlabel = "σ_elastic = " + np.format_float_positional(crosselastic, precision=3) + "b"
inelasticlabel = "σ_inelastic = " + np.format_float_positional(crossinelastic, precision=3) + "b"
inprotonlabel = "σ_protons = " + np.format_float_positional(crossprotons, precision=3) + "b"
inneutronlabel = "σ_neutrons = " + np.format_float_positional(crossneutrons, precision=3) + "b"
indeuteronlabel = "σ_deuterons = " + np.format_float_positional(crossdeuterons, precision=3) + "b"
inalphalabel = "σ_alphas = " + np.format_float_positional(crossalphas, precision=3) + "b"
ingammalabel = "σ_gammas = " + np.format_float_positional(crossgammas, precision=3) + "b"
inelabel = "σ_e-s = " + np.format_float_positional(crosses, precision=3) + "b"
coulomblabel = "σ_coulomb = " + np.format_float_positional(crosscoulomb, precision=3) + "b"
primarycoulomblabel = "σ_primary_cou = " + np.format_float_positional(crossprimarycoulomb, precision=3) + "b"
secondarycoulomblabel = "σ_2nd_cou = " + np.format_float_positional(crosssecondarycoulomb, precision=3) + "b"
morecoulomblabel = "σ_higher_cou = " + np.format_float_positional(crossmorecoulomb, precision=3) + "b"
nuclearlabel = "σ_nuclear = " + np.format_float_positional(crossinelastic - crossprotons - crossneutrons - crossdeuterons - crossalphas -crossgammas -crosses, precision=3) + "b"


logspæs = np.logspace(start=np.log10(1e-6), stop=np.log10(max(pkaenergies)), num=100)
(elasticcounts, bins) = np.histogram(elastics, bins=logspæs)
elasticfreqs = elasticcounts/histories
(inelasticcounts, bins) = np.histogram(inelastics, bins=logspæs)
inelasticfreqs = inelasticcounts/histories
(inprotoncounts, bins) = np.histogram(inprotons, bins=logspæs)
inprotonfreqs = inprotoncounts/histories
(inneutroncounts, bins) = np.histogram(inneutrons, bins=logspæs)
inneutronfreqs = inneutroncounts/histories
(indeuteroncounts, bins) = np.histogram(indeuterons, bins=logspæs)
indeuteronfreqs = indeuteroncounts/histories
(inalphacounts, bins) = np.histogram(inalphas, bins=logspæs)
inalphafreqs = inalphacounts/histories
(ingammacounts, bins) = np.histogram(ingammas, bins=logspæs)
ingammafreqs = ingammacounts/histories
(inecounts, bins) = np.histogram(ines, bins=logspæs)
inefreqs = inecounts/histories
(coulombcounts, bins) = np.histogram(coulombs, bins=logspæs)
coulombfreqs = coulombcounts/coulombhistories
(primarycoulombcounts, bins) = np.histogram(primarycoulombs, bins=logspæs)
primarycoulombfreqs = primarycoulombcounts/coulombhistories
(secondarycoulombcounts, bins) = np.histogram(secondarycoulombs, bins=logspæs)
secondarycoulombfreqs = secondarycoulombcounts/coulombhistories
(morecoulombcounts, bins) = np.histogram(morecoulombs, bins=logspæs)
morecoulombfreqs = morecoulombcounts/coulombhistories

plt.figure(1)
plt.minorticks_on()
plt.grid(True, which='both')
plt.grid(linestyle='dashed', linewidth=0.25, which="minor")
plt.title("Created particles")
plt.xlabel("Energy of created particle (MeV)")
plt.ylabel("Frequency of events in bin")
plt.xscale('log')
plt.xlim([27e-6, max(pkaenergies)])
plt.ylim([1e-8,20*max(inelasticfreqs)])
#plt.yscale('log')
plt.stairs(elasticfreqs, bins, label=elasticlabel,  color='b')
plt.stairs(inelasticfreqs, bins, label=inelasticlabel,  color='k')
plt.stairs(inprotonfreqs, bins, label=inprotonlabel,  color='m', alpha=0.5)
plt.stairs(inneutronfreqs, bins, label=inneutronlabel,  color='y', alpha=0.5)
plt.stairs(indeuteronfreqs, bins, label=indeuteronlabel,  color='c', alpha=0.5)
plt.stairs(inalphafreqs, bins, label=inalphalabel,  color='r', alpha=0.5)
plt.stairs(ingammafreqs, bins, label=ingammalabel,  color='k', alpha=0.5)
plt.stairs(inefreqs, bins, label=inelabel,  color='m', alpha=0.5)
plt.stairs(inelasticfreqs - inprotonfreqs -inneutronfreqs - indeuteronfreqs - inalphafreqs -ingammafreqs -inefreqs, bins, label=nuclearlabel,  color='g', alpha=1)
plt.stairs(coulombfreqs, bins, label=coulomblabel,  color='k', alpha=1)
plt.stairs(primarycoulombfreqs, bins, label=primarycoulomblabel,  color='g', alpha=0.5)
plt.stairs(secondarycoulombfreqs, bins, label=secondarycoulomblabel,  color='r', alpha=0.5)
plt.stairs(morecoulombfreqs, bins, label=morecoulomblabel,  color='b', alpha=0.5)
plt.legend(loc="upper right")
plt.savefig("Frequencies.pdf", format="pdf")


plt.figure(2)
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
print("Elastic damage: ", damageelastic, "Scaled to 1MeV neq:", damageelastic/(0.095))
damageinelastic = sum(damageinelastics)
print("Inelastic damage: ", damageinelastic, "\t", sum(damageinelastics[inelasticparticles == "proton"]), " of which is from protons")
damagecoulomb = sum(damagecoulombs)
print("Coulomb damage: ", damagecoulomb, "Scaled to 1MeV neq:", damagecoulomb/(0.095))
totaldamage = damageelastic + damageinelastic + damagecoulomb
print("Total damage is: ", np.format_float_positional(totaldamage, precision=3), "MeV barn")
print("Scaled to 1MeV neq: ", np.format_float_positional(totaldamage /(95 * 0.001), precision=3))
print(damagecoulomb/(0.095))

###########################

(Delastics, bins) = np.histogram(elastics, bins=logspæs, weights=damageelastics)
(Dinelastics, bins) = np.histogram(inelastics, bins=logspæs, weights=damageinelastics)
(Dprotons, bins) = np.histogram(inprotons, bins=logspæs, weights=damageinelastics[inelasticparticles == "proton"])
(Dneutrons, bins) = np.histogram(inneutrons, bins=logspæs, weights=damageinelastics[inelasticparticles == "neutron"])
(Ddeuterons, bins) = np.histogram(inelastics[inelasticparticles == "deuteron"], bins=logspæs, weights=damageinelastics[inelasticparticles == "deuteron"])
(Dalphas, bins) = np.histogram(inelastics[inelasticparticles == "alpha"], bins=logspæs, weights=damageinelastics[inelasticparticles == "alpha"])
(Dcoulombs, bins) = np.histogram(coulombs, bins=logspæs, weights=damagecoulombs)
(Dprimarycoulombs, bins) = np.histogram(coulombs[coulombgenerations == 0], bins=logspæs, weights=damagecoulombs[coulombgenerations == 0])
(Dsecondarycoulombs, bins) = np.histogram(coulombs[coulombgenerations == 1], bins=logspæs, weights=damagecoulombs[coulombgenerations == 1])
(Dmorecoulombs, bins) = np.histogram(coulombs[coulombgenerations > 1], bins=logspæs, weights=damagecoulombs[coulombgenerations > 1])
Dnuclears = Dinelastics - Dprotons - Dneutrons - Ddeuterons - Dalphas

# Labels for plotting
Delasticlabel = "D_elastic = " + np.format_float_positional(sum(Delastics)/0.095, precision=3) + " 1MeV n_eq"
Dinelasticlabel = "D_inelastic = " + np.format_float_positional(sum(Dinelastics)/0.095, precision=3) + " 1MeV n_eq"
Dinprotonlabel = "D_protons = " + np.format_float_positional(sum(Dprotons)/0.095, precision=3) + " 1MeV n_eq"
Dinneutronlabel = "D_neutrons = " + np.format_float_positional(sum(Dneutrons)/0.095, precision=3) + " 1MeV n_eq"
Dindeuteronlabel = "D_deuterons = " + np.format_float_positional(sum(Ddeuterons)/0.095, precision=3) + " 1MeV n_eq"
Dinalphalabel = "D_alphas = " + np.format_float_positional(sum(Dalphas)/0.095, precision=3) + " 1MeV n_eq"
#Dingammalabel = "D_gammas = " + np.format_float_positional(sum(Dgammas), precision=3) + "/ 95MeV mb"
#Dinelabel = "D_e-s = " + np.format_float_positional(sum(Des), precision=3) + "/ 95MeV mb"
Dcoulomblabel = "D_coulomb = " + np.format_float_positional(sum(Dcoulombs)/0.095, precision=3) + " 1MeV n_eq"
Dprimarycoulomblabel = "D_primary_cou = " + np.format_float_positional(sum(Dprimarycoulombs)/0.095, precision=3) + " 1MeV n_eq"
Dsecondarycoulomblabel = "D_2nd_cou = " + np.format_float_positional(sum(Dsecondarycoulombs)/0.095, precision=3) + " 1MeV n_eq"
Dmorecoulomblabel = "D_higher_cou = " + np.format_float_positional(sum(Dmorecoulombs)/0.095, precision=3) + " 1MeV n_eq"
Dnuclearlabel = "D_nuclear = " + np.format_float_positional((sum(Dinelastics) - sum(Dprotons) - sum(Dneutrons) - sum(Ddeuterons) - sum(Dalphas))/0.095, precision=3) + " 1MeV n_eq"


plt.figure(3)
plt.minorticks_on()
plt.grid(True, which='both')
plt.grid(linestyle='dashed', linewidth=0.25, which="minor")
plt.title("NIEL damage")
plt.xlabel("Energy of created particle (MeV)")
plt.ylabel("NIEL damage in bin")
plt.xscale('log')
plt.xlim([1e-5, max(pkaenergies)])
plt.ylim([0,2*max(Dnuclears)])
#plt.yscale('log')
plt.stairs(Delastics, bins, label=Delasticlabel,  color='b')
plt.stairs(Dinelastics, bins, label=Dinelasticlabel,  color='k')
plt.stairs(Dprotons, bins, label=Dinprotonlabel,  color='m', alpha=0.5)
plt.stairs(Dneutrons, bins, label=Dinneutronlabel,  color='y', alpha=0.5)
plt.stairs(Ddeuterons, bins, label=Dindeuteronlabel,  color='c', alpha=0.5)
plt.stairs(Dalphas, bins, label=Dinalphalabel,  color='r', alpha=0.5)
plt.stairs(Dnuclears, bins, label=Dnuclearlabel,  color='g', alpha=0.5)
plt.stairs(Dcoulombs, bins, label=Dcoulomblabel,  color='k', alpha=1)
plt.stairs(Dprimarycoulombs, bins, label=Dprimarycoulomblabel,  color='g', alpha=0.5)
plt.stairs(Dsecondarycoulombs, bins, label=Dsecondarycoulomblabel,  color='r', alpha=0.5)
plt.stairs(Dmorecoulombs, bins, label=Dmorecoulomblabel,  color='b', alpha=0.5)
plt.legend(loc="upper right")
plt.savefig("Damages.pdf", format="pdf")

plt.figure(4)
plt.minorticks_on()
plt.grid(True, which='both')
plt.grid(linestyle='dashed', linewidth=0.25, which="minor")
plt.title("NIEL damage (coulomb)")
plt.xlabel("Energy of created particle (MeV)")
plt.ylabel("NIEL damage in bin")
plt.xscale('log')
plt.xlim([1e-5, max(pkaenergies)])
plt.ylim([0,2*max(Dcoulombs)])
plt.stairs(Dnuclears, bins, label=Dnuclearlabel,  color='m', alpha=0.5)
plt.stairs(Dcoulombs, bins, label=Dcoulomblabel,  color='k', alpha=1)
plt.stairs(Dprimarycoulombs, bins, label=Dprimarycoulomblabel,  color='g', alpha=0.5)
plt.stairs(Dsecondarycoulombs, bins, label=Dsecondarycoulomblabel,  color='r', alpha=0.5)
plt.stairs(Dmorecoulombs, bins, label=Dmorecoulomblabel,  color='b', alpha=0.5)
plt.legend(loc="upper left")
plt.savefig("CoulombDamages.pdf", format="pdf")

plt.show()

batchresults = open("/home/anton/Desktop/gitrepos/CERN/Simulations/Topas/NIEL/batch/batchresults.csv", "rb+")
batchresults.seek(-1,2)
batchresults.truncate()
batchresults.write(str(sum(Dcoulombs)/(0.095)).encode('utf-8'))
batchresults.write(", ".encode('utf-8'))
batchresults.write(str(sum(Dprimarycoulombs)/(0.095)).encode('utf-8'))
batchresults.write(", ".encode('utf-8'))
batchresults.write(str(sum(Dsecondarycoulombs)/(0.095)).encode('utf-8'))
batchresults.write(", ".encode('utf-8'))
batchresults.write(str(sum(Dmorecoulombs)/(0.095)).encode('utf-8'))
batchresults.write("\n".encode('utf-8'))
batchresults.close()





