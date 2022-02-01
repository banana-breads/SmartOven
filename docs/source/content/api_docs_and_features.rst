******************************
API Documentation and Features
******************************

Here you can find the documentation for SmartOven's main features.


##################
Recipes Management
##################

Application provides a list of endpoints for Creating, Reading, Updating and
Deleting of the recipes from ovens database.

.. GET RECIPES
.. http:get:: /recipe

   Returns all recipes that are stored in oven's database.

   **Example request**

   .. sourcecode:: http

      GET /recipe HTTP/1.1
      Host: localhost:5000
      Accept: application/json
   
   **Example response**
   
   .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: application/json

      [
        {
          "name": "Banana-Bread",
          "prep_time": 10,
          "prep_details": "Details for baking Banana Bread",
          "baking_temperature": 30
        },
        {
          "name": "Apple-Pie",
          "prep_time": 40,
          "prep_details": "Details for baking Apple Pie",
          "baking_temperature": 50
        }
      ]
   
   :statuscode 200: Successfully returned a list of recipes

.. GET RECIPE
.. http:get:: /recipe/{recipe_name}

   Returns the recipes that has the specified name.

   **Example request**

   .. sourcecode:: http

      GET /recipe/test-recipe HTTP/1.1
      Host: localhost:5000
      Accept: application/json
   
   **Example response**
   
   .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: application/json

      {
         "id": "1",
         "name": "test-recipe",
         "prep_time": 40,
         "prep_details": "Details test recipe",
         "baking_temperature": 50
      }
   
   :statuscode 200: Successfully returned a list of recipes
   :statuscode 400: Bad get recipe request (name is not specified)
   :statuscode 404: The recipe with the specified name wasn't found

.. POST RECIPE
.. http:post:: /recipe

   Adds a new recipe to oven's database.

   **Example request**

   .. sourcecode:: http

      POST /recipe HTTP/1.1
      Host: localhost:5000
      Accept: application/json
      
      {
         "name": "test-recipe",
         "prep_time": 40,
         "prep_details": "Details test recipe",
         "baking_temperature": 50 
      }
   
   **Example response**
   
   .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: application/json

      {
         "id": "1",
         "message": "Successfully added a new recipe"
      }
   
   :statuscode 200: Successfully added a new recipe
   :statuscode 400: Some parameters are not specified
   :statuscode 409: The recipe with the specified name already exists


.. UPDATE RECIPE
.. http:put:: /recipe/{recipe_id}

   Updates an existing recipe from oven's database.

   **Example request**

   .. sourcecode:: http

      PUT /recipe/1 HTTP/1.1
      Host: localhost:5000
      Accept: application/json
      
      {
         "name": "test-recipe-updated",
         "prep_time": 50,
      }
   
   **Example response**
   
   .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: application/json

      {
         "message": "Successfully updated the recipe"
      }
   
   :statuscode 200: Successfully updated the recipe
   :statuscode 400: Recipe is missing or has unallowed fields
   :statuscode 409: Recipe does not exist
   :statuscode 500: Server error during recipe update


.. DELETE RECIPE
.. http:delete:: /recipe/{recipe_id}

   Deletes an existing recipe from oven's database.

   **Example request**

   .. sourcecode:: http

      DELETE /recipe/1 HTTP/1.1
      Host: localhost:5000
      Accept: application/json
   
   **Example response**
   
   .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: application/json

      {
         "message": "Successfully deleted the recipe with id 1"
      }
   
   :statuscode 200: Successfully deleted the recipe
   :statuscode 409: Recipe does not exist
   

#############
Recipe Search
#############

.. POST SEARCH
.. http:post:: /recipe/find

   Searches for a new recipe online and if one recipe has been found, take it and add it to oven's database, if it doesn't exist already.

   **Example request**

   .. sourcecode:: http

      POST /recipe/find HTTP/1.1
      Host: localhost:5000
      Accept: application/json
      
      {
         "name": "Banana bread" 
      }
   
   **Example response**
   
   .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: application/json

      {
         "name": "Banana bread",
         "prep_time": 10,
         "prep_details": "Details banana bread preparation",
         "baking_temperature": 50 
      }
   
   :statuscode 200: Successfully found and added the searched recipe
   :statuscode 400: Missing fields to search for recipe
   :statuscode 401: The client is not authorized to search
   :statuscode 404: Recipe was not found online
   :statuscode 409: The recipe with the specified name already exists