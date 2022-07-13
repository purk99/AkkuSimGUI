from tkinter import *
from tkinter import ttk

from time import sleep
from timer import *

from tools_V21 import EepromControl

from EepromData import *

eeprom = EepromControl()

eeprom.sendPackage(uartCMD["eepromReadSingleReg"],0,1)

value = eeprom.receivePackage()
value1 = eeprom.readSingleRegister(1)

print(value)
print(value1)



