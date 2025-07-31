import time
import datetime
import Gpib
import keithleyfunctions as kf

import os
import subprocess
import numpy as np
import threading
import asyncio
import pyqtgraph as pg
import matplotlib
matplotlib.use("QtAgg")
import matplotlib.pyplot as plt
from pyqtgraph.dockarea.Dock import Dock
from pyqtgraph.dockarea.DockArea import DockArea
from pyqtgraph.Qt import QtWidgets
from pyqtgraph.Qt import QtCore

# Note: this code is meant to work using Model 2410 as sourcemeter and 6487 as a picoameter, at least for the moment.
# TO DO: have this code work with both 2410 and 6487 as voltage sources

app = pg.mkQApp("Keithley Controller")
win = QtWidgets.QMainWindow()
area = DockArea()
win.setCentralWidget(area)
win.resize(1600,900)
win.setWindowTitle('Keithley Controller')

## Create docks, place them into the window one at a time.
## Note that size arguments are only a suggestion; docks will still have to
## fill the entire dock area and obey the limits of their internal widgets.
d1 = Dock("Dock1", size=(500,500))     
d2 = Dock("Dock2", size=(500,300), closable=True)
d3 = Dock("Dock3", size=(1000,300))
d4 = Dock("Dock4", size=(1000,200))
d5 = Dock("Dock5", size=(1000,50))
d6 = Dock("Dock6", size=(1000,350))
area.addDock(d1, 'left')      ## place d1 at left edge of dock area (it will fill the whole space since there are no other docks yet)
area.addDock(d2, 'bottom')
area.addDock(d3, 'right', d2)
area.addDock(d4, 'right', d1)
area.addDock(d5, 'bottom', d4)
area.addDock(d6, 'bottom', d5)

## Add widgets into each dock

## first dock gets save/restore buttons
w1 = pg.LayoutWidget()

# Connecting stuff: ####################################################################
# Text that gets displayed
label = QtWidgets.QLabel("Welcome! Please connect to a Keithley device :]")
label.setWordWrap(True)
w1.addWidget(label, row=0, col=0)

# Button for finding the addresses and interface numbers of the Keithely devices and also configure the gpib to use them
# Good for not having to type 'sudo gpib_config' every time the system is restarted, while also confirming that the Keithely numbers are correct.
finder_button = QtWidgets.QPushButton("Find devices")
w1.addWidget(finder_button, row=1, col=0)

# Button for connecting to the Keithely voltage source
connectbutton = QtWidgets.QPushButton("Connect to SourceMeter at (interface, address): ")
w1.addWidget(connectbutton, row=2, col=0)

# Field where you can enter the gpib interface number of the Keithley
gpib_interface = QtWidgets.QTextEdit("1")
gpib_interface.setMaximumHeight(30)
gpib_interface.setMaximumWidth(50)
w1.addWidget(gpib_interface, row=2, col=1)

# Field where you can enter the gpib address of the Keithley
gpibaddress = QtWidgets.QTextEdit("23")
gpibaddress.setMaximumHeight(30)
gpibaddress.setMaximumWidth(50)
w1.addWidget(gpibaddress, row=2, col=2)

# Button for connecting to a second picoammeter 
amp_connectbutton = QtWidgets.QPushButton("Connect to Picoammeter at (interface, address):")
w1.addWidget(amp_connectbutton, row = 8, col=0)

# Field where you can enter the gpib interface of the Keithley
amp_interface = QtWidgets.QTextEdit("0")
amp_interface.setMaximumHeight(30)
amp_interface.setMaximumWidth(50)
w1.addWidget(amp_interface, row=8, col=1)

# Field where you can enter the gpib address of the Keithley
amp_address = QtWidgets.QTextEdit("22")
amp_address.setMaximumHeight(30)
amp_address.setMaximumWidth(50)
w1.addWidget(amp_address, row=8, col=2)
########################################################################################


# Button for loading a .txt file with voltages in it. The file should just be numbers separated by newlines ("\n")
voltagefilebutton = QtWidgets.QPushButton("Load voltage file")
voltagefilebutton.setEnabled(False)
w1.addWidget(voltagefilebutton, row=3, col=0)

