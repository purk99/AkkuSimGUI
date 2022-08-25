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

START_BIT = 2
STOP_BIT = 3

#responsible for communication with INA226
class SensorRead(ttk.Frame):

    def __init__(self,parent): 

        #initialize I2C-communication
        self.ina226_adress = 0x40
        self.ina226 = pi()

        #registers used for access of ina226
        self.ina226_config_reg =    0   #R/W
        self.ina226_shunt_reg =     1   #R
        self.ina226_bus_reg =       2   #R
        self.ina226_power_reg =     3   #R
        self.ina226_curr_reg =      4   #R
        self.ina226_cal_reg =       5   #R/W

        #used for internal calinration of ina226
        self.currentLSB = float16
        self.cal = int16
        self.maxExpCurr = 10
        self.shuntResValue = 0.00475

        #attributes used to save measured values
        self.voltBat = float(10)
        self.voltCell = float(10)
        self.currBat = float(10)
        self.powBat = float(10)

        #offset attributes for measured values 
        self.busVoltOffset = 0
        self.shuntVoltOffset = 0
        self.busCurrOffset = 0
        self.powerOffset = 0

        #initialize frame
        ttk.Frame.__init__(self, parent)
        
        self.grid()

        #GUI elements
        sensFrame = ttk.Labelframe(self,text="Messwerte")
        sensFrame.grid(padx=3, sticky=NSEW)

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
        startMeasB.grid(column=0,row=5, pady=2, sticky=EW, columnspan=2)

        #to recalibrate, uncomment if needed
        #can be used if GUI is extended
        #calB = ttk.Button(sensFrame,text="Neukalibrierung",command=self.calib)
        #calB.grid(column=0,row=5)

        #initializing of core functions
        self.ina226_writeReg(self.ina226_config_reg, 0x45A7)
        self.ina226_calibrateReg(self.maxExpCurr,self.shuntResValue)
        #get right offset values from CSV file
        self.readCalibrationValuesFromCSV()

    #method calls itself every 100ms
    def checkMeas(self):
        #update-method for all measurements
        self.updateValues()
        self.voltageBatl.after(100,self.checkMeas)

    #gui elements are refreshed here
    def updateValues(self):
        cellVoltage = self.ina226_getBusVoltage()/int(EepromDataComplete[2])
        self.currentBatl.configure(text = '{:05.2f}'.format(self.ina226_getCurr()))
        self.voltageCelll.configure(text = '{:05.2f}'.format(cellVoltage))#round(cellVoltage,4)
        self.voltageBatl.configure(text = '{:05.2f}'.format(self.ina226_getBusVoltage()))
        self.shuntVoltL.configure(text='{:05.2f}'.format(self.ina226_getShuntVoltage()))

    #read single register from ina226
    def ina226_readReg(self,adress):
        h = self.ina226.i2c_open(1,self.ina226_adress)
        #self.ina226.i2c_write_byte(h,adress)
        recVal =    uint16(self.ina226.i2c_read_word_data(h,adress))
        regVal =    uint16((recVal >> 8)|(recVal << 8))
        self.ina226.i2c_close(h)
        return regVal

    #write single register to ina226
    def ina226_writeReg(self,adress,content = uint16):
        h = self.ina226.i2c_open(1,self.ina226_adress)
        test = [content >> 8, content & 0xff]
        self.ina226.i2c_write_i2c_block_data(h,adress,test)
        self.ina226.i2c_close(h)

    #calculate and set calibration register value to calibration register
    def ina226_calibrateReg(self, maxExpectCurr = uint16,rShunt = float16):
        self.currentLSB = maxExpectCurr/(2**15)
        self.cal = uint16(0.00512/(self.currentLSB*rShunt))
        self.ina226_writeReg(self.ina226_cal_reg,self.cal)

    #get latest offset values from csv
    def readCalibrationValuesFromCSV(self):
        file = open('calibVals.CSV')
        arr = numpy.loadtxt(file, delimiter=',')
        
        self.shuntVoltOffset    = arr[0]
        self.busVoltOffset      = arr[1]
        self.busCurrOffset      = arr[2]
        self.powerOffset        = arr[3]
       

    #methods for access of the ina226
    def ina226_getShuntVoltage(self):
        shuntVolt = float((int16(self.ina226_readReg(self.ina226_shunt_reg)) * 2.5e-3)/2 + (self.shuntVoltOffset))
        return round(shuntVolt,4)

    def ina226_getBusVoltage(self):
        busVolt = float((self.ina226_readReg(self.ina226_bus_reg) * 1.25e-3) + self.busVoltOffset)
        return round(busVolt,2)

    def ina226_getCurr(self):
        busCurr = float((int16(self.ina226_readReg(self.ina226_curr_reg))*self.currentLSB) + self.busCurrOffset)
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
    
#like SensorRead, but without a Frame
#can be used if ina226 needs to be accessed without gui elements    
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
        self.maxExpCurr = 10
        self.shuntResValue = 0.00475

        self.voltBat = float(10)
        self.voltCell = float(10)
        self.currBat = float(10)

        self.busVoltOffset = 0
        self.shuntVoltOffset = 0
        self.busCurrOffset = 0
        self.powerOffset = 0

        self.ina226_calibrateReg(self.maxExpCurr,self.shuntResValue)
        self.ina226_writeReg(self.ina226_config_reg, 0x45A7)
        self.readCalibrationValuesFromCSV()

    def ina226_readReg(self,adress):
        h = self.ina226.i2c_open(1,self.ina226_adress)
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
           
