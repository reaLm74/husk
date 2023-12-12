from flask import Blueprint, jsonify, request
from flask_login import (current_user, login_user, login_required,
                         logout_user)

from app.request_data_base import (get_user_by_username, add_user)
from app.user.models import Users

blueprint = Blueprint('user', __name__, url_prefix='/todo/api/v1.0/auth')


@blueprint.route('/signup', methods=['POST'])
def signup():
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


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
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


@blueprint.route('/logout', methods=['POST'])
@login_required
def logout():
    try:
        logout_user()
        return jsonify({'auth': f'User is unauthorized'}), 200
    except Exception as e:
        return jsonify({'error': f'Error logout user {str(e)}'}), 404
