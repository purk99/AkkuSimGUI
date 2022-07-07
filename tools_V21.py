from threading import Thread
from tkinter import *
from tkinter import ttk
from time import sleep
from numpy import byte, float16, int16, uint16, uint8
import serial
from smbus2 import SMBus
import csv
import numpy

from EepromData import *
from pigpio import *

START_BIT = 0x02
STOP_BIT = 0x03

#neuer Kommentar

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

        self.maxExpCurr = 10
        self.shuntResValue = 0.00475

        self.voltBat = float(10)
        self.voltCell = float(10)
        self.currBat = float(10)
        self.powBat = float(10)

        self.busVoltOffset = 0
        self.shuntVoltOffset = 0
        self.busCurrOffset = 0
        self.powerOffset = 0
        
        #dummywerte
        #self.voltage_meas = 18
        #self.current_meas = 5

        ttk.Frame.__init__(self, parent)
        
        self.grid(sticky=NSEW)

        sensFrame = ttk.Frame(self,relief='ridge')
        sensFrame.grid(padx=3, pady=3, sticky=NSEW)

        vbl = ttk.Label(sensFrame, text="Spannung Batterie", font=20)
        vbl.grid(column=0,row=1, sticky=W)

        self.voltageBatl = ttk.Label(sensFrame, text = self.voltBat, font=20)
        self.voltageBatl.grid(column=1, row=1, padx=5)

        self.vcl = ttk.Label(sensFrame,text="Spannung Zelle", font=20)
        self.vcl.grid(column=0,row=2, sticky=W)

        self.voltageCelll = ttk.Label(sensFrame, text = self.voltCell, font=20)
        self.voltageCelll.grid(column=1,row=2, padx=5)

        ibl = ttk.Label(sensFrame,text="Batterie Gesamtstrom", font=20)
        ibl.grid(column=0,row=3, sticky=W)

        self.currentBatl = ttk.Label(sensFrame, text = self.currBat, font=20)
        self.currentBatl.grid(column=1,row=3, padx=5)

        self.sVL = ttk.Label(sensFrame, text="Shuntspannung", font=20)
        self.sVL.grid(column=0,row=4, padx=5)

        self.shuntVoltL = ttk.Label(sensFrame,text=self.powBat, font=20)
        self.shuntVoltL.grid(column=1,row=4,padx=5)

        startMeasB = ttk.Button(sensFrame,text="Starte Messung",command=self.checkMeas)
        startMeasB.grid(column=0,row=5, pady=2, sticky=EW)

        #calB = ttk.Button(sensFrame,text="Neukalibrierung",command=self.calib)
        #calB.grid(column=0,row=5)

        self.ina226_writeReg(self.ina226_config_reg, 0x45A7)
        self.ina226_calibrateReg(self.maxExpCurr,self.shuntResValue)
        self.readCalibrationValuesFromCSV()
        
    #def calib(self):
    #   #Config-register beschreiben
    #    self.ina226_calibrateReg(6,0.01)

    def checkMeas(self):
        self.updateValues()
        self.voltageBatl.after(100,self.checkMeas)

    #Testfunktion zum Prüfen der Funktion von I2C Kommunikation
    def updateValues(self):
        cellVoltage = self.ina226_getBusVoltage()/int(EepromDataComplete[2])
        self.currentBatl.configure(text = '{:05.2f}'.format(self.ina226_getCurr()))
        self.voltageCelll.configure(text = '{:05.2f}'.format(cellVoltage))#round(cellVoltage,4)
        self.voltageBatl.configure(text = '{:05.2f}'.format(self.ina226_getBusVoltage()))
        self.shuntVoltL.configure(text='{:05.2f}'.format(self.ina226_getShuntVoltage()))

    #Auslesen von Register 
    def ina226_readReg(self,adress):
        h = self.ina226.i2c_open(1,self.ina226_adress)
        #self.ina226.i2c_write_byte(h,adress)
        recVal =    uint16(self.ina226.i2c_read_word_data(h,adress))
        regVal =    uint16((recVal >> 8)|(recVal << 8))
        self.ina226.i2c_close(h)
        return regVal

    def ina226_writeReg(self,adress,content = uint16):
        h = self.ina226.i2c_open(1,self.ina226_adress)
        test = [content >> 8, content & 0xff]
        self.ina226.i2c_write_i2c_block_data(h,adress,test)
        self.ina226.i2c_close(h)

    #eventuell currentLSB fest berechnen, wenn mit 20A gerechnet wird
    def ina226_calibrateReg(self, maxExpectCurr = uint16,rShunt = float16):
        self.currentLSB = maxExpectCurr/(2**15)
        #self.currentLSB = 0.5e-3
        self.cal = uint16(0.00512/(self.currentLSB*rShunt))
        #self.cal = uint16(1707)
        self.ina226_writeReg(self.ina226_cal_reg,self.cal)

    def readCalibrationValuesFromCSV(self):
        file = open('calibVals.CSV')
        arr = numpy.loadtxt(file, delimiter=',')
        
        self.shuntVoltOffset    = arr[0]
        self.busVoltOffset      = arr[1]
        self.busCurrOffset      = arr[2]
        self.powerOffset        = arr[3]
       

    #kann zu testzwecken ausgelesen werden
    def ina226_getShuntVoltage(self):
        shuntVolt = float((int16(self.ina226_readReg(self.ina226_shunt_reg)) * 2.5e-3)/2 + (self.shuntVoltOffset))
        return round(shuntVolt,4)

    def ina226_getBusVoltage(self):
        busVolt = float((self.ina226_readReg(self.ina226_bus_reg) * 1.25e-3) + self.busVoltOffset)
        return round(busVolt,2)

    def ina226_getCurr(self):
        busCurr = float((int16(self.ina226_readReg(self.ina226_curr_reg))*self.currentLSB) + self.busCurrOffset)
        #busCurr = float((int16(self.ina226_readReg(self.ina226_curr_reg))*0.5e-3) + self.busCurrOffset)
        #busCurr = float(((self.ina226_readReg(self.ina226_curr_reg))*self.currentLSB) + self.busCurrOffset)
        
        return round(busCurr,2)

    def ina226_getPower(self):
        busPow = float(self.ina226_readReg(self.ina226_power_reg)*25*self.currentLSB + self.powerOffset)
        return busPow

    def ina226_getVoltageBat(self):
        return self.voltBat

    def ina226_getVoltageCell(self): 
        return self.voltCell

    def ina226_getCurrBat(self):
        return self.currBat
    
    def ina226_setShuntOffset(self,offset):
        self.shuntVoltOffset = offset
    
    def ina226_setBusVoltOffset(self,offset):
        self.busVoltOffset = offset
    
    def ina226_setBusCurrOffset(self,offset):
        self.busCurrOffset = offset

    def ina226_setBusPowerOffset(self,offset):
        self.powerOffset = offset

    def ina226_setMaxExpCurr(self,value):
        self.maxExpCurr = int(value)

    def ina226_setShuntResValue(self,value):
        self.shuntResValue = int(value)
    
    def ina226_getShuntOffset(self):
        return self.shuntVoltOffset

    def ina226_getBusOffset(self):
        return self.busVoltOffset

    def ina226_getBusCurrOffset(self):
        return self.busCurrOffset

    def ina226_getPowerOffset(self):
        return self.powerOffset

    def ina226_getMaxExpCurr(self):
        return self.maxExpCurr

    def ina226_getShuntResValue(self):
        return self.shuntResValue
    


