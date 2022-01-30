import json
import time
import signal

from paho.mqtt import client as mqtt_client

_client: mqtt_client.Client
_BROKER = "broker.emqx.io"


def _on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client_id = str(client._client_id.decode())
        client.publish('oven/connect', client_id)
    else:
        print("Failed to connect, return code %d\n", rc)


# def _on_disconnect(client):
#     """
#         On forced disconnect, notify
#     """
#     def handler(signal, frame):
#         print(f'Received signal {signal}. Terminating...')
#         client_id = str(client._client_id.decode())
#         client.publish('oven/disconnect', client_id)
#         time.sleep(3)
#         exit(0)
#
#     return handler


def _on_disconnect(client, userdata, rc):
    """
        On disconnect, notify
    """
    client_id = str(client._client_id.decode())
    client.publish('oven/disconnect', client_id)
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


def mqtt_client_connect(device_name, device_serial):
    global _client

    client_id = f'{device_name}-{device_serial}'
    client = mqtt_client.Client(client_id)

    client.on_connect = _on_connect
    client.on_message = _on_connect
    client.on_disconnect = _on_disconnect

    client.connect(_BROKER)


def mqtt_register_callback(sub_topic_filter, callback):
    global _client

    if _client is not None:
        _client.message_callback_add(sub_topic_filter, callback)
    else:
        print("Client is not initialized. Cannot register callback")


def mqtt_unsubscribe(topic):
    global _client

    if _client is not None:
        _client.unsubscribe(topic)
    else:
        print("Client is not initialized. Cannot unsubscribe")


def mqtt_publish_message(topic, message):
    global _client

    if _client is not None:
        _client.publish(topic, message)
    else:
        print("Client is not initialized. Cannot publish message")


def mqtt_start_non_blocking():
    global _client
    _client.loop_start()
