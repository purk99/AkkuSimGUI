from tkinter import *
from tkinter import ttk

from EepromData import *
from tools_V21 import EepromControl


class EepromInfo(Toplevel):
    def __init__(self,master = None):
        super().__init__(master = master)

        modulFrame = ttk.Frame(self,padding=10)
        modulFrame.grid()

        headLabel = ttk.Label(modulFrame,text="Eeprom Informationen")
        headLabel.grid(column=1,row=0)

        chargeButton = ttk.Button(modulFrame, text="Ladeparameter",command=self.chargeParam)
        chargeButton.grid(column=0,row=1)

        cycleButton = ttk.Button(modulFrame,text="Ladezyklen",command=self.cycleParam)
        cycleButton.grid(column=0,row=2)

        rButton = ttk.Button(modulFrame, text="andere Parameter",command=self.safetyParam)
        rButton.grid(column=0,row=3)

        eb = ttk.Button(modulFrame,text="Exit",command=self.destroy)
        eb.grid(column=10,row=10)

    def chargeParam(self):
        cp = EepromChargeParam(self)
        cp.grid(column=0,row=10)

    def cycleParam(self):
        cp = EepromCycleParam(self)
        cp.grid(column=10,row=0)
    
    def safetyParam(self):
        cp = EepromSafetyParam(self)
        cp.grid(column=10,row=10)
    
class EepromChargeParam(ttk.Frame):
    def __init__(self,parent):
        ttk.Frame.__init__(self,parent)

        self.grid()
        self.configure(relief="ridge",padding=10)

        ttk.Label(self,text="Ladeparameter").grid(column=1,row=0,padx=5)
    
        ttk.Label(self,text="T_min").grid(column=0,row=1,padx=5)
        tminLabel = ttk.Label(self,text=EepromDataCharge[0])
        tminLabel.grid(column=2,row=1)

        ttk.Label(self,text="T_cold").grid(column=0,row=2,padx=5)
        tcoldLabel = ttk.Label(self,text=EepromDataCharge[1])
        tcoldLabel.grid(column=2,row=2)

        ttk.Label(self,text="T_warm").grid(column=0,row=3,padx=5)
        twarmLabel = ttk.Label(self,text=EepromDataCharge[2])
        twarmLabel.grid(column=2,row=3)

        ttk.Label(self,text="T_max").grid(column=0,row=4,padx=5)
        tmaxLabel = ttk.Label(self,text=EepromDataCharge[3])
        tmaxLabel.grid(column=2,row=4)

        ttk.Label(self,text="U_cold").grid(column=0,row=5,padx=5)
        ucoldLabel = ttk.Label(self,text=EepromDataCharge[4])
        ucoldLabel.grid(column=2,row=5)

        ttk.Label(self,text="U_warm").grid(column=0,row=6,padx=5)
        uwarmLabel = ttk.Label(self,text=EepromDataCharge[5])
        uwarmLabel.grid(column=2,row=6)

        ttk.Label(self,text="U_max").grid(column=0,row=7,padx=5)
        umaxLabel = ttk.Label(self,text=EepromDataCharge[6])
        umaxLabel.grid(column=2,row=7)
        
        ttk.Label(self,text="I_cold").grid(column=3,row=1,padx=5)
        icoldLabel = ttk.Label(self,text=EepromDataCharge[7])
        icoldLabel.grid(column=4,row=1)

        ttk.Label(self,text="I_warm").grid(column=3,row=2,padx=5)
        iwarmLabel = ttk.Label(self,text=EepromDataCharge[8])
        iwarmLabel.grid(column=4,row=2)

        ttk.Label(self,text="I_max").grid(column=3,row=3,padx=5)
        imaxLabel = ttk.Label(self,text=EepromDataCharge[9])
        imaxLabel.grid(column=4,row=3)

        ttk.Label(self,text="variable Ladeparameter").grid(column=3, row=5,padx=5)
        parActLabel = ttk.Label(self,text=EepromDataCharge[10])
        parActLabel.grid(column=4,row=5)

        self.varChargeActText = StringVar()
        self.varChargeActText.set("Variable Parameter: ein")
        self.changeParActB = ttk.Button(self,textvariable=self.varChargeActText,command=self.changeVarCharge)
        self.changeParActB.grid(column=3,row=6)

        #self.updateChargeLabels()

        uB = ttk.Button(self,text="Daten aktualisieren", command=self.updateChargeLabels)
        uB.grid(column=0,row=10)

        ###Änderungen an Charge-Parametern###
        paramChangeL = ttk.Label(self,text="Parameter: ")
        paramChangeL.grid(column=1,row=10)

        #Combobox
        self.combo = ttk.Combobox(self,values=[  "T_min",
                                            "T_cold",
                                            "T_max",
                                            "U_cold",
                                            "U_warm",
                                            "U_max",
                                            "I_cold",
                                            "I_warm",
                                            "I_max"
                                        ])
        self.combo.grid(column=2,row=10)

        updateB = ttk.Button(self,text="Parameter ändern",command=self.changeChargeLabels)
        updateB.grid(column=3,row=10)

        valL = ttk.Label(self,text="Wert: ")
        valL.grid(column=1,row=11)

        self.valCombo = ttk.Combobox(self,values=EepromDataValues)
        self.valCombo.grid(column=2,row=11)
        
        
        self.tchargeLabels = [  tminLabel,
                                tcoldLabel,
                                tmaxLabel,
                                ucoldLabel,
                                uwarmLabel,
                                umaxLabel,
                                icoldLabel,
                                iwarmLabel,
                                imaxLabel,
                                parActLabel
                             ]

    def updateChargeLabels(self):
        i = 0
        for p in self.tchargeLabels:                	
            self.tchargeLabels[i].configure(text=EepromDataCharge[i])
            i += 1
    
    #unbedingt auf Reihenfolge und Position in EepromData.py achten!
    #bei Veränderung der Listen müssen die Indizes überprüft werden
    def changeChargeLabels(self):

        self.chargeParamSelect =  self.combo.current()
        EepromDataCharge[self.chargeParamSelect] = self.valCombo.get()
        
        #self.chargeParamselect + 10 -> ab Pos 10 fängt EepromDataCharge an
        EepromDataComplete[self.chargeParamSelect+10] = EepromDataCharge[self.chargeParamSelect]
        #aktualisierung Aller Parameter in GUI
        #print(EepromDataCharge[self.chargeParamSelect],end="\n")
        #print(EepromDataComplete[self.chargeParamSelect+10])
        self.updateChargeLabels()
        #Eeprom-Daten auf Arduino überschreiben
        self.changeEepromData(self.chargeParamSelect+10,EepromDataCharge[self.chargeParamSelect])

    #Änderung von Parametern auf Arduino
    def changeEepromData(self,adress,content):
        arduninoEeprom = EepromControl()
        arduninoEeprom.sendPackage(uartCMD["WriteSingleReg"],adress,content)

    def changeVarCharge(self):
        
        if EepromDataCharge[10] == 0xF0:
            self.varChargeActText.set("Variable Parameter: ein")
            EepromDataCharge[10] = 0x0F
            #EepromDataComplete[20] = EepromDataCharge[10]
            self.changeEepromData(20,EepromDataCharge[10])
            self.updateChargeLabels()
        else:
            self.varChargeActText.set("Variable Parameter: aus")
            EepromDataCharge[10] = 0xF0
            #EepromDataComplete[20] = EepromDataCharge[10]
            self.changeEepromData(20,EepromDataCharge[10])
            self.updateChargeLabels()

