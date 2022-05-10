######################################################
###             Hauptprogramm                      ###
######################################################

from cgitb import text
from distutils.command.config import config
from msilib.schema import TextStyle
from socket import ntohl
from tkinter import *
from tkinter import ttk
from tkinter import font
from tokenize import String
from turtle import bgcolor, setundobuffer, width
from pip import main
import time
#für UART
from time import sleep


######################################################
###             Variabeln                          ###
######################################################


#für GPIOs
#import RPi.GPIO as GPIO
#import time
#GPIO-Modus setzen
#GPIO.setmode(GPIO.BCM)

#def zustandAuslesen(adresse):
   # with SMBus(1) as bus:
    #    b = bus.read_byte_data(0xa2 , adresse)
#ausgabe.set(zustandAuslesen(eeprom_adresse))

def modusSpannungProgrammAuswahl(auswahl):
    global modusSpannungAuswahl
    if auswahl == 1:
        modusSpannungAuswahl.set(1) 
    elif auswahl == 2:
        modusSpannungAuswahl.set(2)   
    elif auswahl == 3:
        modusSpannungAuswahl.set(3)
    elif auswahl == 4:
        modusSpannungAuswahl.set(4) 
    
    print(modusSpannungAuswahl)


########################################################
###             Modulauswahl                         ###

def modusSpannung():


    #Fenster für Testmodul SPannung erscheint
    nt = Toplevel(root)
    nt.title('Window Spannung')
    nt.grid()

    #subframe = ttk.Frame(nt, padding=5).grid(column=0, row=0)
    #erst für Anwendung auf Pi oder zum testen
    #nt.attributes("-fullscreen",1)
    
    sb = ttk.Button(nt, text="Starte Test", padding=5)
  
    mb1 = ttk.Button(nt,width=20, text="Tiefenentladung",       command = lambda : modusSpannungProgrammAuswahl(1))
    mb2 = ttk.Button(nt,width=20, text="Ladeschlussspannung",   command = lambda : modusSpannungProgrammAuswahl(2))
    mb3 = ttk.Button(nt,width=20, text="Überladung",            command = lambda : modusSpannungProgrammAuswahl(3))
    mb4 = ttk.Button(nt,width=20, text="Zellimbalance",         command = lambda : modusSpannungProgrammAuswahl(4)) 

    global modusSpannungAuswahl
    nl = ttk.Label(nt,textvariable = modusSpannungAuswahl)
    eb = ttk.Button(nt, text="Fenster schließen",padding =5, command=nt.destroy)

    #erst für Anwendung auf Pi oder zum testen
    #nt.attributes("-fullscreen",1)
    sb.grid(column=0, row=10)
    
    mb1.grid(column=1,row=1)
    mb2.grid(column=1,row=2)
    mb3.grid(column=1,row=3)
    mb4.grid(column=1,row=4) 

    eb.grid(column=10,row=10)
    nl.grid(column=1,row=0)

    #if mb1.instate (['active']):
        #mb2.state(['disabled'])

def modusLZyklen():

    cvStartCounter = StringVar()
    ccStartCounter = StringVar()
    cvStopCounter  = StringVar()

    nt = Toplevel(root)
    nt.grid()
    nt.title('Window Ladezyklen')
    #erst für Anwendung auf Pi oder zum testen
    #nt.attributes("-fullscreen",1)

    nl = ttk.Label(nt,text="Modul Ladezyklen")
    l1 = ttk.Label(nt, text="Zähler CV-Phasen Beginn")
    l2 = ttk.Label(nt, text="Zähler CC-Phasen Beginn")
    l3 = ttk.Label(nt, text="Zähler CV-Phasen Ende")
    cvs= ttk.Label(nt,text=cvStartCounter)
    ccs= ttk.Label(nt,text=ccStartCounter)
    cve= ttk.Label(nt,text=cvStopCounter)

    eb = ttk.Button(nt, text="Fenster schließen", command=nt.destroy).grid(column=0,row=1)

    nl.grid(column=1,row=0)
    l1.grid(column=5,row=1)
    l2.grid(column=5,row=2)
    l3.grid(column=5,row=3)
    cvs.grid(column=6,row=1)
    ccs.grid(column=6,row=2)
    cve.grid(column=6,row=3)

