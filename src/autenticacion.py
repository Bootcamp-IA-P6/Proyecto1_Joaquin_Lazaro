import hashlib
import json
import secrets
import logging
import os
from typing import Dict, Optional
from src.constantes import ARCHIVO_USUARIOS

class GestorAuth:
    def __init__(self):
        self.usuarios: Dict[str, str] = self._cargar_usuarios()

    def _cargar_usuarios(self) -> Dict[str, str]:
        """Carga la base de datos de usuarios desde la constante."""
        if not os.path.exists(ARCHIVO_USUARIOS):
            logging.warning("Archivo de usuarios no encontrado. Se iniciará vacío.")
            return {}
        
        try:
            with open(ARCHIVO_USUARIOS, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logging.error(f"Error cargando usuarios: {e}")
            return {}

    def _guardar_usuarios(self) -> bool:
        """Persiste los usuarios en la ruta definida."""
        try:
            with open(ARCHIVO_USUARIOS, 'w', encoding='utf-8') as f:
                json.dump(self.usuarios, f, indent=4)
            return True
        except IOError as e:
            logging.error(f"Error guardando usuarios: {e}")
            return False

    # ... (El resto de métodos _generar_hash, registrar_usuario, login NO CAMBIAN) ...
    # Copia el resto de métodos tal cual los tenías en el paso anterior.
    def _generar_hash(self, password: str, salt: Optional[str] = None) -> str:
        if salt is None:
            salt = secrets.token_hex(16)
        input_str = salt + password
        hash_obj = hashlib.sha256(input_str.encode('utf-8'))
        return f"{salt}${hash_obj.hexdigest()}"

    def registrar_usuario(self, username: str, password: str) -> bool:
        if username in self.usuarios: return False
        self.usuarios[username] = self._generar_hash(password)
        return self._guardar_usuarios()

    def login(self, username: str, password: str) -> bool:
        if username not in self.usuarios: return False
        almacenado = self.usuarios[username]
        try:
            salt, _ = almacenado.split('$')
        except ValueError: return False
        check_hash = self._generar_hash(password, salt)
        return secrets.compare_digest(almacenado, check_hash)