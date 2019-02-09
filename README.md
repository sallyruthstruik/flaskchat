
# Flask+websocket chat application

## Installation

Prerequisites:

* MongoDB server
* pipenv

Install requirements:

```
pipenv install --dev
```

Run tests:

```
pipenv run pytest
```

Run server:

```
pipenv run python server.py
```

Server will be runned at 127.0.0.1:8000

## Changelog

### Version version-1

* created project structure
* added support for libs: Flask-login, Flask-mongoengine
* added configurations
* added basic models, views, controllers
* login without password
* one room, no websockets, user can get history only by refreshing page


### Version version-2

* Added Flask-socketio and websockets support
* Changed development server to socketio
* New client with VueJS framework
* Client now supports realtime updates
