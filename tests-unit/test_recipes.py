from test_client import client


class TestPostRecipes:

    def test_post_recipes_without_required_fields(self, client):
        # sending request without prep_time field
        recipe = { "name": "Banana bread for testing", "prep_details": "test", "baking_temperature": 200}
        response = client.post('/recipe', json=recipe, follow_redirects=True)
        assert response.status_code == 400

    def test_successful_post_recipes(self, client):
        recipe = { "name": "Banana bread for testing", "prep_time": 60, "prep_details": "test", "baking_temperature": 200}
        response = client.post('/recipe', json=recipe, follow_redirects=True)
        assert response.status_code == 200

    def test_duplicate_key_for_recipe_name(self, client):
        # check if name field is unique
        recipe = { "name": "Banana bread for testing", "prep_time": 60, "prep_details": "test", "baking_temperature": 200}
        response = client.post('/recipe', json=recipe, follow_redirects=True)
        assert response.status_code == 409

class TestGetRecipes:   

    def check_if_responses_are_equal(self, expected_response, our_response):
        result = True
        result = result and all([our_response.get('name'), our_response.get('prep_time'), our_response.get('prep_details'), our_response.get('baking_temperature')])
        result = result and our_response['name'] == expected_response['name']
        result = result and our_response['prep_time'] == expected_response['prep_time']
        result = result and our_response['prep_details'] == expected_response['prep_details']
        result = result and our_response['baking_temperature'] == expected_response['baking_temperature']
        return result

    def test_succesful_get_recipes(self, client):
        expected_response = { "name": "Banana-bread-for-testing", "prep_time": 60, "prep_details": "test", "baking_temperature": 200}
        response = client.get('/recipe', follow_redirects=True)

        assert response.status_code == 200
        assert len(response.json) == 1
        our_response = response.json[0]
        assert self.check_if_responses_are_equal(expected_response, our_response)
    
    def test_succesful_get_recipe(self, client):
        expected_response = { "name": "Banana-bread-for-testing", "prep_time": 60, "prep_details": "test", "baking_temperature": 200}
        response = client.get('/recipe/Banana-bread-for-testing', follow_redirects=True)
        assert response.status_code == 200
        assert self.check_if_responses_are_equal(expected_response, response.json)

    def test_recipe_not_found(self, client):
        response = client.get('/recipe/', follow_redirects=True)
        assert response.status_code == 400

    def test_recipe_not_found(self, client):
        response = client.get('/recipe/qwerty', follow_redirects=True)
        assert response.status_code == 404

class TestUpdateRecipes:

    def get_recipe_id(self, client):
        response = client.get('/recipe/Banana-bread-for-testing', follow_redirects=True)
        return response.json['id']

    def test_update_not_found_recipe(self, client):
        updated_recipe = { "name": "Banana-bread-for-testing", "prep_time": 100, "prep_details": "test", "baking_temperature": 150}
        response = client.put('/recipe/qwerty', json=updated_recipe, follow_redirects=True)
        assert response.status_code == 404

    def test_update_with_unallowed_fields(self, client):
        recipe_id = self.get_recipe_id(client)
        updated_recipe = { "name": "Banana-bread-for-testing", "prep_time": 100, "hacked": "hacked"}
        response = client.put(f'/recipe/{recipe_id}', json=updated_recipe, follow_redirects=True)
        assert response.status_code == 400

    def test_succesful_update(self, client):
        recipe_id = self.get_recipe_id(client)
        updated_recipe = { "name": "Banana-bread-for-testing", "prep_time": 100, "prep_details": "test", "baking_temperature": 150}
        response = client.put(f'/recipe/{recipe_id}', json=updated_recipe, follow_redirects=True)
        assert response.status_code == 200
        assert response.json['message'] == f"Updated recipe with id {recipe_id}"


class TestDeleteRecipes:

    def get_recipe_id(self, client):
        response = client.get('/recipe/Banana-bread-for-testing', follow_redirects=True)
        return response.json['id']

    def test_succesful_delete_recipe(self, client):
        recipe_id = self.get_recipe_id(client)
        response = client.delete(f'/recipe/{recipe_id}', follow_redirects=True)
        assert response.status_code == 200
    
    def test_delete_not_found_recipe(self, client):
        response = client.delete('/recipe/qwerty', follow_redirects=True)
        assert response.status_code == 404

