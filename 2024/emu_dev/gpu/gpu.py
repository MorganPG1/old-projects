from emuLib.memory import MemoryLocation

class VRAM(MemoryLocation):
    def __init__(self, start, end, MemoryManager) -> None:
        self.start = start
        self.end = end
        self.__memory = [0]*(end-start)
        self.MemoryManager = MemoryManager
        MemoryManager.AssignMemoryLocation(self)
        pass
    def WriteByte(self, index, value):
        if index == 0x7fff:
            vramBuffer = []
            hadFirstChar = False
            for byte in self.__memory:
                    if byte == 0 and hadFirstChar:
                        break
                    else:
                        vramBuffer.append(byte)
                        hadFirstChar = True 
                    #print("B:",byte)

            mainStr = ""
            for character in vramBuffer:
                #print(character)
                char= chr(character)
                #print(char)
                mainStr += char
            print(mainStr)
        else:
            #print(f"WRITE {hex(index)}: {hex(value)}")
            self.__memory[index] = value
    def ReadByte(self, index):
        return self.__memory[index]