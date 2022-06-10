from math import ceil
import string
from numpy import char, float16, int16, uint16, uint8
import pigpio

from tkinter import ttk
from tkinter import *

fields = list(range(0,100))


root = Tk()
root.geometry("800x480")

frame = ttk.Frame(root)
frame.grid()

counter = 0
counter1 = 0

for i in fields:
    #ttk.Separator(frame,orient=VERTICAL).grid(column=(counter*2)+1,row=counter1)
    ttk.Label(frame, text=fields[i]).grid(column=counter*2,row=counter1)
    ttk.Label(frame,text=100-fields[i]).grid(column=(counter*2)+1,row=counter1)
    counter1 += 1
    if fields[i]%10 == 9:
        counter += 1
        counter1 = 0

root.mainloop()




