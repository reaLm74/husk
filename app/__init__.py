from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from app.create_db import create_db
from app.models import db
from app.request_data_base import (get_add_task, get_task_detail, get_tasks,
                                   get_update_task, get_delete_task,
                                   get_user_by_username, add_user)
from app.task.models import Tasks
from app.task.views import blueprint as task_blueprint
from app.user.models import Users
from app.user.views import blueprint as user_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config')
    db.init_app(app)
    migrate = Migrate(app, db)

    create_db(app)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(task_blueprint)

    login_manager = LoginManager(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(user_id)

    return app
