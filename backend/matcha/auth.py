from flask import Blueprint, request, current_app as app
from werkzeug.security import check_password_hash, generate_password_hash
from .db import get_engine
from sqlalchemy import text

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        content = request.json
        username = content['username']
        password = content['password']

        app.logger.info(f'username - {username}')
        app.logger.info(f'password - {password}')

        if not username:
            return 'Username is required', 501
        elif not password:
            return 'Password is required', 501
        engine = get_engine()

        result = engine.execute(
            text('SELECT user_id FROM Users WHERE username = :u'),
            u=username
        )
        if result.fetchone() is not None:
            return 'User is already registered', 501

        engine.execute(
            text('INSERT INTO Users (username, password) VALUES (:u, :p)'),
            u=username, p=generate_password_hash(password)
        )
        return 'User registered successfully', 200

    return '', 401
