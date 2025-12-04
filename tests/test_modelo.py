import pytest
import time
from unittest.mock import MagicMock, patch
from src.modelo import Taximetro, Trayecto, Estado

# Definimos tarifas de prueba para no depender del config.json real
TARIFA_PARADO = 2.0
TARIFA_MOVIMIENTO = 5.0

class TestTrayecto:
    @patch('src.modelo.time.time')
    def test_calculo_coste_basico(self, mock_time):
        """Verifica que el trayecto calcula bien el coste en parado y movimiento."""
        # 1. Inicio (T=0)
        mock_time.return_value = 1000.0 
        trayecto = Trayecto(TARIFA_PARADO, TARIFA_MOVIMIENTO)
        
        # 2. Pasan 10 segundos PARADO
        mock_time.return_value = 1010.0
        coste, tiempo, _ = trayecto._calcular_tramo_pendiente()
        
        assert tiempo == 10.0
        assert coste == 10.0 * TARIFA_PARADO  # 20.0

    @patch('src.modelo.time.time')
    def test_cambio_estados(self, mock_time):
        """Simula un viaje completo: Inicio -> Mover -> Parar -> Fin"""
        # T=0: Inicio (Parado por defecto)
        mock_time.return_value = 0.0
        trayecto = Trayecto(TARIFA_PARADO, TARIFA_MOVIMIENTO)
        
        # T=10: Arrancamos (Estuvo 10s parado)
        mock_time.return_value = 10.0
        trayecto.alternar_marcha() # Cambia a MOVIMIENTO
        
        assert trayecto.tiempo_parado == 10.0
        assert trayecto.coste_parado == 20.0 # 10s * 2€
        assert trayecto.estado_actual == Estado.MOVIMIENTO

        # T=30: Frenamos (Estuvo 20s en movimiento)
        mock_time.return_value = 30.0
        trayecto.alternar_marcha() # Cambia a PARADO
        
        assert trayecto.tiempo_movimiento == 20.0
        assert trayecto.coste_movimiento == 100.0 # 20s * 5€
        assert trayecto.estado_actual == Estado.PARADO

        # T=40: Finalizamos (Estuvo 10s parado extra)
        mock_time.return_value = 40.0
        trayecto.finalizar()

        # Verificaciones finales
        assert trayecto.total_tiempo == 40.0
        # Coste total: 20 (inicio) + 100 (marcha) + 20 (final) = 140
        assert trayecto.total_coste == 140.0


class TestTaximetroFacade:
    def test_ciclo_vida_taximetro(self):
        """Prueba la integración del controlador Taximetro con mocks."""
        # Mockeamos las dependencias para no escribir en disco real
        mock_conf = MagicMock()
        mock_conf.get_tarifa.side_effect = lambda k: 2.0 if k == "parado" else 5.0
        mock_conf.moneda = "€"
        
        mock_hist = MagicMock()
        
        taxi = Taximetro(mock_conf, mock_hist)
        
        # 1. Iniciar
        taxi.iniciar_trayecto()
        assert taxi.en_trayecto is True
        assert taxi.estado_carrera == "parado" # type: ignore
        
        # 2. Finalizar
        resumen = taxi.finalizar_trayecto()
        
        assert taxi.en_trayecto is False
        assert resumen is not None
        # Verificar que se llamó al historial para guardar
        mock_hist.guardar.assert_called_once()