import json
from src.constantes import (
    ARCHIVO_CONFIG, 
    DEFAULT_TARIFA_PARADO, 
    DEFAULT_TARIFA_MOVIMIENTO, 
    DEFAULT_MONEDA
)

class GestorConfiguracion:
    def __init__(self):
        self.config = self._cargar_configuracion()

    def _cargar_configuracion(self):
        """Carga la configuración o devuelve valores por defecto desde constantes."""
        try:
            with open(ARCHIVO_CONFIG, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                "tarifa_parado": DEFAULT_TARIFA_PARADO,
                "tarifa_movimiento": DEFAULT_TARIFA_MOVIMIENTO,
                "moneda": DEFAULT_MONEDA
            }

    def guardar_configuracion(self):
        try:
            with open(ARCHIVO_CONFIG, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Error guardando config: {e}")
            return False

    def get_tarifa(self, tipo):
        clave = f"tarifa_{tipo}"
        return self.config.get(clave, 0.0)

    def set_tarifa(self, tipo, valor):
        if valor < 0:
            raise ValueError("La tarifa no puede ser negativa")
        clave = f"tarifa_{tipo}"
        self.config[clave] = float(valor)
        return self.guardar_configuracion()

    @property
    def moneda(self):
        return self.config.get("moneda", DEFAULT_MONEDA)