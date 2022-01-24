import logging
import os
from threading import Lock
from time import time

from flask import Flask, session
from flask_cors import CORS
from flask_socketio import SocketIO, emit

from utils.GridJson import GridJson

async_mode = None

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SOCKET_SECRET")
CORS(app)
socketio = SocketIO(
    app, async_mode=async_mode,
    cors_allowed_origins=os.getenv("ORIGIN")
)
thread = None
thread_lock = Lock()


def background_thread():
    count = 0
    while True:
        socketio.sleep(1)
        time_ = time()
        count += 1
        try:
            data = GridJson().get()
        except Exception as e:
            logging.error("Data get error: %s" % e)
            data = None
        socketio.emit("message", {
            "data": data, "count": count, "process_time": round(time() - time_, 3)
        })


@socketio.event
def data_event(message):
    session["receive_count"] = session.get("receive_count", 0) + 1
    emit("message",
         {"data": message["data"], "count": session["receive_count"]})


@socketio.event
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
    emit("connect", {"data": "Connected", "count": 0})


if __name__ == "__main__":
    socketio.run(app)
