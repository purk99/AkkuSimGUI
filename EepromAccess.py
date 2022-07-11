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
        
        self.arduninoEeprom = EepromControl()
        self.arduninoEeprom.setEeprom()

        self.grid()
        self.configure(relief="ridge")
        
        self.valF = ttk.Frame(self, relief='ridge')
        self.valF.grid(column=0,row=1)
        
        self.parChangeF = ttk.Frame(self, relief='ridge')
        self.parChangeF.grid(column=1,row=1)

        ttk.Label(self,text="Ladeparameter",font='15').grid(column=1,row=0,sticky=EW)

        tMin = ttk.Labelframe(self.valF,text="T_min")
        tMin.grid(column=0,row=0,padx=1)
        tminLabel = ttk.Label(tMin,text=EepromDataComplete[108])
        tminLabel.grid(column=0,row=0)

        tCold = ttk.Labelframe(self.valF,text="T_cold")
        tCold.grid(column=0,row=1,padx=1)
        #ttk.Label(self.valF,text="T_cold").grid(column=0,row=2,padx=1, sticky=W)
        tcoldLabel = ttk.Label(tCold,text=EepromDataComplete[109])
        tcoldLabel.grid(column=0,row=0)

        tWarm = ttk.Labelframe(self.valF,text="T_warm")
        tWarm.grid(column=0,row=2,padx=1)
        #ttk.Label(self.valF,text="T_warm").grid(column=0,row=3,padx=1, sticky=W)
        twarmLabel = ttk.Label(tWarm,text=EepromDataComplete[110])
        twarmLabel.grid(column=0,row=0)

        tMax = ttk.Labelframe(self.valF,text="T_max")
        tMax.grid(column=0,row=3,padx=1)
        #ttk.Label(self.valF,text="T_max").grid(column=0,row=4,padx=1, sticky=W)
        tmaxLabel = ttk.Label(tMax,text=EepromDataComplete[111])
        tmaxLabel.grid(column=0,row=0)

        uCold = ttk.Labelframe(self.valF,text="U_cold")
        uCold.grid(column=0,row=4,padx=1)
        #ttk.Label(self.valF,text="U_cold").grid(column=0,row=5,padx=1, sticky=W)
        ucoldLabel = ttk.Label(uCold,text=EepromDataComplete[112])
        ucoldLabel.grid(column=0,row=0)

        uWarm = ttk.Labelframe(self.valF,text="U_warm")
        uWarm.grid(column=1,row=0,padx=1)
        #ttk.Label(self.valF,text="U_warm").grid(column=0,row=6,padx=1, sticky=W)
        uwarmLabel = ttk.Label(uWarm,text=EepromDataComplete[113])
        uwarmLabel.grid(column=0,row=0)

        uMax = ttk.Labelframe(self.valF,text="U_max")
        uMax.grid(column=1,row=1,padx=1)
        #ttk.Label(self.valF,text="U_max").grid(column=0,row=7,padx=1, sticky=W)
        umaxLabel = ttk.Label(uMax,text=EepromDataComplete[114])
        umaxLabel.grid(column=0,row=0)
        
        iCold = ttk.Labelframe(self.valF,text="I_cold")
        iCold.grid(column=1,row=2,padx=1)
        #ttk.Label(self.valF,text="I_cold").grid(column=3,row=1,padx=1, sticky=W)
        icoldLabel = ttk.Label(iCold,text=EepromDataComplete[115])
        icoldLabel.grid(column=0,row=0)

        iWarm= ttk.Labelframe(self.valF,text="I_warm")
        iWarm.grid(column=1,row=3,padx=1)
        #ttk.Label(self.valF,text="I_warm").grid(column=3,row=2,padx=1, sticky=W)
        iwarmLabel = ttk.Label(iWarm,text=EepromDataComplete[116])
        iwarmLabel.grid(column=0,row=0)

        iMax= ttk.Labelframe(self.valF,text="I_max")
        iMax.grid(column=1,row=4,padx=1)
        #ttk.Label(self.valF,text="I_max").grid(column=3,row=3,padx=1, sticky=W)
        imaxLabel = ttk.Label(iMax,text=EepromDataComplete[117])
        imaxLabel.grid(column=0,row=0)
        '''
        ttk.Label(self.valF,text="variable").grid(column=3, row=4,padx=1, sticky=W)
        parActLabel = ttk.Label(self.valF,text=EepromDataComplete[119])
        parActLabel.grid(column=4,row=5)        
        '''
        self.varChargeActText = StringVar()
        self.varChargeActText.set("Variable Parameter: inaktiv")
        self.changeParActB = ttk.Button(self.parChangeF,textvariable=self.varChargeActText,command=self.changeVarCharge)
        self.changeParActB.grid(column=1,row=0)

        ###Änderungen an Charge-Parametern###
        paramChangeL = ttk.Label(self.parChangeF,text="Parameter: ")
        paramChangeL.grid(column=0,row=1)

        #Combobox
        self.combo = ttk.Combobox(self.parChangeF,values=[  "T_min",
                                            "T_cold",
                                            "T_warm",
                                            "T_max",
                                            "U_cold",
                                            "U_warm",
                                            "U_max",
                                            "I_cold",
                                            "I_warm",
                                            "I_max"
                                        ])
        self.combo.grid(column=1,row=1)

        updateB = ttk.Button(self.parChangeF,text="Parameter ändern",command=self.changeChargeLabels)
        updateB.grid(column=0,row=3)

        valL = ttk.Label(self.parChangeF,text="Wert: ")
        valL.grid(column=0,row=2)

        self.valCombo = ttk.Combobox(self.parChangeF,values=EepromDataValues)
        self.valCombo.grid(column=1,row=2)
        
        
        self.tchargeLabels = [  tminLabel,
                                tcoldLabel,
                                twarmLabel,
                                tmaxLabel,
                                ucoldLabel,
                                uwarmLabel,
                                umaxLabel,
                                icoldLabel,
                                iwarmLabel,
                                imaxLabel
                                #parActLabel
                             ]

    def updateChargeLabels(self):
        i = 0
        for p in self.tchargeLabels:                	
            self.tchargeLabels[i].configure(text=EepromDataComplete[108 + i])
            i += 1
    
    #unbedingt auf Reihenfolge und Position in EepromData.py achten!
    #bei Veränderung der Listen müssen die Indizes überprüft werden
    def changeChargeLabels(self):

        self.chargeParamSelect =  self.combo.current()+108
        EepromDataComplete[self.chargeParamSelect] = self.valCombo.get()
        
        self.updateChargeLabels()
        #Eeprom-Daten auf Arduino überschreiben
        self.changeEepromData(self.chargeParamSelect,EepromDataComplete[self.chargeParamSelect])

    #Änderung von Parametern auf Arduino
    def changeEepromData(self,adress,content):
        self.arduninoEeprom.sendPackage(uartCMD["eepromWriteSingleReg"],adress,content)

    def changeVarCharge(self):
        
        if EepromDataComplete[119] != 0x0F:
            self.varChargeActText.set("Variable Parameter: aktiv")
            EepromDataComplete[119] = 0x0F
            self.changeEepromData(119,EepromDataComplete[119])
            self.updateChargeLabels()
        else:
            self.varChargeActText.set("Variable Parameter: inaktiv")
            EepromDataComplete[119] = 0xF0
            self.changeEepromData(119,EepromDataComplete[119])
            self.updateChargeLabels()

#currently not used
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

    