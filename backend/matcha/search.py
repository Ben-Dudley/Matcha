from flask import Blueprint, request, current_app as app
from sqlalchemy import text

from .db import get_engine
from .db_methods import get_user_id

bp = Blueprint('search', __name__, url_prefix='/search')

@bp.route('', methods=('GET',))
def search():
    content = request.json
    user_name = content['user_name']
    interests = content['interests']

    app.logger.info(f'user_name - {user_name}')
    app.logger.info(f'interests:')
    for item in interests:
        app.logger.info(f'- {item}')

    if not user_name:
        return {'message': 'user_name is required'}, 400

    engine = get_engine()

    # check if user exists
    user_id = get_user_id(engine, user_name)
    if user_id is None:
        return {'message': f'user_name {user_name} not found'}, 400

    search_result = {}
    for item in interests:
        result = engine.execute(
            text('SELECT Users.user_name FROM Users '
                 'JOIN UserInterestRelation ON Users.user_id = UserInterestRelation.user_id '
                 'JOIN Interests ON UserInterestRelation.interest_id = Interests.interest_id '
                 'WHERE Interests.name = :i AND Users.user_id != :u'),
            i=item, u=user_id
        ).fetchall()

        for row in result:
            name = row['user_name']
            if name in search_result:
                search_result[name] += 1
            else:
                search_result[name] = 1

    app.logger.info(search_result)
    sorted_list = sorted(search_result, key=search_result.get, reverse=True)
    return {'users': sorted_list}, 200
