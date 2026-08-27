#### Imports ####

import flask
from hashlib import sha256
import json
import random

####  Config  #####

debug = True #Runs server under port 5000 instead of port 80
ip = "127.0.0.1" #Ip to run under

flaskApp = flask.Flask(__name__)

#### Main functions ####


def isDataValid():
    if len(jsonDatabase) >= 3:
        print("Database loaded successfully")
    else:
        print("Database is missing data! Length is "+len(jsonDatabase)+" and should be 3 or more.")

def main():
    ## Define globals
    global database
    global databaseText
    global jsonDatabase
    ##

    database = open("database.json", "r") #Open database
    databaseText = database.read() #Read all data in database
    database.close()
    
    ## Try and decode the database, printing all errors if caught
    try:
        jsonDatabase = json.loads(databaseText)
    except Exception as error:
        print("Error reading database: "+str(error))
        database.close()
        exit()
    ##

    ## Check if running in debug mode
    if debug:
        flaskApp.run(ip, 5000)
    else:
        flaskApp.run(ip, 80)
    ##

def generateToken(userid):
    base64list = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_" #base64 char list
    token = str(userid)+"-" #base part of token
    
    for i in range(1,50): #repeat 50 times
        token = token + random.choice(base64list) #add a random base64 characte

    return token #return the token

def updateDatabase():
    database = open("database.json", "w")
    database.write(json.dumps(jsonDatabase))
    database.close()
#### Routes ####
@flaskApp.route("/gen-token", methods= ["POST"])

def signupOrLogin(): #Login or signup
    
    requestInfo = flask.request.json #Get request json
    username = requestInfo["username"]
    password = requestInfo["password"]
    userId = jsonDatabase[0] + 1
    hashedPassword = sha256(password.encode("utf-8")).hexdigest()
        
    if "username" in requestInfo and "password" in requestInfo: #Check if request is valid
        if username.lower() not in jsonDatabase[2]: #Check if user does not exist
            

            userData = {
                "username": username,
                "password": hashedPassword,
                "banData": {
                    "banDate": 0,
                    "isBanned": False,
                    "unbanDate": 0,
                    "banLength": 0
                },
                "userId": userId,
                "money": 0
            }

            profileData = {
                "username": username,
                "userId": userId,
                "money": 0
                
            }

            infoData = {
                "username": username,
                "banData": {
                    "banDate": 0,
                    "isBanned": False,
                    "unbanDate": 0,
                    "banLength": 0,
                },
                "userId": userId,
                "money": 0
            }

            token = generateToken(userId) #Generate token

            jsonDatabase[0] = userId #Set latest userId
            jsonDatabase[1][token] = username.lower()
            jsonDatabase[2][username.lower()] = userData #Set private data
            jsonDatabase[3][username.lower()] = infoData #Set data returned by get-info
            jsonDatabase[4][username.lower()] = profileData #Set public data

            updateDatabase() #Update the database
            return flask.make_response({"token": token}, 200) #Return the token

    else: #If data is invalid

        return flask.make_response({"error": "Invalid request"}, 400)
            

main()
database.close()