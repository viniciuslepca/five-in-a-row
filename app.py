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
app.config['SECRET_KEY'] = os.urandom(16)
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

@socket.on('connect')
def on_connect():
    return g.add_player(request.sid)

@socket.on('disconnect')
def on_disconnect():
    g.remove_player(request.sid)

@socket.on('get_board')
def get_board():
    return json.dumps({
        'success': True,
        'board_data': g.board_data
    })

def emit_update_board(success):
    response_object = json.dumps({
        'success': success,
        'board_data': g.board_data,
        'winner': g.winner
    })

    emit('update_board', response_object, broadcast=True)

@socket.on('make_play')
def make_play(x, y):
    success = g.make_play(x, y)
    emit_update_board(success)

@socket.on('reset_game')
def reset_game():
    g.reset_game()
    emit_update_board(True)


if __name__ == '__main__':
    socket.run(app, debug=True)
