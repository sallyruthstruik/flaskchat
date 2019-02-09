
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
pipenv run pytest tests.py
```

Run server:

```
pipenv run python server.py
```

Server will be runned at 127.0.0.1:8000

Run server under docker-compose:

```
docker-compose up
```

In this case server will be runned at 0.0.0.0:80.


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

### Version version-3

* Add Docker environment. In docker server is runned using uWSGI + gevent + monkey-patching
* Add docker-compose with multiserver environment
* Add rabbitmq for correct multiserver support (see https://flask-socketio.readthedocs.io/en/latest/#using-multiple-workers)
* Add nginx frontend with 3 servers in upstream

### Version version-4

* Bugfix: display name in socket add_to_history event
* More docs