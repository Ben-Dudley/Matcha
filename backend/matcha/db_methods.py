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

def update_profile(engine, user_id, gender, preference, biography, interests):
    engine.execute(
        text('UPDATE Users SET gender = :g, preference = :p, biography = :b WHERE user_id = :u'),
        u=user_id, g=gender, p=preference, b=biography
    )

    # TODO need policy to clear unused tags

    # construct list of ids for incoming data
    interest_rows = []
    for item in interests:
        result = engine.execute(
            text('SELECT interest_id FROM Interests WHERE name = :n'),
            n=item
        ).fetchone()
        if result is None:
            # add new entry
            result = engine.execute(
                text('INSERT INTO Interests (name) VALUES (:n) RETURNING interest_id'),
                n=item
            ).fetchone()
            interest_rows.append((user_id, result["interest_id"]))
        else:
            interest_rows.append((user_id, result['interest_id']))

    # clear all relations and add new
    # TODO think of other ways to remove extra work
    engine.execute(
        text('DELETE FROM UserInterestRelation WHERE user_id = :u; '
             f'INSERT INTO UserInterestRelation VALUES {str(interest_rows)[1:-1]}'),
        u=user_id
    )

