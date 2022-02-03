from test_client import client

added_recipe_name = None

class TestSearchRecipes:

    def get_added_recipe_id(self, client):
        global added_recipe_name
        response = client.get(f'/recipe/{added_recipe_name}', follow_redirects=True)
        return response.json['id']

    def delete_added_recipe(self, client):
        recipe_id = self.get_added_recipe_id(client)
        client.delete(f'/recipe/{recipe_id}', follow_redirects=True)

    def test_search_recipes_without_required_fields(self, client):
        response = client.post('/recipe/find', follow_redirects=True)
        assert response.status_code == 400

    def test_search_recipes_not_found(self, client):
        name = {"name": "qwerty"}
        response = client.post('/recipe/find', json=name, follow_redirects=True)
        assert response.status_code == 404

    def test_successful_search_recipes(self, client):
        global added_recipe_name
        name = {"name": "Rice"}
        response = client.post('/recipe/find', json=name, follow_redirects=True)
        added_recipe_name = response.json['name']
        assert response.status_code == 200

    def test_duplicate_key_for_search_name(self, client):
        name = {"name": "Rice"}
        response = client.post('/recipe/find', json=name, follow_redirects=True)
        assert response.status_code == 409
        self.delete_added_recipe(client)
