from car.ecu import ecu
class bus():

    def __init__(self, ecuList:dict = {}) -> None:
        self.ecuList = ecuList
        pass

    def addEcu(self, ecutoadd:ecu):
        if isinstance(ecutoadd, ecu):
            self.ecuList.append(ecu)
        else:
            raise(TypeError("Type not of class or subclass of ecu."))

    def runCommand(self, command:str,ecuId:str="7E0"):
        
        if ecuId in self.ecuList:
            ecuClass:ecu = self.ecuList[ecuId]
            result = ecuClass.runCommand(command)
            return result
        else:
            return "NO DATA"
        
    def mainLoop(self):
        for id, val in self.ecuList.items():
            val.mainLoop()




    