def moduslStrom():

    nt = Toplevel(root)

    li = ttk.Label(nt,text="aktuell eingestellte Parameter")
    lTmin = ttk.Label(nt,text="Ladetemperatur Minimum")
    lTcld = ttk.Label(nt,text="Ladetemperatur max Strom")
    lTwrm = ttk.Label(nt,text="Ladetemperatur max Strom Grenze")
    lTmax = ttk.Label(nt,text="Ladetemperatur Maximum")

    eb = ttk.Button(nt,text="Exit",command=nt.destroy)

    li.grid(column=0,row=0)
    lTmin.grid(column=1,row=0)
    lTmax.grid(column=1,row=2)
    lTcld.grid(column=1,row=1)
    lTwrm.grid(column=1,row=3)
    eb.grid(column=10,row=10)

def modusTemp():
    nt = Toplevel(root)

    hl = ttk.Label(nt, text="Testmodus Temperaturen")
    l1 = ttk.Label(nt, text="Eingabe untere Temperatur")


###############################################################################
###     Hauptfenster, beinhaltet Buttons zum anwählen von Prüfmodulen       ###
###############################################################################
root = Tk()
root.title("Prüfmodulprogram Akkusimulator 2.0")
#nur benötigt für Anwendung auf RaspBi und zum Testen
#root.attributes("-fullscreen",1)

###############################################################################
###     variablen für Auswahl der Prüfprorgamme innerhalb einzelner Module  ###
modusSpannungAuswahl = StringVar()
modusLZyklenAuswahl = StringVar()
modusTempAuswahl = StringVar()


#Hauptmenü - Einstellungen
mainframe = ttk.Frame(root, padding= 10, relief="ridge", borderwidth=5)
mainframe.grid(column=0,row=0)

mainframe.option_add('*Font','20')
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

ttk.Label(mainframe, text = "Startmenü").grid(column=2,row=0)
#ttk.Label(mainframe, text = "Bitte Auswahl treffen").grid(column=2,row=1)

voltageTest = ttk.Button(mainframe,text="Testmodul Spannung",command=modusSpannung,padding=10,width=75).grid(column=2,row=3,pady=5)
eepromTest  = ttk.Button(mainframe,text="Testmodul EEPROM",command=modusLZyklen,padding=10,width=75).grid(column=2,row=4,pady=5)
stromTest   = ttk.Button(mainframe,text="Testmodus Ladestrom",command=moduslStrom,padding=10,width=75).grid(column=2,row=5,pady=5)
temperaturTest = ttk.Button(mainframe,text="Testmodul Temperatur",padding=10,width=75).grid(column=2,row=6,pady=5)
capacityTest = ttk.Button(mainframe,text="Testmodul Kapazität",padding=10,width=75).grid(column=2,row=7,pady=5)
#errorTest = ttk.Button(mainframe,text="Testmodul Fehlerzustände",padding=10,width=75).grid(column=2,row=8,pady=5)
#exitbutton
ttk.Button(mainframe,text="Exit", command=root.destroy, padding=10, width=15).grid(column=10, row=10)

#main thread
root.mainloop()

########################################################
###             Private Funktionen                   ###
########################################################


    

########################################################
###             Funktionen für Testmodul Spannung    ###

###Spannung intern prüfen
###Ladestrom messen
##abhängig von Spannung Fehler oder voller Ladestrom

    

###Ladespannung intern prüfen
###tatsächliche Ladespannung am Ende festhalten
def modusSpannung_lSpannung():
    pass

###imbalance und Überladung zusammen geprüft
###Überspannungsbit muss gesetzt sein
###abhängig von Gesamtspannung kleine/große imbalance erkennen
def modusSpannung_imbalance():
    pass

########################################################
###             Funktionen für Testmodul Ladezyklen  ###

