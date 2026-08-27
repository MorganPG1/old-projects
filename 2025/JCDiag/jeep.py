from obd import Module, OBDReader, ModuleConnection, Car
import time
class KWPConnection(ModuleConnection):
    def __init__(self, reader:OBDReader, can_id:str, can_return:str):

        reader.send("AT D\r") #Hide DLC
        reader.send("AT E0\r") #Turn off echo
        reader.send("AT ST 1F\r") #Set timeout
        reader.send("AT SP A6\r") #Set protocol
        reader.send(f"AT SH {can_id}\r") #Set header to ecu address
        reader.send(f"AT FC SH {can_id}\r") #Set flow control header to ecu address
        reader.send(f"AT CRA {can_return}\r") #Set return address
        reader.send(f"AT FC SM 1\r") #Set flow control mode

        reader.send("10 92\r") #Put module into extended diagnostic mode
        response:str = reader.read()
        if response.startswith("50"): #$50 = Positive response for Start Diagnostic Session
            self.connected = True
        else:
            self.connected = False
        self.reader = reader
    
    def mainloop(self):
        self.reader.send("3E 02\r") #Tell the ECU that the diagnostic session is still active.

    def ReadFaults(self):
        if self.connected:
            self.reader.clear()
            self.reader.send("18 00 FF00\r") #Request all dtcs
            response = self.reader.read()
            response = response.replace("7F 18 78", "") #Remove ECU Not Ready response
            
            lines:list[str] = response.splitlines() #Split into lines
            #print(lines)
            byteList = []
            for line in lines:
                if lines.index(line) == 0 and line.startswith("0:"):
                    print(line)
                    line = line[2:] #Remove line number (not needed)
                
                line = line.replace(" ","")                
                print(line)
                
                if line.startswith("58"): #Check if its thr first line (includes number of dtcs)
                    line = line.removeprefix("58")
                    numDTC = line[0:2] #Get amount of dtcs
                    print(numDTC)
                   #print(numDTC, line)
                    line = line[2:] #Remove amount of dtcs from the line
               
                #print(line, len(line))
                if len(line) != 0:
                    for i in range(0,len(line)//2): #Loop through all the bytes
                        byte = line[0:2]
                        line = line[2:]
                        byteList.append(byte) #Add the bye to the list

              
            #print(byteList)
            dtclist = []
            for i in range(0,int(numDTC, 16)):
                li = 3*i
                b1:str = byteList[li]
                b2:str = byteList[li+1]
                status:str = byteList[li+2]
                
                table = {
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
                b1 = table[b1[0]] + b1[1:]
                dtclist.append((b1+b2, status))
            return dtclist
        else:
            return []
    def ClearFaults(self):
        self.reader.clear()
        self.reader.send("14 FF00")
class KWPModule(Module):
    def __init__(self, name:str, can_id:str, can_return:str):
        self.name = name
        self.id = can_id
        self.ret = can_return
    def connect(self, reader):
        return KWPConnection(reader, self.id, self.ret)
    
class Jeep(Car):
    def __init__(self, reader):
        self.modules = [
            KWPModule("SRS", "6E0", "51C"),
            KWPModule("4WD", "7B6", "7B7"),
            KWPModule("AMP", "7F0", "53E"),
            KWPModule("ABS", "784", "785"),
            KWPModule("AHBM", "710", "522"),
            KWPModule("DDM", "640", "508"),
            KWPModule("ESM", "788", "789"),
            KWPModule("VES", "7D0", "53A"),
            KWPModule("FCM", "620", "504"),
            KWPModule("HFM", "7F8", "53F"),
            KWPModule("HLM", "7C8", "539"),
            KWPModule("HVAC", "688", "511"),
            KWPModule("HSM", "6D8", "518"),
            KWPModule("IPC", "6A0", "514"),
            KWPModule("ITM", "670", "50E"),
            KWPModule("LRS", "780", "530"),
            KWPModule("LRSM", "708", "521"),
            KWPModule("MSMD", "660", "50C"),
            KWPModule("OCM", "6E8", "51D"),
            KWPModule("PTM", "698", "513"),
            KWPModule("PDM", "650", "50A"),
            KWPModule("PLM", "728", "525"),
            KWPModule("ECM", "7E0", "7E8"),
            KWPModule("RADIO", "680", "516"),
            KWPModule("SDAR", "7D8", "538"),
            KWPModule("SDVR", "738", "527"),
            KWPModule("SCM", "622", "484"),
            KWPModule("SCM_E", "6A8", "515"),
            KWPModule("SUNR", "638", "507"),
            KWPModule("TBCM", "6E0", "51C"), #TODO: GET ID FROM TBCM, THIS IS WRONG
            KWPModule("TCM", "7E1", "7E9"),
            KWPModule("WCM", "600", "500"),
            
            

        ]
        self.reader = reader
    def DecodeFaultStatus(self, status):
        statusByte = int(status, 16) #Convert hex string to integer
        #print(bin(statusByte))
        warningIndicator = statusByte & 0b10000000
        if warningIndicator != 0:
            warningIndicator = 1
        else:
            warningIndicator = 0

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
            readiness = 1
        else:
            readiness = 0
        return readiness, storageStateB1 + storageStateB2, warningIndicator
