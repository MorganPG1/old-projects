from enum import Enum
from obd import OBDReader
class DTCState(Enum):
    NO_DTC = 0b00
    HISTORY_DTC = 0b01
    PENDING_DTC = 0b10
    ACTIVE_DTC = 0b11

class DTC():
    def UpdateStatusByte(self, state, mil, testComplete):
        stateByte = bin(state.value)[2:]
        stateByte = stateByte.rjust(2, "0")
        print(stateByte)
        if mil: #Convert Booleans into a bit
            milBit = "1"
        else:
            milBit = "0"
        
        if testComplete:
            testBit = "0"
        else:
            testBit = "1"

        byte = f"{milBit}{stateByte}{testBit}0000"
        byte = int(byte, 2)
        self.statusByte = byte
    def getStatus(self):
        statusByte = int(self.statusByte, 16) #Convert hex string to integer
        warningIndicator = statusByte & 0b10000000
        if warningIndicator != 0:
            warningIndicator = True
        else:
            warningIndicator = False

        storageStateB2 = statusByte & 0b01000000
        storageStateB1 = statusByte & 0b00100000
        if storageStateB1 != 0:
            storageStateB1 = 1
        else:
            storageStateB1 = 0
        if storageStateB2 != 0:
            storageStateB2 = 1
        else:
            storageStateB2 = 0
        readiness = statusByte & 0b00010000
        if readiness != 0:
            readiness = False
        else:
            readiness = True
        return readiness, storageStateB1 + storageStateB2, warningIndicator
    def __init__(self, dtc:str, state:DTCState, mil:bool, testComplete:bool):
        self.statusByte = 0b00
        self.dtc = dtc
        self.UpdateStatusByte(state,mil,testComplete)
        pass
class ECU():
    def __init__(self, ecu_id:str, return_id:str):
        print(ecu_id)
        self.ecu_id = ecu_id
        self.sessionActive = False
        self.dtcs:list[DTC] = [DTC(
            "0710", DTCState.ACTIVE_DTC, True, True
        )]
        self.elevatedState = False
        self.return_id = return_id
        pass
    def setFault(self, dtc):
        self.dtcs.append(dtc)
    def clearFaults(self):
        self.dtcs = []
    def getFaults(self):
        return self.dtcs
    def sendData(self, data:str):
        byteList = data.split(" ")
        if len(byteList) > 1:
            request = byteList[0]
            if request == "10": #Start Diagnostic Session
                self.sessionActive = True
                self.elevatedState = True
                return f"50 {byteList[1]}"
            elif request == "14":
                if not self.elevatedState:
                    return f"7F 14 33"
                self.sessionActive = True
                self.clearFaults()
                return f"54 {byteList[1]} {byteList[2]}"
            elif request == "18":
                response = "58"
                NumDTC = str(len(self.getFaults())).rjust(2,"0")
                response += f" {NumDTC}"
                self.sessionActive = True
                for dtc in self.getFaults():
                    b1 = dtc.dtc[0:2]
                    b2 = dtc.dtc[2:]
                    b3 = hex(dtc.statusByte)[2:]
                    response += f" {b1} {b2} {b3}"
                
                return response
            elif request == "3E":
                self.sessionActive = True
                if byteList[1] == "01":
                    return "7E"

    def mainLoop(self):
        if not self.sessionActive:
            self.elevatedState = False


class Bus():
    def __init__(self):
        self.ecus:list[ECU] = []
        pass
    def add(self, ecu):
        self.ecus.append(ecu)
    def sendData(self,ecu_id:str,data):
        print("BUS DATA: ",ecu_id, data)
        for ecu in self.ecus:
            if type(ecu.ecu_id) == "str":
                if ecu.ecu_id.upper() == ecu_id.upper():
                    response = ecu.sendData(data)
                    self.sendData(ecu.return_id, response)
            else:
                if ecu_id.upper() in ecu.ecu_id:
                    response = ecu.sendData(data)
                    if response:
                        self.sendData(ecu.return_id, response)
                    
class EmulatedTester(OBDReader):
    def __init__(self, bus:Bus):
        self.ecu_id = []
        for ecu in bus.ecus:
            #print(ecu.id)
            if ecu != self:
                self.ecu_id.append(ecu.return_id)
        self.bus = bus
        self.currentEcu = ""
        self.buffer = ""
    def sendData(self,data):
        print("DATA:",data)
        self.buffer = data
        return None
    def send(self, data:str):
        if data.lower().startswith("at"): #Check if command is directed to the tester or the car
            data = data.lower().removeprefix("at ")
            if data.startswith("sh"):
                data = data.removeprefix("sh ")
                #print(data)

                self.currentEcu = data.replace(" ", "").replace("\r", "")
                print(self.currentEcu)
            self.buffer = "OK\n>"
        else:
            print("SENDING: ",self.currentEcu, data)
            self.bus.sendData(self.currentEcu, data)
    def read(self):
        bytelist = self.buffer.replace(" ", "\n").splitlines()
        if len(bytelist) > 8:
            output = ""
            for line in range(0,len(bytelist)//8):
                output += f"{line}: "
                
        else:
            print(self.buffer)
            return self.buffer
