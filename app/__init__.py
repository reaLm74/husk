from flask import Flask, jsonify, request
from flask_login import (LoginManager, current_user, login_user, login_required,
                         logout_user)
from flask_marshmallow import Marshmallow

from app.create_db import create_db
from app.models import db, Tasks, Users
from app.request_data_base import (get_add_task, get_task_detail, get_tasks,
                                   get_update_task, get_delete_task,
                                   get_user_by_username, add_user)


def create_app():
    app = Flask(__name__)
    ma = Marshmallow(app)
    app.config.from_object('app.config')
    db.init_app(app)
    create_db(app)

    login_manager = LoginManager(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(user_id)

    class TasksSchema(ma.Schema):
        class Meta:
            fields = ("id", "title", "description", "done")

    task_schema = TasksSchema()
    tasks_schema = TasksSchema(many=True)

    @app.route('/todo/api/v1.0/tasks', methods=['GET', 'POST'])
    @login_required
    def get_create_tasks():
        """Вывод всех задач и добавление новой"""
        try:
            if request.method == 'GET':
                obj_task = get_tasks()
                output = tasks_schema.dump(obj_task)
                return jsonify({'tasks': output})

            elif request.method == 'POST':
                if 'title' not in request.json:
                    return jsonify({'error': 'Bad request'}), 400
                new_task = get_add_task(request.json)
                output = task_schema.dump(new_task)
                return jsonify({'task': output})
        except Exception as e:
            return jsonify({'error': str(e)}), 404

    @app.route('/todo/api/v1.0/tasks/<int:task_id>',
               methods=['GET', 'PUT', 'DELETE'])
    @login_required
    def get_update_delete_task(task_id):
        """Вывод, изменение или удаление задачи"""
        try:
            if request.method == 'GET':
                obj_task = get_task_detail(task_id)
                output = task_schema.dump(obj_task)
                return jsonify({'task': output})

            elif request.method == 'PUT':
                obj_task = get_update_task(task_id, request.json)
                output = task_schema.dump(obj_task)
                return jsonify({'task': output})

            elif request.method == 'DELETE':
                get_delete_task(task_id)
                return jsonify({'result': 'Task delete'})
        except Exception as e:
            return jsonify({'error': str(e)}), 404

    @app.route('/todo/api/v1.0/auth/login', methods=['GET', 'POST'])
    def login():
        """Авторизация пользователя"""
        try:
            if current_user.is_authenticated:
                return jsonify(
                    {'auth': f'User {current_user} is authorized'}
                ), 200
            if request.method == 'POST':
                user = Users.query.filter(
                    Users.username == request.json['username']
                ).first()
                if user and user.check_password(request.json['password']):
                    login_user(user)
                    return jsonify(
                        {
                            'auth': f'User {request.json["username"]}'
                                    f' is authorized'}
                    ), 200
                return jsonify({'error': 'Invalid username or password'}), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 404

    @app.route('/todo/api/v1.0/auth/signup', methods=['POST'])
    def signup():
        """Регистрация пользователя"""
        try:
            if len(request.json['username']) < 4 or len(
                    str(request.json['password'])) < 6:
                return jsonify(
                    {'error': 'Fields are not filled in correctly'}), 401
            check_user = get_user_by_username(request.json['username'])
            if check_user == 1:
                return jsonify({'error': 'User is registered'}), 401
            add_user(request.json)
            return jsonify({'signup': 'Successful'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 404

    @app.route('/todo/api/v1.0/auth/logout', methods=['POST'])
    @login_required
    def logout():
        """Выход из под пользователя"""
        try:
            logout_user()
            return jsonify({'auth': f'User is unauthorized'}), 200
        except Exception as e:
            return jsonify({'error': f'Error logout user {str(e)}'}), 404

    return app
