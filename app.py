# import eventlet
import json
import argparse
# Monkey-patch (required for SocketIO)
# eventlet.monkey_patch()

from flask import Flask
from flasgger import Swagger
# from threading import Thread
from flask_mqtt import Mqtt
from globals import connected_devices, Oven
import os

import recipes
import recipe_search_online
import db
from constants import MONGO_URI, MONGO_URI_TEST

from spec import SWAGGER_TEMPLATE
from constants import MONGO_URI, SWAGGER_API_URL, SWAGGER_URL
from flask_pymongo import PyMongo


# Flask, MQTT
app: Flask
mqtt: Mqtt
swagger = None
# thread = None

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
    app.register_blueprint(recipe_search_online.bp)

    return app


def mqtt_setup():
    global app, mqtt
    # Setup connection to mqtt broker
    app.config['MQTT_BROKER_URL'] = 'localhost'
    # default port for non-tls connection
    app.config['MQTT_BROKER_PORT'] = 1883
    # set the username here if you need authentication for the broker
    app.config['MQTT_USERNAME'] = ''
    # set the password here if the broker demands authentication
    app.config['MQTT_PASSWORD'] = ''
    # set the time interval for sending a ping to the broker to 5 seconds
    app.config['MQTT_KEEPALIVE'] = 5
    # set TLS to disabled for testing purposes
    app.config['MQTT_TLS_ENABLED'] = False

    mqtt = Mqtt(app)


def mqtt_listeners_setup():
    @mqtt.on_topic('oven/connect')
    def handle_device_connect(client, userdata, msg):
        device_id = msg.payload.decode()

        if device_id not in connected_devices:
            connected_devices[device_id] = Oven(device_id)
            print(f'Device connected {device_id}')

            '''
            new device connected
            subscribe and handle messages sent
            to it's corresponding topic
            '''
            @mqtt.on_topic(f'{device_id}/#')
            def handle_device_info(client, userdata, msg):
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

            mqtt.subscribe(f'{device_id}/#')


    @mqtt.on_topic('oven/disconnect')
    def handle_device_disconnect(client, userdata, msg):
        device_id = msg.payload.decode()
        connected_devices.pop(device_id, None)
        print(f'Device disconnected {device_id}')
        mqtt.unsubscribe(f'{device_id}/#')

    mqtt.subscribe('oven/connect')
    mqtt.subscribe('oven/disconnect')


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
    args = parser.parse_args()
    
    create_app(testing=args.test)
    mqtt_setup()
    mqtt_listeners_setup()
    # start_background_mqtt()
    app.run(debug=False)
