
import time
import datetime
import Gpib
import keithleyfunctions as kf


import os
import numpy as np
import threading
import asyncio
import pyqtgraph as pg
import matplotlib.pyplot as plt
from pyqtgraph.dockarea.Dock import Dock
from pyqtgraph.dockarea.DockArea import DockArea
from pyqtgraph.Qt import QtWidgets
from pyqtgraph.Qt import QtCore

app = pg.mkQApp("Keithley Controller")
win = QtWidgets.QMainWindow()
area = DockArea()
win.setCentralWidget(area)
win.resize(1600,900)
win.setWindowTitle('Keithley Picoammeter')

## Create docks, place them into the window one at a time.
## Note that size arguments are only a suggestion; docks will still have to
## fill the entire dock area and obey the limits of their internal widgets.
d1 = Dock("Dock1", size=(500,400))     ## give this dock the minimum possible size
d2 = Dock("Dock2", size=(500,400), closable=True)
d3 = Dock("Dock3", size=(1000,400))
d4 = Dock("Dock4", size=(1000,400))
d5 = Dock("Dock5", size=(1000,100))
d6 = Dock("Dock6", size=(1000,400))
area.addDock(d1, 'left')      ## place d1 at left edge of dock area (it will fill the whole space since there are no other docks yet)
area.addDock(d2, 'bottom')
area.addDock(d3, 'right', d2)
area.addDock(d4, 'right', d1)
area.addDock(d5, 'bottom', d4)
area.addDock(d6, 'bottom', d5)


## Add widgets into each dock

## first dock gets save/restore buttons
w1 = pg.LayoutWidget()

# Text that gets displayed
label = QtWidgets.QLabel("Welcome! Please connect to a Keithley picoammeter :]")
label.setWordWrap(True)
w1.addWidget(label, row=0, col=0)

# Button for connecting to the Keithely picoammeter
connectbutton = QtWidgets.QPushButton("Connect to Current Source at address: ")
w1.addWidget(connectbutton, row=1, col=0)

# Field where you can enter the gpib address of the Keithley
gpibaddress = QtWidgets.QTextEdit("22")
gpibaddress.setMaximumHeight(30)
gpibaddress.setMaximumWidth(50)
w1.addWidget(gpibaddress, row=1, col=1)

# Button for loading a .txt file with voltages in it. The file should just be numbers separated by newlines ("\n")
voltagefilebutton = QtWidgets.QPushButton("Load voltage file")
voltagefilebutton.setEnabled(False)
w1.addWidget(voltagefilebutton, row=2, col=0)

# Button for starting a measurement
measurebutton = QtWidgets.QPushButton("Start Measurement!")
measurebutton.setEnabled(False)
w1.addWidget(measurebutton, row=3, col=0)

# Button for saving the last measurement, in case you pressed something stupid during the automatic saving process
saver = QtWidgets.QPushButton("Save")
saver.setMaximumHeight(30)
saver.setMaximumWidth(50)
w1.addWidget(saver, row=3, col=1)
saver.setEnabled(False)

# Button for starting a measurement
voltagebutton = QtWidgets.QPushButton("Set voltage to (V):")
voltagebutton.setEnabled(False)
w1.addWidget(voltagebutton, row=4, col=0)

# Field for setting voltage
voltagesetter = QtWidgets.QTextEdit("0") # Sets the limit to 50uA as default
voltagesetter.setMaximumHeight(30)
voltagesetter.setMaximumWidth(50)
w1.addWidget(voltagesetter, row=4, col=1)

# Text for explaining that this is where you set current limit
currentlimittext = QtWidgets.QLabel("Set limit of current (A):")
currentlimittext.setFrameShape(QtWidgets.QFrame.Panel)
currentlimittext.setFrameShadow(QtWidgets.QFrame.Sunken)
currentlimittext.setLineWidth(1)
currentlimittext.setAlignment(QtCore.Qt.AlignCenter)
w1.addWidget(currentlimittext, row=5, col=0)

