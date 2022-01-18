from flask import request
from flask import (Blueprint)
from .db import get_db

bp = Blueprint('recipes', __name__, url_prefix='/recipe')


def add_recipe(recipe_name, time, details, temperature):
    return 0


@bp.route('/')
def get_recipes():
    database = get_db()
    return {"message": "Working"}


@bp.route('/', methods=['POST'])
def manage_recipes():
    if request.method == 'POST':
        return add_recipe(request.form['name'], request.form['time'], request.form['details'], request.form['temperature'])
