

import Gpib

instrument = Gpib.Gpib(0, 22)

instrument.write("*IDN?")
print(instrument.read(100))

