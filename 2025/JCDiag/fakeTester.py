from obd import OBDReader

class FakeReader(OBDReader):
    def __init__(self):
        self.buffer = ""
    def read(self):
        return self.buffer
    def send(self, data:str):
        if data.startswith("10"):
            self.buffer = "50 92"
        elif data.startswith("18"):
            self.buffer = "7F 18 78\r0:58 04 D4 08 30 07\r1: 10 30 D4 0A 30 D4 0C\r2: 30 FF FF FF FF FF"
    