import sqlite3

from flask import jsonify


class RequestDataBase:
    def __init__(self, database):
        self.__database = database
        self.__cursor = database.cursor()

    def sql_query(self, sql):
        self.__cursor.execute(sql)
        return self.__cursor.fetchall()

    def sql_query_commit(self, sql):
        self.__cursor.execute(sql)
        self.__database.commit()

    def get_tasks(self):
        """Вывод всех задач"""
        try:
            sql = "SELECT * FROM tasks"
            res = RequestDataBase.sql_query(self, sql)
            if res:
                response = [{k: item[k] for k in item.keys()} for item in res]
                return response
            else:
                return False
        except sqlite3.Error as e:
            raise Exception(f'Error get tasks from the database {e}')

    def get_task_detail(self, task_id):
        """Вывод одной задачи"""
        try:
            sql = f'SELECT * FROM tasks WHERE id={task_id}'
            res = RequestDataBase.sql_query(self, sql)
            if res:
                response = [{k: item[k] for k in item.keys()} for item in res]
                return response
            else:
                return False
        except sqlite3.Error as e:
            raise Exception(f'Error get task from the database {e}')

    def get_add_task(self, request_data):
        """Добавить задачу"""
        try:
            if 'title' not in request_data:
                return False
            title = request_data['title']
            description = request_data.get('description', "")
            sql = "INSERT INTO tasks(title, description) VALUES(?, ?)"
            creat_task = self.__cursor.execute(sql, (title, description))
            self.__database.commit()
            task_id = creat_task.lastrowid
            return True, task_id
        except sqlite3.Error as e:
            raise Exception(f'Error add tasks {e}')

    def get_update_task(self, task_id, request_data):
        """Обновить задачу"""
        try:
            fields = ''
            for key, value in request_data.items():
                fields += f'{key}="{value}", '
            # Убираем лишнюю запятую
            fields = fields[:-2]
            sql = f'UPDATE tasks SET {fields} WHERE id={task_id}'
            RequestDataBase.sql_query_commit(self, sql)
            return True
        except sqlite3.Error as e:
            raise Exception(f'Error update task {e}')

    def get_delete_task(self, task_id):
        """Удалить задачу"""
        try:
            sql = f'DELETE FROM tasks WHERE id={task_id}'
            RequestDataBase.sql_query_commit(self, sql)
            return True
        except sqlite3.Error as e:
            raise Exception(f'Error delete {e}')

    def add_user(self, username, hash_password):
        """Добавить пользователя"""
        try:
            sql = "INSERT INTO users(username, password) VALUES(?, ?)"
            self.__cursor.execute(sql, (username, hash_password))
            self.__database.commit()
            return True
        except sqlite3.Error as e:
            raise Exception(f'Error add user {e}')

    def get_user(self, user_id):
        """Получение пользователя по id"""
        try:
            self.__cursor.execute(f'SELECT * FROM users WHERE id="{user_id}"')
            result = self.__cursor.fetchone()
            if not result:
                return jsonify({'error': 'No user'}), 401
            return result
        except sqlite3.Error as e:
            return jsonify({'error': f'Bad request {e}'}), 400

    def get_user_by_username(self, username):
        """Получение пользователя по username"""
        try:
            self.__cursor.execute(
                f'SELECT * FROM users WHERE username="{username}"'
            )
            result = self.__cursor.fetchone()
            if not result:
                return False
            return result
        except sqlite3.Error as e:
            raise Exception(f'Error get user {e}')
