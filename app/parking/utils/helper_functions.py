from fastapi import HTTPException
from datetime import datetime
import re

def plate_validation(plate: str) -> str:
  """
  Valida a formatação da placa do veículo de acordo com o padrão AAA-9999
  """
  pattern = r'^[A-Za-z]{3}-\d{4}$'
  if re.match(pattern, plate):
    return plate.upper()
  else:
    raise HTTPException(status_code=422, detail="Formatação da placa incorreta")
  
def get_interval_minutes(created_at: datetime) -> str:
  """
  Calcula o intervalo em minutos entre o datetime atual e o datetime informado. Retorna no formato: 'x minutes'
  """
  minute_diff = (datetime.now() - created_at).total_seconds()/60
  return f"{round(minute_diff)} minutes"

def get_next_parking_id(db) -> int:
  """
  Gera o valor da reserva do veículo por incremento sequencial
  """
  counter = db.counters.find_one_and_update(
    {"_id": "parking"},
    {"$inc": {"seq": 1}},
    return_document=True,
    upsert=True
  )
  return counter["seq"]