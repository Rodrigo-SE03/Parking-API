"""
Testes de Fluxos Completos
Testam cenários reais de uso da API com múltiplas operações
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestFluxosCompletos:
  """Testes de fluxos completos de uso da API"""
  
  def test_fluxo_completo_normal(self):
    """Cenário: Fluxo completo de sucesso (entrada → pagamento → saída)"""
    placa = "FLX-1111"
    
    # 1. Entrada
    entrada = client.post("/parking/", json={"plate": placa})
    assert entrada.status_code == 201
    parking_id = entrada.json()["id"]
    
    # 2. Pagamento
    pagamento = client.put(f"/parking/{placa}/pay")
    assert pagamento.status_code == 200
    assert pagamento.json()["id"] == parking_id
    
    # 3. Saída
    saida = client.put(f"/parking/{placa}/out")
    assert saida.status_code == 200
    assert saida.json()["id"] == parking_id
    
    # 4. Histórico completo
    historico = client.get(f"/parking/{placa}")
    assert historico.status_code == 200
    assert len(historico.json()) == 3
  
  def test_fluxo_reentrada_apos_saida(self):
    """Cenário: Veículo sai e entra novamente - deve criar novo registro"""
    placa = "REE-2222"
    
    # Primeiro ciclo
    client.post("/parking/", json={"plate": placa})
    client.put(f"/parking/{placa}/pay")
    client.put(f"/parking/{placa}/out")
    
    # Segundo ciclo
    entrada2 = client.post("/parking/", json={"plate": placa})
    assert entrada2.status_code == 201
    
    # O ID deve ser diferente (novo registro)
    # Como o código remove o registro anterior, o histórico é perdido
    historico = client.get(f"/parking/{placa}")
    assert historico.status_code == 200
    # Deve ter apenas 1 registro (da nova entrada)
    assert len(historico.json()) == 1
  
  def test_multiplos_veiculos_simultaneos(self):
    """Cenário: Múltiplos veículos no estacionamento ao mesmo tempo"""
    placas = ["MLT-1111", "MLT-2222", "MLT-3333"]
    
    # Todos entram
    for placa in placas:
        response = client.post("/parking/", json={"plate": placa})
        assert response.status_code == 201
    
    # Primeiro paga e sai
    client.put(f"/parking/{placas[0]}/pay")
    client.put(f"/parking/{placas[0]}/out")
    
    # Segundo só paga
    client.put(f"/parking/{placas[1]}/pay")
    
    # Terceiro não faz nada
    
    # Verifica históricos independentes
    h1 = client.get(f"/parking/{placas[0]}")
    assert len(h1.json()) == 3  # Completo
    
    h2 = client.get(f"/parking/{placas[1]}")
    assert len(h2.json()) == 2  # Entrada + pagamento
    
    h3 = client.get(f"/parking/{placas[2]}")
    assert len(h3.json()) == 1  # Só entrada
