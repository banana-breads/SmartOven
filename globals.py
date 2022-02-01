
"""
    Used to store data gathered from connected devices
"""

class Oven:
    def __init__(self, device_id):
        self.id = device_id
        self.temperature = {}
        self.time = {}
        self.state = False
        self.recipe_info = {}


connected_devices = { }
