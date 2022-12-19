import pyvisa
import time

rm = pyvisa.ResourceManager()
my_daq = rm.open_resource("GPIB0::6::INSTR")
print(my_daq)
my_daq.write("*RST")
my_daq.timeout = 20000
print(my_daq.query("*TST?"))
my_daq.timeout = 2000
print(my_daq.query("*IDN?"))

#Print Inserted cards
print(my_daq.query("SYST:CTYPE? 100"))
print(my_daq.query("SYST:CTYPE? 200"))
print(my_daq.query("SYST:CTYPE? 300"))

scanlist = "(@210:212)"
scanIntervals = 2      #Delay in secs, between scans
numberScans = 3        #Number of scan sweeps to measure
channelDelay = 0.1      #Delay, in secs, between relay closure and measurement 
points = 0              #number of data points stored

#setup channels configuration
#my_daq.write("CONF:TEMP TC,T,(@201)")  
#my_daq.write("CONF:TEMP TC,K,(@202)")  
my_daq.write("CONF:VOLT:DC (@210,211,212)")  
my_daq.write("ROUTE:SCAN " + scanlist) 
numberChannels = int(my_daq.query("ROUTE:SCAN:SIZE?"))

#reading format
my_daq.write("FORMAT:READING:CHAN ON")
my_daq.write("FORMAT:READING:TIME ON")  
#channel delay
my_daq.write("ROUT:CHAN:DELAY " + str(channelDelay)+","+scanlist)
#setup when scanning starts and interval rate
my_daq.write("TRIG:COUNT "+str(numberScans)) 
my_daq.write("TRIG:SOUR TIMER")
my_daq.write("TRIG:TIMER " + str(scanIntervals))
my_daq.write("INIT")

'''wait until there is a data available'''
while (points==0):
    points=int(my_daq.query("DATA:POINTS?"))

'''
The data points are printed 
data, time, channel
'''
for scan in range(numberScans):
    time.sleep(scanIntervals)
    for chan in range(numberChannels):
        points=int(my_daq.query("DATA:POINTS?"))
        while (points==0):
            points = int(my_daq.write("DATA:POINTS?"))
        print (my_daq.query("DATA:REMOVE? 1"))

'''Close'''   
my_daq.write("*RST")
my_daq.close()
print("close DAQ connection")