import time as __time
from emuLib.memory import MemoryManager as __MemoryManager

class UnknownOpcodeError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
class Register():
    def __init__(self, name=None) -> None:
        self.value = 0
        self.name = name
        pass

    def set(self, value):
        if type(value) is int:
            if value <= 0xff:
                self.value = value
            else:
                raise OverflowError(f"Value {value} is too big to fit in 8 bit register")
        else:
            raise TypeError("Value is not int")
    def get(self):
        return self.value

class Register16Bit(Register):
    '''
    16 bit register, uses the input registers to create 1 16 bit register.
    '''
    
    def __init__(self, reg1:Register, reg2:Register, name=None) -> None:
        self.reg1 = reg1
        self.reg2 = reg2
        self.name = name
        pass
    def set(self, value):
        if type(value) is int:
            if value <= 0xffff:
                #print(value, hex(value))
                hex0 = hex(value)[2:].rjust(4,"0")

                hex1 = hex0[0:2]
                hex2 = hex0[2:4]
                #if self.name == "SP":
                    #print("set",hex1, hex2)
                self.reg1.set(int(hex1, 16))
                self.reg2.set(int(hex2, 16))
            else:
                raise OverflowError("Value is too big to fit in 16 bit register")
        else:
            raise TypeError("Value is not int")
    
    def get(self):
        val1 = self.reg1.get()
        val2 = self.reg2.get()

        hex1 = hex(val1)[2:].rjust(2,"0")
        hex2 = hex(val2)[2:].rjust(2,"0")
        #if self.name == "SP":
            #print("get",hex1, hex2)
        hex0 = hex1+hex2

        return int(hex0, 16)

class FlagRegister(Register):
    def __init__(self, zeroVal=0, carryVal=0) -> None:
        '''
        Initialises a flag register\n
        carryVal and zeroVal are the values that are added and set to the register
        '''
        super().__init__()
        self.zero = False
        self.carry = False
        self.zeroVal = zeroVal
        self.carryValue = carryVal
    def setFlags(self, zero, carry):
        value = 0
        if zero:
            value += self.zeroVal
            self.zero = True
        else:
            self.zero = False
        if carry:
            value += self.carryValue
            self.carry = True
        else:
            self.carry = False
        self.value = value
class DecodeEncodeType():
    '''
    Base class for all types of data decoding and encoding from instructions.
    '''
    
    def __init__(self) -> None:
        pass

    def Decode(self):
        pass
    def Encode(self, value):
        pass

class r16(DecodeEncodeType):
    '''
    Decode and Encode data from and to a 16 bit register
    '''
    def __init__(self, register) -> None:
        
        self.register:Register = register
        pass

    def __str__(self) -> str:
        if self.register.name:
            return self.register.name
        else:
            return "r16"
    def Decode(self):
        return self.register.get()
    
    def Encode(self,value):
        #print(value)
        self.register.set(value)


class r8(DecodeEncodeType):
    '''
    Decode and Encode data from and to a 8 bit register
    '''
    def __init__(self, register) -> None:
        
        self.register:Register = register
        pass

    def __str__(self) -> str:
        if self.register.name:
            return self.register.name
        else:
            return "r8"
    def Decode(self):
        return self.register.get()
    
    def Encode(self,value):
        self.register.set(value)


class n8(DecodeEncodeType):
    '''
    Decode and Encode data from a 8 bit number
    '''
    def __init__(self, programCounter:Register, memoryManager) -> None:
        
        self.memoryManager = memoryManager
        self.programCounter = programCounter
        pass

    def __str__(self) -> str:
        pc = self.programCounter
        mm = self.memoryManager

        #pc.set(pc.get()+1)
        data = mm.Read(pc.get()+1)
        return hex(data)[2:].ljust(2, "0")
    def Decode(self):
        pc = self.programCounter
        mm = self.memoryManager

        pc.set(pc.get()+1)
        data = mm.Read(pc.get())
        return data
    
    def Encode(self,value):
        raise NotImplementedError("Attempt to encode a n8 value.")
class n16(DecodeEncodeType):
    '''
    Decode and Encode data from a 16 bit number
    '''
    def __init__(self, programCounter:Register, memoryManager) -> None:
        
        self.memoryManager = memoryManager
        self.programCounter = programCounter
        pass

    def __str__(self) -> str:
        pc = self.programCounter
        mm = self.memoryManager
        low = hex(mm.Read(pc.get()+1))[2:].rjust(2,"0")
        high = hex(mm.Read(pc.get()+2))[2:].rjust(2,"0")
        data = int(high+low,16)
        return hex(data)[2:]
    def Decode(self):
        pc = self.programCounter
        mm = self.memoryManager

        pc.set(pc.get()+1)
        low = hex(mm.Read(pc.get()))[2:].rjust(2,"0")
        pc.set(pc.get()+1)
        high = hex(mm.Read(pc.get()))[2:].rjust(2,"0")
        #print(low)
        #print(high)
        data = int(high+low,16)
        #print("DC R16 RET",data)
        return data
    
    def Encode(self,value):
        raise NotImplementedError("Attempt to encode a n8 value.")
