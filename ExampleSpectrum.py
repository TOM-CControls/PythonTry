import pyvisa
import time

rm = pyvisa.ResourceManager()
my_spectrum = rm.open_resource("USB0::0x0957::0xFFEF::CN0743A506::0::INSTR")
print(my_spectrum)
my_spectrum.write("*RST")
my_spectrum.timeout = 20000
print(my_spectrum.query("*TST?"))
my_spectrum.timeout = 2000
print(my_spectrum.query("*IDN?"))

#Config
my_spectrum.write(":INST SA")
my_spectrum.write(":FREQ:STAR 1000")
my_spectrum.write(":FREQ:STAR 500000")
my_spectrum.write(":INIT:CONT ON")

#setup Marker
my_spectrum.write(":CALC:MARK1:MODE POS")  
my_spectrum.write(":CALC:MARK1:STAT ON") 
my_spectrum.write(":CALC:MARK1:MAX") 

#reading values
print(my_spectrum.query(":CALC:MARK1:Y?"))
print(my_spectrum.query(":CALC:MARK1:X?"))

'''Close'''   
my_spectrum.write("*RST")
my_spectrum.close()
print("close spectrum connection")