import time
import uuid

import mqtt_shared.mqtt_manager as mqtt
import mqtt_shared.mqtt_topics as mqtt_topics

from oven.oven import Oven

_PUBLISH_RATE = 3 # pause between publishes

def run():
    client_name = 'oven'
    client_serial = str(uuid.uuid4())

    mqtt.start(client_name, client_serial)

    oven = Oven()
    while True:
        oven.publish_sensor_data()
        time.sleep(_PUBLISH_RATE)

if __name__ == '__main__':
    run()