class memn16(DecodeEncodeType):
    '''
    Decode and Encode data from a 16 bit memory address determnined by a 16 bit number
    '''
    def __init__(self, programCounter:Register, memoryManager) -> None:
        
        self.memoryManager = memoryManager
        self.programCounter = programCounter
        pass

    def __str__(self) -> str:
        return "memn16"
    def Decode(self):
        pc = self.programCounter
        mm = self.memoryManager

        pc.set(pc.get()+1)
        low = hex(mm.Read(pc.get()))[2:]
        pc.set(pc.get()+1)
        high = hex(mm.Read(pc.get()))[2:]
        data = mm.Read(int(high+low,16))
        
        return data
    
    def Encode(self,value):
        pc = self.programCounter
        mm = self.memoryManager

        pc.set(pc.get()+1)
        low = hex(mm.Read(pc.get()))[2:]
        pc.set(pc.get()+1)
        high = hex(mm.Read(pc.get()))[2:]
        mm.Write(int(high+low,16), value)
    

class memr16(DecodeEncodeType):
    '''
    Decode and Encode data from and to a memory address determined by a 16 bit register
    '''
    def __init__(self, register, memoryManager) -> None:
        
        self.register = register
        self.memoryManager = memoryManager
        pass

    def __str__(self) -> str:
        if self.register.name:
            return f"{self.register.name}({hex(self.register.get())[2:]})"
        else:
            return f"memr16({hex(self.register.get())[2:]})"
    def Decode(self):
        memory = self.register.get()
        value = self.memoryManager.Read(memory)
        return value
    def Encode(self,value):
        memory = self.register.get()
        self.memoryManager.Write(memory,value)





class Condition():
    def __init__(self, type, flagRegister) -> None:
        '''
        types:
        Z - zero
        NZ - not zero
        C - carry register
        NC - not carry
        '''
        typeList = [
            "Z",
            "NZ",
            "C",
            "NC"
        ]
        if type in typeList:
            self.type = type
            self.flagRegister = flagRegister
        else:
            raise Exception("Unknown condition: "+type)
        pass

    def IsMet(self):
        if self.flagRegister.zero and self.type == "Z":
            return True
        elif not self.flagRegister.zero and self.type == "NZ":
            return True
        elif self.flagRegister.carry and self.type == "C":
            return True
        elif not self.flagRegister.carry and self.type == "NC":
            return True
        else:
            return False
        
class BaseInstruction():
    def __init__(self, name, func) -> None:
        '''
        Base instruction, eg LD a, b <- base instruction is LD, Instruction is LD a,b
        '''
        self.name = name
        self.func = func
        return None
    def run(self, instruction):
        self.func(instruction)

class Instruction():
    def __init__(self, opcode, baseInstruction:BaseInstruction, data1:DecodeEncodeType, data2:DecodeEncodeType=None, condition:Condition=None, instructionGroup=None) -> None:
        '''

        opcode: The opcode of the instruction,\n
        baseInstruction: the base instruction of the instruction \n
        data1: the first value in the instruction \n
        '''
        self.opcode = opcode
        self.baseInstruction:BaseInstruction = baseInstruction
        self.data1 = data1
        self.data2 = data2
        self.condition = condition
        self.instructionGroup = instructionGroup
        if instructionGroup:
            self.instructionGroup.AddInstruction(self)
            pass
    
    def __str__(self) -> str:
        if self.data2:
            return self.baseInstruction.name +", "+str(self.data1)+", "+str(self.data2)
        elif self.data1:
            return self.baseInstruction.name+", "+str(self.data1)
        else:
            return self.baseInstruction.name
    def run(self):
        self.baseInstruction.run(self)

class InstructionGroup():
    def __init__(self) -> None:
        self.instructionTable = {}
        pass

    def AddInstruction(self, instruction):
        self.instructionTable[instruction.opcode.lower()] = instruction
    
    def GetInstruction(self, opcode) -> Instruction:
        '''
        Gets a instruction from an opcode
        '''
        if opcode.lower() in self.instructionTable:
            return self.instructionTable[opcode.lower()]
        else:
            return None
        



class CPULike():
    '''
    Cpu like object,
    Reference for any CPU related functions
    '''

    def __init__(self, memorymanager) -> None:
        self.registers = {

        }
        self.registers16bit = {

        }
        self.MemoryManager:__MemoryManager = memorymanager
        pass
    def Step(self):
        __time.sleep(0.01)
        
    def Execute(self, instruction):
        pass
        
def Push(self:CPULike, stackPointer:Register16Bit, Value:int):
    hexVal = hex(Value)[2:].rjust(4,"0")
    high = hexVal[0:2]
    low = hexVal[2:4]
    #print(high)
    #print(low)
    #print(hexVal)
    stackPointer.set(stackPointer.get() - 1)
    mem = stackPointer.get()

    self.MemoryManager.Write(mem, int(high, 16))

    stackPointer.set(stackPointer.get() - 1)
    mem = stackPointer.get()

    self.MemoryManager.Write(mem, int(low,16))

def Pop(self:CPULike, stackPointer:Register16Bit):
    val1 = self.MemoryManager.Read(stackPointer.get())
    stackPointer.set(stackPointer.get()+1)
    val2 = self.MemoryManager.Read(stackPointer.get())
    stackPointer.set(stackPointer.get()+1)
    
    high = hex(val2)[2:]
    low = hex(val1)[2:]

    
    return int(high+low, 16)
    
    
     

