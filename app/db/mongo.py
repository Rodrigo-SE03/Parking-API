from pymongo import MongoClient

from app.core.configs import ENV, MONGO_URI

client: MongoClient | None = None

def get_client():
  """Retorna o cliente MongoDB, criando uma nova conexão se necessário."""
  global client
  if client is None:
    try:
      client = MongoClient(MONGO_URI)
    except Exception as e:
      raise e
  return client

def get_db():
  """Retorna o banco de dados MongoDB apropriado (prod ou test)."""
  return get_client()["parking_db"] if ENV == "prod" else get_client()["parking_db_test"]

def get_collection():
  """Retorna a coleção 'parking' do banco de dados."""
  db = get_db()
  collection = db["parking"]
  return collection