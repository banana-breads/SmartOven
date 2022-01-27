import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# MongoDB
MONGODB_PASSWORD = "ingineriesoftware" if os.getenv('MONGODB_PASSWORD') is None else os.getenv('MONGODB_PASSWORD')
MONGO_URI = f"mongodb+srv://smartover-iot:{MONGODB_PASSWORD}@smartover-iot.ccvsc.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
# MONGO_URI = f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}/SmartOvenDB"
