import requests
import json
url = "http://192.168.1.216:25565"
def create():
    password = input("Password: ")
    wallet = requests.get(url=f'{url}/get-wallet?password={password}')
    print(f"Genetated wallet: {wallet.text}")
    main()
def check():
    wallet = input("Wallet: ")
    if wallet == "saved":
        f = open("wallet.txt", "r")
        data = f.read()
        if data != "":
            wallet = data
            f.close()
        else:
            print("NO SAVED WALLET")
            f.close()
            main()
    password = input("Password: ")
    rq = requests.get(url=f'{url}/get-balance?password={password}&wallet={wallet}')
    print(f"You have {rq.text} in the wallet")
def save():
    wallet = input("Wallet (if clearing enter clear): ")
    f = open("wallet.txt", "w")
    if wallet != "clear":
        f.write(wallet)
    else:
        f.write("")
    f.close()
def send():
    wallet = input("Wallet: ")
    if wallet == "saved":
        f = open("wallet.txt", "r")
        data = f.read()
        if data != "":
            wallet = data
            f.close()
        else:
            print("NO SAVED WALLET")
            f.close()
            main()
    password = input("Password: ")
    amount = input("Amount: ")
    recip = input("Recipient: ")
    data=json.dumps({"wallet": wallet, "password":password, "recip":recip, "sendAmount":amount})
    a = requests.post(f"{url}/send-coin", data=data, headers={"Content-Type": "application/json"})
    print(a.text)
    main()
def main():
    print("1) Create account")
    print("2) Send money")
    print("3) Check balance")
    print("4) Save wallet (once used when using any other option and asked for wallet enter saved, doesnt save passwords)")
    a = input("Option: ")
    if a == "1":
        create()
    elif a == "2":
        send()
    elif a == "3":
        check()
    elif a == "4":
        save()
main()