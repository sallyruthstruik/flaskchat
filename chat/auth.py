from flask_login.login_manager import LoginManager

from chat import models

login_manager = LoginManager()

login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return models.User.get(id=user_id)
