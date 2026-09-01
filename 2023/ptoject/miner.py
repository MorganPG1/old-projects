import hashlib
import time
import json
import requests
a = 0
wallet = 'f1855958bf6f05793daa17816c086f8122b0f32173735e1f5a7e531cfc470063'
while True:
    a = a+1
    print(hex(a))
    b = hex(a)
    hash = hashlib.sha256(str.encode(b)).hexdigest()
    print(hash)
    data=json.dumps({"hash":hash, "text":b, "wallet":wallet})
    print(data)
    ab = requests.post(url="http://192.168.1.216:25565/send-hash", data=data, headers={"Content-Type": "application/json"})
    time.sleep(2)
    print(ab.text)