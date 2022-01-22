import os

from flask import Flask
from flask_socketio import SocketIO, send

from utils.GridJson import GridJson

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SOCKET_SECRET")
socketio = SocketIO(app, cors_allowed_origins="https://okx.koval.page")


@socketio.on('data')
def handleMessage(msg):
    return send(GridJson().get(), broadcast=True)


if __name__ == "__main__":
    socketio.run(app)
