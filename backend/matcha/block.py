from flask import Blueprint, request, current_app as app
from sqlalchemy import text

from .db import get_engine
from . import db_methods

bp = Blueprint('block', __name__, url_prefix='/block')


@bp.route('', methods=('GET', 'PUT'))
def block_list():
    content = request.json

    user_name = content['user_name']
    app.logger.info(f'user_name - {user_name}')

    engine = get_engine()

    user_id = db_methods.get_user_id(engine, user_name)
    if user_id is None:
        return {'message': f'user_name {user_name} not found'}, 400

    # get list of blocked users
    if request.method == 'GET':
        result = engine.execute(
            text('SELECT Users.user_name FROM Users JOIN Reactions ON Users.user_id = Reactions.target_id '
                 'WHERE Reactions.user_id = :u AND Reactions.block = TRUE'),
            u=user_id
        ).fetchall()
        users = []
        for row in result:
            users.append({"name": row['user_name']})
        return {'content': {'users': users}}, 200
    # update block list
    else:
        target_name = content['target_name']
        block = content['block']
        app.logger.info(f'target_name - {target_name}')
        app.logger.info(f'block - {block}')

        target_id = db_methods.get_user_id(engine, target_name)
        if target_id is None:
            return {'message': f'target_name {target_name} not found'}, 400

        result = engine.execute(
            text('SELECT target_id FROM Reactions WHERE user_id = :u AND target_id = :t'),
            u=user_id, t=target_id
        ).fetchone()
        if result is None:
            return f'No entry for user_name {user_name} and target_name {target_name}', 400
        engine.execute(
            text('UPDATE Reactions SET block = :b WHERE user_id = :u AND target_id = :t'),
            u=user_id, t=target_id, b=block
        )
        return {'message': 'Block value is updated'}
