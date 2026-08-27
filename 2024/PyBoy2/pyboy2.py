
#TO DO
#When transfer finishes set bit 3 in interrupt register (FF0F)
#Shift data in from the right and out from the left in FF01

#Useful resources
#1 - https://gbdev.io/pandocs/Interrupts.html
#2 - https://gbdev.io/pandocs/Serial_Data_Transfer_(Link_Cable).html

#low = w
from pyboy import PyBoy
import keyboard
from pyboy.pyboy import defaults
from threading import Thread
def set_bit(value, bit):
    return value | (1<<7-bit)

def clear_bit(value, bit):
    return value & ~(1<<7-bit)
def get_bit(byte, bit):
    return (byte >> bit) & 1
def shift_in_bit(byte, new_bit):
    # Read the most significant bit (bit that will be shifted out)
    shifted_out_bit = (byte & 0b10000000) >> 7
    
    # Shift the byte left by 1 and insert the new bit
    byte = ((byte << 1) & 0xFF) | (new_bit & 0b1)
    
    return byte, shifted_out_bit

#print(PyBoy("pokemon.gb").mb)


class LinkCapableDevice():
    def __init__(self) -> None:
        self.isMaster = False
        self.isTransmitting = False
        self.bitsLeft = 0
        pass
    def tick(self):
        pass
    def clock_write(self,link):
        pass
    def clock_read(self, bit:int, link):
        pass
class Link():
    def __init__(self) -> None:
        self.devices:list[LinkCapableDevice] = []
        self.data = 0
        self.lastSender = None
        pass
    def register(self, device:LinkCapableDevice):
        self.devices.append(device)
    def send(self,sender:LinkCapableDevice,bit:int):
        
        for device in self.devices:
            if device == sender:
                print(f"DATA {bit} TRANSMITTED BY {device}")
            if device != sender:
                device.clock_read(bit,self)
                device.clock_write(self)
    def tick(self):
        '''
        for device in self.devices:
            if device.isMaster:
                self.data = device.clock_write(self)
                self.lastSender = device
                if self.data == None:
                    self.data = 0
                    self.lastSender = None

                if self.lastSender != device and self.lastSender != None:
                    print(f"DATA {self.data} transmitted")
                    device.clock_read(self.data, self)
            else:
                if self.lastSender != device and self.lastSender != None:
                    print(f"DATA {self.data} transmitted")
                    device.clock_read(self.data, self)
                else:
                    device.tick()
        '''
        data = self.devices[0].clock_write(self)
        if data == None:
            data = 0xFF
        else:
            print(f"DEVICE 1 SENDS {data}")
        self.devices[1].clock_read(data,self)
        data = self.devices[1].clock_write(self)
        if data == None:
            data = 0xFF
        else:
            print(f"DEVICE 2 SENDS {data}")
        self.devices[0].clock_read(data,self)    
        return True
    
class LinkBoy(PyBoy, LinkCapableDevice):
    def __init__(self, gamerom, *, window="SDL2", scale=2, symbols=None, bootrom=None, sound=False, sound_emulated=False, cgb=None, gameshark=None, log_level="WARNING", **kwargs):
        super().__init__(gamerom, window=window, scale=scale, symbols=symbols, bootrom=bootrom, sound=sound, sound_emulated=sound_emulated, cgb=cgb, gameshark=gameshark, log_level=log_level, **kwargs)
        print(self.register_file.cpu)
        self.isTransmitting = False
        self.isMaster = False
        self.bitsLeft = 0
    
    def tick(self, count=1, render=True):
        SC = self.memory[0xFF02]
        if get_bit(SC,0) == 1:
            self.isMaster = True
        else:
            self.isMaster = False
        
        return super().tick(count, render)
    def clock_write(self, link:Link):
        self.tick()
        SB = self.memory[0xFF01]
        SC = self.memory[0xFF02]
        wasTransmitting = self.isTransmitting

        if get_bit(SC, 7) == 1:
            print(SC)
            self.isTransmitting = True
        else:
    
            self.isTransmitting = False
        
        if get_bit(SC,0) == 1:
            self.isMaster = True
        else:
            self.isMaster = False
        
        if self.isTransmitting and self.bitsLeft == 0:
            self.bitsLeft = 7
            return get_bit(SB,7)
        elif self.bitsLeft != 0:
            self.bitsLeft -= 1
            if self.bitsLeft == 0:
                INTR_VBLANK, INTR_LCDC, INTR_TIMER, INTR_SERIAL, INTR_HIGHTOLOW = [1 << x for x in range(5)]
                self.mb.cpu.set_interruptflag(INTR_SERIAL)
            return get_bit(SB, 7)
            
        else:
            return None
        
    def clock_read(self, bit: int, link):
        SB = self.memory[0xFF01]
        SC = self.memory[0xFF02]
        #print(SC)
        wasTransmitting = self.isTransmitting
        #print(f"Was transmitting: {wasTransmitting}")

        #SC = set_bit(SC,7)
        
        shift_in_bit(SB, bit)
        #self.bitsLeft=8
        self.tick()
        pass
gb1 = LinkBoy("pokemon.gb")
gb2 = LinkBoy("pokemon2.gb")
link = Link()
link.register(gb1)
link.register(gb2)
'''
def GB1Loop():
    while gb1.tick():
        pass

def GB2Loop():
    while gb2.tick():
        pass

tgb1 = Thread(target=GB1Loop)
tgb2 = Thread(target=GB2Loop)
tgb1.start()
tgb2.start()
'''

while link.tick():
    if keyboard.is_pressed("t"):
        gb1.button("up")
    elif keyboard.is_pressed("g"):
        gb1.button("down")
    elif keyboard.is_pressed("f"):
        gb1.button("left")
    elif keyboard.is_pressed("h"):
        gb1.button("right")
    elif keyboard.is_pressed("y"):
        gb1.button("a")
    
    if keyboard.is_pressed("i"):
        gb2.button("up")
    elif keyboard.is_pressed("k"):
        gb2.button("down")
    elif keyboard.is_pressed("j"):
        gb2.button("left")
    elif keyboard.is_pressed("l"):
        gb2.button("right")
    elif keyboard.is_pressed("p"):
        gb2.button("a")
    
    pass