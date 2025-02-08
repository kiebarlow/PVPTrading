from flask import Flask
from Database.py import currentGames

app = Flask(__name__)

@app.route("/getCurrentGames")
def getCurrentGames():
    curr = currentGames("Y")
    currGames = []
    for game in curr:
        currGames.append({
            "game ID":game[0],
            "start time":game[1],
            "end time":game[2],
            "jackpot":game[3]
        })
    return currGames


    