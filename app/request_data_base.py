import sqlite3

from app.models import db, Tasks, Users


def get_task_detail(task_id):
    """Вывод одной задачи"""
    try:
        res = db.get_or_404(Tasks, task_id)
        return res
    except sqlite3.Error as e:
        raise Exception(f'Error get task from the database {e}')


def get_tasks():
    """Вывод всех задач"""
    try:
        res = Tasks.query.all()
        return res
    except sqlite3.Error as e:
        raise Exception(f'Error get tasks from the database {e}')


def get_add_task(request_data):
    """Добавить задачу"""
    try:
        title = request_data['title']
        description = request_data.get('description', "")
        new_task = Tasks(title=title, description=description)
        db.session.add(new_task)
        db.session.flush()
        db.session.commit()
        return new_task
    except sqlite3.Error as e:
        raise Exception(f'Error add tasks {e}')


def get_update_task(task_id, request_data):
    """Обновить задачу"""
    try:
        task = db.get_or_404(Tasks, task_id)
        for key, value in request_data.items():
            if key == 'done':
                setattr(task, key, bool(value))
                continue
            setattr(task, key, value)
        db.session.commit()
        return task
    except sqlite3.Error as e:
        raise Exception(f'Error update task {e}')


def get_delete_task(task_id):
    """Удалить задачу"""
    try:
        task = db.get_or_404(Tasks, task_id)
        db.session.delete(task)
        db.session.commit()
        return True
    except sqlite3.Error as e:
        raise Exception(f'Error delete {e}')


def add_user(request):
    """Добавить пользователя"""
    try:
        print(request)
        new_user = Users(username=request['username'])
        new_user.set_password(request['password'])
        db.session.add(new_user)
        db.session.commit()
    except sqlite3.Error as e:
        raise Exception(f'Error add user {e}')


def get_user_by_username(username):
    """Получение пользователя по username"""
    try:
        user = Users.query.filter(Users.username == username).count()
        return user
    except sqlite3.Error as e:
        raise Exception(f'Error get user {e}')
