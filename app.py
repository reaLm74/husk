import os
import sqlite3

from flask import Flask, jsonify, request, g
from flask_login import (LoginManager, login_user, login_required,
                         logout_user, current_user)
from werkzeug.security import generate_password_hash, check_password_hash

from request_data_base import RequestDataBase
from user_login import UserLogin

app = Flask(__name__)
app.config.from_object('config')
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'sqlite.db')))

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().from_db(user_id, dbase)


def create_db():
    """Вспомогательная функция для создания таблиц  БД"""
    db = connect_db()
    with app.open_resource('new_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def connect_db():
    # Подключение к БД
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


@app.teardown_appcontext
def close_db(error):
    """Закрываем соединение с БД"""
    if hasattr(g, 'link_db'):
        g.link_db.close()


def link_db():
    """Соединение с БД, если оно еще не установлено"""
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


dbase = None


@app.before_request
def before_request():
    """Соединение с БД перед выполнением запроса"""
    global dbase
    db = link_db()
    dbase = RequestDataBase(db)


@app.route('/todo/api/v1.0/tasks', methods=['GET', 'POST'])
@login_required
def get_create_tasks():
    """Вывод всех задач и добавление новой"""
    try:
        if request.method == 'GET':
            get_tasks = dbase.get_tasks()
            if get_tasks is False:
                return jsonify({'error': 'Not tasks'}), 404
            return jsonify({'tasks': get_tasks})

        elif request.method == 'POST':
            result = dbase.get_add_task(request.json)
            if result is False:
                return jsonify({'error': 'Bad request'}), 400
            return dbase.get_task_detail(result[1])
    except Exception as e:
        return jsonify({'error': str(e)}), 404


@app.route('/todo/api/v1.0/tasks/<int:task_id>',
           methods=['GET', 'PUT', 'DELETE'])
@login_required
def get_update_delete_task(task_id):
    """Вывод, изменение или удаление задачи"""
    try:
        if request.method == 'GET':
            get_task = dbase.get_task_detail(task_id)
            if get_task is False:
                return jsonify({'error': 'Not found task'}), 404
            return jsonify({'task': get_task})

        elif request.method == 'PUT':
            check_task = dbase.get_task_detail(task_id)
            if check_task is False:
                return jsonify({'error': 'Not found task'}), 404
            dbase.get_update_task(task_id, request.json)
            get_task = dbase.get_task_detail(task_id)
            return jsonify({'task': get_task})

        elif request.method == 'DELETE':
            get_task = dbase.get_task_detail(task_id)
            if get_task is False:
                return jsonify({'error': 'Not found task'}), 404
            dbase.get_delete_task(task_id)
            return jsonify({'result': 'Task delete'})
    except Exception as e:
        return jsonify({'error': str(e)}), 404


@app.route('/todo/api/v1.0/auth/login', methods=['GET', 'POST'])
def login():
    """Авторизация пользователя"""
    try:
        if current_user.is_authenticated:
            user = current_user.get_name()
            return jsonify({'auth': f'User {user} is authorized'}), 200
        if request.method == 'POST':
            check_user = dbase.get_user_by_username(request.json['username'])
            if check_user is False:
                return jsonify({'error': 'User not found'}), 404
            if check_password_hash(
                    check_user['password'], request.json['password']
            ):
                u_login = UserLogin().create(check_user)
                login_user(u_login)
                return jsonify(
                    {'auth': f'User {request.json["username"]} is authorized'}
                ), 200
            return jsonify({'error': 'Invalid password'}), 200
        else:
            return jsonify({'auth': 'User is not authorized'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 404


@app.route('/todo/api/v1.0/auth/signup', methods=['POST'])
def signup():
    """Регистрация пользователя"""
    try:
        if len(request.json['username']) < 4 or len(
                str(request.json['password'])) < 6:
            return jsonify({'error': 'Fields are not filled in correctly'}), 401
        check_user = dbase.get_user_by_username(request.json['username'])
        if check_user is not False:
            return jsonify({'error': 'User is registered'}), 401
        hash_password = generate_password_hash(request.json['password'])
        dbase.add_user(request.json['username'], hash_password)
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


if __name__ == '__main__':
    app.run()
