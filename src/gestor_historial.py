import datetime
import logging # <--- IMPORTANTE
from typing import Any
from src.constantes import ARCHIVO_HISTORIAL

class GestorHistorial:
    def guardar(self, trayecto: Any, moneda: str) -> bool:
        linea = self._formatear_linea(trayecto, moneda)
        exito = self._escribir_linea(linea)
        
        if exito:
            logging.info("Historial actualizado correctamente.")
        else:
            logging.error("Fallo crítico al actualizar historial.")
            
        return exito

    def _formatear_linea(self, trayecto: Any, moneda: str) -> str:
        fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        duracion = trayecto.total_tiempo
        coste = trayecto.total_coste
        t_parado = trayecto.tarifa_parado
        t_mov = trayecto.tarifa_movimiento

        return (
            f"{fecha_hora} | "
            f"Tiempo: {duracion:.0f}s | "
            f"Tarifas: {t_parado:.2f}/{t_mov:.2f} ({moneda}/s) | "
            f"Total: {coste:.2f}{moneda}\n"
        )

    def _escribir_linea(self, linea: str) -> bool:
        try:
            with open(ARCHIVO_HISTORIAL, 'a', encoding='utf-8') as f:
                f.write(linea)
            return True
        except IOError as e:
            logging.error(f"Error IO en historial: {e}")
            return False