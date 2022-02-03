import json

from flask import Blueprint, request, jsonify
from mqtt_shared import mqtt_manager, mqtt_topics
from recipes import get_one_recipe
from globals import connected_devices


def _check_if_oven_exists(oven_id):
    return oven_id in connected_devices


bp = Blueprint('ovens', __name__, url_prefix='/oven')


@bp.route("/<oven_id>", methods=['GET'])
def get_oven_info(oven_id=None):
    """
    See current oven info.
    ---
    parameters:
        - name: oven_id
          in: path
          required: true
          schema:
              type: string
    responses:
        200:
            description: Successfully returned the specified oven's info
            content:
                application/json:
                    schema:
                        type: object
                        required:
                            - state
                        properties:
                            state:
                                type: string
                            temperature:
                                type: integer
                            time:
                                type: integer
                            recipe:
                                type: object
                                properties:
                                    name:
                                        type: string
                                    prep_time:
                                        type: integer
                                    prep_details:
                                        type: string
                                    baking_temperature:
                                        type: integer
        400:
            description: Bad request - Missing oven ID
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            message:
                                type: string
                                example: Please specify an oven ID
        404:
            description: Oven not found
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            message:
                                type: string
                                example: No oven found with id
    """
    
    if not _check_if_oven_exists(oven_id):
        return jsonify({"message":"No oven found with id"}), 404

    oven = connected_devices[oven_id]
    return jsonify({
        "state": oven.state,
        "temperature": oven.temperature,
        "time": oven.time,
        "recipe": oven.recipe_info
    })


@bp.route("", methods=['GET'])
def get_all_ovens(oven_id=None):
    """
    See currently connected ovens.
    ---
    responses:
        200:
            description: Successfully returned the  ovens' info
            content:
                application/json:
                    schema:
                        type: array
                        items:
                            type: object
                            properties:
                                id:
                                    type: string
                                state:
                                    type: string
                                temperature:
                                    type: integer
                                time:
                                    type: integer
                                recipe:
                                    type: object
                                    properties:
                                        name:
                                            type: string
                                        prep_time:
                                            type: integer
                                        prep_details:
                                            type: string
                                        baking_temperature:
                                            type: integer
    """
    response = []

    for k,oven in connected_devices.items():
        response.append({
            "id": k,
            "state": oven.state["state"],
            "temperature": oven.temperature,
            "time": oven.time,
            "recipe": oven.recipe_info
        })
    return jsonify(response)


@bp.route("/<oven_id>/state", methods=['POST'])
def set_oven_state(oven_id=None):
    """
    Manage oven state (True if oven is on, False otherwise)
    Oven will start preparing food according to its given settings.
    ---
    parameters:
        - name: oven_id
          in: path
          required: true
          schema:
              type: string
    requestBody:
        required: true
        content:
            application/json:
                schema:
                    type: object
                    required:
                        - state
                    properties:
                        state:
                            type: boolean
                            example: true
    responses:
        200:
            description: Successfully changed oven's state
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            message:
                                type: string
                                example: Oven with id has started cooking
        400:
            description: Bad request - Missing state parameter or bad state value
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            message:
                                type: string
                                example: Missing state parameter
        404:
            description: Not found oven with specified id
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            message:
                                type: string
                                example: Oven with id does not exist
    """
    body = request.json
    if body is None or 'state' not in body:
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
        return jsonify({"message": f"Bad value. Cannot change state."}), 400

    topic = mqtt_topics.SET_STATE.format(device_id=oven_id)
    mqtt_manager.publish_message(topic, json.dumps({"state": new_state}))

    return jsonify({"message": result}), 200