# Button for starting a measurement
measurebutton = QtWidgets.QPushButton("Start Measurement!")
measurebutton.setEnabled(False)
w1.addWidget(measurebutton, row=4, col=0)

# Button for saving the last measurement, in case you pressed something stupid during the automatic saving process
saver = QtWidgets.QPushButton("Save")
saver.setMaximumHeight(30)
saver.setMaximumWidth(50)
w1.addWidget(saver, row=4, col=1)
saver.setEnabled(False)


# VOLTAGE CONTROL: ####################################################################
# Button for starting a measurement
voltagebutton = QtWidgets.QPushButton("Set voltage to (V):")
voltagebutton.setEnabled(False)
w1.addWidget(voltagebutton, row=5, col=0)

# Field for setting voltage
voltagesetter = QtWidgets.QTextEdit("0") # Sets the limit to 50uA as default
voltagesetter.setMaximumHeight(30)
voltagesetter.setMaximumWidth(50)
w1.addWidget(voltagesetter, row=5, col=1)
########################################################################################


# Current Limiter: #####################################################################
# Text for explaining that this is where you set current limit
currentlimittext = QtWidgets.QLabel("Set limit of current (A):")
currentlimittext.setFrameShape(QtWidgets.QFrame.Shape.Panel) # this line breaks the code for me, so commented it goes 
currentlimittext.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken) # this line breaks the code for me, so commented it goes 
currentlimittext.setLineWidth(1)
#currentlimittext.setAlignment(QtCore.Qt.AlignCenter) # this line breaks the code for me, so commented it goes (they are mostly cosmetic effects anyway)
w1.addWidget(currentlimittext, row=6, col=0)

# Field for setting current limit
currentlimiter = QtWidgets.QComboBox()
currentlimiter.addItem("5E-6")
currentlimiter.addItem("10E-6")
currentlimiter.addItem("25E-6")
currentlimiter.addItem("250E-6")
currentlimiter.addItem("2.5E-3")
currentlimiter.addItem("25E-3")
currentlimiter.setMaximumHeight(30)
currentlimiter.setMaximumWidth(200)
w1.addWidget(currentlimiter, row=6, col=1, colspan=2)
########################################################################################

d1.addWidget(w1)


commenter = QtWidgets.QTextEdit("Enter comments here")
d2.addWidget(commenter)

plotter = pg.PlotWidget(title="Total current")
plotting = plotter.plot([],[], pen=(255,0,0), name="Total current", symbolBrush=(255,0,0), symbolPen='w')
plotter.setLabel("left", "Current (A)")
plotter.setLabel("bottom", "Voltage (V)")
plotter.showGrid(x=True, y=True)
plotter.setBackground("w")
d3.addWidget(plotter)

padplotter = pg.PlotWidget(title="Pad current")
padplotting = padplotter.plot([],[], pen=(0,0,255), name="Total current", symbolBrush=(0,0,255), symbolPen='w')
padplotter.setLabel("left", "Current (A)")
padplotter.setLabel("bottom", "Voltage (V)")
padplotter.showGrid(x=True, y=True)
padplotter.setBackground("w")
d6.addWidget(padplotter)

liveplotter = pg.PlotWidget(title="Live current")
liveplotting = liveplotter.plot([],[], pen=(200,200,200), symbolBrush=(255,0,0), symbolPen='w')
liveplotter.setLabel("left", "Current (A)")
liveplotter.setLabel("bottom", "Time (s)")
liveplotter.showGrid(x=True, y=True)
liveplotter.setBackground("w")


d4.addWidget(liveplotter)

w5 = pg.LayoutWidget()
d5.addWidget(w5)

# For making it easy to change the updating interval
updatetogglebutton = QtWidgets.QPushButton("Toggle live current reading")
w5.addWidget(updatetogglebutton, row=0, col=0)

reset_live_button = QtWidgets.QPushButton("Reset")
w5.addWidget(reset_live_button, row=0, col=1)

