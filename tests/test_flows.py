"""Testes de Fluxos Completos

Testam cenários reais de uso da API com múltiplas operações
"""
from fastapi.testclient import TestClient

from app.main import app

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
    
    # 4. Histórico deve ter apenas 1 sessão completa (fechada)
    historico = client.get(f"/parking/{placa}")
    assert historico.status_code == 200
    data = historico.json()
    assert len(data) == 1
    assert data[0]["paid"]
    assert data[0]["left"]
  
  def test_fluxo_reentrada_apos_saida(self):
    """Cenário: Veículo sai e entra novamente - deve criar nova sessão"""
    placa = "REE-2222"
    
    # Primeiro ciclo completo
    client.post("/parking/", json={"plate": placa})
    first_id = client.get(f"/parking/{placa}").json()[0]["id"]
    client.put(f"/parking/{placa}/pay")
    client.put(f"/parking/{placa}/out")
    
    # Segunda entrada
    entrada2 = client.post("/parking/", json={"plate": placa})
    assert entrada2.status_code == 201
    second_id = entrada2.json()["id"]
    
    # IDs devem ser diferentes (sessões separadas)
    assert second_id != first_id
    
    # Histórico deve ter 2 sessões
    historico = client.get(f"/parking/{placa}")
    assert historico.status_code == 200
    data = historico.json()
    assert len(data) == 2
    
    # Primeira sessão: fechada
    assert data[0]["id"] == first_id
    assert data[0]["paid"]
    assert data[0]["left"]
    
    # Segunda sessão: ativa
    assert data[1]["id"] == second_id
    assert not data[1]["paid"]
    assert not data[1]["left"]
  
  def test_fluxo_ciclo_multiplo(self):
    """Cenário: Veículo completa 3 ciclos completos"""
    placa = "CIC-3333"
    ids = []
    
    for _ in range(3):
      # Entra
      entrada = client.post("/parking/", json={"plate": placa})
      assert entrada.status_code == 201
      ids.append(entrada.json()["id"])
      
      # Paga e sai
      client.put(f"/parking/{placa}/pay")
      client.put(f"/parking/{placa}/out")
    
    # Histórico deve ter 3 sessões, todas fechadas
    historico = client.get(f"/parking/{placa}")
    assert historico.status_code == 200
    data = historico.json()
    assert len(data) == 3
    
    for i, sessao in enumerate(data):
      assert sessao["id"] == ids[i]
      assert sessao["paid"]
      assert sessao["left"]
  
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
    data1 = h1.json()
    assert len(data1) == 1  # 1 sessão fechada
    assert data1[0]["paid"]
    assert data1[0]["left"]
    
    h2 = client.get(f"/parking/{placas[1]}")
    data2 = h2.json()
    assert len(data2) == 1  # 1 sessão ativa com pagamento
    assert data2[0]["paid"]
    assert not data2[0]["left"]
    
    h3 = client.get(f"/parking/{placas[2]}")
    data3 = h3.json()
    assert len(data3) == 1  # 1 sessão ativa sem pagamento
    assert not data3[0]["paid"]
    assert not data3[0]["left"]
  
  def test_fluxo_sessao_ativa_mantem_tempo_dinamico(self):
    """Cenário: Sessão ativa deve mostrar tempo dinâmico (calculado até agora)"""
    placa = "DIN-4444"
    
    # Entra
    client.post("/parking/", json={"plate": placa})
    
    # Consulta histórico múltiplas vezes
    h1 = client.get(f"/parking/{placa}")
    time1 = h1.json()[0]["time"]
    
    # Segunda consulta (tempo deve ser diferente ou igual se for muito rápido)
    h2 = client.get(f"/parking/{placa}")
    time2 = h2.json()[0]["time"]
    
    # Ambas devem ter tempo válido
    assert "minutes" in time1
    assert "minutes" in time2
    assert not h1.json()[0]["left"]  # Ainda não saiu
