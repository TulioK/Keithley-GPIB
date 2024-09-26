import sys
import random
particles = int(sys.argv[1])
energy = float(sys.argv[2])

file = open("niel.topas", "a")
file.write('ic:So/Beam/NumberOfHistoriesInRun   = '+ str(particles) + '\n')
file.write('dc:So/Beam/BeamEnergy = ' + str(energy) + ' MeV\n')
file.write("i:Ts/Seed = " + str(random.randint(1,1000000000)) + "\n")
file.close()

file = open("lindhard.topas", "a")
file.write('ic:So/Beam/NumberOfHistoriesInRun   = '+ str(particles) + '\n')
file.write('dc:So/Beam/BeamEnergy = ' + str(energy) + ' MeV\n')
file.write("i:Ts/Seed = " + str(random.randint(1,1000000000)) + "\n")
file.close()