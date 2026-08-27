from hashlib import sha256
import json
from random import randrange
import random
import os
from flask import Flask, request, make_response
#a = [{'a': 'b'}]
#print(a[0]['a'])
#datab = open("database.txt", "w")
#datab.write(json.dumps(a))
#datab.close()
#sha256('hi'.encode('utf-8')).hexdigest() - hash
file1 = open('database.txt', 'r') #Open database
strData = file1.read()
print(strData)
data = json.loads(s=strData)
file1.close()
app = Flask(__name__)


@app.route('/gen-token', methods=["GET", "POST"]) #Generate token or create account

def generate_token(): #Define the generation function
    if request.method == "GET": #If using browser
        user = request.args.get('user') #Get the user argument passed into the website
        password = request.args.get('pass') #Get the password argument passed in to website
        user2 = user.lower() #Make username lowercase so it dosent matter if it is capitalized
        if user2 not in data[0] or data[0][user2] != sha256(password.encode('utf-8')).hexdigest(): #Check if the user is not in the database or the password is incorrect
            print(sha256(password.encode('utf-8')).hexdigest()) #Print the hash of the password entered
            return make_response({'error': 'Invalid username or password'}, 403) #Return error data
        print(len(user2)) #Print the length of the username
        chars = 'abcdefABCDEF' #Define characters used in token generation
        for token in list(data[1].keys()): #For all tokens in the database, check if they are tied to the user and if they are delete them
             if data[1][token] == user2: 
                  del data[1][token]
        token = str(randrange(1000, 9999)) + random.choice(chars) + random.choice(chars) + str(randrange(1000, 9999)) + random.choice(chars) + random.choice(chars) + str(randrange(1000, 9999)) + random.choice(chars) + random.choice(chars) + str(randrange(1000, 9999)) + random.choice(chars) + random.choice(chars) + '--' + str(randrange(len(user)*100, len(user)*10000)) + '--' + str(randrange(1000, 9999)) + random.choice(chars) + random.choice(chars) + str(randrange(1000, 9999)) + random.choice(chars) + random.choice(chars) #Generate token
        print(token) #Print token for debugging, however in a production enviroment you may want to comment this out for security
        data[1][token] = user2 #Assign token to account
        file = open("database.txt", "w") #Open the database in write mode
        file.write(json.dumps(data)) #Write data to database
        file.close() #Apply changes
        return {'token': str(token)} #Return token
    else:
       
        a = request.json #Get request data
        if a['username'].lower() not in data[0]: #Check if username is not in database
          if 'username' not in a or 'password' not in a: #Check if username or password is not defined and if so return error
             return make_response({'error': 'Username or Password not defined'}, 400)
          user2 = a['username'] #Get username
          user = a['username'].lower() #Make username lowercase so it dosent matter if its capitalized
          data[0][a['username'].lower()] = sha256(a['password'].encode('utf-8')).hexdigest() #Assign password to new account
          chars = 'abcdefABCDEF' #Define characters used in token generation
          #for token in list(data[1].keys()): #For all tokens in database, check if they are tied to the user and if they are delete them
             #if data[1][token] == user2:
                  #del data[1][token]
          token = str(randrange(1000, 9999)) + random.choice(chars) + random.choice(chars) + str(randrange(1000, 9999)) + random.choice(chars) + random.choice(chars) + str(randrange(1000, 9999)) + random.choice(chars) + random.choice(chars) + str(randrange(1000, 9999)) + random.choice(chars) + random.choice(chars) + '--' + str(randrange(len(a['username'])*100, len(a['username'])*10000)) + '--' + str(randrange(1000, 9999)) + random.choice(chars) + random.choice(chars) + str(randrange(1000, 9999)) + random.choice(chars) + random.choice(chars) #Generate token, this is the longest line in the code because of how complicated i made the generation process
          print(token) #Print token for debugging, however in a production enviroment you may want to comment this out for security
          data[1][token] = a['username'].lower() #Assign token to account
          data[2][a['username'].lower()] = {'username': a['username'], 'isAdmin': False, 'isBanned': False, 'banLength': 0, 'banNote': '', 'banTime': 0, 'balance': 0} #Set user data
          returnData = {'username': a['username'], 'password': sha256(a['password'].encode('utf-8')).hexdigest(), 'token': token} #Define return data
          file = open("database.txt", "w") #Open database in write mode
          print(data) #Print database for debugging, in a production enviroment you may want to comment this out for security
          file.write(json.dumps(data)) #Write data to database
          dumps = json.dumps(returnData) #Define return data in json format
          file.close() #Apply changes
          return dumps #Return the data
        else:
         user2 = a['username'] #Get username
         user = a['username'].lower() #Make username lowercase so it dosent matter if its capitalized 
         password = a['password'] #Get password

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
         file.close()
         return dumps
    
@app.route('/check-token', methods=["GET"]) #Check if token is valid

def check_token():
    token = request.args.get("token")
    if token not in data[1]: #If not valid respond with error
        return make_response({'error': 'Token Invalid'}, 403) #Return error
    else: #If valid return username linked to token
        return {'username': data[1][token]} #Return linked username

@app.route('/deauth-token', methods=["GET"])
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
                    return make_response({'success': 'User banned'})
                else:
                    return make_response({'error': 'User does not exist'}, 400)

app.run()