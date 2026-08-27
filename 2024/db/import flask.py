from flask import request, Flask, make_response
import mysql.connector
import random
import names

db = mysql.connector.connect(host = "localhost", password = "REDACTED", user = "root", database = "testing")
cursor = db.cursor()

app = Flask("__name__")
'''
namesList= [
    
]
list = []
global nm
for i in range(1,20):
    namesList.append((lastid+i, names.get_first_name("Male"), names.get_last_name(), random.randrange(13,52)))

print(namesList)
cursor.executemany("INSERT INTO testtable VALUES (%s, %s, %s, %s);",namesList )
db.commit()
cursor.execute("SELECT * FROM testtable;")
print(cursor.fetchall())
'''

@app.route("/send", methods = ["POST"])
def sendData():
    cursor.execute("SELECT id FROM testtable ORDER BY id ASC;")
    ids = cursor.fetchall()
    if len(ids) < 1:
        lastid = 0
    else:
        lastid = ids[len(ids)-1][0]

    json = request.json
    if "firstName" in json:
        firstName = json["firstName"]
    else:
        firstName = None
    if "lastName" in json:
        lastName = json["lastName"]
    else:
        lastName = None
    if "age" in json:
        age = int(json["age"])
    else:
        age = None
    
    if firstName == None and lastName == None and age == None:
        return make_response("No data passed", 400)
    cursor.execute("INSERT INTO testtable VALUES (%s, %s, %s, %s)", (lastid+1, firstName, lastName, age))
    db.commit()
    return {}

@app.route("/get", methods = ["GET"])
def readData():
    cursor.execute("SELECT * FROM testtable ORDER BY id DESC;")
    people = cursor.fetchmany(10)
    cursor.fetchall()
    list = []
    for person in people:
        if len(person) == 4:
            list.append({"firstName": person[1], "lastName": person[2], "age": person[3]})
    return list
app.run()
    