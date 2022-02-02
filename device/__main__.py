import random
import time
import signal

from oven import Oven
from paho.mqtt import client as mqtt_client

client_id = None
broker = 'localhost'
port = 1883


def on_disconnect(client):
  def handler(signal, frame):
    print(f'Received signal {signal}. Terminating...')
    client.publish('oven/disconnect', client_id)
    time.sleep(3)
    exit(0)

  return handler


def mqtt_connect() -> mqtt_client.Client:
    global client_id

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            client.publish('oven/connect', client_id)
        else:
            print("Failed to connect, return code %d\n", rc)

    client_id = f'oven-{random.randint(0, 1000)}'
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    client.on_disconnect = on_disconnect

    return client

# TODO on message callback
# def on_get_recipe_message(client, userdata, msg):
#     TOPIC = 'oven/recipe/info'
#     client.publish(TOPIC, msg)

def publish(client: mqtt_client.Client, oven):
    topic_actions = {
        f'{client_id}/temperature': oven.get_temperature,
        f'{client_id}/recipe_detalis': oven.get_current_recipe_info,
    }

    while True:
        time.sleep(1)
        for topic, get_message in topic_actions.items():
            msg = get_message()
            result = client.publish(topic, msg)
            status = result[0]
            if status == 0:
                print(f"Send `{msg}` to topic `{topic}`")
            else:
                print(f"Failed to send message to topic {topic}")


def run():
    client = mqtt_connect()
    client.loop_start()

    # handle disconnect
    handler = on_disconnect(client)
    #signal.signal(signal.SIGINT, handler)

    oven = Oven()
    publish(client, oven)

# def subscribe(client: mqtt_client.Client):
#     def on_message(client, userdata, msg):
#         print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
#
#     client.subscribe(topic)
#     client.on_message = on_message

if __name__ == '__main__':
    run()
