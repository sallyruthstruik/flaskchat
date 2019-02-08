import datetime
from unittest.mock import patch

import pytest
import time
from flask.app import Flask
from mongoengine.errors import NotUniqueError

from chat import models, controller
from chat.exceptions import ValidationError
from chat.models import db, get_plain_db

from chat.app import get_app


@pytest.fixture(scope="session")
def app():
    return get_app("chat.config.Testing")


@pytest.fixture(autouse=True)
def clear(app: Flask):
    with app.test_request_context():
        get_plain_db().user.delete_many({})
        get_plain_db().message.delete_many({})


@pytest.fixture()
def request_context(app: Flask):
    with app.test_request_context() as ctx:
        yield ctx


def test_user():
    u = models.User.create(
        username="test"
    )

    assert u.username == "test"
    assert models.User.count() == 1
    assert u.created > datetime.datetime.utcnow() - datetime.timedelta(seconds=1)
    with pytest.raises(NotUniqueError):
        models.User.create(
            username="test"
        )

    u.delete()

    assert models.User.count() == 0


def test_message():
    u = models.User.create(
        username="test"
    )

    m = models.Message.create(
        user=u,
        message="hello"
    )

    assert m.user.fetch() == u


def test_controller(request_context):
    user = controller.login("test")

    with pytest.raises(ValidationError) as e:
        controller.login("test")

    e = e.value
    assert e.code == 400
    assert e.errors == {'username': 'user with username test already registered'}

    with patch.object(controller, "current_user", user):
        controller.new_message("message1")
        time.sleep(.1)
        controller.new_message("message2")

    history = list(controller.history())
    assert len(history) == 2
    assert [h.message for h in history] == ["message1", "message2"]

    assert [h.user._cached_doc.username for h in history] == ["test", "test"]
    assert [h.user.fetch().username for h in history] == ["test", "test"]

