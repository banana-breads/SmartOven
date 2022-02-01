from flask import request, jsonify
from flask import (Blueprint)
from bson import json_util
from bson.objectid import ObjectId
from db import get_db
from recipes import add_recipe
from constants import SPOONACULAR_API_KEY
from pymongo.errors import DuplicateKeyError

import requests
import json
import re

bp = Blueprint('recipe', __name__, url_prefix='/recipe')

@bp.route('/find', methods=['POST'])
def find_and_add():
    """
    Search a new recipe and add it in the oven's database
    ---
    requestBody:
        required: true
        content:
            application/json:
                schema:
                    type: object
                    required:
                        - name
                    properties:
                        name:
                            type: string
                            example: Banana bread
    responses:
        200:
            description: Successfully found and added a new recipe
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            name:
                                type: string
                                example: Test recipe
                            prep_time:
                                type: integer
                                example: 10
                            prep_details:
                                type: string
                                example: Test recipe details
                            baking_temperature:
                                type: integer
                                example: 20
        400:
            description: Bad request - Missing required fields for a recipe
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            message:
                                type: string
                                example: Missing fields to search recipe
        401:
            description: Unauthorised client
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            message:
                                type: string
                                example: The client is not authorised to search

        404:
            description: Recipe not found
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            message:
                                type: string
                                example: No recipe with name found


        409:
            description: Conflict - Duplicate recipe
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            message:
                                type: string
                                example: A recipe with the same name already exists
        
    """
    if not request.json or not request.json.get('name'):
        return jsonify({ 'message': 'Missing fields to search recipe' }), 400

    recipeTitle = request.json['name']
    searchParams = {
        'apiKey':SPOONACULAR_API_KEY,
        'equipment':'oven',
        'number':'1',
        'instructionsRequired':True,
        'titleMatch':recipeTitle
    }
    resultObject = None
    try:
        resultObject = requests.request(method="get", url=f"https://api.spoonacular.com/recipes/complexSearch",params=searchParams).content
        resultObject = json.loads(resultObject)

        if (resultObject["totalResults"] == 0):
            return jsonify({
                'message':'No recipe with name found'
            }), 404
    except:
        return {'message': 'The client is not authorised to search'}, 401
    
    foundRecipeId = resultObject["results"][0]["id"]

    # get details of found recipe

    recipeDetailsParams = {
        'apiKey':SPOONACULAR_API_KEY,
        'includeNutrition':False
    }

    foundRecipeData = requests.request(method="get", url=f"https://api.spoonacular.com/recipes/{foundRecipeId}/information",params=searchParams).content
    foundRecipeData = json.loads(foundRecipeData)
    name = foundRecipeData["title"]
    instructions = foundRecipeData["instructions"]
    oven_time, oven_temp = getOvenSettings(instructions, foundRecipeData["analyzedInstructions"][0]["steps"])

    # if not provided by api, set some defaults
    if oven_time == 0:
        time = 30
    if oven_temp == 0:
        oven_temp = 150

    recipe_info = {
        "name":name,
        "prep_time":oven_time,
        "prep_details":_strip_html(instructions),
        "baking_temperature":oven_temp
    }

    try:
        res = add_recipe(name, oven_time, instructions, oven_temp)
    except DuplicateKeyError:
        return jsonify({ 'message': 'A recipe with the same name already exists' }), 409

    return recipe_info

"""
Helper that clears instructions of html tags
"""
def _strip_html(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def getOvenSettings(instructionsBlock, instructionsList):
    oven_temp = 0
    oven_time = 0
    # search for the recipe step where the oven is used.
    for instruction in instructionsList:
        for equipment in instruction["equipment"]:
            # if i haven't found the oven time yet:
            if not(oven_time):
                # if this instructions lists the oven as being used, get it's time duration.
                if equipment["name"] == "oven":
                    if not("length" in instruction):
                        continue

                    if instruction["length"]["unit"] == "hours":
                        oven_time = instruction["length"]["number"] * 60
                    else:
                        oven_time = instruction["length"]["number"]
            # if i haven't found the oven temp yet:
            if not(oven_temp):
                if equipment["name"] == "oven":
                    # if i'm lucky and the step includes the temperature as a separate parameter
                    if 'temperature' in equipment and 'number' in equipment['temperature']:
                        oven_temp = int(equipment['temperature']['number'])
                        continue
                    
                    # otherwise, try to find it in the step text with regex. woo
                    instructionText = instruction['step']

                    # try to find temperature in text
                    found_temp = findTempInText(instructionText)

                    if found_temp:
                        oven_temp = found_temp

    # if i still haven't found oven temp, regex the entire instructions list in hopes to find it
    if not(oven_temp):
        found_temp = findTempInText(instructionsBlock)

        if found_temp:
            oven_temp = found_temp
    
    return oven_time, oven_temp

def findTempInText(text):
    matches = re.findall(r"([0-9]{3}[ ]?[C,F,c,f]?)", text)
    if len(matches) == 0:
        return 0 # nothing useful found

    # cleanup, remove C/F and spaces
    oven_temp = int(re.findall(r'[0-9]{3}', matches[0])[0])

    # if >200, it's fahrenheit. convert to celsius.
    if oven_temp > 200:
        oven_temp = int((5/9) * (oven_temp - 32))
    
    return oven_temp

