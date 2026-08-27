from hashlib import sha256
import json
from random import randrange
import random
import os
from datetime import datetime
from flask import Flask, request, make_response
#a = [{'a': 'b'}]
#print(a[0]['a'])
#datab = open("database.txt", "w")
#datab.write(json.dumps(a))
#datab.close()
#sha256('hi'.encode('utf-8')).hexdigest() - hash
file1 = open('database.txt', 'r')
strData = file1.read()
print(strData)
data = json.loads(s=strData)
file1.close()

app = Flask(__name__)

@app.route('/gen-token', methods=["GET", "POST"]) #Generate token [expected data for get: /gen-token?user=%username%&pass=%password%  expected data for post: {"username": "username", "paassword": "password"}]

def login():
    if request.method == "GET":
        user = request.args.get('user')
        password = request.args.get('pass')
        user2 = user.lower()
        if user2 not in data[0] or data[0][user2] != sha256(password.encode('utf-8')).hexdigest():
            print(sha256(password.encode('utf-8')).hexdigest())
            return make_response({'error': 'Invalid username or password'}, 403)
        print(len(user2))
        chars = 'abcdefABCDEF'
        for token in list(data[1].keys()):
             if data[1][token] == user2:
                  del data[1][token]
        token = str(randrange(1000, 9999)) + random.choice(chars) + random.choice(chars) + str(randrange(1000, 9999)) + random.choice(chars) + random.choice(chars) + str(randrange(1000, 9999)) + random.choice(chars) + random.choice(chars) + str(randrange(1000, 9999)) + random.choice(chars) + random.choice(chars) + '--' + str(randrange(len(user)*100, len(user)*10000)) + '--' + str(randrange(1000, 9999)) + random.choice(chars) + random.choice(chars) + str(randrange(1000, 9999)) + random.choice(chars) + random.choice(chars)
        print(token)
        data[1][token] = user2
        file = open("database.txt", "w")
        file.write(json.dumps(data))
        return {'token': str(token)}
    else:
       
        a = request.json
        print(a)
        if a['username'].lower() not in data[0]:
          if 'username' not in a or 'password' not in a:
             return make_response({'error': 'Username or Password not defined'}, 400)
          user2 = a['username']
          user = a['username'].lower()
          data[0][a['username'].lower()] = sha256(a['password'].encode('utf-8')).hexdigest()
          chars = 'abcdefABCDEF'
          for token in list(data[1].keys()):
             if data[1][token] == user2:
                  del data[1][token]
          token = str(randrange(1000, 9999)) + random.choice(chars) + random.choice(chars) + str(randrange(1000, 9999)) + random.choice(chars) + random.choice(chars) + str(randrange(1000, 9999)) + random.choice(chars) + random.choice(chars) + str(randrange(1000, 9999)) + random.choice(chars) + random.choice(chars) + '--' + str(randrange(len(a['username'])*100, len(a['username'])*10000)) + '--' + str(randrange(1000, 9999)) + random.choice(chars) + random.choice(chars) + str(randrange(1000, 9999)) + random.choice(chars) + random.choice(chars)
          print(token)
          data[1][token] = a['username'].lower()
          print(data)
          data[2][a['username'].lower()] = {'username': a['username'], 'isAdmin': False, 'isBanned': False, 'banLength': 0, 'banNote': '', 'banTime': 0, 'balance': 0}
          returnData = {'username': a['username'], 'password': sha256(a['password'].encode('utf-8')).hexdigest(), 'token': token}
          file = open("database.txt", "w")
          print(data)
          file.write(json.dumps(data))
          dumps = json.dumps(returnData)
          print(dumps)
          return dumps
        else:
         user2 = a['username']
         user = a['username'].lower()
         password = a['password']

         if user not in data[0] or data[0][user] != sha256(password.encode('utf-8')).hexdigest():
            return make_response({'error': 'Password invalid (if signing up user exists)'}, 403)
         print(len(user))
         chars = 'abcdefABCDEF'
         for token in list(data[1].keys()):
             if data[1][token] == user2:
                  del data[1][token]
         token = str(randrange(1000, 9999)) + random.choice(chars) + random.choice(chars) + str(randrange(1000, 9999)) + random.choice(chars) + random.choice(chars) + str(randrange(1000, 9999)) + random.choice(chars) + random.choice(chars) + str(randrange(1000, 9999)) + random.choice(chars) + random.choice(chars) + '--' + str(randrange(len(user)*100, len(user)*10000)) + '--' + str(randrange(1000, 9999)) + random.choice(chars) + random.choice(chars) + str(randrange(1000, 9999)) + random.choice(chars) + random.choice(chars)
         print(token)
         data[1][token] = user
         returnData = {'username': a['username'], 'password': sha256(a['password'].encode('utf-8')).hexdigest(), 'token': token}
         file = open("database.txt", "w")
         file.write(json.dumps(data))
         dumps = json.dumps(returnData)
         return dumps
    
@app.route('/login-token', methods=["GET"]) #DEPRECATED DO NOT USE, takes in token value
def token():
    token = request.args.get("token")
    if token not in data[1]:
        return make_response({'error': 'Token Invalid'}, 403)
    else:
        return {'username': data[1][token]}

@app.route('/deauth-token', methods=["GET"]) #Delink token
def deauth():
    if request.method == "GET":
        token = request.args.get("token")
        if token not in data[1]:
            return make_response({'error': 'Token Invalid'}, 403)
        del data[1][token]
        file = open("database.txt", "w")
        file.write(json.dumps(data))
        return {'success': "Token "+token+" removed from database."}

@app.route('/get-info', methods=["GET"])
def getinfo():
    token = request.args.get("token")
    if token not in data[1]:
        return make_response({'error': 'Token Invalid'}, 403)
    userinfo = data[2][data[1][token]]
    return userinfo
    
@app.route('/admin/ban-user', methods=["POST"])
def banUser():
    dataBan = request.json
    if 'token' not in dataBan or 'username' not in dataBan or 'length' not in dataBan or 'note' not in dataBan:
        return make_response({'error': 'Missing user or token'}, 400)
    else:
        print(dataBan)
        if dataBan['token'] not in data[1]:
            return make_response({'error': 'Invalid Token'}, 403)
        else:
            userInfo = data[2][data[1][dataBan['token']]]
            if not userInfo['isAdmin']:
                return make_response({'error': 'You are not an admin!'}, 403)
            else:
                if dataBan['username'].lower() in data[0]:
                    banUserInfo = data[2][dataBan['username'].lower()]
                    banUserInfo['isBanned'] = True
                    banUserInfo['banLength'] = dataBan['length']
                    banUserInfo['banNote'] = dataBan['note']
                    banUserInfo['banDate'] = datetime.now().timestamp()
                    return make_response({'success': 'User banned'})
                else:
                    return make_response({'error': 'User does not exist'}, 400)

app.run()