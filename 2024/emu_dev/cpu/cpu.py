# 5 8 bit registers a -> d and f for flags
# 4 16 bit registers, ab, cd, pc (program counter), sp (stack pointer)

'''
Opcodes:
nop = 0x00
ld a, n8 = 0x01
ld a, b = 0x02
ld a, c = 0x03
ld a, d = 0x04
ld (n16), a = 0x05
ld a,(n16) = 0x06
ld b, n8 = 0x07
ld b,a = 0x08
ld b,b = 0x09
ld b,c = 0x0A
ld b,d = 0x0B
ld c, a = 0x0C
ld c, b = 0x0D
ld c, c = 0x0E
ld c, d = 0x0F
ld d, a = 0x10
ld d, b = 0x11
ld d,c = 0x12
ld d,d = 0x13
ld (ab), a = 0x14
ld a, (ab) = 0x15
ld (cd), a = 0x16
ld a, (cd) = 0x17
ld ab, n16 = 0x18
ld cd, n16 = 0x19

22 ld instructions

jp ab = 0x1A
jp cd = 0x1B
jp n16 = 0x1C
jp nz, ab = 0x1D - jump if zero flag not set
jp nz, cd = 0x1E
jp z, ab = 0x1F - jump if zero flag set
jp z, cd = 0x20

call ab = 0x21
call cd = 0x22
call n16 = 0x23
call z ab = 0x24
call z cd = 0x25
call nz ab = 0x26
call nz cd = 0x27

inc a = 0x28
inc b = 0x29
inc (cd) = 0x2A

dec a = 0x2B
dec b = 0x2C
dec (cd) = 0x2D

add a,a = 0x2E
add a,b = 0x2F
add a,c = 0x30
add a,d = 0x31

sub a,a = 0x32
sub a,b = 0x33
sub a,c = 0x34
sub a,d = 0x35

push a = 0x36
push b = 0x37
push c = 0x38
push d = 0x39

pop a = 0x3A
pop b = 0x3B
pop c = 0x3C
pop d = 0x3D

ret = 0x3E
62 instructions

'''
from cpu.instructionSet import init
from emuLib.cpu import *
from emuLib.memory import *
import time
class CPU():
    def __init__(self, memoryManager:MemoryManager, instructionGroup:InstructionGroup, debug:bool=False) -> None:
        self.instructionGrp = instructionGroup
        self.debug = debug
        self.MemoryManager =memoryManager
        self.registers = {
            "A": Register("A"),
            "B": Register("B"),
            "C": Register("C"),
            "D": Register("D"),
            "F": FlagRegister(),
        }
        self.registers16bit = {
            "AB": Register16Bit(self.registers["A"], self.registers["B"],"AB"),
            "CD": Register16Bit(self.registers["C"], self.registers["D"],"CD"),
            "SP": Register16Bit(Register(), Register(),"SP"),
            "PC" : Register16Bit(Register(), Register(),"PC")
        }

        self.instructionSet = init(self)
        for instr in self.instructionSet:
            self.instructionGrp.AddInstruction(instruction=instr)
    def Step(self):
        time.sleep(0.001)

    def Execute(self, instruction):
        instruction2 = self.instructionGrp.GetInstruction(instruction)
        if instruction2:
            if self.debug:
                print(hex(self.registers16bit["PC"].get())[2:].rjust(4,"0")+":",instruction2)
            instruction2.run()
        else:
            raise UnknownOpcodeError("UNKNOWN OPCODE: "+instruction)
        
    def MainLoop(self):
        while self.running:
            pc = self.registers16bit["PC"]
            mm = self.MemoryManager
            

            instruction = hex(mm.Read(pc.get()))[2:]
            self.Execute(instruction)

            #pc.set(pc.get()+0x1)
            self.Step()
    def Start(self):
        self.running = True
        self.registers16bit["SP"].set(0x7fff)
        self.MainLoop()
    def Stop(self):
        self.running = False
        


