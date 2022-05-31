from threading import Thread
from tkinter import *
from tkinter import ttk
from time import sleep
from numpy import byte, float16, int16, uint16, uint8
import serial
from smbus2 import SMBus

from EepromData import *
from pigpio import *

START_BIT = 0x02
STOP_BIT = 0x03

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


        self.voltBat = float(10)
        self.voltCell = float(10)
        self.currBat = float(10)

        self.busVoltOffset = 0
        self.shuntVoltOffset = 0
        self.busCurrOffset = 0
        self.powerOffset = 0
        
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
        #Config-register beschreiben
        #0100 0101 1010 1111 = 0x45AF
        self.ina226_writeReg(self.ina226_config_reg,0x45AF)

        #Kalibrierungsregister beschreiben
        self.ina226_calibrateReg(5,0.01)

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

    #Auslesen von Register 
    def ina226_readReg(self,adress):
        h = self.ina226.i2c_open(1,self.ina226_adress)
        #self.ina226.i2c_write_byte(h,adress)
        recVal =    uint16(self.ina226.i2c_read_word_data(h,adress))
        regVal =    uint16((recVal >> 8)|(recVal << 8))
        self.ina226.i2c_close(h)
        return regVal

    def ina226_writeReg(self,adress,content = int16):
        h = self.ina226.i2c_open(1,self.ina226_adress)
        test = [content >> 8, content & 0xff]
        self.ina226.i2c_write_i2c_block_data(h,adress,test)
        self.ina226.i2c_close(h)

    #eventuell currentLSB fest berechnen, wenn mit 20A gerechnet wird
    def ina226_calibrateReg(self, maxExpectCurr = uint16,rShunt = float16):
        self.currentLSB = maxExpectCurr/(2**15)
        self.cal = uint16(0.00512/(self.currentLSB*rShunt))
        self.ina226_writeReg(self.ina226_cal_reg,self.cal)

    def ina226_getShuntVoltage(self):
        shuntVolt = float((self.ina226_readReg(self.ina226_shunt_reg) * 2.5e-6) + (self.shuntVoltOffset*2.5e-6))
        return round(shuntVolt,4)

    def ina226_getBusVoltage(self):
        busVolt = float(self.ina226_readReg(self.ina226_bus_reg) * 1.25e-3 + self.busVoltOffset)
        return round(busVolt,2)

    def ina226_getCurr(self):
        busCurr = float(self.ina226_readReg(self.ina226_curr_reg)*self.currentLSB + self.busCurrOffset)
        return round(busCurr,2)

    def getPower(self):
        busPow = float(self.ina226_readReg(self.ina226_power_reg)*25*self.currentLSB + self.powerOffset)
        return busPow

    def getVoltageBat(self):
        return self.voltBat

    def getVoltageCell(self):
        return self.voltCell

    def getCurrBat(self):
        return self.currBat
    
    def setShuntOffset(self,offset):
        self.shuntVoltOffset = offset
    
    def setBusVoltOffset(self,offset):
        self.busVoltOffset = offset
    
    def setBusCurrOffset(self,offset):
        self.busCurrOffset = offset

    def setBusPowerOffset(self,offset):
        self.powerOffset = offset


class Countdown(ttk.Frame):
    def __init__(self,parent,duration):
        ttk.Frame.__init__(self, parent)
        #super().__init__()
        
        self.grid()

        #variable für Ausgabe
        #ÄNDERN AUF 30, NUR ZUM TESTEN AUF 10
        self.dur = duration
        self.durStart = self.dur
        self.secFormat = self.dur

        self.tl = ttk.Label(self, text=self.secFormat)
        self.tl.grid(column=2,row=1)

        self.sb = ttk.Button(self,text="Counter starten", command = self.countdown)
        self.sb.grid(column=1,row=1)

###########################################################
###         damit über mehrere Funktionen auf Variablen
###         zugegriffen werden kann
###         --> self. vor jede variable, damit wird
##                          Klassenvariable erzeugt

    #Hier wird countdown erzeugt
    #callback nach 1s auf Funktion selbst
    #--> python after()
    def countdown(self):
        if self.dur >= 0:   
            self.secFormat = '{:02d}'.format(self.dur)
            self.tl.after(1000,self.countdown)
            #schedule timer to update icon every second
            self.tl.configure(text=self.secFormat)
            self.dur -= 1
        #um Timer wieder starten zu können
        #self.dur wird auf durStart +1 gesetzt, damit Variablen 
        #in Abhängigkeit von self.dur nicht sofort wieder umspringen, sondern erst nach neuem Start
        else:
            self.dur = self.durStart + 1
    
    #Hilfsfunktionen
    def getTime(self):
        return self.dur
    def getStartDur(self):
        return self.durStart

#für UART-Kommunikation
class EepromControl():
    def __init__(self):
        #super().__init__()
        self.sendBuffer = bytearray(5)
        self.receiveBuffer = bytearray(3)
        self.ser = serial.Serial("/dev/ttyS0", 9600)

    def sendPackage(self,id,adress,content):
        self.sendBuffer[0] = START_BIT
        self.sendBuffer[1] = id
        self.sendBuffer[2] = adress
        self.sendBuffer[3] = content
        self.sendBuffer[4] = STOP_BIT
        self.ser.write(self.sendBuffer)

    def receivePackage(self):
        self.receiveBuffer = self.ser.read(3)
        
        payload = (self.receiveBuffer[1])
        if self.receiveBuffer[0] == START_BIT & self.receiveBuffer[2] == STOP_BIT:
            return payload

    def readSingleRegister(self,adress):
        self.sendPackage(uartCMD["eepromReadSingleReg"], adress, 1)
        
    def readAllRegisters(self):
        self.sendPackage(uartCMD["eepromReadAll"],0,1)

    def writeSingleRegister(self,adress,content):
        self.sendPackage(uartCMD["eepromWriteSingleReg"],adress,content)

    def readNTC(self):
        self.sendPackage(uartCMD["readNTC"],1,1)
        rec = self.receivePackage()
        ntcVal = rec[0]
        return ntcVal

    def writeNTC(self):
        self.sendPackage(uartCMD["writeNTC"],1,InfoData[0])

    #muss noch zu Ende geschrieben werden
    def readOverVoltage(self):
        self.sendPackage(uartCMD)

#Ermöglicht Konvertieren von EEPROM Werten in auslesbare Werte
class HexValConvert():
    def __init__(self):
        dummyVal = 0

    def shiftLeftByXPos(self,startVal,howMany):
        return uint8(startVal << howMany)

    def shiftRightByXPos(self,startVal,howMany):
        return uint8(startVal >> howMany)