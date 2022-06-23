from re import T
from tkinter import ttk
from tkinter import *
#from moduleEeprom import *

from moduleSpannung import *
from moduleEeprom import *
from moduleTemp import ModulTempHysterese, ModulTempNTCError
from moduleKapazität import *
from moduleCalibration import *
from tools_V21 import *

class ModulSpannung(Toplevel):
    def __init__(self, master = None):
        super().__init__(master = master)
        
        eeprom = EepromControl()
        
        self.modulframe = ttk.Frame(self, relief='ridge')
        self.modulframe.grid(column=0,row=1)

        label2 = ttk.Label(self,text="Testmodul Spannung", font='30',padding=5)
        label2.grid(column=1,row=0)
        
        self.meas = SensorRead(self.modulframe)
        self.meas.grid(column=1,row=1)

        self.vDisCh = ModulSpannungTEntladung(self.modulframe)
        self.vDisCh.grid(column=0,row=1)

        self.oV = ModulSpannungUeIm(self.modulframe)
        self.oV.grid(column=0,row=2)        

        eb = ttk.Button(self,text="Fenster schließen",command=self.destroy)
        eb.grid(column=1,row=5)

class ModulEeprom(Toplevel):
    def __init__(self,master = None):
        super().__init__(master = master)

        self.modulframe = ttk.Frame(self, padding=10)
        self.modulframe.grid()

        headLabel = ttk.Label(self.modulframe, text="Testmodul EEPROM",font='15')
        headLabel.grid(column=1,row=0)

        #CC,CV,CVende, Temperaturbereiche
        buttonLcyc = ttk.Button(self.modulframe, text="Testprogramm Ladezyklen", padding=5,command=self.showModulEepromCycleParam)
        buttonLcyc.grid(column=0,row=1,padx=5,pady=5)

        #12V Akku als 18V Akku definieren
        buttonErr = ttk.Button(self.modulframe,text="Testprogramm Ladeparameter", padding = 5, command=self.showModulEepromChargeParam)
        buttonErr.grid(column=0,row=2,padx=5,pady=5)

        eb = ttk.Button(self.modulframe,text="Fenster schließen",command=self.destroy)
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
        self.attributes('-fullscreen', True)

        self.mainframe = ttk.Frame(self)
        self.mainframe.grid(sticky=NSEW)        

        headLabel = ttk.Label(self.mainframe, text="Testmodul Temperaturen", font='20')
        headLabel.grid(column=1,row=0)

        ntcB = ttk.Button(self.mainframe,text="Testmodul NTC Error",padding=10, command=self.showModulNTCError)
        ntcB.grid(column=0, row=1, sticky=EW)

        hystB = ttk.Button(self.mainframe,text="Testmodul Temperaturhysterese",padding=10, command=self.showModulTempHysterese)
        hystB.grid(column=0, row=2)

        eb = ttk.Button(self.mainframe,text="Programm Beenden",command = self.destroy) 
        eb.grid(column=0,row=10, sticky=EW)

    def showModulNTCError(self):
        ModulTempNTCError()

    def showModulTempHysterese(self):
        ModulTempHysterese()


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

        cal = ModulKalibirerungAllgemein(self)
        cal.grid(column=0,row=2)

        eb = ttk.Button(self.modulframe,text="Fenster schließen",command=self.destroy)
        eb.grid(column=10,row=10) 







