from chat.app import get_app
from chat.websockets import socketio

application = get_app()

if __name__ == '__main__':
    socketio.run(application, port=5000)
