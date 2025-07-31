import Gpib
import subprocess

scout = ""

def device_finder():
    #subprocess.run(["sudo modprobe ni_usb_gpib"]) 
    subprocess.run(["sudo", "ldconfig"]) 
    subprocess.run(["sudo", "gpib_config", "--minor", "0"]) 
    #subprocess.run(["sudo", "gpib_config", "--minor", "1"]) 
    #subprocess.run(["echo", "hello"])
    text = ""
    n = 1 # number of devices connected
    for j in range(n):
        for i in range(30):
            candidate = Gpib.Gpib(j,i) 
            try:
                candidate.write("*IDN?")
                text += ("interface: " + str(j) + " - address: " + str(i) + " = " + candidate.read(100).decode("utf-8") + "\n " ) #
            except:
                #print("oe", i, j)
                #continue
                pass
    global scout
    scout = text
    
device_finder()

print("result:\n\n", scout)
