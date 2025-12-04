import json
import logging
from typing import Dict, Any
from src.constantes import (
    ARCHIVO_CONFIG, 
    TARIFA_PARADO_DEFAULT, 
    TARIFA_MOVIMIENTO_DEFAULT, 
    DEFAULT_MONEDA
)

class GestorConfiguracion:
    def __init__(self):
        self.config: Dict[str, Any] = self._cargar_configuracion()

    def _cargar_configuracion(self) -> Dict[str, Any]:
        """Carga el JSON o usa defaults si falla."""
        defaults = {
            "tarifa_parado": TARIFA_PARADO_DEFAULT,
            "tarifa_movimiento": TARIFA_MOVIMIENTO_DEFAULT,
            "moneda": DEFAULT_MONEDA
        }
        try:
            with open(ARCHIVO_CONFIG, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return {**defaults, **data}
        except (FileNotFoundError, json.JSONDecodeError):
            logging.warning("Configuración no encontrada o corrupta. Usando defaults.")
            return defaults

    def guardar_configuracion(self) -> bool:
        """Escribe el estado actual de self.config en el archivo JSON."""
        try:
            with open(ARCHIVO_CONFIG, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            return True
        except IOError as e:
            logging.error(f"Error guardando config: {e}")
            return False

    def get_tarifa(self, tipo: str) -> float:
        """Obtiene una tarifa por su clave (ej: 'parado')."""
        clave = f"tarifa_{tipo}"
        return float(self.config.get(clave, 0.0))

    # --- ESTE ES EL MÉTODO QUE FALTABA ---
    def set_tarifa(self, tipo: str, valor: float) -> bool:
        """Actualiza una tarifa y guarda el cambio en disco."""
        if valor < 0:
            raise ValueError("La tarifa no puede ser negativa")
        
        clave = f"tarifa_{tipo}"
        self.config[clave] = float(valor)
        return self.guardar_configuracion()
    # -------------------------------------

    @property
    def moneda(self) -> str:
        return self.config.get("moneda", DEFAULT_MONEDA)