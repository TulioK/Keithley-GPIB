import Gpib
def open(bus, address):
    return Gpib.Gpib(bus, address)

def disable_beeper(instrument):
    instrument.write("SYST:BEEP:STAT OFF")

def checkopen(instrument):
    instrument.write("*IDN?")
    return instrument.read(100)

def configurecurrent(instrument):
    instrument.write("CONF:CURR")

def read(instrument):
    instrument.write("READ?")
    return instrument.read()
    
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

def restore_2410(instrument):
#Restore GPIB defaults
    instrument.write("*RST")
 
def single_voltage_read(instrument):
    instrument.write(":FORM:ELEM VOLT")
    instrument.write(":MEAS:VOLT?")
    return instrument.read()
 
def enablev_2410(instrument):
    instrument.write("SOUR:FUNC VOLT")
    instrument.write("OUTP ON")

def set_range_manual(instrument, vrange):
    instrument.write(":SOUR:VOLT:RANG " + str(vrange))

def set_current_range(instrument, irange):
    instrument.write(":SENS:CURR:RANG " + irange)

def setv_2410(instrument, voltage):
    instrument.write("SOUR:VOLT " + str(voltage))   
    
def disablev_2410(instrument):
    instrument.write("OUTP OFF")
    
def setilimit(instrument, currentlimit):
    instrument.write("SOUR:VOLT:ILIM " + currentlimit)
    
def setilimit_2410(instrument, currentlimit):
    instrument.write("SENS:CURR:PROT " + currentlimit)

def readv(instrument):
    instrument.write("SOUR:VOLT:LEV:IMM:AMPL?")
    return instrument.read(100)
    
def readv_2410(instrument):
    instrument.write("SOUR:VOLT:LEV?")
    return instrument.read(100)

def readv_2410_alt(instrument):
    instrument.write("READ?")
    return instrument.read(100)

def prepare_readv_2410(instrument):
    instrument.write("SENS:FUNC VOLT")
    instrument.write("FORM:ELEM VOLT")

def enable_output_2410(instrument):
    instrument.write(":OUTP ON")

def disable_output_2410(instrument):
    instrument.write(":OUTP OFF")

def readi(instrument):
    instrument.write("READ?")
    return instrument.read(100)
    
def configure_sens_curr_2410(instrument):
    instrument.write("SENS:FUNC CURR")
    instrument.write("SENS:CURR:RANG:AUTO 1")
    
def configure_sens_2410(instrument):
    instrument.write(':SENS:FUNC "VOLT","CURR"') 
    
def set_curr_rang_auto_2410(instrument): # redundant
    instrument.write("SENS:CURR:RANG:AUTO 1")
    
def readi_2410(instrument):
    instrument.write("FORM:ELEM CURR")
    instrument.write("READ?")
    return instrument.read(100)

def autorange(instrument):
    instrument.write("SENS:CURR:RANG:AUTO 1")

def interlock(instrument):
    instrument.write("SOUR:VOLT:INT:STAT?")
    return instrument.read(100)

def interlockdisable(instrument):
    instrument.write("SOUR:VOLT:INT:STAT 0")
