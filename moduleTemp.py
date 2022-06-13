
from tkinter import *
from tkinter import ttk

from tools_V21 import *
from EepromData import *

class ModulTempHysterese(ttk.Frame):
    def __init__(self,parent):
        ttk.Frame.__init__(self,parent)

        self.meas = SensorRead(self)
        self.meas.grid(column=10,row=10)

        self.eeprom = EepromControl()

        headLabel = ttk.Label(self,text="Temperaturgesteuerte Stromhysterese",font='10')
        headLabel.grid(column=1,row=0)

        ttk.Label(self,text="Starttemperatur").grid(column=0,row=1)
        self.sgL = ttk.Combobox(self,values=TempDataValues)
        self.sgL.grid(column=1,row=1)

        ttk.Label(self,text="Endtemperatur").grid(column=0,row=3)
        self.egL = ttk.Combobox(self,values=TempDataValues)
        self.egL.grid(column=1,row=3)

        ttk.Label(self,text="Schrittzeit").grid(column=0,row=4)
        self.stepTime = ttk.Combobox(self,values=list(range(11)))
        self.stepTime.grid(column=1,row=4)

    
        tempB = ttk.Button(self,text="Test Starten",command = self.tempHys)
        tempB.grid(column=1, row=6)

        ttk.Label(self,text="Manuelle Temperatureinstellung",font='10').grid(column=1,row=7)

        ttk.Label(self,text="Neue Temperatur").grid(column=0,row=8)
        self.mTempL = ttk.Combobox(self,values=TempDataValues)
        self.mTempL.grid(column=1,row=8)

        self.newTempB = ttk.Button(self,text="Temperatur einstellen",command=self.setManualTemp)
        self.newTempB.grid(column=1,row=9)

        self.tempAktuell = 0
        ttk.Label(self,text="Aktuelle Temperatur",font='15').grid(column=0,row=10)
        self.tAL = ttk.Label(self,text=self.tempAktuell,font='15')
        self.tAL.grid(column=1,row=10)

        eb = ttk.Button(self, text="Fenster schließen",command=self.destroy)
        eb.grid(column=10,row=10)

    def tempHys(self):
        stepTimeinSecs = int(self.stepTime.get())*1000
        if int(self.egL.get()) > int(self.sgL.get()):
            if self.tempAktuell != int(self.egL.get()):
                #refresh Temp in GUI
                self.tAL.configure(text=self.tempAktuell)
                #set InfoData[0](NTC Value) to actual value
                self.setNTCinEeprom(self.tempAktuell)
                self.tempAktuell += 1
                self.tAL.after(stepTimeinSecs,self.tempHys)

            elif self.tempAktuell == int(self.egL.get()):
                self.tAL.configure(text=self.tempAktuell)
                #set Temperature to start Value
                self.tempAktuell = int(self.sgL.get())
                #set actual Temp value in Infodata[0] and Arduino
                self.setNTCinEeprom(self.tempAktuell)
        
        else:
            if self.tempAktuell != int(self.egL.get()):
                self.tAL.configure(text=self.tempAktuell)
                #set InfoData[0](NTC Value) to actual value
                self.setNTCinEeprom(self.tempAktuell)
                #send Value from InfoData to Arduino Eeprom
                self.tempAktuell -= 1
                self.tAL.after(stepTimeinSecs,self.tempHys)

            elif self.tempAktuell == int(self.egL.get()):
                self.tAL.configure(text=self.tempAktuell)
                #set Temperature to start Value
                self.tempAktuell = int(self.sgL.get())
                #set actual Temp value in Infodata[0]
                self.setNTCinEeprom(self.tempAktuell)

    def setManualTemp(self):
        self.tempAktuell = int(self.mTempL.get())
        self.tAL.configure(text=self.tempAktuell)

    def setNTCinEeprom(self,temp): 
        InfoData[0] = temp
        self.eeprom.writeNTC()

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

