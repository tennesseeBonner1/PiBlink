
#This file handles the analog input and output.
#Call getNextSample to busy wait on and then retrieve the next sample when it becomes available.

#ADC (analog input)------------------------------------------------------------------------------------

import os

#Defines a bunch of constants used in our analog input code below such as GAIN_1, POS_AIN0, and NEG_AINCOM
#API found here: https://github.com/ul-gh/PiPyADC/blob/master/ADS1256_definitions.py
from ADS1256_definitions import *

#Defines the ADS class which is used to issue our analog input commands via properties and methods
#API found here: https://github.com/ul-gh/PiPyADC/blob/master/pipyadc.py
from pipyadc_py3 import ADS1256

#Used in example.py from PiPyADC library, don't think this check is required
#...but probably gives a more useful error message
if not os.path.exists("/dev/spidev0.1"):
    raise IOError("Error: No SPI device. Check settings in /boot/config.txt")

#Initial set up for analog input...
def adcInitialSetUp():
    #Create ADS module (instance of class used to interface with analog input library)
    global ads
    ads = ADS1256()

    #Reset all registers so we start from clean slate
    ads.reset()

    #Set the gain (0-5 input voltage * gain of 1 = 0-5 output voltage?)
    ads.pga_gain = GAIN_1

    '''
    Set configuration options hidden inside status register
    This register stores info in binary form where each bit is a flag
    We are...
        DISABLING Buffer (0x02, 2nd bit in register)
        ...we don't need any buffering, we will be busy waiting on each new sample as it comes
        DISABLING Autocal (0x04, 3rd bit in register)
        ...don't need auto calibration
        PRESERVING LSB (0x08, 4th bit in register)
        ...LSB (least significant bit) is responsible for handling endianness, don't touch it!
    '''
    #In effect turn off everything but keep LSB as it was
    if ads._status & ORDER_LSB:
        ads.status = ORDER_LSB #LSB was on, so turn off everything but LSB
    else:
        ads.status = 0 #LSB was off, so just turn off everything

    #Set the rate at which sampling occurs by the library in SPS (samples per second)
    ads.drate = DRATE_1000

    #Set the analog pin we will use for input
    ads.mux = POS_AIN0 | NEG_AINCOM

    #Perform calibration
    ads.cal_self()

adcInitialSetUp()

#Call before start of each data acquisition trial to ensure first sample is not corrupted
def onTrialStart():
    ads.sync()

#Return the next sample (i.e. current amplitude of eyeblink)
#Waits until data is ready to read and return value (new sample every ~1 ms)
def getNextSample():
    #Wait until data is ready to be read
    #Data is ready when DRDY (data ready) pin is in "active low"
    while ads.DRDY_PIN is not None:
        pass

    #Read in the sample from PiPyADC
    '''
        This is the fastest of the read commands from the library because it just reads,
        it doesn't have any unnecessary implicit commands like sync.
        Those implicit commands are needed only when changing input channels or config settings
        while sampling is ongoing which we do not do after initialSetUp.
        We call sync once before the start of each trial just to be safe.
    '''
    rawNumber = ads.read_async()
    
    #Scale the number to be within a range
    refinedNumber = ((-rawNumber) / 3000) - 19
    
    #After scaling the number, it is ready to be returned
    return refinedNumber

#DAC (analog output)------------------------------------------------------------------------------------

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