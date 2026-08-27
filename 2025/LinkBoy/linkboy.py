from pyboy import PyBoy
import logging
import time
l:logging.Logger = None
def setBit(byte:int, bit:int):
    Shifted = 0b1 << bit
    result = byte | Shifted
    return result
def clearBit(byte:int, bit:int):
    Shifted = ~(0b1 << bit)
    result = byte & Shifted
    return result
def getBit(byte:int, bit:int):
    Shifted = 0b1 << bit
    result = byte & Shifted
    if result != 0:
        result = 1
    return result

class LinkDevice:
    def __init__(self):
        self.link = None
        self.SB = 0 #Serial transfer data register
        self.SC = 0 #Serial transfer control register
        pass
    def RecieveBit(self,bit):
        
        self.SB <<= 1 #Shift bit over 1
        self.SB = clearBit(self.SB,8)
        if bit == 1:
            self.SB = setBit(self.SB, 0) #Clear or set bit depending on incoming bit.
        else:
            self.SB = clearBit(self.SB, 0)
        l.info(f"{self}: {bit} RECIEVED, new sb: {bin(self.SB)}")
        pass
    def RecievedFullByte(self):
        self.SC = clearBit(self.SC, 7) #Clear bit 7 to indicate finished transfer
        l.info("Device %s recieved %s", self, self.SB)
        pass
    def TransferredFullByte(self):
        self.SC = clearBit(self.SC, 7) #Clear bit 7 to indicate finished transfer
        print(f"{self}:Transferred full byte! {bin(self.SB)} / {self.SB}")
        pass
    def step(self):
        pass
class Transfer:
    def __init__(self, byte, slave:LinkDevice, master:LinkDevice):
        '''
        A data tranfer from one LinkDevice to another.\n
        Should only be made in the Link object.
        '''
        self.buffer = []
        self.finished = False
        self.slave = slave
        self.master = master
        for i in range(0,7): #Iterate through all bits and add them to the buffer
            self.buffer.append(
                getBit(byte, i)
            )
        pass
    def step(self):
        '''
        Send the next bit.
        '''
        
        if len(self.buffer) == 0 and not self.finished: #If the byte has been transferred, but the other device hasnt been notified
            self.slave.RecievedFullByte() #Notify the slave device the transfer has completed
            self.master.TransferredFullByte()
            self.finished = True
        elif not self.finished: #If transfer not done, send the next bit
            bit = self.buffer.pop(-1)
            l.info(f"{self.master}: SENDING BIT {bit}")
            self.slave.RecieveBit(bit)
class Link:
    def __init__(self, Dev1:LinkDevice, Dev2:LinkDevice):
        '''
        A connection between 2 LinkDevices in which data can be Transferred.
        '''
        Dev1.link = self
        Dev2.link = self
        self.devices:list[LinkDevice] = [Dev1, Dev2]
        self.transfers:list[Transfer] = []
        pass
    def step(self):
        '''
        Step each transfer and device forward.
        '''
        for transfer in self.transfers:
            transfer.step()
            if transfer.finished:
                self.transfers.remove(transfer)
        for device in self.devices:
            device.step()
        time.sleep(0.01)
    def SendByte(self,startingDevice, byte):
        '''
        Send a byte to the other device in the link.
        '''
        
        for device in self.devices:
            if device != startingDevice:
                l.info("Device %s sends %s to %s", startingDevice, byte, device)
                #print(f"DEVICE SENDS {byte} to {device}")
                self.transfers.append(
                    Transfer(byte, device, startingDevice)
                )
    

class LinkBoy(PyBoy, LinkDevice):
    def __init__(self, logger:logging.Logger, gamerom, *, window="SDL2", scale=3, symbols=None, bootrom=None, sound_volume=100, sound_emulated=True, sound_sample_rate=None, cgb=None, gameshark=None, no_input=False, log_level="WARNING", color_palette=(0xFFFFFF, 0x999999, 0x555555, 0x000000), cgb_color_palette=((0xFFFFFF, 0x7BFF31, 0x0063C5, 0x000000),(0xFFFFFF, 0xFF8484, 0x943A3A, 0x000000),(0xFFFFFF, 0xFF8484, 0x943A3A, 0x000000),), **kwargs):
        self.link:Link = None
        global l
        
        logging.basicConfig(filename='myapp.log', level=logging.INFO)
        l = logger
        l.info("logger active!")
        self.transferInProgress = False
        super().__init__(gamerom, window=window, scale=scale, symbols=symbols, bootrom=bootrom, sound_volume=sound_volume, sound_emulated=sound_emulated, sound_sample_rate=sound_sample_rate, cgb=cgb, gameshark=gameshark, no_input=no_input, log_level=log_level, color_palette=color_palette, cgb_color_palette=cgb_color_palette, **kwargs)
    
    def RecieveBit(self, bit):
        SB = self.memory[0xFF01]
        SB <<=1 #Shift bit over 1
        SB = clearBit(SB,8)
        if bit == 1:
            SB = setBit(self.memory[0xFF01], 0) #Clear or set bit depending on incoming bit.
        else:
            SB = clearBit(self.memory[0xFF01], 0)
        pass
        self.memory[0xFF01] = SB
        self.memory[0xFF02] = setBit(self.memory[0xFF02], 7)
    def RecievedFullByte(self):
        l.info("Device %s recieved %s", self, self.memory[0xFF01])
        #self.memory[0xFF02] = clearBit(self.memory[0xFF02], 7)
        #self.mb.cpu.set_interrupt_flag(0b00001000)
    def TransferredFullByte(self):
        self.memory[0xFF02] = clearBit(self.memory[0xFF02], 7)
        self.mb.cpu.set_interrupt_flag(0b00001000)
        self.transferInProgress = False
    def step(self):
        output =  super().tick()
        SC = self.memory[0xFF02]
        if getBit(SC,7) == 1 and self.link and not self.transferInProgress:
            self.link.SendByte(self, self.memory[0xFF01])
            self.transferInProgress = True
        return output