#Creates a timer
class Countdown(ttk.Frame):
    def __init__(self,parent,duration):
        ttk.Frame.__init__(self, parent)
        
        self.grid()

        self.dur = duration
        self.durStart = self.dur
        self.secFormat = self.dur
        
        #create gui elements
        ttk.Label(self, text="Timer", font='20').grid(column=0,row=0, padx=5,sticky=W)

        self.tl = ttk.Label(self, text=self.secFormat, font='20')
        self.tl.grid(column=1,row=0)

        ttk.Label(self,text="Sek.",font='20').grid(column=2,row=0, padx=5)

    #sets self.dur(timer counter variable) to start duration time
    def countdown(self):
        self.dur=self.durStart
        #calls the method to start the countdown
        self.startCountdown()

    def startCountdown(self):
        #update of gui element
        self.secFormat = '{:02d}'.format(self.dur)   
        self.tl.configure(text=self.secFormat)
        if self.dur > 0:   
            self.secFormat = '{:02d}'.format(self.dur)            
            #schedule timer to update icon every second
            self.dur -= 1
            self.tl.after(1000,self.startCountdown)
    
    #getter
    def getTime(self):
        return self.dur
    def getStartDur(self):
        return self.durStart

#UART-communication with Arduino
class EepromControl():
    def __init__(self):

        #communication buffer
        self.sendBuffer = bytearray(5)
        self.receiveBuffer = bytearray(3)
        #initialize uart port on RaspBi
        self.ser = serial.Serial("/dev/ttyAMA0", 9600)

    #basic-level method,
    #creates package with 5 Bytes
    def sendPackage(self,id,adress,content):
        self.sendBuffer[0] = START_BIT
        self.sendBuffer[1] = id
        self.sendBuffer[2] = uint8(adress)
        self.sendBuffer[3] = uint8(content)
        self.sendBuffer[4] = STOP_BIT
        #send package via uart
        self.ser.write(self.sendBuffer)

    #read package from uart bus
    def receivePackage(self):
        self.receiveBuffer = self.ser.read(3)

        #check if package contains start & stop byte
        payload = (self.receiveBuffer[1])
        if ((self.receiveBuffer[0] == START_BIT) & (self.receiveBuffer[2] == STOP_BIT)):
            return uint8(payload)

    #read single register from eeprom-array on arduino
    def readSingleRegister(self,adress):
        #send read eeprom command to arduino
        self.sendPackage(uartCMD["eepromReadSingleReg"], adress, 1)
        return self.receivePackage()

    def readAllRegisters(self):
        #initialize buffer to store eeprom data from arduino
        EepromBuffer = [uint8(0)] * 150
        for i in range(150):
            #read every register from arduino
            EepromBuffer[i] = self.readSingleRegister(i)
        #return 150 bytes
        return EepromBuffer

    #write single register to eeprom-array on arduino
    def writeSingleRegister(self,adress,content):
        #send write command, register adress and new register content 
        self.sendPackage(uartCMD["eepromWriteSingleReg"],adress,content)

    #read value from ntc-array on arduino
    def readNTC(self):
        self.sendPackage(uartCMD["ntcRead"],1,1)
        return self.receivePackage()
    
    #write value to ntc-array on arduino
    def writeNTC(self):
        self.sendPackage(uartCMD["ntcWrite"],1,InfoData[0])

    #read overvoltage value from ntc-array on arduino
    def readOverVoltage(self):
        self.sendPackage(uartCMD["voltageProtectRead"],1,1)
        return self.receivePackage()

    #write overvoltage value to ntc-array on arduino
    def writeOvervoltage(self):
        self.sendPackage(uartCMD["voltageProtectWrite"],1,InfoData[1])

    #set infodata values for ntc on Raspberry Pi from value parameter
    #infodata --> stores ntc and ov-values
    def setNTCValue(self,value):
        InfoData[0] = value
        self.writeNTC()

    #set infodata values for ov on Raspberry Pi from value parameter
    def setOvValue(self,value):
        InfoData[1] = value
        self.writeOvervoltage()

    def getArduinoEepromAndInfoData(self):
        ###Call At the start of the program to synchronise arrays of Raspberry Pi and Arduino###
        #--> Synchronization of EEPROM-simulating-Arrays on Arduino and Raspberry Pi

        #reads Register Values from Arduino and saves them into EepromActualParams
        ardEepromData = self.readAllRegisters()
        #read Info Values and save them into infoActualParams.py
        ardInfoData = [self.readNTC(),self.readOverVoltage()]

        #get eeprom parameter values from csv
        f = open('./EEPROMPARAMS/EepromActualParams.CSV','w')
        writer = csv.writer(f)
        writer.writerow(ardEepromData)
        f.close()

        #get info values from csv
        g = open('./EEPROMPARAMS/InfoActualParams.CSV','w')
        writer = csv.writer(g)
        writer.writerow(ardInfoData)
        g.close()

    def setEeprom(self):
        #reads all Registers from CSV files and feeds them into 
        #Raspberry-Sided EEPROM-Register and Info-Register
        f = open('./EEPROMPARAMS/EepromActualParams.CSV')
        arr = numpy.loadtxt(f,delimiter=',')

        for p in range(size(arr)):
            EepromDataComplete[p] = int(arr[p])

        g = open('./EEPROMPARAMS/InfoActualParams.CSV')
        arr = numpy.loadtxt(g,delimiter=',')

        for p in range(size(arr)):
            InfoData[p] = int(arr[p])

#can be used to convert values from various data types
#needs rework and extension
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