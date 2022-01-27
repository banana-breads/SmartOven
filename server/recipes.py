from flask import request, jsonify
from flask import (Blueprint)
from bson import json_util, ObjectId
from .db import get_db
import json

bp = Blueprint('recipes', __name__, url_prefix='/recipe')


def add_recipe(recipe_name, time, details, temperature):
    db = get_db()
    recipes = db.recipes
    recipe = {"name": recipe_name, "prep_time": time, "prep_details": details, "baking_temperature": temperature}
    result = recipes.insert_one(recipe)
    return result.inserted_id

def get_recipes():
    db = get_db()
    return {"message": "Working"}


@bp.route('/', methods=['GET', 'POST'])
def manage_recipes():
    # print(request.json)
    if request.method == "GET":
        return "Recipe GET"
    if request.method == 'POST':
        recipe_id = add_recipe(request.json['name'], request.json['time'], request.json['details'], request.json['temperature'])
        # print(f"Recipe: {recipe_id}")
        return json.loads(json_util.dumps({"message": "Success", "id": recipe_id}))
