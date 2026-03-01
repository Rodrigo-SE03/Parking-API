from fastapi import APIRouter
from .utils.helper_functions import plate_validation
from .schemas import PlateItem, idSchema, bodySchema, History
from .repo import ParkingRepo
from .service import (
    get_history_service,
    pay_parking_ticket_service,
    leave_parking_lot_service,
    enter_parking_lot_service,
    delete_parking_record_service,
)
from .errors import ENTER_ERRORS, PAY_ERRORS, LEAVE_ERRORS, HISTORY_ERRORS

router = APIRouter(prefix="/parking", tags=["parking"])


@router.get("/{id}", response_model=list[History], responses=HISTORY_ERRORS)
async def get_history(id: str = idSchema):
    """
    Retorna uma lista com o histórico de ações do veículo no estacionamento (entrada, pagamento e saída)
    """
    plate = plate_validation(id)
    response = get_history_service(plate)
    return response


@router.put("/{id}/pay", response_model=History, responses=PAY_ERRORS)
async def pay_parking_ticket(id: str = idSchema):
    """
    Registra o pagamento do estacionamento referente ao veículo
    """
    plate = plate_validation(id)
    response = pay_parking_ticket_service(plate)
    return response


@router.put("/{id}/out", response_model=History, responses=LEAVE_ERRORS)
async def exit_parking_lot(id: str = idSchema):
    """
    Registra a saída do veículo do estacionamento
    """
    plate = plate_validation(id)
    response = leave_parking_lot_service(plate)
    return response


@router.post("", response_model=History, status_code=201, responses=ENTER_ERRORS)
async def enter_parking_lot(plateItem: PlateItem = bodySchema):
    """
    Registra a entrada do veículo do estacionamento
    """
    plate = plate_validation(plateItem.plate)
    response = enter_parking_lot_service(plate)
    return response


@router.delete("/{id}", responses=HISTORY_ERRORS, status_code=204)
async def delete_item(id: str = idSchema):
    """
    Remove um item do banco de dados
    """
    plate = plate_validation(id)
    response = delete_parking_record_service(plate)
    return response

