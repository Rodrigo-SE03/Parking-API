import sys
from pathlib import Path

# Adiciona o diretório 'app' ao path para imports funcionarem
app_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(app_dir))

import pytest
from app.db.mongo import get_collection
from fastapi.testclient import TestClient
from app.main import app

# Cliente de teste para todos os testes
client = TestClient(app)


# ========================
# FIXTURES (Dados Reutilizáveis)
# ========================

@pytest.fixture
def test_client():
  """Retorna o cliente de teste da API"""
  return client


@pytest.fixture
def placa_valida():
  """Retorna uma placa válida para testes"""
  return "ABC-1234"


@pytest.fixture
def veiculo_estacionado():
  """Fixture: Veículo que acabou de entrar no estacionamento"""
  placa = "EST-1111"
  client.post("/parking/", json={"plate": placa})
  return placa


@pytest.fixture
def veiculo_pago():
  """Fixture: Veículo que entrou e já pagou"""
  placa = "PAG-2222"
  client.post("/parking/", json={"plate": placa})
  client.put(f"/parking/{placa}/pay")
  return placa


@pytest.fixture
def veiculo_completo():
  """Fixture: Veículo que completou o ciclo (entrou, pagou e saiu)"""
  placa = "CMP-3333"
  client.post("/parking/", json={"plate": placa})
  client.put(f"/parking/{placa}/pay")
  client.put(f"/parking/{placa}/out")
  return placa


@pytest.fixture(autouse=True)
def limpar_banco():
  """Limpa o banco de dados antes de cada teste"""
  collection = get_collection()
  collection.delete_many({})
  yield
  # Limpeza após o teste
  collection.delete_many({})
