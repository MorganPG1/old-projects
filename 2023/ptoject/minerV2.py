import hashlib
import time
import json
import os
import threading
import requests
file = open("lastID.txt", "r")
global id
if file.read() == "":
    id = 0
else:
    id = int(file.read())
file.close()
wallet = '3f7dea81937ded9041e2466a5f831af8cd60b65b67ec9d5b6d33659489d310b3'
password = 'abc123'
url = "http://192.168.1.216:25565"
def printThread():
    while True:
        time.sleep(0.25)
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
        balance = requests.get(f"{url}/get-balance?wallet={wallet}&password={password}")
        if balance.text == "invalid pass" or balance.text == "invalid wallet":
            print("ERROR GETTING BALANCE")
            print(balance.text)
        else:
            print(f"Balance now is {balance.text} and it has generated {id} passes since the first run")

def main():
    while True:
        global id
        id = id+1
        hexID = format(id, "x")
        hash = hashlib.sha256(str.encode(hexID)).hexdigest()
        data=json.dumps({"hash":hash, "text":hexID, "wallet":wallet})
        ab = requests.post(url=f"{url}/send-hash", data=data, headers={"Content-Type": "application/json"})
        file = open("lastID.txt", "w")
        file.write(str(id))
        file.close()
time.sleep(1)
thread1 = threading.Thread(target=printThread)
thread1.start()
thread2 = threading.Thread(target=main)
thread2.start()