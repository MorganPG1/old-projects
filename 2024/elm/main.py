import elm327.at
from elm327.elm import ELM327
from car.car import Car
from car.bus import bus
from car.ecu import ecu
import serial

ecm = ecu("7E0")

ecuList = {"7E0": ecm}
bus2 = bus(ecuList=ecuList)
car = Car(bus2)
elm = ELM327(car)

ser = serial.Serial("COM3", timeout=3)

while True:
    data = ser.readline()
    print(data)
    if data.decode() != "":
        print("data recieved")
        print(data.decode())

        response = elm.sendCommand(data.decode())
        ser.write(response.encode())
    
    elm.car.bus.mainLoop()