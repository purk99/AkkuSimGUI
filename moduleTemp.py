from tkinter import *
from tkinter import ttk

from tools_V21 import *
from EepromData import *
from EepromAccess import *

#Creates Frame to control NTC on Arduino
class ModulTempNTCError(ttk.Frame):
    def __init__(self,parent):
        ttk.Frame.__init__(self,parent)
        self.grid()
        self.configure(relief='ridge')
        
        headLabel = ttk.Label(self,text="Prüfmodul NTC Error", font='15')
        headLabel.grid(column=1,row=0)

        self.modulframe = ttk.Frame(self)
        self.modulframe.grid(column=1,row=1)

        #create object to control eeprom on Arduino
        self.comm = EepromControl()
        self.comm.setEeprom()   

        self.shortB = ttk.Button(self.modulframe,text="NTC kurzschließen",command=self.shortNTC)
        self.shortB.grid(column=0,row=1, sticky=EW)

        self.discB = ttk.Button(self.modulframe,text="NTC ausstecken", command=self.discNTC)
        self.discB.grid(column=0,row=2, sticky=EW)

        self.infoL = ttk.Label(self.modulframe,text="NTC Normalzustand", font='20')
        self.infoL.grid(column=0,row=4, sticky=EW)  

    #set NTC value to "shorted" value on arduino and in gui
    def shortNTC(self):
        self.comm.setNTCValue(0xF0)
        self.comm.writeNTC()

        self.infoL.configure(text="NTC kurzgeschlossen")

    #set NTC value to "disconnected" value on arduino and in gui
    def discNTC(self):       
        self.comm.setNTCValue(0x0F)
        self.comm.writeNTC()

        self.infoL.configure(text="NTC ausgesteckt")
    
    #used to refresh Value by other test modules
    def refreshNTCValue(self, temp):
        self.infoL.configure(text=temp)

