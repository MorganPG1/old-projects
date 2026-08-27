from __future__ import annotations

import package.ecu as ecu
import time
    
class Acknowledgement:
    def __init__(self) -> None:
        pass


class MessageType:
    def __init__(self) -> None:
        pass
    def isOfType(self, content):
        '''
        Takes content and checks if it is of the correct message type. Will throw a incorrect message type dtc in the gateway module.
        '''
        raise NotImplementedError("MessageType is not to be used, make a child class or use one of the example classes (StringType, IntType and BinaryType)")
    
class IntType(MessageType):
    def __init__(self) -> None:
        super().__init__()
    
    def isOfType(self, content):
        '''
        Takes content and checks if it is of the correct message type. Will throw a incorrect message type dtc in the gateway module.
        '''
        return isinstance(content, int)
        
class StringType(MessageType):
    def __init__(self) -> None:
        super().__init__()
    
    def isOfType(self, content):
        '''
        Takes content and checks if it is of the correct message type. Will throw a incorrect message type dtc in the gateway module.
        '''
        return isinstance(content, str)

class FaultType(MessageType):
    def isOfType(self, content):
        return isinstance(content, ecu.fault)

class AcknowledgementType(MessageType):
    def isOfType(self, content):
        return isinstance(content, Acknowledgement)
class ListType(MessageType):
    def __init__(self, listItemType:MessageType) -> None:
        self.listItemType =  listItemType
        super().__init__()
    
    def isOfType(self, content):
        if isinstance(content, list):
            for item in content:
                if not self.listItemType.isOfType(item):
                    return False
            
            return True
        else:
            return False
    


class Message:
    def __init__(self, type:MessageType, content) -> None:
        self.type = type
        self.content = content
        pass

    def isValid(self):
        return self.type.isOfType(self.content)
    
    def getContent(self):
        return self.content, self.type, self.isValid()

class GetFaultMessage(Message):
    def __init__(self) -> None:
        self.type = StringType()
        self.content = "ReadFaults"
        pass


class ClearFaultMessage(Message):
    def __init__(self) -> None:
        self.type = StringType()
        self.content = "ClearFaults"
        pass

class Response:
    def __init__(self, sender:ecu.ecu, message:Message) -> None:
        self.sender = sender
        self.message = message
        pass

class Bus:
    def __init__(self) -> None:
        self.ecuList: dict[int, ecu.ecu] = {}
        ecu.Gateway(self, 0, "FCM")
        print(self.ecuList)
        pass
    def mainloop(self):
        for id, ecu in self.ecuList.items():
            ecu.mainloop()
    def Register(self, ecu:ecu.ecu, id:int):
        self.ecuList[id] = ecu
    def sendMessage(self, senderEcu:ecu.ecu, recieverId:int|ecu.ecu, message: Message):
        time.sleep(1)
        recieverEcu:ecu.ecu = None
        if isinstance(recieverId, ecu.ecu):
            recieverEcu = recieverId
        elif isinstance(recieverId, int):
            if recieverId in self.ecuList:
                recieverEcu = self.ecuList[recieverId]
               
                
            else:
                fault = ecu.fault("U1000", True, False)
                self.ecuList[0].throwFault(fault=fault)
                return False
        else:
            return False
        
        print(f"{senderEcu.id} -> {recieverEcu.id} - {message.content}")
        response:Message|None = recieverEcu.recieveMessage(senderEcu, message)
        if isinstance(response, Message):
            print(f"{recieverEcu.id} -> {senderEcu.id} - {response.content}")
            return Response(recieverEcu, response)
        else:
            return None


