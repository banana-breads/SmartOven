import json

from datetime import datetime
from mqtt_shared import mqtt_manager as mqtt, \
    mqtt_topics as topics


class Oven():
    def __init__(self):
        self.device_id = mqtt.get_client_id()
        self.state = False # off
        self.current_recipe = None # recipe name
        self.temperature = None # int in Celsius
        self.target_temperature = None # int in Celsius
        self.recipe_end_time = datetime.utcnow() # timestamp UTC
        self.recipe_end_time = datetime.utcnow() # timestamp UTC


    def _get_temperature(self):
        # TODO update with math
        return json.dumps({ "temperature": 150 })


    def _get_current_recipe_info(self):
        if self.state is False:
            return json.dumps({})

        time_left = self.recipe_end_time - datetime.utcnow()
        minutes = time_left.total_seconds() // 60
        seconds = time_left.total_seconds() - minutes * 60
        return json.dumps({
            "name": self.current_recipe,
            "time_left": {
                "minutes": minutes,
                "seconds": seconds,
            }
        })


    def publish_sensor_data(self):
        topic_actions = {
            topics.TEMPERATURE.format(device_id=self.device_id): \
                self._get_temperature,
            topics.RECIPE_DETAILS.format(device_id=self.device_id): \
                self._get_current_recipe_info,
        }

        for topic, get_message in topic_actions.items():
            msg = get_message()
            mqtt.publish_message(topic, msg)
