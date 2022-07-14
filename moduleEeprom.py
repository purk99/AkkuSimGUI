
from tkinter import *
from tkinter import ttk
from tkinter import font

import numpy

from tools_V21 import *
from EepromData import *
from EepromAccess import *
import csv
from os.path import exists

class ModulEepromKomplett(ttk.Frame):
    def __init__(self,parent):
        ttk.Frame.__init__(self,parent)

        self.eeprom = EepromControl()
        self.eeprom.setEeprom()

        self.grid()

        headlabel = ttk.Label(self,text="EEPROM-Daten", font='20')
        headlabel.grid(column=0,row=0, columnspan=4)

        counter = 0
        counter1 = 1

        self.valueF = [ttk.Label] * 150
        self.lfF = [ttk.Labelframe] * 150

        self.regChangeF = ttk.Labelframe(self,text="Registerwert ändern")
        self.regChangeF.grid(column=0,row=4, padx=3,pady=3,sticky=NSEW)

        self.paramFileF = ttk.Frame(self)
        self.paramFileF.grid(column=0,row=3,padx=3,pady=3,sticky=W)

        self.modulcanvas = Canvas(self, width=800, height=205,borderwidth=0)
        self.modulcanvas.grid(column=0,row=1, columnspan=2, sticky=W)

        self.modulframe = ttk.Frame(self.modulcanvas)
        #self.modulframe.grid(column=0,row=1) 

        self.modulcanvas.create_window(0,0,anchor=NW, window=self.modulframe, tags="self.frame")
        self.modulframe.bind("<Configure>", self.onFrameConfigure)

        self.sb = ttk.Scrollbar(self, orient=HORIZONTAL)
        self.sb.grid(column=0,row=2, columnspan=4, sticky=EW)  

        #eb = ttk.Button(self,text="Fenster schließen",command=self.destroy)
        #eb.grid(column=0,row=5)

        self.modulcanvas.config(xscrollcommand=self.sb.set)
        self.sb.config(command=self.modulcanvas.xview)   
        self.modulcanvas.configure(scrollregion=self.modulcanvas.bbox("all"))
        
        for p in range(150):
            indexString = "Pos: {}".format(p)
            self.lfF[p] = ttk.Labelframe(self.modulframe,text=indexString)
            self.lfF[p].grid(column=counter,row=counter1,padx=1)

            counter1 += 1
            if counter1%6 == 0:
                counter += 1
                counter1 = 1
                
        for i in range(150):            
            self.valueF[i] = ttk.Label(self.lfF[i],text=hex(int(EepromDataComplete[i])))
            self.valueF[i].grid(column=1,row=0, sticky=EW)

        ###Single Register Changes Begin
        ttk.Label(self.regChangeF,text="Register wählen").grid(column=0,row=0)

        self.regCombo = ttk.Combobox(self.regChangeF,values=(list(range(150))))
        self.regCombo.grid(column=0,row=1)

        ttk.Label(self.regChangeF,text="Wert wählen").grid(column=1,row=0)

        self.regValCombo = ttk.Combobox(self.regChangeF,values=(list(range(256))))
        self.regValCombo.grid(column=1,row=1)

        self.parChB = ttk.Button(self.regChangeF,text="Parameter ändern",command=self.updateRegValue)
        self.parChB.grid(column=0,row=2,columnspan=2)

        self.resB = ttk.Button(self.regChangeF,text="Auf Standardwerte zurücksetzen",padding=10, command=self.eeprom.setEeprom)
        self.resB.grid(column=2,row=0,rowspan=3,pady=3,padx=3,sticky=NS)

        ###Parameter File Load/Save Begin
        paramSave = ttk.Labelframe(self.paramFileF,text="Neue Datei erzeugen",padding=5)
        paramSave.grid(column=1,row=0, sticky=NS)#, sticky=EW)
        self.fileName = ttk.Entry(paramSave)
        self.fileName.grid(column=0,row=0)
        ttk.Button(paramSave,text="aktuellen Parametersatz \nspeichern",command=self.createNewParamFile).grid(column=1,row=0)

        paramLoad = ttk.Labelframe(self.paramFileF,text="Alte Datei laden", padding=5)
        paramLoad.grid(column=0,row=0)#, sticky=EW)
        ttk.Label(paramLoad,text="Groß-/Kleinschreibung beachten\nNur Dateinamen angeben!").grid(column=0,row=0)
        self.fileLoadName = ttk.Entry(paramLoad)
        self.fileLoadName.grid(column=1,row=1)
        ttk.Button(paramLoad,text="Vorhandenen Parametersatz Laden",command=self.loadParamFile).grid(column=0,row=1)        ###Parameter Load/Save End
        #Parameter File Load/Save End
    def createNewParamFile(self):

        f = open("./Parametersätze/{}".format(self.fileName.get()),'w')
        writer = csv.writer(f)
        writer.writerow(EepromDataComplete)
        f.close()

        infoF = ttk.Frame(self,padding=20,relief='ridge')
        infoF.grid(column=0,row=1,sticky=N ,columnspan=10,rowspan=10)

        infoT = ttk.Label(infoF,text="Neue Datei erzeugt,\nbitte bestätigen",font=15)
        infoT.grid(column=1,row=0)

        infoExitB = ttk.Button(infoF,text="Bestätigen",command=infoF.destroy)
        infoExitB.grid(column=1,row=1)

    def loadParamFile(self):
        #if exists(int("./Parametersätze/{}".format(int(self.fileLoadName.get())))) == True:
        if exists(("./Parametersätze/{}".format((self.fileLoadName.get())))) == True:
            file = open("./Parametersätze/{}".format((self.fileLoadName.get())))
            arr = numpy.loadtxt(file,delimiter=',')

            for p in range(size(EepromDataComplete)):
                EepromDataComplete[p] = arr[p]
                self.valueF[p].configure(text=EepromDataComplete[p])

            #sendeBefehl an Arduino fehlt noch

            infoF = ttk.Frame(self,padding=20,relief='ridge')
            infoF.grid(column=0,row=1,sticky=N ,columnspan=10,rowspan=10)

            infoT = ttk.Label(infoF,text="Parameter geladen,\nDaten Auf Arduino übertragen,\nbitte bestätigen",font=15)
            infoT.grid(column=1,row=0)

            infoExitB = ttk.Button(infoF,text="Bestätigen",command=infoF.destroy)
            infoExitB.grid(column=1,row=1)
        else:
            infoF = ttk.Frame(self,padding=20,relief='ridge')
            infoF.grid(column=0,row=1,sticky=N ,columnspan=10,rowspan=10)

            infoT = ttk.Label(infoF,text="Datei nicht vorhanden\noder Pfad falsch!\nbitte bestätigen",font=15)
            infoT.grid(column=1,row=0)

            infoExitB = ttk.Button(infoF,text="Bestätigen",command=infoF.destroy)
            infoExitB.grid(column=1,row=1)

    def onFrameConfigure(self,event):
        self.modulcanvas.configure(scrollregion=self.modulcanvas.bbox("all"))

    def updateRegValue(self):
        #change Eeprom-Value on Raspberry side
        EepromDataComplete[int(self.regCombo.get())] = int(self.regValCombo.get())
        #Update GUI
        self.valueF[int(self.regCombo.get())].configure(text=EepromDataComplete[int(self.regCombo.get())])
        #change EEPROM-Value on Arduino
        self.eeprom.writeSingleRegister(int(self.regCombo.get()), int(self.regValCombo.get()))
    






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
