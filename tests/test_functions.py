"""Testes unitários para funções auxiliares (helper_functions)"""
from datetime import datetime, timedelta

import pytest
from fastapi import HTTPException

from app.parking.utils.helper_functions import get_interval_minutes, plate_validation


class TestPlateValidation:
    """Testes para validação de placas"""
    
    def test_placa_valida_maiuscula(self):
        """Cenário: Placa válida em maiúscula - deve retornar normalizada"""
        resultado = plate_validation("ABC-1234")
        assert resultado == "ABC-1234"
    
    def test_placa_valida_minuscula(self):
        """Cenário: Placa válida em minúscula - deve converter para maiúscula"""
        resultado = plate_validation("abc-1234")
        assert resultado == "ABC-1234"
    
    def test_placa_valida_mista(self):
        """Cenário: Placa com letras mistas - deve normalizar para maiúscula"""
        resultado = plate_validation("AbC-1234")
        assert resultado == "ABC-1234"
    
    def test_placa_invalida_formato_errado(self):
        """Cenário: Placa com formato inválido - deve lançar HTTPException"""
        with pytest.raises(HTTPException) as exc:
            plate_validation("aaaaaaaa")
        assert exc.value.status_code == 422
        assert "Formatação da placa incorreta" in exc.value.detail
    
    def test_placa_invalida_sem_hifen(self):
        """Cenário: Placa sem hífen - deve lançar HTTPException"""
        with pytest.raises(HTTPException) as exc:
            plate_validation("ABC1234")
        assert exc.value.status_code == 422
    
    def test_placa_invalida_poucos_caracteres(self):
        """Cenário: Placa com poucos caracteres - deve lançar HTTPException"""
        with pytest.raises(HTTPException) as exc:
            plate_validation("AB-123")
        assert exc.value.status_code == 422


class TestIntervalMinutes:
    """Testes para cálculo de intervalo em minutos"""
    
    def test_intervalo_45_minutos(self):
        """Cenário: Diferença de 45 minutos - deve retornar '45 minutes'"""
        inicio = datetime.now() - timedelta(minutes=45)
        fim = datetime.now()
        resultado = get_interval_minutes(inicio, fim)
        assert resultado == "45 minutes"
    
    def test_intervalo_1_minuto(self):
        """Cenário: Diferença de 1 minuto - deve retornar '1 minutes'"""
        inicio = datetime.now() - timedelta(minutes=1)
        fim = datetime.now()
        resultado = get_interval_minutes(inicio, fim)
        assert resultado == "1 minutes"
    
    def test_intervalo_60_minutos(self):
        """Cenário: Diferença de 60 minutos (1 hora) - deve retornar '60 minutes'"""
        inicio = datetime.now() - timedelta(minutes=60)
        fim = datetime.now()
        resultado = get_interval_minutes(inicio, fim)
        assert resultado == "60 minutes"
    
    def test_intervalo_zero_minutos(self):
        """Cenário: Sem diferença de tempo - deve retornar '0 minutes'"""
        agora = datetime.now()
        resultado = get_interval_minutes(agora, agora)
        assert resultado == "0 minutes"