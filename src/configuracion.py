import json
import os
import sys

ARCHIVO_CONFIG = 'config.json'

def cargar_configuracion():
    """Carga la configuración desde el archivo JSON."""
    if not os.path.exists(ARCHIVO_CONFIG):
        print(f"❌ Error crítico: No se encuentra {ARCHIVO_CONFIG}")
        sys.exit(1)
        
    try:
        with open(ARCHIVO_CONFIG, 'r') as f:
            config = json.load(f)
            return config
    except json.JSONDecodeError:
        print(f"❌ Error: {ARCHIVO_CONFIG} tiene un formato inválido.")
        sys.exit(1)