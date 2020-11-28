from flask import Blueprint, request, current_app as app
from werkzeug.security import check_password_hash
from sqlalchemy import text

from .db import get_engine
from .db_methods import register_user, get_user_id, update_profile

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
            return {'message': 'Incorrect user_name'}, 400
        elif not check_password_hash(user['password'], password):
            return {'message': 'Incorrect password'}, 400

        return {'message': 'Successful login'}, 200
    return 405


@bp.route('/register', methods=('POST', 'DELETE'))
def register():
    content = request.json
    user_name = content['user_name']
    password = content['password']
    email = content['email']
    last_name = content['last_name']
    first_name = content['first_name']

    app.logger.info(f'user_name - {user_name}')
    app.logger.info(f'password - {password}')
    app.logger.info(f'first_name - {first_name}')
    app.logger.info(f'last_name - {last_name}')
    app.logger.info(f'email - {email}')

    if not user_name:
        return {'message': 'user_name is required'}, 400
    elif not password:
        return {'message': 'password is required'}, 400

    engine = get_engine()

    # check if user already exists
    result = get_user_id(engine, user_name)
    if request.method == 'POST':
        if result.fetchone() is not None:
            return 'User is already registered', 400

        register_user(engine, user_name, password, first_name, last_name, email)
        return {'message': 'User registered successfully'}, 201
    elif request.method == 'DELETE':
        user = result.fetchone()
        if user is not None:
            if not check_password_hash(user['password'], password):
                return {'message': 'Incorrect password'}, 400
            engine.execute(
                text('DELETE FROM Users WHERE user_name = :u'),
                u=user_name
            )
        return {'message': 'User does not exist'}, 200
    return 405


@bp.route('/profile', methods=('PUT', 'GET'))
def profile():
    content = request.json
    user_name = content['user_name']
    app.logger.info(f'user_name - {user_name}')

    engine = get_engine()

    # check if user exists
    user_id = get_user_id(engine, user_name)
    if user_id is None:
        return {'message': f'user_name {user_name} not found'}, 400

    if request.method == 'GET':
        result = engine.execute(
            text('SELECT first_name, last_name, email, gender, preference, biography FROM Users WHERE user_id = :u'),
            u=user_id
        ).fetchone()
        user_profile = {"user": dict(result)}

        result = engine.execute(
            text('SELECT I.name FROM Interests I JOIN UserInterestRelation R ON R.interest_id = I.interest_id '
                 'JOIN Users U on R.user_id = U.user_id WHERE U.user_id = :u'),
            u=user_id
        ).fetchall()

        user_profile["user"]["interests"] = [r["name"] for r in result]
        return {user_profile}, 200
    else:
        gender = content['gender']
        preference = content['preference']
        biography = content['biography']
        interests = content['interests']

        app.logger.info(f'gender - {gender}')
        app.logger.info(f'preference - {preference}')
        app.logger.info(f'biography - {biography}')
        app.logger.info(f'interests:')
        for item in interests:
            app.logger.info(f'- {item}')

        update_profile(engine, user_id, gender, preference, biography, interests)
        return {'message': f'profile of {user_name} is updated'}, 200
