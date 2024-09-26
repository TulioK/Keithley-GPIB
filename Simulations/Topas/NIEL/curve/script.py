import numpy as np
import sys

particles = sys.argv[1]
energy = sys.argv[2]

data = np.genfromtxt("Score.csv", delimiter=",", skip_header=5)
file = open("nielresults.csv","a")
file.write(", " + str(data))
file.close()

data = np.genfromtxt("Lindhard.csv", delimiter=",", skip_header=5)
file = open("lindhardresults.csv","a")
file.write(", " + str(data))
file.close()
