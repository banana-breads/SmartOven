import json
import time

from datetime import datetime, timedelta
from mqtt_shared import mqtt_manager as mqtt, \
    mqtt_topics as topics


class _Oven():

    _TEMP_INCR_MULTIPLYER = 20
    _BASE_TEMPERATURE = 22

    def __init__(self):
        self.device_id = mqtt.get_client_id()
        self.state = False # on if currently baking, or off
        self.current_temperature = _Oven._BASE_TEMPERATURE # int in Celsius
        self.target_temperature = 0 # int in Celsius
        self.timer = 0
        self.target_time = 0

        # self.recipe_info = {
        #     "name": "",
        #     "prep_details": ""
        # } if using a recipe, keeps its name and instructions. 
        self.recipe_info = None
        self._last_change = time.time()


    def _get_time_left(self):
        if self.state is False:
            return 0.0
        return round(self.target_time - self.timer, 2)


    def _get_temperature_info(self):
        return json.dumps({
            "current_temperature": self.current_temperature,
            "target_temperature": self.target_temperature
         })


    def _get_time_info(self):
        return json.dumps({
            "time_elapsed": round(self.timer, 2),
            "time_left": self._get_time_left(),
            "target_time": self.target_time
         })


    def _get_device_state(self):
        return json.dumps({
            "state": self.state
         })


    def _get_current_recipe_info(self):
        if not self.recipe_info:
            return json.dumps({})
        return json.dumps(self.recipe_info)


    def publish_sensor_data(self):
        topic_actions = {
            topics.TEMPERATURE.format(device_id=self.device_id): \
                self._get_temperature_info,
            topics.TIME.format(device_id=self.device_id): \
                self._get_time_info,
            topics.STATE.format(device_id=self.device_id): \
                self._get_device_state
        }

        for topic, get_message in topic_actions.items():
            msg = get_message()
            mqtt.publish_message(topic, msg)


    def publish_recipe_info(self):
        topic = topics.RECIPE_DETAILS.format(device_id=self.device_id)
        mqtt.publish_message(topic, self._get_current_recipe_info())


    def publish_recipe_done_message(self):
        topic = topics.RECIPE_DONE.format(device_id=self.device_id)

        message = ''
        if self.recipe_info:
          message = f"Recipe {self.recipe_info['name']} has finished cooking."
        else:
          message = f'Your recipe has finished cooking.'

        mqtt.publish_message(topic, json.dumps({"message": message}))


    def simulate_sensors(self):
        time_now = time.time()
        diff = (time_now - self._last_change) / 60 # minutes

        if self.state is True:
            self.timer = min(self.target_time, self.timer + diff)
            if self.current_temperature < self.target_temperature:
                self.current_temperature = min(self.target_temperature, \
                    self.current_temperature + diff * _Oven._TEMP_INCR_MULTIPLYER)
            else:
                self.current_temperature = max(self.target_temperature, \
                    self.current_temperature - diff * _Oven._TEMP_INCR_MULTIPLYER)

            if self.timer == self.target_time:
                self.publish_recipe_done_message()
                self.state = False
                self.timer = 0
        else:
            if self.current_temperature > _Oven._BASE_TEMPERATURE:
                self.current_temperature = max(_Oven._BASE_TEMPERATURE, \
                    self.current_temperature - diff * _Oven._TEMP_INCR_MULTIPLYER)

        self.current_temperature = round(self.current_temperature, 2)
        self._last_change = time_now


    def set_listeners(self):
        self._set_state_listener()
        self._set_recipe_listener()
        self._set_temperature_listener()
        self._set_time_listener()
        self._get_recipe_listener()


    def _set_state_listener(self):
        def state_listener(client, userdata, msg):
            data = json.loads(msg.payload.decode())
            print(f"State: {data}")
            self.state = bool(data.get('state', False))
            if self.state == False:
                self.timer = 0

        topic = topics.SET_STATE.format(device_id=self.device_id)
        mqtt.register_callback(topic, state_listener)


    def _set_recipe_listener(self):
        def recipe_listener(client, userdata, msg):
            data = json.loads(msg.payload.decode())
            print(f"Recipe: {data}")
            try:
                self.recipe_info = {
                    "name": data.get("name", ""),
                    "prep_details": data.get("prep_details", "")
                }
                self.target_temperature = data.get("baking_temperature", 150)
                self.target_time = data.get("prep_time", 30)
                self.publish_recipe_info()

            except:
                self.recipe_info = None
                print("error setting recipe:", data)

        topic = topics.SET_RECIPE.format(device_id=self.device_id)
        mqtt.register_callback(topic, recipe_listener)


    def _set_temperature_listener(self):
        def temperature_listener(client, userdata, msg):
            data = json.loads(msg.payload.decode())
            print(f"Temperature: {data}")
            try:
                self.target_temperature = int(data.get("temperature", 0))
            except:
                self.target_temperature = 0
                print("error setting temperature:",data)

        topic = topics.SET_TEMPERATURE.format(device_id=self.device_id)
        mqtt.register_callback(topic, temperature_listener)


    def _set_time_listener(self):
        def temperature_listener(client, userdata, msg):
            data = json.loads(msg.payload.decode())
            print(f"Cook time: {data}")
            try:
                self.target_time = int(data.get("time", 0))
            except:
                self.target_time = 0
                print("error setting time:",data)

        topic = topics.SET_TIME.format(device_id=self.device_id)
        mqtt.register_callback(topic, temperature_listener)


    def _get_recipe_listener(self):
        def get_recipe_listener(client, userdata, msg):
            self.publish_recipe_info()

        topic = topics.GET_RECIPE_DETAILS.format(device_id=self.device_id)
        mqtt.register_callback(topic, get_recipe_listener)


_oven = None
def get_oven():
    global _oven
    if _oven is None:
        _oven = _Oven()
    return _oven