#kann weg
class EepromParamChange(ttk.Frame):
    def __init__(self,parent):
        ttk.Frame.__init__(self,parent)

        self.grid()
        self.config(relief="ridge", padding=10)
        
        ttk.Label(self,text="Parameter ändern").grid(column=1,row=0)
        

class EepromCycleParam(ttk.Frame):
    def __init__(self,parent):
        ttk.Frame.__init__(self,parent)

        self.grid()
        self.config(relief="ridge",padding=10)

        ttk.Label(self,text="Zyklusparameter").grid(column=1,row=0)

        ttk.Label(self,text="CC-Starts").grid(column=0,row=1)
        ###Byte 1
        ccstartLabel1 = ttk.Label(self,text=EepromDataCycle[0])
        ccstartLabel1.grid(column=1,row=1)
        ###Byte 2
        ccstartLabel2 = ttk.Label(self,text=EepromDataCycle[1])
        ccstartLabel2.grid(column=2,row=1)

        ttk.Label(self,text="CV-Starts").grid(column=0,row=2)
        ###Byte 1
        cvStartLabel1 = ttk.Label(self,text=EepromDataCycle[2])
        cvStartLabel1.grid(column=1,row=2)
        ###byte 2
        cvStartLabel2 = ttk.Label(self,text=EepromDataCycle[3])
        cvStartLabel2.grid(column=2,row=2)

        ttk.Label(self,text="CV-Stopps").grid(column=0,row=3)
        ###Byte 1
        cvStoplabel1 = ttk.Label(self,text=EepromDataCycle[4])
        cvStoplabel1.grid(column=1,row=3)
        ###Byte 2
        cvStoplabel2 = ttk.Label(self,text=EepromDataCycle[5])
        cvStoplabel2.grid(column=2,row=3)

        self.cycleLabels = [ccstartLabel1,
                            ccstartLabel2,
                            cvStartLabel1,
                            cvStartLabel2,
                            cvStoplabel1,
                            cvStoplabel2
                            ]

    def updateCycleLabels(self):
        i = 0
        for p in self.cycleLabels:
            self.cycleLabels[i].configure(text=EepromDataCycle[i])

class EepromSafetyParam(ttk.Frame):


    def __init__(self,parent):
        ttk.Frame.__init__(self,parent)

        self.grid()
        self.configure(relief="ridge",padding=10)

        ttk.Label(self,text="Safetyparameter").grid(column=0,row=0)

        ttk.Label(self,text="Safteybytes").grid(column=0,row=1)
        ###Byte 1
        safeBLabel1 = ttk.Label(self,text=EepromDataSafety[0])
        safeBLabel1.grid(column=1,row=1)
        ###Byte 2
        safeBlabel2 = ttk.Label(self,text=EepromDataSafety[1])
        safeBlabel2.grid(column=2,row=1)

        ttk.Label(self,text="Zellen in Serie").grid(column=0,row=2)
        cellSerLabel = ttk.Label(self,text=EepromDataSafety[2])
        cellSerLabel.grid(column=1,row=2)

        self.safetyLabels = [   safeBLabel1,
                                safeBlabel2,
                                cellSerLabel
                            ]

    def updateSafetyLabels(self):
        i = 0
        for p in self.safetyLabels:
            self.safetyLabels[i].configure(text=EepromDataSafety[i])

    