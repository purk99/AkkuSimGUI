##################################################
#   File for testing the display of all 
#   register positions of the eeprom 
##################################################

from cgitb import text
from itertools import tee
import string
import tkinter
from tkinter import *
from tkinter import ttk


root = Tk()
root.geometry("800x480")
root.grid()

frame = ttk.Frame(root)
frame.grid(column=0,row=1)

counter = 0
counter1 = 1

indexF = [ttk.Label] * 135
valueF = [ttk.Label] * 135
lfF = [ttk.Labelframe] * 135

ttk.Label(root,text="EEPROM Daten",font='30').grid(column=0,row=0)

for p in range(135):
    indexString = "Pos: {}".format(p)
    lfF[p] = ttk.Labelframe(frame,text=p)
    lfF[p].grid(column=counter,row=counter1,padx=1)

    counter1 += 1
    if p%10 == 9:
        counter += 1
        counter1 = 1

for i in range(135):
    indexF[i] = ttk.Label(lfF[i], text="{:03d}".format(i))
    indexF[i].grid(column=0,row=0, sticky=W)
    valueF[i] = ttk.Label(lfF[i],text="{:03d}".format(i))
    valueF[i].grid(column=1,row=0, sticky=E)

root.mainloop()