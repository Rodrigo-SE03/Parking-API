from pydantic import BaseModel, Field, field_validator
from fastapi import Path, Body
from typing import Optional
from datetime import datetime
from bson import ObjectId

class PlateItem(BaseModel):
  plate: str

bodySchema = Body(description="Placa do veículo", examples={"plate": "AAA-9999"})

idSchema = Path(description="Placa do veículo", examples="AAA-9999")

class ParkingItem(BaseModel):
  id: Optional[str] = Field(None, alias="_id")
  parking_id: int
  plate: str
  time_enter: str = "0 minutes"
  time_paid: str = "0 minutes"
  time_left: str = "0 minutes"
  paid: bool = False
  left: bool = False
  created_at: datetime

  # Na validação, converte o ObjectID do Mongo para string
  @field_validator("id", mode="before")
  @classmethod
  def oid_to_str(cls, value):
    if isinstance(value,ObjectId):
      return str(value)
    return value

class History(BaseModel):
  id: int
  time: str = "0 minutes"
  paid: bool = False
  left: bool = False