liveplotupdatetext = QtWidgets.QLabel("Update interval (ms):")
w5.addWidget(liveplotupdatetext, row=0, col=2)
updatetime = QtWidgets.QTextEdit("500") # Sets 500ms as default
updatetime.setMaximumHeight(30)
updatetime.setMaximumWidth(50)
w5.addWidget(updatetime, row=0, col=3)

liveplotlengthtext = QtWidgets.QLabel("Time (s):")
w5.addWidget(liveplotlengthtext, row=0, col=4)
plotlength = QtWidgets.QTextEdit("10") # Sets 10s as default
plotlength.setMaximumHeight(30)
plotlength.setMaximumWidth(50)
w5.addWidget(plotlength, row=0, col=5)


# Variables for storing the live plot variables
liveplotts = []
liveplotis = []
starttime = time.time()
updating = False # Global variable so threads can check if the live current is being read out

# Function that gets current and updates the liveplot
def updateliveplot():
    global updating
    updating = True
    readout = kf.readi(amp_inst).decode("utf-8")
    readout = readout[0:readout.find('A')]
    liveplotis.append(float(readout))
    liveplotts.append(time.time() - starttime)
    while liveplotts[-1] - liveplotts[0] > float(plotlength.toPlainText()): # Keeps removing the first index if it is too far in time from the latest measurement
        liveplotts.pop(0)
        liveplotis.pop(0)
    liveplotting.setData(liveplotts, liveplotis)
    updating = False

def updatethreader():
    if not updating: # Only tries to read the current value if the Keithley isn't already trying. This is relevant because sometimes the Keithley can be really slow (when it needs to scan across many ranges in autorange mode)
        t1 = threading.Thread(target=updateliveplot)
        t1.start()
        timer.setInterval(int(updatetime.toPlainText())) # Updates the interval to the value that has been set by the user
        t1.join()

timer = QtCore.QTimer()
timer.setInterval(int(updatetime.toPlainText()))
timer.timeout.connect(updatethreader)


def timertoggle():
    if timer.isActive():
        timer.stop()
    else:
        timer.start()
updatetogglebutton.clicked.connect(timertoggle)

def live_reseter():
    global starttime
    starttime = time.time()
    global liveplotts
    liveplotts = []
    global liveplotis
    liveplotis = []
reset_live_button.clicked.connect(live_reseter)


## Functionality of stuff
# Globals
sourceconnected = False
currentmetter_connected = False
voltages = []
v_set             = []
v_read            = []
v_sigmas          = []
measurements      = []
measurementsigmas = []
pads              = []
padsigmas         = []
repeatmeasurements = 5
devices_names = ""

## Connects to the Keithly 2410 SourceMeter
def connectfunction():
    number = int(gpibaddress.toPlainText())
    inter  = int(gpib_interface.toPlainText())
    global inst
    inst = kf.open(inter, number)
    time.sleep(0.1)
    kf.restore_2410(inst)
    kf.disable_beeper(inst)
    kf.setilimit_2410(inst, currentlimiter.currentText())
    globals()['devices_names'] += ("[Voltage Source]:" + " interface " + str(inter) + "; address " + str(number) + " - " + kf.checkopen(inst).decode("utf-8") + "\n")
    label.setText("Connected to:\n\n" + devices_names)
    voltagefilebutton.setEnabled(True)
    voltagebutton.setEnabled(True)
    connectbutton.setEnabled(False)
    global sourceconnected
    sourceconnected = True
connectbutton.clicked.connect(connectfunction)

## Connects to the Keithly currentmeter (Pad measuring device)
def amp_connectfunction():
    number = int(amp_address.toPlainText())
    inter  = int(amp_interface.toPlainText())
    global amp_inst
    amp_inst = kf.open(inter, number)
    time.sleep(0.1)
    kf.configurecurrent(amp_inst)
    kf.autorange(amp_inst)
    globals()['devices_names'] += ("[Picoammeter]:" + " interface " + str(inter) + "; address " + str(number) + " - " + kf.checkopen(amp_inst).decode("utf-8") + "\n")
    label.setText("Connected to:\n\n" + devices_names)
    amp_connectbutton.setEnabled(False)
    global currentmetter_connected
    currentmetter_connected = True
