########################################################
###         Zentrale Datei zum Speichern 
#                 von Zuständen 
###                Für Arduino
#       (sowohl EEPROM als auch NTC und Overvoltage)
########################################################

###                         !!ACHTUNG!!
#bei Veränderung der Listen müssen die Indizes in EepromAccess überprüft werden
#in EepromAccess wird auf diese Listen zugegriffen! Bei jeder Veränderung auf richtige
#Indizierung prüfen
###                         !!ACHTUNG!!

from numpy import *

###Commands für Arduino
uartCMD = {
    "eepromReadSingleReg"   :   0x01,
    "eepromWriteSingleReg"  :   0x02,
    "eepromReadAll"         :   0x03,
    "ntcRead"               :   0x04,
    "ntcWrite"              :   0x05,
    "voltageProtectRead"    :   0x06,
    "voltageProtectWrite"   :   0x07,
    "setEepromToNormalState":   0x08,
    "setEepromToSmallState" :   0x09
}

###Values, that are neccessary or appear more than once
EepromDataDict = {
    "safetyB1"      : 0x93,
    "safetyB2"      : 0xDA,
    "cellsInSer"    : 5,
    "U_min"         : 0x19,
    "capBat"        : 0xA,
    "U_charge"      : 0xC7,
    "max_temp"      : 0,
    "min_temp"      : 0xFF,
    "CellsInPar"    : 1,
    "numCCstart1"   : 0,
    "numCCstart2"   : 1,
    "numCVstart1"   : 0,
    "numCVstart2"   : 1,
    "numCVstop1"    : 0,
    "numCVstop2"    : 1,
    "numStartChaSub30Deg1"   : 0,
    "numStartChaSub30Deg2"   : 1,
    "T_min"         : 0x20,
    "T_cold"        : 0x22,
    "T_warm"        : 0x30,
    "T_max"         : 0x50,
    "U_cold"        : 0x20,
    "U_warm"        : 0x22,
    "U_max"         : 0x53,
    "I_cold"        : 0x20,
    "I_warm"        : 0x22,
    "I_max"         : 0x80,
    "varCharge"     : 0xF0
}

InfoDataDict = {
    "NTCvalue"      : 0xf0,
    "Overvoltage"   : 0xf0
                }
#bei Veränderung der Listen müssen die Indizes in EepromAccess überprüft werden
#in EepromAccess wird auf diese Listen zugegriffen! Bei jeder Veränderung auf richtige
#Indizierung prüfen
EepromDataComplete = [1] * 150

#contains data for ntc(0) and ov(1)
InfoData = [InfoDataDict["NTCvalue"],
            InfoDataDict["Overvoltage"]

            ]

EepromDataSafety = [EepromDataDict["safetyB1"],
                    EepromDataDict["safetyB2"],
                    EepromDataDict["cellsInSer"]
                ]

#bei Veränderung der Listen müssen die Indizes in EepromAccess überprüft werden
#in EepromAccess wird auf diese Listen zugegriffen! Bei jeder Veränderung auf richtige
#Indizierung prüfen
EepromDataCharge = [EepromDataDict["T_min"],
                    EepromDataDict["T_cold"],
                    EepromDataDict["T_warm"],
                    EepromDataDict["T_max"],
                    EepromDataDict["U_cold"],
                    EepromDataDict["U_warm"],
                    EepromDataDict["U_max"],
                    EepromDataDict["I_cold"],
                    EepromDataDict["I_warm"],
                    EepromDataDict["I_max"],
                    EepromDataDict["varCharge"]
                    ]
                    
EepromDataCycle = [ EepromDataDict["numCCstart1"],
                    EepromDataDict["numCCstart2"],
                    EepromDataDict["numCVstart1"],
                    EepromDataDict["numCVstart2"],
                    EepromDataDict["numCVstop1"],
                    EepromDataDict["numCVstop2"]
                ]

EepromDataValues = list(range(256))
CalibrationFine = list(arange(0,1,0.1))
CalibrationCoarse = list(range(0,6))

#Setup of Temprature Data of NTC
#file = open("/home/festool/Documents/AkkuSimGUI/NTCValues.CSV") 
file = open("NTCValues.CSV") 
arr = loadtxt(file,delimiter=';')

#values are set below
NTCTempValues = [None] * 116
NTCTemps = [None] * 116
for p in range(size(arr,0)):
    NTCTempValues[p] = int(arr[p][1])
    NTCTemps[p] = int(arr[p][0])
