import json

from flask import Flask
from flasgger import Swagger
from globals import connected_devices, Oven
import os

import recipes
import ovens
import recipe_search_online
import db
from mqtt_shared import mqtt_manager, mqtt_topics
from constants import MONGO_URI, MONGO_URI_TEST
import argparse

from spec import SWAGGER_TEMPLATE, dump_apispecs_to_json
from flask_pymongo import PyMongo

swagger = None

# TODO have blueprints in a spepparate module

# Arguments
parser = argparse.ArgumentParser(description="SmartOven Flask server")
parser.add_argument('-t', '--test',
    help='Run the server in testing mode',
    action="store_true"
)

def create_app(test_config=None, testing=None):
    global app, swagger
    app = Flask(__name__, instance_relative_config=True)
    if not testing:
        app.config.from_mapping(
            SECRET_KEY='dev',
            MONGO_URI=MONGO_URI,
        )
    else:
        app.config.from_mapping(
            SECRET_KEY='test',
            MONGO_URI=MONGO_URI_TEST,
        )

    # Setting up Swagger API
    app.config['SWAGGER'] = {
        'uiversion': 3,
        'openapi': '3.0.2'
    }
    swagger = Swagger(app, template=SWAGGER_TEMPLATE)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    # App blueprints
    app.register_blueprint(recipes.bp)
    app.register_blueprint(ovens.bp)
    app.register_blueprint(recipe_search_online.bp)

    # Save OpenAPI specs
    # with app.app_context():
    #     dump_apispecs_to_json(swagger)

    mqtt_manager.start("server", 1, [
        (mqtt_topics.CONNECT, _handle_device_connect),
        (mqtt_topics.DISCONNECT, _handle_device_disconnect)
    ])
    return app

def _handle_device_connect(client, userdata, msg):
    client_id = client._client_id.decode()
    device_id = msg.payload.decode()
    if client_id == device_id:
        return

    if device_id not in connected_devices:
        connected_devices[device_id] = Oven(device_id)
        print(f'Device connected {device_id}')

        '''
        new device connected
        subscribe and handle messages sent
        to it's corresponding topic
        '''
        def _handle_device_info(client, userdata, msg):
            topic = msg.topic
            payload = msg.payload.decode()
            data = json.loads(payload)
            info_type = topic.split('/')[-1]

            print(data)
            if device_id not in connected_devices:
                # TODO logging
                print(f'Device {device_id} not connected')
                return

            device = connected_devices[device_id]
            if info_type == 'temperature':
                device.temperature = data
            elif info_type == 'recipe_details':
                device.recipe_info = data
            elif info_type == 'time':
                device.time = data
            elif info_type == 'state':
                device.state = data
            elif info_type == 'recipe_done':
                # can be replace with notifications in production
                print(data.get('message', "Recipe done"))


        topic = mqtt_topics.INFO_PREFIX.format(device_id=device_id) + "/#"
        mqtt_manager.register_callback(topic, _handle_device_info)


def _handle_device_disconnect(client, userdata, msg):
    device_id = msg.payload.decode()
    connected_devices.pop(device_id, None)
    print(f'Device disconnected {device_id}')
    topic = mqtt_topics.INFO_PREFIX.format(device_id=device_id) + "/#"
    mqtt_manager.unsubscribe(topic)


if __name__ == "__main__":
    args = parser.parse_args()
    create_app(testing=args.test)
    app.run(debug=False)
