from flask import Blueprint, request, current_app as app
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import text

from .db import get_engine

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('', methods=('POST',))
def login():
    if request.method == 'POST':
        content = request.json
        user_name = content['user_name']
        password = content['password']

        app.logger.info(f'username - {user_name}')
        app.logger.info(f'password - {password}')
        engine = get_engine()

        user = engine.execute(
            text('SELECT * FROM Users WHERE user_name = :u'),
            u=user_name
        ).fetchone()

        if user is None:
            return 'Incorrect user_name', 400
        elif not check_password_hash(user['password'], password):
            return 'Incorrect password', 400

        return 'Successful login', 200
    return 405


@bp.route('/register', methods=('POST', 'DELETE'))
def register():
    content = request.json
    user_name = content['user_name']
    password = content['password']

    app.logger.info(f'user_name - {user_name}')
    app.logger.info(f'password - {password}')

    if not user_name:
        return 'user_name is required', 400
    elif not password:
        return 'password is required', 400

    engine = get_engine()

    result = engine.execute(
        text('SELECT * FROM Users WHERE user_name = :u'),
        u=user_name
    )
    if request.method == 'POST':
        if result.fetchone() is not None:
            return 'User is already registered', 400

        engine.execute(
            text('INSERT INTO Users (user_name, password) VALUES (:u, :p)'),
            u=user_name, p=generate_password_hash(password)
        )
        return 'User registered successfully', 201
    elif request.method == 'DELETE':
        user = result.fetchone()
        if user is not None:
            if not check_password_hash(user['password'], password):
                return 'Incorrect password', 400
            engine.execute(
                text('DELETE FROM Users WHERE user_name = :u'),
                u=user_name
            )
        return 'User does not exist', 200
    return 405

