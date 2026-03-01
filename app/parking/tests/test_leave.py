"""Testes para o endpoint PUT /parking/{id}/out (Saída do estacionamento)
"""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestLeaveParkingLot:
  """Testes para saída do estacionamento"""
  
  def test_saida_sucesso(self, veiculo_pago):
    """Cenário: Saída após entrada e pagamento - deve retornar 200"""
    response = client.put(f"/parking/{veiculo_pago}/out")
    
    assert response.status_code == 200
    data = response.json()
    assert data["paid"] == True
    assert data["left"] == True
    assert "time" in data

  def test_saida_sem_pagamento(self, veiculo_estacionado):
    """Cenário: Tentar sair sem ter pago - deve retornar 412"""
    response = client.put(f"/parking/{veiculo_estacionado}/out")
    
    assert response.status_code == 412
    assert "pagamento ainda não foi efetuado" in response.json()["detail"]
  
  def test_saida_veiculo_nao_existe(self):
    """Cenário: Tentar sair sem ter entrado - deve retornar 404"""
    response = client.put("/parking/GHO-0000/out")
    
    assert response.status_code == 404
    assert "não encontrada no sistema" in response.json()["detail"]
  
  def test_saida_duplicada(self, veiculo_completo):
    """Cenário: Tentar sair duas vezes - deve retornar 409"""
    response = client.put(f"/parking/{veiculo_completo}/out")
    
    assert response.status_code == 409
    assert "Saída do veículo já registrada" in response.json()["detail"]
  
  def test_saida_placa_invalida(self):
    """Cenário: Placa com formato inválido - deve retornar 422"""
    response = client.put("/parking/INVALIDA/out")
    
    assert response.status_code == 422
    assert "Formatação da placa incorreta" in response.json()["detail"]
