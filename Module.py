from re import T
from tkinter import ttk
from tkinter import *
#from moduleEeprom import *

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
        
        self.modulframe = ttk.Frame(self, relief='ridge')
        self.modulframe.grid(column=0,row=1)

        label2 = ttk.Label(self,text="Testmodul Spannung", font='30',padding=5)
        label2.grid(column=0,row=0)
        
        self.meas = SensorRead(self.modulframe)
        self.meas.grid(column=1,row=1)

        self.vDisCh = ModulSpannungTEntladung(self.modulframe)
        self.vDisCh.grid(column=0,row=1)

        self.oV = ModulSpannungUeIm(self.modulframe)
        self.oV.grid(column=0,row=2)        

        eb = ttk.Button(self,text="Fenster schließen",command=self.destroy)
        eb.grid(column=0,row=5, ipadx=5, ipady=5 , sticky=E)

class ModulEeprom(Toplevel):
    def __init__(self,master = None):
        super().__init__(master = master)
        self.attributes('-fullscreen',True)

        self.eeprom = EepromControl()
        self.eeprom.setEeprom()

        self.grid()

        counter = 0
        counter1 = 1

        valueF = [ttk.Label] * 135
        lfF = [ttk.Labelframe] * 135

        self.modulframe = ttk.Frame(self, padding=10)
        self.modulframe.grid(column=0,row=1)

        headLabel = ttk.Label(self, text="EEPROM Daten",font='15')
        headLabel.grid(column=0,row=0)

        for p in range(135):
            indexString = "Pos: {}".format(p)
            lfF[p] = ttk.Labelframe(self.modulframe,text=indexString)
            lfF[p].grid(column=counter,row=counter1,padx=1)

            counter1 += 1
            if p%10 == 9:
                counter += 1
                counter1 = 1
        
        for i in range(135):            
            valueF[i] = ttk.Label(lfF[i],text=hex(EepromDataComplete[i]))
            valueF[i].grid(column=1,row=0, sticky=EW)

        eb = ttk.Button(self,text="Fenster schließen",command=self.destroy)
        eb.grid(column=10,row=10)

class ModulTemperatur(Toplevel):
    def __init__(self,master=None):
        super().__init__(master=master)
        self.attributes('-fullscreen', True)
        self.grid()

        #show actual charge parameters 
        self.chargePar = EepromChargeParam(self)
        self.chargePar.grid(column=0,row=2,sticky=S)
        
        self.meas = SensorRead(self)
        self.meas.grid(column=1,row=1,padx=5)
        
        self.ntc = ModulTempNTCError(self)
        self.ntc.grid(column=1,row=2,sticky=NSEW)
        
        self.valF = ttk.Frame(self, relief = 'ridge')
        self.valF.grid(column=0,row=1, sticky=NSEW)
        self.valF.columnconfigure(0,weight=1)
        self.valF.rowconfigure(0,weight=1)

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
        tempB.grid(column=1, row=6)

        ttk.Label(self.valF,text="Manuelle Temperatureinstellung",font='10').grid(column=0,row=7)

        ttk.Label(self.valF,text="Neue Temperatur").grid(column=0,row=8)
        self.mTempL = ttk.Combobox(self.valF,values=NTCTemps)
        self.mTempL.grid(column=1,row=8,sticky=W)

        self.newTempB = ttk.Button(self.valF,text="Temperatur einstellen",command=self.setManualTemp)
        self.newTempB.grid(column=1,row=9)

        self.tempAktuell = self.eeprom.readNTC()
        ttk.Label(self.valF,text="Aktuelle Temperatur",font='15').grid(column=0,row=10)
        self.tAL = ttk.Label(self.valF,text=self.tempAktuell,font='15')
        self.tAL.grid(column=1,row=10)

        self.testStatus = ttk.Label(self.valF,text="Teststatus",font='15').grid(column=0,row=11)
        self.tSL = ttk.Label(self.valF,text="Okay",font='15')
        self.tSL.grid(column=1,row=11)

        eb = ttk.Button(self, text="Fenster schließen",command=self.destroy)
        eb.grid(column=1,row=10)

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
        self.tAL.configure(text=self.tempAktuell)
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







