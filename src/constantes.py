from pathlib import Path

# --- Rutas del Sistema ---
# Se calcula dinámicamente para funcionar en cualquier SO
BASE_DIR = Path(__file__).resolve().parent.parent

ARCHIVO_USUARIOS = BASE_DIR / "users.json"
ARCHIVO_CONFIG = BASE_DIR / "config.json"
ARCHIVO_HISTORIAL = BASE_DIR / "history.txt"
ARCHIVO_LOG = BASE_DIR / "taximetro.log"

# --- Valores por Defecto (Fallback de Negocio) ---
TARIFA_PARADO_DEFAULT = 2.0      # céntimos/segundo
TARIFA_MOVIMIENTO_DEFAULT = 5.0  # céntimos/segundo
DEFAULT_MONEDA = "€"