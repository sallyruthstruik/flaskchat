import logging
import os

from flask.app import Flask

from chat.auth import login_manager
from chat.models import db


app = Flask(__name__)


def get_app(config_name="chat.config.Development")-> Flask:
    config_name = os.environ.get("APP_CONFIG", config_name)

    app.config.from_object(config_name)

    app.template_folder = "templates"

    db.init_app(app)
    login_manager.init_app(app)

    # to load all routes
    import chat.views

    logging.basicConfig(
        level=app.config["LOGLEVEL"],
        format="%(asctime)s [%(levelname)s][%(name)s] %(message)s",
    )
    logging.info("Created new server!")

    return app
