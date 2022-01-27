from flask import request, jsonify
from flask import (Blueprint)
from bson import json_util
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

def delete_recipes(recipe_name):
    db = get_db()
    recipes = db.recipes
    delete_result = recipes.delete_many({'name': recipe_name})
    return delete_result.deleted_count

@bp.route('/', methods=['GET', 'POST', 'DELETE'])
def manage_recipes():

    if request.method == "GET":
        if request.json and 'name' in request.json:
            return get_recipe(request.json['name'])
        return get_recipes()

    if request.method == 'POST':
        recipe_id = add_recipe(request.json['name'], request.json['time'], request.json['details'], request.json['temperature'])
        return json.loads(json_util.dumps({'message': 'Success', 'id': recipe_id}))

    if request.method == 'DELETE':
        if request.json and 'name' in request.json:
            recipe_name = request.json['name']
            deleted_count = delete_recipes(recipe_name)
            return jsonify({"message": f"Deleted {deleted_count} {recipe_name} recipes"})
        else:
            return jsonify({"message": "Delete request body should contain recipe's name"}), 422
