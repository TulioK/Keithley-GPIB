import Gpib
def open(bus, address):
    return Gpib.Gpib(bus, address)

def checkopen(instrument):
    instrument.write("*IDN?")
    return instrument.read(100)

def configurecurrent(instrument):
    instrument.write("CONF:CURR")

def read(instrument):
    instrument.write("READ?")
    return instrument.read(100)

def setv(instrument, voltage):
    if voltage <= 10:
        instrument.write("SOUR:VOLT:RANG 10")
    elif voltage <= 50:
        instrument.write("SOUR:VOLT:RANG 50")
    else:
        instrument.write("SOUR:VOLT:RANG 500")

    voltagestring = str(voltage)
    string = "SOUR:VOLT:LEV:IMM:AMPL " + voltagestring
    instrument.write(string)

def enablev(instrument):
    instrument.write("SOUR:VOLT:STAT 1")

def disablev(instrument):
    instrument.write("SOUR:VOLT:STAT 0")

def setilimit(instrument, currentlimit):
    instrument.write("SOUR:VOLT:ILIM " + currentlimit)

def readv(instrument):
    instrument.write("SOUR:VOLT:LEV:IMM:AMPL?")
    return instrument.read(100)

def readi(instrument):
    #instrument.write("INIT")
    #instrument.write("SENS:DATA?")
    instrument.write("READ?")
    return instrument.read(100)

def autorange(instrument):
    instrument.write("SENS:CURR:RANG:AUTO 1")

def interlock(instrument):
    instrument.write("SOUR:VOLT:INT:STAT?")
    return instrument.read(100)

def interlockdisable(instrument):
    instrument.write("SOUR:VOLT:INT:STAT 0")



