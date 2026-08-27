import requests
import json
import os

url = 'http://127.0.0.1:5000/'
token_get_url = url+'gen-token'
login_url = url+'login-token?token='


headers = {'Content-Type': 'application/json'}
def clearTerm():
    os.system('cls' if os.name == 'nt' else 'clear')
clearTerm()
print("Signup or Login?")
sol = input("")
if sol.lower() == "signup":
    print("Username: ")
    user = input()
    print("Password: ")
    passw = input()
    data = {'username': user, 'password': passw}
    a = requests.post(token_get_url, json.dumps(data), headers=headers)
    print(a.text)
    bc = requests.get(url+'get-info?token=' + a.json()['token'])
    b = bc.json()
    print(b)
    exit()
    def commandList():
        if b['isAdmin']:
            print("Options:")
            print("Get Token")
            print("Admin Panel")
            print("Logout")
        else:
            print("Options:")
            print("Get Token")
            
            print("Logout")
    if 'error' in b:
        clearTerm()
        print("Server side error: " + b['error'])
    else:
        clearTerm()
        if b['isBanned']:
            if b['banLength'] == -1:
                print("Permantely banned")
                print(" ")
                print("Note: "+b['banNote'])
                print(" ")
                print("Options:")
                print("Logout")
                while True:
                    com = input()
                    if com.lower == "logout":
                        requests.get(url+'deauth-token?token='+a.json()['token'])
                        break
            else:
                print("Banned for " + str(b['banLength']) + "day(s)")
                print(" ")
                print("Note: "+b['banNote'])
                print(" ")
                print("Options:")
                print("Logout")
                while True:
                    com = input()
                    if com.lower() == "logout":
                        requests.get(url+'deauth-token?token='+a.json()['token'])
                        exit()
        else:
            if b['isAdmin']:
                print("Welcome [ADMIN] " + b['username'])
                print("Balance: "+"{:,}".format(b['balance']))
                print(" ")
                commandList()
            else:
                print("Welcome " + b['username'])
                print("Balance: "+"{:,}".format(b['balance']))
                print(" ")
                commandList()
        while True:
            com = input()
            if com.lower() == "get token":
                print("Token: " + a.json()['token'])
            if com.lower() == "logout":
                requests.get(url+'deauth-token?token='+a.json()['token'])
                break
            if com.lower() == "admin panel":
                print(" ")
                print("Admin Options")
                print("Ban User")
                cool = input()
                if cool.lower() == "ban user":
                    print("Who?")
                    u = input()
                    print("How long (in days, -1 = perm)")
                    t = input()
                    print("Note?")
                    n = input()
                    resp = {'token': a.json()['token'], 'username': u, 'length': int(t), 'note': str(n)}
                    a = requests.post(url + '/admin/ban-user', json.dumps({'token': a.json()['token'], 'username': u, 'length': int(t), 'note': str(n)}), headers=headers)
                    print(resp)
                    
