



class MemoryLocation():
    '''
    Location in memory, ReadByte() and WriteByte() should go through MemoryManager, not the memorylocation
    '''
    def __init__(self, start, end, MemoryManager) -> None:
        '''
        Location in memory, ReadByte() and WriteByte() should go through MemoryManager, not the memorylocation
        '''
        self.start = start
        self.end = end
        self.__memory = [0]*(end-start)
        self.MemoryManager = MemoryManager
        MemoryManager.AssignMemoryLocation(self)
        pass

    def ReadByte(self, index):
        #print("IND",index)
        return self.__memory[index]
    
    def WriteByte(self, index, value):
        if type(value) is not int:
            raise TypeError("value is not int, value is "+str(type(value)))
        self.__memory[index] = value

class MemoryManager():
    '''
    Manages all memory locations, all reads and writes go through this \n
    Similar to a bus
    '''

    def __init__(self) -> None:
        '''
        Manages all memory locations, all reads and writes go through this \n
        Similar to a bus
        '''
        self.memoryLocations = []
        pass

    def writeToRom(self, addr, value):
        print(f"WRITE TO ROM AT {hex(addr)} with value {hex(value)}")
        '''
        Change this function in cases such as gameboy emulators, where writing to certain locations in rom changes settings.
        '''
        pass

    def InMemoryLocation(self, index, memoryLocation:MemoryLocation):
        '''
        Returns false if the index is not in the memory location\n
        Returns the index within the memory location if it is inside the memory location
        '''

        if memoryLocation.start <= index and memoryLocation.end >= index:
            if memoryLocation.start == 0:
                return index, True
            else:
                return index-memoryLocation.start, False
        else:

            return False, False
    def AssignMemoryLocation(self, memoryLocation:MemoryLocation):
        self.memoryLocations.append(memoryLocation)
    
    def Read(self, index):
        '''
        Write data from a point in the memory map
        '''
        data = None
        for memoryLocation in self.memoryLocations:
            pos, ifZero = self.InMemoryLocation(index, memoryLocation)

            if pos or ifZero:
                data = memoryLocation.ReadByte(pos)
                #print(f"READ FROM {hex(index)[2:].rjust(4, "0")} RETURN: {data}")
        if not data:

            return 0
        else:
            return data
    def Write(self, index, value):
        '''
        Write data to a point in the memory map
        '''
        for memoryLocation in self.memoryLocations:
            pos, ifZero = self.InMemoryLocation(index, memoryLocation)
            if pos != False:
                #print(f"WRITE TO {hex(index)[2:].rjust(4, "0")}: {hex(value)}")
                if isinstance(memoryLocation, ROMMemoryLocation):
                    
                    self.writeToRom(pos, value)
                else:
                    memoryLocation.WriteByte(pos, value)
            
      
class ROMMemoryLocation(MemoryLocation):
    def __init__(self, start:int, end:int, data:bytes, MemoryManager:MemoryManager) -> None:
        '''
        A memory location used for the games ROM,\n
        Only supports reading.
        '''
        
        self.start = start
        self.end = end
        self.MemoryManager = MemoryManager.AssignMemoryLocation(self)
        self.data = data
    
    def ReadByte(self, index):
        #print(index)
        return self.data[index]
    
    def WriteByte(self, index, value):
        pass


