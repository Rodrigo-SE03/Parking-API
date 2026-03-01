"""Testes para o endpoint GET /parking/{id} (Histórico)
"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestGetHistory:
  """Testes para consulta de histórico por sessões"""
  
  def test_historico_apenas_entrada(self, veiculo_estacionado):
    """Cenário: Histórico de veículo que só entrou - deve ter 1 sessão ativa"""
    response = client.get(f"/parking/{veiculo_estacionado}")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["paid"] == False
    assert data[0]["left"] == False
    assert "time" in data[0]
  
  def test_historico_entrada_e_pagamento(self, veiculo_pago):
    """Cenário: Histórico de veículo que entrou e pagou - deve ter 1 sessão ativa com pagamento"""
    response = client.get(f"/parking/{veiculo_pago}")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["paid"] == True
    assert data[0]["left"] == False
    assert "time" in data[0]
  
  def test_historico_ciclo_completo(self, veiculo_completo):
    """Cenário: Histórico completo (entrada, pagamento, saída) - deve ter 1 sessão fechada"""
    response = client.get(f"/parking/{veiculo_completo}")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["paid"] == True
    assert data[0]["left"] == True
    assert "time" in data[0]
  
  def test_historico_multiplas_sessoes(self):
    """Cenário: Veículo que entrou, saiu e entrou novamente - deve ter 2 sessões"""
    placa = "MSS-1111"
    
    # Primeira sessão completa
    client.post("/parking/", json={"plate": placa})
    client.put(f"/parking/{placa}/pay")
    client.put(f"/parking/{placa}/out")
    
    # Segunda sessão (nova entrada)
    client.post("/parking/", json={"plate": placa})
    
    response = client.get(f"/parking/{placa}")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    # Primeira sessão: fechada
    assert data[0]["paid"] == True
    assert data[0]["left"] == True
    # Segunda sessão: ativa
    assert data[1]["paid"] == False
    assert data[1]["left"] == False
  
  def test_historico_tres_sessoes(self):
    """Cenário: Veículo com 3 sessões completas - histórico deve mostrar todas"""
    placa = "TRS-3333"
    
    # Sessão 1
    client.post("/parking/", json={"plate": placa})
    client.put(f"/parking/{placa}/pay")
    client.put(f"/parking/{placa}/out")
    
    # Sessão 2
    client.post("/parking/", json={"plate": placa})
    client.put(f"/parking/{placa}/pay")
    client.put(f"/parking/{placa}/out")
    
    # Sessão 3 (ativa)
    client.post("/parking/", json={"plate": placa})
    
    response = client.get(f"/parking/{placa}")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    # Primeiras duas: fechadas
    assert data[0]["left"] == True
    assert data[1]["left"] == True
    # Terceira: ativa
    assert data[2]["left"] == False
  
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