# Field for setting current limit
#currentlimiter = QtWidgets.QTextEdit("1e-5") # Sets the limit to 10uA as default
currentlimiter = QtWidgets.QComboBox()
currentlimiter.addItem("25E-6")
currentlimiter.addItem("250E-6")
currentlimiter.addItem("2.5E-3")
currentlimiter.addItem("25E-3")
currentlimiter.setMaximumHeight(30)
currentlimiter.setMaximumWidth(50)
w1.addWidget(currentlimiter, row=5, col=1)


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

liveplotupdatetext = QtWidgets.QLabel("Update interval (ms):")
w5.addWidget(liveplotupdatetext, row=0, col=1)
updatetime = QtWidgets.QTextEdit("500") # Sets 500ms as default
updatetime.setMaximumHeight(30)
updatetime.setMaximumWidth(50)
w5.addWidget(updatetime, row=0, col=2)

liveplotlengthtext = QtWidgets.QLabel("Time (s):")
w5.addWidget(liveplotlengthtext, row=0, col=3)
plotlength = QtWidgets.QTextEdit("10") # Sets 10s as default
plotlength.setMaximumHeight(30)
plotlength.setMaximumWidth(50)
w5.addWidget(plotlength, row=0, col=4)

# Button for connecting to a second picoammeter for pad current measurements
padconnectbutton = QtWidgets.QPushButton("Connect to pad current measurer at address:")
w1.addWidget(padconnectbutton, row = 6, col=0)

# Field where you can enter the gpib address of the Keithley
padaddress = QtWidgets.QTextEdit("23")
padaddress.setMaximumHeight(30)
padaddress.setMaximumWidth(50)
w1.addWidget(padaddress, row=6, col=1)

compliancelabel = QtWidgets.QLabel("Use software compliance?")
compliancelabel.setFrameShape(QtWidgets.QFrame.Panel)
compliancelabel.setFrameShadow(QtWidgets.QFrame.Sunken)
compliancelabel.setLineWidth(1)
compliancelabel.setAlignment(QtCore.Qt.AlignCenter)
w1.addWidget(compliancelabel, row=7, col=0)

compliancebutton = QtWidgets.QRadioButton()
w1.addWidget(compliancebutton, row=7, col=1)

compliancevalue = QtWidgets.QTextEdit("25")
compliancevalue.setMaximumHeight(30)
compliancevalue.setMaximumWidth(50)
w1.addWidget(compliancevalue, row=7, col=2)

complianceunits = QtWidgets.QLabel("μA")
complianceunits.setMaximumHeight(30)
complianceunits.setMaximumWidth(50)
w1.addWidget(complianceunits, row=7, col=3)

# Variables for storing the live plot variables
liveplotts = []
liveplotis = []
starttime = time.time()
updating = False # Global variable so threads can check if the live current is being read out

# Function that gets current and updates the liveplot
def updateliveplot():
    global updating
    updating = True
    readout = kf.readi(inst).decode("utf-8")
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


## Functionality of stuff
# Globals
sourceconnected = False
padmeasurerconnected = False
voltages = []
measurements = []
measurementsigmas = []
pads = []
padsigmas = []
repeatmeasurements = 5

## Connects to the Keithly currentmeter
def connectfunction():
    number = int(gpibaddress.toPlainText())
    global inst
    inst = kf.open(0, number)
    time.sleep(0.1)
    kf.configurecurrent(inst)
    kf.autorange(inst)
    kf.setilimit(inst, currentlimiter.currentText())
    label.setText("Connected to:\n" + kf.checkopen(inst).decode("utf-8"))
    voltagefilebutton.setEnabled(True)
    voltagebutton.setEnabled(True)
    connectbutton.setEnabled(False)
    global sourceconnected
    sourceconnected = True
    #timer.start() #Start the timer which updates the live plotting thingy
connectbutton.clicked.connect(connectfunction)

