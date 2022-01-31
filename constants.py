import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# MongoDB
MONGODB_PASSWORD = "ingineriesoftware" if os.getenv('MONGODB_PASSWORD') is None else os.getenv('MONGODB_PASSWORD')
MONGO_URI = f"mongodb+srv://smartover-iot:{MONGODB_PASSWORD}@smartover-iot.ccvsc.mongodb.net/SMART_OVEN_DB?retryWrites=true&w=majority"

MONGO_URI_TEST = f"mongodb+srv://smartover-iot:{MONGODB_PASSWORD}@smartover-iot.ccvsc.mongodb.net/SMART_OVEN_DB_TEST?retryWrites=true&w=majority"

# Swagger UI
SWAGGER_URL = "/docs"
SWAGGER_API_URL = "/static/swagger.json"

SPOONACULAR_API_KEY = os.getenv("SPOONACULAR")
