from tkinter import *
from tkinter import ttk

from time import sleep
from timer import *
from tools import SensorRead


root = Tk()
root.title("Testfenster")

mainframe = ttk.Frame(root)
mainframe.grid()

sr = SensorRead(mainframe)
sr.grid(column=3,row=3)

#tL = ttk.Label(mainframe,textvariable=val1)
tL = ttk.Label(mainframe,text="Test")
tL.grid(column=1,row=1)

uB = ttk.Button(mainframe,text="Starte Counter")
uB.grid(column=0,row=1)

eb = ttk.Button(mainframe,text="Exit",command=root.destroy)
eb.grid(column=10,row=10)

root.mainloop()




