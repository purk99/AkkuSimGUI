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

'''

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
        self.secFormat = '{:02d}'.format(self.dur)   
        self.tl.configure(text=self.secFormat)
        print(self.dur)        
        if self.dur > 0:   
            self.secFormat = '{:02d}'.format(self.dur)            
            #schedule timer to update icon every second
            #self.tl.configure(text=self.secFormat)            
            self.dur -= 1
            #self.tl.configure(text=self.secFormat)
            self.tl.after(1000,self.startCountdown)

    
    def getTime(self):
        return self.dur
    def getStartDur(self):
        return self.durStart
'''

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

cd = Countdown(frame,10)
ttk.Button(frame,text="start",command=cd.countdown).grid(column=5,row=5)

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




