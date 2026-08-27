class OBDReader():
    def __init__(self):
        '''
        Handle connection to OBD Reader
        '''
        pass
    def clear(self):
        '''
        Clear the output buffer
        '''
        pass
    def send(self, data):
        '''
        Handle sending data to OBD Reader
        '''
        pass
    def read(self) -> str:
        '''
        Handle reading data from OBD Reader
        '''
        pass
class ModuleConnection():
    def __init__(self, reader:OBDReader):
        '''
        Try to connect to the module, if it fails then self.connected is false.
        '''
        self.reader = reader
        self.connected = False
        pass
    def mainloop(self):
        '''
        Keep the communication active
        '''
        pass
    def ReadFaults(self) -> list[str]:
        '''
        Read the faults for the module
        '''
        pass
    def ClearFaults(self) -> bool:
        '''
        Clear the faults for the module
        '''
        pass
class Module():
    def __init__(self):
        self.name:str = None
        pass
    def connect(self, reader:OBDReader) -> ModuleConnection:
        pass
class Car():
    def __init__(self, reader:OBDReader):
        self.modules:list[Module] = []
        self.reader = reader
        pass
    def connect(self):
        '''
        Handle car connection, this should just initialise values and do nothing else\n
        All other comms should be done through modules
        '''
        pass
    def clearAllModules(self):
        '''
        Clear all module faults.
        '''
        for module in self.modules:
            connection = module.connect(self.reader) #Connect to the module
            connection.ClearFaults() #Clear the faults

    def readAllModules(self):
        '''
        Read all module faults.
        '''
        dtcList = {}
        for module in self.modules:
            connection = module.connect(self.reader)
            dtcList[module.name] = [] #Initialise the module in the dtc list
            dtcList[module.name] = connection.ReadFaults()

        return dtcList
        pass
