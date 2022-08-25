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
        
        #headLabel = ttk.Label(self,text="Prüfmodul NTC Error", font='15')
        #headLabel.grid(column=1,row=0)

        self.modulframe = ttk.Labelframe(self,text="NTC-Error")
        self.modulframe.grid(column=0,row=0,sticky=NSEW)
        
        self.ntcStatusF = ttk.Labelframe(self.modulframe, text="NTC-Status")
        self.ntcStatusF.grid(column=0,row=3, sticky=EW)

        #create object to control eeprom on Arduino
        self.comm = EepromControl()
        self.comm.setEeprom()   

        self.shortB = ttk.Button(self.modulframe,text="NTC kurzschließen",command=self.shortNTC, width=30, padding=10)
        self.shortB.grid(column=0,row=1, sticky=EW)

        self.discB = ttk.Button(self.modulframe,text="NTC ausstecken", command=self.discNTC, width=30, padding=10)
        self.discB.grid(column=0,row=2, sticky=EW)

        self.infoL = ttk.Label(self.ntcStatusF,text="Normalzustand", font='20', padding=30)
        self.infoL.grid(column=0,row=4, sticky=EW)  

    #set NTC value to "shorted" value on arduino and in gui
    def shortNTC(self):
        #method sets ntc Value in raspberry and Arduino
        self.comm.setNTCValue(0x0)

        self.infoL.configure(text="NTC kurzgeschlossen")

    #set NTC value to "disconnected" value on arduino and in gui
    def discNTC(self):      
        #method sets ntc Value in raspberry and Arduino 
        self.comm.setNTCValue(0xFF)

        self.infoL.configure(text="NTC ausgesteckt")
    
    #used to refresh Value by other test modules
    def refreshNTCValue(self, temp):
        self.infoL.configure(text=temp)

