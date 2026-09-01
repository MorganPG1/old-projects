'''
This application should be able to read and clear all faults in a vehicle,
$xxx = ecu id
$0x = obd2 basic command 
All vehicles should be able to read $7E0 (ecm/pcm), $7E1 (tcm), $03 (current obd-ii codes), $07 (pending obd-ii codes), $0A (permanant obd-ii codes) - However basic obd-ii reading is not used as you can obtain better results from reading ecm fault codes
'''

from obd2.OBDMain import OBD, CommandReturn, dprint
from obd2.commands import at as atCommands
import obd2.commands as commands
  #Python-OBD ( https://python-obd.readthedocs.io/en/latest/ )
'''
basic usage of python-obd
import obd

connection = obd.OBD(port) # auto-connects to USB or RF port

cmd = obd.commands.SPEED # select an OBD command (sensor)

response = connection.query(cmd) # send the command, and parse the response

print(response.value) # returns unit-bearing values thanks to Pint
print(response.value.to("mph")) # user-friendly unit conversions

Note to future me: remove this as it is for a basic reference.
'''
class ecu:
    def __init__(self, name, id, returnid, longName:str="") -> None:
        self.name = name
        self.id = id
        self.returnid = returnid
        self.longName = longName
        pass
port = "COM5"
obd = OBD()

ecuList = [
    ecu("SRS", "6E0", "51C", "Airbag"),
    ecu("4WD", "7B6", "7B7", "Final drive"),
    ecu("AMP", "7F0", "53E", "Amplifier"),
    ecu("ABS", "784", "785", "ABS"),
    ecu("AHBM", "710", "522", "Auto High Beam"),
    ecu("DDM", "640", "508","Driver Door"),
    ecu("ESM", "788", "789","Electronic Shifter"),
    ecu("VES", "7D0", "53A","Entertainment System"),
    ecu("FCM", "620", "504","Front control"),
    ecu("HFM", "7F8", "53F","Hands free"),
    ecu("HLM", "7C8", "539","Headlamp Leveling"),
    ecu("HVAC", "688", "511","Heat ventilation and a/c"),
    ecu("HSM", "6D8", "51B","Heated seat"),
    ecu("IPC", "6A0", "514","Instrument Panel"),
    ecu("ITM", "670", "50E","Intrustion"),
    ecu("LRS", "780", "530","Last row screen"),
    ecu("LRSM", "708", "521","Rain sensor"),
    ecu("MSMD", "660", "50C","Memory seat"),
    ecu("OCM", "6E8", "51D","Occupant Seat"),
    ecu("PTM", "698", "513","Parktronics"),
    ecu("PDM", "650", "50A","Passenger door"),
    ecu("PLM", "728", "525","Power liftgate"),
    ecu("ECM", "7E0", "7E8","Engine control"),
    ecu("RADIO", "6B0", "516","Radio"),
    ecu("SDAR", "7D8", "53B","Satellite reciever"),
    ecu("SDVR", "738", "527","Satellite video reciever"),
    ecu("SCM", "622", "484","Steering column"),
    ecu("SCM_E", "6A8", "515","Steering column (early)"),
    ecu("SUNR", "638", "507","Sunroof module"),
    ecu("TBCM", "6E0", "51C", "Trailer module"),
    
    ecu("TCM", "7E1", "7E9","Transmission control"),
    ecu("WCM", "600", "500","Wireless control"),
    
    
]
print(obd.query(atCommands.RV))

initQueries = {
    atCommands.D: "",
    atCommands.ST: "1F",
    atCommands.SP: "A6",

}


def init():
    for command, args in initQueries.items():
        dprint(obd.query(command, args))

def readfaults(ecuid,ecureturn):
    obd.query(atCommands.SH, ecuid)
    obd.query(atCommands.FCSH, ecuid)
    obd.query(atCommands.CRA, ecureturn)
    obd.query(atCommands.FCSD, "30 00 00")
    obd.query(atCommands.FCSM, "1")
    return obd.query(commands.EscalateConnection_KWP, "92"), obd.query(commands.ReadDTCS_KWP, "00 FF00")

init()
'''

'''
log = open("logaaaaaaaaaaaaaaaaa.log", "w")
def logprint(text):
    log.write(text+"\n")
    print(text)

index = 0
validIndex = []
for ecu2 in ecuList:
    if obd.query(commands.TesterPresent, "01 1").value:
        print(f"{index}: {ecu2.name} ({ecu2.longName})")
        validIndex.append(index)
    index += 1

userEcu = int(input("Pick a ecu: "))
if userEcu in validIndex:
    chosenEcu = ecuList[userEcu]
    print("---------------------------------------------")
    print("Elevated or normal diagnostic session")
    print("Normal diagnostic can only read dtcs,")
    print("while elevated diagnostic can do multiple")
    print("functions. However, elevated diagnostics")
    print(",for certain modules, turns on warning lights")
    print("without setting dtcs. This is only to ")
    print("indicate you are in extended diag.")
    print("---------------------------------------------")
    print("1) Extended 2) Normal")
    extOrNormal = input(":")
    mode = ""
    if extOrNormal == "1":
        mode = "Extended"
    else:
        mode = "Normal"
    print(mode)
else:
    print("Not a option!")    

for ecu2 in ecuList:
    
    resp, faults = readfaults(ecu2.id, ecureturn=ecu2.returnid)
    faultsData:commands.DTC = faults.value
    dprint(resp.value)
    logprint(f"----{ecu2.name} ({ecu2.longName})----")
    if not isinstance(faultsData, commands.NoResponse):  
        for fault in faultsData:
            logprint(f"--{fault.code}-{fault.state}-")
        logprint("----END----\n")
    else:
        logprint("NO RESPONSE")
        logprint("----END----\n")

'''
import customtkinter

ctk = customtkinter.CTk()
ctk.minsize(800,600)
ctk.maxsize(800, 600)

customtkinter.CTkLabel(ctk, 20,20,0, font=customtkinter.CTkFont("Helvetica", 20),text="sigma window").place(x=350,y=0)

customtkinter.CTkButton(ctk, corner_radius=0, text="Read faults").place(x=100, y=50)

ctk.mainloop()
log.close()
'''