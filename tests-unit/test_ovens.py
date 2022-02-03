import os
import sys
from threading import Thread
from test_client import client
from time import sleep

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import device
from globals import connected_devices


our_device_id = None

def connect_device():
    thread = Thread(target=device.run)
    thread.start()
    sleep(5)

def set_device_id():
    global our_device_id
    if len(connected_devices) == 1:
        our_device_id = list(connected_devices.keys())[0]
    else:
        raise Exception("No devices or too many devices connected")

def connecting():
    while len(connected_devices) == 0:
        connect_device()
    set_device_id()  


class TestGetOvenInfo():

    def test_not_found_oven(self, client):
        response = client.get('/oven/qwerty', follow_redirects=True)
        assert response.status_code == 404
        assert response.json['message'] == "No oven found with id"

    def test_succesfully_get_oven_info(self, client):
        global our_device_id
        connecting()
        response = client.get(f'/oven/{our_device_id}', follow_redirects=True)
        assert response.status_code == 200

class TestPostOvenState():

    def test_change_state_no_state(self, client):
        global our_device_id
        connecting()
        response = client.post(f'oven/{our_device_id}/state', follow_redirects=True)
        assert response.status_code ==  400
        assert response.json['message'] == f'Missing state parameter.' \
                        f'No action taken on oven {our_device_id}.'

    def test_change_state_invalid_state(self, client):
        global our_device_id
        connecting()
        body = {'state': 'abracadabra'}
        response = client.post(f'oven/{our_device_id}/state', json=body, follow_redirects=True)
        assert response.status_code ==  400
        assert response.json['message'] == "Bad value. Cannot change state."

    def test_change_state_oven_not_found(self, client):
        body = {'state': True}
        response = client.post('oven/qwerty/state', json=body, follow_redirects=True)
        assert response.status_code ==  404
        assert response.json['message'] == f"Oven with id qwerty does not exist." \
                        " Cannot modify state."

    def test_succesful_chage_oven_state(self, client):
        global our_device_id
        connecting()
        body = {'state': False}
        response = client.post(f'oven/{our_device_id}/state', json=body, follow_redirects=True)
        assert response.status_code ==  200
        assert response.json['message'] == f"Oven with id {our_device_id} has stopped cooking."


class TestPostOvenRecipe():
    def add_recipe(self, client):
        recipe = { "name": "Banana bread for oven", "prep_time": 60, "prep_details": "test", "baking_temperature": 200}
        client.post('/recipe', json=recipe, follow_redirects=True)

    def delete_recipe(self, client):
        recipe = client.get('/recipe/Banana-bread-for-oven', follow_redirects=True)
        recipe_id = recipe.json['id']
        client.delete(f'/recipe/{recipe_id}', follow_redirects=True)

    def test_set_recipe_oven_not_found(self, client):
        #self.delete_recipe(client)
        self.add_recipe(client)
        response = client.post('oven/qwerty/recipe/Banana-bread-for-oven', follow_redirects=True)
        assert response.status_code ==  404
        assert response.json['message'] == f"Oven with id qwerty does not exist." \
                        " Cannot set recipe."
    
    def test_set_not_found_recipe(self, client):
        global our_device_id
        connecting()
        response = client.post(f'oven/{our_device_id}/recipe/qwerty', follow_redirects=True)
        assert response.status_code ==  404
        assert response.json['message'] == f"Recipe 'qwerty' does not exist." \
                        " Cannot set recipe."

    def test_succesfully_set_recipe(self, client):
        global our_device_id
        connecting()
        response = client.post(f'oven/{our_device_id}/recipe/Banana-bread-for-oven', follow_redirects=True)
        self.delete_recipe(client)
        assert response.status_code == 200
        assert response.json['message'] == "Success"   


class TestPostOvenTemperature():

    def test_change_temp_no_temp(self, client):
        global our_device_id
        connecting()
        response = client.post(f'oven/{our_device_id}/temperature', follow_redirects=True)
        assert response.status_code ==  400
        assert response.json['message'] == f'Missing temperature parameter.' \
                        f'No action taken on oven {our_device_id}.'

    def test_change_temp_invalid_temp(self, client):
        global our_device_id
        connecting()
        body = {'temperature': 251}
        response = client.post(f'oven/{our_device_id}/temperature', json=body, follow_redirects=True)
        assert response.status_code ==  400
        assert response.json['message'] == f"Oven cannot run on temperatures " \
                " negative or hotter than 250C. Cannot set temperature."

    def test_change_temp_oven_not_found(self, client):
        body = {'temperature': 200}
        response = client.post('oven/qwerty/temperature', json=body, follow_redirects=True)
        assert response.status_code ==  404
        assert response.json['message'] == f"Oven with id qwerty does not exist." \
                        " Cannot set temperature."

    def test_succesful_chage_oven_temperature(self, client):
        global our_device_id
        connecting()
        body = {'temperature': 210}
        response = client.post(f'oven/{our_device_id}/temperature', json=body, follow_redirects=True)
        assert response.status_code ==  200
        assert response.json['message'] == "Success"


class TestPostOvenTime():

    def test_change_temp_no_time(self, client):
        global our_device_id
        connecting()
        response = client.post(f'oven/{our_device_id}/time', follow_redirects=True)
        assert response.status_code ==  400
        assert response.json['message'] == f'Missing time parameter.' \
                        f' No action taken on oven {our_device_id}.'


    def test_change_time_invalid_time(self, client):
        global our_device_id
        connecting()
        body = {'time': -2}
        response = client.post(f'oven/{our_device_id}/time', json=body, follow_redirects=True)
        assert response.status_code ==  400
        assert response.json['message'] == f"Cannot cook food for more than 12" \
                            " hours or negative values. Cannot set time."

    def test_change_time_oven_not_found(self, client):
        body = {'time': 60}
        response = client.post('oven/qwerty/time', json=body, follow_redirects=True)
        assert response.status_code ==  404
        assert response.json['message'] == f"Oven with id qwerty does not exist." \
                        " Cannot set time."

    def test_succesful_chage_oven_time(self, client):
        global our_device_id
        connecting()
        body = {'time': 70}
        response = client.post(f'oven/{our_device_id}/time', json=body, follow_redirects=True)
        assert response.status_code ==  200
        assert response.json['message'] == "Success"