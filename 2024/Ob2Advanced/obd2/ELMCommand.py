
from . import OBDMain
from .OBDMain import dprint

class ELMReturnType(OBDMain.ReturnType):
    def decode(self, value:str) -> OBDMain.CommandReturn:
        if value.startswith("ok"):
            return OBDMain.CommandReturn(True, "ELMCommand")
        else:
            return OBDMain.CommandReturn(False, "ELMCommand")

class ELMVoltage(OBDMain.ReturnType):
    def decode(self, value:str) -> OBDMain.CommandReturn:

        value = value.replace("\r", "")
        value =  value.replace("\n", "")
        value = value.removesuffix(">")
        value = value.upper()
        dprint(value)
        
        if value.endswith("V"):
            value = value.removesuffix("V")
            return OBDMain.CommandReturn(float(value), "Voltage", value+"V")
        else:

            return OBDMain.CommandReturn(0, "VoltageFail", "?V")


class ELMCommand(OBDMain.Command):
    def __init__(self, command: str, returnType: OBDMain.ReturnType=ELMReturnType, name: str = "", description: str = "", space:bool=True) -> None:
        command = "AT "+command.upper()
        super().__init__( command, returnType, name, description, space=space) 
    


