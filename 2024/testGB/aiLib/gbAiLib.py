from pyboy import PyBoy
'''
Makes AI training easier\n

Goals: \n
    reset() function\n
    easy auto load of save states\n
    define memory variables (addVariable() readVariable() and Variable class. Variables have a memory value to read from)\n
    easy read and write to ram functions\n
'''
class AIBoy():
    '''
    Makes AI training easier\n

    Goals: \n
        reset() function\n
        easy auto load of save states\n
        define memory variables (addVariable() readVariable() and Variable. Variables have a memory value to read from\n
        easy read and write to ram functions\n
        tick and second counter (not irl seconds, ingame seconds)\n
    '''

    def __init__(self, rom:str="rom.gb", state:str=None, speedLimiter:bool=False) -> None:
        '''
        Load a rom and initialise PyBoy instance\n
        rom: Path to rom file\n
        state: save state to load on reset and on start
        '''
        self.rom = rom
        self.speedLimiter = speedLimiter
        self.pyboy = PyBoy(rom)
        self.state = state
        self.ticks = 0
        self.seconds = 0
        self.memory = self.pyboy.memory
        if state:
            #Load save state
            self.loadState()
        if not speedLimiter:
            self.pyboy.set_emulation_speed(0)
        pass
    def loadState(self):
        stateFile = open(self.state,"rb")
        self.pyboy.load_state(stateFile)
    def updateTimer(self):
        self.ticks += 1
        if self.ticks % 60 == 0:
            self.seconds = self.ticks/60
    def step(self, count=1, render=True):
        '''
        Redirect to PyBoy.tick()
        '''
        self.updateTimer()
        return self.pyboy.tick(count,render)
    def stop(self):
        '''
        Redirect to PyBoy.stop()
        '''
        self.pyboy.stop()
    def tick(self, count=1, render=True):
        '''
        Redirect to PyBoy.tick()
        '''
        self.updateTimer()
        return self.pyboy.tick(count, render)
    def reset(self):
        '''
        Stops and then restarts the PyBoy instance\n
        If save state is defined then restart from state
        '''

        self.ticks = 0
        self.seconds = 0
        self.loadState()
        if not self.speedLimiter:
            self.pyboy.set_emulation_speed(0)
        pass
    def readMem(self, addr):
        '''
        Read from location in memory space
        '''
        if isinstance(addr, Variable):
            return self.memory[addr.addr]
        else:
            return self.memory[addr]
    def writeMem(self,addr, value):
        '''
        Write to location in memory space
        '''
        if isinstance(addr, Variable):
            self.memory[addr.addr] = value
        else:
            self.memory[addr] = value    
    
class Variable():
    def __init__(self, addr:int, aiBoy:AIBoy) -> None:
        self.addr = addr
        self.aiBoy = aiBoy
        pass
    def getVal(self):
        return self.aiBoy.memory[self.addr]
    def setVal(self, value):
        self.aiBoy.memory[self.addr] = value