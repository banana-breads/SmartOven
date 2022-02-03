import json
import yaml

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


def dump_apispecs_to_json(swagger, path="./static/swagger"):
    with open(f"{path}.json", 'w') as f:
        json.dump(swagger.get_apispecs(), f, indent=2)
    with open(f"{path}.yml", 'w') as f:
        with open(f"{path}.json") as jf:
            data = json.load(jf)
            if data.get("definitions") == {}:
                data.pop("definitions")
            yaml.dump(data, f)
