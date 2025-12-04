import time

def calcular_coste_tramo(tiempo_inicio, estado, tarifa_parado, tarifa_movimiento):
    """
    Calcula los datos de un tramo específico.
    Requiere las tarifas como argumentos para desacoplar la lógica de la config.
    """
    tiempo_actual = time.time()
    segundos_transcurridos = tiempo_actual - tiempo_inicio
    
    precio_actual = tarifa_movimiento if estado == "movimiento" else tarifa_parado
    coste_tramo = segundos_transcurridos * precio_actual
    
    return coste_tramo, segundos_transcurridos, tiempo_actual