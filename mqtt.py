from flask import Flask
from flask_mqtt import Mqtt
from threading import Thread


SUBSCRIBE_TOPICS = [('mqtt/#', 0)]
mqttClient: Mqtt

@mqttClient.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    print(data)

def setup( app: Flask):
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


topics = [("mqtt/#", 0)]
for topic, qos in topics:
    mqtt.subscribe(topic, qos)
