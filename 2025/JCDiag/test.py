import jeep
import emulator
bus = emulator.Bus()
ecm = emulator.ECU(
    "7E0",
    "7E8"
)
print(ecm.ecu_id, ecm.return_id)
bus.add(
ecm
)

reader = emulator.EmulatedTester(bus)
bus.add(reader)
car = jeep.Jeep(reader)

def statusToString(status):
    readiness, storage, warning = car.DecodeFaultStatus(status)
    print(readiness, storage, warning)
    statusString = ""
    if readiness == 1:
        statusString += "Test not complete "
    else:
        statusString += "Test complete "
    
    if storage == 1:
        statusString += ", Historical DTC "
    elif storage == 2:
        statusString += ", Pending DTC "
    elif storage == 3:
        statusString += ", Active DTC "
    
    if warning == 1:
        statusString += ", Warning Lamp Requested "
    return statusString
for module, dtcs in car.readAllModules().items():
    print(module)
    for dtc in dtcs:
        print(dtc[0], statusToString(dtc[1]))
