
from tkinter import *
from tkinter import ttk

from tools import *
from EepromData import *

class ModulTempHysterese(ttk.Frame):
    def __init__(self,parent):
        ttk.Frame.__init__(self,parent)

        headLabel = ttk.Label(self,text="Temperaturgesteuerte Stromhysterese")
        headLabel.grid(column=1,row=0)

        self.ug = 5
        ttk.Label(self,text="Untere Grenze").grid(column=0,row=2)
        ogL = ttk.Label(self,text=self.ug)
        ogL.grid(column=1,row=2)

        self.og = 10
        ttk.Label(self,text="Obere Grenze").grid(column=0,row=3)
        ugL = ttk.Label(self,text=self.og)
        ugL.grid(column=1,row=3)

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

        headLabel = ttk.Label(self,text="Prüfmodul NTC Error", font='20')
        headLabel.grid(column=1,row=0)

        shortB = ttk.Button(self,text="NTC kurzgeschlossen",command=self.shortNTC)
        shortB.grid(column=0,row=1)

        discB = ttk.Button(self,text="NTC ausgesteckt", command=self.discNTC)
        discB.grid(column=0,row=2)

    def shortNTC(self):
        ###0x25 ist nur Platzhalter
        #test = self.comm.readSingleRegister(0x25)
        test = 0x0

        if test != 0xf0:
            test = 0xf0

        #self.comm.writeSingleRegister(0x26,0x25,test)

        infoLabel = ttk.Label(self.modulframe,text="Display prüfen, NTC kurzgeschlossen")
        infoLabel.grid(column=0,row=5)

    def discNTC(self):
        ###0x25 ist nur Platzhalter
        #test = self.comm.readSingleRegister(0x25)
        test = 0

        if test != 0x0f:
            test = 0x0f

        #self.comm.writeSingleRegister(0x26,0x25,test)

        infoLabel = ttk.Label(self.modulframe, text="Display prüfen, NTC disconnect")
        infoLabel.grid(column=0,row=5)

