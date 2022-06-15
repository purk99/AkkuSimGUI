
from tkinter import *
from tkinter import ttk
from tkinter import font

from tools_V21 import *
from EepromData import *
from EepromAccess import *

class ModulEepromKomplett(ttk.Frame):
    def __init__(self,parent):
        ttk.Frame.__init__(self,parent)

        self.grid()

        headlabel = ttk.Label(self,text="EEPROM-Daten", font='20')
        headlabel.grid(column=1,row=0)

        counter = 0
        counter1 = 1
        self.regPointer = [None] * 128
        self.regValue = [None] * 128
        fields = list(range(129))
        for i in fields:
            ttk.Label(self, text=hex(fields[i])).grid(column=counter*2,row=counter1,pady=2,sticky=E)
            self.regValue[i] = ttk.Label(self,text=hex(EepromDataComplete[i]))
            self.regValue.grid(column=(counter*2)+1,row=counter1,pady=2,sticky=W)
            counter1 += 1
            if fields[i]%10 == 9:
                counter += 1
                counter1 = 1

        ttk.Label(self,text="Register wählen").grid(column=0,row=12)

        self.regCombo = ttk.Combobox(self,values=hex(list(range(129))))
        self.regCombo.grid(column=1,row=12)

        self.regValCombo = ttk.Combobox(self,values=hex(list(range(129))))
        self.regValCombo.grid(column=2,row=12)

        self.parChB = ttk.Button(self,text="Parameter ändern")
        self.parChB.grid(column=3,row=12)

    def updateRegValue(self,reg,val):
        EepromDataComplete[reg] = val
        self.regValue[reg].configure(text=EepromDataComplete[reg])





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
