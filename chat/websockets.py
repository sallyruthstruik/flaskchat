import logging
from functools import wraps

from flask import json, abort
from flask_login import current_user
from flask_socketio import SocketIO, emit

from chat import controller

socketio = SocketIO()


def check_user(hdlr):
    @wraps(hdlr)
    def inner(*a, **k):
        if not current_user or not current_user.is_authenticated:
            logging.error("not authenticated socket message: current_user=%s, args=%s, kwargs=%s",
                          current_user, a, k)
            return False

        return hdlr(*a, **k)
    return inner


@socketio.on("enter_room")
@check_user
def handle_connect(message):
    logging.info("new handle_connect: %s, %s", message, current_user.username)


@socketio.on("new_message")
@check_user
def handle_new_message(message):
    logging.info("new handle_new_message: %s, %s", message, current_user.username)
    message = controller.new_message(message)

    user = message.user.fetch().to_dict()
    message = message.to_dict()
    message["user"] = user

    emit("add_to_history", json.dumps(message), broadcast=True)
