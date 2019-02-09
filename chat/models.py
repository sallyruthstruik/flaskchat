"""
This module provides model classes for business entities.
We're store data in mongodb, so mongoengine+Flask-mongoengine are used.
"""
import datetime
from flask.globals import current_app
from flask_login.mixins import UserMixin
from flask_mongoengine import MongoEngine
import mongoengine as me
from mongoengine.queryset.manager import QuerySetManager
from mongoengine.queryset.queryset import QuerySet
from pymongo.database import Database

db = MongoEngine()


class ModelMixin:
    """
    Common mixin, allows to incapsulate and make easy
    logic of getting and creating items
    """
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
        """
        Because user is related field,
        message.user.fetch() will trigger db query.
        To prevent this, I override QuerySet and add this method
        which prefetches all user objects for current message queryset

        .. warning::

            This method should be used last, otherwise
            there are some side effects may be.

        """
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
            # prefetch user.
            # after that, calling message.user.fetch()
            # won't trigger db query
            item.user._cached_doc = users[item.user.id]
            out.append(item)

        return out


class MessageQSManager(QuerySetManager):
    """
    Manager runs queryset on model
    """
    default = MessageQuerySet


class Message(me.Document,
              ModelMixin):
    objects = MessageQSManager()
    user = me.LazyReferenceField(User)
    message = me.StringField(max_length=10000, min_length=1)

    meta = {
        'indexes': {
            # need descending create index,
            # becase there is search query in controller.history
            # In future it also can be useful, because we'll be able
            # to set ttl index and autoremove old messages.
            '-created'
        }
    }