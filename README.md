# Husk

---
1. Проведен рефакторинг кода.
2. Добавлен новый функционал:
    * Добавлена возможность редактировать задачи.
    * Реализована простая система аутентификации пользователей.
3. Интегрирована SQLite база данных для хранения задач.
4. Написана краткая документация к API.

---

## Технологии

- Python
- Flask
- SQLAlchemy

---
### Запуск
<details> 
<summary> Подробнее </summary>

- Установите и активируйте виртуальное окружение
- Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
``` 

<details> <summary> Шаблон наполнения .env </summary>

```
FLASK_APP=app
FLASK_ENV=development
FLASK_DEBUG=true

SECRET_KEY = 'hfoi7y2btb2trfdsfsfs2pb9fyb2b893YRNWPRYbypyrnpyBYRb8yNPy'
```
</details>

- Запустите веб-сервер:
```
flask run
```

</details>

---

## Примеры запросов

Регистрация пользователя
```
POST http://127.0.0.1:5000/todo/api/v1.0/auth/signup
```
Пример запроса:
```
{
    "username": "realm",
    "password": "92fsdgsgs7"
    }
```
Примеры ответа:
```
{"signup": "Successful"}
```
```
{"error": "User is registered"}
```
```
{"error": "Fields are not filled in correctly"}
```
Авторизация
```
POST http://127.0.0.1:5000/todo/api/v1.0/auth/login
```
Пример запроса:
```
{
    "username": "realm",
    "password": "92fsdgsgs7"
    }
```
Примеры ответа:
```
{"auth": "User realm is authorized"}
```
```
{"error": "User not found"}
```
```
{"error": "Invalid password"}
```
Запрос состояния пользователя
```
GET http://127.0.0.1:5000/todo/api/v1.0/auth/login
```
Примеры ответа:
```
{"auth": "User is not authorized"}
```
```
{"auth": "User realm is authorized"}
```

Выход из пользователя (доступна только авторизованным)
```
POST http://127.0.0.1:5000/todo/api/v1.0/auth/logout
```
Примеры ответа:
```
{"auth": "User is unauthorized"}
```


Создание публикации

```
POST http://127.0.0.1:5000/todo/api/v1.0/tasks
```

Пример запроса:

```
{
    "description": "22effft1",
    "title": "Read a book 2"
  }
```

Пример ответа:

```
[
    {
        "description": "22effft1",
        "done": 0,
        "id": 42,
        "title": "Read a book 2"
    }
]
```
```
{"error": "Bad request"}
```

Получение всех задач

```
GET http://127.0.0.1:5000/todo/api/v1.0/tasks
```

Пример ответа:

```
{
    "tasks": [
        {
            "description": "22est1",
            "done": 0,
            "id": 3,
            "title": "Read 3"
        },
        {
            "description": "22eTest1",
            "done": 1,
            "id": 5,
            "title": "Read 2"
        }
    ]
}
```
```
{"error": "Not tasks"}
```

Получение одной задачи

```
GET http://127.0.0.1:5000/todo/api/v1.0/tasks/12
```

Пример ответа:

```
{
    "task": [
        {
            "description": "226eTest1",
            "done": 0,
            "id": 14,
            "title": "Read 3"
        }
    ]
}
```

Изменение задачи (изменение названия, описания или статуса выполнения)

```
PUT http://127.0.0.1:5000/todo/api/v1.0/tasks/14
```

Пример запроса:

```
{
    "description": "Tefst",
    "title": "Read a bbvvvook 2",
    "done": "1"
  }
```
```
{
    "description": "Tefst",
    "done": "1"
  }
```
```
{
    "title": "Read a bbvvvook 2"
  }
```

Пример ответа:

```
{
    "task": [
        {
            "description": "Tefst",
            "done": 1,
            "id": 14,
            "title": "Read a bbvvvook 2"
        }
    ]
}
```
```
{"error": "Not found task"}
```


Удаление задачи

```
DELETE http://127.0.0.1:5000/todo/api/v1.0/tasks/14
```

Пример ответа:

```
{"result": "Task delete"}
```
```
{"error": "Not found task"}
```
