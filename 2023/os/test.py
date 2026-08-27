import platform
import psutil
import socket
name = "UNNAMED KERNEL"
ver = "DEV1"

def getSystemInfo():
    info = {}
    info["cpuName"] = platform.processor()
    info["cpuCores"] = psutil.cpu_count()
    info["cpuFreq"] = psutil.cpu_freq().max
    info["cpuFreqCurrent"] = psutil.cpu_freq().current
    info["memoryTotal"] = psutil.virtual_memory().total
    info["memoryFree"] = psutil.virtual_memory().free
    return info

def getKernelInfo():
    info = {}
    info["kernelVer"] = ver
    info["kernelName"] = name
    return info

def getNetworkInfo():
    info = {}
    interfaces = psutil.net_if_addrs().items()
    for key, val in interfaces:
        info[key] = {}
        for interface in val:
            
            if interface.family == socket.AF_INET:
                
                info[key]["ipAddr"] = interface.address
                info[key]["ipBroadcast"] = interface.broadcast
            elif interface.family == psutil.AF_LINK:
                info[key]["macAddr"] = interface.address
    return info

#print(getNetworkInfo())