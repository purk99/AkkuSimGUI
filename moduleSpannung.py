from tkinter import *
from tkinter import ttk
from turtle import bgcolor
from click import style

from tools_V21 import *

#class for test module "Tiefenentladung"
class ModulSpannungTEntladung(ttk.Frame):
    def __init__(self,parent):
        
        ttk.Frame.__init__(self,parent)
        self.grid(sticky=NSEW)
                   
        self.modulFrame = ttk.Labelframe(self,text="Modul Tiefenentladung")
        self.modulFrame.grid(column=0,row=0, sticky=NS)     
        
        #create countdown object
        self.cd = Countdown(self.modulFrame,30)
        self.cd.grid(column=0, row=1, padx=5, sticky=W)
        
        self.tSB = ttk.Button(self.modulFrame,text="Modul starten", command=self.startMeas)
        self.tSB.grid(column=5,row=2,padx=5,pady=5, ipadx=5)

        self.indText = "Test inaktiv"
        self.indLabel = ttk.Label(self.modulFrame, text=self.indText,font='15')
        self.indLabel.grid(column=0,row=2, padx=5, pady=5, sticky=W)

    #method called by button click
    def startMeas(self):
        #create object to communicate with ina226(no gui elements)      
        self.meas = SensorReadValuesOnly() 
        self.indLabel.configure(text="Test aktiv,\nwarte auf Ladestrom")
        #call next method
        self.waitForCurrent()
        

    def waitForCurrent(self):        
        #if measured bus-current > 1A
        if int(self.meas.ina226_getCurr()) > 1:
            #change displayed text in GUI
            self.indLabel.configure(text="Ladestrom liegt an")
            #call next method
            self.checkStatus()
            #start 30s countdown
            self.cd.countdown()
        #if measured bus-current < 1A
        else:
            #methods calls itself every 500 ms
            self.indLabel.after(500,self.waitForCurrent)
    
    #display status according to timer 
    #show time in seconds after charger error
    def checkStatus(self):
        errorCheck = False
        if int(self.meas.ina226_getCurr() < 1):
            outputString = "Ladegerät Error nach \n{} Sekunden".format((self.cd.getStartDur() - self.cd.getTime()))
            self.indLabel.configure(text=outputString)
            errorCheck = True

        if errorCheck == False:
            #method calls itself every 500 ms
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

#class for test module "Überladung/Imbalance"
class ModulSpannungUeIm(ttk.Frame):
    def __init__(self,parent):
        ttk.Frame.__init__(self,parent)

        #self.s = ttk.Style()
        #self.s.configure('ILabelFrame.Label',background = 'green')

        #initialize gui elements
        self.modulFrame = ttk.Labelframe(self,text="Modul Überladung/Imbalance")
        self.modulFrame.grid(column=5,row=0, columnspan=2, rowspan=2)  

        bSetUe = ttk.Button(self.modulFrame,text="Überspannungsflag setzen",command=self.setUeFlagActive)
        bSetUe.grid(column=0,row=1, sticky=EW)

        bUnSetUe = ttk.Button(self.modulFrame,text="Überspannungsflag deaktivieren", command=self.setUeFlagInactive)
        bUnSetUe.grid(column=0,row=2, sticky=EW)

        self.tsB = ttk.Button(self.modulFrame,text="Modul starten", command=self.startModule)
        self.tsB.grid(column=5,row=5,sticky=E)

        self.tStatusL = ttk.Label(self.modulFrame,text="Test inaktiv", font='15')
        self.tStatusL.grid(column=0,row=5, padx=5, pady=5, sticky=W)


    def startModule(self):

        #create object to control eeprom
        self.ser = EepromControl()

        #create object to communicate with ina226(no gui elements)
        self.meas = SensorReadValuesOnly()
        
        self.tStatusL.configure(text="Test aktiv,\nÜberspannung inaktiv")

    #set Overvoltage value to active 
    def setUeFlagActive(self):    
        #set eeprom-array on Raspberry Pi
        #send overvoltage value from eeprom-array(raspberry pi) to arduino
        self.ser.setOvValue(0xF0) 
        
        self.tStatusL.configure(text="Überspannung aktiv")
    
    #set Overvoltage value to inactive 
    def setUeFlagInactive(self):    
        #set eeprom-array on Raspberry Pi
        #send overvoltage value from eeprom-array(raspberry pi) to arduino
        self.ser.setOvValue(0x0F)     

        self.tStatusL.configure(text="Test aktiv,\nÜberspannung inaktiv")
       




