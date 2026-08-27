from flask import Flask, make_response, render_template, request, redirect
import mysql.connector


db = mysql.connector.connect(
    user = "root",
    password = "REDACTED",
    database = "bs_scores"
)

database = db.cursor()
app = Flask("main")

@app.route("/")
def home():
    database.execute("SELECT * FROM scoretable ORDER BY score DESC;")
    scores = database.fetchmany(10)
    database.fetchall()
    print(scores)
    scoreList = []
    for score in scores:
        print(score)
        username = score[0]
        songId = score[1]
        scoreAmount = score[2]
        difficulty = score[3]
        database.execute("SELECT songName FROM songs WHERE id = %s;", (songId,))
        songName = database.fetchall()
        print(songName)
        scoreList.append({
            "username":username,
            "song":songName[0][0],
            "score":scoreAmount,
            "difficulty":difficulty
        })
    return render_template("index.html", list=scoreList)
@app.route("/add-score", methods = ["GET", "POST"])
def addScore():
    if request.method == "GET":
        database.execute("SELECT * FROM songs ORDER BY songname ASC;")
        song = database.fetchall()
        songs = []
        for song in song:
            print(song)
            id = song[0]
            name = song[1]
            songs.append({
                "id":id,
                "name":name
            })
        return render_template("add-score.html", songs = songs)
    else:
        name = request.form.get("username")
        score = request.form.get("score")
        song = request.form.get("song")
        difficulty = request.form.get("difficulty")
        if name == "" or score == "" or song == "" or difficulty == "":
            
            return redirect("/")
        else:
            print("Succ")
            print(name, score, song, difficulty)
            database.execute('INSERT INTO scoretable (username, song, score, difficulty) VALUES (%s, %s,%s, %s);', (name, song, score, difficulty))
            db.commit()
            return redirect("/")

@app.route("/search", methods = ["GET", "POST"])
def search():
    if request.method == "GET":
            database.execute("SELECT * FROM songs ORDER BY songname ASC;")
            song = database.fetchall()
            songs = []
            for song in song:
                print(song)
                id = song[0]
                name = song[1]
                songs.append({
                    "id":id,
                    "name":name
                })
            return render_template("search.html", songs = songs)
    else:
            name = request.form.get("username")
            score = request.form.get("score")
            song = request.form.get("song")
            difficulty = request.form.get("difficulty")
            sql = "SELECT * FROM scoretable"

            if song != "":
                if sql.endswith("scoretable"):
                    sql += " WHERE song = "+song
                else:
                    sql += " AND song = "+song
            if name != "":
                if sql.endswith("scoretable"):
                    sql += " WHERE username = '"+name+"'"
                else:
                    sql += " AND username = '"+name+"'" 
            if score !="":
                if sql.endswith("scoretable"):
                    sql += " WHERE score >= "+score
                else:
                    sql += " AND score >= "+score
            if difficulty != "":
                if sql.endswith("scoretable"):
                    sql += " WHERE difficulty = '"+difficulty+"'"
                else:
                    sql += " AND difficulty = '"+difficulty+"'" 
            sql += " ORDER BY score DESC;"
            print(sql)
            database.execute(sql)
            results = database.fetchall()
            print(results)
            resultTable = []
            for result in results:
                name = result[0]
                database.execute("SELECT songName FROM songs WHERE id = %s;", (result[1],))
                song = database.fetchall()[0][0]
                score = result[2]
                difficulty = result[3]
                resultTable.append({
                    "username": name,
                    "song": song,
                    "score": score,
                    "difficulty":difficulty
                })
            return render_template("results.html", scores = resultTable)
app.run("0.0.0.0", 1234)