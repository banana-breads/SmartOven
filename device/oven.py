import json

from datetime import datetime


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
        return json.dumps({ "temperature": 150 })


    def get_current_recipe_info(self):
        if self.state is False:
            return None

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
