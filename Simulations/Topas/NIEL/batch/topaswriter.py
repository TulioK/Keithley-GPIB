
import sys
import random
particles = int(sys.argv[1])
energy = float(sys.argv[2])

nuclear = open("nuclear.topas", "a")
nuclear.write('ic:So/Beam/NumberOfHistoriesInRun   = '+ str(particles) + '\n')
nuclear.write('s:Ph/Default/Type = "FTFP_BERT_HP"\n')
nuclear.write('s:Sc/Knock/OutputFile = "Knock"\n')
nuclear.write('dc:So/Beam/BeamEnergy = ' + str(energy) + ' MeV\n')
nuclear.write("i:Ts/Seed = " + str(random.randint(1,1000000000)) + "\n")
nuclear.close()

coulomb = open("coulomb.topas", "a")
coulomb.write('ic:So/Beam/NumberOfHistoriesInRun   = '+ str(int(particles/100)) + '\n')
coulomb.write('Ph/Default/Modules = 6 "g4em-standard_SS" "g4decay" "g4h-elastic_HP" "g4h-phy_FTFP_BERT_HP" "g4stopping" "g4ion-binarycascade" \n')
coulomb.write('d:Ph/Default/CutForProton = 0.0001 mm\n')
coulomb.write('s:Sc/Knock/OutputFile = "CoulombKnock"\n')
coulomb.write('dc:So/Beam/BeamEnergy = ' + str(energy) + ' MeV\n')
coulomb.write("i:Ts/Seed = " + str(random.randint(1,1000000000)) + "\n")
coulomb.close()


