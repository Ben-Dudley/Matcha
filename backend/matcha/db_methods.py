from sqlalchemy import text
from werkzeug.security import generate_password_hash


def get_user_id(engine, user_name):
    result = engine.execute(
        text('SELECT user_id FROM Users WHERE user_name = :u'),
        u=user_name
    ).fetchone()

    if result is not None:
        return result['user_id']


def register_user(engine, user_name, password, first_name, last_name, email):
    engine.execute(
        text('INSERT INTO Users (user_name, password, first_name, last_name, email) VALUES (:u, :p, :f, :l, :e)'),
        u=user_name, p=generate_password_hash(password), f=first_name, l=last_name, e=email
    )
