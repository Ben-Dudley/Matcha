from flask import Blueprint, request, current_app as app
from sqlalchemy import text

from enum import Enum, unique
from .db import get_engine
from . import db_methods

bp = Blueprint('reaction', __name__, url_prefix='/reaction')


@unique
class Reaction(Enum):
    VIEW = 1
    LIKE = 2
    CONNECTION = 3


def check_reaction(engine, user_id, target_id):
    result = engine.execute(
        text('SELECT reaction FROM Reactions WHERE user_id = :u AND target_id = :t'),
        u=user_id, t=target_id
    ).fetchone()
    return result


def update_reaction(engine, user_id, target_id, react):
    engine.execute(
        text('UPDATE Reactions SET reaction = :r WHERE user_id = :u AND target_id = :t'),
        u=user_id, t=target_id, r=react
    )


def update_both_reactions(engine, user_id, target_id, react):
    engine.execute(
        text('UPDATE Reactions SET reaction = :r WHERE user_id = :u AND target_id = :t;'
             'UPDATE Reactions SET reaction = :r WHERE user_id = :t AND target_id = :u'),
        u=user_id, t=target_id, r=react
    )


@bp.route('', methods=('GET', 'PUT'))
def reaction():
    content = request.json
    user_name = content['user_name']

    if not user_name:
        return 'user_name is required', 400

    app.logger.info(f'user_name - {user_name}')

    engine = get_engine()

    user_id = db_methods.get_user_id(user_name)
    if user_id is None:
        return f'user_name {user_name} not found', 400

    if request.method == 'GET':
        result = engine.execute(
            text('SELECT Users.user_name, Reactions.reaction FROM Users JOIN Reactions '
                 'ON Users.user_id = Reactions.target_id WHERE Reactions.user_id = :u'),
            u=user_id
        ).fetchall()

        targets = []
        for row in result:
            targets.append({"name": row['user_name'], "reaction": row['reaction']})

        return {"targets": targets}, 200
    else:
        target_name = content['target_name']
        react = content['reaction']

        if not target_name:
            return 'target_name is required', 400
        if not react:
            return 'reaction is required', 400

        app.logger.info(f'target - {target_name}')
        app.logger.info(f'reaction - {react}')

        target_id = db_methods.get_user_id(target_name)
        if target_id is None:
            return f'target_name {target_name} not found', 400
        elif react != Reaction.VIEW.value and react != Reaction.LIKE.value:
            return f'Cannot update reaction with value {react}', 400

        result = check_reaction(engine, user_id, target_id)
        if result is None:
            if react == Reaction.VIEW.value:
                engine.execute(
                    text('INSERT INTO Reactions (user_id, target_id, reaction) VALUES (:u, :t, :r)'),
                    u=user_id, t=target_id, r=Reaction.VIEW.value
                )
                return 'Reaction entry is created', 201
            else:
                return 'Cant update like without preexisting view', 400
        else:
            db_react = result['reaction']
            if db_react == react:
                return 'Reaction already exists', 200
            if react == Reaction.VIEW.value:
                update_reaction(engine, user_id, target_id, Reaction.VIEW.value)
                if db_react == Reaction.CONNECTION.value:
                    update_reaction(engine, target_id, user_id, Reaction.LIKE.value)
                return 'Reaction updated', 200
            else:
                result = check_reaction(engine, target_id, user_id)
                if result is None or result['reaction'] == Reaction.VIEW.value:
                    update_reaction(engine, user_id, target_id, Reaction.LIKE.value)
                    return 'Reaction entry is updated', 201
                else:
                    update_both_reactions(engine, user_id, target_id, Reaction.CONNECTION.value)
                    return 'Both user and target reactions are updated', 200
