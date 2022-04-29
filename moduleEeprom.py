
from tkinter import *
from tkinter import ttk
from tkinter import font

from tools import *
from EepromData import *
from EepromAccess import *

class ModulEepromZyklen(ttk.Frame):
    def __init__(self,parent):
        ttk.Frame.__init__(self,parent)

        self.config(width=200,height=200)
        self.grid(column=5,row=0, columnspan=2, rowspan=2)

        headlabel = ttk.Label(self,text="Modul Ladezyklen", font='10')
        headlabel.grid(column=1,row=0)

        cF = EepromCycleParam(self)
        cF.grid(column=3,row=0)
        
class ModulEepromFehler(ttk.Frame):
    def __init__(self,parent):
        ttk.Frame.__init__(self,parent)

        self.config(width=200,height=200)
        self.grid(column=5,row=0, columnspan=2, rowspan=2)

        headlabel = ttk.Label(self,text="Modul Ladezyklen", font='10')
        headlabel.grid(column=1,row=0)    

        eF = EepromChargeParam()
        eF.grid(column=3,row=0)
