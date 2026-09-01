from .. import OBDMain
from ..OBDMain import dprint
'''

    def decode(self, value) -> OBDMain.CommandReturn:
'''

class DTC:
    _Table = {
        "0": "P0",
        "1": "P1",
        "2": "P2",
        "3": "P3",
        "4": "C0",
        "5": "C1",
        "6": "C2",
        "7": "C3",
        "8": "B0",
        "9": "B1",
        "A": "B2",
        "B": "B3",
        "C": "U0",
        "D": "U1",
        "E": "U2",
        "F": "U3",
        
    }

    def __init__(self,code) -> None:
        self.baseCode=code
        self.code = code
        self.testComplete = False
        self.state = "Active"
        self.milRequested = False
        if code[0] in self._Table:
            
            a = code[0]
            code = code[1:]
            self.code = self._Table[a] + code 
        pass
    def __str__(self) -> str:
        return self.code+ " "+ self.state
    def setStatus(self, statusByte):
        self.statusByte = statusByte
        statusbinary = bin(int(statusByte, 16))[2:].zfill(8)

        status = statusbinary[0:4]
        readinessFlag = status[3]
        storageState = status[1:3]
        MILRequest = status[0]

        dprint(statusbinary, status, readinessFlag, MILRequest,storageState)
        if readinessFlag == "0":
            self.testComplete = True
        if MILRequest == "1":
            self.milRequested = True
        
        storageStateTable = {
            "00" : "Stored",
            "01": "Stored",
            "10": "Pending",
            "11": "Active"
        }

        if storageState in storageStateTable:
            self.state = storageStateTable[storageState]
class NoResponse:
    def __init__(self) -> None:
        pass

class KWPReadFaultsReturn(OBDMain.ReturnType):
    def decode(self, value) -> OBDMain.CommandReturn:
        value = value.splitlines()

        byteList = []
        linenum = 0
        linenumInLineEver = False
        for line in value:
            if f"{linenum}:" in line:
                linenumInLineEver = True
                line = line.split(f"{linenum}:")
                line = line[1]
                dprint(value)
                dprint(line)
                dprint(linenum)
                if (line.startswith("58") or line.startswith(" 58")):       
                    line = line.removeprefix("58 ")
                    line = line.removeprefix(" 58 ")
                    
                    numdtcs = line[0:2]
                    dprint(numdtcs + "!")
                    line = line.removeprefix(numdtcs + " ")
                    ind = 0
                    for char in line:
                        dprint(char)
                        if ind+1 < len(line):
                            if char != " " and line[ind + 1] != " ":
                                byteList.append(char+line[ind + 1])
                        ind+=1
                elif linenum > 0:
                    line = line.removeprefix(" ")
                    ind = 0
                    for char in line:
                        if ind+1 < len(line):
                            if char != " " and line[ind + 1] != " ":
                                dprint(ind)
                                dprint(char, line[ind+1])
                                if not line[ind + 1].endswith(":"):
                                    byteList.append(char+line[ind + 1])
                        ind+=1
                linenum += 1
            elif (line.startswith("58") or line.startswith(" 58")):       
                    linenumInLineEver = True
                    line = line.removeprefix("58 ")
                    line = line.removeprefix(" 58 ")
                    
                    numdtcs = line[0:2]
                    dprint(numdtcs + "!")
                    line = line.removeprefix(numdtcs + " ")
                    ind = 0
                    for char in line:
                        dprint(char)
                        if ind+1 < len(line):
                            if char != " " and line[ind + 1] != " ":
                                byteList.append(char+line[ind + 1])
                        ind+=1
            dprint(byteList, linenum)  
        ind = 0
        countInd = 1
        dtcList:list[DTC] = []
        for byte in byteList:
            
            if countInd != 3:
                dprint(countInd)
                if countInd != 2 and ind+1 < len(byteList):
                    if byte + byteList[ind+1] != "FFFF":
                        dtcList.append(DTC(byte + byteList[ind+1]))
                countInd+=1    
            else:
                if byte != "FF":
                    dtcList[-1].setStatus(byte)
                countInd=1
            ind+=1

        dprint(dtcList)
        for dtc in dtcList:
            dprint(dtc.code, dtc.state,dtc.milRequested, dtc.testComplete)
        if linenumInLineEver:
            return OBDMain.CommandReturn(dtcList, "ListOfDtcs", str(dtcList))
        else:
            return OBDMain.CommandReturn(NoResponse(), "NoResponseFromECU")
    