amp_connectbutton.clicked.connect(amp_connectfunction)


## Function for choosing a file with voltages to measure on
voltagefilechooser = QtWidgets.QFileDialog()
def voltageloadfunction():
    global voltages
    global v_set
    voltagefilechooser.exec()
    voltagefile = voltagefilechooser.selectedFiles()
    voltages = np.genfromtxt(voltagefile[0])
    measurebutton.setEnabled(True)
voltagefilebutton.clicked.connect(voltageloadfunction)


## Making a dialog system for saving or not saving data
savefiledialog = QtWidgets.QDialog()
savefiledialog.setWindowTitle("Save data?")
savefilelayout = QtWidgets.QHBoxLayout()

## If you want to save data
savebutton = QtWidgets.QPushButton("Save")
savefilelayout.addWidget(savebutton)
def savefunction():
    print("Trying to save file")
    ## First lets the user specify what the file should be called
    pwd = os.getcwd()
    filepath = pwd + "/trash.txt" ## Makes a trash file in current directory by default
    filepathchooser = QtWidgets.QFileDialog()
    filepathchooser.setAcceptMode(QtWidgets.QFileDialog.AcceptMode.AcceptSave) #debug?
    filepathchooser.exec()
    if filepathchooser.selectedFiles(): ## This is just a quick check to see if the user actually chose a file.
        filepath = filepathchooser.selectedFiles()[0]

    ## Then writes the measurements into a file
    file = open(filepath, "w") ## Will give error if that file exists

    file.write("Measurement done: " + str(datetime.datetime.now()) +"\n")
    file.write("Voltage SourceMeter: Keithley 2410" +"\n")
    file.write("Pad Currentmeter:    Keithley 6487" +"\n")
    file.write("\nComments: \n")
    file.write(commenter.toPlainText() +"\n\n")
    file.write("Number of points for median: " + str(repeatmeasurements) +"\n")
    file.write("Hardware compliance: " + str(currentlimiter.currentText()) +"\n")
    file.write("Set voltage (V), \t Measured voltage (V), \t σ_voltage (V), \t Total current (A), \t σ_total,  \t Pad current (A), \t σ_pad" +"\n")
    
    file.write("BEGIN" +"\n")
    if len(pads) == len(measurements): # If there are pad measurements, write it all
        for n in range(len(measurements)):
            file.write(str(voltages[n]) + ",\t" + str(v_read[n]) + ",\t" + str(v_sigmas[n]) + ",\t" + str(measurements[n]) + ",\t" + str(measurementsigmas[n])+ ",\t" + str(pads[n]) + ",\t" + str(padsigmas[n]) + "\n" )
    else: # Else just fill in zeroes (this is done to keep the format, makes for easier data scripting I think
        for n in range(len(measurements)):
            file.write(str(voltages[n]) + ",\t" + str(v_read[n]) + ",\t" + str(v_sigmas[n]) + ",\t" + str(measurements[n]) + ",\t" + str(measurementsigmas[n])+ ",\t" + str(0) + ",\t" + str(0) + "\n")
    file.write("END")
    file.close()
    savefiledialog.done(1)

    print("Making plot")
    # Then make an automatic plot of the data, because why not?
    fig = plt.figure(figsize=[6,4], dpi=200)
    axis1 = fig.add_subplot()
    axis2 = axis1.twinx()
    axis1.minorticks_on()
    axis1.grid(True, which='both')
    axis1.grid(linestyle='dashed', linewidth=0.25, which="minor")
    axis1.set_xlabel("Bias voltage (V)")
    axis1.set_ylabel("Pad current (A)")
    axis2.set_ylabel("Total current (A)")
    axis1.errorbar(v_read[0:len(pads)], pads, yerr=padsigmas, label="Pad Current (A)", color="b", linestyle="solid", linewidth=1, capsize=5, fmt='.')
    axis1.legend(loc="upper left")
    axis2.errorbar(v_read[0:len(measurements)], measurements, yerr=measurementsigmas, label="Total current (A)", alpha=0.5, color="r", linestyle="dashed", capsize=5, fmt='.')
    axis2.legend(loc="upper right")

    plt.show()

    plt.savefig(filepath[0:-4] + ".png") # Automatically saves the plot as the same name as the file, which is kinda hacky but whatever.
