import os
import sys
from threading import Thread
from time import sleep
from test_client import client

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import device

def connect_device():
    thread = Thread(target=device.run)
    thread.start()
    sleep(2)

class TestIntegration:

    def test_integration1(self, client):
        # caut reteta pe net
        # iau datele cuptorului
        # pun reteta pe cuptor
        # pornesc cuptorul
        # opresc cuptorul
        # sters reteta
        pass

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
        connect_device()
        response = client.get('/oven', follow_redirects=True)
        print(response.json)
        oven = response.json[0]
        assert response.status_code == 200
        return oven

    def delete_recipe(self, client, recipe_id):
        response = client.delete(f'/recipe/{recipe_id}', follow_redirects=True)
        assert response.status_code == 200

    def test_integration2(self, client):
        recipe_name = 'Banana-bread-for-integration'
        recipe = { "name": "Banana-bread-for-integration", "prep_time": 60, "prep_details": "test", "baking_temperature": 200}
        recipe_edited = { "name": "Banana-bread-for-integration", "prep_time": 60, "prep_details": "test", "baking_temperature": 150}
        recipe_id = None
        self.delete_recipe(client, '61faf12458b5fd7b3c0c05d4')
        self.add_recipe(client, recipe)
        recipe_id = self.get_recipe(client, recipe_name, recipe)['id']
        self.edit_recipe(client, recipe_id, recipe_edited)
        new_recipe = self.get_recipe(client, recipe_name, recipe_edited)
        oven = self.get_oven(client)
        oven_id = oven['id']

        # setez temperatura din reteta
        body = {'temperature': new_recipe['temperature']}
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
        assert response.json['message'] == f"Oven with id {oven_id} has stopped cooking."

        # opresc cuptorul
        body = {'state': False}
        response = client.post(f'oven/{oven_id}/state', json=body, follow_redirects=True)
        assert response.status_code ==  200
        assert response.json['message'] == f"Oven with id {oven_id} has stopped cooking."

        # sters reteta
        self.delete_recipe(client, recipe_id)

