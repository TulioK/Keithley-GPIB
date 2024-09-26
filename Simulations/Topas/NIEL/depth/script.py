import numpy as np
import sys

#particles = sys.argv[1]
#energy = sys.argv[2]

data = np.genfromtxt("Displacement.csv", delimiter=",", skip_header=8)[:,3]

file = open("depthresults.csv","a")
for n in range(len(data)):
    if n<len(data)-1:
        file.write(str(data[n]) + ", ")
    else:
        file.write(str(data[n]))
file.write("\n")
file.close()


