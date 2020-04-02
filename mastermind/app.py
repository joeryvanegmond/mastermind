from .controllers.GameController import gameController
from flask import Flask, render_template, session, request, redirect
from MysqlConnection import db_connection

app = Flask(__name__)
app.config['SECRET_KEY'] = 'prettyprinted'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/stats')
def stats():
    return render_template('stats.html')

@app.route('/start')
def start():

    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    name = request.form['name']
    db_connection.query('INSERT INTO stats VALUES(null, ?, null, null, null)', [name])

    return render_template('home.html', name=name)



@app.route('/game/create')
def createGame(game):
    return render_template('game.html', game=gameController(username="fred", size=5, maxvalue=5, doubles=True, cheatmode=True))

@app.route('/game/run/')
def runGame():
    return render_template('game.html')

if __name__ == '__main__':
    app.run()
