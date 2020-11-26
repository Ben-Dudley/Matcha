from sqlalchemy import text
from .db import get_engine


def get_user_id(user_name):
    engine = get_engine()

    result = engine.execute(
        text('SELECT user_id FROM Users WHERE user_name = :u'),
        u=user_name
    ).fetchone()

    if result is not None:
        return result['user_id']

# TODO create methods for user registration
