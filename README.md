# Five in a Row
This is the repository for a game of Five in a Row 
(https://en.wikipedia.org/wiki/Gomoku). It is based on a React web application 
with a Flask API powering its backend. Communication between server and client 
happens through Socket.io to ensure real-time updates. 
The application can be accessed through
[https://five-in-a-row-game.herokuapp.com/](https://five-in-a-row-game.herokuapp.com/)

To play the game:
1. Join the web page and wait for a second user to join.
2. When the second user joins, the game will automatically start.
3. Play until there is a winner.
4. Restart the game if desired.

## Getting Started
### Installing dependencies
#### Python3 and Node
This project requires having Python3 and Node installed on your machine.

#### Virtual Environment
It is recommended to use a virtual environment to install the necessary Python packages.
To create a virtual environment, follow those steps:
1. Install `virtualenv` if you haven't done so yet: `pip install virtualenv`
2. From the root directory, create a virtual environment called `env`: `python -m venv env`
3. Activate the virtual environment: `source env/bin/activate`
4. To deactivate the virtual environment, simply run: `deactivate`

#### Backend Dependencies (PIP)
Once you have your virtual environment setup and running, install dependencies by running the following command
from the root directory:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Backend Dependencies
- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. 
Flask is required to handle requests and responses.

- [Flask-SocketIO](https://flask-socketio.readthedocs.io/en/latest/) gives Flask applications 
access to low latency bi-directional communications between the clients and the server.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/) is a Flask extension for handling 
Cross Origin Resource Sharing (CORS), making cross-origin AJAX possible.

#### Frontend Dependencies (NPM)
Starting from the root directory, run the following commands:
```bash
cd client
npm install
```
This will install all the necessary requirements.

#### Key Frontend Dependencies
- [React.js](https://reactjs.org/) as the frontend framework of choice.

- [React-Bootstrap](https://react-bootstrap.github.io/) is an implementation of 
[Bootstrap](https://getbootstrap.com/) for React

- [Socket.io-client](https://socket.io/docs/client-api/) is the client facing library
of Socket.io, to interface with the backend.

### Running the Application
There are two ways to run the application locally: development and production.
#### Development
1. From the client directory: `npm start`
2. In a separate terminal, from the root directory: `python app.py`
3. Open `http://localhost:3000/`

#### Production
1. From the client directory: `npm run build`
2. In a separate terminal, from the root directory: `python app.py`
3. Open `http://localhost:5000/`

