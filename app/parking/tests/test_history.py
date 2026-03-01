"""Testes para o endpoint GET /parking/{id} (Histórico)
"""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestGetHistory:
  """Testes para consulta de histórico"""
  
  def test_historico_apenas_entrada(self, veiculo_estacionado):
    """Cenário: Histórico de veículo que só entrou - deve ter 1 registro"""
    response = client.get(f"/parking/{veiculo_estacionado}")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["paid"] == False
    assert data[0]["left"] == False
  
  def test_historico_entrada_e_pagamento(self, veiculo_pago):
    """Cenário: Histórico de veículo que entrou e pagou - deve ter 2 registros"""
    response = client.get(f"/parking/{veiculo_pago}")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    # Primeiro registro: entrada
    assert data[0]["paid"] == False
    assert data[0]["left"] == False
    # Segundo registro: pagamento
    assert data[1]["paid"] == True
    assert data[1]["left"] == False
  
  def test_historico_ciclo_completo(self, veiculo_completo):
    """Cenário: Histórico completo (entrada, pagamento, saída) - deve ter 3 registros"""
    response = client.get(f"/parking/{veiculo_completo}")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    # Entrada
    assert data[0]["paid"] == False
    assert data[0]["left"] == False
    # Pagamento
    assert data[1]["paid"] == True
    assert data[1]["left"] == False
    # Saída
    assert data[2]["paid"] == True
    assert data[2]["left"] == True
  
  def test_historico_veiculo_nao_existe(self):
    """Cenário: Consultar histórico de veículo inexistente - deve retornar 404"""
    response = client.get("/parking/GHO-0000")
    
    assert response.status_code == 404
    assert "não encontrada no sistema" in response.json()["detail"]
  
  def test_historico_placa_invalida(self):
    """Cenário: Placa com formato inválido - deve retornar 422"""
    response = client.get("/parking/INVALIDA")
    
    assert response.status_code == 422
    assert "Formatação da placa incorreta" in response.json()["detail"]
