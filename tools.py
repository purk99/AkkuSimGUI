from threading import Thread
from tkinter import *
from tkinter import ttk
import time
from time import sleep
#from anyio import start_blocking_portal
import serial
from smbus2 import SMBus

from EepromData import *

#from timerTest import countdown

START_BIT = 0x02
STOP_BIT = 0x03

class SensorRead(ttk.Frame):
    def __init__(self,parent):
        self.i2c_bus = SMBus(1)
        self.i2cadress = 0x31
        #i2c_sense.write_byte_data(i2cadressb,IOCON,0x02) 

        self.voltBat = StringVar()
        self.voltCell = StringVar()
        self.currBat = StringVar()
        
        #dummywerte
        #self.voltage_meas = 18
        #self.current_meas = 5

        ttk.Frame.__init__(self, parent)

        sensFrame = self
        sensFrame.grid()

        vbl = ttk.Label(sensFrame, text="Spannung Batterie")
        vbl.grid(column=2,row=1)

        self.voltageBatl = ttk.Label(sensFrame, textvariable=self.voltBat)
        self.voltageBatl.grid(column=3, row=1)

        self.vcl = ttk.Label(sensFrame,text="Spannung Zelle")
        self.vcl.grid(column=2,row=2)

        voltageCelll = ttk.Label(sensFrame, textvariable=self.voltCell)
        voltageCelll.grid(column=3,row=2)

        ibl = ttk.Label(sensFrame,text="Batterie Gesamtstrom")
        ibl.grid(column=2,row=3)

        self.currentBatl = ttk.Label(sensFrame, textvariable=self.currBat)
        self.currentBatl.grid(column=3,row=3)

        startMeasB = ttk.Button(sensFrame,text="Starte Messung",command=self.startMeas)
        startMeasB.grid(column=3,row=4)
        
    def startMeas(self):
        self.checkVoltage()
        #self.checkCellVoltage()
        self.checkCurrent()
        #self.i2c_getvoltageData()

    #Befehl in Verbindung mit I2C-Bus
    def checkVoltage(self):
        self.voltBat.set(self.i2c_getvoltageData())
        self.voltageBatl.after(100,self.checkVoltage)

    def checkCellVoltage(self):
        self.voltCell.set(int(self.voltBat.get) / EepromDataDict["cellsInSer"])
        self.vcl.after(100,self.checkCellVoltage)

    def checkCurrent(self):
        #Befehl in Verbindung mit I2C-Bus
        self.currBat.set(self.i2c_getCurrentData())
        self.currentBatl.after(100,self.checkCurrent)

    def i2c_getvoltageData(self):
        self.i2c_bus.write_byte(self.i2cadress,0x01)
        val = self.i2c_bus.read_byte(self.i2cadress)
        #self.voltBat.set(val)
        #self.voltageBatl.after(100,self.i2c_getvoltageData)
        return val
    
    def i2c_getCurrentData(self):
        self.i2c_bus.write_byte(self.i2cadress,0x02)
        val = self.i2c_bus.read_byte(self.i2cadress)
        return val

    def getVoltageBat(self):
        return self.voltBat

    def getVoltageCell(self):
        return self.voltCell

    def getCurrBat(self):
        return self.currBat

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

    #Hier wird countdown erzeugt+
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
        #print(self.sendBuffer)

    def receivePackage(self):
        #self.receiveBuffer = self.ser.read(5)
        #Byte 1 --> Start Byte
        #Byte 2,3 --> payload
        #Byte 4 --> Stop Byte

        #PacketHandler
        #elf.receiveBuffer[0] == 0x2:
        #for l in testList:
        #    if self.receiveBuffer[1] == l:
        #        testList[l] = self.receiveBuffer[2]
        #if self.receiveBuffer[3] == STOP_BIT:
        #    return 1
        #else: 
        #    return -1

        self.receiveBuffer = self.ser.read(3)
        
        payload = (self.receiveBuffer[1])
        if self.receiveBuffer[0] == START_BIT & self.receiveBuffer[2] == STOP_BIT:
            return payload



    def readSingleRegister(self,adress):
        self.sendPackage(uartCMD["eepromReadSingleReg"], adress, 1)
        #proof = self.receivePackage()
        #if proof != 
        
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

class INA226():
    pass