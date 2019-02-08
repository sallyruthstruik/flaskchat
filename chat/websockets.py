import logging

from flask import json
from flask_login import current_user
from flask_socketio import SocketIO, emit

from chat import controller

socketio = SocketIO()


def check_user():
    pass


@socketio.on("enter_room")
def handle_connect(message):
    logging.info("new handle_connect: %s, %s", message, current_user.username)


@socketio.on("new_message")
def handle_new_message(message):
    logging.info("new handle_new_message: %s, %s", message, current_user.username)
    message = controller.new_message(message)
    emit("add_to_history", json.dumps(message), broadcast=True)
