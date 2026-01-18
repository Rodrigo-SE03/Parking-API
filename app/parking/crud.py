from app.db.mongo import get_collection, get_db
from .schemas import ParkingItem
from typing import Literal
from datetime import datetime
from .utils.helper_functions import get_interval_minutes, get_next_parking_id

Action = Literal["pay", "leave"]

class ParkingRepo:
  def __init__(self):
    self.collection = get_collection()

  def get_item(self, plate: str) -> ParkingItem | None:
    item = self.collection.find_one({ "plate": plate })
    if item == None:
      return None
    
    return ParkingItem.model_validate(item)
  
  def insert_item(self, plate: str) -> ParkingItem | None:
    item = ParkingItem(parking_id=get_next_parking_id(get_db()),plate=plate, created_at=datetime.now())
    doc = item.model_dump()
    
    self.collection.insert_one(doc)
    
    return self.get_item(plate)
  
  def update_item(self, plate: str, action: Action) -> ParkingItem | None:
    entry_time = self.get_item(plate).created_at
    update = {}
    diff = get_interval_minutes(entry_time)
    if action == "pay":
      update = {"$set": {"paid": True, "time_paid": diff}}
    elif action == "leave":
      update = {"$set": {"left": True, "time_left": diff}}
    
    self.collection.update_one({ "plate": plate },update)

    return self.get_item(plate=plate)

  def remove_item(self, plate: str):
    self.collection.delete_one({ "plate": plate })