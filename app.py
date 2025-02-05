# Basic structure inspired by
# https://stackoverflow.com/questions/44209978/serving-a-front-end-created-with-create-react-app-with-flask

import os
import json

from flask import Flask, send_from_directory, jsonify, request, abort
from flask_cors import CORS
from flask_socketio import SocketIO, emit

from game import Game

HEIGHT = 19
WIDTH = 19
g = Game(HEIGHT, WIDTH)
app = Flask(__name__, static_folder='client/build')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(16))
cors = CORS(app)
socket = SocketIO(app, cors_allowed_origins='*')


# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


def get_user_turn():
    if len(g.players) < 2:
        user_turn = None
    else:
        user_turn = g.players[0] if g.first_player_turn else g.players[1]
    return user_turn


def get_user_stone(user_turn):
    if user_turn is None:
        return None

    return g.BLACK if g.players.index(user_turn) == 0 else g.WHITE


def generate_board_object(success):
    user_turn = get_user_turn()
    user_stone = get_user_stone(user_turn)

    return json.dumps({
        'success': success,
        'board_data': g.board_data,
        'winner': g.winner,
        'user_turn': user_turn,
        'user_stone': user_stone,
        'num_players': len(g.players)
    })


def emit_update_board(success):
    board = generate_board_object(success)
    emit('update_board', board, broadcast=True)


@socket.on('connect')
def on_connect():
    success = g.add_player(request.sid)
    emit_update_board(True)
    return success


@socket.on('disconnect')
def on_disconnect():
    g.remove_player(request.sid)
    g.reset_game()
    emit_update_board(True)


@socket.on('get_board')
def get_board():
    return generate_board_object(True)


@socket.on('make_play')
def make_play(x, y):
    success = g.make_play(x, y, request.sid)
    emit_update_board(success)


@socket.on('reset_game')
def reset_game():
    g.reset_game()
    emit_update_board(True)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socket.run(app, host='0.0.0.0', port=port, debug=True)
