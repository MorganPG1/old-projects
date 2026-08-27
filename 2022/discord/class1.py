
import imp
import colors
from colors import red
import requests
import os

#Config
webhook = 'https://discord.com/api/webhooks/REDACTED'
while True:
    print("Enter content")
    cnt = input()
    a = requests.post(webhook, data={"content": cnt})
    if a.status_code == 204:
        print("Request Succeded")
        os.system("cls")
    else:
       os.system("cls")
       print(red("Request Failed: "),a.status_code)

    if a.text != "":
        print("Request recieved response: ",a.text)