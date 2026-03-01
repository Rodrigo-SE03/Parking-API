"""Testes para o endpoint PUT /parking/{id}/pay (Pagamento)
"""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestPayParkingTicket:
  """Testes para pagamento do estacionamento"""
  
  def test_pagamento_sucesso(self, veiculo_estacionado):
    """Cenário: Pagamento normal após entrada - deve retornar 200"""
    response = client.put(f"/parking/{veiculo_estacionado}/pay")
    
    assert response.status_code == 200
    data = response.json()
    assert data["paid"] == True
    assert data["left"] == False
    assert "time" in data
  
  def test_pagamento_veiculo_nao_existe(self):
    """Cenário: Tentar pagar sem ter entrado - deve retornar 404"""
    response = client.put("/parking/GHO-0000/pay")
    
    assert response.status_code == 404
    assert "não encontrada no sistema" in response.json()["detail"]
  
  def test_pagamento_duplicado(self, veiculo_pago):
    """Cenário: Tentar pagar duas vezes - deve retornar 409"""
    response = client.put(f"/parking/{veiculo_pago}/pay")
    
    assert response.status_code == 409
    assert "já registrado" in response.json()["detail"]
  
  def test_pagamento_apos_saida(self):
    """Cenário: Tentar pagar depois de já ter saído - deve retornar 409"""
    placa = "SAI-9999"
    client.post("/parking/", json={"plate": placa})
    client.put(f"/parking/{placa}/pay")
    client.put(f"/parking/{placa}/out")
    
    # Tenta pagar novamente após saída
    response = client.put(f"/parking/{placa}/pay")
    
    assert response.status_code == 409
    assert "já registrado" in response.json()["detail"]
  
  def test_pagamento_placa_invalida(self):
    """Cenário: Placa com formato inválido - deve retornar 422"""
    response = client.put("/parking/INVALIDA/pay")
    
    assert response.status_code == 422
    assert "Formatação da placa incorreta" in response.json()["detail"]
