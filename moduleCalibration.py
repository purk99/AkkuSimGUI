from ast import match_case
from difflib import Match
from tkinter import ttk
from tkinter import *
from EepromData import *
from tools_V21 import SensorRead

class ModulKalibirerungAllgemein(ttk.Frame):
    def __init__(self,parent):
        ttk.Frame.__init__(self,parent)

        self.grid()

        self.meas = SensorRead(self)
        #self.meas.grid(column=5,row=1)

        infoL = ttk.Label(self,text="Mit genauem Netzteil kalibrieren!")
        infoL.grid(column=1,row=1)

        ttk.Label(self,text="Shuntspannung Offset:").grid(column=0,row=2)
        #shuntCalL = ttk.Label(self,text=self.meas.ina226_getShuntVoltage())
        shuntCalL = ttk.Label(self,text=10)
        shuntCalL.grid(column=1,row=2)

        ttk.Label(self,text="Busspannung Offset:").grid(column=0,row=3)
        #busCalL = ttk.Label(self,text=self.meas.ina226_getBusVoltage())
        busCalL = ttk.Label(self,text=10)
        busCalL.grid(column=1,row=3)

        ttk.Label(self,text="Busstrom Offset:").grid(column=0,row=4)
        #currCalL = ttk.Label(self,text=self.meas.ina226_getCurr())
        currCalL = ttk.Label(self,text=10)
        currCalL.grid(column=1,row=4)

        ttk.Label(self,text="Leistung Offset:").grid(column=0,row=5)
        #powCalL = ttk.Label(self,text=self.meas.getPower())
        powCalL = ttk.Label(self,text=10)
        powCalL.grid(column=1,row=5)

        self.calSelectCombo = ttk.Combobox(self,values=[
                                                        "Shunt-Offset[mV]",
                                                        "Bus-Offset[V]",
                                                        "Strom-Offset[A]",
                                                        "Power-Offset[W]"
                                                        ])

        ttk.Label(self,text="Was soll kalibriert werden?").grid(column=0,row=6)


        self.calSelectCombo.grid(column=0,row=7)
        self.calValFineCombo = ttk.Combobox(self,values=CalibrationCoarse)
        self.calValFineCombo.grid(column=1,row=7)
        self.calValCoarseCombo = ttk.Combobox(self,values=CalibrationFine)
        self.calValCoarseCombo.grid(column=2,row=7)

        ttk.Button(self,text="Aufaddieren").grid(column=0,row=8)
        ttk.Button(self,text="Abziehen").grid(column=1,row=8)

    def calibrateMeas_Add(self):
        switchVal = self.calSelectCombo.current()
        match switchVal:
            case 0: self.meas.setShuntOffset(int(self.calValCoarseCombo.get()+self.calValFineCombo.get()))
            case 1: self.meas.setBusVoltOffset(int(self.calValCoarseCombo.get()+self.calValFineCombo.get()))
            case 2: self.meas.setBusCurrOffset(int(self.calValCoarseCombo.get()+self.calValFineCombo.get()))
            case 3: self.meas.setBusPowerOffset(int(self.calValCoarseCombo.get()+self.calValFineCombo.get()))

    def calibrateMeas_Subtract(self):
        switchVal = self.calSelectCombo.current()
        match switchVal:
            case 0: self.meas.setShuntOffset(-1*int(self.calValCoarseCombo.get()+self.calValFineCombo.get()))
            case 1: self.meas.setBusVoltOffset(-1*int(self.calValCoarseCombo.get()+self.calValFineCombo.get()))
            case 2: self.meas.setBusCurrOffset(-1*int(self.calValCoarseCombo.get()+self.calValFineCombo.get()))
            case 3: self.meas.setBusPowerOffset(-1*int(self.calValCoarseCombo.get()+self.calValFineCombo.get()))
        
        