class SensorReadValuesOnly():
    def __init__(self):
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

        self.maxExpCurr = 10
        self.shuntResValue = 0.00475

        self.voltBat = float(10)
        self.voltCell = float(10)
        self.currBat = float(10)

        self.busVoltOffset = 0
        self.shuntVoltOffset = 0
        self.busCurrOffset = 0
        self.powerOffset = 0

        #initialize calibration Register on INA226 Chip
        self.ina226_calibrateReg(self.maxExpCurr,self.shuntResValue)
        self.ina226_writeReg(self.ina226_config_reg, 0x45A7)
        #read correction Values from CSV File
        self.readCalibrationValuesFromCSV()

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

    def ina226_calibrateReg(self, maxExpectCurr = uint16,rShunt = float16):
        self.currentLSB = maxExpectCurr/(2**15)
        self.cal = uint16(0.00512/(self.currentLSB*rShunt))
        self.ina226_writeReg(self.ina226_cal_reg,self.cal)

    def readCalibrationValuesFromCSV(self):
        file = open('calibVals.CSV')
        arr = numpy.loadtxt(file, delimiter=',')
        
        self.shuntVoltOffset    = arr[0]
        self.busVoltOffset      = arr[1]
        self.busCurrOffset      = arr[2]
        self.powerOffset        = arr[3]

    #kann zu testzwecken ausgelesen werden
    def ina226_getShuntVoltage(self):
        shuntVolt = float((self.ina226_readReg(self.ina226_shunt_reg) * 2.5e-6) + (self.shuntVoltOffset))
        return round(shuntVolt,4)

    def ina226_getBusVoltage(self):
        busVolt = float(self.ina226_readReg(self.ina226_bus_reg) * 1.25e-3 + self.busVoltOffset)
        return round(busVolt,2)

    def ina226_getCellVoltage(self):
        cellVolt = self.ina226_getBusVoltage()/int(EepromDataComplete[2])
        return round(cellVolt,2)

    def ina226_getCurr(self):
        busCurr = float(self.ina226_readReg(self.ina226_curr_reg)*self.currentLSB + self.busCurrOffset)
        return round(busCurr,2)

    def ina226_getPower(self):
        busPow = float(self.ina226_readReg(self.ina226_power_reg)*25*self.currentLSB + self.powerOffset)
        return busPow

    def ina226_getVoltageBat(self):
        return self.voltBat

    def ina226_getVoltageCell(self): 
        return self.voltCell

    def ina226_getCurrBat(self):
        return self.currBat
    
    def ina226_setShuntOffset(self,offset):
        self.shuntVoltOffset = offset
    
    def ina226_setBusVoltOffset(self,offset):
        self.busVoltOffset = offset
    
    def ina226_setBusCurrOffset(self,offset):
        self.busCurrOffset = offset

    def ina226_setBusPowerOffset(self,offset):
        self.powerOffset = offset

    def ina226_setMaxExpCurr(self,value):
        self.maxExpCurr = int(value)

    def ina226_setShuntResValue(self,value):
        self.shuntResValue = int(value)
    
    def ina226_getShuntOffset(self):
        return self.shuntVoltOffset

    def ina226_getBusOffset(self):
        return self.busVoltOffset

    def ina226_getBusCurrOffset(self):
        return self.busCurrOffset

    def ina226_getPowerOffset(self):
        return self.powerOffset

    def ina226_getMaxExpCurr(self):
        return self.maxExpCurr

    def ina226_getShuntResValue(self):
        return self.shuntResValue

                
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
        
        ttk.Label(self, text="Timer", font='20').grid(column=0,row=0, padx=5,sticky=W)

        self.tl = ttk.Label(self, text=self.secFormat, font='20')
        self.tl.grid(column=1,row=0)

        ttk.Label(self,text="Sek.",font='20').grid(column=2,row=0, padx=5)

