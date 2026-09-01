from flask import Flask, make_response, Response, request
import hashlib
import http
import random
import json
import threading
import time

global hashStr
hashStr = ""
global string
string = ""
hashed = {}
def read(fileName):
    file = open(fileName, "r")
    cont = json.loads(file.read())
    file.close()
    return cont

def write(fileName, text):
    file = open(fileName, "w")
    file.write(json.dumps(text))
    file.close()
wallets = read("wallets.json")
server = Flask(__name__)


def addToList():
    time.sleep(1)
    f = open("hashes.json")
    a = f.read()
    ab = json.loads(a)
    f.close()
    if hashStr not in ab:
        ab[hashStr] = string
        f = open("hashes.json", "w")
        f.write(json.dumps(ab))
        f.close()

@server.route("/send-hash", methods=["POST"])
def main():
    global hashStr
    global string
    hashStr = request.get_json()["hash"]
    string = request.get_json()["text"]
    wallet = request.get_json()["wallet"]
    
    strHashed = hashlib.sha256(str.encode(string)).hexdigest()
    if strHashed == hashStr and wallet != None and wallet in wallets:
        wallets[wallet]["value"] = wallets[wallet]['value'] + 0.001
        if request.remote_addr not in hashed:
            hashed[request.remote_addr] = []
            hashed[request.remote_addr].append(hashStr)
            thr1 = threading.Thread(target=addToList)
            thr1.start()
        else:
            if hashStr not in hashed[request.remote_addr]:
                hashed[request.remote_addr].append(hashStr)
                thr1 = threading.Thread(target=addToList)
                thr1.start()

            else:
                return "fail"
        write("wallets.json", wallets)
        return "success"
    else:
        print(string)
        print(hashStr)
        print(strHashed)
        return "fail"
@server.route("/send-coin", methods=["POST", "get"])
def send():
    if request.method == "GET":
        return Response(status=418)
    
    wallet = request.get_json()["wallet"]
    password = request.get_json()["password"]
    recip = request.get_json()["recip"]
    sendAmount = request.get_json()["sendAmount"]
    if wallet in wallets and recip in wallets:
        if hashlib.sha256(bytes(password.encode())).hexdigest() == wallets[wallet]["password"]:
            wallets[wallet]["value"] = wallets[wallet]["value"] - int(sendAmount)
            wallets[recip]["value"] = wallets[recip]["value"] + int(sendAmount)
            write("wallets.json", wallets)
            return "Success"
        else:
            return make_response("Invalid Password", 403)
    else:
        return make_response("Wallet(s) not found", 404)
@server.route("/get-balance")
def balance():
    if request.args.get("wallet") in wallets:
        passw = request.args.get("password")
        if hashlib.sha256(bytes(passw.encode("utf-8"))).hexdigest() == wallets[request.args.get("wallet")]["password"]: 
                return str(wallets[request.args.get("wallet")]["value"])
        else:
            print()
            print(wallets[request.args.get("wallet")]["password"])
            return "invalid pass"
    else:
        return "invalid wallet"
@server.route("/get-wallet")
def walletGen():
    if request.args.get("password") != None:
        walletName = hashlib.sha256(bytes(random.randrange(1,10000000))).hexdigest()
        if walletName not in wallets:
            wallets[walletName] = {"password":hashlib.sha256(bytes(request.args.get("password").encode("utf-8"))).hexdigest(), "value":0}
            write("wallets.json", wallets)
            return walletName
        else:
            return "Try again"
    else:
        return "no pass"
#server.run("127.0.0.1", 25565)
server.run("192.168.1.216", 25565)