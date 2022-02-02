from test_client import client
from test_ovens import connecting

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
        #recipe = { "name": "Banana bread for integration", "prep_time": 60, "prep_details": "test", "baking_temperature": 200}
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

    def get_recipe_id(self, client, expected_response):
        #expected_response = { "name": "Banana-bread-for-integration", "prep_time": 60, "prep_details": "test", "baking_temperature": 200}
        response = client.get('/recipe/Banana-bread-for-testing', follow_redirects=True)
        assert response.status_code == 200
        assert self.check_if_responses_are_equal(expected_response, response.json)

    def edit_recipe(self, client, recipe_id):
        recipe_id = self.get_recipe_id(client)
        updated_recipe = { "name": "Banana-bread-for-testing", "prep_time": 100, "prep_details": "test", "baking_temperature": 150}
        response = client.put(f'/recipe/{recipe_id}', json=updated_recipe, follow_redirects=True)
        assert response.status_code == 200
        assert response.json['message'] == f"Updated recipe with id {recipe_id}"

    def test_integration2(self, client):
        # adaugam reteta
        # editam reteta
        # iau reteta
        # setez temperatura din reteta
        # setez timpul din reteta
        # pornesc cuptorul
        # opresc cuptorul
        # sters reteta
        pass

