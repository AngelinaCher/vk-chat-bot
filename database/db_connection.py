from pymongo.mongo_client import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

USERNAME_DB = os.getenv('USERNAME_DB')
PASSWORD = os.getenv('PASSWORD')

uri = f"mongodb+srv://{USERNAME_DB}:{PASSWORD}@cluster0.kmmaypl.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri)

db = client.vk_bot
db_collection = db.users

if __name__ == '__main__':
    try:
        client.admin.command('ping')
        print("База данных успешно подключена!")
    except Exception as e:
        print(e)
