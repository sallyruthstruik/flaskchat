"""
This module contains controller functions.
Extracting layer controller allows to don't worry about server implementation.
For example it will be easy to switch login from HTML form to AJAX when login logic is separated
from view logic.

All methods in this module raise :class:`.ValidationError` in case of bad input
"""
from flask_login.utils import login_user, current_user
from mongoengine.errors import NotUniqueError

from chat import models
from chat.exceptions import ValidationError


def login(username: str)-> models.User:
    """
    Performs login for user with username
    """
    if not username:
        raise ValidationError.field_error("username", "need at least 3 symbols")

    try:
        user = models.User.create(username=username)
    except NotUniqueError:
        raise ValidationError({"username": f"user with username {username} already registered"})

    login_user(user)
    return user


def new_message(message):
    """
    Method creates new message in database
    """
    return models.Message.create(message=message, user=current_user.id)


def history():
    """
    Method returns last 20 :class:`.models.Message` items (so it is message history)
    Items are ordered by created DESC
    """
    messages = models.Message.objects.order_by("-created").limit(20).fetch_users()
    return reversed(messages)

