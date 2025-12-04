import time
import logging
from enum import Enum
from typing import Tuple, Optional

class Estado(Enum):
    PARADO = "parado"
    MOVIMIENTO = "movimiento"
    FINALIZADO = "finalizado"

class Trayecto:
    def __init__(self, tarifa_parado: float, tarifa_movimiento: float):
        self.tarifa_parado = tarifa_parado
        self.tarifa_movimiento = tarifa_movimiento
        
        self.inicio = time.time()
        self.ultimo_cambio = self.inicio
        self.estado_actual = Estado.PARADO
        
        self.tiempo_parado = 0.0
        self.tiempo_movimiento = 0.0
        self.coste_parado = 0.0
        self.coste_movimiento = 0.0

    def _calcular_tramo_pendiente(self) -> Tuple[float, float, float]:
        ahora = time.time()
        tiempo_tramo = ahora - self.ultimo_cambio
        coste_tramo = 0.0

        if self.estado_actual == Estado.PARADO:
            coste_tramo = tiempo_tramo * self.tarifa_parado
        elif self.estado_actual == Estado.MOVIMIENTO:
            coste_tramo = tiempo_tramo * self.tarifa_movimiento
            
        return coste_tramo, tiempo_tramo, ahora

    def alternar_marcha(self) -> Estado:
        if self.estado_actual == Estado.FINALIZADO:
            return self.estado_actual

        coste, tiempo, ahora = self._calcular_tramo_pendiente()
        
        if self.estado_actual == Estado.PARADO:
            self.tiempo_parado += tiempo
            self.coste_parado += coste
            nuevo_estado = Estado.MOVIMIENTO
        else:
            self.tiempo_movimiento += tiempo
            self.coste_movimiento += coste
            nuevo_estado = Estado.PARADO

        self.ultimo_cambio = ahora
        self.estado_actual = nuevo_estado
        return self.estado_actual

    def finalizar(self):
        if self.estado_actual != Estado.FINALIZADO:
            coste, tiempo, _ = self._calcular_tramo_pendiente()
            if self.estado_actual == Estado.PARADO:
                self.tiempo_parado += tiempo
                self.coste_parado += coste
            else:
                self.tiempo_movimiento += tiempo
                self.coste_movimiento += coste
            
            self.estado_actual = Estado.FINALIZADO

    def obtener_totales_tiempo_real(self) -> Tuple[float, float]:
        if self.estado_actual == Estado.FINALIZADO:
            return self.total_tiempo, self.total_coste

        coste_p, tiempo_p, _ = self._calcular_tramo_pendiente()
        return (self.total_tiempo + tiempo_p, self.total_coste + coste_p)

    @property
    def total_tiempo(self) -> float:
        return self.tiempo_parado + self.tiempo_movimiento

    @property
    def total_coste(self) -> float:
        return self.coste_parado + self.coste_movimiento


class Taximetro:
    def __init__(self, gestor_config, gestor_historial):
        self.config = gestor_config
        self.historial = gestor_historial
        self.trayecto_actual: Optional[Trayecto] = None

    @property
    def en_trayecto(self) -> bool:
        return self.trayecto_actual is not None

    @property
    def estado_carrera(self) -> str:
        """Propiedad necesaria para los tests y observación de estado."""
        if not self.trayecto_actual:
            return "LIBRE"
        return self.trayecto_actual.estado_actual.value

    def iniciar_trayecto(self):
        t_parado = self.config.get_tarifa("parado")
        t_mov = self.config.get_tarifa("movimiento")
        
        logging.info(f"INICIO DE CARRERA. Tarifas aplicadas: Parado={t_parado}, Mov={t_mov}")
        
        self.trayecto_actual = Trayecto(t_parado, t_mov)

    def alternar_estado_movimiento(self):
        if self.trayecto_actual:
            nuevo_estado = self.trayecto_actual.alternar_marcha()
            
            logging.info(f"CAMBIO DE ESTADO: El taxi ahora está {nuevo_estado.name} (T={self.trayecto_actual.total_tiempo:.1f}s)")
            
            return nuevo_estado

    def finalizar_trayecto(self) -> Trayecto:
        if not self.trayecto_actual:
            logging.warning("Intento de finalizar carrera sin trayecto activo.")
            return None # type: ignore
        
        trayecto_cerrado = self.trayecto_actual
        trayecto_cerrado.finalizar()
        
        logging.info(f"FIN DE CARRERA. Total: {trayecto_cerrado.total_coste:.2f} {self.config.moneda}. Tiempo: {trayecto_cerrado.total_tiempo:.2f}s")
        
        self.historial.guardar(trayecto_cerrado, self.config.moneda)
        
        self.trayecto_actual = None
        return trayecto_cerrado

    def obtener_info_tiempo_real(self) -> Tuple[float, float]:
        if self.trayecto_actual:
            return self.trayecto_actual.obtener_totales_tiempo_real()
        return 0.0, 0.0