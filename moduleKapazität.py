########################################
### Currently not used, since 
### test module "Kapazität"
### is not supported yet
########################################

from tkinter import *
from tkinter import ttk

from tools_V21 import SensorRead

class ModulCapCapacity(ttk.Frame):
    def __init__(self,parent):
        ttk.Frame.__init__(self,parent)

        headLabel = ttk.Label(self,text="Testmodul Kapazität", font='20')
        headLabel.grid(column=1,row=0)

        self.chargeCap = 0x80

        ttk.Label(self,text="einzuladende Kapazität").grid(column=0,row=1)
        self.capLabel = ttk.Label(self,text=self.chargeCap)
        self.capLabel.grid(column=1,row=1)

        meas = SensorRead(self)
        meas.grid(column=3,row=3)


