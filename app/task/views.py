from flask import jsonify, request, Blueprint
from flask_login import (login_required)
from flask_marshmallow import Marshmallow

from app.request_data_base import (get_add_task, get_task_detail, get_tasks,
                                   get_update_task, get_delete_task)

blueprint = Blueprint('task', __name__, url_prefix='/todo/api/v1.0/tasks')
ma = Marshmallow(blueprint)


class TasksSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "description", "done")


task_schema = TasksSchema()
tasks_schema = TasksSchema(many=True)


@blueprint.route('', methods=['GET', 'POST'])
@login_required
def get_create_tasks():
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


@blueprint.route('/<int:task_id>',
                 methods=['GET', 'PUT', 'DELETE'])
@login_required
def get_update_delete_task(task_id):
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
