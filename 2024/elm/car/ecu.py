import time as _time


def ResetECU(self,ecu,args:str):
    _time.sleep(4)
    return ecu.busId+"51"+args.upper()

class ecu():
    def __init__(self, busId) -> None:
        '''
        Basic class of an ecu, make sublclasses for each ecu in the car
        '''
        self.busId = busId
        self.commandList = {
            "11":command(ResetECU, "ResetECU")
        }

        
        pass
    
    def mainLoop(self, func=None):
        if func != None:
            func(self)

    def runCommand(self, command):
        if len(command) > 2:
            args = command[2:]
            command = command[0:2]
            print(args)
        
        if command in self.commandList:
            print(command)
            if args:
                result = self.commandList[command].run(self, args)
            else:
                result = self.commandList[command].run(self)
            print(result)
            if isinstance(result,str):
                return result
            else:
                return "NO DATA"
        else:
            return "NO DATA"
    
class command():
    def __init__(self, runFunction, label:str="") -> None:
        '''
            Class of a basic command (or service for uds and obd), eg: 22 \n
            runFunction = function ran by command ( executes as runFunction(self, ecu, args) make sure you have all 3 positional arguments even if they arent used) \n
            Label = description of command eg Read data by identifier\n
        '''

        self.func = runFunction
        self.label = label
        pass

    def run(self, ecu:ecu, args:str=""):
        '''
        ecu: Ecu executing the command, \n
        args: Command arguments: EG: 22F190's args are F190 ,the command (service) is 22\n
        '''
        
        return self.func(self,ecu,args)
