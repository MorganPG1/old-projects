from jeep import Jeep
from serialAdapter import SerialReader

reader = SerialReader("COM3")
car = Jeep(reader)

print(Jeep.readAllModules())
