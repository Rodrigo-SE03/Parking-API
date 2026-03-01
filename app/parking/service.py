from fastapi import HTTPException
from datetime import datetime

from .repo import ParkingRepo
from .schemas import History

from .utils.helper_functions import get_interval_minutes

parking_repo = ParkingRepo()

def enter_parking_lot_service(id: str):
  # Verifica se já existe uma sessão ativa (sem saída registrada)
  active_session = parking_repo.get_item(id)
  if active_session:
    raise HTTPException(status_code=409, detail="O veículo já está no estacionamento")
  
  # Cria uma nova sessão
  new_item = parking_repo.insert_item(plate=id)
  return History(id=new_item.parking_id)

def get_history_service(id: str):
  items = parking_repo.get_all_sessions(id)
  if not items:
    raise HTTPException(status_code=404, detail="Placa não encontrada no sistema")
  
  item_history: list[History] = []
  
  for item in items:
    # Se a sessão está concluída (tem time_left), o tempo é fixo entre entrada e saída
    if item.time_left:
      time_str = get_interval_minutes(item.time_enter, item.time_left)
      item_history.append(History(
        id=item.parking_id,
        time=time_str,
        paid=True,
        left=True
      ))
    # Se a sessão está ativa (sem time_left), calcula o tempo até agora
    else:
      time_str = get_interval_minutes(item.time_enter, datetime.now())
      item_history.append(History(
        id=item.parking_id,
        time=time_str,
        paid=bool(item.time_paid),
        left=False
      ))

  return item_history
  
def pay_parking_ticket_service(id: str):
  item = parking_repo.get_item(id)
  if item == None:
    raise HTTPException(status_code=404, detail="Placa não encontrada no sistema")
  if item.time_paid:
    raise HTTPException(status_code=409, detail="Pagamento já registrado para o veículo")
  if item.time_left:
    raise HTTPException(status_code=409, detail="Saída do veículo já registrada")
  
  updated_item = parking_repo.update_item(id,"pay")
  return History(id=updated_item.parking_id,time=get_interval_minutes(updated_item.time_enter, updated_item.time_paid),paid=True)

def leave_parking_lot_service(id: str):
  item = parking_repo.get_item(id)
  if item == None:
    raise HTTPException(status_code=404, detail="Placa não encontrada no sistema")
  if not item.time_paid:
    raise HTTPException(status_code=412, detail="O pagamento ainda não foi efetuado")
  if item.time_left:
    raise HTTPException(status_code=409, detail="Saída do veículo já registrada")
  
  updated_item = parking_repo.update_item(id,"leave")
  return History(id=updated_item.parking_id,time=get_interval_minutes(updated_item.time_enter, updated_item.time_left),paid=True,left=True)

def delete_parking_record_service(id: str):
  item = parking_repo.get_item(id)
  if item == None:
    raise HTTPException(status_code=404, detail="Placa não encontrada no sistema")
  
  parking_repo.remove_item(id)