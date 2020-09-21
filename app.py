# Basic structure inspired by
# https://stackoverflow.com/questions/44209978/serving-a-front-end-created-with-create-react-app-with-flask

import os

from flask import Flask, send_from_directory, jsonify, request, abort
from flask_cors import CORS

from game import Game

HEIGHT = 19
WIDTH = 19
g = Game(HEIGHT, WIDTH)
app = Flask(__name__, static_folder='client/build')
cors = CORS(app)


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
    val = body.get('val')
    success = g.make_play(x, y, val)

    return jsonify({
        'success': success,
        'board_data': g.board_data,
        'winner': g.winner
    })


if __name__ == '__main__':
    app.run(debug=True)
