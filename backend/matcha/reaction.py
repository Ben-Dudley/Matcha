from flask import Blueprint, request, current_app as app
from sqlalchemy import text

from .db import get_engine

bp = Blueprint('reaction', __name__, url_prefix='/reaction')


@bp.route('', methods=('GET', 'POST', 'PUT'))
def reaction():
    content = request.json
    user_name = content['user_name']

    app.logger.info(f'user_name - {user_name}')

    if request.method == 'GET':
        engine = get_engine()

        result = engine.execute(
            text('SELECT Users.user_name, Reactions.reaction FROM Users JOIN Reactions '
                 'ON Users.user_id = Reactions.admirer_id '
                 'WHERE Reactions.user_id = (SELECT user_id FROM Users WHERE user_name = :u)'),
            u=user_name
        ).fetchall()

        users = []
        for row in result:
            users.append({"name": row['user_name'], "reaction": row['reaction']})

        return {"users": users}, 200
    elif request.method == 'POST':
        admirer_name = content['admirer_name']
        react = content['reaction']

        app.logger.info(f'admirer - {admirer_name}')
        app.logger.info(f'reaction - {react}')

        if not user_name:
            return 'user_name is required', 400
        if not admirer_name:
            return 'admirer_name is required', 400
        if not isinstance(react, bool):
            return 'Reaction is of type boolean', 400

        engine = get_engine()
        # TODO add relation check

        engine.execute(
            text('INSERT INTO Reactions (user_id, admirer_id, reaction) VALUES ('
                 '(SELECT user_id from Users WHERE user_name=:u),'
                 '(SELECT user_id from Users WHERE user_name=:a),'
                 ':r)'),
            u=user_name, a=admirer_name, r=react
        )
        return 'Reaction entry is created', 201
    elif request.method == 'PUT':
        admirer_name = content['admirer_name']
        react = content['reaction']

        app.logger.info(f'reaction - {react}')
        app.logger.info(f'admirer - {admirer_name}')

        if not admirer_name:
            return 'admirer_name is required', 400

        engine = get_engine()
        engine.execute(
            text('UPDATE Reactions SET reaction = :r WHERE '
                 'user_id = (SELECT user_id FROM Users WHERE user_name = :u) AND '
                 'admirer_id = (SELECT user_id FROM Users WHERE user_name = :a)'),
            u=user_name, a=admirer_name, r=react
        )
        return 'Reaction updated', 200

    return 405
