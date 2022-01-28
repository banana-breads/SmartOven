import eventlet
# Monkey-patch (required for SocketIO)
eventlet.monkey_patch()

from flask import Flask
from threading import Thread
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
import json
import time
import os

import recipes
import db
from constants import MONGO_URI
from flask_pymongo import PyMongo


# Flask, MQTT and SocketIO apps
app = None
mqtt = None
socketio = None
thread = None


def create_app(test_config=None):
    global app
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

    # TODO: Delete at the end
    @app.route('/')
    def hello_world():
        return "Hello World!"


def setup_mqtt_and_socketio():
    global app, mqtt, socketio

    # Setup connection to mqtt broker
    app.config['MQTT_BROKER_URL'] = 'localhost'  # use the free broker from HIVEMQ
    app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
    app.config['MQTT_USERNAME'] = ''  # set the username here if you need authentication for the broker
    app.config['MQTT_PASSWORD'] = ''  # set the password here if the broker demands authentication
    app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
    app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes

    thread = None
    mqtt = Mqtt(app)
    socketio = SocketIO(app, async_mode="eventlet")


def start_background_mqtt():
    global thread
    if thread is None:
        thread = Thread(target=background_thread)
        thread.daemon = True
        thread.start()


# Function that every second publishes a message
def background_thread():
    while True:
        time.sleep(1)
        # Using app context is required because the get_status() functions
        # requires access to the db.
        with app.app_context():
            message = json.dumps({"name": "Test"}, default=str)
        # Publish
        mqtt.publish('python/mqtt', message)


if __name__ == "__main__":
    create_app()
    setup_mqtt_and_socketio()
    start_background_mqtt()
    socketio.run(app, host='localhost', port=5000, use_reloader=False, debug=True)
