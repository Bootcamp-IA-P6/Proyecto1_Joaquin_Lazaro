import logging
from typing import Optional

def leer_float_seguro(mensaje: str, permitir_negativos: bool = False, token_cancelar: str = 'c') -> Optional[float]:
    """
    Solicita un número decimal de forma robusta con logging y feedback específico.
    
    Args:
        mensaje: El prompt para el usuario.
        permitir_negativos: Valida si acepta valores < 0.
        token_cancelar: Token para abortar la operación.
    
    Returns:
        float: El valor validado.
        None: Si el usuario cancela.
    """
    while True:
        entrada = input(mensaje).strip()
        
        # 1. Chequeo de cancelación
        if entrada.lower() == token_cancelar.lower():
            logging.info("Input de usuario: Cancelación solicitada por el usuario.")
            return None
            
        try:
            # 2. Intento de conversión
            valor = float(entrada)
            
            # 3. Validación de negocio (negativos)
            if not permitir_negativos and valor < 0:
                msg = f"Intento inválido: Valor negativo ({valor})"
                print("⚠️  Error: El valor no puede ser negativo.")
                logging.warning(msg)
                continue
                
            return valor

        except ValueError:
            # 4. Manejo de errores específico (Feedback UX)
            if "," in entrada:
                msg_log = f"Error de formato: Usuario usó coma en '{entrada}'"
                msg_user = "❌ Formato incorrecto: Detectada una coma (,)."
                sugerencia = f"👉 Por favor, usa PUNTO (.) para decimales. Ejemplo: {entrada.replace(',', '.')}"
            else:
                msg_log = f"Error de tipo: '{entrada}' no es numérico"
                msg_user = f"❌ Error: '{entrada}' no es un número válido."
                sugerencia = "👉 Ejemplo correcto: 1.50 o 0.05"
            
            # Registrar y notificar
            logging.warning(msg_log)
            print(msg_user)
            print(sugerencia)