from __future__ import annotations

import package.bus as _bus
class fault:
    def __init__(self, code, active, history) -> None:
        if not isinstance(code, str):
            raise TypeError("Code is not a string")
        if not isinstance(active, bool):
            raise TypeError("Active is not a boolean")
        if not isinstance(history, bool):
            raise TypeError("History is not a boolean")
        
        self.code = code
        self.active = active
        self.history = history
        pass
    
    def getState(self):
        if self.active:
            return "active"
        elif self.history:
            return "history"
        else:
            return "pending"
        

class ecu:

    def getFaults(self):
        return self.faults
    def __init__(self,bus:_bus.Bus, id:int, name:str) -> None:
        self.bus = bus
        self.name = name
        self.id = id
        bus.Register(self, id)
        self.faults:list[fault] = []
        pass
    
    def throwFault(self, fault:fault):
        print(fault.code)

        faultExists = False
        for fault2 in self.faults:
            if fault2.code == fault.code:
                faultExists = True
                break
        if not faultExists:
            self.faults.append(fault)

    def sendMessage(self, recieverId, message:_bus.Message):
        print(self.name, recieverId, message.content)
        response = self.bus.sendMessage(self, recieverId, message)
    
        if response == None or response == False:
            self.throwFault(fault("U1002", True, False))
            return None
        if not response.message.isValid():
            self.throwFault(fault("U1001", True, False))
            return None

        return response
    def recieveMessage(self, sender:ecu, message:_bus.Message):
        if message.isValid():
            if message.content == "ping":
                return _bus.Message(_bus.AcknowledgementType(), _bus.Acknowledgement())
            if message.content == "ReadFaults":
                return _bus.Message(_bus.ListType(_bus.FaultType()), self.getFaults())
            elif message.content == "clearFaults":
                self.faults = []
                return _bus.Message(_bus.AcknowledgementType(), _bus.Acknowledgement)
        else:
            self.throwFault(fault("U1001", True, False))
            return None

    def mainloop(self, *args):
        pass

class Gateway(ecu):
    
    def mainloop(self, *args):
        
        for id, ecu in self.bus.ecuList.items():
            if id != 0:
                faults:list[fault] = self.faults
                for fault in faults:

                    print(self.name, " - ", fault.code, f"({fault.getState()})")

                response = self.sendMessage(id, _bus.GetFaultMessage())
                
                if response != None:
                    print(response, response.message.content)
                    faults:list[fault] = response.message.content
                    for fault in faults:

                        print(ecu.name, " - ", fault.code, f"({fault.getState()})")
                else:
                    response = self.sendMessage(10,_bus.Message(_bus.StringType(), "ActivateMIL-FCM"),)


class Test(ecu):
    def sendMessage(self, recieverId, message:_bus.Message):
        print(self.name, recieverId, message.content)
        message2 = _bus.Message(_bus.IntType(), message.content)
        response = self.bus.sendMessage(self, recieverId, message2)
        if response == None or response == False:
            self.throwFault(fault("U1002", True, False))
        return response
    def recieveMessage(self, sender: ecu, message: _bus.Message):
        return None
    def mainloop(self, *args):
        for id, ecu in self.bus.ecuList.items():
            if id != 9:
                response = self.sendMessage(id, _bus.GetFaultMessage())
                if response != None:
                    print(response, response.message.content)
                    faults:list[fault] = response.message.content

                    for fault in faults:

                        print(ecu.name, " - ", fault.code, f"({fault.getState()})")
                        