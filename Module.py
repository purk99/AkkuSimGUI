#####################################################
### File for Toplevel-Classes
### TopLevel Classes Generate new Windows
### which can be filled with Frames(other classes)
#####################################################

from re import T
from tkinter import ttk
from tkinter import *
from moduleEeprom import *

from moduleSpannung import *
from moduleEeprom import *
from moduleTemp import ModulTempNTCError
from moduleKapazität import *
from moduleCalibration import *
from tools_V21 import *
from EepromData import *

class ModulSpannung(Toplevel):
    def __init__(self, master = None):
        super().__init__(master = master)
        self.attributes('-fullscreen',True)
        
        eeprom = EepromControl()
        eeprom.setEeprom()
        
        self.modulframe = ttk.Frame(self)
        self.modulframe.grid(column=0,row=1,padx=3,pady=3, ipadx=3, ipady=3, columnspan=2)

        label2 = ttk.Label(self,text="Testmodul Spannung", font='30')
        label2.grid(column=1,row=0)
        
        self.meas = SensorRead(self.modulframe)
        self.meas.grid(column=1,row=0, ipady=3)

        self.vDisCh = ModulSpannungTEntladung(self.modulframe)
        self.vDisCh.grid(column=0,row=0,ipady=3, sticky=EW)

        self.oV = ModulSpannungUeIm(self.modulframe)
        self.oV.grid(column=0,row=1, sticky=NSEW)        

        eb = ttk.Button(self,text="Fenster schließen",command=self.destroy)
        eb.grid(column=0,row=5, ipadx=5, ipady=5 , sticky=E)

class ModulEeprom(Toplevel):
    def __init__(self,master = None):
        super().__init__(master = master)
        self.attributes('-fullscreen',True)

        self.eepromComplete = ModulEepromKomplett(self)
        self.eepromComplete.grid(column=0,row=0)

        eb = ttk.Button(self,text="Fenster schließen",command=self.destroy)
        eb.grid(column=0,row=1,sticky=W)

class ModulTemperatur(Toplevel):
    def __init__(self,master=None):
        super().__init__(master=master)
        self.attributes('-fullscreen', True)
        self.grid()

        #show actual charge parameters 
        self.chargePar = EepromChargeParam(self)
        self.chargePar.grid(column=0,row=2,sticky=S)
        
        self.meas = SensorRead(self)
        self.meas.grid(column=1,row=1,padx=3, sticky=N)
        
        self.ntc = ModulTempNTCError(self)
        self.ntc.grid(column=1,row=2,sticky=NSEW)
        
        self.valF = ttk.Labelframe(self,text="Temperaturhysterese")
        #self.valF = ttk.Frame(self, relief = 'ridge')
        self.valF.grid(column=0,row=1, sticky=NSEW)
        self.valF.columnconfigure(0,weight=1)
        self.valF.rowconfigure(0,weight=1)

        self.manTempF = ttk.Labelframe(self.valF,text="Manuelle Temperatur")
        self.manTempF.grid(columnspan=1,column=0,row=7, sticky=W)
        
        self.currTemp = ttk.Labelframe(self.valF, text="Aktuelle Temperatur")
        self.currTemp.grid(column=1, row=7, sticky=NSEW)

        self.eeprom = EepromControl()
        self.eeprom.setEeprom()

        headLabel = ttk.Label(self,text="Testmodul Temperatur",font='30')
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
        tempB.grid(column=1, row=6, sticky=EW)

        #ttk.Label(self.valF,text="Manuelle Temperatureinstellung",font='10').grid(column=0,row=7)

        ttk.Label(self.manTempF,text="Neue Temperatur").grid(column=0,row=0)
        self.mTempL = ttk.Combobox(self.manTempF,values=NTCTemps)
        self.mTempL.grid(column=1,row=0,sticky=W)

        self.newTempB = ttk.Button(self.manTempF,text="Temperatur einstellen",command=self.setManualTemp)
        self.newTempB.grid(column=1,row=1,sticky=EW)

        self.tempAktuell = InfoData[0]
        tempText = "{}°C".format(self.tempAktuell) 
        self.tAL = ttk.Label(self.currTemp,text=tempText,font=30)
        self.tAL.grid(padx=75,pady=20)

        #self.testStatus = ttk.Label(self.valF,text="Teststatus",font='15').grid(column=0,row=11)
        #self.tSL = ttk.Label(self.valF,text="Okay",font='15')
        #self.tSL.grid(column=1,row=11)

        eb = ttk.Button(self, text="Fenster schließen",command=self.destroy)
        eb.grid(column=1,row=10, sticky=E)

    def checkTestStatus(self):
        if self.meas.ina226_getCurrBat() == 0:
            self.tSL.configure(text="Ladegerät Error")
        self.tSL.after(2000,self.checkTestStatus)
        
    def setTempToStartVal(self):
        self.tempAktuell = int(self.sgL.get())
        self.tAL.configure(text=self.tempAktuell)
        self.ntc.refreshNTCValue("NTC Normalzustand")
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
        tempText = "{} °C".format(self.tempAktuell)
        self.tAL.configure(text=tempText)
        self.ntc.refreshNTCValue("NTC Normalzustand")
        self.setNTCinEeprom(NTCTempValues[self.tempAktuell+35])

    def setNTCinEeprom(self,temp): 
        self.eeprom.setNTCValue(temp)
        self.eeprom.writeNTC()

class ModulKapazität(Toplevel):
    def __init__(self,master = None):
        super().__init__(master = master)
        self.attributes('-fullscreen',True)

        self.modulframe = ttk.Frame(self, padding = 10)
        self.modulframe.grid()

        cF = ModulCapCapacity(self.modulframe)
        cF.grid(column=1,row=1)

        eb = ttk.Button(self.modulframe,text="Fenster schließen",command=self.destroy)
        eb.grid(column=10,row=10)        

class ModulKalibrierung(Toplevel):
    def __init__(self,master = None):
        super().__init__(master = master)
        self.attributes('-fullscreen',True)

        self.modulframe = ttk.Frame(self,padding = 10)
        self.modulframe.grid()

        ttk.Label(self.modulframe, text="Kalibrierungsmodul", padding=10, font='20').grid(column=0,row=0)

        cal = ModulKalibirerungAllgemein(self.modulframe)
        cal.grid(column=0,row=2)

        eb = ttk.Button(self.modulframe,text="Fenster schließen",command=self.destroy)
        eb.grid(column=10,row=10) 







