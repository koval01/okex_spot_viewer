from flask import Flask
from flask_socketio import SocketIO, emit

from utils.GridJson import GridJson

app = Flask(__name__)
app.config['SECRET_KEY'] = 'EAWn3Tbyih4tpyuYCjZ1'
socketio = SocketIO(app)


@socketio.on('OkxData')
def handle_my_custom_event(data):
    return emit(
        "OkxData", GridJson().get(),
        namespace="/data", broadcast=True
    )


if __name__ == "__main__":
    socketio.run(app)
