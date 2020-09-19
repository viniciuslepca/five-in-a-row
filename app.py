# Basic structure inspired by
# https://stackoverflow.com/questions/44209978/serving-a-front-end-created-with-create-react-app-with-flask

import os

from flask import Flask, send_from_directory, jsonify

app = Flask(__name__, static_folder='client/build')


# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


@app.route('/test')
def test():
    return jsonify({
        'success': True,
        'value': 'test'
    })


if __name__ == '__main__':
    app.run(debug=True)
