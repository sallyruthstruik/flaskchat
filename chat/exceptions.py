
class ChatException(Exception):
    """
    Base exception class for all project exceptions
    """


class ResponseException(ChatException):
    code = 500
    message = "Server error"

    @property
    def name(self):
        return self.__class__.__name__

    def __init__(self, code, message):
        self.code = code
        self.message = message


class ValidationError(ResponseException):
    errors = None

    @classmethod
    def field_error(cls, field, error):
        return cls({field: error})

    def __init__(self, errors):
        super().__init__(400, "Validation error")
        self.errors = errors

    def __getattr__(self, item):
        return self.errors[item]