class KWPResponse(OBDMain.ReturnType):
    def __init__(self, id) -> None:
        self.id = id
    def decode(self, value:str) -> OBDMain.CommandReturn:
        id = int(self.id, 16) + int("40", 16)
        hexid = hex(id)[2:].upper()
        if hexid in value:
            return OBDMain.CommandReturn(True, "Success")
        else:
            dprint(hexid)
            return OBDMain.CommandReturn(False, "Error")
class KWPVinResponse(OBDMain.ReturnType):
    def __init__(self,id) -> None:
        self.id = id
    def decode(self, value) -> OBDMain.CommandReturn:
        id = int(self.id, 16) + int("40", 16)
        hexid = hex(id)[2:].upper()
        byteList = []
        linenum = 0
        if hexid in value:
            for line in value:
                if f"{linenum}:" in line:
                    linenumInLineEver = True
                    line = line.split(f"{linenum}:")
                    line = line[1]
                    dprint(value)
                    dprint(line)
                    dprint(linenum)
                    if (line.startswith(hexid) or line.startswith(f" {hexid}")):       
                        line = line.removeprefix(f"{hexid} ")
                        line = line.removeprefix(f" {hexid} ")
                        line = line.removeprefix(f"90 ")
                        ind = 0
                        for char in line:
                            dprint(char)
                            if ind+1 < len(line):
                                if char != " " and line[ind + 1] != " ":
                                    byteList.append(char+line[ind + 1])
                            ind+=1
                    elif linenum > 0:
                        line = line.removeprefix(" ")
                        ind = 0
                        for char in line:
                            if ind+1 < len(line):
                                if char != " " and line[ind + 1] != " ":
                                    dprint(ind)
                                    dprint(char, line[ind+1])
                                    if not line[ind + 1].endswith(":"):
                                        byteList.append(char+line[ind + 1])
                            ind+=1
                    linenum += 1
                elif (line.startswith(hexid) or line.startswith(f" {hexid}")):       
                        linenumInLineEver = True
                        line = line.removeprefix(f"{hexid} ")
                        line = line.removeprefix(f" {hexid} ")
                        line = line.removeprefix(f"90 ")                        
                        ind = 0
                        for char in line:
                            dprint(char)
                            if ind+1 < len(line):
                                if char != " " and line[ind + 1] != " ":
                                    byteList.append(char+line[ind + 1])
                            ind+=1
                dprint(byteList, linenum) 
            
            str2 = ""
            for byte in byteList:
                str2 += byte
            if linenumInLineEver:
                return OBDMain.CommandReturn(str2, "ListOfDtcs")
            else:
                return OBDMain.CommandReturn(NoResponse(), "NoResponseFromECU")
ReadDTCS_KWP = OBDMain.Command(
    "18", 
    KWPReadFaultsReturn(),
    description="Read faults from ecu", 
)
ReadVIN_KWP = OBDMain.Command(
    "1A 90", 
    KWPVinResponse("1A")
)
EscalateConnection_KWP = OBDMain.Command(
    "10",
    KWPResponse("10"),
    description="Escalate connection to access advanced features"
)
TesterPresent = OBDMain.Command(
    "3E",
    KWPResponse("3E"),
    description="Continue session"
),
RestartEcu = OBDMain.Command(
    "11",
    KWPResponse("11"),
    description="Reset ECU"
)
ClearDTC = OBDMain.Command(
    "14", 
    KWPResponse("14"),
    "Clear DTCs"
)