###########################################################
###         damit über mehrere Funktionen auf Variablen
###         zugegriffen werden kann
###         --> self. vor jede variable, damit wird
##                          Klassenvariable erzeugt

    #Hier wird countdown erzeugt
    #callback nach 1s auf Funktion selbst
    #--> python after()

    def countdown(self):
        self.dur=self.durStart
        self.startCountdown()

    def startCountdown(self):
        #update happens before if condition
        self.secFormat = '{:02d}'.format(self.dur)   
        self.tl.configure(text=self.secFormat)
        if self.dur > 0:   
            self.secFormat = '{:02d}'.format(self.dur)            
            #schedule timer to update icon every second
            self.dur -= 1
            self.tl.after(1000,self.startCountdown)
    
    def getTime(self):
        return self.dur
    def getStartDur(self):
        return self.durStart

#für UART-Kommunikation
class EepromControl():
    def __init__(self):
        #super().__init__()
        #self.setEeprom()
        self.sendBuffer = bytearray(5)
        self.receiveBuffer = bytearray(3)
        self.ser = serial.Serial("/dev/ttyAMA0", 9600)

    def sendPackage(self,id,adress,content):
        self.sendBuffer[0] = START_BIT
        self.sendBuffer[1] = id
        self.sendBuffer[2] = uint8(adress)
        self.sendBuffer[3] = uint8(content)
        self.sendBuffer[4] = STOP_BIT
        self.ser.write(self.sendBuffer)

    def receivePackage(self):
        self.receiveBuffer = self.ser.read(3)
        
        payload = (self.receiveBuffer[1])
        if self.receiveBuffer[0] == START_BIT & self.receiveBuffer[2] == STOP_BIT:
            return uint8(payload)

    def readSingleRegister(self,adress):
        self.sendPackage(uartCMD["eepromReadSingleReg"], adress, 1)
        return self.receivePackage()

    #unbenutzte Funktion        
    def readAllRegisters(self):
        for i in range(256):
            EepromDataComplete[i] = self.readSingleRegister(i)

    def writeSingleRegister(self,adress,content):
        self.sendPackage(uartCMD["eepromWriteSingleReg"],adress,content)

    def readNTC(self):
        self.sendPackage(uartCMD["ntcRead"],1,1)
        return self.receivePackage()
        
    def writeNTC(self):
        self.sendPackage(uartCMD["ntcWrite"],1,InfoData[0])

    def readOverVoltage(self):
        self.sendPackage(uartCMD["voltageProtectRead"],1,1)
        return self.receivePackage()

    def writeOvervoltage(self):
        self.sendPackage(uartCMD["voltageProtectWrite"],1,InfoData[1])

    def setNTCValue(self,value):
        InfoData[0] = value

    def setOvValue(self,value):
        InfoData[1] = value

    def setEeprom(self):
        #Akkupack Infos 1/3
        EepromDataComplete[0] = EepromDataDict["safetyB1"]
        EepromDataComplete[1] = EepromDataDict["safetyB2"]
        EepromDataComplete[2] = EepromDataDict["cellsInSer"]    #number of cells in Series
        EepromDataComplete[3] = EepromDataDict["U_min"]         #U_min
        EepromDataComplete[4] = 0x18                            #T_max
        EepromDataComplete[5] = 0x80                            #not specified
        EepromDataComplete[6] = 0xD4                            #calibration value
        EepromDataComplete[7] = 0xC0                             #calibration value
        EepromDataComplete[8] = EepromDataDict["capBat"]                              #C_batt
        EepromDataComplete[9] = EepromDataDict["U_charge"]                             #U_charge

        EepromDataComplete[10] = 1;                             #min temp(not specified)
        EepromDataComplete[11] = 1;                             #max temp(not specified)

        EepromDataComplete[12] = 242                           #Detection of Eeprom Assignment
        EepromDataComplete[13] = EepromDataDict["CellsInPar"]  #number of cells in Parallel
        EepromDataComplete[14] = EepromDataDict["numCCstart1"] #charging operations values start
        EepromDataComplete[15] = EepromDataDict["numCCstart2"]
        EepromDataComplete[16] = EepromDataDict["numCVstart1"]
        EepromDataComplete[17] = EepromDataDict["numCVstart2"]
        EepromDataComplete[18] = EepromDataDict["numCVstop1"]
        EepromDataComplete[19] = EepromDataDict["numCVstop2"]  #charging operations stop

        EepromDataComplete[20] = 0x1E                          #Value w/o function
        EepromDataComplete[21] = 0x43                          #Value w/p function
        EepromDataComplete[22] = EepromDataDict["U_charge"]                           #U_charge

        EepromDataComplete[23] = 0xE7                          #Value w/o function

        #Registers 24 - 27 are 0 by default
        EepromDataComplete[28] = 200
        EepromDataComplete[29] = 106
        EepromDataComplete[30] = 11      
        EepromDataComplete[31] = 152

        EepromDataComplete[32] = 0xE0                          #Value w/o function or address to activate check capacity gauge

        #Akkupack Infos 2/3
        EepromDataComplete[33] = EepromDataDict["safetyB1"]
        EepromDataComplete[34] = EepromDataDict["safetyB2"]
        EepromDataComplete[35] = EepromDataDict["numStartChaSub30Deg1"]         #Number of start charging              H Byte
        EepromDataComplete[36] = EepromDataDict["numStartChaSub30Deg2"]         #operations with temperature <30°C     L Byte
        EepromDataComplete[37] = EepromDataDict["U_charge"]                          #U_charge
        EepromDataComplete[38] = EepromDataDict["min_temp"]                          #min ever reached BatPAck Temp
        EepromDataComplete[39] = EepromDataDict["max_temp"]                          #max ever reached BatPack Temp
        EepromDataComplete[40] = EepromDataDict["U_charge"]                          #U_charge
        EepromDataComplete[41] = 0                            #Battery Pack manufacturer

        EepromDataComplete[42] = 0                            #charging operations start
        EepromDataComplete[43] = 1
        EepromDataComplete[44] = 0
        EepromDataComplete[45] = 1
        EepromDataComplete[46] = 0
        EepromDataComplete[47] = 1                             #charging operations stop

        EepromDataComplete[48] = 0                             #supplier of cells
        EepromDataComplete[49] = 0                             #designation of cell

        EepromDataComplete[108] = EepromDataDict["T_min"]
        EepromDataComplete[109] = EepromDataDict["T_cold"]
        EepromDataComplete[110] = EepromDataDict["T_warm"]
        EepromDataComplete[111] = EepromDataDict["T_max"]
        EepromDataComplete[112] = EepromDataDict["U_cold"]
        EepromDataComplete[113] = EepromDataDict["U_warm"]
        EepromDataComplete[114] = EepromDataDict["U_max"]
        EepromDataComplete[115] = EepromDataDict["I_cold"]
        EepromDataComplete[116] = EepromDataDict["I_warm"]
        EepromDataComplete[117] = EepromDataDict["I_max"]

        #capacity display available(0x0F)/not available(0xF0)
        EepromDataComplete[118] = 0xF0
        #variable Ladeparameter 
        #--> 0xF0 = off
        #--> 0x0F = on;
        #default off
        EepromDataComplete[119] = 0xF0
        

#Ermöglicht Konvertieren von EEPROM Werten in auslesbare Werte
class HexValConvert():
    def __init__(self):
        dummyVal = 0

    def shiftLeftByXPos(self,startVal,howMany):
        return uint8(startVal << howMany)

    def shiftRightByXPos(self,startVal,howMany):
        return uint8(startVal >> howMany)

    #Values dont match, needs rework
    def convertNTCTempToDec(self,temp):
        return 200-(temp*3)