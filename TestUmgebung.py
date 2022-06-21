from tkinter import *
from tkinter import ttk

from time import sleep
from timer import *

from tools_V21 import EepromControl

from EepromData import *
from EepromAccess import EepromChargeParam
from moduleTemp import ModulTempHysterese

root = Tk()
root.title("Testfenster")
root.geometry("800x480")

eeprom = EepromControl()

mainframe = ttk.Frame(root)
mainframe.grid(sticky=NSEW)

test = ModulTempHysterese(mainframe)
test.grid()

'''
tL = ttk.Label(mainframe,text="Testumgebung",font='20')
tL.grid(column=1,row=0)

headLabel = ttk.Label(mainframe,text="Temperaturgesteuerte Stromhysterese",font='10')
headLabel.grid(column=1,row=0)

ttk.Label(mainframe,text="Starttemperatur").grid(column=0,row=1)
sgL = ttk.Combobox(mainframe,values=NTCTemps)
sgL.grid(column=1,row=1)

ttk.Label(mainframe,text="Endtemperatur").grid(column=0,row=3)
egL = ttk.Combobox(mainframe,values=NTCTemps)
egL.grid(column=1,row=3)

ttk.Label(mainframe,text="Schrittzeit").grid(column=0,row=4)
stepTime = ttk.Combobox(mainframe,values=list(range(11)))
stepTime.grid(column=1,row=4)

tempB = ttk.Button(mainframe,text="Test Starten")
tempB.grid(column=1, row=6)

ttk.Label(mainframe,text="Manuelle Temperatureinstellung",font='10').grid(column=1,row=7)
ttk.Label(mainframe,text="Neue Temperatur").grid(column=0,row=8)
mTempL = ttk.Combobox(mainframe,values=NTCTemps)
mTempL.grid(column=1,row=8)

newTempB = ttk.Button(mainframe,text="Temperatur einstellen")
newTempB.grid(column=1,row=9)

tempAktuell = 0
ttk.Label(mainframe,text="Aktuelle Temperatur",font='15').grid(column=0,row=10)
tAL = ttk.Label(mainframe,text=tempAktuell,font='15')
tAL.grid(column=1,row=10)

eb = ttk.Button(mainframe,text="Exit",command=root.destroy)
eb.grid(column=10,row=10)
'''


root.mainloop()




