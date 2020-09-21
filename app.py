# Basic structure inspired by
# https://stackoverflow.com/questions/44209978/serving-a-front-end-created-with-create-react-app-with-flask

import os

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


@app.route('/game')
def get_game():
    return jsonify({
        'success': True,
        'board_data': g.board_data
    })


@app.route('/game', methods=['POST'])
def make_play():
    body = request.get_json()
    if body is None:
        abort(400)
    x = body.get('x')
    y = body.get('y')
    success = g.make_play(x, y)

    return jsonify({
        'success': success,
        'board_data': g.board_data,
        'winner': g.winner
    })


@app.route('/new_game')
def reset_game():
    g.reset_game()

    return jsonify({
        'success': True,
        'board_data': g.board_data
    })

@socket.on('connect')
def on_connect():
    print(request.sid, 'connected')

@socket.on('disconnect')
def on_disconnect():
    print(request.sid, 'disconnected')

@socket.on('my event')
def get_my_event(json, arg2):
    print('my event:', json, arg2)

if __name__ == '__main__':
    socket.run(app, debug=True)
