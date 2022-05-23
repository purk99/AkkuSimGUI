from json import tool
from tkinter import *
from tkinter import ttk
from turtle import bgcolor
from unittest import TestCase

from click import style

from tools import *

class ModulSpannungTEntladung(ttk.Frame):
    def __init__(self,parent):
        #super.__init__(self,parent)

        ttk.Frame.__init__(self,parent)

        self.modulFrame = self
        self.modulFrame.config(width=100,height=100)
        self.modulFrame.grid(column=5,row=0, columnspan=2, rowspan=2)

        headLabel = ttk.Label(self.modulFrame, text="Modul Tiefenentladung",font='10')
        headLabel.grid(column=1,row=0)

        self.indText = "reduzierter Ladestrom"
        self.indLabel = ttk.Label(self.modulFrame, text=self.indText)
        self.indLabel.grid(column=0,row=3)

        self.meas = SensorRead(self.modulFrame)
        self.meas.grid(column=1,row=1)

        self.deepDischarge()

    def deepDischarge(self):
        #auf Teststart warten
        
        self.cd = Countdown(self.modulFrame,30)
        '''
        self.cd.grid(column=1,row=2)
            #zeit starten, bis t=30s muss spannung gestiegen sein
        self.indLabel.after(1000,self.checkCountStatus)
        '''
        
    #Prüfen des Status des Timers, um Variable zu setzen
    #eventuell in tools.py verlegen
    def checkStatus(self):
            #'ÄNDERN AUF 30
        if self.meas.getVoltageCell > 0 & self.meas.getVoltageCell < 2.5:
            self.indLabel.configure(text="Reduzierter Ladestrom")
        
        if self.meas.getVoltageCell < 2.5 & self.cd.getTime() == 0:
            self.indLabel.configure(text="Ladegerät Error, LED prüfen")

        if self.meas.getVoltageCell > 2.5:
            self.indLabel.configure(text="voller Ladestrom")

        if self.cd.getTime() == self.cd.getStartDur():
            self.indLabel.configure(text=self.indText)
        self.indLabel.after(1000,self.checkStatus)      
                
class ModulSpannungLSchluss(ttk.Frame):
    def __init__(self,parent):
        #super.__init__(self,parent)
        ttk.Frame.__init__(self,parent)
        
        self.modulFrame = self
        self.modulFrame.config(width=100,height=100)
        self.modulFrame.grid(column=5,row=0, columnspan=2, rowspan=2)

        headLabel = ttk.Label(self.modulFrame, text="Modul Ladeschlussspannung",font='10')
        headLabel.grid(column=1,row=0)

        self.meas = SensorRead(self.modulFrame)
        self.meas.grid(column=1,row=1)

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

        self.s = ttk.Style()
        self.s.configure('ILabelFrame.Label',background = 'green')

        self.modulFrame = self
        self.modulFrame.config(width=100,height=100)
        self.modulFrame.grid(column=5,row=0, columnspan=2, rowspan=2)

        headLabel = ttk.Label(self.modulFrame, text="Modul Überladung/Imbalance", font='10')
        headLabel.grid(column=1,row=0)

        meas = SensorRead(self)
        meas.grid(column=1,row=1)

        self.SetUeFlagActiveFrame = ttk.Labelframe(self,style="ILabelFrame.Label")
        self.SetUeFlagActiveFrame.grid(column=1,row=2)

        bSetUe = ttk.Button(self.SetUeFlagActiveFrame,text="Überspannungsflag setzen",command=self.setUeFlagActive)#,style="ILabelFrame.Label")
        bSetUe.grid(column=1,row=3)

        bUnSetUe = ttk.Button(self.SetUeFlagActiveFrame,text="Überspannungsflag deaktivieren", command=self.setUeFlagInactive)
        bUnSetUe.grid(column=1,row=4)

    def setUeFlagActive(self):
        self.ser = EepromControl()
        self.ser.sendPackage(0x30,0)
        if self.ser.receivePackage() == 1:
            self.SetUeFlagActiveFrame.configure(bg = 'green')

    def setUeFlagInactive(self):
        self.ser = EepromControl()
        self.ser.sendPackage(0x30,1)
        if self.ser.receivePackage() == 1:
            self.SetUeFlagActiveFrame.configure(bg = '0xff')




