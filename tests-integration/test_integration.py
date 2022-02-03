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

class TestIntegration:

    def check_if_oven_state_is_set_correctly(self, client, expected_state):
        oven = self.get_oven(client)
        assert oven["state"] == expected_state

    def check_if_oven_recipe_is_set_correctly(self, client, expected_recipe):
        oven = self.get_oven(client)
        assert oven["recipe"]["name"] == expected_recipe["name"] 
        assert oven["recipe"]["prep_details"] == expected_recipe["prep_details"]
        assert oven["temperature"]["target_temperature"] == expected_recipe["baking_temperature"]
        assert oven["time"]["target_time"] == expected_recipe["prep_time"]
    
    def add_recipe(self, client, recipe):
        response = client.post('/recipe', json=recipe, follow_redirects=True)
        assert response.status_code == 200

    def check_if_responses_are_equal(self, expected_response, our_response):
        result = True
        result = result and all([our_response.get('name'), our_response.get('prep_time'), our_response.get('prep_details'), our_response.get('baking_temperature')])
        result = result and our_response['name'] == expected_response['name']
        result = result and our_response['prep_time'] == expected_response['prep_time']
        result = result and our_response['prep_details'] == expected_response['prep_details']
        result = result and our_response['baking_temperature'] == expected_response['baking_temperature']
        return result

    def get_recipe(self, client, recipe_name, expected_response):
        response = client.get(f'/recipe/{recipe_name}', follow_redirects=True)
        assert response.status_code == 200
        assert self.check_if_responses_are_equal(expected_response, response.json)
        return response.json

    def edit_recipe(self, client, recipe_id, updated_recipe):
        response = client.put(f'/recipe/{recipe_id}', json=updated_recipe, follow_redirects=True)
        assert response.status_code == 200
        assert response.json['message'] == f"Updated recipe with id {recipe_id}"

    def get_oven(self, client):
        connecting()
        response = client.get('/oven', follow_redirects=True)
        print(response.json)
        oven = response.json[0]
        assert response.status_code == 200
        return oven

    def delete_recipe(self, client, recipe_id):
        response = client.delete(f'/recipe/{recipe_id}', follow_redirects=True)
        assert response.status_code == 200

    def test_integration1(self, client):
        connecting()

        # caut reteta pe net
        searched_recipe = {
            "name":"Rustic Pasta with Chunky Vegetables"
        }
        recipe_name = "Rustic-Pasta-with-Chunky-Vegetables" # numele corespondent al retetei
        response = client.post('/recipe/find', json=searched_recipe, follow_redirects=True)
        assert response.status_code == 200

        # vad daca s-a adaugat reteta
        response = client.get(f'/recipe/{recipe_name}', follow_redirects=True)
        assert response.status_code == 200

        recipe = response.json
        recipe_id = recipe['id']

        # iau datele cuptorului
        oven = self.get_oven(client)
        oven_id = oven['id']

        # pun reteta pe cuptor
        response = client.post(f'oven/{oven_id}/recipe/{recipe_name}', follow_redirects=True)
        assert response.status_code == 200
        assert response.json['message'] == "Success"      

        sleep(3)
        #verific ca s-a setat corect
        self.check_if_oven_recipe_is_set_correctly(client, recipe)

        # pornesc cuptorul
        body = {'state': True}
        response = client.post(f'oven/{oven_id}/state', json=body, follow_redirects=True)
        assert response.status_code ==  200
        assert response.json['message'] == f"Oven with id {oven_id} has started cooking."

        sleep(3)
        #verific ca a pornit
        self.check_if_oven_state_is_set_correctly(client, True)

        # opresc cuptorul
        body = {'state': False}
        response = client.post(f'oven/{oven_id}/state', json=body, follow_redirects=True)
        assert response.status_code ==  200
        assert response.json['message'] == f"Oven with id {oven_id} has stopped cooking."
        sleep(3)

        #verific ca s-a oprit
        self.check_if_oven_state_is_set_correctly(client, False)

        # sterg reteta
        self.delete_recipe(client, recipe_id)
        sleep(1)

    def test_integration2(self, client):
        recipe_name = 'Banana-bread-for-integration'
        recipe = { "name": "Banana-bread-for-integration", "prep_time": 60, "prep_details": "test", "baking_temperature": 200}
        recipe_edited = { "name": "Banana-bread-for-integration", "prep_time": 60, "prep_details": "test", "baking_temperature": 150}
        recipe_id = None

        connecting()
        self.add_recipe(client, recipe)
        recipe_id = self.get_recipe(client, recipe_name, recipe)['id']
        self.edit_recipe(client, recipe_id, recipe_edited)
        new_recipe = self.get_recipe(client, recipe_name, recipe_edited)
        oven = self.get_oven(client)
        oven_id = oven['id']

        # setez temperatura din reteta
        body = {'temperature': new_recipe['baking_temperature']}
        response = client.post(f'oven/{oven_id}/temperature', json=body, follow_redirects=True)
        assert response.status_code ==  200
        assert response.json['message'] == "Success"

        # setez timpul din reteta
        body = {'time': new_recipe['prep_time']}
        response = client.post(f'oven/{oven_id}/time', json=body, follow_redirects=True)
        assert response.status_code ==  200
        assert response.json['message'] == "Success"

        # pornesc cuptorul
        body = {'state': True}
        response = client.post(f'oven/{oven_id}/state', json=body, follow_redirects=True)
        assert response.status_code ==  200
        assert response.json['message'] == f"Oven with id {oven_id} has started cooking."

        # opresc cuptorul
        body = {'state': False}
        response = client.post(f'oven/{oven_id}/state', json=body, follow_redirects=True)
        assert response.status_code ==  200
        assert response.json['message'] == f"Oven with id {oven_id} has stopped cooking."

        # sterg reteta
        self.delete_recipe(client, recipe_id)