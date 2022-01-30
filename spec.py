import json

SWAGGER_TEMPLATE = {
    "info": {
        "title": "SmartOven",
        "description": "Oven. But smart.",
        "version": "1.0.0",
        "license": {
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
        }
    }
}


def dump_apispecs_to_json(swagger, path="./static/swagger.json"):
    with open(path, 'w') as f:
        json.dump(swagger.get_apispecs(), f, indent=2)