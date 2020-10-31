from flask import Blueprint, request, current_app as app
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import text

from .db import get_engine

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('', methods=('POST',))
def login():
    if request.method == 'POST':
        content = request.json
        username = content['username']
        password = content['password']

        app.logger.info(f'username - {username}')
        app.logger.info(f'password - {password}')
        engine = get_engine()

        user = engine.execute(
            text('SELECT * FROM Users WHERE username = :u'),
            u=username
        ).fetchone()

        if user is None:
            return 'Incorrect username', 400
        elif not check_password_hash(user['password'], password):
            return 'Incorrect password', 400

        return 'Successful login', 200


@bp.route('/register', methods=('POST', 'DELETE'))
def register():
    content = request.json
    username = content['username']
    password = content['password']

    app.logger.info(f'username - {username}')
    app.logger.info(f'password - {password}')

    if not username:
        return 'Username is required', 400
    elif not password:
        return 'Password is required', 400

    engine = get_engine()

    result = engine.execute(
        text('SELECT user_id FROM Users WHERE username = :u'),
        u=username
    )
    if request.method == 'POST':
        if result.fetchone() is not None:
            return 'User is already registered', 400

        engine.execute(
            text('INSERT INTO Users (username, password) VALUES (:u, :p)'),
            u=username, p=generate_password_hash(password)
        )
        return 'User registered successfully', 201
    else:
        if result.fetchone() is not None:
            engine.execute(
                text('DELETE FROM Users WHERE username = :u'),
                u=username
            )
        return 'User does not exist', 200
