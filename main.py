import logging
import tkinter as tk
import sys

from src.constantes import ARCHIVO_LOG
from src.configuracion import GestorConfiguracion
from src.gestor_historial import GestorHistorial
from src.autenticacion import GestorAuth
from src.modelo import Taximetro
from src.gui import AplicacionGUI

# Configuración de Logging Global
logging.basicConfig(
    filename=ARCHIVO_LOG,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def main():
    """Punto de entrada principal de la aplicación GUI."""
    logging.info("=== INICIO DE SESIÓN TAXÍMETRO (GUI) ===")

    # 1. Inicialización de capas de persistencia y configuración
    try:
        conf = GestorConfiguracion()
        hist = GestorHistorial()
        auth = GestorAuth()
    except Exception as e:
        logging.critical(f"Error inicializando componentes base: {e}")
        sys.exit(1)

    # 2. Inicialización de lógica de negocio (Inyección de dependencias)
    taxi = Taximetro(conf, hist)

    # 3. Inicialización de Interfaz Gráfica
    root = tk.Tk()
    
    # Inyectamos todas las dependencias en la GUI
    app = AplicacionGUI(root, auth, taxi, conf)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        logging.info("Interrupción de teclado detectada. Cerrando app.")
    except Exception as e:
        logging.error(f"Error no controlado en GUI: {e}")
    finally:
        logging.info("=== CIERRE DE APLICACIÓN ===")

if __name__ == "__main__":
    main()