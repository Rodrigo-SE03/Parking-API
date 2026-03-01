import os

from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv("ENV", "dev")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://admin:admin@localhost:27017")

