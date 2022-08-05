from tkinter import ttk
from tkinter import *

from EepromData import *
from tools_V21 import *
from moduleEeprom import ModulEepromKomplett
import csv
import numpy

#class used to set offset values for ina226 measurement
class ModulKalibirerungAllgemein(ttk.Frame):
    def __init__(self,parent):
        ttk.Frame.__init__(self,parent)

        self.grid()

        self.meas = SensorRead(self)
        self.meas.grid(column=0,row=1)
        
        #initialize array for offset-values
        self.calibVals = [0,0,0,0]

        infoL = ttk.Label(self,text="Mit genauem Netzteil kalibrieren!")
        infoL.grid(column=1,row=1)

        #initialize gui elements
        ttk.Label(self,text="Shuntspannung Offset:").grid(column=0,row=2)
        #get ofsett-data from ina226
        self.shuntCalL = ttk.Label(self,text=self.meas.ina226_getShuntOffset())
        self.shuntCalL.grid(column=1,row=2)

        ttk.Label(self,text="Busspannung Offset:").grid(column=0,row=3)
        #get ofsett-data from ina226
        self.busCalL = ttk.Label(self,text=self.meas.ina226_getBusOffset())
        self.busCalL.grid(column=1,row=3)

        ttk.Label(self,text="Busstrom Offset:").grid(column=0,row=4)
        #get ofsett-data from ina226
        self.currCalL = ttk.Label(self,text=self.meas.ina226_getBusCurrOffset())
        self.currCalL.grid(column=1,row=4)

        ttk.Label(self,text="Leistung Offset:").grid(column=0,row=5)
        #get ofsett-data from ina226
        self.powCalL = ttk.Label(self,text=self.meas.ina226_getPowerOffset())
        self.powCalL.grid(column=1,row=5)

        #needed for selection of the value for the offset to be applied to
        self.calSelectCombo = ttk.Combobox(self,values=[
                                                        "Shunt-Offset[mV]",
                                                        "Bus-Offset[V]",
                                                        "Strom-Offset[A]",
                                                        "Power-Offset[W]"
                                                        ])

        ttk.Label(self,text="Was soll kalibriert werden?").grid(column=0,row=6)

        #comboboxes for selection of offset-value
        self.calSelectCombo.grid(column=0,row=7)
        self.calValCoarseCombo = ttk.Combobox(self,values=CalibrationCoarse)
        self.calValCoarseCombo.grid(column=1,row=7)
        self.calValFineCombo = ttk.Combobox(self,values=CalibrationFine)
        self.calValFineCombo.grid(column=2,row=7)

        #buttons for method-call
        ttk.Button(self,text="Aufaddieren", command=self.calibrateMeas_Add).grid(column=0,row=8)
        ttk.Button(self,text="Abziehen", command=self.calibrateMeas_Subtract).grid(column=1,row=8)

        #call method to get offset values from csv
        self.readCalValuesFromCSV()
        #call method to refresh all gui elements and set offset values in SensorRead class from values in csv
        self.setMeasCalibration()

    #if this method is called, the 
    #selected offset-value from comboboxes above is positive
    #and will be added to ina226 values
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
        
    #if this method is called, the 
    #selected offset-value from comboboxes above is negative
    #and will be subtracted from ina226 values
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

    #save new Offset-values to csv
    def saveCalValuesToCSV(self):
        f = open('calibVals.CSV','wb')
        writer = csv.writer(f)
        writer.writerow(self.calibVals)
        f.close()
        
    #get offset values from csv
    def readCalValuesFromCSV(self):
        f = open('calibVals.CSV')
        arr = numpy.loadtxt(f, delimiter=',')
        
        for p in range(size(arr)):
            self.calibVals[p] = arr[p]

    #set offset-values in Sensorread-class(controls the ina226)
    #refresh gui elements of Calibration class to latest offset-values
    def setMeasCalibration(self):
        self.meas.ina226_setShuntOffset(self.calibVals[0])
        self.meas.ina226_setBusVoltOffset(self.calibVals[1])
        self.meas.ina226_setBusCurrOffset(self.calibVals[2])
        self.meas.ina226_setBusPowerOffset(self.calibVals[3])

        self.shuntCalL.configure(text=self.meas.ina226_getShuntOffset())
        self.busCalL.configure(text=self.meas.ina226_getBusOffset())
        self.currCalL.configure(text=self.meas.ina226_getBusCurrOffset())
        self.powCalL.configure(text=self.meas.ina226_getPowerOffset())
            
#class for first calibration and synchronization after program startup
class ModulStartKalibrierung(Toplevel):
    def __init__(self,master = None):
        super().__init__(master = master)
        self.attributes('-fullscreen', True)

        ttk.Label(self,text="Parameter mit Arduino synchronisiert",font='20').grid(column=0,row=0,columnspan=10)
        
        #create object to control uart
        eeprom = EepromControl()
        #method to get all register values for eeprom on arduino
        eeprom.getArduinoEepromAndInfoData()
        #write eeprom-values received from arduino into eeprom-array in rapsberry pi
        eeprom.setEeprom()

        #used for eeprom register display
        counter = 0
        counter1 = 1

        #initialize arrays which hold gui elements for eeprom registers
        self.valueF = [ttk.Label] * 150
        self.lfF = [ttk.Labelframe] * 150

        #initialize gui elements
        self.modulcanvas = Canvas(self, width=700, height=400,borderwidth=0)
        self.modulcanvas.grid(column=0,row=1, columnspan=4, rowspan=2)

        self.modulframe = ttk.Frame(self.modulcanvas)
        self.modulframe.grid(column=0,row=0) 

        self.modulcanvas.create_window(0,0,anchor=NW, window=self.modulframe, tags="self.frame")
        self.modulframe.bind("<Configure>", self.onFrameConfigure)

        self.sb = ttk.Scrollbar(self, orient=HORIZONTAL)
        self.sb.grid(column=0,row=3, columnspan=4, sticky=EW)  

        eb = ttk.Button(self,text="Fenster schließen",command=self.destroy)
        eb.grid(column=0,row=10,sticky=W)

        self.modulcanvas.config(xscrollcommand=self.sb.set)
        self.sb.config(command=self.modulcanvas.xview)   
        self.modulcanvas.configure(scrollregion=self.modulcanvas.bbox("all"))
        
        #create elements for eeprom-register display
        for p in range(150):
            indexString = "Pos: {}".format(p)
            self.lfF[p] = ttk.Labelframe(self.modulframe,text=indexString)
            self.lfF[p].grid(column=counter,row=counter1,padx=1)

            counter1 += 1
            if counter1%11 == 0:
                counter += 1
                counter1 = 1
                
        #fill eeprom-register elements with data from Raspberry Pi eeprom
        for i in range(150):            
            self.valueF[i] = ttk.Label(self.lfF[i],text=hex(int(EepromDataComplete[i])))
            self.valueF[i].grid(column=1,row=0, sticky=EW)

        #gui elements to display information data
        ntcF = ttk.Labelframe(self,text="NTC-Wert")
        ntcF.grid(column=5,row=1, sticky=NSEW)

        ntcVal = ttk.Label(ntcF,text=InfoData[0],font='10')
        ntcVal.grid()

        ovF = ttk.Labelframe(self,text="OV-Wert")
        ovF.grid(column=5,row=2, sticky=NSEW)

        ovVal = ttk.Label(ovF,text=InfoData[1], font='10')
        ovVal.grid()


    #event to make scrollbar scrollable
    def onFrameConfigure(self,event):
        self.modulcanvas.configure(scrollregion=self.modulcanvas.bbox("all"))









