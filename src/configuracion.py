import json
import os

class GestorConfiguracion:
    ARCHIVO_CONFIG = 'config.json'
    DEFAULT_CONFIG = {
        "tarifa_parado": 0.02, 
        "tarifa_movimiento": 0.05, 
        "moneda": "€"
    }

    def __init__(self):
        self.config = self._cargar_configuracion()

    def _cargar_configuracion(self):
        """Carga la configuración o devuelve valores por defecto."""
        try:
            with open(self.ARCHIVO_CONFIG, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return self.DEFAULT_CONFIG.copy()

    def guardar_configuracion(self):
        """Persiste la configuración actual en disco."""
        try:
            with open(self.ARCHIVO_CONFIG, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Error guardando config: {e}")
            return False

    def get_tarifa(self, tipo):
        """Recupera una tarifa específica."""
        clave = f"tarifa_{tipo}"  # parado o movimiento
        return self.config.get(clave, 0.0)

    def set_tarifa(self, tipo, valor):
        """Actualiza una tarifa y guarda."""
        if valor < 0:
            raise ValueError("La tarifa no puede ser negativa")
        clave = f"tarifa_{tipo}"
        self.config[clave] = float(valor)
        return self.guardar_configuracion()

    @property
    def moneda(self):
        return self.config.get("moneda", "€")