import datetime
import typing

from flask.globals import current_app
from flask_login.mixins import UserMixin
from flask_mongoengine import MongoEngine
import mongoengine as me
from mongoengine.queryset.manager import QuerySetManager
from mongoengine.queryset.queryset import QuerySet
from pymongo.database import Database

db = MongoEngine()


class ModelMixin:
    created = me.DateTimeField(default=datetime.datetime.utcnow)

    def to_dict(self):
        return self.to_mongo()

    @classmethod
    def get(cls, **params):
        return cls.objects.get(**params)

    @classmethod
    def create(cls, **kwargs):
        return cls.objects.create(**kwargs)

    @classmethod
    def count(cls):
        return cls.objects.count()


def get_plain_db()-> Database:
    return db.connection[current_app.config["MONGODB_SETTINGS"]["db"]]


class User(me.Document,
           ModelMixin,
           UserMixin):
    username = me.StringField(max_length=1000, regex=r"\w+", min_length=3, unique=True)

    def get_id(self):
        try:
            return str(self.id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    def __repr__(self):
        return f"User(username={self.username!r}, id={self.id!r})"


class MessageQuerySet(QuerySet):
    def fetch_users(self, max_depth=1)-> list:
        uids = {
            item.user.id
            for item in self
        }

        users = {
            u.id: u
            for u in User.objects.filter(
                id__in=uids
            )
        }

        out = []
        for item in self:
            item.user._cached_doc = users[item.user.id]
            out.append(item)

        return out

class MessageQSManager(QuerySetManager):
    default = MessageQuerySet


class Message(me.Document,
              ModelMixin):
    objects = MessageQSManager()
    user = me.LazyReferenceField(User)
    message = me.StringField(max_length=10000, min_length=1)
