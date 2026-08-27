from __future__ import annotations
import package.ui as ui
from package.ecu import ecu
from package.bus import Bus, Message, Response, Acknowledgement, AcknowledgementType

class color():

    def __init__(self, str:str = "red") -> None:
        self.str = str
        pass

    
class colors:
    red = color("red")
    orange = color("orange")
    yellow = color("yellow")
    green = color("green")
class Indicator:

    def __str__(self) -> str:
        return f"{self.label}: {self.getState()}"
    def __init__(self, label, color:color = colors.red) -> None:
        self.label = label
        self.isOn = False
        self.color = color
        pass

    def activate(self):
        self.isOn = True
        pass

    def disable(self):
        self.isOn = False
    
    def getState(self):
        return self.isOn

class IPC(ecu):
    def __init__(self, bus: Bus, id: int, name: str) -> None:
        self.indicators:dict[str, Indicator] = {"ECM":Indicator("CEL"), "FCM":Indicator("BUS")}
        self.ui = ui.UI()
        super().__init__(bus, id, name)
    '''
    Dashboard controll module, shows indicator lights \n
    List of messages: ReadFaults, ClearFaults, ActivateMIL-ECM, DisableMIL-ECM, ActivateMIL-FCM, DisableMIL-FCM
    '''
    def recieveMessage(self, sender: ecu, message: Message):
        a = super().recieveMessage(sender, message)
        if isinstance(a,Response):
            return a
        elif message.isValid():
            if isinstance(message.content, str):
                if message.content.startswith("ActivateMIL-"):
                    split = message.content.split("-")
                    if split[1] in self.indicators:
                        self.indicators[split[1]].activate()
                    return Message(AcknowledgementType(), Acknowledgement())
            

    
    def mainloop(self, *args):
        self.ui.mainLoop(self.indicators)
        for name, val in self.indicators.items():
            print(val)