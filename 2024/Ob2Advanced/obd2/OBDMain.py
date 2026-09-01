import serial
import time
import random

isDebug = False

def dprint(*args):
    if isDebug:
        print("[DEBUG]",*args)
class FakeSerial():
    ResponseTable = {
        #b"18 00 FF00" : b"7F 18 78 \r00E \r0: 58 04 D4 08 30 07\r1: 10 30 D4 0A 30 D4 0C 2: 30 FF FF FF FF F\r FF \r\r>",
        b"18 00 FF00" : b"58 01 C1 84 60 \r\r>",
        b"10": b"50 92",
        b"3E": b"7E",
        #b"1A 90": b"REDACTED (my dad's vin number)"
    }
    def __init__(self) -> None:
        self.readBuffer = []
        self.writeBuffer = []
        pass
    def read_all(self):
        main = b""
        dprint(self.readBuffer)
        
        ind = 0
        for strl in self.readBuffer:
            if ind+1 >=  len(self.readBuffer):
                main += strl
            else:
                main += strl + b"\r"
            ind+=1
        dprint(main)
        
        self.readBuffer = []
        return main
    def readline(self):
        buffer = self.readBuffer[-1]
        self.readBuffer.pop()
        return buffer
    def writelines(self, lines:list[str]):
        print(lines)
        for value in lines:
            self.write(value)    	
    def write(self, value):
        iscommand = False
        self.writeBuffer.append(value)
        if self.writeBuffer[-1] == b"\r":

            str = b""
            for value in self.writeBuffer:
                str += value
            self.writeBuffer = []
            value = str
            if isinstance(value,bytes):
                dprint("command")

                for command, response in self.ResponseTable.items():

                    if value.startswith(command):
                        iscommand = True
                        if random.randrange(0,5) == 1:
                            self.readBuffer.append(b"SEARCHING... \rUNABLE TO CONNECT")
                        else:
                            self.readBuffer.append(response)
                        break
                
                if value.startswith(b"AT RV") and not iscommand:
                    self.readBuffer.append(b"12.5V\r\r>")
                elif value.startswith(b"AT") and not iscommand:
                    self.readBuffer.append(b"OK\r\r>")
                elif not iscommand:
                    self.readBuffer.append(b"BUS ERROR\r\r>")
                
            else:
                raise TypeError("Not bytes.")    
    def reset_input_buffer(self):
        self.readBuffer = []
        
class CommandReturn:
    def __init__(self, value, name:str = "", strValue:str=None) -> None:
        self.value = value
        self.name = name
        self.strValue = strValue
        pass
    def __str__(self):
        if self.strValue != None:
            return self.strValue
        else:
            return str(self.value)
        
    
class ReturnType:
    def __init__(self) -> None:
        pass
    
    def decode(self, value) -> CommandReturn:
        raise NotImplementedError("Do not use ReturnType as a returntype, instead make a child/sub class of it and use that")


class Command:
    
    def __init__(self, command:str, returnType:ReturnType, name:str="", description:str="", space:bool=True ) -> None:
        self.name = name
        self.description = description
        self.command = command
        self.returnType = returnType
        
        self.space = space
        pass

    def run(self, serial:serial.Serial, arg=""):

        command = self.command
        if self.space:
             command = command+" "+arg
        else:
             command = command+arg
        command
        time.sleep(0.1)
        serial.read_all()
        for char in command:
             serial.write(char.encode())
	
        serial.write(b"\r")
        

        dprint(command.encode())
        time.sleep(0.25)
        s = serial.read_all()
        returnedVal = s.decode().removeprefix(command).replace("\x07", "")

        dprint(returnedVal, s)
        return self.returnType.decode(returnedVal)

    
class OBD:
    
    def __init__(self, port:str=None) -> None:
        '''
        Port: The serial port to communicate with
        '''
        if port:
            
            self.serial = serial.Serial(port, timeout=5)
            self.serial.write(b"A")
            self.serial.write(b"T")
            self.serial.write(b"E")
            self.serial.write(b"0")
            self.serial.write(b"\r")

            
        
        else:
            self.serial = FakeSerial()
            self.serial.write(b"A")
            self.serial.write(b"T")
            self.serial.write(b"E")
            self.serial.write(b"0")
            self.serial.write(b"\r")
           
        pass
    
    def query(self, command:Command, args:str=""):
        a = command.run(self.serial, args)
        return a