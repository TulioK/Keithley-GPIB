Controller for Keithley voltage source and picoameter using GPIB connections

This is an attempt to update [Anton's IV characterisation code](https://github.com/AntonKristensen/CERN/tree/main/Instruments/KeithleyPicoammeter), to be used to characterize LGADs IV curves using Keithley SMUs during test beams. The most important updates included enabling the measurement and registration of the actual output voltages, instead of the one configured by the user. Also relevant was adding commands for usage of Keithley Model 2410, a voltage source with hardware compliance.  

Anton's code produces a graphical interface using the _pyqtgraph_ library, where the user can set a few configuration parameters and view the IV curves read from the LGADs in real time. The actual measurements are performed using Keithley devices, such as the Keithley 2410 SourceMeter and the Model 6487 Picoammeter/Voltage Source. These devices are controlled remotelly using commands in SCPI language. A General Purpose Interface Bus (GPIB) connector in each device is used for data transfer, via a cable with a USB adapter. The use of such a connector requires some configuration to be carried out in the controller machine. For linux systems, [these configuration instructions ](https://gist.github.com/ochococo/8362414fff28fa593bc8f368ba94d46a) has proven to be quite useful, except for the configuration steps in the linux-gpib-user folder. The fix is to first run ./bootstrap and ./configure:

```
cd ~/linux-gpib-code/linux-gpib-user
./bootstrap
./configure
make
make install
```
The remaining of the instructions are fine.

The Gpib python library is used to facilitate the control via a python script. An exemple of such script would be the one bellow, which can be used to set Model 2410 to operate as a voltage source, outputing 42 volts, and makes a reading. This reading is a string with 5 quantities separated by commas. The first one is the voltage, while the second is the current.

```python
import Gpib

instrument = Gpib.Gpib(interface, address)
instrument.write("SOUR:FUNC VOLT") #set source function: volt
instrument.write("OUTP ON") #enables the output
instrument.write(':SENS:FUNC "VOLT","CURR"') # sets to read both voltage and current from measurements (as opposed to settings)
voltage    = 42 #some voltage to set the source.
instrument.write("SOUR:VOLT " + str(voltage)) 
readout    = instrument.write("READ?").decode("utf-8")
print(readout)
instrument.write("OUTP OFF") #disables the output

```

The :SENS:FUNC "VOLT","CURR" instruction is used here to tell the SourceMeter to inform the actual output voltage alongside with the measured current. Alternatively, :SENS:FUNC "CURR" can be used to measure the current only, and the voltage returned by the reading will be exactly the one configured by the user.

The GUI has a button to help find the interface and address number of the connected devices, which also prompts their gpib configuration. Two separate connection buttons for the SourceMeter and Picoammeter allows to easily change the connection parameters if needed. The following is a screenshot from the GUI, after a preliminary measurement was performed in a standard LGAD at room temperature.

The GUI presents three different plots. The top one can be turned on whenever there is no measurement being performed, and shows the live current resulting from the voltage that is being applied, plotted as a function of time for the last few seconds. The middle one is an IV curve measuring the "pad" current, which is crossing one of the pixels. Finally, the bottom panel shows the total current being drawn by the sensor.

The measurement of the curve is automated based on voltage values listed in a simple text file, which can be loaded with a press of a button. Once finished with all measurements, the results are saved to a text file.

The current state of the code is meant for usage with Model 2410 as a source, and model 6487 as a pad amperimeter. The goal for the future is to generalize for multiple configurations of devices.
