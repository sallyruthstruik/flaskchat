
class BaseConfig:
    DEBUG = False
    TESTING = False
    LOGLEVEL = "INFO"

    SECRET_KEY = "123enaDC;LKASE-2309U8EOPAIdjLKADNMNWdpokwe[f0okvt09hi460j7eyhgnkrstgbvn kajlercnoiQWJD[   3JIEP9843"

    MONGODB_SETTINGS = {
        "host": "localhost",
        "db": "chat",
    }

    # connection string to rabbitmq.
    # It's needed for correct message broadcasting,
    # see https://flask-socketio.readthedocs.io/en/latest/#using-multiple-workers.
    SOCKETIO_QUEUE = "amqp://"


class Development(BaseConfig):
    DEBUG = True


class Testing(BaseConfig):
    DEBUG = True
    Testing = True

    MONGODB_SETTINGS = {
        "host": "localhost",
        "db": "chat_test",
    }


class Docker(BaseConfig):
    DEBUG = False
    Testing = False

    MONGODB_SETTINGS = {
        "host": "mongo",
        "db": "chat",
    }

    SOCKETIO_QUEUE = "amqp://rabbit"
