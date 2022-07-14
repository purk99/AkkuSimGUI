from tkinter import *
from tkinter import ttk
from turtle import bgcolor
from click import style

from tools_V21 import *

class ModulSpannungTEntladung(ttk.Frame):
    def __init__(self,parent):
    
        ttk.Frame.__init__(self,parent)
        self.grid(sticky=NSEW)
                   
        self.modulFrame = ttk.Labelframe(self,text="Modul Tiefenentladung")
        self.modulFrame.grid(column=0,row=0, sticky=NS)     
        
        self.cd = Countdown(self.modulFrame,30)
        self.cd.grid(column=0, row=1, padx=5, sticky=W)
        
        self.tSB = ttk.Button(self.modulFrame,text="Modul starten", command=self.startMeas)
        self.tSB.grid(column=5,row=2,padx=5,pady=5, ipadx=5)

        self.indText = "Test inaktiv"
        self.indLabel = ttk.Label(self.modulFrame, text=self.indText,font='15')
        self.indLabel.grid(column=0,row=2, padx=5, pady=5, sticky=W)

    def startMeas(self):
        #wait for test to start        
        self.meas = SensorReadValuesOnly() 
        self.indLabel.configure(text="Test aktiv,\nwarte auf Ladestrom")
        self.waitForCurrent()
        

    def waitForCurrent(self):        
        if int(self.meas.ina226_getCurr()) > 1:
            self.checkStatus()
            self.cd.countdown()
        else:
            self.indLabel.after(500,self.waitForCurrent)
    
    #display status according to timer 
    def checkStatus(self):
        errorCheck = False
        if int(self.meas.ina226_getCurr() < 1):
            outputString = "Ladegerät Error nach \n{} Sekunden".format(self.cd.getTime())
            self.indLabel.configure(text=outputString)
            errorCheck = True

        if errorCheck == False:
            self.indLabel.after(500,self.checkStatus) 
             
#currently not used
class ModulSpannungLSchluss(ttk.Frame):
    def __init__(self,parent):
        #super.__init__(self,parent)
        ttk.Frame.__init__(self,parent)
        
        self.modulFrame = ttk.Frame(self,relief='ridge')
        self.modulFrame.config(width=100,height=100)
        self.modulFrame.grid(column=5,row=0, columnspan=2, rowspan=2)

        headLabel = ttk.Label(self.modulFrame, text="Modul Ladeschlussspannung",font='20')
        headLabel.grid(column=0,row=0)


        maxBatVolt = ttk.Label(self,text="Ladeschlussspannung[V]:")
        maxBatVolt.grid(column=1,row=2)
        
        self.voltVal = 0
        self.maxBatVoltL = ttk.Label(self,text=self.voltVal)
        self.maxBatVoltL.grid(column=2,row=2)

        self.checkMaxVol()

    def checkMaxVol(self):
        actualVoltVal = self.meas.getVoltageBat
        if actualVoltVal > self.voltVal:
            self.voltVal = actualVoltVal
        self.maxBatVoltL.configure(text=self.voltVal)
        self.maxBatVoltL.after(1000,self.checkMaxVol)

class ModulSpannungUeIm(ttk.Frame):
    def __init__(self,parent):
        ttk.Frame.__init__(self,parent)

        self.ser = EepromControl()

        #self.s = ttk.Style()
        #self.s.configure('ILabelFrame.Label',background = 'green')

        self.modulFrame = ttk.Labelframe(self,text="Modul Überladung/Imbalance")
        self.modulFrame.grid(column=5,row=0, columnspan=2, rowspan=2)

        #headLabel = ttk.Label(self.modulFrame, text="Modul Überladung/Imbalance", font='10')
        #headLabel.grid(column=0,row=0, padx=2, pady=2, sticky=W)        

        bSetUe = ttk.Button(self.modulFrame,text="Überspannungsflag setzen",command=self.setUeFlagActive)#,style="ILabelFrame.Label")
        bSetUe.grid(column=0,row=1, sticky=EW)

        bUnSetUe = ttk.Button(self.modulFrame,text="Überspannungsflag deaktivieren", command=self.setUeFlagInactive)
        bUnSetUe.grid(column=0,row=2, sticky=EW)

        self.tsB = ttk.Button(self.modulFrame,text="Modul starten", command=self.startModule)
        self.tsB.grid(column=5,row=5,sticky=E)

        self.tStatusL = ttk.Label(self.modulFrame,text="Test inaktiv", font='15')
        self.tStatusL.grid(column=0,row=5, padx=5, pady=5, sticky=W)


    def startModule(self):
        self.meas = SensorReadValuesOnly()
        self.tStatusL.configure(text="Test aktiv,\nÜberspannung inaktiv")

    def setUeFlagActive(self):    
        self.ser.setOvValue(0xF0) 
        self.ser.writeOvervoltage()
        self.tStatusL.configure(text="Überspannung aktiv")
        
    def setUeFlagInactive(self):    
        self.ser.setOvValue(0x0F)     
        self.ser.writeOvervoltage()
        self.tStatusL.configure(text="Test aktiv,\nÜberspannung inaktiv")
       




