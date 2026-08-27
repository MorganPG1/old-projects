from package import ecu, bus, dcm

bus = bus.Bus()
ecu.ecu(bus, 1, "ECM")
ecu.Test(bus, 9, "DDM")
dcm.IPC(bus, 10, "IPC")
while True:
    bus.mainloop()