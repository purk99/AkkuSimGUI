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

'''
fields = list(range(10))

f = open('calibVals.CSV','w')
writer = writer(f)
writer.writerow(fields)
print("schreiben abgeschlossen")
f.close()

#neuer Kommentar


root = Tk()

labelframe = LabelFrame(root, text="This is a LabelFrame")
labelframe.pack(fill="both", expand="yes")
 
left = Label(labelframe, text="Inside the LabelFrame")
left.pack()
 
root.mainloop()

root = Tk()
root.geometry("800x480")

frame = ttk.Frame(root)
frame.grid()

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




