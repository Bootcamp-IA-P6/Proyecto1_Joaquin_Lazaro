import pytest
import time
from unittest.mock import MagicMock, patch
from src.modelo import Taximetro, Trayecto, Estado
from src.configuracion import GestorConfiguracion

# --- FIXTURES (Datos de prueba reutilizables) ---

@pytest.fixture
def mock_config():
    """Crea un gestor de configuración falso (Mock) para no leer ficheros reales."""
    config = MagicMock(spec=GestorConfiguracion)
    config.get_tarifa.side_effect = lambda tipo: 2.0 if tipo == "parado" else 5.0
    config.moneda = "€"
    return config

@pytest.fixture
def taximetro(mock_config):
    """Instancia un taxímetro con la configuración mockeada."""
    return Taximetro(mock_config)

# --- TESTS DE CLASE TRAYECTO ---

def test_calculo_trayecto_parado():
    """Verifica que el cálculo en estado PARADO sea correcto (Tiempo * Tarifa)."""
    # Config: Tarifa Parado = 2.0
    trayecto = Trayecto(tarifa_parado=2.0, tarifa_movimiento=5.0)
    
    # Simulamos que pasa 1 segundo
    time.sleep(0.1) 
    # Forzamos los tiempos internos para ser deterministas y no depender del sleep real
    trayecto.inicio = 1000
    trayecto.ultimo_cambio = 1000
    
    # Simulamos cambio a los 10 segundos
    with patch('time.time', return_value=1010):
        coste, tiempo = trayecto.cambiar_estado(Estado.MOVIMIENTO)
    
    # Esperado: 10s * 2.0€ = 20€
    assert tiempo == 10
    assert coste == 20.0
    assert trayecto.coste_parado == 20.0
    assert trayecto.estado_actual == Estado.MOVIMIENTO

def test_calculo_trayecto_movimiento():
    """Verifica el cálculo en MOVIMIENTO."""
    # Config: Tarifa Movimiento = 5.0
    trayecto = Trayecto(tarifa_parado=2.0, tarifa_movimiento=5.0)
    
    # Setup inicial manual
    trayecto.estado_actual = Estado.MOVIMIENTO
    trayecto.ultimo_cambio = 1000
    
    # Simulamos avance de 5 segundos
    with patch('time.time', return_value=1005):
        coste, tiempo = trayecto.cambiar_estado(Estado.PARADO)
        
    # Esperado: 5s * 5.0€ = 25€
    assert tiempo == 5
    assert coste == 25.0
    assert trayecto.coste_movimiento == 25.0

def test_transicion_estado_invalida():
    """No se debe poder cambiar a Parado si ya estás Parado."""
    trayecto = Trayecto(1, 1)
    trayecto.estado_actual = Estado.PARADO
    
    with pytest.raises(ValueError):
        trayecto.cambiar_estado(Estado.PARADO)

# --- TESTS DE CLASE TAXIMETRO ---

def test_flujo_completo_taximetro(taximetro):
    """Prueba de integración de un viaje completo controlada por el Taxímetro."""
    # 1. Iniciar
    trayecto = taximetro.iniciar_carrera()
    assert trayecto.estado_actual == Estado.PARADO
    
    # Mockeamos el tiempo para simular:
    # Inicio: 0s
    # Cambio a Movimiento: 10s (Estuvo 10s parado) -> 10s * 2€ = 20€
    # Finalizar: 20s (Estuvo 10s en movimiento) -> 10s * 5€ = 50€
    # Total esperado: 70€
    
    trayecto.ultimo_cambio = 1000 # T=0
    
    # A) Cambiar a movimiento (T=1010)
    with patch('time.time', return_value=1010):
        taximetro.cambiar_estado("movimiento")
    
    assert trayecto.coste_parado == 20.0
    
    # B) Finalizar (T=1020)
    with patch('time.time', return_value=1020):
        # Mockear guardar_historial para que no escriba en disco real
        with patch('src.modelo.guardar_trayecto') as mock_guardar:
            mock_guardar.return_value = True
            resumen = taximetro.finalizar_carrera()
    
    # Validaciones Finales
    assert resumen.coste_movimiento == 50.0
    assert resumen.total_coste == 70.0 # 20 + 50
    assert resumen.total_tiempo == 20.0
    assert taximetro.trayecto_actual is None # Debe quedar libre

def test_error_cambio_sin_carrera(taximetro):
    """No se puede cambiar estado si no hay carrera iniciada."""
    with pytest.raises(RuntimeError):
        taximetro.cambiar_estado("movimiento")