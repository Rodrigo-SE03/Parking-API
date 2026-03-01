"""Testes para o endpoint POST /parking/ (Entrada no estacionamento)
"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestEnterParkingLot:
  """Testes para entrada de veículos no estacionamento"""
  
  def test_entrada_sucesso(self):
    """Cenário: Primeira entrada de um veículo - deve retornar 201"""
    response = client.post("/parking/", json={"plate": "NEW-1000"})
    
    assert response.status_code == 201
    data = response.json()
    assert "id" in data  # Deve ter um ID
    assert isinstance(data["id"], int)  # ID deve ser número inteiro
    assert data["paid"] == False
    assert data["left"] == False
    assert "time" in data
  
  def test_entrada_placa_minuscula(self):
    """Cenário: Placa em minúscula deve ser convertida para maiúscula"""
    response = client.post("/parking/", json={"plate": "abc-9999"})
    
    assert response.status_code == 201
    # Verifica se foi salva corretamente consultando histórico
    history_response = client.get("/parking/ABC-9999")
    assert history_response.status_code == 200
  
  def test_entrada_placa_invalida_formato_errado(self):
    """Cenário: Placa com formato inválido - deve retornar 422"""
    placas_invalidas = [
        "INVALIDA",
        "AB-1234",
        "ABCD-123",
        "123-ABCD",
        "ABC1234",
        "ABC-12345",
        "aaaaaa",
        "######",
        "1234156"
    ]
    
    for placa in placas_invalidas:
      response = client.post("/parking/", json={"plate": placa})
      assert response.status_code == 422
      assert "Formatação da placa incorreta" in response.json()["detail"]
  
  def test_entrada_veiculo_ja_estacionado(self, veiculo_estacionado):
    """Cenário: Veículo tenta entrar mas já está dentro - deve retornar 409"""
    response = client.post("/parking/", json={"plate": veiculo_estacionado})
    
    assert response.status_code == 409
    assert "já está no estacionamento" in response.json()["detail"]
  
  def test_entrada_apos_ciclo_completo(self, veiculo_completo):
    """Cenário: Veículo que saiu pode entrar novamente - deve criar novo registro"""
    response = client.post("/parking/", json={"plate": veiculo_completo})
    
    assert response.status_code == 201
    data = response.json()
    assert data["paid"] == False
    assert data["left"] == False
  
  def test_entrada_sem_body(self):
    """Cenário: Requisição sem body - deve retornar 422"""
    response = client.post("/parking/")
    assert response.status_code == 422
  
  def test_entrada_body_vazio(self):
    """Cenário: Body sem campo 'plate' - deve retornar 422"""
    response = client.post("/parking/", json={})
    assert response.status_code == 422
