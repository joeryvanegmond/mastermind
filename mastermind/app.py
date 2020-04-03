from .controllers.GameController import gameController
from flask import Flask, render_template, session, request, redirect, url_for, Response
from .MysqlConnection import db_connection

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
    session.clear()
    session['username'] = request.form['name']
    session['size'] = int(request.form['positions'])
    session['cheatmode'] = True
    session['maxvalue'] = int(request.form['colors'])
    session['doubles'] = False
    session['code'] = 0
    return redirect(url_for('run_game'))


@app.route('/game', methods=['GET', 'POST'])
def run_game():
    if session['code'] == 0:
        print("1")
        controller = gameController(session['username'], int(session['size']), session['cheatmode'], round=0)
        session['code'] = controller.generatecode(int(session['maxvalue']), int(session['doubles']))
        session['round'] = 0
        session['stats'] = []
        return render_template('game.html')
    else:
        print("2")
        controller = gameController(session['username'], int(session['size']), session['cheatmode'], int(session['round']))
        controller.set_code(session['code'])
        print("2.5")
        if controller.processanwser(session['anwser']):
            print("3")
            session['stats'].append(controller.turns)
            session['round'] += 1
            return redirect(url_for('victory'))
        print("4")
        session['stats'].append(controller.turns)
        session['round'] += 1
        return render_template('game.html')


@app.route('/update-game', methods=['GET', 'POST'])
def update_game():
    session['anwser'] = request.form['anwser']
    return redirect(url_for('run_game'))

@app.route('/test')
def test():
    session.clear()
    session['username'] = "Hans"
    session['size'] = 5
    session['cheatmode'] = True
    session['maxvalue'] = 5
    session['doubles'] = True
    session['code'] = 0
    return redirect(url_for('run_game'))

@app.route('/victory')
def victory():
    # db_connection.query("INSERT INTO stats VALUES()")
    return render_template('victory.html')

if __name__ == '__main__':
    app.run()
