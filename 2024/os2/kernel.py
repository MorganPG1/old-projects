import kernelClasses

class OutOfRAMBounds(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
class UnusedMemory():
    def __init__(self) -> None:
        pass
class RAM():
    def __init__(self, length) -> None:
        self.length = length
        self.list = [UnusedMemory()] * length
        pass
    def read(self, pos):
        if pos > self.length-1:
            raise OutOfRAMBounds("Memory position requested for read is greater than the size of ram.")
        else:
            return self.list[pos]
 
    def write(self,pos, data):
        if pos > self.length-1:
            raise OutOfRAMBounds("Memory position requested for write is greater than the size of ram.")
        else:

            self.list[pos]= data
class HardwareList():
    def __init__(self) -> None:
        self.hwList:list[kernelClasses.Hardware] = []
        pass
    def __iter__(self):
        return iter(self.hwList)
    def register(self,value, name):
        self.hwList.append(kernelClasses.Hardware(name, value))
'''
for count in range(0,1000000000):
    print(count)
    try:
        print("Memory before write is:",ram.read(count))
        ram.write(count, 1)
        print("Read back memory after write, value is:",ram.read(count))
    except OutOfRAMBounds:
        print("Error thrown. Length is",count)
        break
'''
class Logger():
    def __init__(self) -> None:
        pass
    def log(self, process:str, text):
        print(f"[{process}] [LOG] {text}")
class Variable():
    def __init__(self, ram:RAM, value) -> None:
        self.ram = ram,
        self.ramPos = None
        for count in range(0,ram.length):
            valueOfRam = ram.read(count)
            if isinstance(valueOfRam, UnusedMemory):
                self.ramPos = count
                ram.write(count, value)
                break
        if self.ramPos == None:
            raise OutOfRAMBounds("No more ram space for variable to fit in")
        pass
    def get(self):
        return ram.read(self.ramPos)
    def set(self, value):
        ram.write(self.ramPos, value)
    def delete(self):
        ram.write(self.ramPos, UnusedMemory())
'''
a = Variable(ram,"Hello")
b = Variable(ram,"world!")

for count in range(0,200):
    count2 = Variable(ram, count)
    print(count2.get())
    count2.delete()
print(a.get(), b.get())
'''
class Kernel():
    def __init__(self, ram:RAM, hw:HardwareList) -> None:
        self.ram = ram
        self.hwInit = Variable(ram, False)
        self.logger = Logger()
        self.ticks = Variable(ram, 0)
        self.hasRanRamTest = Variable(ram,False)
        self.hasPassedRamTest = Variable(ram,True)
        pass
    def ramtest(self):
        self.logger.log("KernelMain-RamTest", f"ram size is {self.ram.length} objects.")
        self.logger.log("KernelMain-RamTest", "Beginning ram test")
        for count in range(0,self.ram.length):
            if not isinstance(self.ram.read(count), UnusedMemory):
                self.logger.log("KernelMain-RamTest", f"Skipping memory at position {count}, data is stored: {self.ram.read(count)}")
            else:
                self.ram.write(count, 255)
                if self.ram.read(count) == 255:
                    #self.logger.log("KernelMain-RamTest", f"RAM AT {count} PASSED TEST")
                    self.ram.write(count, UnusedMemory())
                    pass
                else:
                    self.logger.log("KernelMain-RamTest",f"RAM AT {count} FAILED!!!")
                    self.hasPassedRamTest.set(ram,False)
                    break
        self.hasRanRamTest.set(True) 
    def mainloop(self):
        self.ticks.set(self.ticks.get()+1)
        if self.ticks.get() == 1:
            self.logger.log("KernelMain", "Kernel initialising")
        if not self.hasRanRamTest.get():
            self.logger.log("KernelMain", "Running ram test.")
            self.ramtest()
        else:

            for hardware in hw:

                    
                if isinstance(hardware.getValue(), kernelClasses.GPUClass):
                        if not self.hwInit.get():
                            self.logger.log("Kernel-HW", "Initialising GPU...")
                            hardware.getValue().init(18)
                            hardware.getValue().PrintText("PGos Kernel")
                            hardware.getValue().PrintText(f"Ram is {self.ram.length} objects.")
                            ramSpaceUsed = 0
                            for data in self.ram.list:
                                if not isinstance(data, UnusedMemory):
                                    print(data)
                                    print("a")
                                    ramSpaceUsed += 1
                                else:
                                    break
                            hardware.getValue().PrintText(f"{self.ram.length-ramSpaceUsed} objects free")
                        hardware.getValue().mainloop()
                self.hwInit.set(True)

            
    def createVariable(self, value) -> Variable:
        return Variable(self.ram, value)
    
import gpu
ram = RAM(1024)
hw = HardwareList()
hw.register(gpu.GPU(400,300), "GPU")
k = Kernel(ram, HardwareList())
while True:
    k.mainloop()