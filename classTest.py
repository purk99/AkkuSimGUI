from doctest import master
import tkinter as tk
from tkinter import StringVar, Toplevel, ttk
from tkinter import font
from turtle import width

import serial
from time import sleep

from moduleSpannung import *
from Module import *

class root(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Klasse")
        self.grid()
        self.attributes('-fullscreen',True)

        mainframe = ttk.Frame(self, padding= 10, relief="ridge", borderwidth=5)
        mainframe.grid(sticky=NSEW)
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        voltageTest = ttk.Button(mainframe,text="Testmodul Spannung",padding=10,width=75,command = self.openWindowSpannung)
        voltageTest.grid(column=1,row=3,pady=5)

        eepromTest  = ttk.Button(mainframe,text="Testmodul EEPROM",padding=10,width=75, command=self.openWindowEeprom)
        eepromTest.grid(column=1,row=4,pady=5)

        #stromTest   = ttk.Button(mainframe,text="Testmodus Ladestrom",padding=10,width=75)
        #stromTest.grid(column=1,row=5,pady=5)

        temperaturTest = ttk.Button(mainframe,text="Testmodul Temperatur",padding=10,width=75, command=self.openWindowTemp)
        temperaturTest.grid(column=1,row=6,pady=5)

        capacityTest = ttk.Button(mainframe,text="Testmodul Kapazität",padding=10,width=75,command=self.openWindowCap)
        capacityTest.grid(column=1,row=7,pady=5)

        calibration = ttk.Button(mainframe,text="Kalibrierungsmodul",padding=10,width=75,command=self.openWindowCal)
        calibration.grid(column=1,row=8,pady=5)
        #zum testen genutzt
        #button = ttk.Button(mainframe, text = "nächstes Fenster öffnen",command = self.openNewWindow)
        #button.grid(column=1,row=1)

        label = ttk.Label(mainframe, text="Modul wählen",font='30')
        label.grid(column=1,row=0)

        eb = ttk.Button(mainframe,text="Programm Beenden",command = self.destroy) 
        eb.grid(column=1,row=10)

    def openWindowSpannung(self):
        ModulSpannung() 

    def openWindowEeprom(self):
        ModulEeprom()

    def openWindowLadestrom(self):
        pass

    def openWindowTemp(self):
        ModulTemperatur()

    def openWindowCap(self):
        ModulKapazität()

    def openWindowCal(self):
        ModulKalibrierung()


#if __name__ == "__main__":
app = root()
app.mainloop()
        

