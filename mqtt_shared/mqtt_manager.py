import json
import time
import signal

from paho.mqtt import client as mqtt_client
from mqtt_shared.mqtt_topics import CONNECT, DISCONNECT

_client: mqtt_client.Client
# _BROKER = "broker.emqx.io"
_BROKER = 'localhost'
_PORT = 1883


def get_client_id():
    global _client
    return _client._client_id.decode()


def _on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.publish(CONNECT, get_client_id())
    else:
        print("Failed to connect, return code %d\n", rc)


def _disconnect_handler():
    """
        On forced disconnect, notify
    """
    def handler(signal, frame):
        print(f'Received signal {signal}. Terminating...')
        _client.publish(DISCONNECT, get_client_id())
        _client.disconnect()
        time.sleep(2)
        exit(0)

    return handler


def _on_disconnect(client, userdata, rc):
    """
        On disconnect, notify
    """
    if rc == 0:
        print("Disconnect successful")
    else:
        print("Forced disconnect")


def _on_message(client, userdata, msg):
    """
        Generic message callback
        Will be called when a topic-specific handler is not defined
    """
    try:
        topic = msg.topic
        data = json.loads(msg.payload.decode())
        print(f"Received {data} on topic {topic}")
    except:
        data = None
        # TODO add logger
        print("could load data")


def _on_publish(client, userdata, msg):
    """
        Print successful published messages. For debug only
    """
    topic = msg.topic
    data = json.loads(msg.payload.decode())
    print(f"Successfully published {data} on topic {topic}")


def _client_connect(device_name, device_serial):
    global _client

    client_id = f'{device_name}-{device_serial}'
    _client = mqtt_client.Client(client_id)

    _client.on_connect = _on_connect
    _client.on_message = _on_connect
    _client.on_disconnect = _on_disconnect
    #signal.signal(signal.SIGINT, _disconnect_handler())

    _client.connect(_BROKER, _PORT)


def _start_non_blocking():
    global _client
    _client.loop_start()


def register_callback(sub_topic_filter, callback):
    global _client

    if _client is not None:
        _client.subscribe(sub_topic_filter)
        _client.message_callback_add(sub_topic_filter, callback)
    else:
        print("Client is not initialized. Cannot register callback")


def unsubscribe(topic):
    global _client

    if _client is not None:
        _client.unsubscribe(topic)
    else:
        print("Client is not initialized. Cannot unsubscribe")


def publish_message(topic, message):
    global _client
    if _client is not None:
        _client.publish(topic, message)
    else:
        print("Client is not initialized. Cannot publish message")


def start(device_name, device_serial, callbacks=[]):
    _client_connect(device_name, device_serial)
    for topic, fun in callbacks:
        register_callback(topic, fun)
    _start_non_blocking()
