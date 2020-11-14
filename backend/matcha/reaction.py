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
    UNLIKE = 3
    CONNECTION = 4

    @classmethod
    def get(cls, react):
        for item in cls:
            if react == item.name.lower():
                return item

    @classmethod
    def get_from_int(cls, react):
        for item in cls:
            if react == item.value:
                return item


def get_reaction(engine, user_id, target_id):
    result = engine.execute(
        text('SELECT reaction FROM Reactions WHERE user_id = :u AND target_id = :t'),
        u=user_id, t=target_id
    ).fetchone()
    if result is not None:
        app.logger.info(f'db_reaction1 - {result["reaction"]}')
        return Reaction.get_from_int(result['reaction'])


def update_reaction(engine, user_id, target_id, react):
    engine.execute(
        text('UPDATE Reactions SET reaction = :r WHERE user_id = :u AND target_id = :t'),
        u=user_id, t=target_id, r=react
    )


def get_reaction_list(engine, user_id, react):
    result = engine.execute(
        text('SELECT Users.user_name FROM Users JOIN Reactions '
             'ON Users.user_id = Reactions.target_id '
             'WHERE Reactions.user_id = :u AND Reactions.reaction = :r'),
        u=user_id, r=react
    ).fetchall()

    users = []
    for row in result:
        users.append({"name": row['user_name']})

    return users


@bp.route('', methods=('GET', 'PUT'))
def reaction():
    if request.method == 'GET':

        content = request.json
        entity = content['entity']
        user_name = content['user_name']
        react = content['reaction']

        if not user_name:
            return 'user_name is required', 400
        if not entity:
            return f'entity field is required', 400
        if not react:
            return f'reaction field is required', 400

        app.logger.info(f'user_name - {user_name}')
        app.logger.info(f'entity - {entity}')
        app.logger.info(f'reaction - {react}')

        user_id = db_methods.get_user_id(user_name)
        react = Reaction.get(content['reaction'])

        if user_id is None:
            return f'user_name {user_name} not found', 400
        if react is None:
            return f'reaction field is not valid', 400

        engine = get_engine()

        if entity == 'user':
            # User requests data about his view, likes, chat list
            result = engine.execute(
                text('SELECT Users.user_name FROM Users JOIN Reactions ON Users.user_id = Reactions.target_id '
                     'WHERE Reactions.user_id = :u AND Reactions.reaction = :r'),
                u=user_id, r=react.value
            ).fetchall()

            users = []
            for row in result:
                users.append({"name": row['user_name']})

            return {"users": users}, 200
        elif entity == 'target':
            # Server requests data about views, likes and chat list for target user
            result = engine.execute(
                text('SELECT Users.user_name FROM Users JOIN Reactions ON Users.user_id = Reactions.user_id '
                     'WHERE Reactions.target_id = :t AND Reactions.reaction = :r'),
                t=user_id, r=react.value
            ).fetchall()

            users = []
            for row in result:
                users.append({"name": row['user_name']})

            return {"users": users}, 200
        else:
            return 'wrong entity', 400
        # TODO User requests data about block list
    else:

        content = request.json
        user_name = content['user_name']
        react = content['reaction']
        target_name = content['target_name']

        if not user_name:
            return 'user_name is required', 400
        if not target_name:
            return f'target_name field is required', 400
        if not react:
            return f'reaction field is required', 400

        app.logger.info(f'user_name - {user_name}')
        app.logger.info(f'reaction - {react}')

        user_id = db_methods.get_user_id(user_name)
        target_id = db_methods.get_user_id(target_name)
        react = Reaction.get(content['reaction'])

        if user_id is None:
            return f'user_name {user_name} not found', 400
        if target_id is None:
            return f'target_name {user_name} not found', 400
        if react is None:
            return f'reaction field is not valid', 400

        engine = get_engine()

        if react == Reaction.VIEW:
            # create entry with View
            engine.execute(
                text('INSERT INTO Reactions (user_id, target_id, reaction, block) VALUES (:u, :t, :r, false)'),
                u=user_id, t=target_id, r=Reaction.VIEW.value
            )
            return 'Reaction entry is created', 201
        elif react == Reaction.LIKE:
            # check if target likes back
            db_reaction = get_reaction(engine, target_id, user_id)
            if db_reaction is not None and db_reaction == Reaction.LIKE:
                engine.execute(
                    text('UPDATE Reactions SET reaction = :r WHERE user_id = :u AND target_id = :t;'
                         'UPDATE Reactions SET reaction = :r WHERE user_id = :t AND target_id = :u'),
                    u=user_id, t=target_id, r=Reaction.CONNECTION.value
                )
                return 'Both user and target are upgraded to CONNECTION', 200
            # Set user to Like
            update_reaction(engine, user_id, target_id, Reaction.LIKE.value)
            return 'User upgraded to LIKE', 200
        elif react == Reaction.UNLIKE:
            # set user to View
            update_reaction(engine, user_id, target_id, Reaction.VIEW.value)
            # check if target has connection
            db_reaction = get_reaction(engine, target_id, user_id)
            app.logger.info(f'db_reaction - {db_reaction}')
            if db_reaction is not None and db_reaction == Reaction.CONNECTION:
                # set target to Like
                update_reaction(engine, target_id, user_id, Reaction.LIKE.value)
                return 'User downgraded to VIEW, target downgrade to LIKE', 200
            return 'User downgraded to VIEW', 200
        else:
            pass
