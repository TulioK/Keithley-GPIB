import sys
import random
particles = int(sys.argv[1])
energy = float(sys.argv[2])
size = float(sys.argv[3])

file = open("niel.topas", "a")
file.write('ic:So/Beam/NumberOfHistoriesInRun   = '+ str(particles) + '\n')
file.write('dc:So/Beam/BeamEnergy = ' + str(energy) + ' MeV\n')
file.write("i:Ts/Seed = " + str(random.randint(1,1000000000)) + "\n")
file.write("d:Ge/World/HLX = " + str(size * 1.) + " mm\n")
file.write("d:Ge/World/HLY = " + str(size * 1.) + " mm\n")
file.write("d:Ge/World/HLZ = " + str(size * 1.) + " mm\n")
file.write("d:Ge/MyBox/HLX = " + str(size * 0.5) + " mm\n")
file.write("d:Ge/MyBox/HLY = " + str(size * 0.5) + " mm\n")
file.write("d:Ge/MyBox/HLZ = " + str(size * 0.05) + " mm\n")
file.close()
