import logging
import os

from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit

from utils.GridJson import GridJson

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SOCKET_SECRET")
socketio = SocketIO(app, cors_allowed_origins="https://okx.koval.page")
CORS(app)

clients = []


@socketio.on('connect')
def handle_connect():
    logging.info('Client connected')
    clients.append(request.sid)


@socketio.on('disconnect')
def handle_disconnect():
    logging.info('Client disconnected')
    clients.remove(request.sid)


def send_message(client_id):
    emit('message', GridJson().get(), room=client_id)


# def main():
#     webapp_thread = threading.Thread(target=run_web_app)
#     webapp_thread.start()
#
#     while not clients:
#         logging.info("waiting for client to connect")
#         sleep(1)
#
#     sleep(1)
#     send_message(clients[0])


if __name__ == "__main__":
    socketio.run(app)
