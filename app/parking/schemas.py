from datetime import datetime

from bson import ObjectId
from fastapi import Body, Path
from pydantic import BaseModel, Field, field_validator


class PlateItem(BaseModel):
  """Schema para validação de entrada de placa."""
  plate: str

bodySchema = Body(description="Placa do veículo", examples={"plate": "AAA-9999"})

idSchema = Path(description="Placa do veículo", examples="AAA-9999")

class ParkingItem(BaseModel):
  """Modelo de dados de uma sessão de estacionamento."""
  id: str | None = Field(None, alias="_id")
  parking_id: int
  plate: str
  time_enter: datetime | None = None
  time_paid: datetime | None = None
  time_left: datetime | None = None
  created_at: datetime

  # Na validação, converte o ObjectID do Mongo para string
  @field_validator("id", mode="before")
  @classmethod
  def oid_to_str(cls, value):
    """Converte ObjectId do MongoDB para string."""
    if isinstance(value,ObjectId):
      return str(value)
    return value

class History(BaseModel):
  """Schema de resposta com histórico de sessão."""
  id: int
  time: str = "0 minutes"
  paid: bool = False
  left: bool = False