@bp.route("/<oven_id>/recipe/<recipe_name>", methods=['POST'])
def set_oven_recipe(oven_id=None, recipe_name=None):
    """
    Sets the oven to the cooking parameters specified in the recipe
    (cooking temperature, cooking time).
    ---
    parameters:
        - name: oven_id
          in: path
          required: true
          schema:
              type: string
        - name: recipe_name
          in: path
          required: true
          schema:
              type: string
    responses:
        200:
            description: Successfully added the recipe to the oven
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            message:
                                type: string
                                example: Success
        404:
            description: Not found oven/recipe with specified id/name
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            message:
                                type: string
                                example: Oven with id does not exist
    """
    if not _check_if_oven_exists(oven_id):
        return jsonify({"message": f"Oven with id {oven_id} does not exist." \
                        " Cannot set recipe."}), 404

    recipe = get_one_recipe(recipe_name)

    if not recipe:
        return jsonify({"message": f"Recipe '{recipe_name}' does not exist." \
                        " Cannot set recipe."}), 404

    topic = mqtt_topics.SET_RECIPE.format(device_id=oven_id)
    mqtt_manager.publish_message(topic, json.dumps(recipe))

    return jsonify({"message":"Success"}), 200


@bp.route("/<oven_id>/temperature", methods=['POST'])
def set_oven_temperature(oven_id=None):
    """
    Manually sets the oven temperature (in Celsius).
    ---
    parameters:
        - name: oven_id
          in: path
          required: true
          schema:
              type: string
    requestBody:
        required: true
        content:
            application/json:
                schema:
                    type: object
                    required:
                        - temperature
                    properties:
                        temperature:
                            type: integer
                            example: 50
    responses:
        200:
            description: Successfully changed oven's temperature
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            message:
                                type: string
                                example: Success
        400:
            description: Bad request - Missing temperature parameter or bad state value
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            message:
                                type: string
                                example: Missing temperature parameter
        404:
            description: Not found oven with specified id
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            message:
                                type: string
                                example: Oven with id does not exist
    """
    body = request.json
    if body is None or 'temperature' not in body:
        return jsonify({ 'message': f'Missing temperature parameter.' \
                        f'No action taken on oven {oven_id}.' }), 400

    if not _check_if_oven_exists(oven_id):
        return jsonify({"message": f"Oven with id {oven_id} does not exist." \
                        " Cannot set temperature."}), 404

    try:
        temperature = int(body["temperature"])
        if temperature < 0 or temperature > 250:
            return jsonify({"message": f"Oven cannot run on temperatures " \
                " negative or hotter than 250C. Cannot set temperature."}), 400
    except:
        return jsonify({"message": f"Bad value. Cannot set temperature."}), 400

    topic = mqtt_topics.SET_TEMPERATURE.format(device_id=oven_id)
    mqtt_manager.publish_message(topic, json.dumps({"temperature": temperature}))

    return jsonify({"message":"Success"}), 200


@bp.route("/<oven_id>/time", methods=['POST'])
def set_oven_time(oven_id=None):
    """
    Manually sets the oven time (in minutes).
    ---
    parameters:
        - name: oven_id
          in: path
          required: true
          schema:
              type: string
    requestBody:
        required: true
        content:
            application/json:
                schema:
                    type: object
                    required:
                        - time
                    properties:
                        time:
                            type: integer
                            example: 50
    responses:
        200:
            description: Successfully changed oven's time
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            message:
                                type: string
                                example: Success
        400:
            description: Bad request - Missing time parameter or bad state value
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            message:
                                type: string
                                example: Missing time parameter
        404:
            description: Not found oven with specified id
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            message:
                                type: string
                                example: Oven with id does not exist
    """
    body = request.json
    if body is None or 'time' not in body:
        return jsonify({ 'message': f'Missing time parameter.' \
                        f' No action taken on oven {oven_id}.' }), 400
    if not _check_if_oven_exists(oven_id):
        return jsonify({"message": f"Oven with id {oven_id} does not exist." \
                        " Cannot set time."}), 404

    try:
        time = int(body["time"])
        # no bigger than 12 hours
        if time < 0 or time > 720:
            return jsonify({"message": f"Cannot cook food for more than 12" \
                            " hours or negative values. Cannot set time."}), 400
    except:
        return jsonify({"message": f"Bad value. Cannot set time."}), 400

    topic = mqtt_topics.SET_TIME.format(device_id=oven_id)
    mqtt_manager.publish_message(topic, json.dumps({"time": time}))

    return jsonify({"message":"Success"}), 200
