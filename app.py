import os

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit

from utils.GridJson import GridJson

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SOCKET_SECRET")
socketio = SocketIO(app, cors_allowed_origins="https://okx.koval.page")
CORS(app)


@socketio.on('data')
def handleMessage(msg):
    return emit("data", GridJson().get(), broadcast=True)


if __name__ == "__main__":
    socketio.run(app)
