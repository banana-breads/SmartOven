from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from db import get_db
from mqtt_shared import mqtt_manager
from recipes import get_one_recipe

bp = Blueprint('ovens', __name__, url_prefix='/oven')

"""
Manage oven state (True if oven is on, False otherwise)
Oven will start preparing food according to its given settings.
"""
@bp.route("/oven/<oven_id>/state", methods=['POST'])
def set_oven_state(oven_id=None, new_state=False):
    print(oven_id, new_state)
    body = request.json
    if body is None or not body.get('state'):
        return jsonify({ 'message': f'Missing state parameter. No action taken on oven {oven_id}.' }), 400


    if not check_if_oven_exists(oven_id):
        return jsonify({"message": f"Oven with id {oven_id} does not exist. Cannot modify state."}), 404
    
    mqtt_manager.publish_message(f"/oven/{oven_id}/state", jsonify.dumps({"state":new_state}))

    new_state = body['state']
    result = ""
    if new_state == True:
        result = f"Oven with id {oven_id} has started cooking."
    else:
        result = f"Oven with id {oven_id} has stopped cooking."
    return jsonify({"message": result}), 200

"""
Sets the oven to the cooking parameters specified in the recipe (cooking temperature, cooking time).
"""
@bp.route("/oven/<oven_id>/setRecipe/<recipe_name>", methods=['POST'])
def set_oven_recipe(oven_id=None, recipe_name=None):
    if not check_if_oven_exists(oven_id):
        return jsonify({"message": f"Oven with id {oven_id} does not exist. Cannot set recipe."}), 404

    recipe = get_one_recipe(recipe_name)

    if not recipe:
        return jsonify({"message": f"Recipe '{recipe_name}' does not exist. Cannot set recipe."}), 404

    mqtt_manager.publish_message(f"/oven/{oven_id}/setRecipe", jsonify.dumps({"state":new_state}))

    return jsonify({"message":"Success"}), 200

"""
Manually sets the oven temperature (in Celsius).
"""
@bp.route("/oven/<oven_id>/setTemperature", methods=['POST'])
def set_oven_temperature(oven_id=None, recipe_name=None):
    body = request.json
    if body is None or not body.get('temperature'):
        return jsonify({ 'message': f'Missing temperature parameter. No action taken on oven {oven_id}.' }), 400
    temperature = body["temperature"]

    if not check_if_oven_exists(oven_id):
        return jsonify({"message": f"Oven with id {oven_id} does not exist. Cannot set temperature."}), 404

    mqtt_manager.publish_message(f"/oven/{oven_id}/setTemperature", jsonify.dumps({"temperature":temperature}))

    return jsonify({"message":"Success"}), 200

"""
Manually sets the oven time (in minutes).
"""
@bp.route("/oven/<oven_id>/setTime", methods=['POST'])
def set_oven_time(oven_id=None, recipe_name=None):
    body = request.json
    if body is None or not body.get('temperature'):
        return jsonify({ 'message': f'Missing time parameter. No action taken on oven {oven_id}.' }), 400
    time = body["time"]

    if not check_if_oven_exists(oven_id):
        return jsonify({"message": f"Oven with id {oven_id} does not exist. Cannot set time."}), 404

    mqtt_manager.publish_message(f"/oven/{oven_id}/setTime", jsonify.dumps({"time":time}))

    return jsonify({"message":"Success"}), 200



def check_if_oven_exists(oven_id):
    device_ids = [x.id for x in connected_devices]
    if oven_id not in device_ids:
        return False
    return True
