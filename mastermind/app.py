from flask import Flask, render_template
from .controllers.GameController import gameController

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('start.html')


@app.route('/game/create')
def createGame(game):
    return render_template('game.html', game=gameController(username="fred", size=5, maxvalue=5, doubles=True, cheatmode=True))

@app.route('/game/run/')
def runGame():
    return render_template('game.html')

if __name__ == '__main__':
    app.run()
