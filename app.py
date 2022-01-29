import eventlet
import json
# Monkey-patch (required for SocketIO)
eventlet.monkey_patch()

from flask import Flask
from threading import Thread
from flask_mqtt import Mqtt
from globals import connected_devices, Oven
import os

import recipes
import db
from constants import MONGO_URI


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        MONGO_URI=MONGO_URI,
    )

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

    return app


def mqtt_setup(app):
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
    return mqtt


def mqtt_listeners_setup(mqtt):
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
    app = create_app()
    mqtt = mqtt_setup(app)
    mqtt_listeners_setup(mqtt)
    # start_background_mqtt()
    app.run(debug=False)
