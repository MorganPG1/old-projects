import cpu.cpu
from emuLib.memory import *
from gpu.gpu import VRAM
from emuLib.cpu import InstructionGroup

InstrGroup = InstructionGroup()
MemoryMan = MemoryManager()

def LoadRom(rom):
    filedata = open(rom, "br")
    data = filedata.read()
    return data

romData = LoadRom("test2.rom")
print(romData)
ROM = ROMMemoryLocation(0, 0x4fff, romData, MemoryMan)
RAM  = MemoryLocation(0x5000, 0x7fff, MemoryMan)
VidRAM = VRAM(0x8000, 0xffff, MemoryMan)
#8000-ffff = vram
CPU = cpu.cpu.CPU(MemoryMan, InstrGroup)

CPU.Start()