def padconnectfunction():
    number = int(padaddress.toPlainText())
    global padinst
    padinst = kf.open(1, number)
    time.sleep(0.1)
    kf.configurecurrent(padinst)
    kf.autorange(padinst)
    label.setText("Connected to:\n" + kf.checkopen(padinst).decode("utf-8"))
    global padmeasurerconnected
    padmeasurerconnected = True
    padconnectbutton.setEnabled(False)
padconnectbutton.clicked.connect(padconnectfunction)


## Function for choosing a file with voltages to measure on
voltagefilechooser = QtWidgets.QFileDialog()
def voltageloadfunction():
    global voltages
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
    filepathchooser.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
    filepathchooser.exec()
    if filepathchooser.selectedFiles(): ## This is just a quick check to see if the user actually chose a file.
        filepath = filepathchooser.selectedFiles()[0]

    ## Then writes the measurements into a file
    file = open(filepath, "w") ## Will give error if that file exists

    file.write("Measurement done: " + str(datetime.datetime.now()) +"\n")
    file.write("Sourcemeter: Keithley 6487" +"\n")
    file.write("Currentmeter: Keithley 6487" +"\n")
    file.write("\nComments: \n")
    file.write(commenter.toPlainText() +"\n\n")
    file.write("Number of points for median: " + str(repeatmeasurements) +"\n")
    file.write("Hardware compliance: " + str(currentlimiter.currentText()) +"\n")
    file.write("Software compliance used: " + str(compliancebutton.isChecked()) + ", value: " + compliancevalue.toPlainText() +"μA\n")
    file.write("Voltage (V), \t Total current (A), \t σ_total,  \t Pad current (A), \t σ_pad" +"\n")

    file.write("BEGIN" +"\n")
    if len(pads) == len(measurements): # If there are pad measurements, write it all
        for n in range(len(measurements)):
            file.write(str(voltages[n]) + ",\t" + str(measurements[n]) + ",\t" + str(measurementsigmas[n])+ ",\t" + str(pads[n]) + ",\t" + str(padsigmas[n]) + "\n" )
    else: # Else just fill in zeroes (this is done to keep the format, makes for easier data scripting I think
        for n in range(len(measurements)):
            file.write(str(voltages[n]) + ",\t" + str(measurements[n]) + ",\t" + str(measurementsigmas[n])+ ",\t" + str(0) + ",\t" + str(0) + "\n")
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
    axis1.errorbar(voltages[0:len(pads)], pads, yerr=padsigmas, label="Pad Current (A)", color="b", linestyle="solid", linewidth=1, capsize=5, fmt='.')
    axis1.legend(loc="upper left")
    axis2.errorbar(voltages[0:len(measurements)], measurements, yerr=measurementsigmas, label="Total current (A)", alpha=0.5, color="r", linestyle="dashed", capsize=5, fmt='.')
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
        readout = kf.readi(inst).decode("utf-8")
        readout = readout[0:readout.find('A')]
        values.append(float(readout))
    measurements.append(np.median(values)) # Finds the median, since it's a more robust estimator. Consider adding the uncertainty here also
    measurementsigmas.append(np.std(values) / np.sqrt(len(values))   *   np.sqrt(np.pi/2 * len(values) / (len(values) + 2) )  )
    # Uncertainty for median is sqrt(pi/2)*N/(N+2) * std_mean


