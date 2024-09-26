import numpy as np
import sys

particles = sys.argv[1]
energy = sys.argv[2]
size = sys.argv[3]

data = np.genfromtxt("Score.csv", delimiter=",", skip_header=5)
print(data)
file = open("results.csv","a")
file.write(", " + str(data))
file.close()


data = np.genfromtxt("Lindhard.csv", delimiter=",", skip_header=5)
print(data)
file = open("Lindhardresults.csv","a")
file.write(", " + str(data))
file.close()