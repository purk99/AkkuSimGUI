from tkinter import ttk
from tkinter import *

from EepromData import *
from tools_V21 import *
import csv
import numpy

class ModulKalibirerungAllgemein(ttk.Frame):
    def __init__(self,parent):
        ttk.Frame.__init__(self,parent)

        self.grid()
        
        #needed for initialization of Eeprom Values
        eeprom = EepromControl()

        self.meas = SensorRead(self)
        self.meas.grid(column=0,row=1)
        
        self.calibVals = [0,0,0,0]

        infoL = ttk.Label(self,text="Mit genauem Netzteil kalibrieren!")
        infoL.grid(column=1,row=1)

        ttk.Label(self,text="Shuntspannung Offset:").grid(column=0,row=2)
        self.shuntCalL = ttk.Label(self,text=self.meas.ina226_getShuntOffset())
        #shuntCalL = ttk.Label(self,text=10)
        self.shuntCalL.grid(column=1,row=2)

        ttk.Label(self,text="Busspannung Offset:").grid(column=0,row=3)
        self.busCalL = ttk.Label(self,text=self.meas.ina226_getBusOffset())
        #self.busCalL = ttk.Label(self,text=10)
        self.busCalL.grid(column=1,row=3)

        ttk.Label(self,text="Busstrom Offset:").grid(column=0,row=4)
        self.currCalL = ttk.Label(self,text=self.meas.ina226_getBusCurrOffset())
        #currCalL = ttk.Label(self,text=10)
        self.currCalL.grid(column=1,row=4)

        ttk.Label(self,text="Leistung Offset:").grid(column=0,row=5)
        self.powCalL = ttk.Label(self,text=self.meas.ina226_getPowerOffset())
        #powCalL = ttk.Label(self,text=10)
        self.powCalL.grid(column=1,row=5)

        self.calSelectCombo = ttk.Combobox(self,values=[
                                                        "Shunt-Offset[mV]",
                                                        "Bus-Offset[V]",
                                                        "Strom-Offset[A]",
                                                        "Power-Offset[W]"
                                                        ])

        ttk.Label(self,text="Was soll kalibriert werden?").grid(column=0,row=6)


        self.calSelectCombo.grid(column=0,row=7)
        self.calValCoarseCombo = ttk.Combobox(self,values=CalibrationCoarse)
        self.calValCoarseCombo.grid(column=1,row=7)
        self.calValFineCombo = ttk.Combobox(self,values=CalibrationFine)
        self.calValFineCombo.grid(column=2,row=7)

        ttk.Button(self,text="Aufaddieren", command=self.calibrateMeas_Add).grid(column=0,row=8)
        ttk.Button(self,text="Abziehen", command=self.calibrateMeas_Subtract).grid(column=1,row=8)

        self.readCalValuesFromCSV()
        self.setMeasCalibration()

    def calibrateMeas_Add(self):
        switchVal = self.calSelectCombo.current()
        print(switchVal)
        if switchVal == 0:
            self.calibVals[0] = float(self.calValCoarseCombo.get())+float(self.calValFineCombo.get())
        if switchVal == 1:
            self.calibVals[1] = float(self.calValCoarseCombo.get())+float(self.calValFineCombo.get())
        if switchVal == 2:
            self.calibVals[2] = float(self.calValCoarseCombo.get())+float(self.calValFineCombo.get())
        if switchVal == 3:
            self.calibVals[3] = float(self.calValCoarseCombo.get())+float(self.calValFineCombo.get())
        self.setMeasCalibration()
        self.saveCalValuesToCSV()
        

    def calibrateMeas_Subtract(self):
        switchVal = self.calSelectCombo.current()
        if switchVal == 0:
            self.calibVals[0] = -1*(float(self.calValCoarseCombo.get())+float(self.calValFineCombo.get()))
        if switchVal == 1:
            self.calibVals[1] = -1*(float(self.calValCoarseCombo.get())+float(self.calValFineCombo.get()))
        if switchVal == 2:
            self.calibVals[2] = -1*(float(self.calValCoarseCombo.get())+float(self.calValFineCombo.get()))
        if switchVal == 3:
            self.calibVals[3] = -1*(float(self.calValCoarseCombo.get())+float(self.calValFineCombo.get()))
        self.setMeasCalibration()
        self.saveCalValuesToCSV()

    def saveCalValuesToCSV(self):

        f = open('calibVals.CSV','w')
        writer = csv.writer(f)
        writer.writerow(self.calibVals)
        f.close()
        

    def readCalValuesFromCSV(self):
        file = open('calibVals.CSV')
        arr = numpy.loadtxt(file, delimiter=',')
        
        for p in range(size(arr)):
            self.calibVals[p] = arr[p]

    def setMeasCalibration(self):
        self.meas.ina226_setShuntOffset(self.calibVals[0])
        self.meas.ina226_setBusVoltOffset(self.calibVals[1])
        self.meas.ina226_setBusCurrOffset(self.calibVals[2])
        self.meas.ina226_setBusPowerOffset(self.calibVals[3])

        self.shuntCalL.configure(text=self.meas.ina226_getShuntOffset())
        self.busCalL.configure(text=self.meas.ina226_getBusOffset())
        self.currCalL.configure(text=self.meas.ina226_getBusCurrOffset())
        self.powCalL.configure(text=self.meas.ina226_getPowerOffset())
            








