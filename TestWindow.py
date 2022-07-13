from csv import *
from itertools import count
from math import ceil
import re
import string
from numpy import char, float16, int16, size, uint16, uint8
import numpy
import pigpio

from tkinter import ttk
from tkinter import *
#from tools_V21 import Countdown
#from moduleEeprom import ModulEepromKomplett
from EepromData import *
import csv

'''

file = open('calibVals.CSV')
arr = numpy.loadtxt(file,delimiter=',')
print(arr)

calibrationValues = [None] * 4
for p in range(size(arr)):
    calibrationValues[p] = arr[p]

print(calibrationValues)

def turnIntoTuple():
    return tuple(calibrationValues)

print(type(turnIntoTuple()))
x = turnIntoTuple()
print(x[1])

fields = list(range(4))

f = open('calibVals.CSV','w')
writer = writer(f)
writer.writerow(fields)
print("schreiben abgeschlossen")
f.close()

#neuer Kommentar


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
        
        ttk.Label(self, text="Timer", font='20').grid(column=0,row=0,sticky=W)

        self.tl = ttk.Label(self, text=self.secFormat, font='20')
        self.tl.grid(column=1,row=0)

        ttk.Label(self,text="Sek.",font='20').grid(column=2,row=0)

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
        #self.secFormat = '{:02d}'.format(self.dur)   
        self.tl.configure(text='{:05.2f}'.format(self.dur))
        #print(self.dur)        
        if self.dur > 0:   
            #self.secFormat = '{:02d}'.format(self.dur)            
            #schedule timer to update icon every second
            #self.tl.configure(text=self.secFormat)            
            self.dur -= 1
            #self.tl.configure(text=self.secFormat)
            self.tl.after(1000,self.startCountdown)

    
    def getTime(self):
        return self.dur
    def getStartDur(self):
        return self.durStart

root = Tk()

labelframe = LabelFrame(root, text="This is a LabelFrame")
labelframe.pack(fill="both", expand="yes")
 
left = Label(labelframe, text="Inside the LabelFrame")
left.pack()
'''


root = Tk()
root.geometry("800x480")

frame = ttk.Frame(root)
frame.grid()

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
        

#eeprom = ModulEepromKomplett(frame)
f = open('./EEPROMPARAMS/EepromStandardParams.CSV','w')
writer = csv.writer(f)
writer.writerow(EepromDataComplete)
f.close()

root.mainloop()

'''
counter = 0
counter1 = 0
lfF = [None] * 65
lfF[0] = ttk.Labelframe(frame,text="test",padding=1)
lfF[0].grid(column=1,row=1)
ttk.Label(lfF[0], text=hex(100)).grid(column=0,row=0,pady=2,sticky=E)
ttk.Label(lfF[0], text=hex(50)).grid(column=1,row=0,pady=2,sticky=W)

for p in range(65):
    ttk.Labelframe(frame,text="test").grid(column=counter,row=counter1)
    #lfF[p].grid(column=counter,row=counter1)
    
        
for i in fields:
    ttk.Label(frame, text=hex(fields[i])).grid(column=counter*3,row=counter1,pady=2,sticky=E)
    ttk.Label(frame,text=hex(100-fields[i])).grid(column=(counter*3)+1,row=counter1,pady=2,sticky=W)
    counter1 += 1
    if fields[i]%10 == 9:
        counter += 1
        counter1 = 0



for p in range(20):
    if p%2 == 0:
        ttk.Separator(frame,orient='vertical').grid(column=p,row=0,ipady=200)




file = open("NTCValues.csv")
arr = numpy.loadtxt(file,delimiter=';')
#print(arr[0,0])
werteArray = [None] * 116
tempArray = [None] * 116
for p in range(size(arr,0)):
    werteArray[p] = arr[p][1]
    tempArray[p] = arr[p][0]

print(werteArray)
root.mainloop()
'''