savebutton.clicked.connect(savefunction)
saver.clicked.connect(savefunction)

## If you don't want the data to be saved
saventbutton = QtWidgets.QPushButton("Saven't")
saventbutton.clicked.connect(savefiledialog.done)
savefilelayout.addWidget(saventbutton)

## Basic layout
savefiledialog.setLayout(savefilelayout)
savefiledialog.resize(200,100)

## Functions for threading
def totalmeasure():
    values = []
    for k in range(repeatmeasurements):
        readout = kf.readi_2410(inst).decode("utf-8")
        readout = readout[0:readout.find('A')]
        values.append(float(readout))
    measurements.append(np.median(values)) # Finds the median, since it's a more robust estimator. Consider adding the uncertainty here also
    measurementsigmas.append(np.std(values) / np.sqrt(len(values))   *   np.sqrt(np.pi/2 * len(values) / (len(values) + 2) )  )
    # Uncertainty for median is sqrt(pi/2)*N/(N+2) * std_mean

def padmeasure():
    values = []
    for k in range(repeatmeasurements):
        readout = kf.readi(amp_inst).decode("utf-8")
        readout = readout[0:readout.find('A')]
        values.append(-float(readout))
        time.sleep(0.1)
    pads.append(np.median(values)) # Finds the median, since it's a more robust estimator. Consider adding the uncertainty here also
    padsigmas.append(np.std(values) / np.sqrt(len(values))   *   np.sqrt(np.pi/2 * len(values) / (len(values) + 2) )  )
    # Uncertainty for median is sqrt(pi/2)*N/(N+2) * std_mean

def v_measure():
    values = []
    for k in range(repeatmeasurements):
        kf.prepare_readv_2410(inst)
        readout = kf.readv_2410_alt(inst).decode("utf-8")
        readout = readout[0:readout.find('V')]
        values.append(float(readout))
    v_read.append(np.median(values)) # Finds the median, since it's a more robust estimator. Consider adding the uncertainty here also
    v_sigmas.append(np.std(values) / np.sqrt(len(values))   *   np.sqrt(np.pi/2 * len(values) / (len(values) + 2) )  )
    # Uncertainty for median is sqrt(pi/2)*N/(N+2) * std_mean
    
def total_vi_measure():
    values_i = []
    values_v = []
    for k in range(repeatmeasurements):     
        readout = kf.read(inst).decode("utf-8").strip().split(",")
        print(readout)
        ro_v = readout[0]
        ro_i = readout[1]
        values_i.append(float(ro_i))
        values_v.append(float(ro_v))
        time.sleep(0.1)
    v_read.append(np.median(values_v)) # Finds the median, since it's a more robust estimator. Consider adding the uncertainty here also
    v_sigmas.append(np.std(values_v) / np.sqrt(len(values_v))   *   np.sqrt(np.pi/2 * len(values_v) / (len(values_v) + 2) )  )
    measurements.append(np.median(values_i)) # Finds the median, since it's a more robust estimator. Consider adding the uncertainty here also
    measurementsigmas.append(np.std(values_i) / np.sqrt(len(values_i))   *   np.sqrt(np.pi/2 * len(values_i) / (len(values_i) + 2) )  )
    # Uncertainty for median is sqrt(pi/2)*N/(N+2) * std_mean

########################################################################################
###################### The Measurement #################################################
########################################################################################
v_autorange     = False
pad_i_autorange = False

