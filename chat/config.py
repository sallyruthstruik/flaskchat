
class BaseConfig:
    DEBUG = False
    TESTING = False
    LOGLEVEL = "INFO"

    SECRET_KEY = "123enaDC;LKASE-2309U8EOPAIdjLKADNMNWdpokwe[f0okvt09hi460j7eyhgnkrstgbvn kajlercnoiQWJD[   3JIEP9843"

    MONGODB_SETTINGS = {
        "host": "localhost",
        "db": "chat",
    }


class Development(BaseConfig):
    DEBUG = True


class Testing(BaseConfig):
    DEBUG = True
    Testing = True

    MONGODB_SETTINGS = {
        "host": "localhost",
        "db": "chat_test",
    }
