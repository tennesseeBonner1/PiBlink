
#This file handles the analog input and output.
#Call getEyeblinkAmplitude to get the most recent value of the eyeblink amplitude.

#ADC (analog input)-----------------------------------------------------------------

import os
from ADS1256_definitions import *
from pipyadc_py3 import ADS1256

if not os.path.exists("/dev/spidev0.1"):
    raise IOError("Error: No SPI device. Check settings in /boot/config.txt")

#Analog input channel for eyeblink amplitude
EYEBLINK = POS_AIN0|NEG_AINCOM

#Sequence of all analog input channels (we only have eyeblink channel)
CH_SEQUENCE = ([EYEBLINK])

#Create ADS module and self-calibrate it
ads = ADS1256()
ads.cal_self()

#I believe calling read_sequence only draws from a buffer the library maintains and this buffer...
#is udpdated at the rate defined by here. It seems like the library might actually be performing...
#some averaging of the most recent samples to smooth it out and minimize the occurance of outlying values.
ads.drate = DRATE_1000 #In SPS (samples per second)
#Refer to PiPyADC's ADS1256_definitions.py for list of valid DRATE's

#Return a single numerical value of the "current" (most recent read from A/D library) eyeblink amplitude
def getEyeblinkAmplitude():
    #Read in the data from PiPyADC
    raw_channels = ads.read_sequence(CH_SEQUENCE)
    
    #Extract the raw input value/number
    raw_number = raw_channels[0]
    
    #Scale the number to be within a range
    refined_number = ((-raw_number) / 3000) - 19
    
    #After scaling the number, it is ready to be plotted in the graph
    return refined_number

#DAC (analog output)-----------------------------------------------------------------

import subprocess
#import atexit

#Run the daemon the pigpio library requires to function
#Since its a daemon it survives even after the program is terminated
#However only one can be spawned at a time so calling this command
#while one is already running won't spawn two (second call is just ignored)
subprocess.run(["sudo", "pigpiod"])

#In the shell...
#Daemon can be started with: "sudo pigpiod"
#Check if daemon is running and get PID: "ps -aux | grep pigpiod"
#Kill the daemon: "sudo killall pigpiod"

#Can only be imported after the daemon is up and running
from dac8552 import DAC8552, DAC_A, DAC_B, MODE_POWER_DOWN_100K

#Create the DAC module
dac = DAC8552()

#Calibrate it
dac.v_ref = 5.0
highVoltage = int(5.0 * dac.digit_per_v)

def setCSAmplitude(high):
    if high:
        dac.write_dac(DAC_A, highVoltage)
    else:
        dac.power_down(DAC_A, MODE_POWER_DOWN_100K)

def setUSAmplitude(high):
    if high:
        dac.write_dac(DAC_B, highVoltage)
    else:
        dac.power_down(DAC_B, MODE_POWER_DOWN_100K)

#Doesn't get called for some reason
#Clean up: kill the pigpio daemon since we're done using it
#def onSystemExit():
#    subprocess.run(["sudo", "killall", "pigpiod"])

#atexit.register(onSystemExit)