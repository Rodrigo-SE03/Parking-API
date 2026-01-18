"""
Testes para o endpoint DELETE /parking/{id} (Remoção de registros)
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestDeleteItem:
  """Testes para remoção de registros"""
  
  def test_delete_sucesso(self, veiculo_estacionado):
    """Cenário: Remover registro existente - deve retornar 204"""
    response = client.delete(f"/parking/{veiculo_estacionado}")
    
    assert response.status_code == 204
    
    # Verifica que realmente foi removido
    history_response = client.get(f"/parking/{veiculo_estacionado}")
    assert history_response.status_code == 404
  
  def test_delete_veiculo_nao_existe(self):
    """Cenário: Tentar remover veículo inexistente - deve retornar 404"""
    response = client.delete("/parking/GHO-0000")
    
    assert response.status_code == 404
  
  def test_delete_placa_invalida(self):
    """Cenário: Placa com formato inválido - deve retornar 422"""
    response = client.delete("/parking/INVALIDA")
    
    assert response.status_code == 422
    assert "Formatação da placa incorreta" in response.json()["detail"]
