from flask import request, jsonify
from flask import (Blueprint)
from bson import json_util
from bson.objectid import ObjectId
from .db import get_db
import json

bp = Blueprint('recipes', __name__, url_prefix='/recipe')


def add_recipe(recipe_name, time, details, temperature):
    db = get_db()
    recipes = db.recipes
    recipe = {'name': recipe_name, 'prep_time': time, 'prep_details': details, 'baking_temperature': temperature}
    result = recipes.insert_one(recipe)
    return result.inserted_id

def get_recipes():
    db = get_db()
    recipes = db.recipes
    all_recipes = recipes.find({}, {'_id': 0})
    return json_util.dumps(list(all_recipes))

def get_recipe(recipe_name):
    db = get_db()
    recipes = db.recipes
    my_recipe = recipes.find_one({'name': recipe_name}, {'_id': 0})
    return my_recipe

@bp.route('/', methods=['GET', 'POST'])
def manage_recipes():

    if request.method == "GET":
        if request.json and 'name' in request.json:
            return get_recipe(request.json['name'])
        return get_recipes()

    if request.method == 'POST':
        recipe_id = add_recipe(request.json['name'], request.json['time'], request.json['details'], request.json['temperature'])
        return json.loads(json_util.dumps({'message': 'Success', 'id': recipe_id}))

@bp.route('/<recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id=None):
    db = get_db()
    recipes = db.recipes
    recipes.delete_one({'_id': ObjectId(recipe_id)})
    return jsonify({"message": f"Deleted recipe with id {recipe_id}"})
