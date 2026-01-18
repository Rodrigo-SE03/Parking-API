ENTER_ERRORS = {
  409: {"content": {"application/json": {"example": {"detail": "O veículo já está no estacionamento"}}}},
  422: {"content": {"application/json": {"example": {"detail": "Formatação da placa incorreta"}}}}
}

PAY_ERRORS = {
  404: {"content": {"application/json": {"example": {"detail": "Placa não encontrada no sistema"}}}},
  409: {"content": {"application/json": {"example": {"detail": "Pagamento já registrado para o veículo"}}}},
  422: {"content": {"application/json": {"example": {"detail": "Formatação da placa incorreta"}}}}
}

LEAVE_ERRORS = {
  404: {"content": {"application/json": {"example": {"detail": "Placa não encontrada no sistema"}}}},
  409: {"content": {"application/json": {"example": {"detail": "Saída do veículo já registrada"}}}},
  412: {"content": {"application/json": {"example": {"detail": "O pagamento ainda não foi efetuado"}}}},
  422: {"content": {"application/json": {"example": {"detail": "Formatação da placa incorreta"}}}}
}

HISTORY_ERRORS = {
  404: {"content": {"application/json": {"example": {"detail": "Placa não encontrada no sistema"}}}},
  422: {"content": {"application/json": {"example": {"detail": "Formatação da placa incorreta"}}}}
}