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
    sql = "SELECT * FROM stats ORDER BY cheatmode, rounds ASC"
    data = db_connection.select_query(sql)
    return render_template('stats.html', data=data)

@app.route('/start')
def start():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.form.get('allowdouble') == None:
        if request.form['positions'] > request.form['colors']:
            flash('kan geen spel creeëren met deze instellingen, verhoog het aantal mogelijke waardes, verlaag de lengte van de code, of schakel dubbelen waardes in.')
            return render_template('login.html')

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
    if len(request.form['anwser']) == session['size']:
        session['anwser'] = request.form['anwser']
        return redirect(url_for('run_game'))
    else:
        flash('zorg ervoor dat je code ' + str(session['size']) + ' lang is!')
        return render_template('game.html')

@app.route('/victory')
def victory():
    sql = "INSERT INTO stats (name, playtime, rounds, cheatmode) VALUES(?, ?, ?,?)"
    val = (session['username'], datetime.now(), session['round'], session['cheatmode'])
    db_connection.query(sql, val)
    return render_template('victory.html', name=session['username'], round=session['round'])

@app.template_filter('datetimeformat')
def datetimeformat(value):
    datetime_obj = datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f")
    return datetime_obj.strftime("%d-%m-%Y %H:%M")


if __name__ == '__main__':
    app.run()
