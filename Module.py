from re import T
from tkinter import ttk
from tkinter import *
#from moduleEeprom import *

from moduleSpannung import *
from moduleEeprom import *
from moduleTemp import ModulTempHysterese, ModulTempNTCError
from moduleKapazität import *
from tools_V21 import *

class ModulSpannung(Toplevel):
    def __init__(self, master = None):
        super().__init__(master = master)   
        #self.nt = Toplevel(root)
        self.grid()
        
        frame2 = ttk.Frame(self)
        frame2.grid()

        label2 = ttk.Label(frame2,text="Testmodul Spannung", font='30',padding=5)
        label2.grid(column=1,row=0)

        button = ttk.Button(frame2,text="Modul Tiefenentladung",padding=5, command = self.showModuleTEntladung)
        button.grid(column=1,row=1,padx=5,pady=5)

        button1 = ttk.Button(frame2,text="Modul Ladeschlussspannung",padding=5, command = self.showModuleLSpannung)
        button1.grid(column=1,row=2,padx=5,pady=5)

        bUe = ttk.Button(frame2, text="Modul Überladung/Imbalance",padding=5, command = self.showModuleUe)
        bUe.grid(column=1,row=3,padx=5,pady=5)

        eb = ttk.Button(frame2,text="Fenster schließen",command=self.destroy)
        eb.grid(column=10,row=10)

    def showModuleTEntladung(self):
        ModulSpannungTEntladung(self)

    def showModuleLSpannung(self):
        ModulSpannungLSchluss(self)

    def showModuleUe(self):
        ModulSpannungUeIm(self)

class ModulEeprom(Toplevel):
    def __init__(self,master = None):
        super().__init__(master = master)

        modulframe = ttk.Frame(self, padding=10)
        modulframe.grid()

        headLabel = ttk.Label(modulframe, text="Testmodul EEPROM",font='15')
        headLabel.grid(column=1,row=0)

        #CC,CV,CVende, Temperaturbereiche
        buttonLcyc = ttk.Button(modulframe, text="Testprogramm Ladezyklen", padding=5,command=self.showModulEepromCycleParam)
        buttonLcyc.grid(column=0,row=1,padx=5,pady=5)

        #12V Akku als 18V Akku definieren
        buttonErr = ttk.Button(modulframe,text="Testprogramm Ladeparameter", padding = 5, command=self.showModulEepromChargeParam)
        buttonErr.grid(column=0,row=2,padx=5,pady=5)

        eb = ttk.Button(modulframe,text="Fenster schließen",command=self.destroy)
        eb.grid(column=10,row=10)

    def showModulEepromChargeParam(self):
        cF = EepromChargeParam(self)
        cF.grid(column=3,row=0)

    def showModulEepromCycleParam(self):
        cF = EepromCycleParam(self)
        cF.grid(column=0,row=3)

class ModulTemperatur(Toplevel):
    def __init__(self,master=None):
        super().__init__(master = master)

        modulframe = ttk.Frame(self)
        modulframe.grid()

        headLabel = ttk.Label(modulframe, text="Testmodul Temperaturen", font='20')
        headLabel.grid(column=1,row=0)

        ntcB = ttk.Button(self,text="Testmodul NTC Error",padding=10, command=self.showModulNTCError)
        ntcB.grid(column=0, row=1)

        hystB = ttk.Button(self,text="Testmodul Temperaturhysterese",padding=10, command=self.showModulTempHysterese)
        hystB.grid(column=0, row=2)

    def showModulNTCError(self):
        cF = ModulTempHysterese(self)
        cF.grid(column=0,row=10)

    def showModulTempHysterese(self):
        cF = ModulTempNTCError(self)
        cF.grid(column=10,row=0)

class ModulKapazität(Toplevel):
    def __init__(self,master = None):
        super().__init__(master = master)

        self.modulframe = ttk.Frame(self, padding = 10)
        self.modulframe.grid()

        cF = ModulCapCapacity(self.modulframe)
        cF.grid(column=1,row=1)

        eb = ttk.Button(self.modulframe,text="Fenster schließen",command=self.destroy)
        eb.grid(column=10,row=10)        

class ModulKalibrierung(Toplevel):
    def __init__(self,master = None):
        super().__init__(master = master)

        self.modulframe = ttk.Frame(self,padding = 10)
        self.modulframe.grid()

        ttk.Label(self.modulframe, text="Kalibrierungsmodul", padding=10, font='20').grid(column=1,row=0)

        cal = SensorRead(self.modulframe)
        cal.grid(column=0,row=1)

        eb = ttk.Button(self.modulframe,text="Fenster schließen",command=self.destroy)
        eb.grid(column=10,row=10) 







