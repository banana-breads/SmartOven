from flask import Blueprint, request, jsonify
from mqtt_shared import mqtt_manager, mqtt_topics
from recipes import get_one_recipe
from globals import connected_devices


def _check_if_oven_exists(oven_id):
    device_ids = [x.id for x in connected_devices]
    if oven_id not in device_ids:
        return False
    return True


bp = Blueprint('ovens', __name__, url_prefix='/oven')

"""
Manage oven state (True if oven is on, False otherwise)
Oven will start preparing food according to its given settings.
"""
@bp.route("/oven/<oven_id>/state", methods=['POST'])
def set_oven_state(oven_id=None):
    body = request.json
    if body is None or not body.get('state'):
        return jsonify({ 'message': f'Missing state parameter.' \
                        f'No action taken on oven {oven_id}.' }), 400

    if not _check_if_oven_exists(oven_id):
        return jsonify({"message": f"Oven with id {oven_id} does not exist." \
                        " Cannot modify state."}), 404

    new_state = body['state']
    result = ""
    if new_state == True:
        result = f"Oven with id {oven_id} has started cooking."
    elif new_state == False:
        result = f"Oven with id {oven_id} has stopped cooking."
    else:
        return jsonify({"message": f"Bad value. Cannot change state."}), 404

    topic = mqtt_topics.SET_STATE.format(device_id=oven_id)
    mqtt_manager.publish_message(topic, jsonify.dumps({"state": new_state}))

    return jsonify({"message": result}), 200

"""
Sets the oven to the cooking parameters specified in the recipe
(cooking temperature, cooking time).
"""
@bp.route("/oven/<oven_id>/setRecipe/<recipe_name>", methods=['POST'])
def set_oven_recipe(oven_id=None, recipe_name=None):
    if not _check_if_oven_exists(oven_id):
        return jsonify({"message": f"Oven with id {oven_id} does not exist." \
                        " Cannot set recipe."}), 404

    recipe = get_one_recipe(recipe_name)

    if not recipe:
        return jsonify({"message": f"Recipe '{recipe_name}' does not exist." \
                        " Cannot set recipe."}), 404

    topic = mqtt_topics.SET_RECIPE.format(device_id=oven_id)
    mqtt_manager.publish_message(topic, jsonify.dumps({"recipe": recipe}))

    return jsonify({"message":"Success"}), 200

"""
Manually sets the oven temperature (in Celsius).
"""
@bp.route("/oven/<oven_id>/setTemperature", methods=['POST'])
def set_oven_temperature(oven_id=None):
    body = request.json
    if body is None or not body.get('temperature'):
        return jsonify({ 'message': f'Missing temperature parameter.' \
                        'No action taken on oven {oven_id}.' }), 400

    if not _check_if_oven_exists(oven_id):
        return jsonify({"message": f"Oven with id {oven_id} does not exist." \
                        " Cannot set temperature."}), 404

    try:
        temperature = int(body["temperature"])
        if temperature < 0 or temperature > 250:
            return jsonify({"message": f"Oven cannot run on temperatures " \
                " negative or hotter than 250C. Cannot set temperature."}), 404
    except:
        return jsonify({"message": f"Bad value. Cannot set temperature."}), 404

    topic = mqtt_topics.SET_TEMPERATURE.format(device_id=oven_id)
    mqtt_manager.publish_message(topic, jsonify.dumps({"temperature": temperature}))

    return jsonify({"message":"Success"}), 200

"""
Manually sets the oven time (in minutes).
"""
@bp.route("/oven/<oven_id>/setTime", methods=['POST'])
def set_oven_time(oven_id=None):
    body = request.json
    if body is None or not body.get('time'):
        return jsonify({ 'message': f'Missing time parameter.' \
                        ' No action taken on oven {oven_id}.' }), 400
    if not _check_if_oven_exists(oven_id):
        return jsonify({"message": f"Oven with id {oven_id} does not exist." \
                        " Cannot set time."}), 404

    try:
        time = int(body["time"])
        # no bigger than 12 hours
        if time < 0 or time > 720:
            return jsonify({"message": f"Cannot cook food for more than 12" \
                            " hours or negative values. Cannot set time."}), 404
    except:
        return jsonify({"message": f"Bad value. Cannot set time."}), 404

    topic = mqtt_topics.SET_TIME.format(device_id=oven_id)
    mqtt_manager.publish_message(topic, jsonify.dumps({"time": time}))

    return jsonify({"message":"Success"}), 200
