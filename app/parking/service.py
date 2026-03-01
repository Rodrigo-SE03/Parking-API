from .repo import ParkingRepo
from fastapi import HTTPException
from .schemas import History

parking_repo = ParkingRepo()

def enter_parking_lot_service(id: str):
  item = parking_repo.get_item(id)
  if item:
    if not item.left:
      raise HTTPException(status_code=409, detail="O veículo já está no estacionamento")
    else:
      parking_repo.remove_item(id)
  
  new_item = parking_repo.insert_item(plate=id)
  return History(id=new_item.parking_id)

def get_history_service(id: str):
  item = parking_repo.get_item(id)
  if item == None:
    raise HTTPException(status_code=404, detail="Placa não encontrada no sistema")
  item_history: list[History] = []
  item_history.append(History(id=item.parking_id,time=item.time_enter))
  if item.paid:
    item_history.append(History(id=item.parking_id,time=item.time_paid,paid=item.paid))
  if item.left:
    item_history.append(History(id=item.parking_id,time=item.time_left,paid=item.paid,left=item.left))

  return item_history
  
def pay_parking_ticket_service(id: str):
  item = parking_repo.get_item(id)
  if item == None:
    raise HTTPException(status_code=404, detail="Placa não encontrada no sistema")
  if item.paid:
    raise HTTPException(status_code=409, detail="Pagamento já registrado para o veículo")
  if item.left:
    raise HTTPException(status_code=409, detail="Saída do veículo já registrada")
  
  updated_item = parking_repo.update_item(id,"pay")
  return History(id=updated_item.parking_id,time=updated_item.time_paid,paid=updated_item.paid)

def leave_parking_lot_service(id: str):
  item = parking_repo.get_item(id)
  if item == None:
    raise HTTPException(status_code=404, detail="Placa não encontrada no sistema")
  if not item.paid:
    raise HTTPException(status_code=412, detail="O pagamento ainda não foi efetuado")
  if item.left:
    raise HTTPException(status_code=409, detail="Saída do veículo já registrada")
  
  updated_item = parking_repo.update_item(id,"leave")
  return History(id=updated_item.parking_id,time=updated_item.time_left,paid=updated_item.paid,left=updated_item.left)

def delete_parking_record_service(id: str):
  item = parking_repo.get_item(id)
  if item == None:
    raise HTTPException(status_code=404, detail="Placa não encontrada no sistema")
  
  parking_repo.remove_item(id)