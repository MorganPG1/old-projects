from car.ecu import command

def reset():
    return "ELM327 v1.5"
atCommands = {
    "ATZ": command(reset, "ATZ"),
    "ATRV": 
}