def padmeasure():
    values = []
    for k in range(repeatmeasurements):
        readout = kf.readi(padinst).decode("utf-8")
        readout = readout[0:readout.find('A')]
        values.append(-float(readout))
    pads.append(np.median(values)) # Finds the median, since it's a more robust estimator. Consider adding the uncertainty here also
    padsigmas.append(np.std(values) / np.sqrt(len(values))   *   np.sqrt(np.pi/2 * len(values) / (len(values) + 2) )  )
    # Uncertainty for median is sqrt(pi/2)*N/(N+2) * std_mean


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
    kf.configurecurrent(inst)
    kf.autorange(inst)
    kf.setilimit(inst, currentlimiter.currentText())
    if padmeasurerconnected:
        kf.configurecurrent(padinst)
        kf.autorange(padinst)
    ## Do the measurements
    kf.enablev(inst)

    compliancereached = False  # Boolean for indicating whether or not the compliance has been hit

    # Measure all the voltages in the voltage file
    for n in range(len(voltages)):
        # Logic for doing slow raises of voltage if software compliance is enabled
        if compliancebutton.isChecked():
            currentvoltage = kf.readv(inst).decode("utf-8") # Reads the current voltage
            currentvoltage = float(currentvoltage[0:currentvoltage.find('V')]) # Makes it into a number instead of a string/bitarray


            # Do a check on the current voltage
            if not compliancereached:
                current = kf.readi(inst).decode("utf-8")
                current = float(current[0:current.find('A')])
                if current >= float(compliancevalue.toPlainText()) / 1000000:
                    kf.disablev(inst) # TURN IT OFF!!!
                    compliancereached = True
                    label.setText("Oops, hit the compliance!!!")

            # This logic is for slowly raising the voltage and checking the current, until the desired voltage is found
            stepsize = 0.1 # How big the small voltage steps should be
            while voltages[n] >= currentvoltage + stepsize and not compliancereached:
                kf.setv(inst, currentvoltage + stepsize) # Set a higher voltage
                time.sleep(0.01)
                # Then measure current and see if it hits compliance
                current = kf.readi(inst).decode("utf-8")
                current = float(current[0:current.find('A')])

                # If the current is above compliance then stop
                if current >= float(compliancevalue.toPlainText()) / 1000000:
                    kf.disablev(inst)  # TURN IT OFF!!!
                    compliancereached = True
                    label.setText("Oops, hit the compliance!!!")

                # Update the voltage to the new value
                currentvoltage = kf.readv(inst).decode("utf-8")  # Reads the current voltage
                currentvoltage = float(currentvoltage[0:currentvoltage.find('V')])
                print("V = ", currentvoltage, "\tI = ", current)


            if not compliancereached: # If the compliance was not reached, then do measurement as normal
                kf.setv(inst, voltages[n])
                time.sleep(0.01)
                totalthread = threading.Thread(target=totalmeasure)
                totalthread.start()
                padthread = threading.Thread(target=padmeasure)
                padthread.start()
                totalthread.join()
                padthread.join()

        else:
            kf.setv(inst, voltages[n])
            time.sleep(0.01)
            totalthread = threading.Thread(target=totalmeasure)
            totalthread.start()
            print("pad connected? ", padmeasurerconnected)
            if padmeasurerconnected: # This allows for measurements of just the total current
                padthread = threading.Thread(target=padmeasure)
                padthread.start()
                padthread.join()
            totalthread.join()

        time.sleep(0.01)

        plotting.setData(voltages[0:len(measurements)], measurements)
        padplotting.setData(voltages[0:len(measurements)], pads)
        app.processEvents()
    kf.disablev(inst) #Turns off voltage supply
    kf.setv(inst, 0) # Sets voltage to zero after measurements are done
    ## Open a dialog
    savefiledialog.exec()
    saver.setEnabled(True)
    #timer.start() # Starts the live current measuring again
    label.setText("Measurement done!")
measurebutton.clicked.connect(measurefunction)


def voltagesetterfunction():
    kf.enablev(inst)
    kf.setv(inst, float(voltagesetter.toPlainText()))
    if float(voltagesetter.toPlainText())==0: # This here turns off the voltage function if 0V is chosen, just for good measure and safety
        kf.disablev(inst)
voltagebutton.clicked.connect(voltagesetterfunction)






win.show()

if __name__ == '__main__':
    pg.exec()
    if sourceconnected: # Turns of the voltage if the sourcemeter was ever connected, just for good measure and safety etc
        kf.setv(inst, 0)
        kf.disablev(inst)


