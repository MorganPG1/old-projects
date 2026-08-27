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

Memory range
0000-4fff = ROM
5000-7fff = RAM
8001-ffff = VRAM (write any value to 0xffff to save the changes to the display)
'''
cpu = None
from emuLib.cpu import Condition, DecodeEncodeType, Instruction, BaseInstruction, r16, r8, n16, n8, memn16, memr16, CPULike, Pop, Push

def incProgramCounter(cpu:CPULike):
    cpu.registers16bit["PC"].set(cpu.registers16bit["PC"].get()+1)
def _LD(instruction:Instruction):
    data2 = instruction.data2.Decode()
    instruction.data1.Encode(data2)
    incProgramCounter(cpu)
    pass
LD = BaseInstruction("LD", _LD) 

def _NOP():
    incProgramCounter(cpu)
    pass
NOP = BaseInstruction("NOP", _NOP  )

def _JP(instruction:Instruction):
    condition = instruction.condition
    data1 = instruction.data1.Decode()
    if condition:
        if condition.IsMet():
            cpu.registers16bit["PC"].set(data1)
    else:
        cpu.registers16bit["PC"].set(data1)

JP = BaseInstruction("JP", _JP)

def _CALL(instruction:Instruction):
    condition = instruction.condition
    data1 = instruction.data1.Decode()
    if condition:
        if condition.IsMet():
            Push(cpu, cpu.registers16bit["SP"], cpu.registers16bit["PC"].get()+1)
            cpu.registers16bit["PC"].set(data1)
    else:
        Push(cpu, cpu.registers16bit["SP"], cpu.registers16bit["PC"].get()+1)
        cpu.registers16bit["PC"].set(data1)

CALL = BaseInstruction("CALL", _CALL)

def _RET(instruction:Instruction):
    regADDR = Pop(cpu, cpu.registers16bit["SP"])
    #print(regADDR)
    cpu.registers16bit["PC"].set(regADDR)

RET = BaseInstruction("RET", _RET)

def _INC(instruction:Instruction):
    og = instruction.data1.Decode()
    #print(instruction, instruction.data1.Decode())
    instruction.data1.Encode(og+1)
    incProgramCounter(cpu)
    
def _DEC(instruction:Instruction):
    og = instruction.data1.Decode()
    instruction.data1.Encode(og-1)
    incProgramCounter(cpu)
INC = BaseInstruction("INC", _INC)
DEC = BaseInstruction("DEC", _DEC)
class NOPInstruction(Instruction):
    def __init__(self, opcode, baseInstruction: BaseInstruction, instructionGroup=None) -> None:
        super().__init__(opcode, baseInstruction, None, None, instructionGroup)
    def run(self):
        _NOP()
def init(self:CPULike):
    global cpu
    cpu = self
    flagReg = cpu.registers["F"]
    pc = self.registers16bit["PC"]
    mm = self.MemoryManager
    a = self.registers["A"]
    b = self.registers["B"]
    c = self.registers["C"]
    d = self.registers["D"]
    ab = self.registers16bit["AB"]
    cd = self.registers16bit["CD"]
    instructionSet = [
        NOPInstruction("0", NOP),
        Instruction("1", LD, r8(a), n8(pc, mm)), #LD a, n8
        Instruction("2", LD, r8(a), r8(b)), #LD a, b
        Instruction("3", LD, r8(a), r8(c)), #LD a, d
        Instruction("4", LD, r8(a), r8(d)), #LD a, d
        Instruction("5", LD, memn16(pc, mm), r8(a)), #LD (n16), a
        Instruction("6", LD, r8(a), memn16(pc, mm)), #LD a, (n16)
        Instruction("7", LD, r8(b), n8(pc, mm)), #LD B, n8
        Instruction("8", LD, r8(b), r8(b)), #LD b, a
        Instruction("9", LD, r8(b), r8(c)), #LD b, b
        Instruction("A", LD, r8(b), r8(d)), #LD b, c
        Instruction("B", LD, r8(b), r8(d)), #LD b, D
        Instruction("C", LD, r8(c), r8(b)), #LD c, a
        Instruction("D", LD, r8(c), r8(c)), #LD c, b
        Instruction("E", LD, r8(c), r8(d)), #LD c, c
        Instruction("F", LD, r8(c), r8(d)), #LD c, D
        Instruction("10", LD, r8(d), r8(b)), #LD d, a
        Instruction("11", LD, r8(d), r8(c)), #LD d, b
        Instruction("12", LD, r8(d), r8(d)), #LD d, c
        Instruction("13", LD, r8(d), r8(d)), #LD d, D
        Instruction("14", LD, memr16(ab, mm), r8(a)), #LD (ab), a
        Instruction("15", LD, r8(a), memr16(ab, mm)), #LD a, (ab)
        Instruction("16", LD, memr16(cd, mm), r8(a)), #LD (cd), a
        Instruction("17", LD, r8(a), memr16(cd, mm)), #LD a, (cd)
        Instruction("18", LD, r16(ab), n16(pc, mm)), #LD ab, n16
        Instruction("19", LD, r16(cd), n16(pc, mm)), #LD ab, n16   
        Instruction("1A", JP, r16(ab)),# JP ab
        Instruction("1B", JP, r16(cd)),# JP cd
        Instruction("1C", JP, n16(pc, mm)), #JP n16
        Instruction("1D", JP, r16(ab), condition=Condition("NZ", flagReg)), #JP nz, ab
        Instruction("1E", JP, r16(cd), condition=Condition("NZ", flagReg)), #JP nz, cd
        Instruction("1F", JP, r16(ab), condition=Condition("Z", flagReg)), #JP z, ab
        Instruction("20", JP, r16(cd), condition=Condition("Z", flagReg)), #JP z, cd
        Instruction("21", CALL, r16(ab)),# JP ab
        Instruction("22", CALL, r16(cd)),# JP cd
        Instruction("23", CALL, n16(pc, mm)), #JP n16
        Instruction("24", CALL, r16(ab), condition=Condition("Z", flagReg)), #JP nz, ab
        Instruction("25", CALL, r16(cd), condition=Condition("Z", flagReg)), #JP nz, cd
        Instruction("26", CALL, r16(ab), condition=Condition("NZ", flagReg)), #JP z, ab
        Instruction("27", CALL, r16(cd), condition=Condition("NZ", flagReg)), #JP z, cd
        Instruction("28", INC, r8(a)),
        Instruction("29", INC, r8(b)),
        Instruction("2A", INC, memr16(cd, mm)),
        Instruction("2B", DEC, r8(a)),
        Instruction("2C", DEC, r8(b)),
        Instruction("2D", DEC, memr16(cd, mm)),
        Instruction("3E", RET, None), #RET
    ]
    return instructionSet


