
from tkinter import *
from tkinter import ttk

from tools_V21 import *
from EepromData import *

class ModulTempHysterese(ttk.Frame):
    def __init__(self,parent):
        ttk.Frame.__init__(self,parent)

        headLabel = ttk.Label(self,text="Temperaturgesteuerte Stromhysterese")
        headLabel.grid(column=1,row=0)

        self.ug = 5
        ttk.Label(self,text="Starttemperatur").grid(column=0,row=1)
        self.ogL = ttk.Combobox(self,textvariable=TempDataValues)
        self.ogL.grid(column=1,row=1)

        self.og = 10
        ttk.Label(self,text="Endtemperatur").grid(column=0,row=3)
        self.ugL = ttk.Label(self,text=self.og)
        self.ugL.grid(column=1,row=3)

        self.tempAktuell = self.ug
        ttk.Label(self,text="Aktuelle Temperatur").grid(column=0,row=4)
        self.tAL = ttk.Label(self,text=self.tempAktuell)
        self.tAL.grid(column=1,row=4)

        tempB = ttk.Button(self,text="Test Starten",command = self.tempHys)
        tempB.grid(column=1, row=5)

        #meas = SensorRead(self)
        #meas.grid(column=10,row=10)

        eb = ttk.Button(self, text="Fenster schließen",command=self.destroy)
        eb.grid(column=10,row=10)

    def tempHys(self):
        if self.tempAktuell != self.og:
            self.tAL.configure(text=self.tempAktuell)
            self.tempAktuell += 1
            self.tAL.after(1000,self.tempHys)
        elif self.tempAktuell == self.og:
            self.tAL.configure(text=self.tempAktuell)
            self.tempAktuell = self.ug

class ModulTempNTCError(ttk.Frame):
    def __init__(self,parent):
        ttk.Frame.__init__(self,parent)

        self.modulframe = self

        #erst auf Raspbi aktivieren, sonst Error
        self.comm = EepromControl()

        self.meas = SensorRead(self)
        self.meas.grid(column=1,row=1)

        headLabel = ttk.Label(self,text="Prüfmodul NTC Error", font='20')
        headLabel.grid(column=1,row=0)

        self.shortB = ttk.Button(self,text="NTC kurzschließen",command=self.shortNTC)
        self.shortB.grid(column=0,row=1)

        self.discB = ttk.Button(self,text="NTC ausstecken", command=self.discNTC)
        self.discB.grid(column=0,row=2)

        self.infoL = ttk.Label(self,text="NTC Normalzustand")
        self.infoL.grid(column=0,row=5)

    def shortNTC(self):
        test = self.comm.readSingleRegister(0x2)

        if test != 0xf0:
            test = 0xf0

        self.comm.writeSingleRegister(0x2,test)

        self.infoL.configure(text="NTC kurzgeschlossen")

    def discNTC(self):
        test = self.comm.readSingleRegister(0x2)
        test = 0

        if test != 0x0f:
            test = 0x0f

        self.comm.writeSingleRegister(0x2,test)
        self.infoL.configure(text="NTC ausgesteckt")

