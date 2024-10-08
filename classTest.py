####################################################
###First and Central file to be called in program###
###Distribution into separate Modules            ###
####################################################

from doctest import master
import tkinter as tk
from tkinter import StringVar, Toplevel, ttk
from tkinter import font
from turtle import width
from tkinter import *

import serial
from time import sleep

from moduleSpannung import *
from Module import *
from moduleCalibration import ModulStartKalibrierung

class root(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Klasse")
        #self.grid()
        self.attributes('-fullscreen',True)

        mainframe = ttk.Frame(self, padding= 10, relief="ridge", borderwidth=5)
        mainframe.pack(fill="both", expand="yes")
        
        checkFrame = ttk.Frame(self)
        checkFrame.pack(anchor=N)

        headLabel = ttk.Label(mainframe,text="Akkuprüfeinheit V2", font=('bold','40'))
        headLabel.pack()

        label = ttk.Label(mainframe, text="Modul wählen",font='30')
        label.pack()

        startTest   = ttk.Button(mainframe,text="\tRegisterwerte Prüfen\nNach jedem Neustart durchführen!",padding=10,width=75, command=self.openWindowRegisterCheck)
        startTest.pack(pady=5)

        voltageTest = ttk.Button(mainframe,text="Testmodul Spannung",padding=10,width=75,command = self.openWindowSpannung)
        voltageTest.pack(pady=5)

        eepromTest  = ttk.Button(mainframe,text="Testmodul EEPROM",padding=10,width=75, command=self.openWindowEeprom)
        eepromTest.pack(pady=5)

        temperaturTest = ttk.Button(mainframe,text="Testmodul Temperatur",padding=10,width=75, command=self.openWindowTemp)
        temperaturTest.pack(pady=5)

        #Testmodule Capacity
        #Currently not used, can be used for extension 
        #capacityTest = ttk.Button(mainframe,text="Testmodul Kapazität",padding=10,width=75,command=self.openWindowCap)
        #capacityTest.grid(column=1,row=7,pady=5)

        calibration = ttk.Button(mainframe,text="Kalibrierungsmodul",padding=10,width=75,command=self.openWindowCal)
        calibration.pack(pady=5)

        #Close complete Program
        eb = ttk.Button(mainframe,text="Programm Beenden",command = self.destroy) 
        eb.pack(pady=5)

    #Methods to call/open Other Testmodules/Windows
    def openWindowSpannung(self):
        ModulSpannung() 

    def openWindowEeprom(self):
        ModulEeprom()

    def openWindowRegisterCheck(self):
        ModulStartKalibrierung()

    def openWindowTemp(self):
        ModulTemperatur()

    def openWindowCap(self):
        ModulKapazität()

    def openWindowCal(self):
        ModulKalibrierung()


#if __name__ == "__main__":
app = root()
app.mainloop()
        

