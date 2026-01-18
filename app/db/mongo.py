from pymongo import MongoClient
from app.core.configs import MONGO_URI, ENV

client: MongoClient | None = None

def get_client():
  global client
  if client is None:
    client = MongoClient(MONGO_URI)
  return client

def get_db():
  return get_client()["parking_db"] if ENV == "prod" else get_client()["parking_db_test"]

def get_collection():
  db = get_db()
  collection = db["parking"]
  return collection