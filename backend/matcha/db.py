import click
import json

from flask import current_app, g
from flask.cli import with_appcontext

from sqlalchemy import create_engine, text
from werkzeug.security import generate_password_hash

#from sqlalchemy_utils import functions


#def check_db_connection(url):
    #for i in range(5):
        #print(f'Checking db... attempt {i}')
        #result = functions.database_exists(url)
        #if result:
            #print('Connection established')
            #return True
    #print("Database not available")
    #return False


def get_engine():
    if 'engine' not in g:
        g.engine = create_engine(
            current_app.config['DATABASE'],
            isolation_level='AUTOCOMMIT',
            client_encoding='utf8',
            echo=True)

    return g.engine


def close_engine(e=None):
    engine = g.pop('engine', None)

    if engine is not None:
        engine.dispose()


def init_db():
    engine = get_engine()

    with engine.connect() as conn:
        with current_app.open_resource('schema.sql') as f:
            query = text(f.read().decode('utf8'))
            conn.execute(query)


def init_db_contents():
    engine = get_engine()

    with current_app.open_resource('data.json') as f:
        data = json.loads(f.read().decode('utf-8'))
        for user in data['users']:
            engine.execute(
                text('INSERT INTO Users (user_name, password) VALUES (:u, :p)'),
                u=user['user_name'], p=generate_password_hash(user['password'])
            )
            click.echo(f'Created user {user["user_name"]}')


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database')


@click.command('init-db-contents')
@with_appcontext
def init_db_contents_command():
    """Fill in data in fresh database"""
    init_db_contents()
    click.echo('Initialized the database contents')


def init_app(app):
    app.teardown_appcontext(close_engine)
    app.cli.add_command(init_db_command)
    app.cli.add_command(init_db_contents_command)
