from flask import session
# from Game import Game
from MysqlConnection import db_connection


class Player:
    def __init__(self, name: str):
        if 'player' not in session:
            session['player'] = name
            rows = db_connection.select_query('SELECT * FROM stats WHERE name = ?', [name])
            if len(rows) == 0:
                db_connection.query('INSERT INTO User VALUES(null, ?)', [name])
                rows = db_connection.select_query('SELECT * FROM User WHERE username = ?', [name])
            session['player_id'] = rows[0][0]

    # @staticmethod
    # def begin_game():
    #     return Game(session['player_id'], True)