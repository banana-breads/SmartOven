import random
from datetime import datetime

from paho.mqtt import client as mqtt_client


broker = 'localhost'
port = 1883

####
# Oven 
####
class Oven():
    def __init__(self):
        self.state = False # off
        self.current_recipe = None # recipe name
        self.temperature = None # int in Celsius
        self.target_temperature = None # int in Celsius
        self.recipe_end_time = datetime.utcnow() # timestamp UTC
        self.recipe_end_time = datetime.utcnow() # timestamp UTC
        pass

    def get_temperature(self):
        # TODO update with math
        return 150


    def get_current_recipe_info(self):
        if self.state is False:
            return None

        time_left = self.recipe_end_time - datetime.utcnow()
        minutes = time_left.total_seconds() // 60
        seconds = time_left.total_seconds() - minutes * 60
        return {
            "name": self.current_recipe,
            "time_left": {
                "minutes": minutes,
                "seconds": seconds,
            }
        }

####


def connect_mqtt() -> mqtt_client.Client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client_id = f'python-mqtt-{random.randint(0, 1000)}'
    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


# def publish(client: mqtt_client.Client):
#     msg_count = 0
#     while True:
#         time.sleep(1)
#         msg = f"messages: {msg_count}"
#         result = client.publish(topic, msg)
#         # result: [0, 1]
#         status = result[0]
#         if status == 0:
#             print(f"Send `{msg}` to topic `{topic}`")
#         else:
#             print(f"Failed to send message to topic {topic}")
#         msg_count += 1


def run():
    client = connect_mqtt()
    client.loop_start()
    # publish(client)
# run()

# import random
#
# from paho.mqtt import client as mqtt_client
#
#
# broker = 'localhost'
# port = 1883
# topic = "python/mqtt"
# # generate client ID with pub prefix randomly
# client_id = f'python-mqtt-{random.randint(0, 100)}'
#
#
# def connect_mqtt() -> mqtt_client.Client:
#     def on_connect(client, userdata, flags, rc):
#         if rc == 0:
#             print("Connected to MQTT Broker!")
#         else:
#             print("Failed to connect, return code %d\n", rc)
#
#     client = mqtt_client.Client(client_id)
#     # client.username_pw_set(username, password)
#     client.on_connect = on_connect
#     client.connect(broker, port)
#     return client
#
#
# def subscribe(client: mqtt_client.Client):
#     def on_message(client, userdata, msg):
#         print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
#
#     client.subscribe(topic)
#     client.on_message = on_message
#
#
# def run():
#     client = connect_mqtt()
#     subscribe(client)
#     client.loop_forever()
#
#
# if __name__ == '__main__':
#     run()
