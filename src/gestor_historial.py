import datetime
from typing import Any
from src.constantes import ARCHIVO_HISTORIAL

class GestorHistorial:

    def guardar(self, trayecto: Any, moneda: str) -> bool:
        """Orquesta el guardado del trayecto."""
        linea = self._formatear_linea(trayecto, moneda)
        return self._escribir_linea(linea)

    def _formatear_linea(self, trayecto: Any, moneda: str) -> str:
        """Construye la cadena de texto con el formato legible."""
        fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        duracion = trayecto.total_tiempo
        coste = trayecto.total_coste
        t_parado = trayecto.tarifa_parado
        t_mov = trayecto.tarifa_movimiento

        return (
            f"{fecha_hora} | "
            f"Tiempo: {duracion:.2f}s | "
            f"Tarifas: {t_parado:.2f}/{t_mov:.2f} ({moneda}/s) | "
            f"Total: {coste:.2f}{moneda}\n"
        )

    def _escribir_linea(self, linea: str) -> bool:
        """Maneja la I/O usando la ruta constante."""
        try:
            with open(ARCHIVO_HISTORIAL, 'a', encoding='utf-8') as f:
                f.write(linea)
            return True
        except IOError as e:
            print(f"❌ Error crítico escribiendo historial: {e}")
            return False