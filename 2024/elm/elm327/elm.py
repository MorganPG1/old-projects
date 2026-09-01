from car.car import Car
class ELM327():

    def __init__(self, car:Car) -> None:
        self.car = car
        pass

    def sendCommand(self, command:str):
        if command.startswith("AT"):
            return "?>"
        else:
            return self.car.bus.runCommand(command) +">"