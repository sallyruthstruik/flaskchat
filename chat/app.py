import datetime
import logging
import os
from logging import StreamHandler

import mongoengine
import sys
from bson import ObjectId
from flask.app import Flask
from flask.json import JSONEncoder
from mongoengine.base import BaseDocument

from chat.auth import login_manager
from chat.models import db, ModelMixin
from chat.websockets import socketio

app = Flask(__name__)


class ChatJsonEncoder(JSONEncoder):

    def default(self, o):
        # import ipdb;ipdb.set_trace()
        if isinstance(o, ModelMixin):
            return o.to_dict()
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, (datetime.datetime, datetime.date)):
            return o.strftime("%Y-%m-%d %H:%M:%S")

        return super().default(o)


def get_app(config_name="chat.config.Development")-> Flask:
    config_name = os.environ.get("APP_CONFIG", config_name)

    app.config.from_object(config_name)

    app.template_folder = "templates"

    db.init_app(app)
    socketio.init_app(app, message_queue=app.config["SOCKETIO_QUEUE"])
    login_manager.init_app(app)

    app.json_encoder = ChatJsonEncoder

    # to load all routes
    import chat.views

    logging.basicConfig(
        level=app.config["LOGLEVEL"],
        format="%(asctime)s [%(levelname)s][%(name)s] %(message)s",
        handlers=[
            StreamHandler(stream=sys.stderr)
        ]
    )
    logging.info("Created new server!")

    return app
