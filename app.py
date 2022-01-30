# import eventlet
import json
# Monkey-patch (required for SocketIO)
# eventlet.monkey_patch()

from flask import Flask
from flasgger import Swagger
# from threading import Thread
from globals import connected_devices, Oven
import os

import recipes
import ovens
import db
from mqtt_shared import mqtt_manager, mqtt_topics
from constants import MONGO_URI

from spec import SWAGGER_TEMPLATE
from constants import MONGO_URI, SWAGGER_API_URL, SWAGGER_URL
from flask_pymongo import PyMongo

swagger = None
# thread = None


def create_app(test_config=None):
    global app, swagger
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        MONGO_URI=MONGO_URI,
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


def _handle_device_connect(client, userdata, msg):
    device_id = msg.payload.decode()

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
            info_type = topic.split('/')[1]

            if device_id not in connected_devices:
                # TODO logging
                print(f'Device {device_id} not connected')
                return

            device = connected_devices[device_id]
            if info_type == 'temperature':
                device.temperature = data
            elif info_type == 'recipe_details':
                device.recipe_details = data

        mqtt_manager.register_callback(INFO_PREFIX.format(device_id=device_id) + "/#",_handle_device_info)


def _handle_device_disconnect(client, userdata, msg):
    device_id = msg.payload.decode()
    connected_devices.pop(device_id, None)
    print(f'Device disconnected {device_id}')
    mqtt.unsubscribe(INFO_PREFIX.format(device_id=device_id) + "/#")


# Function that every second publishes a message
# def background_thread():
#     while True:
#         time.sleep(1)
#         # Using app context is required because the get_status() functions
#         # requires access to the db.
#         with app.app_context():
#             message = json.dumps({"name": "Test"}, default=str)
#         # Publish
#         mqtt.publish('python/mqtt', message)
#
#
# def start_background_mqtt():
#     global thread
#     thread = Thread(target=background_thread)
#     thread.daemon = True
#     thread.start()


if __name__ == "__main__":
    create_app()
    mqtt_manager.start("server", 1,[(mqtt_topics.CONNECT, _handle_device_connect), (mqtt_topics.DISCONNECT, _handle_device_disconnect)])
    # start_background_mqtt()
    app.run(debug=False)
