import test
import time
running = False
kernelInfo = test.getKernelInfo()
def sysInfo():
    info = test.getSystemInfo()
    memoryTotal = int(info["memoryTotal"])/1073741824
    memoryFree = int(info["memoryFree"])/1073741824
    print("--CPU--")
    print("Name:",info["cpuName"])
    print("Cores:",info["cpuCores"])
    print("Freq: {:0.0f}GHz".format(info["cpuFreqCurrent"]))
    print("--RAM--")
    print("Total: {:0.1f}GB".format(memoryTotal))
    print("Free: {:0.1f}GB".format(memoryFree))
    print("--Other--")
    print("Kernel:",kernelInfo["kernelName"])
    print("Kernel Version:",kernelInfo["kernelVer"])
def ifconfig():
    # Use the `test` library to get network interface information
    network_info = test.getNetworkInfo()

    # Iterate through the network interfaces
    for interface_name, interface_info in network_info.items():
        print("Interface:", interface_name)

        # Check if the interface has an IP address
        if "ipAddr" in interface_info:
            print("  IP Address:", interface_info["ipAddr"])

        # Check if the interface has a MAC address
        if "macAddr" in interface_info:
            print("  MAC Address:", interface_info["macAddr"])
def shutdown():
    global running
    running = False
commands = {
    "sysinfo": sysInfo,
    "si":sysInfo,
    "shutdown": shutdown,
    "ifconfig": ifconfig
    
}


print("KERNEL:",kernelInfo["kernelName"],kernelInfo["kernelVer"])
print("STARTING....")
time.sleep(3)
running = True
while running:
    term = input("user@os $ ")
    if term.lower() in commands:
        commands[term.lower()]()
    