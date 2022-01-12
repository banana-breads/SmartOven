import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# MongoDB
MONGODB_HOST = '127.0.0.1' if os.getenv('MONGODB_HOST') is None else os.getenv('MONGODB_HOST')
MONGODB_PORT = 27017 if os.getenv('MONGODB_PORT') is None else os.getenv('MONGODB_PORT')
MONGO_URI = f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}/SmartOvenDB"
