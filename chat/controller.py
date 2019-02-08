from flask_login.utils import login_user, current_user
from mongoengine.errors import NotUniqueError

from chat import models
from chat.exceptions import ValidationError


def login(username):
    if not username:
        raise ValidationError.field_error("username", "need at least 3 symbols")

    try:
        user = models.User.create(username=username)
    except NotUniqueError:
        raise ValidationError({"username": f"user with username {username} already registered"})

    login_user(user)
    return user


def new_message(message):
    models.Message.create(message=message, user=current_user.id)


def history():
    messages = models.Message.objects.order_by("-created").limit(50).fetch_users()
    return reversed(messages)

