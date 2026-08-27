from serial import Serial
from obd import OBDReader

class SerialReader():
    def __init__(self, port):
        '''
            Handle serial communication to OBD Reader
        '''
        self.serialConnection =  Serial(port)
        pass
    def clear(self):
        '''
        Clear the buffers
        '''
        self.serialConnection.flush()
        pass
    def send(self, data):
        self.serialConnection.write(data.encode())
        pass
    def read(self) -> str:
        response = self.serialConnection.read()
        return response.decode()

