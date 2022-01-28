from flask import request, jsonify
from flask import (Blueprint)
from bson import json_util
from bson.objectid import ObjectId
from db import get_db
import json

bp = Blueprint('recipes', __name__, url_prefix='/recipe')

def add_recipe(recipe_name, time, details, temperature):
    db = get_db()
    recipes = db.recipes
    recipe_name = recipe_name.replace(" ", "-")
    recipe = {'name': recipe_name, 'prep_time': time, 'prep_details': details, 'baking_temperature': temperature}
    result = recipes.insert_one(recipe)
    return result.inserted_id

def get_recipes():
    db = get_db()
    recipes = db.recipes
    all_recipes = recipes.find({}, {'_id': 0})
    return json_util.dumps(list(all_recipes))

@bp.route('/', methods=['GET', 'POST'])
def manage_recipes():
    if request.method == "GET":
        return get_recipes()

    if request.method == 'POST':
        recipe_id = add_recipe(request.json['name'], request.json['prep_time'], request.json['prep_details'], request.json['baking_temperature'])
        return json.loads(json_util.dumps({'message': 'Success', 'id': recipe_id}))

@bp.route('/<recipe_name>', methods=['GET'])
def get_recipe(recipe_name=None):
    db = get_db()
    recipes = db.recipes
    my_recipe = recipes.find_one({'name': recipe_name}, {'_id': 0})
    if my_recipe is None:
        return {"message": f"No {recipe_name} recipe"}
    return my_recipe


@bp.route('/<recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id=None):
    db = get_db()
    recipes = db.recipes
    recipes.delete_one({'_id': ObjectId(recipe_id)})
    return jsonify({"message": f"Deleted recipe with id {recipe_id}"})

@bp.route('/<recipe_id>', methods=['PUT'])
def update_recipe(recipe_id=None):
    db = get_db()
    recipes = db.recipes
    updated_recipe = request.json
    recipes.update_one({'_id': ObjectId(recipe_id)}, {"$set": updated_recipe})
    return jsonify({"message": f"Updated recipe with id {recipe_id}"})