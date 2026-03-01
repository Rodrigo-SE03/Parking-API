from datetime import datetime
from typing import Literal

from bson import ObjectId

from app.db.mongo import get_collection, get_db

from .schemas import ParkingItem
from .utils.helper_functions import get_next_parking_id

Action = Literal["pay", "leave"]

class ParkingRepo:
  def __init__(self):
    self.collection = get_collection()

  def get_item(self, plate: str) -> ParkingItem | None:
    """Retorna apenas a sessão ativa (sem saída) do veículo"""
    item = self.collection.find_one({ "plate": plate, "time_left": None })
    if item == None:
      return None
    
    return ParkingItem.model_validate(item)
  
  def get_all_sessions(self, plate: str) -> list[ParkingItem]:
    """Retorna todas as sessões do veículo, ordenadas por data de entrada"""
    items = self.collection.find({ "plate": plate }).sort("time_enter", 1)
    return [ParkingItem.model_validate(item) for item in items]
  
  def insert_item(self, plate: str) -> ParkingItem | None:
    item = ParkingItem(parking_id=get_next_parking_id(get_db()),plate=plate, created_at=datetime.now(), time_enter=datetime.now())
    doc = item.model_dump()
    
    self.collection.insert_one(doc)
    
    return self.get_item(plate)
  
  def update_item(self, plate: str, action: Action) -> ParkingItem | None:
    active_session = self.get_item(plate)
    if not active_session:
      return None
    
    update = {}
    if action == "pay":
      update = {"$set": {"time_paid": datetime.now()}}
    elif action == "leave":
      update = {"$set": {"time_left": datetime.now()}}
    
    object_id = ObjectId(active_session.id)
    self.collection.update_one({ "_id": object_id }, update)
    
    updated = self.collection.find_one({ "_id": object_id })
    return ParkingItem.model_validate(updated) if updated else None

  def remove_item(self, plate: str):
    """Remove apenas a sessão ativa do veículo"""
    self.collection.delete_one({ "plate": plate, "time_left": None })