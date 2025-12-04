import pytest
import json
from unittest.mock import mock_open, patch
from src.configuracion import GestorConfiguracion
from src.autenticacion import GestorAuth

class TestConfiguracion:
    def test_carga_defaults_si_falla_archivo(self):
        """Si no existe config.json, debe cargar defaults."""
        with patch("builtins.open", side_effect=FileNotFoundError):
            gestor = GestorConfiguracion()
            assert gestor.get_tarifa("parado") > 0
            assert gestor.get_tarifa("movimiento") > 0
            assert gestor.moneda == "€"

    def test_set_tarifa_valida(self):
        """Prueba que set_tarifa actualiza el valor y guarda."""
        # Simulamos lectura y escritura
        mock_file = mock_open(read_data='{}')
        with patch("builtins.open", mock_file):
            with patch("json.dump") as mock_json_dump:
                gestor = GestorConfiguracion()
                
                # Ejecutar cambio
                gestor.set_tarifa("parado", 3.50)
                
                # Verificar memoria
                assert gestor.get_tarifa("parado") == 3.50
                # Verificar que intentó guardar
                assert mock_json_dump.called

    def test_set_tarifa_negativa_error(self):
        """No se deben permitir tarifas negativas."""
        gestor = GestorConfiguracion()
        with pytest.raises(ValueError):
            gestor.set_tarifa("parado", -1.0)


class TestAutenticacion:
    def test_registro_y_login(self):
        """Flujo completo de registro y login exitoso."""
        # Mockeamos open para no tocar users.json real
        with patch("builtins.open", mock_open(read_data='{}')), \
             patch("src.autenticacion.GestorAuth._guardar_usuarios") as mock_guardar:
            
            auth = GestorAuth()
            
            # 1. Registro
            auth.registrar_usuario("testuser", "1234")
            assert "testuser" in auth.usuarios
            
            # 2. Login Correcto
            assert auth.login("testuser", "1234") is True
            assert auth.usuario_actual == "testuser"

    def test_login_fallido(self):
        """Login con contraseña incorrecta."""
        with patch("builtins.open", mock_open(read_data='{}')):
            auth = GestorAuth()
            auth.registrar_usuario("user", "password")
            
            assert auth.login("user", "WRONG_PASS") is False
            assert auth.usuario_actual is None