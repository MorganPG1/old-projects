import requests
#r = requests.post("http://127.0.0.1:5000/send", json={""})
r = requests.get("http://127.0.0.1:5000/get")
if r.status_code == 200:
    for item in r.json():

        print("Name:", str(item["firstName"]) +" "+ str(item["lastName"]),"Age:", str(item["age"]))