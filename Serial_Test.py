import serial
from time import sleep

START_BIT = 0x02
STOP_BIT = 0x03

testList = [0x55, 0x30,0x28,1]

############################
###   Serial Test        ###
### not used in project  ###
### deprecated Version of###
### EepromControl        ###
############################

class EepromControl():
    def __init__(self):
        #super().__init__()
        self.sendBuffer = bytearray(5)
        self.receiveBuffer = bytearray(4)
        self.payload = [0x0,0x0]
        self.ser = serial.Serial("/dev/ttyS0", 9600)

    def sendPackage(self,adress,data):
        self.sendBuffer[0] = START_BIT
        self.sendBuffer[1] = adress
        self.sendBuffer[2] = data[0]
        self.sendBuffer[3] = data[1]
        self.sendBuffer[4] = STOP_BIT
        #self.ser.write(self.sendBuffer)
        #print(self.sendBuffer)

    def receivePackage(self):
        #self.receiveBuffer = self.ser.read(5)
        #Byte 1 --> Start Byte
        #Byte 2 --> Adresse
        #Byte 3 --> payload
        #Byte 4 --> Stop Byte
        self.receiveBuffer = [0x00,0x01,0x02,0x03]

        if self.receiveBuffer[0] == 0x2:
            for l in testList:
                if self.receiveBuffer[1] == l:
                    testList[l] = self.receiveBuffer[2]
            if self.receiveBuffer[3] == STOP_BIT:
                return 1
            else: 
                return -1

    def readSingleRegister(self, id):
        self.sendPackage(id,1,0x32)
        self.receivePackage()
        
    def readAllRegisters(self):
        self.sendPackage(0x25,0)
        for list in testList:
            self.receivePackage()

    def writeSingleRegister(self,id,adress,content):
        self.sendPackage(id,adress,content)
        

test = EepromControl()
test.sendPackage(0x50,0x51,0x52)
#test.readSingleRegister(0x45)




"""
#port mit baudrate öffnen
ser = serial.Serial ("/dev/ttyS0", 9600)

while True:
    #serial port auslesen
    received_data = ser.read()
    sleep(0.03)
    #auf "wartende" Bytes prüfen
    data_left = ser.inWaiting() 
    received_data += ser.read(data_left)
    #daten über Bus senden
    ser.write(received_data)
###############################
"""

