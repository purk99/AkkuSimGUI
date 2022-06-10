from tkinter import *
from tkinter import ttk

from time import sleep
from timer import *
#from Module import *
#from moduleCalibration import *
from moduleTemp import ModulTempHysterese

root = Tk()
root.title("Testfenster")
root.geometry("800x480")

mainframe = ttk.Frame(root)
mainframe.grid()

#tL = ttk.Label(mainframe,textvariable=val1)
tL = ttk.Label(mainframe,text="Testumgebung",font='20')
tL.grid(column=1,row=0)

test = ModulTempHysterese(mainframe)
test.grid(column=1,row=1)

eb = ttk.Button(mainframe,text="Exit",command=root.destroy)
eb.grid(column=10,row=10)

root.mainloop()