## Function that starts a measurement
def measurefunction():
    label.setText("Measuring...")
    timer.stop() # Stops the live current measuring
    global measurements
    measurements = []
    global measurementsigmas
    measurementsigmas = []
    global pads
    pads = []
    global padsigmas
    padsigmas = []
    global v_read
    v_read = []
    global v_sigmas
    v_sigmas = []
    
    
    kf.enablev_2410(inst) #set source function: volt, and enables the output
    kf.configure_sens_2410(inst)
    if v_autorange:
        kf.autorange(inst)
    else: 
        kf.set_range_manual(inst, 1000)
    
    kf.setilimit_2410(inst, currentlimiter.currentText()) # redundant, it's also in the connecting function.
    if currentmetter_connected: 
        kf.configurecurrent(amp_inst)
        if pad_i_autorange:
            kf.autorange(amp_inst)
        else:
            kf.set_current_range(amp_inst, '2E-7')
    ## Do the measurements
    
    # Measure all the voltages in the voltage file
    print("pad connected? ", currentmetter_connected)
    for n in range(len(voltages)):
        kf.setv_2410(inst, voltages[n])
        time.sleep(0.10) # time delay for stability

        totalthread = threading.Thread(target=total_vi_measure)
        totalthread.start()

        if currentmetter_connected: # This allows for measurements of just the total current (if false)
            padthread = threading.Thread(target=padmeasure)
            padthread.start()
            padthread.join()
        totalthread.join()
            
        time.sleep(0.2) # time delay for stability

        plotting.setData(v_read[0:len(measurements)], measurements)
        padplotting.setData(v_read[0:len(measurements)], pads)
        app.processEvents()
    kf.setv_2410(inst, 0) # Sets voltage to zero after measurements are done
    kf.disablev_2410(inst) #Turns off output
    ## Open a dialog
    savefiledialog.exec()
    saver.setEnabled(True)
    label.setText("Measurement done!")
measurebutton.clicked.connect(measurefunction)
########################################################################################

def voltagesetterfunction():
    kf.enablev(inst)
    kf.setv(inst, float(voltagesetter.toPlainText()))
    if float(voltagesetter.toPlainText())==0: # This here turns off the voltage function if 0V is chosen, just for good measure and safety
        kf.disablev(inst)
#voltagebutton.clicked.connect(voltagesetterfunction)

def voltage_setter_2410():
    kf.enablev_2410(inst)
    kf.setv_2410(inst, float(voltagesetter.toPlainText()))
    kf.setilimit_2410(inst, currentlimiter.currentText())
    if float(voltagesetter.toPlainText())==0: # This here turns off the voltage function if 0V is chosen, just for good measure and safety
        kf.disablev_2410(inst)
voltagebutton.clicked.connect(voltage_setter_2410)

# Function to find the address and interface numbers of the connected devices and also configure the gpib to use them
def device_finder():
# VALID ONLY WHEN YOU > KNOW < 2 DEVICES ARE CORRECTLY CONNECTED.
# TO DO: generalize for an arbitrary number of devices;
    subprocess.run(["sudo", "ldconfig"]) 
    subprocess.run(["sudo", "gpib_config", "--minor", "0"]) 
    #subprocess.run(["sudo", "gpib_config", "--minor", "1"]) 
    text = ""
    #n = 2 # number of devices connected
    n = 1
    debug_mode = False
    for j in range(n):
        for i in range(30):
            candidate = Gpib.Gpib(j,i) 
            try:
                candidate.write("*IDN?")
                text += ("interface: " + str(j) + " - address: " + str(i) + " = " + candidate.read(100).decode("utf-8") + "\n") #
            except:
                pass
    label.setText("Devices found:\n\n" + text)
finder_button.clicked.connect(device_finder)

def set_v_range():
    kf.set_range_manual(inst, 1000)
## DISABLE FOR NOW manual_v_range_button.clicked.connect(set_v_range)

def single_v_measure():
    kf.enable_output_2410(inst)
    readout = kf.single_voltage_read(inst).decode("utf-8")
    label.setText(f"Measured voltage: {readout}")
    kf.disable_output_2410(inst)
## DISABLE FOR NOW test_measure_button.clicked.connect(single_v_measure)


win.show()

if __name__ == '__main__':
    pg.exec()
    if sourceconnected: # Turns of the voltage if the sourcemeter was ever connected, just for good measure and safety etc
        kf.setv_2410(inst, 0)
        kf.disablev_2410(inst)


