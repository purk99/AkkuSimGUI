########################################################
###         Zentrale Datei zum Speichern 
#                 von Zuständen 
###                Für Arduino
#       (sowohl EEPROM als auch NTC und Overvoltage)
########################################################

###Commands für Arduino
uartCMD = {
    "eepromReadSingleReg"   :   0x01,
    "eepromWriteSingleReg"  :   0x02,
    "eepromReadAll"         :   0x03,
    "ntcRead"               :   0x04,
    "ntcWrite"              :   0x05,
    "voltageProtectRead"    :   0x06,
    "voltageProtectWrite"   :   0x07
}


EepromDataDict = {
    "safetyB1"      : 0x93,
    "safetyB2"      : 0xDA,
    "cellsInSer"    : 0x20,
    "capBat"        : 0x0F,
    "numCCstart1"   : 0,
    "numCCstart2"   : 0,
    "numCVstart1"   : 0,
    "numCVstart2"   : 0,
    "numCVstop1"    : 0,
    "numCVstop2"    : 0,
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

EepromDataComplete = [  EepromDataDict["safetyB1"],
                        EepromDataDict["safetyB2"],
                        EepromDataDict["cellsInSer"],
                        EepromDataDict["capBat"],
                        EepromDataDict["numCCstart1"],
                        EepromDataDict["numCCstart2"],
                        EepromDataDict["numCVstart1"],
                        EepromDataDict["numCVstart2"],
                        EepromDataDict["numCVstop1"],
                        EepromDataDict["numCVstop2"],
                        EepromDataDict["T_min"],
                        EepromDataDict["T_cold"],
                        EepromDataDict["T_warm"],
                        EepromDataDict["U_cold"],
                        EepromDataDict["U_warm"],
                        EepromDataDict["U_max"],
                        EepromDataDict["I_cold"],
                        EepromDataDict["I_warm"],
                        EepromDataDict["I_max"],
                        EepromDataDict["varCharge"]
                    ]

InfoData = [InfoDataDict["NTCvalue"],
            InfoDataDict["Overvoltage"]

            ]

EepromDataSafety = [EepromDataDict["safetyB1"],
                    EepromDataDict["safetyB2"],
                    EepromDataDict["cellsInSer"]
                ]

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