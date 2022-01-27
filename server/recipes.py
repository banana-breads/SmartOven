from flask import request
from flask import (Blueprint)
from .db import get_db

bp = Blueprint('recipes', __name__, url_prefix='/recipe')


def add_recipe(recipe_name, time, details, temperature):
    db = get_db()
    recipes = db.recipes
    recipe = {"name": recipe_name, "prep_time": time, "prep_details": details, "baking_temperature": temperature}
    recipes.insert_one(recipe)


def get_recipes():
    db = get_db()
    return {"message": "Working"}


@bp.route('/', methods=['POST'])
def manage_recipes():
    print("Hello")
    print(request.method)
    if request.method == 'POST':
        return add_recipe(request.form['name'], request.form['time'], request.form['details'], request.form['temperature'])
