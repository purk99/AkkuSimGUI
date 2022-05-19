from threading import Thread
from tkinter import *
from tkinter import ttk
from time import sleep
from numpy import byte, float16, int16, uint16, uint8
import serial
from smbus2 import SMBus

from EepromData import *
from pigpio import *


class SensorRead(ttk.Frame):
    def __init__(self,parent):

        #I2C-Kommunikation initialisieren
        #self.ina226 = SMBus(1)
        self.ina226_adress = 0x40
        self.ina226 = pi()

        self.ina226_config_reg =    0   #R/W
        self.ina226_shunt_reg =     1   #R
        self.ina226_bus_reg =       2   #R
        self.ina226_power_reg =     3   #R
        self.ina226_curr_reg =      4   #R
        self.ina226_cal_reg =       5   #R/W

        self.currentLSB = float16
        self.cal = int16
        #I2C Ende

        #Werte zum Testen
        #self.ina226_calibrateReg(1,0.01)

        #self.i2c_bus = SMBus(1)
        #self.i2cadress = 0x31
        #i2c_sense.write_byte_data(i2cadressb,IOCON,0x02) 

        self.voltBat = float(10)
        self.voltCell = float(10)
        self.currBat = float(10)
        
        #dummywerte
        #self.voltage_meas = 18
        #self.current_meas = 5

        ttk.Frame.__init__(self, parent)

        sensFrame = self
        sensFrame.grid()

        vbl = ttk.Label(sensFrame, text="Spannung Batterie")
        vbl.grid(column=2,row=1)

        self.voltageBatl = ttk.Label(sensFrame, text = self.voltBat)
        self.voltageBatl.grid(column=3, row=1)

        self.vcl = ttk.Label(sensFrame,text="Spannung Zelle")
        self.vcl.grid(column=2,row=2)

        self.voltageCelll = ttk.Label(sensFrame, text = self.voltCell)
        self.voltageCelll.grid(column=3,row=2)

        ibl = ttk.Label(sensFrame,text="Batterie Gesamtstrom")
        ibl.grid(column=2,row=3)

        self.currentBatl = ttk.Label(sensFrame, text = self.currBat)
        self.currentBatl.grid(column=3,row=3)

        startMeasB = ttk.Button(sensFrame,text="Starte Messung",command=self.checkMeas)
        startMeasB.grid(column=3,row=4)

        calB = ttk.Button(sensFrame,text="Kalibrierung",command=self.calib)
        calB.grid(column=3,row=5)
        
    def calib(self):
        self.ina226_writeReg(self.ina226_cal_reg,10000)
        print(self.ina226_readReg(self.ina226_cal_reg))

    def checkMeas(self):
        #self.voltageBatl.configure(text = self.ina226_getBusVoltage())
        #self.currentBatl.configure(text = self.ina226_getCurr())
        #self.voltageCelll.configure(text = self.voltCell/5)
        self.test()
        self.voltageBatl.after(100,self.checkMeas)

    #Testfunktion zum Prüfen der Funktion von I2C Kommunikation
    def test(self):
        self.currentBatl.configure(text = self.ina226_getCurr())
        self.voltageCelll.configure(text = self.ina226_getShuntVoltage())
        self.voltageBatl.configure(text = self.ina226_getBusVoltage())

    def getVoltageBat(self):
        return self.voltBat

    def getVoltageCell(self):
        return self.voltCell

    def getCurrBat(self):
        return self.currBat

    #Auslesen von Register 
    def ina226_readReg(self,adress):
        regVal = int16
        h = self.ina226.i2c_open(1,self.ina226_adress)
        self.ina226.i2c_write_byte(h,adress)
        regVal =    self.ina226.i2c_read_byte(h) << 8
        regVal |=   self.ina226.i2c_read_byte(h)
        return regVal

    def ina226_writeReg(self,adress,content = int16):
        h = self.ina226.i2c_open(1,self.ina226_adress)
        self.ina226.i2c_write_i2c_block_data(h,adress,[(content >> 8),(content & 0xFF)])
        print("(writeReg)Sendebuffer Inhalt: ",end='\n')
        print(content)

    def ina226_getShuntVoltage(self):
        #self.ina226.write_byte(self.ina226_adress,self.ina226_bus_reg)
        #shuntVolt = (self.ina226.read_byte(self.ina226_adress) << 8)
        #shuntVolt |= self.ina226.read_byte(self.ina226_adress)
        shuntVolt = float((self.ina226_readReg(self.ina226_shunt_reg) * 2.5e-6)/2)
        return shuntVolt

    def ina226_getBusVoltage(self):
        busVolt = float(self.ina226_readReg(self.ina226_bus_reg) * 1.25e-3)
        return busVolt

    def ina226_getCurr(self):
        busCurr = float(self.ina226_readReg(self.ina226_curr_reg)*self.currentLSB)
        return busCurr

    def getPower(self):
        busPow = float(self.ina226_readReg(self.ina226_power_reg)*25*self.currentLSB)
        return busPow

    #eventuell currentLSB fest berechnen, wenn mit 20A gerechnet wird
    def ina226_calibrateReg(self, maxExpectCurr = uint16,rShunt = float16):
        self.currentLSB = maxExpectCurr/(2**15)
        self.cal = int16(0.00512/(self.currentLSB*rShunt))

        print(self.currentLSB,end='\t')
        print(self.cal)
        self.ina226_writeReg(self.ina226_cal_reg,self.cal)