from flask import Flask, render_template, session
from MysqlConnection import db_connection

app = Flask(__name__)





@app.route('/')
def home():
    return render_template('home.html')

@app.route('/stats')
def stats():
    return render_template('stats.html')

@app.route('/start')
def start():

    return render_template('start.html')

@app.route('/handle_username', methods=['POST'])
def handle_username():
    projectpath = request.form['projectFilepath']
    # do something with incoming data
    return render_template('home.html')


if __name__ == '__main__':
    app.run()
