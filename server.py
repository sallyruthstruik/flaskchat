from chat.app import get_app

application = get_app()

if __name__ == '__main__':
    application.run(port=8000)
