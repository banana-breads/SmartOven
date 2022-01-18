import bson
import click
from flask import current_app, g
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
from flask.cli import with_appcontext

def get_db():
    if 'database' in g:
        return g.database
        #db = getattr(g, "_database", None)

    #if db is None:
    db = g.database = PyMongo(current_app).db

    database = db.smart_oven
    return database
    
def close_db(e=None):
    db = g.pop('_database', None)

def init_db():
    db = get_db()

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database")

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)