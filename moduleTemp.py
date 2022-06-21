
from re import T
from tkinter import *
from tkinter import ttk

from tools_V21 import *
from EepromData import *
from EepromAccess import *

class ModulTempHysterese(ttk.Frame):
    def __init__(self,parent):
        ttk.Frame.__init__(self,parent)

        #show actual charge parameters 
        self.chargePar = EepromChargeParam(self)
        self.chargePar.grid(column=0,row=2,sticky=S)
        

        self.meas = SensorRead(self)
        self.meas.grid(column=1,row=1,padx=5)
        
        self.valF = ttk.Frame(self, relief = 'ridge')
        self.valF.grid(column=0,row=1, sticky=NSEW)
        self.valF.columnconfigure(0,weight=1)
        self.valF.rowconfigure(0,weight=1)

        self.eeprom = EepromControl()
        self.eeprom.setEeprom()

        headLabel = ttk.Label(self,text="Temperaturgesteuerte Stromhysterese",font='10')
        headLabel.grid(column=0,row=0)

        ttk.Label(self.valF,text="Starttemperatur").grid(column=0,row=1)
        self.sgL = ttk.Combobox(self.valF,values=NTCTemps)
        self.sgL.grid(column=1,row=1,sticky=W)

        ttk.Label(self.valF,text="Endtemperatur").grid(column=0,row=3)
        self.egL = ttk.Combobox(self.valF,values=NTCTemps)
        self.egL.grid(column=1,row=3,sticky=W)

        ttk.Label(self.valF,text="Schrittzeit").grid(column=0,row=4)
        self.stepTime = ttk.Combobox(self.valF,values=list(range(11)))
        self.stepTime.grid(column=1,row=4,sticky=W)

    
        tempB = ttk.Button(self.valF,text="Test Starten",command = self.setTempToStartVal)
        tempB.grid(column=1, row=6)

        ttk.Label(self.valF,text="Manuelle Temperatureinstellung",font='10').grid(column=0,row=7)

        ttk.Label(self.valF,text="Neue Temperatur").grid(column=0,row=8)
        self.mTempL = ttk.Combobox(self.valF,values=NTCTemps)
        self.mTempL.grid(column=1,row=8,sticky=W)

        self.newTempB = ttk.Button(self.valF,text="Temperatur einstellen",command=self.setManualTemp)
        self.newTempB.grid(column=1,row=9)

        self.tempAktuell = 0
        ttk.Label(self.valF,text="Aktuelle Temperatur",font='15').grid(column=0,row=10)
        self.tAL = ttk.Label(self.valF,text=self.tempAktuell,font='15')
        self.tAL.grid(column=1,row=10)

        self.testStatus = ttk.Label(self.valF,text="Teststatus",font='15').grid(column=0,row=11)
        self.tSL = ttk.Label(self.valF,text="Okay",font='15')
        self.tSL.grid(column=1,row=11)

        eb = ttk.Button(self, text="Fenster schließen",command=self.destroy)
        eb.grid(column=2,row=20)

    def checkTestStatus(self):
        if self.meas.getCurrBat() == 0:
            self.tSL.configure(text="Ladegerät Error")
        self.tSL.after(2000,self.checkTestStatus)
        
    def setTempToStartVal(self):
        self.tempAktuell = int(self.sgL.get())
        self.tAL.configure(text=self.tempAktuell)
        self.tempHys()


    def tempHys(self):
        stepTimeinSecs = int(self.stepTime.get())*1000        
        if int(self.egL.get()) > int(self.sgL.get()):
            if self.tempAktuell != int(self.egL.get()):
                #refresh Temp in GUI
                self.tAL.configure(text=self.tempAktuell)
                #set InfoData[0](NTC Value) to actual value
                self.setNTCinEeprom(NTCTempValues[self.tempAktuell+35])
                self.tempAktuell += 1
                self.tAL.after(stepTimeinSecs,self.tempHys)

            elif self.tempAktuell == int(self.egL.get()):
                self.tAL.configure(text=self.tempAktuell)
                #set Temperature to start Value
                self.tempAktuell = int(self.sgL.get())
                #set actual Temp value in Infodata[0] and Arduino
                #self.setNTCinEeprom(NTCTempValues[self.tempAktuell+35])
        
        else:
            if self.tempAktuell != int(self.egL.get()):
                self.tAL.configure(text=self.tempAktuell)
                #set InfoData[0](NTC Value) to actual value
                self.setNTCinEeprom(NTCTempValues[self.tempAktuell+35])
                #send Value from InfoData to Arduino Eeprom
                self.tempAktuell -= 1
                self.tAL.after(stepTimeinSecs,self.tempHys)

            elif self.tempAktuell == int(self.egL.get()):
                self.tAL.configure(text=self.tempAktuell)
                #set Temperature to start Value
                self.tempAktuell = int(self.sgL.get())
                #set actual Temp value in Infodata[0]
                #self.setNTCinEeprom(NTCTempValues[self.tempAktuell+35])

    def setManualTemp(self):
        self.tempAktuell = int(self.mTempL.get())
        self.tAL.configure(text=self.tempAktuell)
        self.setNTCinEeprom(NTCTempValues[self.tempAktuell+35])

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

