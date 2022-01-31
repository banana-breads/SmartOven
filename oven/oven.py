import json

from datetime import datetime, timedelta
from mqtt_shared import mqtt_manager as mqtt, \
    mqtt_topics as topics


class _Oven():
    def __init__(self):
        self.device_id = mqtt.get_client_id()
        self.state = False # off
        self.current_recipe = None # recipe name
        self.temperature = None # int in Celsius
        self.target_temperature = None # int in Celsius
        self.recipe = None
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


    def set_listeners(self):
        self._set_state_listener()
        self._set_recipe_listener()
        self._set_temperature_listener()
        self._set_time_listener()


    def _set_state_listener(self):
        def state_listener(client, userdata, msg):
            data = json.loads(msg.payload.decode())
            print(f"State: {data}")
            self.state = data

        topic = topics.SET_STATE.format(device_id=self.device_id)
        mqtt.register_callback(topic, state_listener)


    def _set_recipe_listener(self):
        def recipe_listener(client, userdata, msg):
            data = json.loads(msg.payload.decode())
            print(f"Recipe: {data}")
            self.recipe = data

        topic = topics.SET_RECIPE.format(device_id=self.device_id)
        mqtt.register_callback(topic, recipe_listener)


    def _set_temperature_listener(self):
        def temperature_listener(client, userdata, msg):
            data = json.loads(msg.payload.decode())
            print(f"Temperature: {data}")
            self.target_temperature = data

        topic = topics.SET_TEMPERATURE.format(device_id=self.device_id)
        mqtt.register_callback(topic, temperature_listener)


    def _set_time_listener(self):
        def temperature_listener(client, userdata, msg):
            data = json.loads(msg.payload.decode())
            print(f"Cook time: {data}")
            self.recipe_end_time = datetime.utcnow() + timedelta(minutes=data)

        topic = topics.SET_TIME.format(device_id=self.device_id)
        mqtt.register_callback(topic, temperature_listener)


_oven = None
def get_oven():
    global _oven
    if _oven is None:
        _oven = _Oven()
    return _oven
