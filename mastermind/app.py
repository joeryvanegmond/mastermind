from .controllers.GameController import gameController
from flask import Flask, render_template, session, request, redirect, url_for, flash
from .MysqlConnection import db_connection
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'prettyprinted'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/stats')
def stats():
    sql = "SELECT * FROM stats"
    return str(db_connection.query(sql))
    return render_template('stats.html')

@app.route('/start')
def start():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.form.get('allowdouble') is None:
        if request.form['positions'] > request.form['colors']:
            flash('kan geen spel creeëren met deze instellingen, verhoog het aantal mogelijke waardes, verlaag de lengte van de code, of schakel dubbelen waardes in.')
            return redirect(url_for('start'))

    session.clear()
    session['username'] = request.form['name']
    session['size'] = int(request.form['positions'])
    session['cheatmode'] = request.form.get('cheatmode')
    session['maxvalue'] = int(request.form['colors'])
    session['doubles'] = request.form.get('allowdouble')
    session['code'] = 0
    return redirect(url_for('run_game'))


@app.route('/game', methods=['GET', 'POST'])
def run_game():
    if session['code'] == 0:
        controller = gameController(session['username'], int(session['size']), session['cheatmode'], round=0)
        session['code'] = controller.generatecode(int(session['maxvalue']), session['doubles'])
        session['round'] = 0
        session['stats'] = []
        return render_template('game.html')
    else:
        controller = gameController(session['username'], int(session['size']), session['cheatmode'], int(session['round']))
        controller.set_code(session['code'])
        if controller.processanwser(session['anwser']):
            session['stats'].append(controller.turns)
            session['round'] += 1
            return redirect(url_for('victory'))
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
    sql = "INSERT INTO stats (name, playtime, rounds, cheatmode) VALUES(?, ?, ?,?)"
    val = (session['username'], datetime.now(), session['round'], session['cheatmode'])
    db_connection.query(sql, val)
    return render_template('victory.html', name=session['username'], round=session['round'])

if __name__ == '__main__':
    app.run()
